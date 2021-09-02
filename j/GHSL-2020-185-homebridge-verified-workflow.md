<header class="post-header d-block mb-6">
      <div class="date text-mono f5 my-3">February 3, 2021</div>
      <h1 class="my-2 h00-mktg lh-condensed">GHSL-2020-185: Arbitrary code execution in Plugins Verified by Homebridge workflow</h1>

      
      
      
      
      

      

      <a target="_blank" class="sc-frDJqD SgxRc d-inline-flex flex-row flex-items-center text-gray" href="https://github.com/jarlob">
        <img class="mr-3" src="https://avatars.githubusercontent.com/u/26652396?s=35" height="35" width="35">
        <span>Jaroslav Lobacevski</span>
      </a>
    </header>

    <main id="content" class="markdown-body" aria-label="Content">
      <h2 id="coordinated-disclosure-timeline">Coordinated Disclosure Timeline</h2>

<ul>
  <li>10/16/2020: Report sent to vendor</li>
  <li>10/20/2020: Issue fixed</li>
</ul>

<h2 id="summary">Summary</h2>

<p>The <a href="https://github.com/homebridge/verified/blob/master/.github/workflows/plugin-prechecks.yml">‘plugin-prechecks.yml’ GitHub workflow</a> is vulnerable to arbitrary code execution, that may lead to the repository being compromised.</p>

<h2 id="product">Product</h2>

<p><a href="https://github.com/homebridge/verified">homebridge/verified GitHub repository</a></p>

<h2 id="tested-version">Tested Version</h2>

<p><a href="https://github.com/homebridge/verified/blob/master/.github/workflows/plugin-prechecks.yml">plugin-prechecks.yml</a> from the master branch.</p>

<h2 id="details">Details</h2>

<h3 id="issue-the-tested-npm-package-may-use-the-temporary-github-authorization-token-to-make-arbitrary-changes-in-the-repository">Issue: The tested npm package may use the temporary GitHub authorization token to make arbitrary changes in the repository</h3>

<p>When a user creates a public issue or comments on an existing issue with <code class="language-plaintext highlighter-rouge">/check</code> it automatically starts the <a href="https://github.com/homebridge/verified/blob/master/.github/workflows/plugin-prechecks.yml">plugin-prechecks.yml</a> GitHub workflow. The body of the issue is used in the custom <a href="https://github.com/homebridge/verified/blob/master/precheck/">precheck</a> action.</p>

<div class="language-ts highlighter-rouge"><div class="highlight"><pre class="highlight"><code>    <span class="kd">const</span> <span class="nx">matches</span> <span class="o">=</span> <span class="nx">issueBody</span><span class="p">.</span><span class="nx">split</span><span class="p">(</span><span class="dl">'</span><span class="se">\n</span><span class="dl">'</span><span class="p">)</span>
      <span class="p">.</span><span class="nx">map</span><span class="p">((</span><span class="nx">line</span><span class="p">)</span> <span class="o">=&gt;</span> <span class="p">{</span>
        <span class="kd">const</span> <span class="nx">match</span> <span class="o">=</span> <span class="nx">line</span> <span class="p">?</span> <span class="nx">line</span><span class="p">.</span><span class="nx">match</span><span class="p">(</span><span class="sr">/</span><span class="se">(</span><span class="sr">https</span><span class="se">?</span><span class="sr">:</span><span class="se">\/\/</span><span class="sr">.</span><span class="se">[^</span><span class="sr"> </span><span class="se">]</span><span class="sr">*</span><span class="se">)</span><span class="sr">/gi</span><span class="p">)</span> <span class="p">:</span> <span class="kc">null</span>
        <span class="k">if</span> <span class="p">(</span><span class="nx">match</span><span class="p">)</span> <span class="p">{</span>
          <span class="k">return</span> <span class="nx">match</span><span class="p">.</span><span class="nx">find</span><span class="p">((</span><span class="nx">x</span><span class="p">)</span> <span class="o">=&gt;</span> <span class="nx">x</span><span class="p">.</span><span class="nx">includes</span><span class="p">(</span><span class="dl">'</span><span class="s1">npmjs.com/package</span><span class="dl">'</span><span class="p">));</span>
        <span class="p">}</span>
      <span class="p">})</span>
      <span class="p">.</span><span class="nx">filter</span><span class="p">((</span><span class="nx">m</span><span class="p">)</span> <span class="o">=&gt;</span> <span class="nx">m</span><span class="p">)</span>
      <span class="p">.</span><span class="nx">map</span><span class="p">((</span><span class="nx">x</span><span class="p">)</span> <span class="o">=&gt;</span> <span class="p">{</span>
        <span class="kd">const</span> <span class="nx">pluginName</span> <span class="o">=</span> <span class="nx">x</span><span class="p">.</span><span class="nx">split</span><span class="p">(</span><span class="dl">'</span><span class="s1">/</span><span class="dl">'</span><span class="p">).</span><span class="nx">splice</span><span class="p">(</span><span class="mi">4</span><span class="p">).</span><span class="nx">join</span><span class="p">(</span><span class="dl">'</span><span class="s1">/</span><span class="dl">'</span><span class="p">).</span><span class="nx">replace</span><span class="p">(</span><span class="sr">/</span><span class="se">[^</span><span class="sr">a-zA-Z0-9@</span><span class="se">\\/</span><span class="sr">-</span><span class="se">]</span><span class="sr">/g</span><span class="p">,</span> <span class="dl">''</span><span class="p">);</span>
        <span class="k">return</span> <span class="nx">pluginName</span><span class="p">;</span>
      <span class="p">});</span>
<span class="p">...</span>
      <span class="kd">const</span> <span class="nx">proc</span> <span class="o">=</span> <span class="nx">child_process</span><span class="p">.</span><span class="nx">spawn</span><span class="p">(</span><span class="dl">'</span><span class="s1">npm</span><span class="dl">'</span><span class="p">,</span> <span class="p">[</span><span class="dl">'</span><span class="s1">install</span><span class="dl">'</span><span class="p">,</span> <span class="k">this</span><span class="p">.</span><span class="nx">packageName</span><span class="p">],</span> <span class="p">{</span>
        <span class="na">cwd</span><span class="p">:</span> <span class="k">this</span><span class="p">.</span><span class="nx">testPath</span><span class="p">,</span>
</code></pre></div></div>

<h4 id="impact">Impact</h4>

<p>Since <code class="language-plaintext highlighter-rouge">npm install</code> also executes post install scripts from the package this leads to arbitrary code execution of untrusted npm packages in the context of a GitHub action runner. It makes a temporary GitHub repository token available to the potentially malicious code which can be used to modify the repository content or run any malicious code in the hosted environment.</p>

<h2 id="credit">Credit</h2>

<p>This issue was discovered and reported by GHSL team member <a href="https://github.com/JarLob">@JarLob (Jaroslav Lobačevski)</a>.</p>

<h2 id="contact">Contact</h2>

<p>You can contact the GHSL team at <code class="language-plaintext highlighter-rouge">securitylab@github.com</code>, please include a reference to <code class="language-plaintext highlighter-rouge">GHSL-2020-185</code> in any communication regarding this issue.</p>
