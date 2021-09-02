<header class="post-header d-block mb-6">
      <div class="date text-mono f5 my-3">June 17, 2020</div>
      <h1 class="my-2 h00-mktg lh-condensed">GHSL-2020-075, GHSL-2020-079, GHSL-2020-080, GHSL-2020-081, GHSL-2020-082, GHSL-2020-083, GHSL-2020-084: Multiple vulnerabilities in SANE Backends (DoS, RCE)</h1>

      
      
      
      
      

      

      <a target="_blank" class="sc-frDJqD SgxRc d-inline-flex flex-row flex-items-center text-gray" href="https://github.com/kevinbackhouse">
        <img class="mr-3" src="https://avatars.githubusercontent.com/u/4358136?s=35" height="35" width="35">
        <span>Kevin Backhouse</span>
      </a>
    </header>

    <main id="content" class="markdown-body" aria-label="Content">
      <h2 id="summary">Summary</h2>

<p><a href="https://gitlab.com/sane-project/backends">SANE Backends</a> contains several memory corruption vulnerabilities which can be triggered by a malicious device or computer that is connected to the same network. The vulnerabilities are triggered when an application such as <a href="http://manpages.ubuntu.com/manpages/bionic/man1/simple-scan.1.html">simple-scan</a> searches the network for scanners. In the specific case of simple-scan, this happens immediately when simple-scan starts, so there isn’t even any need to trick the user into thinking that the scanner is genuine so that they will click on it.</p>

<p>We have also identified some other vulnerabilities in SANE Backends, which are less severe because they <em>do</em> require the user to click the “Scan” button after connecting to a malicious device.</p>

<h2 id="product">Product</h2>

<p><a href="https://gitlab.com/sane-project/backends">SANE Backends</a></p>

<h2 id="tested-version">Tested Version</h2>

<p><a href="https://packages.ubuntu.com/bionic/libsane1">libsane1</a> 1.0.27-1~experimental3ubuntu2.2, tested on Ubuntu 18.04.4 LTS with <a href="https://packages.ubuntu.com/bionic/simple-scan">simple-scan</a> 3.28.0-0ubuntu1.</p>

<h2 id="details">Details</h2>

<h3 id="issue-1-ghsl-2020-075-cve-2020-12867-null-pointer-dereference-in-sanei_epson_net_read">Issue 1 (<code class="language-plaintext highlighter-rouge">GHSL-2020-075</code>, <code class="language-plaintext highlighter-rouge">CVE-2020-12867</code>): null pointer dereference in <code class="language-plaintext highlighter-rouge">sanei_epson_net_read</code></h3>

<p>The function <a href="https://gitlab.com/sane-project/backends/-/blob/1.0.27/backend/epson2_net.c#L66"><code class="language-plaintext highlighter-rouge">sanei_epson_net_read</code></a> has buggy code for handling the situation where it receives a response with an unexpected size:</p>

<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="cm">/* receive net header */</span>
<span class="n">size</span> <span class="o">=</span> <span class="n">sanei_epson_net_read_raw</span><span class="p">(</span><span class="n">s</span><span class="p">,</span> <span class="n">header</span><span class="p">,</span> <span class="mi">12</span><span class="p">,</span> <span class="n">status</span><span class="p">);</span>
<span class="k">if</span> <span class="p">(</span><span class="n">size</span> <span class="o">!=</span> <span class="mi">12</span><span class="p">)</span> <span class="p">{</span>
  <span class="k">return</span> <span class="mi">0</span><span class="p">;</span>
<span class="p">}</span>

<span class="k">if</span> <span class="p">(</span><span class="n">header</span><span class="p">[</span><span class="mi">0</span><span class="p">]</span> <span class="o">!=</span> <span class="sc">'I'</span> <span class="o">||</span> <span class="n">header</span><span class="p">[</span><span class="mi">1</span><span class="p">]</span> <span class="o">!=</span> <span class="sc">'S'</span><span class="p">)</span> <span class="p">{</span>
  <span class="n">DBG</span><span class="p">(</span><span class="mi">1</span><span class="p">,</span> <span class="s">"header mismatch: %02X %02x</span><span class="se">\n</span><span class="s">"</span><span class="p">,</span> <span class="n">header</span><span class="p">[</span><span class="mi">0</span><span class="p">],</span> <span class="n">header</span><span class="p">[</span><span class="mi">1</span><span class="p">]);</span>
  <span class="o">*</span><span class="n">status</span> <span class="o">=</span> <span class="n">SANE_STATUS_IO_ERROR</span><span class="p">;</span>
  <span class="k">return</span> <span class="mi">0</span><span class="p">;</span>
<span class="p">}</span>

<span class="n">size</span> <span class="o">=</span> <span class="n">be32atoh</span><span class="p">(</span><span class="o">&amp;</span><span class="n">header</span><span class="p">[</span><span class="mi">6</span><span class="p">]);</span>  <span class="o">&lt;=====</span> <span class="n">size</span> <span class="n">is</span> <span class="n">controlled</span> <span class="n">by</span> <span class="n">attacker</span>

<span class="nf">DBG</span><span class="p">(</span><span class="mi">23</span><span class="p">,</span> <span class="s">"%s: wanted = %lu, available = %lu</span><span class="se">\n</span><span class="s">"</span><span class="p">,</span> <span class="n">__func__</span><span class="p">,</span>
  <span class="p">(</span><span class="n">u_long</span><span class="p">)</span> <span class="n">wanted</span><span class="p">,</span> <span class="p">(</span><span class="n">u_long</span><span class="p">)</span> <span class="n">size</span><span class="p">);</span>

<span class="o">*</span><span class="n">status</span> <span class="o">=</span> <span class="n">SANE_STATUS_GOOD</span><span class="p">;</span>

<span class="k">if</span> <span class="p">(</span><span class="n">size</span> <span class="o">==</span> <span class="n">wanted</span><span class="p">)</span> <span class="p">{</span>

  <span class="n">DBG</span><span class="p">(</span><span class="mi">15</span><span class="p">,</span> <span class="s">"%s: full read</span><span class="se">\n</span><span class="s">"</span><span class="p">,</span> <span class="n">__func__</span><span class="p">);</span>

  <span class="n">read</span> <span class="o">=</span> <span class="n">sanei_epson_net_read_raw</span><span class="p">(</span><span class="n">s</span><span class="p">,</span> <span class="n">buf</span><span class="p">,</span> <span class="n">size</span><span class="p">,</span> <span class="n">status</span><span class="p">);</span>

  <span class="k">if</span> <span class="p">(</span><span class="n">s</span><span class="o">-&gt;</span><span class="n">netbuf</span><span class="p">)</span> <span class="p">{</span>
    <span class="n">free</span><span class="p">(</span><span class="n">s</span><span class="o">-&gt;</span><span class="n">netbuf</span><span class="p">);</span>
    <span class="n">s</span><span class="o">-&gt;</span><span class="n">netbuf</span> <span class="o">=</span> <span class="nb">NULL</span><span class="p">;</span>
    <span class="n">s</span><span class="o">-&gt;</span><span class="n">netlen</span> <span class="o">=</span> <span class="mi">0</span><span class="p">;</span>
  <span class="p">}</span>

  <span class="k">if</span> <span class="p">(</span><span class="n">read</span> <span class="o">&lt;</span> <span class="mi">0</span><span class="p">)</span> <span class="p">{</span>
    <span class="k">return</span> <span class="mi">0</span><span class="p">;</span>
  <span class="p">}</span>

<span class="cm">/*  } else if (wanted &lt; size &amp;&amp; s-&gt;netlen == size) { */</span>
<span class="p">}</span> <span class="k">else</span> <span class="p">{</span>
  <span class="n">DBG</span><span class="p">(</span><span class="mi">23</span><span class="p">,</span> <span class="s">"%s: partial read</span><span class="se">\n</span><span class="s">"</span><span class="p">,</span> <span class="n">__func__</span><span class="p">);</span>

  <span class="n">read</span> <span class="o">=</span> <span class="n">sanei_epson_net_read_raw</span><span class="p">(</span><span class="n">s</span><span class="p">,</span> <span class="n">s</span><span class="o">-&gt;</span><span class="n">netbuf</span><span class="p">,</span> <span class="n">size</span><span class="p">,</span> <span class="n">status</span><span class="p">);</span>  <span class="o">&lt;=====</span> <span class="n">s</span><span class="o">-&gt;</span><span class="n">netbuf</span> <span class="n">could</span> <span class="n">be</span> <span class="nb">NULL</span>
  <span class="k">if</span> <span class="p">(</span><span class="n">read</span> <span class="o">!=</span> <span class="n">size</span><span class="p">)</span> <span class="p">{</span>
    <span class="k">return</span> <span class="mi">0</span><span class="p">;</span>
  <span class="p">}</span>

  <span class="n">s</span><span class="o">-&gt;</span><span class="n">netlen</span> <span class="o">=</span> <span class="n">size</span> <span class="o">-</span> <span class="n">wanted</span><span class="p">;</span>
  <span class="n">s</span><span class="o">-&gt;</span><span class="n">netptr</span> <span class="o">+=</span> <span class="n">wanted</span><span class="p">;</span>
  <span class="n">read</span> <span class="o">=</span> <span class="n">wanted</span><span class="p">;</span>

  <span class="n">DBG</span><span class="p">(</span><span class="mi">23</span><span class="p">,</span> <span class="s">"0,4 %02x %02x</span><span class="se">\n</span><span class="s">"</span><span class="p">,</span> <span class="n">s</span><span class="o">-&gt;</span><span class="n">netbuf</span><span class="p">[</span><span class="mi">0</span><span class="p">],</span> <span class="n">s</span><span class="o">-&gt;</span><span class="n">netbuf</span><span class="p">[</span><span class="mi">4</span><span class="p">]);</span>  <span class="o">&lt;=====</span> <span class="n">s</span><span class="o">-&gt;</span><span class="n">netbuf</span> <span class="n">could</span> <span class="n">be</span> <span class="nb">NULL</span>
  <span class="n">DBG</span><span class="p">(</span><span class="mi">23</span><span class="p">,</span> <span class="s">"storing %lu to buffer at %p, next read at %p, %lu bytes left</span><span class="se">\n</span><span class="s">"</span><span class="p">,</span>
    <span class="p">(</span><span class="n">u_long</span><span class="p">)</span> <span class="n">size</span><span class="p">,</span> <span class="n">s</span><span class="o">-&gt;</span><span class="n">netbuf</span><span class="p">,</span> <span class="n">s</span><span class="o">-&gt;</span><span class="n">netptr</span><span class="p">,</span> <span class="p">(</span><span class="n">u_long</span><span class="p">)</span> <span class="n">s</span><span class="o">-&gt;</span><span class="n">netlen</span><span class="p">);</span>

  <span class="n">memcpy</span><span class="p">(</span><span class="n">buf</span><span class="p">,</span> <span class="n">s</span><span class="o">-&gt;</span><span class="n">netbuf</span><span class="p">,</span> <span class="n">wanted</span><span class="p">);</span>
<span class="p">}</span>

<span class="k">return</span> <span class="n">read</span><span class="p">;</span>
</code></pre></div></div>

<p>Notice that the value of <code class="language-plaintext highlighter-rouge">size</code> is read from an incoming message, so an attacker can set it to any value they like. In the <code class="language-plaintext highlighter-rouge">else</code> branch, which handles the case where <code class="language-plaintext highlighter-rouge">size != wanted</code>, there is no check that <code class="language-plaintext highlighter-rouge">s-&gt;netbuf</code> is large enough for <code class="language-plaintext highlighter-rouge">size</code> bytes. This could potentially lead to a buffer overflow. However, our proof-of-concept exploit for this bug triggers a case where <code class="language-plaintext highlighter-rouge">s-&gt;netbuf</code> hasn’t even been initialized so the program crashes due to a null pointer dereference, rather than a buffer overflow.</p>

<h4 id="impact">Impact</h4>

<p>This issue may lead to remote denial of service, where “remote” means a device or computer connected to the same network as the victim. For example, in a typical office environment the malicious device would need to be somewhere inside the building. Because the vulnerability causes <code class="language-plaintext highlighter-rouge">simple-scan</code> to crash as soon as it starts, it makes the application unusable.</p>

<h3 id="issue-2-ghsl-2020-079-cve-2020-12866-null-pointer-dereference-in-epsonds_net_read">Issue 2 (<code class="language-plaintext highlighter-rouge">GHSL-2020-079</code>, <code class="language-plaintext highlighter-rouge">CVE-2020-12866</code>): null pointer dereference in <code class="language-plaintext highlighter-rouge">epsonds_net_read</code></h3>

<p>The function <a href="https://gitlab.com/sane-project/backends/-/blob/1.0.27/backend/epsonds-net.c#L66"><code class="language-plaintext highlighter-rouge">epsonds_net_read</code></a> has buggy code for handling the situation where it receives a response with an unexpected size:</p>

<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="cm">/* receive net header */</span>
<span class="n">size</span> <span class="o">=</span> <span class="n">epsonds_net_read_raw</span><span class="p">(</span><span class="n">s</span><span class="p">,</span> <span class="n">header</span><span class="p">,</span> <span class="mi">12</span><span class="p">,</span> <span class="n">status</span><span class="p">);</span>
<span class="k">if</span> <span class="p">(</span><span class="n">size</span> <span class="o">!=</span> <span class="mi">12</span><span class="p">)</span> <span class="p">{</span>
  <span class="k">return</span> <span class="mi">0</span><span class="p">;</span>
<span class="p">}</span>

<span class="k">if</span> <span class="p">(</span><span class="n">header</span><span class="p">[</span><span class="mi">0</span><span class="p">]</span> <span class="o">!=</span> <span class="sc">'I'</span> <span class="o">||</span> <span class="n">header</span><span class="p">[</span><span class="mi">1</span><span class="p">]</span> <span class="o">!=</span> <span class="sc">'S'</span><span class="p">)</span> <span class="p">{</span>
  <span class="n">DBG</span><span class="p">(</span><span class="mi">1</span><span class="p">,</span> <span class="s">"header mismatch: %02X %02x</span><span class="se">\n</span><span class="s">"</span><span class="p">,</span> <span class="n">header</span><span class="p">[</span><span class="mi">0</span><span class="p">],</span> <span class="n">header</span><span class="p">[</span><span class="mi">1</span><span class="p">]);</span>
  <span class="o">*</span><span class="n">status</span> <span class="o">=</span> <span class="n">SANE_STATUS_IO_ERROR</span><span class="p">;</span>
  <span class="k">return</span> <span class="mi">0</span><span class="p">;</span>
<span class="p">}</span>

<span class="c1">// incoming payload size</span>
<span class="n">size</span> <span class="o">=</span> <span class="n">be32atoh</span><span class="p">(</span><span class="o">&amp;</span><span class="n">header</span><span class="p">[</span><span class="mi">6</span><span class="p">]);</span>

<span class="n">DBG</span><span class="p">(</span><span class="mi">23</span><span class="p">,</span> <span class="s">"%s: wanted = %lu, available = %lu</span><span class="se">\n</span><span class="s">"</span><span class="p">,</span> <span class="n">__func__</span><span class="p">,</span>
  <span class="p">(</span><span class="n">u_long</span><span class="p">)</span> <span class="n">wanted</span><span class="p">,</span> <span class="p">(</span><span class="n">u_long</span><span class="p">)</span> <span class="n">size</span><span class="p">);</span>

<span class="o">*</span><span class="n">status</span> <span class="o">=</span> <span class="n">SANE_STATUS_GOOD</span><span class="p">;</span>

<span class="k">if</span> <span class="p">(</span><span class="n">size</span> <span class="o">==</span> <span class="n">wanted</span><span class="p">)</span> <span class="p">{</span>

  <span class="n">DBG</span><span class="p">(</span><span class="mi">15</span><span class="p">,</span> <span class="s">"%s: full read</span><span class="se">\n</span><span class="s">"</span><span class="p">,</span> <span class="n">__func__</span><span class="p">);</span>

  <span class="k">if</span> <span class="p">(</span><span class="n">size</span><span class="p">)</span> <span class="p">{</span>
    <span class="n">read</span> <span class="o">=</span> <span class="n">epsonds_net_read_raw</span><span class="p">(</span><span class="n">s</span><span class="p">,</span> <span class="n">buf</span><span class="p">,</span> <span class="n">size</span><span class="p">,</span> <span class="n">status</span><span class="p">);</span>
  <span class="p">}</span>

  <span class="k">if</span> <span class="p">(</span><span class="n">s</span><span class="o">-&gt;</span><span class="n">netbuf</span><span class="p">)</span> <span class="p">{</span>
    <span class="n">free</span><span class="p">(</span><span class="n">s</span><span class="o">-&gt;</span><span class="n">netbuf</span><span class="p">);</span>
    <span class="n">s</span><span class="o">-&gt;</span><span class="n">netbuf</span> <span class="o">=</span> <span class="nb">NULL</span><span class="p">;</span>
    <span class="n">s</span><span class="o">-&gt;</span><span class="n">netlen</span> <span class="o">=</span> <span class="mi">0</span><span class="p">;</span>
  <span class="p">}</span>

  <span class="k">if</span> <span class="p">(</span><span class="n">read</span> <span class="o">&lt;</span> <span class="mi">0</span><span class="p">)</span> <span class="p">{</span>
    <span class="k">return</span> <span class="mi">0</span><span class="p">;</span>
  <span class="p">}</span>

<span class="p">}</span> <span class="k">else</span> <span class="nf">if</span> <span class="p">(</span><span class="n">wanted</span> <span class="o">&lt;</span> <span class="n">size</span><span class="p">)</span> <span class="p">{</span>

  <span class="n">DBG</span><span class="p">(</span><span class="mi">23</span><span class="p">,</span> <span class="s">"%s: long tail</span><span class="se">\n</span><span class="s">"</span><span class="p">,</span> <span class="n">__func__</span><span class="p">);</span>

  <span class="n">read</span> <span class="o">=</span> <span class="n">epsonds_net_read_raw</span><span class="p">(</span><span class="n">s</span><span class="p">,</span> <span class="n">s</span><span class="o">-&gt;</span><span class="n">netbuf</span><span class="p">,</span> <span class="n">size</span><span class="p">,</span> <span class="n">status</span><span class="p">);</span>  <span class="o">&lt;=====</span> <span class="n">no</span> <span class="n">bounds</span> <span class="n">check</span>
  <span class="k">if</span> <span class="p">(</span><span class="n">read</span> <span class="o">!=</span> <span class="n">size</span><span class="p">)</span> <span class="p">{</span>
    <span class="k">return</span> <span class="mi">0</span><span class="p">;</span>
  <span class="p">}</span>

  <span class="n">memcpy</span><span class="p">(</span><span class="n">buf</span><span class="p">,</span> <span class="n">s</span><span class="o">-&gt;</span><span class="n">netbuf</span><span class="p">,</span> <span class="n">wanted</span><span class="p">);</span>
  <span class="n">read</span> <span class="o">=</span> <span class="n">wanted</span><span class="p">;</span>

  <span class="n">free</span><span class="p">(</span><span class="n">s</span><span class="o">-&gt;</span><span class="n">netbuf</span><span class="p">);</span>
  <span class="n">s</span><span class="o">-&gt;</span><span class="n">netbuf</span> <span class="o">=</span> <span class="nb">NULL</span><span class="p">;</span>
  <span class="n">s</span><span class="o">-&gt;</span><span class="n">netlen</span> <span class="o">=</span> <span class="mi">0</span><span class="p">;</span>

<span class="p">}</span> <span class="k">else</span> <span class="p">{</span>

  <span class="n">DBG</span><span class="p">(</span><span class="mi">23</span><span class="p">,</span> <span class="s">"%s: partial read</span><span class="se">\n</span><span class="s">"</span><span class="p">,</span> <span class="n">__func__</span><span class="p">);</span>

  <span class="n">read</span> <span class="o">=</span> <span class="n">epsonds_net_read_raw</span><span class="p">(</span><span class="n">s</span><span class="p">,</span> <span class="n">s</span><span class="o">-&gt;</span><span class="n">netbuf</span><span class="p">,</span> <span class="n">size</span><span class="p">,</span> <span class="n">status</span><span class="p">);</span>
  <span class="k">if</span> <span class="p">(</span><span class="n">read</span> <span class="o">!=</span> <span class="n">size</span><span class="p">)</span> <span class="p">{</span>
    <span class="k">return</span> <span class="mi">0</span><span class="p">;</span>
  <span class="p">}</span>

  <span class="n">s</span><span class="o">-&gt;</span><span class="n">netlen</span> <span class="o">=</span> <span class="n">size</span> <span class="o">-</span> <span class="n">wanted</span><span class="p">;</span>  <span class="o">&lt;=====</span> <span class="n">negative</span> <span class="n">integer</span> <span class="n">overflow</span> <span class="p">(</span><span class="n">because</span> <span class="n">size</span> <span class="o">&lt;</span> <span class="n">wanted</span><span class="p">)</span>
  <span class="n">s</span><span class="o">-&gt;</span><span class="n">netptr</span> <span class="o">+=</span> <span class="n">wanted</span><span class="p">;</span>
  <span class="n">read</span> <span class="o">=</span> <span class="n">wanted</span><span class="p">;</span>

  <span class="n">DBG</span><span class="p">(</span><span class="mi">23</span><span class="p">,</span> <span class="s">"0,4 %02x %02x</span><span class="se">\n</span><span class="s">"</span><span class="p">,</span> <span class="n">s</span><span class="o">-&gt;</span><span class="n">netbuf</span><span class="p">[</span><span class="mi">0</span><span class="p">],</span> <span class="n">s</span><span class="o">-&gt;</span><span class="n">netbuf</span><span class="p">[</span><span class="mi">4</span><span class="p">]);</span>
  <span class="n">DBG</span><span class="p">(</span><span class="mi">23</span><span class="p">,</span> <span class="s">"storing %lu to buffer at %p, next read at %p, %lu bytes left</span><span class="se">\n</span><span class="s">"</span><span class="p">,</span>
    <span class="p">(</span><span class="n">u_long</span><span class="p">)</span> <span class="n">size</span><span class="p">,</span> <span class="n">s</span><span class="o">-&gt;</span><span class="n">netbuf</span><span class="p">,</span> <span class="n">s</span><span class="o">-&gt;</span><span class="n">netptr</span><span class="p">,</span> <span class="p">(</span><span class="n">u_long</span><span class="p">)</span> <span class="n">s</span><span class="o">-&gt;</span><span class="n">netlen</span><span class="p">);</span>

  <span class="n">memcpy</span><span class="p">(</span><span class="n">buf</span><span class="p">,</span> <span class="n">s</span><span class="o">-&gt;</span><span class="n">netbuf</span><span class="p">,</span> <span class="n">wanted</span><span class="p">);</span>  <span class="o">&lt;=====</span> <span class="n">no</span> <span class="n">bounds</span> <span class="n">check</span>
<span class="p">}</span>

<span class="k">return</span> <span class="n">read</span><span class="p">;</span>
</code></pre></div></div>

<p>This code is very similar to the code in <code class="language-plaintext highlighter-rouge">epson2_net.c</code> (see issue 1) and has similar bugs. The first of these is a NULL pointer exception at <a href="https://gitlab.com/sane-project/backends/-/blob/1.0.27/backend/epsonds-net.c#L160">epsonds-net.c, line 160</a>.</p>

<h4 id="impact-1">Impact</h4>

<p>This issue may lead to remote denial of service, where “remote” means a device or computer connected to the same network as the victim. For example, in a typical office environment the malicious device would need to be somewhere inside the building. Because the vulnerability causes <code class="language-plaintext highlighter-rouge">simple-scan</code> to crash as soon as it starts, it makes the application unusable.</p>

<h3 id="issue-3-ghsl-2020-080-cve-2020-12861-heap-buffer-overflow-in-epsonds_net_read">Issue 3 (<code class="language-plaintext highlighter-rouge">GHSL-2020-080</code>, <code class="language-plaintext highlighter-rouge">CVE-2020-12861</code>): heap buffer overflow in <code class="language-plaintext highlighter-rouge">epsonds_net_read</code></h3>

<p>This bug is in the same function as issue 2: <code class="language-plaintext highlighter-rouge">epsonds_net_read</code>. There is a heap buffer overflow at <a href="https://gitlab.com/sane-project/backends/-/blob/1.0.27/backend/epsonds-net.c#L135">epsonds-net.c, line 135</a>. The value of <code class="language-plaintext highlighter-rouge">size</code> is controlled by the attacker, so an arbitrary amount of attacker-controlled data is written to <code class="language-plaintext highlighter-rouge">s-&gt;netbuf</code>.</p>

<h4 id="impact-2">Impact</h4>

<p>This issue may lead to remote code execution, where “remote” means a device or computer connected to the same network as the victim. For example, in a typical office environment the malicious device would need to be somewhere inside the building.</p>

<h3 id="issue-4-ghsl-2020-081-cve-2020-12864-reading-uninitialized-data-in-epsonds_net_read">Issue 4 (<code class="language-plaintext highlighter-rouge">GHSL-2020-081</code>, <code class="language-plaintext highlighter-rouge">CVE-2020-12864</code>): reading uninitialized data in <code class="language-plaintext highlighter-rouge">epsonds_net_read</code></h3>

<p>This bug is in the same function as issue 2: <code class="language-plaintext highlighter-rouge">epsonds_net_read</code>. The <code class="language-plaintext highlighter-rouge">memcpy</code> at <a href="https://gitlab.com/sane-project/backends/-/blob/1.0.27/backend/epsonds-net.c#L164">epsonds-net.c, line 164</a> can read uninitialized data. The value of <code class="language-plaintext highlighter-rouge">size</code> is controlled by the attacker, so the attacker can specify that <code class="language-plaintext highlighter-rouge">size == 0</code>. Since <code class="language-plaintext highlighter-rouge">s-&gt;netbuf</code> is a newly allocated heap buffer, it contains uninitialized memory.</p>

<h4 id="impact-3">Impact</h4>

<p>By itself, the severity of this issue is very low. However, it may be very useful to an attacker who is attempting to exploit one of the buffer overflow vulnerabilities, such as issue 3, because it may enable the attacker to obtain the ASLR offsets of the program.</p>

<h3 id="issue-5-ghsl-2020-082-cve-2020-12862-out-of-bounds-read-in-decode_binary">Issue 5 (<code class="language-plaintext highlighter-rouge">GHSL-2020-082</code>, <code class="language-plaintext highlighter-rouge">CVE-2020-12862</code>): out-of-bounds read in <code class="language-plaintext highlighter-rouge">decode_binary</code></h3>

<p>The function <a href="https://gitlab.com/sane-project/backends/-/blob/1.0.27/backend/epsonds-cmd.c#L258"><code class="language-plaintext highlighter-rouge">decode_binary</code></a> has an out-of-bounds read:</p>

<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="cm">/* h000 */</span>
<span class="k">static</span> <span class="kt">char</span> <span class="o">*</span><span class="nf">decode_binary</span><span class="p">(</span><span class="kt">char</span> <span class="o">*</span><span class="n">buf</span><span class="p">)</span>
<span class="p">{</span>
  <span class="kt">char</span> <span class="n">tmp</span><span class="p">[</span><span class="mi">6</span><span class="p">];</span>
  <span class="kt">int</span> <span class="n">hl</span><span class="p">;</span>

  <span class="n">memcpy</span><span class="p">(</span><span class="n">tmp</span><span class="p">,</span> <span class="n">buf</span><span class="p">,</span> <span class="mi">4</span><span class="p">);</span>
  <span class="n">tmp</span><span class="p">[</span><span class="mi">4</span><span class="p">]</span> <span class="o">=</span> <span class="sc">'\0'</span><span class="p">;</span>

  <span class="k">if</span> <span class="p">(</span><span class="n">buf</span><span class="p">[</span><span class="mi">0</span><span class="p">]</span> <span class="o">!=</span> <span class="sc">'h'</span><span class="p">)</span>
    <span class="k">return</span> <span class="nb">NULL</span><span class="p">;</span>

  <span class="n">hl</span> <span class="o">=</span> <span class="n">strtol</span><span class="p">(</span><span class="n">tmp</span> <span class="o">+</span> <span class="mi">1</span><span class="p">,</span> <span class="nb">NULL</span><span class="p">,</span> <span class="mi">16</span><span class="p">);</span>
  <span class="k">if</span> <span class="p">(</span><span class="n">hl</span><span class="p">)</span> <span class="p">{</span>

    <span class="kt">char</span> <span class="o">*</span><span class="n">v</span> <span class="o">=</span> <span class="n">malloc</span><span class="p">(</span><span class="n">hl</span> <span class="o">+</span> <span class="mi">1</span><span class="p">);</span>
    <span class="n">memcpy</span><span class="p">(</span><span class="n">v</span><span class="p">,</span> <span class="n">buf</span> <span class="o">+</span> <span class="mi">4</span><span class="p">,</span> <span class="n">hl</span><span class="p">);</span>
    <span class="n">v</span><span class="p">[</span><span class="n">hl</span><span class="p">]</span> <span class="o">=</span> <span class="sc">'\0'</span><span class="p">;</span>

    <span class="k">return</span> <span class="n">v</span><span class="p">;</span>
  <span class="p">}</span>

  <span class="k">return</span> <span class="nb">NULL</span><span class="p">;</span>
<span class="p">}</span>
</code></pre></div></div>

<p>The value of <code class="language-plaintext highlighter-rouge">hl</code> is controlled by the attacker and can be any value between 0 and 0xFFF (4095). <code class="language-plaintext highlighter-rouge">buf</code> is a pointer to a 64 byte stack buffer (<code class="language-plaintext highlighter-rouge">rbuf</code> in <a href="https://gitlab.com/sane-project/backends/-/blob/1.0.27/backend/epsonds-cmd.c#L136"><code class="language-plaintext highlighter-rouge">esci2_cmd</code></a>), so the memcpy at line 273 can copy up to 4095 bytes from the stack into the newly allocated buffer.</p>

<h4 id="impact-4">Impact</h4>

<p>By itself, the severity of this issue is very low. However, it may be very useful to an attacker who is attempting to exploit one of the buffer overflow vulnerabilities, such as issue 3, because it may enable the attacker to obtain the ASLR offsets of the program.</p>

<h3 id="issue-6-ghsl-2020-083-cve-2020-12863-out-of-bounds-read-in-esci2_check_header">Issue 6 (<code class="language-plaintext highlighter-rouge">GHSL-2020-083</code>, <code class="language-plaintext highlighter-rouge">CVE-2020-12863</code>): out-of-bounds read in <code class="language-plaintext highlighter-rouge">esci2_check_header</code></h3>

<p><a href="https://gitlab.com/sane-project/backends/-/blob/1.0.27/backend/epsonds-cmd.c#L93"><code class="language-plaintext highlighter-rouge">esci2_check_header</code></a> uses <code class="language-plaintext highlighter-rouge">sscanf</code> to read a number from the message:</p>

<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="cm">/* INFOx0000100#.... */</span>

<span class="cm">/* read the answer len */</span>
<span class="k">if</span> <span class="p">(</span><span class="n">buf</span><span class="p">[</span><span class="mi">4</span><span class="p">]</span> <span class="o">!=</span> <span class="sc">'x'</span><span class="p">)</span> <span class="p">{</span>
  <span class="n">DBG</span><span class="p">(</span><span class="mi">1</span><span class="p">,</span> <span class="s">"unknown type in header: %c</span><span class="se">\n</span><span class="s">"</span><span class="p">,</span> <span class="n">buf</span><span class="p">[</span><span class="mi">4</span><span class="p">]);</span>
  <span class="k">return</span> <span class="mi">0</span><span class="p">;</span>
<span class="p">}</span>

<span class="n">err</span> <span class="o">=</span> <span class="n">sscanf</span><span class="p">(</span><span class="o">&amp;</span><span class="n">buf</span><span class="p">[</span><span class="mi">5</span><span class="p">],</span> <span class="s">"%x#"</span><span class="p">,</span> <span class="n">more</span><span class="p">);</span>
<span class="k">if</span> <span class="p">(</span><span class="n">err</span> <span class="o">!=</span> <span class="mi">1</span><span class="p">)</span> <span class="p">{</span>
  <span class="n">DBG</span><span class="p">(</span><span class="mi">1</span><span class="p">,</span> <span class="s">"cannot decode length from header</span><span class="se">\n</span><span class="s">"</span><span class="p">);</span>
  <span class="k">return</span> <span class="mi">0</span><span class="p">;</span>
<span class="p">}</span>
</code></pre></div></div>

<p><code class="language-plaintext highlighter-rouge">buf</code> is a pointer to a 64 byte stack buffer (<code class="language-plaintext highlighter-rouge">rbuf</code> in <a href="https://gitlab.com/sane-project/backends/-/blob/1.0.27/backend/epsonds-cmd.c#L136"><code class="language-plaintext highlighter-rouge">esci2_cmd</code></a>), the contents of which are entirely controlled by the attacker. If the attacker fills the buffer with the character ‘0’, then <code class="language-plaintext highlighter-rouge">sscanf</code> will read off the end of the buffer. If the characters beyond the buffer are valid hexadecimal digits, then they will be converted to a number and written to the variable named <code class="language-plaintext highlighter-rouge">more</code>. The value of <code class="language-plaintext highlighter-rouge">more</code> is included in the next message that is sent to the malicious device, so this issue is an information leak vulnerability.</p>

<h4 id="impact-5">Impact</h4>

<p>This issue may lead to remote information disclosure, where “remote” means a device or computer connected to the same network as the victim. In practice, though, this issue is very low severity, because the byte immediately following the buffer is usually not a valid hexadecimal digit, so no information disclosure occurs.</p>

<h3 id="issue-7-ghsl-2020-084-cve-2020-12865-buffer-overflow-in-esci2_img">Issue 7 (<code class="language-plaintext highlighter-rouge">GHSL-2020-084</code>, <code class="language-plaintext highlighter-rouge">CVE-2020-12865</code>): buffer overflow in <code class="language-plaintext highlighter-rouge">esci2_img</code></h3>

<p>This issue requires the user to click the “Scan” button, so it is a one-click vulnerability, rather than a zero-click vulnerability. The function <a href="https://gitlab.com/sane-project/backends/-/blob/1.0.27/backend/epsonds-cmd.c#L838"><code class="language-plaintext highlighter-rouge">esci2_img</code></a> has a heap buffer overflow:</p>

<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="n">SANE_Status</span>
<span class="nf">esci2_img</span><span class="p">(</span><span class="k">struct</span> <span class="n">epsonds_scanner</span> <span class="o">*</span><span class="n">s</span><span class="p">,</span> <span class="n">SANE_Int</span> <span class="o">*</span><span class="n">length</span><span class="p">)</span>
<span class="p">{</span>
  <span class="n">SANE_Status</span> <span class="n">status</span> <span class="o">=</span> <span class="n">SANE_STATUS_GOOD</span><span class="p">;</span>
  <span class="n">SANE_Status</span> <span class="n">parse_status</span><span class="p">;</span>
  <span class="kt">unsigned</span> <span class="kt">int</span> <span class="n">more</span><span class="p">;</span>
  <span class="kt">ssize_t</span> <span class="n">read</span><span class="p">;</span>

  <span class="o">*</span><span class="n">length</span> <span class="o">=</span> <span class="mi">0</span><span class="p">;</span>

  <span class="k">if</span> <span class="p">(</span><span class="n">s</span><span class="o">-&gt;</span><span class="n">canceling</span><span class="p">)</span>
    <span class="k">return</span> <span class="n">SANE_STATUS_CANCELLED</span><span class="p">;</span>

  <span class="cm">/* request image data */</span>
  <span class="n">eds_send</span><span class="p">(</span><span class="n">s</span><span class="p">,</span> <span class="s">"IMG x0000000"</span><span class="p">,</span> <span class="mi">12</span><span class="p">,</span> <span class="o">&amp;</span><span class="n">status</span><span class="p">,</span> <span class="mi">64</span><span class="p">);</span>
  <span class="k">if</span> <span class="p">(</span><span class="n">status</span> <span class="o">!=</span> <span class="n">SANE_STATUS_GOOD</span><span class="p">)</span> <span class="p">{</span>
    <span class="k">return</span> <span class="n">status</span><span class="p">;</span>
  <span class="p">}</span>

  <span class="cm">/* receive DataHeaderBlock */</span>
  <span class="n">memset</span><span class="p">(</span><span class="n">s</span><span class="o">-&gt;</span><span class="n">buf</span><span class="p">,</span> <span class="mh">0x00</span><span class="p">,</span> <span class="mi">64</span><span class="p">);</span>
  <span class="n">eds_recv</span><span class="p">(</span><span class="n">s</span><span class="p">,</span> <span class="n">s</span><span class="o">-&gt;</span><span class="n">buf</span><span class="p">,</span> <span class="mi">64</span><span class="p">,</span> <span class="o">&amp;</span><span class="n">status</span><span class="p">);</span>
  <span class="k">if</span> <span class="p">(</span><span class="n">status</span> <span class="o">!=</span> <span class="n">SANE_STATUS_GOOD</span><span class="p">)</span> <span class="p">{</span>
    <span class="k">return</span> <span class="n">status</span><span class="p">;</span>
  <span class="p">}</span>

  <span class="cm">/* check if we need to read any image data */</span>
  <span class="n">more</span> <span class="o">=</span> <span class="mi">0</span><span class="p">;</span>
  <span class="k">if</span> <span class="p">(</span><span class="o">!</span><span class="n">esci2_check_header</span><span class="p">(</span><span class="s">"IMG "</span><span class="p">,</span> <span class="p">(</span><span class="kt">char</span> <span class="o">*</span><span class="p">)</span><span class="n">s</span><span class="o">-&gt;</span><span class="n">buf</span><span class="p">,</span> <span class="o">&amp;</span><span class="n">more</span><span class="p">))</span> <span class="p">{</span>  <span class="o">&lt;=====</span> <span class="n">attacker</span> <span class="n">controls</span> <span class="n">value</span> <span class="n">of</span> <span class="err">`</span><span class="n">more</span><span class="err">`</span>
    <span class="k">return</span> <span class="n">SANE_STATUS_IO_ERROR</span><span class="p">;</span>
  <span class="p">}</span>

  <span class="cm">/* this handles eof and errors */</span>
  <span class="n">parse_status</span> <span class="o">=</span> <span class="n">esci2_parse_block</span><span class="p">((</span><span class="kt">char</span> <span class="o">*</span><span class="p">)</span><span class="n">s</span><span class="o">-&gt;</span><span class="n">buf</span> <span class="o">+</span> <span class="mi">12</span><span class="p">,</span> <span class="mi">64</span> <span class="o">-</span> <span class="mi">12</span><span class="p">,</span> <span class="n">s</span><span class="p">,</span> <span class="o">&amp;</span><span class="n">img_cb</span><span class="p">);</span>

  <span class="cm">/* no more data? return using the status of the esci2_parse_block
   * call, which might hold other error conditions.
   */</span>
  <span class="k">if</span> <span class="p">(</span><span class="o">!</span><span class="n">more</span><span class="p">)</span> <span class="p">{</span>
    <span class="k">return</span> <span class="n">parse_status</span><span class="p">;</span>
  <span class="p">}</span>

  <span class="cm">/* ALWAYS read image data */</span>
  <span class="k">if</span> <span class="p">(</span><span class="n">s</span><span class="o">-&gt;</span><span class="n">hw</span><span class="o">-&gt;</span><span class="n">connection</span> <span class="o">==</span> <span class="n">SANE_EPSONDS_NET</span><span class="p">)</span> <span class="p">{</span>
    <span class="n">epsonds_net_request_read</span><span class="p">(</span><span class="n">s</span><span class="p">,</span> <span class="n">more</span><span class="p">);</span>
  <span class="p">}</span>

  <span class="n">read</span> <span class="o">=</span> <span class="n">eds_recv</span><span class="p">(</span><span class="n">s</span><span class="p">,</span> <span class="n">s</span><span class="o">-&gt;</span><span class="n">buf</span><span class="p">,</span> <span class="n">more</span><span class="p">,</span> <span class="o">&amp;</span><span class="n">status</span><span class="p">);</span>  <span class="o">&lt;=====</span> <span class="n">heap</span> <span class="n">buffer</span> <span class="n">overflow</span>
  <span class="k">if</span> <span class="p">(</span><span class="n">status</span> <span class="o">!=</span> <span class="n">SANE_STATUS_GOOD</span><span class="p">)</span> <span class="p">{</span>
    <span class="k">return</span> <span class="n">status</span><span class="p">;</span>
  <span class="p">}</span>

  <span class="k">if</span> <span class="p">(</span><span class="n">read</span> <span class="o">!=</span> <span class="n">more</span><span class="p">)</span> <span class="p">{</span>
    <span class="k">return</span> <span class="n">SANE_STATUS_IO_ERROR</span><span class="p">;</span>
  <span class="p">}</span>

  <span class="cm">/* handle esci2_parse_block errors */</span>
  <span class="k">if</span> <span class="p">(</span><span class="n">parse_status</span> <span class="o">!=</span> <span class="n">SANE_STATUS_GOOD</span><span class="p">)</span> <span class="p">{</span>
    <span class="k">return</span> <span class="n">parse_status</span><span class="p">;</span>
  <span class="p">}</span>

  <span class="n">DBG</span><span class="p">(</span><span class="mi">15</span><span class="p">,</span> <span class="s">"%s: read %lu bytes, status: %d</span><span class="se">\n</span><span class="s">"</span><span class="p">,</span> <span class="n">__func__</span><span class="p">,</span> <span class="p">(</span><span class="kt">unsigned</span> <span class="kt">long</span><span class="p">)</span> <span class="n">read</span><span class="p">,</span> <span class="n">status</span><span class="p">);</span>

  <span class="o">*</span><span class="n">length</span> <span class="o">=</span> <span class="n">read</span><span class="p">;</span>

  <span class="k">if</span> <span class="p">(</span><span class="n">s</span><span class="o">-&gt;</span><span class="n">canceling</span><span class="p">)</span> <span class="p">{</span>
    <span class="k">return</span> <span class="n">SANE_STATUS_CANCELLED</span><span class="p">;</span>
  <span class="p">}</span>

  <span class="k">return</span> <span class="n">SANE_STATUS_GOOD</span><span class="p">;</span>
<span class="p">}</span>
</code></pre></div></div>

<h4 id="impact-6">Impact</h4>

<p>This issue may lead to remote code execution, where “remote” means a device or computer connected to the same network as the victim. For example, in a typical office environment the malicious device would need to be somewhere inside the building.</p>

<h2 id="cves">CVEs</h2>

<ul>
  <li>GHSL-2020-075 -&gt; CVE-2020-12867</li>
  <li>GHSL-2020-079 -&gt; CVE-2020-12866</li>
  <li>GHSL-2020-080 -&gt; CVE-2020-12861</li>
  <li>GHSL-2020-081 -&gt; CVE-2020-12864</li>
  <li>GHSL-2020-082 -&gt; CVE-2020-12862</li>
  <li>GHSL-2020-083 -&gt; CVE-2020-12863</li>
  <li>GHSL-2020-084 -&gt; CVE-2020-12865</li>
</ul>

<h2 id="coordinated-disclosure-timeline">Coordinated Disclosure Timeline</h2>

<p>This report was subject to the GHSL <a href="https://securitylab.github.com/advisories/#policy">coordinated disclosure policy</a>.</p>

<ul>
  <li>2020-04-21 reported: https://gitlab.com/sane-project/backends/-/issues/279</li>
  <li>2020-04-21 acknowledged by Olaf Meeuwissen</li>
  <li>2020-05-14 CVE request submitted to Mitre</li>
  <li>2020-05-17 bugs announced on http://www.sane-project.org/ and on their <a href="https://alioth-lists.debian.net/pipermail/sane-announce/2020/000041.html">mailing list</a></li>
  <li>2020-05-30 <a href="https://gitlab.com/sane-project/backends/-/issues/279">issue 279</a> is derestricted. The original <a href="https://gitlab.com/sane-project/backends/uploads/7aa1c15de003074e2c13dc928f0a523f/fakescanner.cpp">PoC</a> is attached to the issue and is therefore also publicly visible.</li>
</ul>

<h2 id="resources">Resources</h2>

<ul>
  <li>https://gitlab.com/sane-project/backends/-/issues/279</li>
  <li>https://alioth-lists.debian.net/pipermail/sane-announce/2020/000041.html</li>
  <li>https://github.com/github/securitylab/tree/38b182e96a48f19b412039c0b321d6faec2b5c55/SecurityExploits/SANE/epsonds_CVE-2020-12861</li>
</ul>

<h2 id="credit">Credit</h2>

<p>These issues were discovered and reported by GHSL team member <a href="https://github.com/kevinbackhouse">@kevinbackhouse (Kevin Backhouse)</a>.</p>

<h2 id="contact">Contact</h2>

<p>You can contact the GHSL team at <code class="language-plaintext highlighter-rouge">securitylab@github.com</code>, please include the relevant GHSL IDs in any communicati