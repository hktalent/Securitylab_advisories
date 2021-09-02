<header class="post-header d-block mb-6">
      <div class="date text-mono f5 my-3">May 26, 2020</div>
      <h1 class="my-2 h00-mktg lh-condensed">GHSL-2020-073: Path traversal in Jooby - CVE-2020-7647</h1>

      
      
      
      
      

      

      <a target="_blank" class="sc-frDJqD SgxRc d-inline-flex flex-row flex-items-center text-gray" href="https://github.com/pwntester">
        <img class="mr-3" src="https://avatars.githubusercontent.com/u/125701?s=35" height="35" width="35">
        <span>Alvaro Munoz</span>
      </a>
    </header>

    <main id="content" class="markdown-body" aria-label="Content">
      <h2 id="summary">Summary</h2>
<p>A Path Traversal vulnerability was identified in Jooby which allows an attacker to access arbitrary classpath resources including <code class="language-plaintext highlighter-rouge">.properties</code> and <code class="language-plaintext highlighter-rouge">.class</code> files.</p>

<h2 id="product">Product</h2>
<p>Jooby</p>

<h2 id="tested-version">Tested Version</h2>
<p>1.6.6</p>

<h2 id="fix">Fix</h2>
<p>Patched versions: 1.6.7 and 2.8.2</p>

<h2 id="details">Details</h2>

<h3 id="arbitrary-classpath-resource-access">Arbitrary classpath resource access</h3>

<p>When exposing a <em>file system</em> directory such as in:</p>

<div class="language-java highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="n">assets</span><span class="o">(</span><span class="s">"/static/**"</span><span class="o">,</span> <span class="nc">Paths</span><span class="o">.</span><span class="na">get</span><span class="o">(</span><span class="s">"static"</span><span class="o">));</span>
</code></pre></div></div>

<p>Jooby uses the following code in <a href="https://github.com/jooby-project/jooby/blob/1.x/jooby/src/main/java/org/jooby/handlers/AssetHandler.java">AssetHandler.loader()</a> to access the file:</p>

<div class="language-java highlighter-rouge"><div class="highlight"><pre class="highlight"><code>  <span class="kd">private</span> <span class="kd">static</span> <span class="nc">Loader</span> <span class="nf">loader</span><span class="o">(</span><span class="kd">final</span> <span class="nc">Path</span> <span class="n">basedir</span><span class="o">,</span> <span class="kd">final</span> <span class="nc">ClassLoader</span> <span class="n">classloader</span><span class="o">)</span> <span class="o">{</span>
    <span class="k">if</span> <span class="o">(</span><span class="nc">Files</span><span class="o">.</span><span class="na">exists</span><span class="o">(</span><span class="n">basedir</span><span class="o">))</span> <span class="o">{</span>
      <span class="k">return</span> <span class="n">name</span> <span class="o">-&gt;</span> <span class="o">{</span>
        <span class="nc">Path</span> <span class="n">path</span> <span class="o">=</span> <span class="n">basedir</span><span class="o">.</span><span class="na">resolve</span><span class="o">(</span><span class="n">name</span><span class="o">).</span><span class="na">normalize</span><span class="o">();</span>
        <span class="k">if</span> <span class="o">(</span><span class="nc">Files</span><span class="o">.</span><span class="na">exists</span><span class="o">(</span><span class="n">path</span><span class="o">)</span> <span class="o">&amp;&amp;</span> <span class="n">path</span><span class="o">.</span><span class="na">startsWith</span><span class="o">(</span><span class="n">basedir</span><span class="o">))</span> <span class="o">{</span>
          <span class="k">try</span> <span class="o">{</span>
            <span class="k">return</span> <span class="n">path</span><span class="o">.</span><span class="na">toUri</span><span class="o">().</span><span class="na">toURL</span><span class="o">();</span>
          <span class="o">}</span> <span class="k">catch</span> <span class="o">(</span><span class="nc">MalformedURLException</span> <span class="n">x</span><span class="o">)</span> <span class="o">{</span>
            <span class="c1">// shh</span>
          <span class="o">}</span>
        <span class="o">}</span>
        <span class="k">return</span> <span class="n">classloader</span><span class="o">.</span><span class="na">getResource</span><span class="o">(</span><span class="n">name</span><span class="o">);</span>
      <span class="o">};</span>
    <span class="o">}</span>
    <span class="k">return</span> <span class="nl">classloader:</span><span class="o">:</span><span class="n">getResource</span><span class="o">;</span>
  <span class="o">}</span>
</code></pre></div></div>

<p>However, if the file does not exist or the normalized name is outside of Jooby’s base directory, the classpath is also searched in <code class="language-plaintext highlighter-rouge">classloader.getResource()</code>.</p>

<p>An attacker can access a URL such as <code class="language-plaintext highlighter-rouge">http://server/static/WEB-INF/web.xml</code> which will make Jooby search the <code class="language-plaintext highlighter-rouge">&lt;base directory&gt;/static</code> path for the referenced file. If this is not found, the classpath will be searched for <code class="language-plaintext highlighter-rouge">/WEB-INF/web.xml</code> instead and its contents will be returned. This way an attacker can access any configuration file or even the application class files.</p>

<p>Note that even if assets are configured for a certain extension, it is still possible to bypass this, e.g.:</p>

<div class="language-java highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="n">assets</span><span class="o">(</span><span class="s">"/static/**/*.js"</span><span class="o">,</span> <span class="nc">Paths</span><span class="o">.</span><span class="na">get</span><span class="o">(</span><span class="s">"static"</span><span class="o">));</span>
</code></pre></div></div>

<p>In this case, an attacker can access <code class="language-plaintext highlighter-rouge">io.yiss.App</code> bytecode by sending:</p>

<div class="language-plaintext highlighter-rouge"><div class="highlight"><pre class="highlight"><code>http://localhost:8080/static/io/yiss/App.class.js
</code></pre></div></div>
<p>.
This vulnerability also affects assets configured to access resources from the root of the class path, e.g.:</p>

<div class="language-java highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="n">assets</span><span class="o">(</span><span class="s">"/static/**"</span><span class="o">);</span>
</code></pre></div></div>

<p>In this case we can traverse <code class="language-plaintext highlighter-rouge">/static</code> using:</p>

<div class="language-plaintext highlighter-rouge"><div class="highlight"><pre class="highlight"><code>http://localhost:8080/static/..%252fio/yiss/App.class
</code></pre></div></div>

<h3 id="impact">Impact</h3>

<p>This issue may lead to Classpath Resource Disclosure (Information Disclosure).</p>

<h2 id="cve">CVE</h2>

<ul>
  <li>CVE-2020-7647</li>
</ul>

<h2 id="coordinated-disclosure-timeline">Coordinated Disclosure Timeline</h2>

<p>This report was subject to the GHSL <a href="https://securitylab.github.com/advisories/#policy">coordinated disclosure policy</a>.</p>

<ul>
  <li>04/15/2020: Report sent to vendor</li>
  <li>05/10/2020: Issue is fixed</li>
  <li>05/11/2020: Public advisory</li>
</ul>

<h2 id="resources">Resources</h2>

<ul>
  <li><a href="https://github.com/jooby-project/jooby/security/advisories/GHSA-px9h-x66r-8mpc">Vendor advisory</a></li>
</ul>

<h2 id="credit">Credit</h2>

<p>This issue was discovered and reported by GHSL team member <a href="https://github.com/pwntester">@pwntester (Alvaro Muñoz)</a>.</p>

<h2 id="contact">Contact</h2>

<p>You can contact the GHSL team at <code class="language-plaintext highlighter-rouge">securitylab@github.com</code>. Please include <code class="language-plaintext highlighter-rouge">GHSL-2020-073</code> in any communication regarding this issue.</p>

 