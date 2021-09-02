<header class="post-header d-block mb-6">
      <div class="date text-mono f5 my-3">May 4, 2021</div>
      <h1 class="my-2 h00-mktg lh-condensed">GHSL-2021-032: Template object injection in Mailtrain - CVE-2021-27136</h1>

      
      
      
      
      

      

      <a target="_blank" class="sc-frDJqD SgxRc d-inline-flex flex-row flex-items-center text-gray" href="https://github.com/agustingianni">
        <img class="mr-3" src="https://avatars.githubusercontent.com/u/102623?s=35" height="35" width="35">
        <span>Agustin Gianni</span>
      </a>
    </header>

    <main id="content" class="markdown-body" aria-label="Content">
      
<h2 id="coordinated-disclosure-timeline">Coordinated Disclosure Timeline</h2>

<ul>
  <li>03/02/2021: Report sent to Vendor</li>
  <li>10/02/2021: Report sent again to a different contact address due to lack of response.</li>
  <li>24/02/2021: Report sent again to a different contact address due to lack of response.</li>
  <li>30/03/2021: Created a public issue asking for a contact address.</li>
  <li>07/04/2021: Maintainer mentioned that branch v1 is deprecated.</li>
  <li>08/04/2021: Maintainer deprecated the vulnerable branch</li>
</ul>

<h2 id="summary">Summary</h2>

<p>Dangerous usage of the template rendering API may lead to Cross Site Scripting (XSS), file disclosure, and Remote Code Execution (RCE).</p>

<h2 id="product">Product</h2>
<p>Mailtrain</p>

<h2 id="tested-version">Tested Version</h2>
<p>Master branch at commit <code class="language-plaintext highlighter-rouge">281072ac1bb43d539f6dd13ceed6390a8581c248</code>.</p>

<h2 id="details">Details</h2>

<h3 id="template-object-injection">Template object injection</h3>

<p>Passing attacker supplied objects to the <a href="http://expressjs.com/en/api.html#res.render">res.render</a> method leads to several security problems such as XSS and file disclosure as demonstrated in the proofs of concepts. The way in which this exploit works is by overwriting internal configuration variables of the rendering engine such as <code class="language-plaintext highlighter-rouge">settings.views</code>, with attacker supplied values (in this PoC we have used <code class="language-plaintext highlighter-rouge">req.query</code> but any source of data can be used).</p>

<p>There is a non trivial amount of places in which user influenced objects land in a call to <a href="http://expressjs.com/en/api.html#res.render">res.render</a>. We have used <code class="language-plaintext highlighter-rouge">CodeQL</code> to identify potential places that need attention. You can find the query and its results <a href="https://lgtm.com/query/3199569237347440822/">here</a>.</p>

<p>From the results of the query we have selected <code class="language-plaintext highlighter-rouge">/routes/lists.js</code> to illustrate the issue but there are more cases that behave similarly:</p>

<div class="language-js highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="nx">router</span><span class="p">.</span><span class="kd">get</span><span class="p">(</span><span class="dl">'</span><span class="s1">/create</span><span class="dl">'</span><span class="p">,</span> <span class="nx">passport</span><span class="p">.</span><span class="nx">csrfProtection</span><span class="p">,</span> <span class="p">(</span><span class="nx">req</span><span class="p">,</span> <span class="nx">res</span><span class="p">)</span> <span class="o">=&gt;</span> <span class="p">{</span>
    <span class="kd">let</span> <span class="nx">data</span> <span class="o">=</span> <span class="nx">tools</span><span class="p">.</span><span class="nx">convertKeys</span><span class="p">(</span><span class="nx">req</span><span class="p">.</span><span class="nx">query</span><span class="p">,</span> <span class="p">{</span>
        <span class="na">skip</span><span class="p">:</span> <span class="p">[</span><span class="dl">'</span><span class="s1">layout</span><span class="dl">'</span><span class="p">]</span>
    <span class="p">});</span>

    <span class="nx">data</span><span class="p">.</span><span class="nx">csrfToken</span> <span class="o">=</span> <span class="nx">req</span><span class="p">.</span><span class="nx">csrfToken</span><span class="p">();</span>

    <span class="k">if</span> <span class="p">(</span><span class="o">!</span><span class="p">(</span><span class="dl">'</span><span class="s1">publicSubscribe</span><span class="dl">'</span> <span class="k">in</span> <span class="nx">data</span><span class="p">))</span> <span class="p">{</span>
        <span class="nx">data</span><span class="p">.</span><span class="nx">publicSubscribe</span> <span class="o">=</span> <span class="kc">true</span><span class="p">;</span>
    <span class="p">}</span>

    <span class="nx">data</span><span class="p">.</span><span class="nx">unsubscriptionModeOptions</span> <span class="o">=</span> <span class="nx">getUnsubscriptionModeOptions</span><span class="p">(</span><span class="nx">data</span><span class="p">.</span><span class="nx">unsubscriptionMode</span> <span class="o">||</span> <span class="nx">lists</span><span class="p">.</span><span class="nx">UnsubscriptionMode</span><span class="p">.</span><span class="nx">ONE_STEP</span><span class="p">);</span>

    <span class="nx">res</span><span class="p">.</span><span class="nx">render</span><span class="p">(</span><span class="dl">'</span><span class="s1">lists/create</span><span class="dl">'</span><span class="p">,</span> <span class="nx">data</span><span class="p">);</span>
<span class="p">});</span>
</code></pre></div></div>

<p>In the above code we can see that the object <code class="language-plaintext highlighter-rouge">data</code> is populated with content coming from the <code class="language-plaintext highlighter-rouge">req.query</code> objects which is in turn parsed from the URL. This allow an attacker to craft complex objects that will be supplied to the rendering engine.</p>

<h4 id="xss-proof-of-concept">XSS Proof of Concept.</h4>

<p>An authenticated user can be tricked to open the following URL that will execute arbitrary JavaScript code in the context of the user.</p>

<div class="language-plaintext highlighter-rouge"><div class="highlight"><pre class="highlight"><code>http://localhost:3000/lists/create?indexPage=true&amp;shoutout=&lt;script&gt;alert("XSS")&lt;/script&gt;
</code></pre></div></div>

<h4 id="file-disclosure">File disclosure</h4>

<p>An authenticated user can disclose the content of arbitrary files in the system. The following URL will show the contents of the file <code class="language-plaintext highlighter-rouge">/app/setup/mailtrain.conf</code>.</p>

<div class="language-plaintext highlighter-rouge"><div class="highlight"><pre class="highlight"><code>http://localhost:3000/lists/create?indexPage=true&amp;shoutout=goose&amp;settings[views]=/app/setup/&amp;settings[view%20options][layout])=mailtrain.conf
</code></pre></div></div>

<h4 id="impact">Impact</h4>

<p>The impact of this vulnerability depends on the underlying template rendering in use. We have verified that XSS and file disclosure are possible but remote code execution cannot be completely discarded.</p>

<h2 id="cve">CVE</h2>

<ul>
  <li>CVE-2021-27136</li>
</ul>

<h2 id="resources">Resources</h2>

<ul>
  <li>A single instance of the vulnerability got published by another party: https://arjunshibu.tech/intro-to-open-source-bug-bounty/</li>
  <li>One instance of the vulnerability got addressed: https://github.com/Mailtrain-org/mailtrain/pull/1029/files</li>
</ul>

<h2 id="credit">Credit</h2>

<p>This issue was discovered and reported by GHSL team member <a href="https://github.com/agustingianni">@agustingianni (Agustin Gianni)</a>.</p>

<h2 id="contact">Contact</h2>

<p>You can contact the GHSL team at <code class="language-plaintext highlighter-rouge">securitylab@github.com</code>, please include a reference to <code class="language-plaintext highlighter-rouge">GHSL-2021-032</code> in any communication regarding this issue.</p>


    