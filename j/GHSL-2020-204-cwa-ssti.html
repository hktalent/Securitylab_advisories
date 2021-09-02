<header class="post-header d-block mb-6">
      <div class="date text-mono f5 my-3">December 3, 2020</div>
      <h1 class="my-2 h00-mktg lh-condensed">GHSL-2020-204: Server-Side Template Injection in Corona Warn App Server</h1>

      
      
      
      
      

      

      <a target="_blank" class="sc-frDJqD SgxRc d-inline-flex flex-row flex-items-center text-gray" href="https://github.com/pwntester">
        <img class="mr-3" src="https://avatars.githubusercontent.com/u/125701?s=35" height="35" width="35">
        <span>Alvaro Munoz</span>
      </a>
    </header>

    <main id="content" class="markdown-body" aria-label="Content">
      <h2 id="summary">Summary</h2>

<p>A Server-Side Template Injection was identified in Corona Warn App Server enabling attackers to inject arbitrary Java EL expressions, leading to un-auth Remote Code Execution (RCE) vulnerability.</p>

<h2 id="product">Product</h2>

<p>Corona Warn App Server</p>

<h2 id="tested-version">Tested Version</h2>

<p>latest commit to the date of testing: 3fd6baf</p>

<h2 id="details">Details</h2>

<h3 id="remote-code-execution---javael-injection">Remote Code Execution - JavaEL Injection</h3>

<p>It is possible to run arbitrary code on the server (with Submission service account privileges) by injecting arbitrary Java Expression Language (EL) expressions.</p>

<p>Submission server uses Java Bean Validation (JSR 380) custom constraint validators such as  <a href="https://github.com/corona-warn-app/cwa-server/blob/ee30b89ecf0aa431876c30b822334af15b22ddbe/services/submission/src/main/java/app/coronawarn/server/services/submission/validation/ValidSubmissionPayload.java"><code class="language-plaintext highlighter-rouge">ValidSubmissionPayload</code></a>:
When building custom constraint violation error messages, it is important to understand that they support different types of interpolation, including <a href="https://docs.jboss.org/hibernate/validator/5.1/reference/en-US/html/chapter-message-interpolation.html#section-interpolation-with-message-expressions">Java EL expressions</a>. Therefore if an attacker can inject arbitrary data in the error message template being passed to <code class="language-plaintext highlighter-rouge">ConstraintValidatorContext.buildConstraintViolationWithTemplate()</code> argument, they will be able to run arbitrary Java code. Unfortunately, it is common that validated (and therefore, normally untrusted) bean properties flow into the custom error message. In this case there are, at least, two paths where attacker controlled strings are included in custom constraint error validation messages:</p>

<div class="language-java highlighter-rouge"><div class="highlight"><pre class="highlight"><code>    <span class="kd">private</span> <span class="kt">boolean</span> <span class="nf">checkVisitedCountriesAreValid</span><span class="o">(</span><span class="nc">SubmissionPayload</span> <span class="n">submissionPayload</span><span class="o">,</span>
        <span class="nc">ConstraintValidatorContext</span> <span class="n">validatorContext</span><span class="o">)</span> <span class="o">{</span>
      <span class="k">if</span> <span class="o">(</span><span class="n">submissionPayload</span><span class="o">.</span><span class="na">getVisitedCountriesList</span><span class="o">().</span><span class="na">isEmpty</span><span class="o">())</span> <span class="o">{</span>
        <span class="k">return</span> <span class="kc">true</span><span class="o">;</span>
      <span class="o">}</span>
      <span class="nc">Collection</span><span class="o">&lt;</span><span class="nc">String</span><span class="o">&gt;</span> <span class="n">invalidVisitedCountries</span> <span class="o">=</span> <span class="n">submissionPayload</span><span class="o">.</span><span class="na">getVisitedCountriesList</span><span class="o">().</span><span class="na">stream</span><span class="o">()</span>
          <span class="o">.</span><span class="na">filter</span><span class="o">(</span><span class="n">not</span><span class="o">(</span><span class="nl">supportedCountries:</span><span class="o">:</span><span class="n">contains</span><span class="o">)).</span><span class="na">collect</span><span class="o">(</span><span class="n">toList</span><span class="o">());</span>

      <span class="k">if</span> <span class="o">(!</span><span class="n">invalidVisitedCountries</span><span class="o">.</span><span class="na">isEmpty</span><span class="o">())</span> <span class="o">{</span>
        <span class="n">invalidVisitedCountries</span><span class="o">.</span><span class="na">forEach</span><span class="o">(</span><span class="n">country</span> <span class="o">-&gt;</span> <span class="n">addViolation</span><span class="o">(</span><span class="n">validatorContext</span><span class="o">,</span>
            <span class="s">"["</span> <span class="o">+</span> <span class="n">country</span> <span class="o">+</span> <span class="s">"]: Visited country is not part of the supported countries list"</span><span class="o">));</span>
      <span class="o">}</span>
      <span class="k">return</span> <span class="n">invalidVisitedCountries</span><span class="o">.</span><span class="na">isEmpty</span><span class="o">();</span>
    <span class="o">}</span>
</code></pre></div></div>

<p>and</p>

<div class="language-java highlighter-rouge"><div class="highlight"><pre class="highlight"><code>    <span class="kd">private</span> <span class="kt">boolean</span> <span class="nf">checkOriginCountryIsValid</span><span class="o">(</span><span class="nc">SubmissionPayload</span> <span class="n">submissionPayload</span><span class="o">,</span>
        <span class="nc">ConstraintValidatorContext</span> <span class="n">validatorContext</span><span class="o">)</span> <span class="o">{</span>
      <span class="nc">String</span> <span class="n">originCountry</span> <span class="o">=</span> <span class="n">submissionPayload</span><span class="o">.</span><span class="na">getOrigin</span><span class="o">();</span>
      <span class="k">if</span> <span class="o">(</span><span class="n">submissionPayload</span><span class="o">.</span><span class="na">hasOrigin</span><span class="o">()</span> <span class="o">&amp;&amp;</span> <span class="o">!</span><span class="n">originCountry</span><span class="o">.</span><span class="na">isEmpty</span><span class="o">()</span>
          <span class="o">&amp;&amp;</span> <span class="o">!</span><span class="n">supportedCountries</span><span class="o">.</span><span class="na">contains</span><span class="o">(</span><span class="n">originCountry</span><span class="o">))</span> <span class="o">{</span>
        <span class="n">addViolation</span><span class="o">(</span><span class="n">validatorContext</span><span class="o">,</span> <span class="nc">String</span><span class="o">.</span><span class="na">format</span><span class="o">(</span>
            <span class="s">"Origin country %s is not part of the supported countries list"</span><span class="o">,</span> <span class="n">originCountry</span><span class="o">));</span>
        <span class="k">return</span> <span class="kc">false</span><span class="o">;</span>
      <span class="o">}</span>
      <span class="k">return</span> <span class="kc">true</span><span class="o">;</span>
    <span class="o">}</span>
</code></pre></div></div>

<p>The <code class="language-plaintext highlighter-rouge">ValidSubmissionPayload</code> annotation is used to validate data received by the Submission service controller exposed in <code class="language-plaintext highlighter-rouge">/version/v1/diagnosis-keys</code>:</p>

<div class="language-java highlighter-rouge"><div class="highlight"><pre class="highlight"><code>  <span class="cm">/**
   * Handles diagnosis key submission requests.
   *
   * @param exposureKeys The unmarshalled protocol buffers submission payload.
   * @param tan          A tan for diagnosis verification.
   * @return An empty response body.
   */</span>
  <span class="nd">@PostMapping</span><span class="o">(</span><span class="n">value</span> <span class="o">=</span> <span class="no">SUBMISSION_ROUTE</span><span class="o">,</span> <span class="n">headers</span> <span class="o">=</span> <span class="o">{</span><span class="s">"cwa-fake=0"</span><span class="o">})</span>
  <span class="nd">@Timed</span><span class="o">(</span><span class="n">description</span> <span class="o">=</span> <span class="s">"Time spent handling submission."</span><span class="o">)</span>
  <span class="kd">public</span> <span class="nc">DeferredResult</span><span class="o">&lt;</span><span class="nc">ResponseEntity</span><span class="o">&lt;</span><span class="nc">Void</span><span class="o">&gt;&gt;</span> <span class="nf">submitDiagnosisKey</span><span class="o">(</span>
      <span class="nd">@ValidSubmissionPayload</span> <span class="nd">@RequestBody</span> <span class="nc">SubmissionPayload</span> <span class="n">exposureKeys</span><span class="o">,</span>
      <span class="nd">@RequestHeader</span><span class="o">(</span><span class="s">"cwa-authorization"</span><span class="o">)</span> <span class="nc">String</span> <span class="n">tan</span><span class="o">)</span> <span class="o">{</span>
    <span class="n">submissionMonitor</span><span class="o">.</span><span class="na">incrementRequestCounter</span><span class="o">();</span>
    <span class="n">submissionMonitor</span><span class="o">.</span><span class="na">incrementRealRequestCounter</span><span class="o">();</span>
    <span class="k">return</span> <span class="nf">buildRealDeferredResult</span><span class="o">(</span><span class="n">exposureKeys</span><span class="o">,</span> <span class="n">tan</span><span class="o">);</span>
  <span class="o">}</span>
</code></pre></div></div>

<p><a href="https://github.com/corona-warn-app/cwa-server/blob/master/services/submission/src/main/java/app/coronawarn/server/services/submission/config/SecurityConfig.java">Spring security policies</a> are defined to protect the endpoints but, in this case, all requests to the Submission endpoint are allowed with no authentication/authorization:</p>

<div class="language-java highlighter-rouge"><div class="highlight"><pre class="highlight"><code>  <span class="kd">protected</span> <span class="kt">void</span> <span class="nf">configure</span><span class="o">(</span><span class="nc">HttpSecurity</span> <span class="n">http</span><span class="o">)</span> <span class="kd">throws</span> <span class="nc">Exception</span> <span class="o">{</span>
    <span class="n">http</span><span class="o">.</span><span class="na">authorizeRequests</span><span class="o">()</span>
        <span class="o">.</span><span class="na">mvcMatchers</span><span class="o">(</span><span class="nc">HttpMethod</span><span class="o">.</span><span class="na">GET</span><span class="o">,</span> <span class="no">HEALTH_ROUTE</span><span class="o">,</span> <span class="no">PROMETHEUS_ROUTE</span><span class="o">,</span> <span class="no">READINESS_ROUTE</span><span class="o">,</span> <span class="no">LIVENESS_ROUTE</span><span class="o">).</span><span class="na">permitAll</span><span class="o">()</span>
        <span class="o">.</span><span class="na">mvcMatchers</span><span class="o">(</span><span class="nc">HttpMethod</span><span class="o">.</span><span class="na">POST</span><span class="o">,</span> <span class="no">SUBMISSION_ROUTE</span><span class="o">).</span><span class="na">permitAll</span><span class="o">()</span>
        <span class="o">.</span><span class="na">anyRequest</span><span class="o">().</span><span class="na">denyAll</span><span class="o">()</span>
        <span class="o">.</span><span class="na">and</span><span class="o">().</span><span class="na">csrf</span><span class="o">().</span><span class="na">disable</span><span class="o">();</span>
    <span class="n">http</span><span class="o">.</span><span class="na">headers</span><span class="o">().</span><span class="na">contentSecurityPolicy</span><span class="o">(</span><span class="s">"default-src 'self'"</span><span class="o">);</span>
  <span class="o">}</span>
</code></pre></div></div>

<h4 id="impact">Impact</h4>

<p>This issue leads to Remote Code execution</p>

<h2 id="coordinated-disclosure-timeline">Coordinated Disclosure Timeline</h2>

<ul>
  <li>10/21/2020: Reported through SAP Trust Center</li>
  <li>10/22/2020: Issue reception is acknowledged</li>
  <li>10/23/2020: Issue is <a href="https://github.com/corona-warn-app/cwa-server/pull/922">fixed</a> in public repo</li>
  <li>10/28/2020: SAP confirms that the issue is fixed in release 1.5.1 which was deployed on 10/27/2020. SAP also informs GHSL that <a href="https://www.bsi.bund.de/DE/Home/home_node.html">BSI (Bundesamt für Sicherheit in der Informationstechnik</a> is currently testing the fix and asks to keep the issue confidential till BSI has done their tests and has confirmed that the fix is okay.</li>
  <li>11/01/2020: A more robust <a href="https://github.com/corona-warn-app/cwa-server/pull/945/">fix</a> is merged.</li>
  <li>11/09/2020: SAP told us that BSI has confirmed the fix.</li>
</ul>

<h2 id="resources">Resources</h2>

<p>SAP ID SR-20-00362</p>

<h2 id="credit">Credit</h2>

<p>This issue was discovered and reported by GHSL team member <a href="https://github.com/pwntester">@pwntester (Alvaro Muñoz)</a>.</p>

<h2 id="contact">Contact</h2>

<p>You can contact the GHSL team at <code class="language-plaintext highlighter-rouge">securitylab@github.com</code>, please include a reference to <code class="language-plaintext highlighter-rouge">GHSL-2020-204</code> in any communication regarding this issue.</p>

  