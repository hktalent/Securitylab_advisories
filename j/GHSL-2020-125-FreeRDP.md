>
    <header class="post-header d-block mb-6">
      <div class="date text-mono f5 my-3">July 1, 2020</div>
      <h1 class="my-2 h00-mktg lh-condensed">GHSL-2020-125: integer signedness mismatch vulnerability in FreeRDP leads to OOB read - CVE-2020-4032</h1>

      
      
      
      
      

      

      <a target="_blank" class="sc-frDJqD SgxRc d-inline-flex flex-row flex-items-center text-gray" href="https://github.com/antonio-morales">
        <img class="mr-3" src="https://avatars.githubusercontent.com/u/55253029?s=35" height="35" width="35">
        <span>Antonio Morales</span>
      </a>
    </header>

    <main id="content" class="markdown-body" aria-label="Content">
      <h2 id="summary">Summary</h2>

<p>An integer casting vulnerability has been detected in <code class="language-plaintext highlighter-rouge">update_recv_secondary_order</code> in <code class="language-plaintext highlighter-rouge">orders.c</code>.</p>

<h2 id="product">Product</h2>

<p>FreeRDP</p>

<h2 id="tested-version">Tested Version</h2>

<p>Development version - master branch (May 27, 2020)</p>

<h2 id="details-integer-casting-vulnerability-in-update_recv_secondary_order">Details: Integer casting vulnerability in <code class="language-plaintext highlighter-rouge">update_recv_secondary_order</code></h2>

<p>Under certain circumstances (glyph-cache and relax-order-checks should be enabled) the <code class="language-plaintext highlighter-rouge">update_recv_secondary_order</code> function in <code class="language-plaintext highlighter-rouge">orders.c</code> is affected by an integer signedness mismatch vulnerability.</p>

<p>The problem is that the <code class="language-plaintext highlighter-rouge">size_t diff</code> variable is an unsigned integer type, but <code class="language-plaintext highlighter-rouge">start - end</code> is a signed integer arithmetic expression that can return a negative value. When such a negative value is assigned to the unsigned <code class="language-plaintext highlighter-rouge">size_t diff</code> variable, it becomes a very large positive value at [1] up to and including <code class="language-plaintext highlighter-rouge">SIZE_MAX</code>. Consequently, <code class="language-plaintext highlighter-rouge">Stream_Seek</code> will be called with an extremely large <code class="language-plaintext highlighter-rouge">diff</code> value, moving the <code class="language-plaintext highlighter-rouge">s</code> stream pointer to an invalid address [2].</p>

<p><a href="https://github.com/FreeRDP/FreeRDP/blob/05cd9ea2290d23931f615c1b004d4b2e69074e27/libfreerdp/core/orders.c#L3765">View on GitHub!</a></p>
<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="cm">/* libfreerdp/core/orders.c */</span>
<span class="p">...</span>
<span class="n">diff</span> <span class="o">=</span> <span class="n">start</span> <span class="o">-</span> <span class="n">end</span><span class="p">;</span> <span class="c1">// [1]</span>
<span class="k">if</span> <span class="p">(</span><span class="n">diff</span> <span class="o">&gt;</span> <span class="mi">0</span><span class="p">)</span>
<span class="p">{</span>
		<span class="n">WLog_Print</span><span class="p">(</span><span class="n">update</span><span class="o">-&gt;</span><span class="n">log</span><span class="p">,</span> <span class="n">WLOG_DEBUG</span><span class="p">,</span>
		           <span class="s">"SECONDARY_ORDER %s: read %"</span> <span class="n">PRIuz</span> <span class="s">"bytes short, skipping"</span><span class="p">,</span> <span class="n">name</span><span class="p">,</span> <span class="n">diff</span><span class="p">);</span>
		<span class="n">Stream_Seek</span><span class="p">(</span><span class="n">s</span><span class="p">,</span> <span class="n">diff</span><span class="p">);</span> <span class="c1">// [2]</span>
<span class="p">}</span>
<span class="k">return</span> <span class="n">rc</span><span class="p">;</span>
<span class="p">...</span>
</code></pre></div></div>

<h3 id="impact">Impact</h3>

<p>This issue may lead to Out-of-Bounds read.</p>

<h2 id="cve">CVE</h2>

<ul>
  <li>CVE-2020-4032</li>
</ul>

<h2 id="coordinated-disclosure-timeline">Coordinated Disclosure Timeline</h2>

<p>This report was subject to the GHSL <a href="https://securitylab.github.com/advisories/#policy">coordinated disclosure policy</a>.</p>

<ul>
  <li>05/27/2020: Report sent to Vendor</li>
  <li>05/27/2020: Vendor acknowledges report</li>
  <li>06/22/2020: Bug fixed and patch released by the vendor</li>
</ul>

<h2 id="supporting-resources">Supporting Resources</h2>

<ul>
  <li>https://github.com/FreeRDP/FreeRDP/security/advisories/GHSA-3898-mc89-x2vc</li>
  <li>https://github.com/FreeRDP/FreeRDP/commit/e7bffa64ef5ed70bac94f823e2b95262642f5296</li>
</ul>

<h2 id="credit">Credit</h2>

<p>This issue was discovered and reported by GHSL team member <a href="https://github.com/antonio-morales">@antonio-morales (Antonio Morales)</a>.</p>

<h2 id="contact">Contact</h2>

<p>You can contact the GHSL team at <code class="language-plaintext highlighter-rouge">securitylab@github.com</code>, please include the <code class="language-plaintext highlighter-rouge">GHSL-2020-125</code> in any communication regarding this issue.</p>