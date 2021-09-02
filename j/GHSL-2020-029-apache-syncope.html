<header class="post-header d-block mb-6">
      <div class="date text-mono f5 my-3">May 11, 2020</div>
      <h1 class="my-2 h00-mktg lh-condensed">GHSL-2020-029: Server-Side template injection in Apache Syncope (RCE) - CVE-2020-1959</h1>

      
      
      
      
      

      

      <a target="_blank" class="sc-frDJqD SgxRc d-inline-flex flex-row flex-items-center text-gray" href="https://github.com/pwntester">
        <img class="mr-3" src="https://avatars.githubusercontent.com/u/125701?s=35" height="35" width="35">
        <span>Alvaro Munoz</span>
      </a>
    </header>

    <main id="content" class="markdown-body" aria-label="Content">
      <h2 id="summary">Summary</h2>

<p>A Server-Side Template Injection was identified in Apache Syncope enabling attackers to inject arbitrary Java EL expressions, leading to a Remote Code Execution (RCE) vulnerability.</p>

<h2 id="product">Product</h2>

<p>Apache Syncope</p>

<h2 id="tested-version">Tested Version</h2>

<p>2.1.5</p>

<h2 id="issues-found">Issues found</h2>

<h3 id="ghsl-2020-029-details---remote-code-execution---javael-injection-cve-2020-1959">GHSL-2020-029 Details - Remote Code Execution - JavaEL Injection (CVE-2020-1959)</h3>

<p>It is possible to run arbitrary code on the server (with Syncope service account privileges) by injecting arbitrary Java Expression Language (EL) expressions.</p>

<p>Apache Syncope uses Java Bean Validation (JSR 380) custom constraint validators such as <code class="language-plaintext highlighter-rouge">org.apache.syncope.core.persistence.jpa.validation.entity.AnyObjectValidator</code>
When building custom constraint violation error messages, it is important to understand that they support different types of interpolation, including <a href="https://docs.jboss.org/hibernate/validator/5.1/reference/en-US/html/chapter-message-interpolation.html#section-interpolation-with-message-expressions">Java EL expressions</a>. Therefore if an attacker can inject arbitrary data in the error message template being passed to <code class="language-plaintext highlighter-rouge">ConstraintValidatorContext.buildConstraintViolationWithTemplate()</code> argument, he will be able to run arbitrary Java code. Unfortunately, it is common that validated (and therefore, normally untrusted) bean properties flow into the custom error message.</p>

<div class="language-java highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="kd">public</span> <span class="kd">class</span> <span class="nc">AnyObjectValidator</span> <span class="kd">extends</span> <span class="nc">AbstractValidator</span><span class="o">&lt;</span><span class="nc">AnyObjectCheck</span><span class="o">,</span> <span class="nc">AnyObject</span><span class="o">&gt;</span> <span class="o">{</span>

    <span class="nd">@Override</span>
    <span class="kd">public</span> <span class="kt">boolean</span> <span class="nf">isValid</span><span class="o">(</span><span class="kd">final</span> <span class="nc">AnyObject</span> <span class="n">anyObject</span><span class="o">,</span> <span class="kd">final</span> <span class="nc">ConstraintValidatorContext</span> <span class="n">context</span><span class="o">)</span> <span class="o">{</span>
        <span class="n">context</span><span class="o">.</span><span class="na">disableDefaultConstraintViolation</span><span class="o">();</span>

        <span class="kt">boolean</span> <span class="n">isValid</span> <span class="o">=</span> <span class="n">anyObject</span><span class="o">.</span><span class="na">getName</span><span class="o">()</span> <span class="o">!=</span> <span class="kc">null</span> <span class="o">&amp;&amp;</span> <span class="no">KEY_PATTERN</span><span class="o">.</span><span class="na">matcher</span><span class="o">(</span><span class="n">anyObject</span><span class="o">.</span><span class="na">getName</span><span class="o">()).</span><span class="na">matches</span><span class="o">();</span>

        <span class="k">if</span> <span class="o">(!</span><span class="n">isValid</span><span class="o">)</span> <span class="o">{</span>
            <span class="n">context</span><span class="o">.</span><span class="na">buildConstraintViolationWithTemplate</span><span class="o">(</span>
                    <span class="n">getTemplate</span><span class="o">(</span><span class="nc">EntityViolationType</span><span class="o">.</span><span class="na">InvalidName</span><span class="o">,</span> <span class="n">anyObject</span><span class="o">.</span><span class="na">getName</span><span class="o">())).</span>
                    <span class="n">addPropertyNode</span><span class="o">(</span><span class="s">"name"</span><span class="o">).</span><span class="na">addConstraintViolation</span><span class="o">();</span>
        <span class="o">}</span>

        <span class="k">return</span> <span class="n">isValid</span><span class="o">;</span>
    <span class="o">}</span>
<span class="o">}</span>
</code></pre></div></div>

<p>There are a total of 25 validators using <code class="language-plaintext highlighter-rouge">ConstraintValidatorContext.buildConstraintViolationWithTemplate(0)</code> out of which 20 appear to be vulnerable (reflecting validated value in the error message)</p>

<h4 id="impact">Impact</h4>

<p>This issue may lead to Remote Code execution.</p>

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

<p>This issue was addressed in the following <a href="https://github.com/apache/syncope/commit/3edc7490da72fad3bd46a72b5e86227db27c4476">commit</a>.</p>

<h2 id="cve">CVE</h2>

<ul>
  <li>CVE-2020-1959</li>
</ul>

<h2 id="coordinated-disclosure-timeline">Coordinated Disclosure Timeline</h2>

<p>This report was subject to the GHSL <a href="https://securitylab.github.com/advisories/#policy">coordinated disclosure policy</a>.</p>

<ul>
  <li>02/18/2020: Report sent to Vendor (security@apache.org)</li>
  <li>03/12/2020: Ping them for acknowledgement</li>
  <li>03/25/2020: Got email reception confirmation</li>
  <li>03/26/2020: Issue is acknowledged</li>
  <li>04/01/2020: Apache sends fix and draft advisory</li>
  <li>05/11/2020: Public Advisory</li>
</ul>

<h2 id="supporting-resources">Supporting Resources</h2>

<ul>
  <li><a href="https://syncope.apache.org/security">Vendor Advisory</a></li>
</ul>

<h2 id="credit">Credit</h2>

<p>This issue was discovered and reported by GHSL team member <a href="https://github.com/pwntester">@pwntester (Alvaro Muñoz)</a>.</p>

<h2 id="contact">Contact</h2>

<p>You can contact the GHSL team at <code class="language-plaintext highlighter-rouge">securitylab@github.com</code>, please include the <code class="language-plaintext highlighter-rouge">GHSL-2020-029</code> in any communication regarding this issue.</p>

   