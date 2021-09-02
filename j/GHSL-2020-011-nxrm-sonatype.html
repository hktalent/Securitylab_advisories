<header class="post-header d-block mb-6">
      <div class="date text-mono f5 my-3">April 3, 2020</div>
      <h1 class="my-2 h00-mktg lh-condensed">GHSL-2020-011: Remote Code Execution - JavaEL Injection (low privileged accounts) in Nexus Repository Manager</h1>

      
      
      
      
      

      

      <a target="_blank" class="sc-frDJqD SgxRc d-inline-flex flex-row flex-items-center text-gray" href="https://github.com/pwntester">
        <img class="mr-3" src="https://avatars.githubusercontent.com/u/125701?s=35" height="35" width="35">
        <span>Alvaro Munoz</span>
      </a>
    </header>

    <main id="content" class="markdown-body" aria-label="Content">
      <h2 id="summary">Summary</h2>

<p>Remote Code Execution - JavaEL Injection (low privileged accounts)</p>

<h2 id="cve">CVE</h2>

<p>CVE-2020-10199</p>

<h2 id="product">Product</h2>
<p>Nexus Repository Manager</p>

<h2 id="tested-version">Tested Version</h2>
<p>3.20.1</p>

<h2 id="details">Details</h2>
<p>It is possible for any authenticated user, no matter the permissions granted, to run arbitrary code on the server (with Nexus process privileges) by injecting arbitrary Java Expression Language (EL) expressions.</p>

<p>We conducted a CodeQL-based variant analysis of CVE-2018-16621 and found that the applied mitigation (<code class="language-plaintext highlighter-rouge">stripJavaEL()</code>) was not applied to <code class="language-plaintext highlighter-rouge">org.sonatype.nexus.validation.ConstraintViolationFactory</code>. Therefore when user-controlled data flows into <code class="language-plaintext highlighter-rouge">createViolation(final String path, final String message)</code> it will get evaluated as a Java EL by <code class="language-plaintext highlighter-rouge">buildConstraintViolationWithTemplate()</code>:</p>

<div class="language-java highlighter-rouge"><div class="highlight"><pre class="highlight"><code>  <span class="kd">private</span> <span class="kd">static</span> <span class="kd">class</span> <span class="nc">HelperValidator</span> <span class="kd">extends</span> <span class="nc">ConstraintValidatorSupport</span><span class="o">&lt;</span><span class="nc">HelperAnnotation</span><span class="o">,</span> <span class="nc">HelperBean</span><span class="o">&gt;</span> <span class="o">{</span>
    <span class="nd">@Override</span>
    <span class="kd">public</span> <span class="kt">boolean</span> <span class="nf">isValid</span><span class="o">(</span><span class="kd">final</span> <span class="nc">HelperBean</span> <span class="n">bean</span><span class="o">,</span> <span class="kd">final</span> <span class="nc">ConstraintValidatorContext</span> <span class="n">context</span><span class="o">)</span> <span class="o">{</span>
      <span class="n">context</span><span class="o">.</span><span class="na">disableDefaultConstraintViolation</span><span class="o">();</span>

      <span class="c1">// build a custom property path</span>
      <span class="nc">ConstraintViolationBuilder</span> <span class="n">builder</span> <span class="o">=</span> <span class="n">context</span><span class="o">.</span><span class="na">buildConstraintViolationWithTemplate</span><span class="o">(</span><span class="n">bean</span><span class="o">.</span><span class="na">getMessage</span><span class="o">());</span>
      <span class="nc">NodeBuilderCustomizableContext</span> <span class="n">nodeBuilder</span> <span class="o">=</span> <span class="kc">null</span><span class="o">;</span>
      <span class="k">for</span> <span class="o">(</span><span class="nc">String</span> <span class="n">part</span> <span class="o">:</span> <span class="n">bean</span><span class="o">.</span><span class="na">getPath</span><span class="o">().</span><span class="na">split</span><span class="o">(</span><span class="s">"\\."</span><span class="o">))</span> <span class="o">{</span>
        <span class="k">if</span> <span class="o">(</span><span class="n">nodeBuilder</span> <span class="o">==</span> <span class="kc">null</span><span class="o">)</span> <span class="o">{</span>
          <span class="n">nodeBuilder</span> <span class="o">=</span> <span class="n">builder</span><span class="o">.</span><span class="na">addPropertyNode</span><span class="o">(</span><span class="n">part</span><span class="o">);</span>
        <span class="o">}</span>
        <span class="k">else</span> <span class="o">{</span>
          <span class="n">nodeBuilder</span> <span class="o">=</span> <span class="n">nodeBuilder</span><span class="o">.</span><span class="na">addPropertyNode</span><span class="o">(</span><span class="n">part</span><span class="o">);</span>
        <span class="o">}</span>
      <span class="o">}</span>
      <span class="k">if</span> <span class="o">(</span><span class="n">nodeBuilder</span> <span class="o">!=</span> <span class="kc">null</span><span class="o">)</span> <span class="o">{</span>
        <span class="n">nodeBuilder</span><span class="o">.</span><span class="na">addConstraintViolation</span><span class="o">();</span>
      <span class="o">}</span>

      <span class="k">return</span> <span class="kc">false</span><span class="o">;</span>
    <span class="o">}</span>
  <span class="o">}</span>
<span class="o">}</span>
</code></pre></div></div>

<p>We found multiple paths flowing into <code class="language-plaintext highlighter-rouge">ConstraintViolationFactory.createViolation(1)</code>. This issue (GHSL-2020-011) focuses on the endpoints which are accessible to any authenticated user, no matter the permissions granted.</p>

<p>On <code class="language-plaintext highlighter-rouge">src/main/java/org/sonatype/nexus/repository/rest/api/AbstractGroupRepositoriesApiResource.java:97</code> group format and members are validated and failures are reported using the insecure <code class="language-plaintext highlighter-rouge">createViolation</code> method:</p>

<div class="language-java highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="kd">private</span> <span class="kt">void</span> <span class="nf">validateGroupMembers</span><span class="o">(</span><span class="no">T</span> <span class="n">request</span><span class="o">)</span> <span class="o">{</span>
  <span class="nc">String</span> <span class="n">groupFormat</span> <span class="o">=</span> <span class="n">request</span><span class="o">.</span><span class="na">getFormat</span><span class="o">();</span>
  <span class="nc">Set</span><span class="o">&lt;</span><span class="nc">ConstraintViolation</span><span class="o">&lt;?&gt;&gt;</span> <span class="n">violations</span> <span class="o">=</span> <span class="nc">Sets</span><span class="o">.</span><span class="na">newHashSet</span><span class="o">();</span>
  <span class="nc">Collection</span><span class="o">&lt;</span><span class="nc">String</span><span class="o">&gt;</span> <span class="n">memberNames</span> <span class="o">=</span> <span class="n">request</span><span class="o">.</span><span class="na">getGroup</span><span class="o">().</span><span class="na">getMemberNames</span><span class="o">();</span>
  <span class="k">for</span> <span class="o">(</span><span class="nc">String</span> <span class="n">repositoryName</span> <span class="o">:</span> <span class="n">memberNames</span><span class="o">)</span> <span class="o">{</span>
    <span class="nc">Repository</span> <span class="n">repository</span> <span class="o">=</span> <span class="n">repositoryManager</span><span class="o">.</span><span class="na">get</span><span class="o">(</span><span class="n">repositoryName</span><span class="o">);</span>
    <span class="k">if</span> <span class="o">(</span><span class="n">nonNull</span><span class="o">(</span><span class="n">repository</span><span class="o">))</span> <span class="o">{</span>
      <span class="nc">String</span> <span class="n">memberFormat</span> <span class="o">=</span> <span class="n">repository</span><span class="o">.</span><span class="na">getFormat</span><span class="o">().</span><span class="na">getValue</span><span class="o">();</span>
      <span class="k">if</span> <span class="o">(!</span><span class="n">memberFormat</span><span class="o">.</span><span class="na">equals</span><span class="o">(</span><span class="n">groupFormat</span><span class="o">))</span> <span class="o">{</span>
        <span class="n">violations</span><span class="o">.</span><span class="na">add</span><span class="o">(</span><span class="n">constraintViolationFactory</span><span class="o">.</span><span class="na">createViolation</span><span class="o">(</span><span class="s">"memberNames"</span><span class="o">,</span>
            <span class="s">"Member repository format does not match group repository format: "</span> <span class="o">+</span> <span class="n">repositoryName</span><span class="o">));</span>
      <span class="o">}</span>
    <span class="o">}</span>
    <span class="k">else</span> <span class="o">{</span>
      <span class="n">violations</span><span class="o">.</span><span class="na">add</span><span class="o">(</span><span class="n">constraintViolationFactory</span><span class="o">.</span><span class="na">createViolation</span><span class="o">(</span><span class="s">"memberNames"</span><span class="o">,</span>
          <span class="s">"Member repository does not exist: "</span> <span class="o">+</span> <span class="n">repositoryName</span><span class="o">));</span>
    <span class="o">}</span>
  <span class="o">}</span>
  <span class="n">maybePropagate</span><span class="o">(</span><span class="n">violations</span><span class="o">,</span> <span class="n">log</span><span class="o">);</span>
<span class="o">}</span>
</code></pre></div></div>

<p>This sink can be reached from any class extending <code class="language-plaintext highlighter-rouge">AbstractGroupRepositoriesApiResource</code>. At the moment of reporting, there is only one class that meets this requirement: <code class="language-plaintext highlighter-rouge">GolangGroupRepositoriesApiResource</code>.</p>

<p>These paths can be exercised by creating or updating a GoLang group repository which enforces authentication but since authorization checks are performed after bean validation, the RCE sink can be reached by any authenticated user.</p>

<h3 id="impact">Impact</h3>

<p>This issue may lead to Remote Code execution by any low-privilege user</p>

<h3 id="remediation">Remediation</h3>

<p>Apply <code class="language-plaintext highlighter-rouge">stripJavaEL()</code> in <code class="language-plaintext highlighter-rouge">HelperValidator</code>:</p>

<div class="language-plaintext highlighter-rouge"><div class="highlight"><pre class="highlight"><code>ConstraintViolationBuilder builder = context.buildConstraintViolationWithTemplate(getEscapeHelper().stripJavaEl(bean.getMessage()));
</code></pre></div></div>

<h2 id="coordinated-disclosure-timeline">Coordinated Disclosure Timeline</h2>
<ul>
  <li>02/03/2020: Report sent to Sonatype</li>
  <li>02/03/2020: Sonatype acknowledged report</li>
  <li>02/14/2020: Sonatype raises questions about some of the issues</li>
  <li>02/17/2020: GHSL answers Sonatype questions</li>
  <li>02/19/2020: Sonatype agrees with GHSL comments</li>
</ul>

<h2 id="vendor-advisories">Vendor advisories</h2>
<p><a href="https://support.sonatype.com/hc/en-us/articles/360044882533-CVE-2020-10199-Nexus-Repository-Manager-3-Remote-Code-Execution-2020-03-31">CVE-2020-10199 Nexus Repository Manager 3 - Remote Code Execution - 2020-03-31</a></p>

<h2 id="credit">Credit</h2>

<p>This issue was discovered and reported by GHSL team member <a href="https://github.com/pwntester">@pwntester (Alvaro Muñoz)</a>.</p>

<h2 id="contact">Contact</h2>

<p>You can contact the GHSL team at <code class="language-plaintext highlighter-rouge">securitylab@github.com</code>, please include the <code class="language-plaintext highlighter-rouge">GHSL-2020-011</code> in any communication regarding this issue.</p>

   