<header class="post-header d-block mb-6">
      <div class="date text-mono f5 my-3">March 25, 2020</div>
      <h1 class="my-2 h00-mktg lh-condensed">GHSL-2020-027: Server-Side Template Injection in Netflix Conductor</h1>

      
      
      
      
      

      

      <a target="_blank" class="sc-frDJqD SgxRc d-inline-flex flex-row flex-items-center text-gray" href="https://github.com/pwntester">
        <img class="mr-3" src="https://avatars.githubusercontent.com/u/125701?s=35" height="35" width="35">
        <span>Alvaro Munoz</span>
      </a>
    </header>

    <main id="content" class="markdown-body" aria-label="Content">
      <h2 id="summary">Summary</h2>

<p>A Server-Side Template Injection was identified in Netflix Conductor enabling attackers to inject arbitrary Java EL expressions, leading to a pre-auth Remote Code Execution (RCE) vulnerability.</p>

<h2 id="cve">CVE</h2>

<p>CVE-2020-9296</p>

<h2 id="product">Product</h2>

<p>Netflix Conductor</p>

<h2 id="tested-version">Tested Version</h2>

<p>v2.25.1-alpha</p>

<h2 id="issues-found">Issues found</h2>

<h3 id="ghsl-2020-027-details---remote-code-execution---javael-injection">GHSL-2020-027 Details - Remote Code Execution - JavaEL Injection</h3>

<p>It is possible to run arbitrary code on the server (with Conductor service account privileges) by injecting arbitrary Java Expression Language (EL) expressions.</p>

<p>Netflix Conductor uses Java Bean Validation (JSR 380) custom constraint validators such as <code class="language-plaintext highlighter-rouge">com.netflix.conductor.common.constraints.TaskTimeoutConstraint.TaskTimeoutValidator</code>
When building custom constraint violation error messages, it is important to understand that they support different types of interpolation, including <a href="https://docs.jboss.org/hibernate/validator/5.1/reference/en-US/html/chapter-message-interpolation.html#section-interpolation-with-message-expressions">Java EL expressions</a>. Therefore if an attacker can inject arbitrary data in the error message template being passed to <code class="language-plaintext highlighter-rouge">ConstraintValidatorContext.buildConstraintViolationWithTemplate()</code> argument, they will be able to run arbitrary Java code. Unfortunately, it is common that validated (and therefore, normally untrusted) bean properties flow into the custom error message.</p>

<div class="language-java highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="kd">class</span> <span class="nc">TaskTimeoutValidator</span> <span class="kd">implements</span> <span class="nc">ConstraintValidator</span><span class="o">&lt;</span><span class="nc">TaskTimeoutConstraint</span><span class="o">,</span> <span class="nc">TaskDef</span><span class="o">&gt;</span> <span class="o">{</span>
    <span class="nd">@Override</span>
    <span class="kd">public</span> <span class="kt">void</span> <span class="nf">initialize</span><span class="o">(</span><span class="nc">TaskTimeoutConstraint</span> <span class="n">constraintAnnotation</span><span class="o">)</span> <span class="o">{</span>
    <span class="o">}</span>
    <span class="nd">@Override</span>
    <span class="kd">public</span> <span class="kt">boolean</span> <span class="nf">isValid</span><span class="o">(</span><span class="nc">TaskDef</span> <span class="n">taskDef</span><span class="o">,</span> <span class="nc">ConstraintValidatorContext</span> <span class="n">context</span><span class="o">)</span> <span class="o">{</span>
        <span class="n">context</span><span class="o">.</span><span class="na">disableDefaultConstraintViolation</span><span class="o">();</span>
        <span class="kt">boolean</span> <span class="n">valid</span> <span class="o">=</span> <span class="kc">true</span><span class="o">;</span>
        <span class="k">if</span> <span class="o">(</span><span class="n">taskDef</span><span class="o">.</span><span class="na">getTimeoutSeconds</span><span class="o">()</span> <span class="o">&gt;</span> <span class="mi">0</span><span class="o">)</span> <span class="o">{</span>
            <span class="k">if</span> <span class="o">(</span><span class="n">taskDef</span><span class="o">.</span><span class="na">getResponseTimeoutSeconds</span><span class="o">()</span> <span class="o">&gt;</span> <span class="n">taskDef</span><span class="o">.</span><span class="na">getTimeoutSeconds</span><span class="o">())</span> <span class="o">{</span>
                <span class="n">valid</span> <span class="o">=</span> <span class="kc">false</span><span class="o">;</span>
                <span class="nc">String</span> <span class="n">message</span> <span class="o">=</span> <span class="nc">String</span><span class="o">.</span><span class="na">format</span><span class="o">(</span><span class="s">"TaskDef: %s responseTimeoutSeconds: %d must be less than timeoutSeconds: %d"</span><span class="o">,</span>
                        <span class="n">taskDef</span><span class="o">.</span><span class="na">getName</span><span class="o">(),</span> <span class="n">taskDef</span><span class="o">.</span><span class="na">getResponseTimeoutSeconds</span><span class="o">(),</span> <span class="n">taskDef</span><span class="o">.</span><span class="na">getTimeoutSeconds</span><span class="o">());</span>
                <span class="n">context</span><span class="o">.</span><span class="na">buildConstraintViolationWithTemplate</span><span class="o">(</span><span class="n">message</span><span class="o">).</span><span class="na">addConstraintViolation</span><span class="o">();</span>
            <span class="o">}</span>
        <span class="o">}</span>
        <span class="k">return</span> <span class="n">valid</span><span class="o">;</span>
    <span class="o">}</span>
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
  <li>02/19/2020: Sent new RCE payload</li>
  <li>02/19/2020: Netflix acknowledged issue as P2 on secondary target. Awards $1500</li>
</ul>

<h2 id="supporting-resources">Supporting resources</h2>

<ul>
  <li><a href="https://github.com/Netflix/security-bulletins/blob/master/advisories/nflx-2020-001.md">Vendor Advisory</a></li>
</ul>

<h2 id="credit">Credit</h2>

<p>This issue was discovered and reported by GHSL team member <a href="https://github.com/pwntester">@pwntester (Alvaro Muñoz)</a>.
We would like to thank Guillaume Smet from the Hibernate Validator team for help with the remediation advice.</p>

<h2 id="contact">Contact</h2>

<p>You can contact the GHSL team at <code class="language-plaintext highlighter-rouge">securitylab@github.com</code>, please include the <code class="language-plaintext highlighter-rouge">GHSL-YEAR-ID</code> in any communication regarding this issue.</p>

   