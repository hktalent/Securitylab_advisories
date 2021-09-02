>
    <header class="post-header d-block mb-6">
      <div class="date text-mono f5 my-3">July 1, 2020</div>
      <h1 class="my-2 h00-mktg lh-condensed">GHSL-2020-128: OOB read vulnerability in FreeRDP RLEDECOMPRESS - CVE-2020-4033</h1>

      
      
      
      
      

      

      <a target="_blank" class="sc-frDJqD SgxRc d-inline-flex flex-row flex-items-center text-gray" href="https://github.com/antonio-morales">
        <img class="mr-3" src="https://avatars.githubusercontent.com/u/55253029?s=35" height="35" width="35">
        <span>Antonio Morales</span>
      </a>
    </header>

    <main id="content" class="markdown-body" aria-label="Content">
      <h2 id="summary">Summary</h2>

<p>An out-of-bounds (OOB) read vulnerability has been detected in <code class="language-plaintext highlighter-rouge">RLEDECOMPRESS</code> due to an incorrect range checking in <code class="language-plaintext highlighter-rouge">pbSrc</code>.</p>

<h2 id="product">Product</h2>

<p>FreeRDP</p>

<h2 id="tested-version">Tested Version</h2>

<p>Development version - master branch (Jun 01, 2020)</p>

<h2 id="details-out-of-bound-read-in-rledecompress">Details: Out-of-bound read in <code class="language-plaintext highlighter-rouge">RLEDECOMPRESS</code></h2>

<p>The <code class="language-plaintext highlighter-rouge">RLEDECOMPRESS</code> function in <code class="language-plaintext highlighter-rouge">codec\include\bitmap.c</code> performs a call to <code class="language-plaintext highlighter-rouge">SRCREADPIXEL(pixelA, pbSrc)</code> (line 255), where <code class="language-plaintext highlighter-rouge">SRCREADPIXEL</code> is a macro that assigns the value pointed to by <code class="language-plaintext highlighter-rouge">pbSrc</code> to <code class="language-plaintext highlighter-rouge">pixelA</code> variable:</p>

<p><a href="https://github.com/FreeRDP/FreeRDP/blob/733026dada313cf345c3e3664cfe5790519e9fae/libfreerdp/codec/interleaved.c#L252">View on GitHub!</a></p>
<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="cm">/* libfreerdp/codec/interleaved.c */</span>
<span class="p">...</span>
<span class="cp">#define SRCREADPIXEL(_pix, _buf) _pix = (_buf)[0]
</span><span class="p">...</span>

</code></pre></div></div>

<p><code class="language-plaintext highlighter-rouge">pbSrc</code> is a pointer acting as an iterator which points to the next unread byte in the <code class="language-plaintext highlighter-rouge">pbSrcBuffer</code> array:</p>

<p><a href="https://github.com/FreeRDP/FreeRDP/blob/e7bffa64ef5ed70bac94f823e2b95262642f5296/libfreerdp/codec/include/bitmap.c#L91">View on GitHub!</a></p>
<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="cm">/* libfreerdp/codec/interleaved.c */</span>
<span class="p">...</span>
<span class="k">const</span> <span class="n">BYTE</span><span class="o">*</span> <span class="n">pbSrc</span> <span class="o">=</span> <span class="n">pbSrcBuffer</span><span class="p">;</span>
<span class="k">const</span> <span class="n">BYTE</span><span class="o">*</span> <span class="n">pbEnd</span><span class="p">;</span>
<span class="p">...</span>
<span class="k">while</span> <span class="p">(</span><span class="n">pbSrc</span> <span class="o">&lt;</span> <span class="n">pbEnd</span><span class="p">)</span>
<span class="p">{</span>
<span class="p">...</span>
</code></pre></div></div>

<p>Also, <code class="language-plaintext highlighter-rouge">pbEnd</code> points to the last element of <code class="language-plaintext highlighter-rouge">pbsrcBuffer</code>. And <code class="language-plaintext highlighter-rouge">while (pbSrc &lt; pbEnd)</code> is the loop which iterates through the <code class="language-plaintext highlighter-rouge">pbSrcBuffer</code> array while <code class="language-plaintext highlighter-rouge">pbEnd</code> is greater than <code class="language-plaintext highlighter-rouge">pbSrc</code>.</p>

<p>But the problem here is that this condition is not checked consistently inside the loop. As you can see below, the <code class="language-plaintext highlighter-rouge">advance</code> variable is passed by reference to <code class="language-plaintext highlighter-rouge">ExtractRunLength</code> function. And then it is added to pbSrc:</p>

<p><a href="https://github.com/FreeRDP/FreeRDP/blob/e7bffa64ef5ed70bac94f823e2b95262642f5296/libfreerdp/codec/include/bitmap.c#L253">View on GitHub!</a></p>
<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="cm">/* libfreerdp/codec/interleaved.c */</span>
<span class="p">...</span>
<span class="n">runLength</span> <span class="o">=</span> <span class="n">ExtractRunLength</span><span class="p">(</span><span class="n">code</span><span class="p">,</span> <span class="n">pbSrc</span><span class="p">,</span> <span class="o">&amp;</span><span class="n">advance</span><span class="p">);</span>
<span class="n">pbSrc</span> <span class="o">=</span> <span class="n">pbSrc</span> <span class="o">+</span> <span class="n">advance</span><span class="p">;</span>
<span class="n">SRCREADPIXEL</span><span class="p">(</span><span class="n">pixelA</span><span class="p">,</span> <span class="n">pbSrc</span><span class="p">);</span>
<span class="p">...</span>
</code></pre></div></div>
<p>So, if <code class="language-plaintext highlighter-rouge">pbSrc + advance</code> is greater than <code class="language-plaintext highlighter-rouge">pbEnd</code> OOB read will occur resulting in accessing a memory location that is outside of the boundaries of the <code class="language-plaintext highlighter-rouge">pbSrcBuffer</code> array.</p>

<h3 id="impact">Impact</h3>

<p>This issue may lead to Out-of-Bounds read.</p>

<h2 id="cve">CVE</h2>

<ul>
  <li>CVE-2020-4033</li>
</ul>

<h2 id="coordinated-disclosure-timeline">Coordinated Disclosure Timeline</h2>

<p>This report was subject to the GHSL <a href="https://securitylab.github.com/advisories/#policy">coordinated disclosure policy</a>.</p>

<ul>
  <li>06/01/2020: Vendor contacted</li>
  <li>06/02/2020: Vendor acknowledges report</li>
  <li>06/22/2020: Bug fixed and patch released by the vendor</li>
</ul>

<h2 id="supporting-resources">Supporting Resources</h2>

<ul>
  <li>https://github.com/FreeRDP/FreeRDP/security/advisories/GHSA-7rhj-856w-82p8</li>
  <li>https://github.com/FreeRDP/FreeRDP/commit/0a98c450c58ec150e44781c89aa6f8e7e0f571f5</li>
</ul>

<h2 id="credit">Credit</h2>

<p>This issue was discovered and reported by GHSL team member <a href="https://github.com/antonio-morales">@antonio-morales (Antonio Morales)</a>.</p>

<h2 id="contact">Contact</h2>

<p>You can contact the GHSL team at <code class="language-plaintext highlighter-rouge">securitylab@github.com</code>, please include the <code class="language-plaintext highlighter-rouge">GHSL-2020-128</code> in any communication regarding this issue.</p>