<header class="post-header d-block mb-6">
      <div class="date text-mono f5 my-3">April 13, 2020</div>
      <h1 class="my-2 h00-mktg lh-condensed">GHSL-2020-012: Remote Code Execution - JavaEL Injection (high privileged accounts) in Nexus Repository Manager</h1>

      
      
      
      
      

      

      <a target="_blank" class="sc-frDJqD SgxRc d-inline-flex flex-row flex-items-center text-gray" href="https://github.com/pwntester">
        <img class="mr-3" src="https://avatars.githubusercontent.com/u/125701?s=35" height="35" width="35">
        <span>Alvaro Munoz</span>
      </a>
    </header>

    <main id="content" class="markdown-body" aria-label="Content">
      <h2 id="summary">Summary</h2>
<p>GHSL-2020-012 - Remote Code Execution - JavaEL Injection (high privileged accounts)</p>

<h2 id="product">Product</h2>
<p>Nexus Repository Manager</p>

<h2 id="tested-version">Tested Version</h2>
<p>3.20.1</p>

<h2 id="cve">CVE</h2>
<p><a href="https://support.sonatype.com/hc/en-us/articles/360044882533-CVE-2020-10199-Nexus-Repository-Manager-3-Remote-Code-Execution-2020-03-31">CVE-2020-10199</a></p>

<h2 id="details">Details</h2>
<p>It is possible for high privilege users (eg: admins), to run arbitrary code on the server (with Nexus process privileges) by injecting arbitrary Java Expression Language (EL) expressions.</p>

<p>The following paths share the same sink in the <code class="language-plaintext highlighter-rouge">ConstraintViolationFactory</code>:</p>

<h3 id="path-1">Path 1</h3>
<ul>
  <li>Source: <code class="language-plaintext highlighter-rouge">src/main/java/org/sonatype/nexus/coreui/RepositoryComponent.groovy:232</code></li>
  <li>Sink: <code class="language-plaintext highlighter-rouge">src/main/java/org/sonatype/nexus/cleanup/CleanupConfigurationValidator.java:120</code></li>
  <li>Permissions: <code class="language-plaintext highlighter-rouge">nx-repository-admin-*-*-*</code></li>
</ul>

<p><em>Note:</em> There are many endpoints that may end up calling <code class="language-plaintext highlighter-rouge">validateConfiguration()</code>, for example <code class="language-plaintext highlighter-rouge">coreui_Repository.create</code> will call <code class="language-plaintext highlighter-rouge">repositoryManager.create(config)</code> which will call <code class="language-plaintext highlighter-rouge">validateConfiguration</code></p>

<h3 id="path-2">Path 2</h3>
<ul>
  <li>Source: <code class="language-plaintext highlighter-rouge">src/main/java/org/sonatype/nexus/coreui/ComponentComponent.groovy:188</code></li>
  <li>Sink: <code class="language-plaintext highlighter-rouge">src/main/java/org/sonatype/nexus/selector/SelectorFactory.java:76</code></li>
  <li>Permissions: <code class="language-plaintext highlighter-rouge">nx-selectors-*</code></li>
</ul>

<p><em>Note:</em> This is an interesting vector since we are passing either a JEXL or CSEL expression which are not exploitable (because of the sandboxed JEXL engine). However when expressions are validated, the following code gets executed:</p>

<div class="language-java highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="kd">public</span> <span class="kt">void</span> <span class="nf">validateSelector</span><span class="o">(</span><span class="kd">final</span> <span class="nc">String</span> <span class="n">type</span><span class="o">,</span> <span class="kd">final</span> <span class="nc">String</span> <span class="n">expression</span><span class="o">)</span> <span class="o">{</span>
  <span class="k">try</span> <span class="o">{</span>
    <span class="k">switch</span> <span class="o">(</span><span class="n">type</span><span class="o">)</span> <span class="o">{</span>
      <span class="k">case</span> <span class="nc">JexlSelector</span><span class="o">.</span><span class="na">TYPE</span><span class="o">:</span>
        <span class="n">jexlEngine</span><span class="o">.</span><span class="na">parseExpression</span><span class="o">(</span><span class="n">expression</span><span class="o">);</span>
        <span class="k">break</span><span class="o">;</span>
      <span class="k">case</span> <span class="nc">CselSelector</span><span class="o">.</span><span class="na">TYPE</span><span class="o">:</span>
        <span class="n">validateCselExpression</span><span class="o">(</span><span class="n">jexlEngine</span><span class="o">.</span><span class="na">parseExpression</span><span class="o">(</span><span class="n">expression</span><span class="o">));</span>
        <span class="k">break</span><span class="o">;</span>
      <span class="k">default</span><span class="o">:</span>
        <span class="k">throw</span> <span class="k">new</span> <span class="nf">IllegalArgumentException</span><span class="o">(</span><span class="s">"Unknown selector type: "</span> <span class="o">+</span> <span class="n">type</span><span class="o">);</span>
    <span class="o">}</span>
  <span class="o">}</span>
  <span class="k">catch</span> <span class="o">(</span><span class="nc">Exception</span> <span class="n">e</span><span class="o">)</span> <span class="o">{</span>
    <span class="nc">String</span> <span class="n">detail</span> <span class="o">=</span> <span class="n">format</span><span class="o">(</span><span class="s">"Invalid %s: %s"</span><span class="o">,</span> <span class="n">upper</span><span class="o">(</span><span class="n">type</span><span class="o">),</span>
        <span class="n">e</span> <span class="k">instanceof</span> <span class="nc">JexlException</span> <span class="o">?</span> <span class="n">expandExceptionDetail</span><span class="o">((</span><span class="nc">JexlException</span><span class="o">)</span> <span class="n">e</span><span class="o">)</span> <span class="o">:</span> <span class="n">e</span><span class="o">.</span><span class="na">getMessage</span><span class="o">());</span>

    <span class="n">log</span><span class="o">.</span><span class="na">debug</span><span class="o">(</span><span class="n">detail</span><span class="o">,</span> <span class="n">e</span><span class="o">);</span>

    <span class="k">throw</span> <span class="k">new</span> <span class="nf">ConstraintViolationException</span><span class="o">(</span><span class="n">e</span><span class="o">.</span><span class="na">getMessage</span><span class="o">(),</span>
        <span class="nc">ImmutableSet</span><span class="o">.</span><span class="na">of</span><span class="o">(</span><span class="n">constraintViolationFactory</span><span class="o">.</span><span class="na">createViolation</span><span class="o">(</span><span class="s">"expression"</span><span class="o">,</span> <span class="n">detail</span><span class="o">)));</span>
  <span class="o">}</span>
<span class="o">}</span>
</code></pre></div></div>

<p>If there are any errors during the validation, the exception’s message will be passed to <code class="language-plaintext highlighter-rouge">createViolation</code> which will turn into Java EL evaluation.
A simple way to be sure that the JavaEL expression gets into the exception’s message is to put it in single back-quotes which represents a multiline literal in JEXL.</p>

<h3 id="path-3">Path 3</h3>
<ul>
  <li>Source: <code class="language-plaintext highlighter-rouge">src/main/java/org/sonatype/nexus/coreui/SelectorComponent.groovy:91</code></li>
  <li>Sink: <code class="language-plaintext highlighter-rouge">src/main/java/org/sonatype/nexus/coreui/SelectorComponent.groovy:92</code></li>
  <li>Permissions: <code class="language-plaintext highlighter-rouge">nx-selectors-create</code></li>
</ul>

<h3 id="path-4">Path 4</h3>
<ul>
  <li>Source: <code class="language-plaintext highlighter-rouge">src/main/java/org/sonatype/nexus/coreui/SelectorComponent.groovy:109</code></li>
  <li>Sink:  <code class="language-plaintext highlighter-rouge">src/main/java/org/sonatype/nexus/coreui/SelectorComponent.groovy:110</code></li>
  <li>Permissions: <code class="language-plaintext highlighter-rouge">nx-selectors-update</code></li>
</ul>

<h3 id="path-5">Path 5</h3>
<ul>
  <li>Source: <code class="language-plaintext highlighter-rouge">src/main/java/org/sonatype/nexus/repository/rest/internal/resources/ContentSelectorsApiResource.java:89</code></li>
  <li>Sink: <code class="language-plaintext highlighter-rouge">src/main/java/org/sonatype/nexus/repository/rest/internal/resources/ContentSelectorsApiResource.java:90</code></li>
  <li>Permissions: <code class="language-plaintext highlighter-rouge">nx-selectors-create</code></li>
</ul>

<h3 id="path-6">Path 6</h3>
<ul>
  <li>Source: <code class="language-plaintext highlighter-rouge">src/main/java/org/sonatype/nexus/repository/rest/internal/resources/ContentSelectorsApiResource.java:110</code></li>
  <li>Sink: <code class="language-plaintext highlighter-rouge">src/main/java/org/sonatype/nexus/repository/rest/internal/resources/ContentSelectorsApiResource.java:113</code></li>
  <li>Permissions: <code class="language-plaintext highlighter-rouge">nx-selectors-update</code></li>
</ul>

<h3 id="path-7">Path 7</h3>
<ul>
  <li>Sink: <code class="language-plaintext highlighter-rouge">src/main/java/org/sonatype/nexus/repository/storage/StorageFacetImpl.java:176</code></li>
  <li>Permissions: <code class="language-plaintext highlighter-rouge">nx-blobstores-create</code></li>
</ul>

<h3 id="path-8">Path 8</h3>
<ul>
  <li>Sink: <code class="language-plaintext highlighter-rouge">src/main/java/org/sonatype/nexus/repository/storage/ContentSelectorUpgradeManager.java:56</code></li>
  <li>Permissions: <code class="language-plaintext highlighter-rouge">nx-selectors-*</code></li>
</ul>

<p>The attacker needs to create a JEXL selector (not possible through UI, so either they intercept the request and change the type from <code class="language-plaintext highlighter-rouge">CSEL</code> to <code class="language-plaintext highlighter-rouge">JEXL</code> or use the REST API.</p>

<p>In order to trigger the vulnerability, the attacker needs to wait until lifecycle phase changes or something triggers the content selector upgrade process. If the attacker has enough permissions, they can trigger the upgrade by bouncing the lifecycle phase manually using the REST API.</p>

<h3 id="impact">Impact</h3>

<p>This issue may lead to Remote Code execution by high-privilege users</p>

<h3 id="remediation">Remediation</h3>

<p>Apply <code class="language-plaintext highlighter-rouge">stripJavaEL()</code>  in <code class="language-plaintext highlighter-rouge">HelperValidator</code>:</p>

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

<h2 id="credit">Credit</h2>

<p>This issue was discovered and reported by GHSL team member <a href="https://github.com/pwntester">@pwntester (Alvaro Muñoz)</a>.</p>

<h2 id="contact">Contact</h2>

<p>You can contact the GHSL team at <code class="language-plaintext highlighter-rouge">securitylab@github.com</code>, please include the <code class="language-plaintext highlighter-rouge">GHSL-2020-012</code> in any communication regarding this issue.</p>
