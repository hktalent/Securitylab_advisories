>
    <header class="post-header d-block mb-6">
      <div class="date text-mono f5 my-3">July 1, 2020</div>
      <h1 class="my-2 h00-mktg lh-condensed">GHSL-2020-105: OOB read vulnerability in FreeRDP glyph_cache_put - CVE-2020-11098</h1>

      
      
      
      
      

      

      <a target="_blank" class="sc-frDJqD SgxRc d-inline-flex flex-row flex-items-center text-gray" href="https://github.com/antonio-morales">
        <img class="mr-3" src="https://avatars.githubusercontent.com/u/55253029?s=35" height="35" width="35">
        <span>Antonio Morales</span>
      </a>
    </header>

    <main id="content" class="markdown-body" aria-label="Content">
      <h2 id="summary">Summary</h2>

<p>An out-of-bounds (OOB) read vulnerability has been detected in glyph_cache_put due to an Off-by-one error in boundary condition checking.</p>

<h2 id="product">Product</h2>

<p>FreeRDP</p>

<h2 id="tested-version">Tested Version</h2>

<p>Development version - master branch (May 22, 2020)</p>

<h2 id="details-out-of-bound-read-in-glyph_cache_put">Details: Out-of-bound read in <code class="language-plaintext highlighter-rouge">glyph_cache_put</code></h2>

<p>The <code class="language-plaintext highlighter-rouge">glyph_cache_put</code> function in “glyph.c” performs a call to <code class="language-plaintext highlighter-rouge">glyphCache-&gt;glyphCache[id].entries[index]</code> where <code class="language-plaintext highlighter-rouge">index</code> is a value that can be controlled indirectly by a potential attacker:</p>

<p><a href="https://github.com/FreeRDP/FreeRDP/blob/6ade7b4cbfd71c54b3d724e8f2d6ac76a58e879a/libfreerdp/cache/glyph.c#L590">View on GitHub!</a></p>
<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="cm">/* libfreerdp/cache/glyph.c */</span>
<span class="p">...</span>
<span class="p">[</span><span class="n">line</span> <span class="mi">582</span><span class="p">]</span> <span class="k">if</span> <span class="p">(</span><span class="n">index</span> <span class="o">&gt;</span> <span class="n">glyphCache</span><span class="o">-&gt;</span><span class="n">glyphCache</span><span class="p">[</span><span class="n">id</span><span class="p">].</span><span class="n">number</span><span class="p">)</span>
           <span class="p">{</span>
		          <span class="n">WLog_ERR</span><span class="p">(</span><span class="n">TAG</span><span class="p">,</span> <span class="s">"invalid glyph cache index: %"</span> <span class="n">PRIu32</span> <span class="s">" in cache id: %"</span> <span class="n">PRIu32</span> <span class="s">""</span><span class="p">,</span> <span class="n">index</span><span class="p">,</span> <span class="n">id</span><span class="p">);</span>
		          <span class="k">return</span> <span class="n">FALSE</span><span class="p">;</span>
           <span class="p">}</span>
<span class="p">...</span>
<span class="p">[</span><span class="n">line</span> <span class="mi">590</span><span class="p">]</span> <span class="n">prevGlyph</span> <span class="o">=</span> <span class="n">glyphCache</span><span class="o">-&gt;</span><span class="n">glyphCache</span><span class="p">[</span><span class="n">id</span><span class="p">].</span><span class="n">entries</span><span class="p">[</span><span class="n">index</span><span class="p">]</span>
<span class="p">...</span>
</code></pre></div></div>
<p>As you can see above, the <code class="language-plaintext highlighter-rouge">index</code> value is checked to not be greater than <code class="language-plaintext highlighter-rouge">glyphCache-&gt;glyphCache[id].number</code>, where this value is the number of elements in <code class="language-plaintext highlighter-rouge">entries</code> array. However, in the C programmin glanguage array indexes start with 0.</p>

<p>So, if the <code class="language-plaintext highlighter-rouge">index</code> value is equal to <code class="language-plaintext highlighter-rouge">glyphCache-&gt;glyphCache[id].number</code> OOB reads will occur resulting in accessing a memory location that is outside of the boundaries of the <code class="language-plaintext highlighter-rouge">glyphCache[id].entries</code> array.</p>

<h3 id="impact">Impact</h3>

<p>This issue may lead to Out-of-Bounds read.</p>

<h2 id="cve">CVE</h2>

<ul>
  <li>CVE-2020-11098</li>
</ul>

<h2 id="coordinated-disclosure-timeline">Coordinated Disclosure Timeline</h2>

<p>This report was subject to the GHSL <a href="https://securitylab.github.com/advisories/#policy">coordinated disclosure policy</a>.</p>

<ul>
  <li>05/22/2020: Vendor contacted</li>
  <li>05/26/2020: Vendor acknowledges report</li>
  <li>06/22/2020: Bug fixed and patch released by the vendor</li>
</ul>

<h2 id="supporting-resources">Supporting Resources</h2>

<ul>
  <li>https://github.com/FreeRDP/FreeRDP/security/advisories/GHSA-jr57-f58x-hjmv</li>
  <li>https://github.com/FreeRDP/FreeRDP/commit/c0fd449ec0870b050d350d6d844b1ea6dad4bc7d</li>
</ul>

<h2 id="credit">Credit</h2>

<p>This issue was discovered and reported by GHSL team member <a href="https://github.com/antonio-morales">@antonio-morales (Antonio Morales)</a>.</p>

<h2 id="contact">Contact</h2>

<p>You can contact the GHSL team at <code class="language-plaintext highlighter-rouge">securitylab@github.com</code>, please include the <code class="language-plaintext highlighter-rouge">GHSL-2020-105</code> in any communication regarding this issue.