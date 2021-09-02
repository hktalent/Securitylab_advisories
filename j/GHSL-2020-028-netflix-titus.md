<header class="post-header d-block mb-6">
      <div class="date text-mono f5 my-3">March 25, 2020</div>
      <h1 class="my-2 h00-mktg lh-condensed">GHSL-2020-028: Server-Side Template Injection in Netflix Titus</h1>

      
      
      
      
      

      

      <a target="_blank" class="sc-frDJqD SgxRc d-inline-flex flex-row flex-items-center text-gray" href="https://github.com/pwntester">
        <img class="mr-3" src="https://avatars.githubusercontent.com/u/125701?s=35" height="35" width="35">
        <span>Alvaro Munoz</span>
      </a>
    </header>

    <main id="content" class="markdown-body" aria-label="Content">
      <h2 id="summary">Summary</h2>

<p>A Server-Side Template Injection was identified in Netflix Titus enabling attackers to inject arbitrary Java EL expressions, leading to a pre-auth Remote Code Execution (RCE) vulnerability.</p>

<h2 id="cve">CVE</h2>

<p>CVE-2020-9297</p>

<h2 id="product">Product</h2>

<p>Netflix Titus</p>

<h2 id="tested-version">Tested Version</h2>

<p>v0.1.1-rc.263</p>

<h2 id="issues-found">Issues found</h2>

<h3 id="ghsl-2020-028-details---remote-code-execution---javael-injection">GHSL-2020-028 Details - Remote Code Execution - JavaEL Injection</h3>

<p>It is possible to run arbitrary code on the server (with Titus service account privileges) by injecting arbitrary Java Expression Language (EL) expressions.</p>

<p>Netflix Titus uses Java Bean Validation (JSR 380) custom constraint validators such as <code class="language-plaintext highlighter-rouge">com.netflix.titus.api.jobmanager.model.job.sanitizer.SchedulingConstraintSetValidator</code>
When building custom constraint violation error messages, it is important to understand that they support different types of interpolation, including <a href="https://docs.jboss.org/hibernate/validator/5.1/reference/en-US/html/chapter-message-interpolation.html#section-interpolation-with-message-expressions">Java EL expressions</a>. Therefore if an attacker can inject arbitrary data in the error message template being passed to <code class="language-plaintext highlighter-rouge">ConstraintValidatorContext.buildConstraintViolationWithTemplate()</code> argument, they will be able to run arbitrary Java code. Unfortunately, it is common that validated (and therefore, normally untrusted) bean properties flow into the custom error message.</p>

<div class="language-java highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="nd">@Override</span>
<span class="kd">public</span> <span class="kt">boolean</span> <span class="nf">isValid</span><span class="o">(</span><span class="nc">Container</span> <span class="n">container</span><span class="o">,</span> <span class="nc">ConstraintValidatorContext</span> <span class="n">context</span><span class="o">)</span> <span class="o">{</span>
    <span class="k">if</span> <span class="o">(</span><span class="n">container</span> <span class="o">==</span> <span class="kc">null</span><span class="o">)</span> <span class="o">{</span>
        <span class="k">return</span> <span class="kc">true</span><span class="o">;</span>
    <span class="o">}</span>
    <span class="nc">Set</span><span class="o">&lt;</span><span class="nc">String</span><span class="o">&gt;</span> <span class="n">common</span> <span class="o">=</span> <span class="k">new</span> <span class="nc">HashSet</span><span class="o">&lt;&gt;(</span><span class="n">container</span><span class="o">.</span><span class="na">getSoftConstraints</span><span class="o">().</span><span class="na">keySet</span><span class="o">());</span>
    <span class="n">common</span><span class="o">.</span><span class="na">retainAll</span><span class="o">(</span><span class="n">container</span><span class="o">.</span><span class="na">getHardConstraints</span><span class="o">().</span><span class="na">keySet</span><span class="o">());</span>
    <span class="k">if</span> <span class="o">(</span><span class="n">common</span><span class="o">.</span><span class="na">isEmpty</span><span class="o">())</span> <span class="o">{</span>
        <span class="k">return</span> <span class="kc">true</span><span class="o">;</span>
    <span class="o">}</span>
    <span class="n">context</span><span class="o">.</span><span class="na">buildConstraintViolationWithTemplate</span><span class="o">(</span>
            <span class="s">"Soft and hard constraints not unique. Shared constraints: "</span> <span class="o">+</span> <span class="n">common</span>
    <span class="o">).</span><span class="na">addConstraintViolation</span><span class="o">().</span><span class="na">disableDefaultConstraintViolation</span><span class="o">();</span>
    <span class="k">return</span> <span class="kc">false</span><span class="o">;</span>
<span class="o">}</span>
</code></pre></div></div>

<p>We found multiple paths flowing into <code class="language-plaintext highlighter-rouge">ConstraintValidatorContext.buildConstraintViolationWithTemplate(0)</code>.</p>

<h4 id="impact">Impact</h4>

<p>This issue may lead to Remote Code execution</p>

<h4 id="remediation">Remediation</h4>

<p>There are different approaches to remediate the issue:</p>
<ul>
  <li>Do not include validated bean properties in the custom error message.</li>
  <li>Sanitize the validated bean properties to make sure that there are no EL expressions. An example of valid sanitization logic can be found <a href="https://github.com/hibernate/hibernate-validator/blob/master/engine/src/main/java/org/hibernate/validator/internal/engine/messageinterpolation/util/InterpolationHelper.java#L17">here</a>.</li>
  <li>Disable the EL interpolation and only use <code class="language-plaintext highlighter-rouge">ParameterMessageInterpolator</code>:
    <div class="language-java highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="nc">Validator</span> <span class="n">validator</span> <span class="o">=</span> <span class="nc">Validation</span><span class="o">.</span><span class="na">byDefaultProvider</span><span class="o">()</span>
 <span class="o">.</span><span class="na">configure</span><span class="o">()</span>
 <span class="o">.</span><span class="na">messageInterpolator</span><span class="o">(</span> <span class="k">new</span> <span class="nc">ParameterMessageInterpolator</span><span class="o">()</span> <span class="o">)</span>
 <span class="o">.</span><span class="na">buildValidatorFactory</span><span class="o">()</span>
 <span class="o">.</span><span class="na">getValidator</span><span class="o">();</span>
</code></pre></div>    </div>
  </li>
  <li>Replace Hibernate-Validator with Apache BVal which in its latest version does not interpolate EL expressions by default. Note that this replacement may not be a simple drop-in replacement.</li>
</ul>

<h2 id="coordinated-disclosure-timeline">Coordinated Disclosure Timeline</h2>

<p>This report was subject to the GHSL <a href="https://securitylab.github.com/advisories/#policy">coordinated disclosure policy</a></p>

<ul>
  <li>02/18/2020: Report sent to Vendor via BugCrowd</li>
  <li>02/19/2020: Vulnerability acknowledged</li>
  <li>02/19/2020: Netflix acknowledged issue as P1 on secondary target. Awards $3000</li>
</ul>

<h2 id="supporting-resources">Supporting Resources</h2>

<ul>
  <li><a href="https://github.com/Netflix/security-bulletins/blob/master/advisories/nflx-2020-002.md">Vendor Advisory</a></li>
</ul>

<h2 id="credit">Credit</h2>

<p>This issue was discovered and reported by GHSL team member <a href="https://github.com/pwntester">@pwntester (Alvaro Muñoz)</a>.
We would like to thank Guillaume Smet from the Hibernate Validator team for help with the remediation advice.</p>

<h2 id="contact">Contact</h2>

<p>You can contact the GHSL team at <code class="language-plaintext highlighter-rouge">securitylab@github.com</code>, please include the <code class="language-plaintext highlighter-rouge">GHSL-YEAR-ID</code> in any communication regarding this issue.</p>

   