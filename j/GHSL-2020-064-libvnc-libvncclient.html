<header class="post-header d-block mb-6">
      <div class="date text-mono f5 my-3">June 17, 2020</div>
      <h1 class="my-2 h00-mktg lh-condensed">GHSL-2020-064: integer overflow in LibVNCClient HandleCursorShape resulting in remote heap overflow - CVE-2019-20788</h1>

      
      
      
      
      

      

      <a target="_blank" class="sc-frDJqD SgxRc d-inline-flex flex-row flex-items-center text-gray" href="https://github.com/anticomputer">
        <img class="mr-3" src="https://avatars.githubusercontent.com/u/13686387?s=35" height="35" width="35">
        <span>Bas Alberts</span>
      </a>
    </header>

    <main id="content" class="markdown-body" aria-label="Content">
      <h2 id="summary">Summary</h2>

<p>There exists an integer overflow in <code class="language-plaintext highlighter-rouge">HandleCursorShape</code> RFB event handler in libvncclient, which is the client implementation for LibVNC included with libvncserver.</p>

<p>This issue allows a malicious VNC server to trigger a remote heap overflow in a connecting VNC client, which may lead to Remote Code Excution (RCE). This issue was addressed in libvncclient 0.9.13.</p>

<p>NOTE: this issue was addressed in the LibVNC pre-release branch on Nov 17, 2019, prior to GHSL’s discovery of the same issue in a release version (0.9.11) as shipped in a mainline Linux distribution. In coordination with the maintainer the GHSL decided to still fully triage this issue with CVE assignment so that the various Linux distributions shipping this library would be aware of the included security fix and update accordingly.</p>

<h2 id="product">Product</h2>

<p>libvncserver/libvncclient</p>

<h2 id="tested-versions">Tested Versions</h2>

<ul>
  <li>libvnccserver 0.9.11</li>
</ul>

<h2 id="details-potential-integer-overflow-in-handlecursorshape-rfb-event-handling">Details: Potential integer overflow in <code class="language-plaintext highlighter-rouge">HandleCursorShape</code> RFB event handling</h2>

<p>All source snippets are based on the 0.9.11 release of libvncserver.</p>

<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="n">libvncclient</span><span class="o">/</span><span class="n">cursor</span><span class="p">.</span><span class="n">c</span>
<span class="p">...</span>
<span class="n">rfbBool</span> <span class="nf">HandleCursorShape</span><span class="p">(</span><span class="n">rfbClient</span><span class="o">*</span> <span class="n">client</span><span class="p">,</span><span class="kt">int</span> <span class="n">xhot</span><span class="p">,</span> <span class="kt">int</span> <span class="n">yhot</span><span class="p">,</span> <span class="kt">int</span> <span class="n">width</span><span class="p">,</span> <span class="kt">int</span> <span class="n">height</span><span class="p">,</span> <span class="kt">uint32_t</span> <span class="n">enc</span><span class="p">)</span>
<span class="p">{</span>
  <span class="kt">int</span> <span class="n">bytesPerPixel</span><span class="p">;</span>
  <span class="kt">size_t</span> <span class="n">bytesPerRow</span><span class="p">,</span> <span class="n">bytesMaskData</span><span class="p">;</span>
  <span class="n">rfbXCursorColors</span> <span class="n">rgb</span><span class="p">;</span>
  <span class="kt">uint32_t</span> <span class="n">colors</span><span class="p">[</span><span class="mi">2</span><span class="p">];</span>
  <span class="kt">char</span> <span class="o">*</span><span class="n">buf</span><span class="p">;</span>
  <span class="kt">uint8_t</span> <span class="o">*</span><span class="n">ptr</span><span class="p">;</span>
  <span class="kt">int</span> <span class="n">x</span><span class="p">,</span> <span class="n">y</span><span class="p">,</span> <span class="n">b</span><span class="p">;</span>

  <span class="n">bytesPerPixel</span> <span class="o">=</span> <span class="n">client</span><span class="o">-&gt;</span><span class="n">format</span><span class="p">.</span><span class="n">bitsPerPixel</span> <span class="o">/</span> <span class="mi">8</span><span class="p">;</span>
  <span class="n">bytesPerRow</span> <span class="o">=</span> <span class="p">(</span><span class="n">width</span> <span class="o">+</span> <span class="mi">7</span><span class="p">)</span> <span class="o">/</span> <span class="mi">8</span><span class="p">;</span>
  <span class="n">bytesMaskData</span> <span class="o">=</span> <span class="n">bytesPerRow</span> <span class="o">*</span> <span class="n">height</span><span class="p">;</span>

  <span class="k">if</span> <span class="p">(</span><span class="n">width</span> <span class="o">*</span> <span class="n">height</span> <span class="o">==</span> <span class="mi">0</span><span class="p">)</span>
    <span class="k">return</span> <span class="n">TRUE</span><span class="p">;</span>

  <span class="cm">/* Allocate memory for pixel data and temporary mask data. */</span>
  <span class="k">if</span><span class="p">(</span><span class="n">client</span><span class="o">-&gt;</span><span class="n">rcSource</span><span class="p">)</span>
    <span class="n">free</span><span class="p">(</span><span class="n">client</span><span class="o">-&gt;</span><span class="n">rcSource</span><span class="p">);</span>

<span class="p">[</span><span class="mi">1</span><span class="p">]</span>
  <span class="n">client</span><span class="o">-&gt;</span><span class="n">rcSource</span> <span class="o">=</span> <span class="n">malloc</span><span class="p">(</span><span class="n">width</span> <span class="o">*</span> <span class="n">height</span> <span class="o">*</span> <span class="n">bytesPerPixel</span><span class="p">);</span>
  <span class="k">if</span> <span class="p">(</span><span class="n">client</span><span class="o">-&gt;</span><span class="n">rcSource</span> <span class="o">==</span> <span class="nb">NULL</span><span class="p">)</span>
    <span class="k">return</span> <span class="n">FALSE</span><span class="p">;</span>

  <span class="n">buf</span> <span class="o">=</span> <span class="n">malloc</span><span class="p">(</span><span class="n">bytesMaskData</span><span class="p">);</span>
  <span class="k">if</span> <span class="p">(</span><span class="n">buf</span> <span class="o">==</span> <span class="nb">NULL</span><span class="p">)</span> <span class="p">{</span>
    <span class="n">free</span><span class="p">(</span><span class="n">client</span><span class="o">-&gt;</span><span class="n">rcSource</span><span class="p">);</span>
    <span class="n">client</span><span class="o">-&gt;</span><span class="n">rcSource</span> <span class="o">=</span> <span class="nb">NULL</span><span class="p">;</span>
    <span class="k">return</span> <span class="n">FALSE</span><span class="p">;</span>
  <span class="p">}</span>

  <span class="cm">/* Read and decode cursor pixel data, depending on the encoding type. */</span>

  <span class="k">if</span> <span class="p">(</span><span class="n">enc</span> <span class="o">==</span> <span class="n">rfbEncodingXCursor</span><span class="p">)</span> <span class="p">{</span>
    <span class="cm">/* Read and convert background and foreground colors. */</span>
    <span class="k">if</span> <span class="p">(</span><span class="o">!</span><span class="n">ReadFromRFBServer</span><span class="p">(</span><span class="n">client</span><span class="p">,</span> <span class="p">(</span><span class="kt">char</span> <span class="o">*</span><span class="p">)</span><span class="o">&amp;</span><span class="n">rgb</span><span class="p">,</span> <span class="n">sz_rfbXCursorColors</span><span class="p">))</span> <span class="p">{</span>
      <span class="n">free</span><span class="p">(</span><span class="n">client</span><span class="o">-&gt;</span><span class="n">rcSource</span><span class="p">);</span>
      <span class="n">client</span><span class="o">-&gt;</span><span class="n">rcSource</span> <span class="o">=</span> <span class="nb">NULL</span><span class="p">;</span>
      <span class="n">free</span><span class="p">(</span><span class="n">buf</span><span class="p">);</span>
      <span class="k">return</span> <span class="n">FALSE</span><span class="p">;</span>
    <span class="p">}</span>
    <span class="n">colors</span><span class="p">[</span><span class="mi">0</span><span class="p">]</span> <span class="o">=</span> <span class="n">RGB24_TO_PIXEL</span><span class="p">(</span><span class="mi">32</span><span class="p">,</span> <span class="n">rgb</span><span class="p">.</span><span class="n">backRed</span><span class="p">,</span> <span class="n">rgb</span><span class="p">.</span><span class="n">backGreen</span><span class="p">,</span> <span class="n">rgb</span><span class="p">.</span><span class="n">backBlue</span><span class="p">);</span>
    <span class="n">colors</span><span class="p">[</span><span class="mi">1</span><span class="p">]</span> <span class="o">=</span> <span class="n">RGB24_TO_PIXEL</span><span class="p">(</span><span class="mi">32</span><span class="p">,</span> <span class="n">rgb</span><span class="p">.</span><span class="n">foreRed</span><span class="p">,</span> <span class="n">rgb</span><span class="p">.</span><span class="n">foreGreen</span><span class="p">,</span> <span class="n">rgb</span><span class="p">.</span><span class="n">foreBlue</span><span class="p">);</span>

    <span class="cm">/* Read 1bpp pixel data into a temporary buffer. */</span>
    <span class="k">if</span> <span class="p">(</span><span class="o">!</span><span class="n">ReadFromRFBServer</span><span class="p">(</span><span class="n">client</span><span class="p">,</span> <span class="n">buf</span><span class="p">,</span> <span class="n">bytesMaskData</span><span class="p">))</span> <span class="p">{</span>
      <span class="n">free</span><span class="p">(</span><span class="n">client</span><span class="o">-&gt;</span><span class="n">rcSource</span><span class="p">);</span>
      <span class="n">client</span><span class="o">-&gt;</span><span class="n">rcSource</span> <span class="o">=</span> <span class="nb">NULL</span><span class="p">;</span>
      <span class="n">free</span><span class="p">(</span><span class="n">buf</span><span class="p">);</span>
      <span class="k">return</span> <span class="n">FALSE</span><span class="p">;</span>
    <span class="p">}</span>

    <span class="cm">/* Convert 1bpp data to byte-wide color indices. */</span>
    <span class="n">ptr</span> <span class="o">=</span> <span class="n">client</span><span class="o">-&gt;</span><span class="n">rcSource</span><span class="p">;</span>
    <span class="k">for</span> <span class="p">(</span><span class="n">y</span> <span class="o">=</span> <span class="mi">0</span><span class="p">;</span> <span class="n">y</span> <span class="o">&lt;</span> <span class="n">height</span><span class="p">;</span> <span class="n">y</span><span class="o">++</span><span class="p">)</span> <span class="p">{</span>
      <span class="k">for</span> <span class="p">(</span><span class="n">x</span> <span class="o">=</span> <span class="mi">0</span><span class="p">;</span> <span class="n">x</span> <span class="o">&lt;</span> <span class="n">width</span> <span class="o">/</span> <span class="mi">8</span><span class="p">;</span> <span class="n">x</span><span class="o">++</span><span class="p">)</span> <span class="p">{</span>
	<span class="k">for</span> <span class="p">(</span><span class="n">b</span> <span class="o">=</span> <span class="mi">7</span><span class="p">;</span> <span class="n">b</span> <span class="o">&gt;=</span> <span class="mi">0</span><span class="p">;</span> <span class="n">b</span><span class="o">--</span><span class="p">)</span> <span class="p">{</span>
	  <span class="o">*</span><span class="n">ptr</span> <span class="o">=</span> <span class="n">buf</span><span class="p">[</span><span class="n">y</span> <span class="o">*</span> <span class="n">bytesPerRow</span> <span class="o">+</span> <span class="n">x</span><span class="p">]</span> <span class="o">&gt;&gt;</span> <span class="n">b</span> <span class="o">&amp;</span> <span class="mi">1</span><span class="p">;</span>
	  <span class="n">ptr</span> <span class="o">+=</span> <span class="n">bytesPerPixel</span><span class="p">;</span>
	<span class="p">}</span>
      <span class="p">}</span>
      <span class="k">for</span> <span class="p">(</span><span class="n">b</span> <span class="o">=</span> <span class="mi">7</span><span class="p">;</span> <span class="n">b</span> <span class="o">&gt;</span> <span class="mi">7</span> <span class="o">-</span> <span class="n">width</span> <span class="o">%</span> <span class="mi">8</span><span class="p">;</span> <span class="n">b</span><span class="o">--</span><span class="p">)</span> <span class="p">{</span>
	<span class="o">*</span><span class="n">ptr</span> <span class="o">=</span> <span class="n">buf</span><span class="p">[</span><span class="n">y</span> <span class="o">*</span> <span class="n">bytesPerRow</span> <span class="o">+</span> <span class="n">x</span><span class="p">]</span> <span class="o">&gt;&gt;</span> <span class="n">b</span> <span class="o">&amp;</span> <span class="mi">1</span><span class="p">;</span>
	<span class="n">ptr</span> <span class="o">+=</span> <span class="n">bytesPerPixel</span><span class="p">;</span>
      <span class="p">}</span>
    <span class="p">}</span>

    <span class="cm">/* Convert indices into the actual pixel values. */</span>
    <span class="k">switch</span> <span class="p">(</span><span class="n">bytesPerPixel</span><span class="p">)</span> <span class="p">{</span>
    <span class="k">case</span> <span class="mi">1</span><span class="p">:</span>
      <span class="k">for</span> <span class="p">(</span><span class="n">x</span> <span class="o">=</span> <span class="mi">0</span><span class="p">;</span> <span class="n">x</span> <span class="o">&lt;</span> <span class="n">width</span> <span class="o">*</span> <span class="n">height</span><span class="p">;</span> <span class="n">x</span><span class="o">++</span><span class="p">)</span>
	<span class="n">client</span><span class="o">-&gt;</span><span class="n">rcSource</span><span class="p">[</span><span class="n">x</span><span class="p">]</span> <span class="o">=</span> <span class="p">(</span><span class="kt">uint8_t</span><span class="p">)</span><span class="n">colors</span><span class="p">[</span><span class="n">client</span><span class="o">-&gt;</span><span class="n">rcSource</span><span class="p">[</span><span class="n">x</span><span class="p">]];</span>
      <span class="k">break</span><span class="p">;</span>
    <span class="k">case</span> <span class="mi">2</span><span class="p">:</span>
      <span class="k">for</span> <span class="p">(</span><span class="n">x</span> <span class="o">=</span> <span class="mi">0</span><span class="p">;</span> <span class="n">x</span> <span class="o">&lt;</span> <span class="n">width</span> <span class="o">*</span> <span class="n">height</span><span class="p">;</span> <span class="n">x</span><span class="o">++</span><span class="p">)</span>
	<span class="p">((</span><span class="kt">uint16_t</span> <span class="o">*</span><span class="p">)</span><span class="n">client</span><span class="o">-&gt;</span><span class="n">rcSource</span><span class="p">)[</span><span class="n">x</span><span class="p">]</span> <span class="o">=</span> <span class="p">(</span><span class="kt">uint16_t</span><span class="p">)</span><span class="n">colors</span><span class="p">[</span><span class="n">client</span><span class="o">-&gt;</span><span class="n">rcSource</span><span class="p">[</span><span class="n">x</span> <span class="o">*</span> <span class="mi">2</span><span class="p">]];</span>
      <span class="k">break</span><span class="p">;</span>
    <span class="k">case</span> <span class="mi">4</span><span class="p">:</span>
      <span class="k">for</span> <span class="p">(</span><span class="n">x</span> <span class="o">=</span> <span class="mi">0</span><span class="p">;</span> <span class="n">x</span> <span class="o">&lt;</span> <span class="n">width</span> <span class="o">*</span> <span class="n">height</span><span class="p">;</span> <span class="n">x</span><span class="o">++</span><span class="p">)</span>
	<span class="p">((</span><span class="kt">uint32_t</span> <span class="o">*</span><span class="p">)</span><span class="n">client</span><span class="o">-&gt;</span><span class="n">rcSource</span><span class="p">)[</span><span class="n">x</span><span class="p">]</span> <span class="o">=</span> <span class="n">colors</span><span class="p">[</span><span class="n">client</span><span class="o">-&gt;</span><span class="n">rcSource</span><span class="p">[</span><span class="n">x</span> <span class="o">*</span> <span class="mi">4</span><span class="p">]];</span>
      <span class="k">break</span><span class="p">;</span>
    <span class="p">}</span>

  <span class="p">}</span> <span class="k">else</span> <span class="p">{</span>			<span class="cm">/* enc == rfbEncodingRichCursor */</span>

    <span class="k">if</span> <span class="p">(</span><span class="o">!</span><span class="n">ReadFromRFBServer</span><span class="p">(</span><span class="n">client</span><span class="p">,</span> <span class="p">(</span><span class="kt">char</span> <span class="o">*</span><span class="p">)</span><span class="n">client</span><span class="o">-&gt;</span><span class="n">rcSource</span><span class="p">,</span> <span class="n">width</span> <span class="o">*</span> <span class="n">height</span> <span class="o">*</span> <span class="n">bytesPerPixel</span><span class="p">))</span> <span class="p">{</span>
      <span class="n">free</span><span class="p">(</span><span class="n">client</span><span class="o">-&gt;</span><span class="n">rcSource</span><span class="p">);</span>
      <span class="n">client</span><span class="o">-&gt;</span><span class="n">rcSource</span> <span class="o">=</span> <span class="nb">NULL</span><span class="p">;</span>
      <span class="n">free</span><span class="p">(</span><span class="n">buf</span><span class="p">);</span>
      <span class="k">return</span> <span class="n">FALSE</span><span class="p">;</span>
    <span class="p">}</span>

  <span class="p">}</span>

  <span class="cm">/* Read and decode mask data. */</span>

  <span class="k">if</span> <span class="p">(</span><span class="o">!</span><span class="n">ReadFromRFBServer</span><span class="p">(</span><span class="n">client</span><span class="p">,</span> <span class="n">buf</span><span class="p">,</span> <span class="n">bytesMaskData</span><span class="p">))</span> <span class="p">{</span>
    <span class="n">free</span><span class="p">(</span><span class="n">client</span><span class="o">-&gt;</span><span class="n">rcSource</span><span class="p">);</span>
    <span class="n">client</span><span class="o">-&gt;</span><span class="n">rcSource</span> <span class="o">=</span> <span class="nb">NULL</span><span class="p">;</span>
    <span class="n">free</span><span class="p">(</span><span class="n">buf</span><span class="p">);</span>
    <span class="k">return</span> <span class="n">FALSE</span><span class="p">;</span>
  <span class="p">}</span>

  <span class="n">client</span><span class="o">-&gt;</span><span class="n">rcMask</span> <span class="o">=</span> <span class="n">malloc</span><span class="p">(</span><span class="n">width</span> <span class="o">*</span> <span class="n">height</span><span class="p">);</span>
  <span class="k">if</span> <span class="p">(</span><span class="n">client</span><span class="o">-&gt;</span><span class="n">rcMask</span> <span class="o">==</span> <span class="nb">NULL</span><span class="p">)</span> <span class="p">{</span>
    <span class="n">free</span><span class="p">(</span><span class="n">client</span><span class="o">-&gt;</span><span class="n">rcSource</span><span class="p">);</span>
    <span class="n">client</span><span class="o">-&gt;</span><span class="n">rcSource</span> <span class="o">=</span> <span class="nb">NULL</span><span class="p">;</span>
    <span class="n">free</span><span class="p">(</span><span class="n">buf</span><span class="p">);</span>
    <span class="k">return</span> <span class="n">FALSE</span><span class="p">;</span>
  <span class="p">}</span>

  <span class="n">ptr</span> <span class="o">=</span> <span class="n">client</span><span class="o">-&gt;</span><span class="n">rcMask</span><span class="p">;</span>
  <span class="k">for</span> <span class="p">(</span><span class="n">y</span> <span class="o">=</span> <span class="mi">0</span><span class="p">;</span> <span class="n">y</span> <span class="o">&lt;</span> <span class="n">height</span><span class="p">;</span> <span class="n">y</span><span class="o">++</span><span class="p">)</span> <span class="p">{</span>
    <span class="k">for</span> <span class="p">(</span><span class="n">x</span> <span class="o">=</span> <span class="mi">0</span><span class="p">;</span> <span class="n">x</span> <span class="o">&lt;</span> <span class="n">width</span> <span class="o">/</span> <span class="mi">8</span><span class="p">;</span> <span class="n">x</span><span class="o">++</span><span class="p">)</span> <span class="p">{</span>
      <span class="k">for</span> <span class="p">(</span><span class="n">b</span> <span class="o">=</span> <span class="mi">7</span><span class="p">;</span> <span class="n">b</span> <span class="o">&gt;=</span> <span class="mi">0</span><span class="p">;</span> <span class="n">b</span><span class="o">--</span><span class="p">)</span> <span class="p">{</span>
	<span class="o">*</span><span class="n">ptr</span><span class="o">++</span> <span class="o">=</span> <span class="n">buf</span><span class="p">[</span><span class="n">y</span> <span class="o">*</span> <span class="n">bytesPerRow</span> <span class="o">+</span> <span class="n">x</span><span class="p">]</span> <span class="o">&gt;&gt;</span> <span class="n">b</span> <span class="o">&amp;</span> <span class="mi">1</span><span class="p">;</span>
      <span class="p">}</span>
    <span class="p">}</span>
    <span class="k">for</span> <span class="p">(</span><span class="n">b</span> <span class="o">=</span> <span class="mi">7</span><span class="p">;</span> <span class="n">b</span> <span class="o">&gt;</span> <span class="mi">7</span> <span class="o">-</span> <span class="n">width</span> <span class="o">%</span> <span class="mi">8</span><span class="p">;</span> <span class="n">b</span><span class="o">--</span><span class="p">)</span> <span class="p">{</span>
      <span class="o">*</span><span class="n">ptr</span><span class="o">++</span> <span class="o">=</span> <span class="n">buf</span><span class="p">[</span><span class="n">y</span> <span class="o">*</span> <span class="n">bytesPerRow</span> <span class="o">+</span> <span class="n">x</span><span class="p">]</span> <span class="o">&gt;&gt;</span> <span class="n">b</span> <span class="o">&amp;</span> <span class="mi">1</span><span class="p">;</span>
    <span class="p">}</span>
  <span class="p">}</span>

  <span class="k">if</span> <span class="p">(</span><span class="n">client</span><span class="o">-&gt;</span><span class="n">GotCursorShape</span> <span class="o">!=</span> <span class="nb">NULL</span><span class="p">)</span> <span class="p">{</span>
     <span class="n">client</span><span class="o">-&gt;</span><span class="n">GotCursorShape</span><span class="p">(</span><span class="n">client</span><span class="p">,</span> <span class="n">xhot</span><span class="p">,</span> <span class="n">yhot</span><span class="p">,</span> <span class="n">width</span><span class="p">,</span> <span class="n">height</span><span class="p">,</span> <span class="n">bytesPerPixel</span><span class="p">);</span>
  <span class="p">}</span>

  <span class="n">free</span><span class="p">(</span><span class="n">buf</span><span class="p">);</span>

  <span class="k">return</span> <span class="n">TRUE</span><span class="p">;</span>
<span class="p">}</span>

</code></pre></div></div>

<p>When handling <code class="language-plaintext highlighter-rouge">rfbFramebufferUpdate</code> RFB messages, the <code class="language-plaintext highlighter-rouge">libvnclient</code> code will check whether <code class="language-plaintext highlighter-rouge">rect.encoding</code> is set to <code class="language-plaintext highlighter-rouge">rfbEncodingXcursor</code> or <code class="language-plaintext highlighter-rouge">rfbEncodingRichcursor</code>. If this is the case, it will then pass remote (server side) controlled 16bit integer values as parameters into <code class="language-plaintext highlighter-rouge">HandleCursorShape</code>. This includes the <code class="language-plaintext highlighter-rouge">xhot</code>, <code class="language-plaintext highlighter-rouge">yhot</code>, <code class="language-plaintext highlighter-rouge">width</code>, <code class="language-plaintext highlighter-rouge">height</code> and <code class="language-plaintext highlighter-rouge">enc</code> parameters.</p>

<p>At [1] we observe a 32bit integer arithmetic expression that involves the <code class="language-plaintext highlighter-rouge">width</code>, <code class="language-plaintext highlighter-rouge">height</code> and <code class="language-plaintext highlighter-rouge">bytesPerPixel</code> integers. A malicious VNC server can control up to 16bits of the <code class="language-plaintext highlighter-rouge">width</code> and <code class="language-plaintext highlighter-rouge">height</code> integers, and it may set the <code class="language-plaintext highlighter-rouge">bytesPerPixel</code> integer to <code class="language-plaintext highlighter-rouge">1</code>,<code class="language-plaintext highlighter-rouge">2</code> or <code class="language-plaintext highlighter-rouge">4</code> based on its control over the “Bits Per Pixel” value of the session (8bits, 24bits, or 32bits, divided by 8).</p>

<p>This level of control over the allocation size integer arithmetic expression allows a malicious VNC server to induce an integer overflow and subsequently under-allocate the intended <code class="language-plaintext highlighter-rouge">client-&gt;rcSource</code> memory region.</p>

<p>The subsequent population of this memory region is based on the <code class="language-plaintext highlighter-rouge">width</code> and <code class="language-plaintext highlighter-rouge">height</code> parameters, which will in turn result in potentially exploitable memory tresspasses.</p>

<h3 id="impact">Impact</h3>

<p>It is possible to craft this vulnerability into a remote heap overflow which, under the right circumstances, may result in remote code execution. However, due to the specifics of the integer overwrap which results in a fairly limited range allocation control vs overflow length, we do not consider this likely.</p>

<h2 id="cve">CVE</h2>

<ul>
  <li>CVE-2019-20788</li>
</ul>

<h2 id="coordinated-disclosure-timeline">Coordinated Disclosure Timeline</h2>

<ul>
  <li>04/10/2020: maintainer contacted</li>
  <li>04/10/2020: maintainer notes issue has already been fixed in master</li>
  <li>04/10/2020: GHSL suggests further triage due to distributions shipping vulnerable versions</li>
  <li>04/23/2020: CVE assigned</li>
  <li>04/23/2020: GHSL agrees to delay public advisory until 0.9.13 stable is released</li>
  <li>06/01/2020: GHSL requests release timeline update from maintainer</li>
  <li>06/13/2020: 0.9.13 stable released</li>
</ul>

<h2 id="resources">Resources</h2>

<ul>
  <li><a href="https://github.com/LibVNC/libvncserver/commit/54220248886b5001fbbb9fa73c4e1a2cb9413fed#diff-8963122010aecb6910aeca7f70d1eb3d">fix commit</a></li>
</ul>

<h2 id="credit">Credit</h2>

<p>This issue was discovered and reported by the <a href="https://securitylab.github.com">GitHub Security Lab</a>.</p>

<h2 id="contact">Contact</h2>

<p>You can contact the GHSL team at <code class="language-plaintext highlighter-rouge">securitylab@github.com</code>, please include <code class="language-plaintext highlighter-rouge">GHSL-2020-064</code> in any communication regarding this issue.</p>