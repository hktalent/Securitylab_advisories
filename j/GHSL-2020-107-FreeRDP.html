>
    <header class="post-header d-block mb-6">
      <div class="date text-mono f5 my-3">July 1, 2020</div>
      <h1 class="my-2 h00-mktg lh-condensed">GHSL-2020-107: OOB read vulnerability in FreeRDP update_read_cache_bitmap_v3_order - CVE-2020-11096</h1>

      
      
      
      
      

      

      <a target="_blank" class="sc-frDJqD SgxRc d-inline-flex flex-row flex-items-center text-gray" href="https://github.com/antonio-morales">
        <img class="mr-3" src="https://avatars.githubusercontent.com/u/55253029?s=35" height="35" width="35">
        <span>Antonio Morales</span>
      </a>
    </header>

    <main id="content" class="markdown-body" aria-label="Content">
      <h2 id="summary">Summary</h2>

<p>A global out-of-bounds (OOB) read vulnerability has been detected in <code class="language-plaintext highlighter-rouge">update_read_cache_bitmap_v3_order</code> due to global array access with attacker-controlled index.</p>

<h2 id="product">Product</h2>

<p>FreeRDP</p>

<h2 id="tested-version">Tested Version</h2>

<p>Development version - master branch (May 26, 2020)</p>

<h2 id="details-global-oob-read-in-update_read_cache_bitmap_v3_order">Details: Global OOB read in <code class="language-plaintext highlighter-rouge">update_read_cache_bitmap_v3_order</code></h2>

<p>The <code class="language-plaintext highlighter-rouge">update_read_cache_bitmap_v3_order</code> function in <code class="language-plaintext highlighter-rouge">orders.c</code> performs a call to <code class="language-plaintext highlighter-rouge">cache_bitmap_v3-&gt;bpp = CBR23_BPP[bitsPerPixelId]</code> (line 2158), where <code class="language-plaintext highlighter-rouge">bitsPerPixelId</code> is a value that can be controlled directly by a potential attacker.</p>

<p>As we can see below, <code class="language-plaintext highlighter-rouge">CBR23_BPP</code> is an static array of size 7:</p>

<p><a href="https://github.com/FreeRDP/FreeRDP/blob/733ee3208306b1ea32697b356c0215180fc3f049/libfreerdp/core/orders.c#L121">View on GitHub!</a></p>
<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="cm">/* libfreerdp/core/orders.c */</span>

<span class="k">static</span> <span class="k">const</span> <span class="n">BYTE</span> <span class="n">CBR23_BPP</span><span class="p">[]</span> <span class="o">=</span> <span class="p">{</span> <span class="mi">0</span><span class="p">,</span> <span class="mi">0</span><span class="p">,</span> <span class="mi">0</span><span class="p">,</span> <span class="mi">8</span><span class="p">,</span> <span class="mi">16</span><span class="p">,</span> <span class="mi">24</span><span class="p">,</span> <span class="mi">32</span> <span class="p">};</span>
</code></pre></div></div>

<p>So, if <code class="language-plaintext highlighter-rouge">bitsPerPixelId</code> value is greater than 6, an OOB read occurs resulting in accessing a memory location that is outside of the boundaries of the static array <code class="language-plaintext highlighter-rouge">CBR23_BPP</code>.</p>

<h3 id="impact">Impact</h3>

<p>This issue may lead to Out-of-Bounds read.</p>

<h2 id="cve">CVE</h2>

<ul>
  <li>CVE-2020-11096</li>
</ul>

<h2 id="coordinated-disclosure-timeline">Coordinated Disclosure Timeline</h2>

<p>This report was subject to the GHSL <a href="https://securitylab.github.com/advisories/#policy">coordinated disclosure policy</a>.</p>

<ul>
  <li>05/26/2020: Report sent to Vendor</li>
  <li>05/26/2020: Vendor acknowledges report</li>
  <li>06/22/2020: Bug fixed and patch released by the vendor</li>
</ul>

<h2 id="supporting-resources">Supporting Resources</h2>

<ul>
  <li>https://github.com/FreeRDP/FreeRDP/security/advisories/GHSA-mjw7-3mq2-996x</li>
  <li>https://github.com/FreeRDP/FreeRDP/commit/b8beb55913471952f92770c90c372139d78c16c0</li>
</ul>

<h2 id="credit">Credit</h2>

<p>This issue was discovered and reported by GHSL team member <a href="https://github.com/antonio-morales">@antonio-morales (Antonio Morales)</a>.</p>

<h2 id="contact">Contact</h2>

<p>You can contact the GHSL team at <code class="language-plaintext highlighter-rouge">securitylab@github.com</code>, please include the <code class="language-plaintext highlighter-rouge">GHSL-2020-107</code> in any communication regarding this issue.</p>