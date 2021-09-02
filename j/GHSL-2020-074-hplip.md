<header class="post-header d-block mb-6">
      <div class="date text-mono f5 my-3">September 30, 2020</div>
      <h1 class="my-2 h00-mktg lh-condensed">GHSL-2020-074, 077, 078: Memory corruptions in HPLIP - CVE-2020-6923</h1>

      
      
      
      
      

      

      <a target="_blank" class="sc-frDJqD SgxRc d-inline-flex flex-row flex-items-center text-gray" href="https://github.com/kevinbackhouse">
        <img class="mr-3" src="https://avatars.githubusercontent.com/u/4358136?s=35" height="35" width="35">
        <span>Kevin Backhouse</span>
      </a>
    </header>

    <main id="content" class="markdown-body" aria-label="Content">
      <h2 id="summary">Summary</h2>

<p>HPLIP contains two memory corruption vulnerabilities which can be triggered by a malicious device or computer that is connected to the same network. The vulnerabilities are triggered when an application such as <a href="http://manpages.ubuntu.com/manpages/bionic/man1/simple-scan.1.html">simple-scan</a> searches the network for scanners. In the specific case of simple-scan, this happens immediately when simple-scan starts, so there isn’t even any need to trick the user into thinking that the scanner is genuine so that they will click on it.</p>

<p>We have also identified two lower-severity bugs in HPLIP, which we have also included in this report.</p>

<h2 id="product">Product</h2>
<p>HP Linux Imaging and Printing (HPLIP).</p>

<h2 id="tested-version">Tested Version</h2>
<p>HPLIP 3.17.10+repack0-5, tested on Ubuntu 18.04.4 LTS with simple-scan 3.28.0-0ubuntu1.</p>

<h2 id="details">Details</h2>

<h3 id="issue-1-ghsl-2020-074-cve-2020-6923-heap-buffer-overflow-in-mdns_readname">Issue 1 (<code class="language-plaintext highlighter-rouge">GHSL-2020-074</code>, <code class="language-plaintext highlighter-rouge">CVE-2020-6923</code>): Heap buffer overflow in <code class="language-plaintext highlighter-rouge">mdns_readName</code></h3>

<p>The function <code class="language-plaintext highlighter-rouge">mdns_readName</code> (protocol/discovery/mdns.c, line 177) is used during parsing of an MDNS message. The MDNS message is a response to a broadcast message that was sent out by <code class="language-plaintext highlighter-rouge">mdns_probe_nw_scanners</code> (protocol/discovery/mdns.c, line 426). Any device that is connected to the same network can receive the broadcast message and respond to it, so the response could come from a malicious device. The parsed name is written to <code class="language-plaintext highlighter-rouge">buf</code>, which is a pointer to a 256 byte buffer on the heap. There is no bounds checking in this function, so the malicious device can send a message that overflows the heap buffer.</p>

<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="k">static</span> <span class="kt">int</span> <span class="nf">mdns_readName</span><span class="p">(</span><span class="kt">unsigned</span> <span class="kt">char</span><span class="o">*</span> <span class="n">start</span><span class="p">,</span> <span class="kt">unsigned</span> <span class="kt">char</span> <span class="o">*</span><span class="n">Response</span><span class="p">,</span> <span class="kt">char</span> <span class="o">*</span><span class="n">buf</span><span class="p">)</span>
<span class="p">{</span>
    <span class="kt">int</span> <span class="n">size</span> <span class="o">=</span> <span class="mi">0</span><span class="p">;</span>
    <span class="kt">char</span> <span class="o">*</span><span class="n">name</span> <span class="o">=</span> <span class="n">buf</span><span class="p">;</span>
    <span class="kt">unsigned</span> <span class="kt">char</span> <span class="o">*</span><span class="n">p</span> <span class="o">=</span> <span class="n">Response</span><span class="p">;</span>

    <span class="k">while</span> <span class="p">(</span><span class="n">size</span> <span class="o">=</span> <span class="o">*</span><span class="n">p</span><span class="o">++</span><span class="p">)</span>
    <span class="p">{</span>
        <span class="k">if</span> <span class="p">(</span><span class="n">size</span> <span class="o">&gt;=</span> <span class="mh">0xC0</span><span class="p">)</span>
        <span class="p">{</span>
            <span class="c1">//Compressed Size. Just ignore it.</span>
            <span class="n">p</span><span class="o">++</span><span class="p">;</span> <span class="c1">//skip Offset byte</span>
            <span class="k">return</span> <span class="p">(</span><span class="n">p</span> <span class="o">-</span> <span class="n">Response</span><span class="p">);</span>
        <span class="p">}</span>
        <span class="n">memcpy</span><span class="p">(</span><span class="n">name</span><span class="p">,</span> <span class="n">p</span><span class="p">,</span> <span class="n">size</span><span class="p">);</span>  <span class="o">&lt;=====</span> <span class="n">heap</span> <span class="n">buffer</span> <span class="n">overflow</span>
        <span class="n">name</span><span class="p">[</span><span class="n">size</span><span class="p">]</span> <span class="o">=</span> <span class="sc">'.'</span><span class="p">;</span>
        <span class="n">p</span> <span class="o">+=</span> <span class="n">size</span><span class="p">;</span>
        <span class="n">name</span> <span class="o">+=</span> <span class="n">size</span> <span class="o">+</span> <span class="mi">1</span><span class="p">;</span>
    <span class="p">}</span>

    <span class="o">*</span><span class="p">(</span><span class="n">name</span> <span class="o">-</span> <span class="mi">1</span><span class="p">)</span> <span class="o">=</span> <span class="sc">'\0'</span><span class="p">;</span>

    <span class="n">DBG</span><span class="p">(</span><span class="s">"Name = [%s]</span><span class="se">\n</span><span class="s">"</span><span class="p">,</span> <span class="n">buf</span><span class="p">);</span>
    <span class="k">return</span> <span class="p">(</span><span class="n">p</span> <span class="o">-</span> <span class="n">Response</span><span class="p">);</span>
<span class="p">}</span>
</code></pre></div></div>

<p>We have included a proof-of-concept exploit for this vulnerability. Compile and run the PoC as follows:</p>

<div class="language-bash highlighter-rouge"><div class="highlight"><pre class="highlight"><code>g++ fakescanner.cpp <span class="nt">-o</span> fakescanner
./fakescanner hplip 0
</code></pre></div></div>

<p>Now run <code class="language-plaintext highlighter-rouge">simple-scan</code> on a different computer that is connected to the same network (ethernet or wifi):</p>

<div class="language-bash highlighter-rouge"><div class="highlight"><pre class="highlight"><code>simple-scan
</code></pre></div></div>

<p>You should see <code class="language-plaintext highlighter-rouge">simple-scan</code> crash with a segmentation fault.</p>

<h4 id="impact">Impact</h4>

<p>This issue may lead to remote code execution, where “remote” means a device or computer connected to the same network as the victim. For example, in a typical office environment the malicious device would need to be somewhere inside the building.</p>

<p>Mitigations such as ASLR may make it difficult for an attacker to create a reliable RCE exploit for the vulnerability. The PoC that we have provided only causes HPLIP to crash.</p>

<h4 id="resources">Resources</h4>

<p>We have published the source code for our PoC, <a href="https://github.com/github/securitylab/blob/main/SecurityExploits/SANE/epsonds_CVE-2020-12861/fakescanner.cpp">fakescanner.cpp</a>.</p>

<h3 id="issue-2-ghsl-2020-077-cve-2020-6923-stack-buffer-overflow-in-mdns_update_uris">Issue 2 (<code class="language-plaintext highlighter-rouge">GHSL-2020-077</code>, <code class="language-plaintext highlighter-rouge">CVE-2020-6923</code>): Stack buffer overflow in <code class="language-plaintext highlighter-rouge">mdns_update_uris</code></h3>

<p>The function <code class="language-plaintext highlighter-rouge">mdns_update_uris</code> (protocol/discovery/mdns.c, line 381) is used to process a linked list of MDNS messages. The MDNS messages are the responses to a broadcast message that was sent out by <code class="language-plaintext highlighter-rouge">mdns_probe_nw_scanners</code> (protocol/discovery/mdns.c, line 426). Any device that is connected to the same network can receive the broadcast message and respond to it, so one of the responses could come from a malicious device. <code class="language-plaintext highlighter-rouge">mdns_update_uris</code> has a stack buffer overflow:</p>

<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="k">static</span> <span class="kt">int</span> <span class="nf">mdns_update_uris</span><span class="p">(</span><span class="n">DNS_RECORD</span> <span class="o">*</span><span class="n">rr</span><span class="p">,</span> <span class="kt">char</span><span class="o">*</span> <span class="n">uris_buf</span><span class="p">,</span> <span class="kt">int</span> <span class="n">buf_size</span><span class="p">,</span> <span class="kt">int</span> <span class="o">*</span><span class="n">count</span><span class="p">)</span>
<span class="p">{</span>
    <span class="kt">char</span> <span class="n">tempuri</span><span class="p">[</span><span class="n">MAX_URI_LEN</span><span class="p">]</span> <span class="o">=</span> <span class="p">{</span><span class="mi">0</span><span class="p">};</span>
    <span class="kt">int</span> <span class="n">bytes_read</span> <span class="o">=</span> <span class="mi">0</span><span class="p">;</span>

    <span class="n">DBG</span><span class="p">(</span><span class="s">"mdns_update_uris.</span><span class="se">\n</span><span class="s">"</span><span class="p">);</span>

    <span class="o">*</span><span class="n">count</span> <span class="o">=</span> <span class="mi">0</span><span class="p">;</span>
    <span class="n">memset</span><span class="p">(</span><span class="n">uris_buf</span><span class="p">,</span> <span class="mi">0</span><span class="p">,</span> <span class="n">buf_size</span><span class="p">);</span>

    <span class="k">while</span><span class="p">(</span><span class="n">rr</span><span class="p">)</span>
    <span class="p">{</span>
        <span class="k">if</span> <span class="p">(</span><span class="n">rr</span><span class="o">-&gt;</span><span class="n">mdl</span><span class="p">[</span><span class="mi">0</span><span class="p">]</span> <span class="o">&amp;&amp;</span> <span class="n">rr</span><span class="o">-&gt;</span><span class="n">ip</span><span class="p">[</span><span class="mi">0</span><span class="p">]</span> <span class="cm">/*&amp;&amp; strstr(rr-&gt;mdl, "scanjet")*/</span><span class="p">)</span>
        <span class="p">{</span>
            <span class="n">memset</span><span class="p">(</span><span class="n">tempuri</span><span class="p">,</span> <span class="mi">0</span><span class="p">,</span> <span class="k">sizeof</span><span class="p">(</span><span class="n">tempuri</span><span class="p">));</span>
            <span class="n">sprintf</span><span class="p">(</span><span class="n">tempuri</span><span class="p">,</span> <span class="s">"hp:/net/%s?ip=%s&amp;queue=false"</span><span class="p">,</span> <span class="n">rr</span><span class="o">-&gt;</span><span class="n">mdl</span><span class="p">,</span> <span class="n">rr</span><span class="o">-&gt;</span><span class="n">ip</span><span class="p">);</span>   <span class="o">&lt;=====</span> <span class="n">stack</span> <span class="n">buffer</span> <span class="n">overflow</span>

            <span class="c1">//Check whether buffer has enough space to add new URI and check for duplicate URIs.</span>
            <span class="k">if</span><span class="p">(</span><span class="n">bytes_read</span> <span class="o">+</span> <span class="k">sizeof</span><span class="p">(</span><span class="n">tempuri</span><span class="p">)</span> <span class="o">&lt;</span> <span class="n">buf_size</span>  <span class="o">&amp;&amp;</span> <span class="o">!</span><span class="n">strstr</span><span class="p">(</span><span class="n">uris_buf</span><span class="p">,</span> <span class="n">tempuri</span><span class="p">))</span>
            <span class="p">{</span>
                <span class="n">bytes_read</span> <span class="o">+=</span> <span class="n">sprintf</span><span class="p">(</span><span class="n">uris_buf</span> <span class="o">+</span> <span class="n">bytes_read</span><span class="p">,</span> <span class="s">"%s;"</span><span class="p">,</span> <span class="n">tempuri</span><span class="p">);</span>
                <span class="p">(</span><span class="o">*</span><span class="n">count</span><span class="p">)</span><span class="o">++</span><span class="p">;</span>
                <span class="o">*</span><span class="p">(</span><span class="n">uris_buf</span> <span class="o">+</span> <span class="n">bytes_read</span><span class="p">)</span> <span class="o">=</span> <span class="sc">'\0'</span><span class="p">;</span>
            <span class="p">}</span>
        <span class="p">}</span>
        <span class="n">rr</span> <span class="o">=</span> <span class="n">rr</span><span class="o">-&gt;</span><span class="n">next</span><span class="p">;</span>
    <span class="p">}</span>

    <span class="n">DBG</span><span class="p">(</span><span class="s">"mdns_update_uris Count=[%d] bytes=[%d] URIs = %s</span><span class="se">\n</span><span class="s">"</span><span class="p">,</span><span class="o">*</span><span class="n">count</span><span class="p">,</span> <span class="n">bytes_read</span><span class="p">,</span> <span class="n">uris_buf</span><span class="p">);</span>
    <span class="k">return</span> <span class="n">bytes_read</span><span class="p">;</span>
<span class="p">}</span>
</code></pre></div></div>

<p>A stack buffer overflow can occur if the combined length of <code class="language-plaintext highlighter-rouge">rr-&gt;mdl</code> and <code class="language-plaintext highlighter-rouge">rr-&gt;ip</code> leads to a uri string that is too big to fit in <code class="language-plaintext highlighter-rouge">tempuri</code>. Both of these strings are controlled by the attacker, because they are parsed from the MDNS message, during <code class="language-plaintext highlighter-rouge">mdns_parse_respponse</code>.</p>

<p>We have included a proof-of-concept exploit for this vulnerability. Compile and run the PoC as follows:</p>

<div class="language-bash highlighter-rouge"><div class="highlight"><pre class="highlight"><code>g++ fakescanner.cpp <span class="nt">-o</span> fakescanner
./fakescanner hplip 1
</code></pre></div></div>

<p>Now run <code class="language-plaintext highlighter-rouge">simple-scan</code> on a different computer that is connected to the same network (ethernet or wifi):</p>

<div class="language-bash highlighter-rouge"><div class="highlight"><pre class="highlight"><code>simple-scan
</code></pre></div></div>

<p>You should see <code class="language-plaintext highlighter-rouge">simple-scan</code> abort with a “stack smashing detected” error message.</p>

<h4 id="impact-1">Impact</h4>

<p>This issue may lead to remote code execution, where “remote” means a device or computer connected to the same network as the victim. For example, in a typical office environment the malicious device would need to be somewhere inside the building.</p>

<p>Mitigations such as stack smashing detection may make it difficult for an attacker to create a reliable RCE exploit for the vulnerability. The PoC that we have provided only causes HPLIP to crash.</p>

<h4 id="resources-1">Resources</h4>

<p>We have published the source code for our PoC, <a href="https://github.com/github/securitylab/blob/main/SecurityExploits/SANE/epsonds_CVE-2020-12861/fakescanner.cpp">fakescanner.cpp</a>.</p>

<h3 id="issue-3-ghsl-2020-078-cve-2020-6923-out-of-bounds-read-in-mdns_parse_respponse">Issue 3 (<code class="language-plaintext highlighter-rouge">GHSL-2020-078</code>, <code class="language-plaintext highlighter-rouge">CVE-2020-6923</code>): Out-of-bounds read in <code class="language-plaintext highlighter-rouge">mdns_parse_respponse</code></h3>

<p>The function <code class="language-plaintext highlighter-rouge">mdns_parse_respponse</code> (protocol/discovery/mdns.c, line 381) is used to parse an MDNS message. The MDNS message is a response to a broadcast message that was sent out by <code class="language-plaintext highlighter-rouge">mdns_probe_nw_scanners</code> (protocol/discovery/mdns.c, line 426). Any device that is connected to the same network can receive the broadcast message and respond to it, so the response could come from a malicious device. <code class="language-plaintext highlighter-rouge">mdns_parse_respponse</code> has an out-of-bounds read:</p>

<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="k">static</span> <span class="kt">void</span> <span class="nf">mdns_parse_respponse</span><span class="p">(</span><span class="kt">unsigned</span> <span class="kt">char</span> <span class="o">*</span><span class="n">Response</span><span class="p">,</span> <span class="n">DNS_RECORD</span> <span class="o">*</span><span class="n">rr</span><span class="p">)</span>
<span class="p">{</span>
    <span class="kt">unsigned</span> <span class="kt">char</span> <span class="o">*</span><span class="n">p</span> <span class="o">=</span> <span class="n">Response</span><span class="p">;</span>
    <span class="kt">unsigned</span> <span class="kt">short</span> <span class="n">type</span> <span class="o">=</span> <span class="mi">0</span><span class="p">,</span> <span class="n">data_len</span> <span class="o">=</span> <span class="mi">0</span><span class="p">;</span>
    <span class="n">DNS_PKT_HEADER</span> <span class="n">h</span><span class="p">;</span>
    <span class="kt">int</span> <span class="n">i</span> <span class="o">=</span> <span class="mi">0</span><span class="p">;</span>

    <span class="n">DBG</span><span class="p">(</span><span class="s">"mdns_parse_respponse entry.</span><span class="se">\n</span><span class="s">"</span><span class="p">);</span>
    <span class="n">mdns_read_header</span><span class="p">(</span><span class="n">Response</span><span class="p">,</span> <span class="o">&amp;</span><span class="n">h</span><span class="p">);</span>
    <span class="n">p</span> <span class="o">+=</span> <span class="n">MDNS_HEADER_SIZE</span><span class="p">;</span>

    <span class="k">for</span> <span class="p">(</span><span class="n">i</span> <span class="o">=</span> <span class="mi">0</span><span class="p">;</span> <span class="n">i</span> <span class="o">&lt;</span> <span class="n">h</span><span class="p">.</span><span class="n">questions</span><span class="p">;</span> <span class="n">i</span><span class="o">++</span><span class="p">)</span>
    <span class="p">{</span>
        <span class="n">p</span> <span class="o">+=</span> <span class="n">mdns_readName</span><span class="p">(</span><span class="n">Response</span><span class="p">,</span> <span class="n">p</span><span class="p">,</span> <span class="n">rr</span><span class="o">-&gt;</span><span class="n">name</span><span class="p">);</span>
        <span class="n">p</span> <span class="o">+=</span> <span class="mi">4</span><span class="p">;</span> <span class="c1">//Skip TYPE(2 bytes)/CLASS(2 bytes)</span>
    <span class="p">}</span>

    <span class="k">for</span> <span class="p">(</span><span class="n">i</span> <span class="o">=</span> <span class="mi">0</span><span class="p">;</span> <span class="n">i</span> <span class="o">&lt;</span> <span class="p">(</span><span class="n">h</span><span class="p">.</span><span class="n">answers</span> <span class="o">+</span> <span class="n">h</span><span class="p">.</span><span class="n">additionals</span><span class="p">);</span> <span class="n">i</span><span class="o">++</span><span class="p">)</span>
    <span class="p">{</span>
        <span class="n">p</span> <span class="o">+=</span> <span class="n">mdns_readName</span><span class="p">(</span><span class="n">Response</span><span class="p">,</span> <span class="n">p</span><span class="p">,</span> <span class="n">rr</span><span class="o">-&gt;</span><span class="n">name</span><span class="p">);</span>  <span class="o">&lt;=====</span> <span class="p">(</span><span class="n">step</span> <span class="mi">3</span><span class="p">)</span> <span class="n">out</span><span class="o">-</span><span class="n">of</span><span class="o">-</span><span class="n">bounds</span> <span class="n">read</span>
        <span class="n">type</span> <span class="o">=</span> <span class="p">(</span><span class="o">*</span><span class="n">p</span> <span class="o">&lt;&lt;</span> <span class="mi">8</span>  <span class="o">|</span> <span class="o">*</span><span class="p">(</span><span class="n">p</span><span class="o">+</span><span class="mi">1</span><span class="p">));</span>
        <span class="n">p</span> <span class="o">+=</span> <span class="mi">8</span><span class="p">;</span>  <span class="c1">//Skip type(2 bytes)/class(2 bytes)/TTL(4 bytes)</span>

        <span class="n">data_len</span> <span class="o">=</span> <span class="p">(</span> <span class="o">*</span><span class="n">p</span> <span class="o">&lt;&lt;</span> <span class="mi">8</span>  <span class="o">|</span> <span class="o">*</span><span class="p">(</span><span class="n">p</span><span class="o">+</span><span class="mi">1</span><span class="p">));</span>  <span class="o">&lt;=====</span> <span class="p">(</span><span class="n">step</span> <span class="mi">1</span><span class="p">)</span> <span class="n">data_len</span> <span class="n">is</span> <span class="n">controlled</span> <span class="n">by</span> <span class="n">the</span> <span class="n">attacker</span>
        <span class="n">p</span> <span class="o">+=</span> <span class="mi">2</span><span class="p">;</span>  <span class="c1">//Skip data_len(2 bytes)</span>

        <span class="k">switch</span> <span class="p">(</span><span class="n">type</span><span class="p">)</span>
        <span class="p">{</span>
            <span class="k">case</span> <span class="n">QTYPE_A</span><span class="p">:</span>
                <span class="n">sprintf</span><span class="p">(</span><span class="n">rr</span><span class="o">-&gt;</span><span class="n">ip</span><span class="p">,</span> <span class="s">"%d.%d.%d.%d"</span><span class="p">,</span> <span class="n">p</span><span class="p">[</span><span class="mi">0</span><span class="p">],</span> <span class="n">p</span><span class="p">[</span><span class="mi">1</span><span class="p">],</span> <span class="n">p</span><span class="p">[</span><span class="mi">2</span><span class="p">],</span> <span class="n">p</span><span class="p">[</span><span class="mi">3</span><span class="p">]);</span>
                <span class="k">break</span><span class="p">;</span>
            <span class="k">case</span> <span class="n">QTYPE_TXT</span><span class="p">:</span>
                <span class="n">mdns_readMDL</span><span class="p">(</span><span class="n">p</span><span class="p">,</span> <span class="n">rr</span><span class="o">-&gt;</span><span class="n">mdl</span><span class="p">,</span> <span class="n">data_len</span><span class="p">);</span>
                <span class="k">break</span><span class="p">;</span>
            <span class="nl">default:</span>
                <span class="k">break</span><span class="p">;</span>
        <span class="p">}</span>

        <span class="n">p</span> <span class="o">+=</span> <span class="n">data_len</span><span class="p">;</span>  <span class="o">&lt;=====</span> <span class="p">(</span><span class="n">step</span> <span class="mi">2</span><span class="p">)</span> <span class="n">p</span> <span class="n">can</span> <span class="n">advance</span> <span class="n">beyond</span> <span class="n">the</span> <span class="n">end</span> <span class="n">of</span> <span class="n">the</span> <span class="n">buffer</span>
        <span class="c1">//DBG("TYPE = %d, Length = %d\n",type, data_len);</span>
    <span class="p">}</span>

    <span class="n">DBG</span><span class="p">(</span><span class="s">"mdns_parse_respponse returning MDL = %s, IP = %s</span><span class="se">\n</span><span class="s">"</span><span class="p">,</span><span class="n">rr</span><span class="o">-&gt;</span><span class="n">mdl</span><span class="p">,</span> <span class="n">rr</span><span class="o">-&gt;</span><span class="n">ip</span><span class="p">);</span>
<span class="p">}</span>
</code></pre></div></div>

<p>We have included a proof-of-concept exploit for this vulnerability. Compile and run the PoC as follows:</p>

<div class="language-bash highlighter-rouge"><div class="highlight"><pre class="highlight"><code>g++ fakescanner.cpp <span class="nt">-o</span> fakescanner
./fakescanner hplip 2
</code></pre></div></div>

<p>Now run <code class="language-plaintext highlighter-rouge">simple-scan</code> with gdb on a different computer that is connected to the same network (ethernet or wifi):</p>

<div class="language-bash highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="nv">$ </span>gdb simple-scan
<span class="o">(</span>gdb<span class="o">)</span> <span class="nb">break </span>mdns_parse_respponse
<span class="o">(</span>gdb<span class="o">)</span> run
</code></pre></div></div>

<p>You need to run <code class="language-plaintext highlighter-rouge">simple-scan</code> with a debugger (gdb) to see the bug, because the out-of-bounds read does not cause a crash.</p>

<h4 id="impact-2">Impact</h4>

<p>By itself, the severity of this issue is very low. However, it may be very useful to an attacker who is attempting to exploit one of the previous two issues, because it provides a way to read outside the buffer, which may enable the attacker to deduce information such as the ASLR offsets or the value of the stack canary.</p>

<h4 id="resources-2">Resources</h4>

<p>We have published the source code for our PoC, <a href="https://github.com/github/securitylab/blob/main/SecurityExploits/SANE/epsonds_CVE-2020-12861/fakescanner.cpp">fakescanner.cpp</a>.</p>

<h3 id="issue-4-stack-buffer-overflow-in-mdns_lookup">Issue 4: Stack buffer overflow in <code class="language-plaintext highlighter-rouge">mdns_lookup</code></h3>

<p>This issue is unrelated to the other issues, but we have included it in this report because the bug is in the same source file as the other bugs. The function <code class="language-plaintext highlighter-rouge">mdns_lookup</code> (protocol/discovery/mdns.c, line 462) has a stack buffer overflow:</p>

<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="kt">int</span> <span class="nf">mdns_lookup</span><span class="p">(</span><span class="kt">char</span><span class="o">*</span> <span class="n">hostname</span><span class="p">,</span> <span class="kt">unsigned</span> <span class="kt">char</span><span class="o">*</span> <span class="n">ip</span><span class="p">)</span>
<span class="p">{</span>
    <span class="kt">int</span> <span class="n">udp_socket</span> <span class="o">=</span> <span class="mi">0</span><span class="p">;</span>
    <span class="kt">int</span> <span class="n">stat</span> <span class="o">=</span> <span class="n">MDNS_STATUS_ERROR</span><span class="p">;</span>
    <span class="kt">char</span> <span class="n">fqdn</span><span class="p">[</span><span class="n">MAX_NAME_LENGTH</span><span class="p">]</span> <span class="o">=</span> <span class="p">{</span><span class="mi">0</span><span class="p">};</span>
    <span class="n">DNS_RECORD</span> <span class="o">*</span><span class="n">rr_list</span> <span class="o">=</span> <span class="nb">NULL</span><span class="p">;</span>

    <span class="n">DBG</span><span class="p">(</span><span class="s">"mdns_probe_nw_scanners entry.</span><span class="se">\n</span><span class="s">"</span><span class="p">);</span>
    <span class="cm">/* Open UDP socket */</span>
    <span class="k">if</span> <span class="p">(</span><span class="n">mdns_open_socket</span><span class="p">(</span><span class="o">&amp;</span><span class="n">udp_socket</span><span class="p">)</span> <span class="o">!=</span> <span class="n">MDNS_STATUS_OK</span><span class="p">)</span>
        <span class="k">goto</span> <span class="n">bugout</span><span class="p">;</span>

    <span class="cm">/* Send dns query */</span>
    <span class="n">sprintf</span><span class="p">(</span><span class="n">fqdn</span><span class="p">,</span> <span class="s">"%s.local"</span><span class="p">,</span> <span class="n">hostname</span><span class="p">);</span>  <span class="o">&lt;=====</span> <span class="n">stack</span> <span class="n">buffer</span> <span class="n">overflow</span>
    <span class="n">mdns_send_query</span><span class="p">(</span><span class="n">udp_socket</span><span class="p">,</span> <span class="n">fqdn</span><span class="p">,</span> <span class="n">QTYPE_A</span><span class="p">);</span>

    <span class="cm">/* Read Responses */</span>
    <span class="n">rr_list</span> <span class="o">=</span> <span class="n">mdns_read_responses</span><span class="p">(</span><span class="n">udp_socket</span><span class="p">,</span> <span class="n">MODE_READ_SINGLE</span><span class="p">);</span>

    <span class="cm">/* Update IP Address buffer */</span>
    <span class="k">if</span><span class="p">(</span><span class="n">rr_list</span><span class="p">)</span>
    <span class="p">{</span>
        <span class="n">strcpy</span><span class="p">(</span><span class="n">ip</span><span class="p">,</span> <span class="n">rr_list</span><span class="o">-&gt;</span><span class="n">ip</span><span class="p">);</span>
        <span class="n">stat</span> <span class="o">=</span> <span class="n">MDNS_STATUS_OK</span><span class="p">;</span>
        <span class="n">DBG</span><span class="p">(</span><span class="s">"IP = [%s].</span><span class="se">\n</span><span class="s">"</span><span class="p">,</span><span class="n">ip</span><span class="p">);</span>
    <span class="p">}</span>

<span class="nl">bugout:</span>
    <span class="k">if</span> <span class="p">(</span><span class="n">udp_socket</span> <span class="o">&gt;=</span> <span class="mi">0</span><span class="p">)</span>
        <span class="n">close</span><span class="p">(</span><span class="n">udp_socket</span><span class="p">);</span>

    <span class="n">mdns_rr_cleanup</span><span class="p">(</span><span class="n">rr_list</span><span class="p">);</span>
    <span class="k">return</span> <span class="n">stat</span><span class="p">;</span>
<span class="p">}</span>
</code></pre></div></div>

<p>You can trigger the bug by running this command:</p>

<div class="language-bash highlighter-rouge"><div class="highlight"><pre class="highlight"><code>hp-makeuri <span class="nt">-g</span> xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
</code></pre></div></div>

<h4 id="impact-3">Impact</h4>

<p>As far as we are aware this issue does not have any security impact. That is because we are not aware of any scenario in which <code class="language-plaintext highlighter-rouge">mdns_lookup</code> is exposed to attacker-controlled data. Our PoC is a local attack, so it does not demonstrate an interesting attack surface.</p>

<h2 id="cve">CVE</h2>

<ul>
  <li>CVE-2020-6923 (HP PSRT ID: PSR-2020-0077)</li>
</ul>

<h2 id="coordinated-disclosure-timeline">Coordinated Disclosure Timeline</h2>
<ul>
  <li>2020-04-20 reported: https://bugs.launchpad.net/hplip/+bug/1873901</li>
  <li>2020-05-05 no response on the bug report, so I used the main <a href="https://ssl.www8.hp.com/h41268/live/index.aspx?qid=25434">HP PSRT contact form</a> to ask if they can chase the HPLIP team down.</li>
  <li>2020-05-05 Reply from HP PSRT, asking for more details. I sent them another copy of the report and PoC.</li>
  <li>2020-07-02 I emailed HP PSRT to remind them that the 90 day deadline expires on 2020-07-19.</li>
  <li>2020-07-06 Reply from HP PSRT. They have assigned this: PSR-2020-0077.</li>
  <li>2020-07-13 HP PSRT inform me that they have resolved the issue. They ask me to test and confirm.</li>
  <li>2020-07-13 I ask for the latest source code so that I can confirm the fix.</li>
  <li>2020-07-15 HP PSRT send me the latest source code.</li>
  <li>2020-07-15 I inform HP PSRT that the bugs have not been fixed.</li>
  <li>2020-07-16 HP PSRT confirm that they were mistaken and that the fix has not yet been released.</li>
  <li>2020-07-30 HP PSRT send me an updated version of the source code.</li>
  <li>2020-08-11 I confirm that the original bugs have been fixed, but also inform HP PSRT that some new bugs have been introduced.</li>
  <li>2020-08-21 HP PSRT send me an updated version of the source code.</li>
  <li>2020-08-21 I confirm that the bugs are fixed.</li>
  <li>2020-08-28 HP PSRT sets a disclosure date of 2020-09-30.</li>
  <li>2020-09-30 Vulnerability disclosed.</li>
</ul>

<h2 id="resources-3">Resources</h2>

<ul>
  <li>https://support.hp.com/us-en/document/c06927115</li>
</ul>

<h2 id="credit">Credit</h2>

<p>These issues were discovered and reported by GHSL team member <a href="https://github.com/kevinbackhouse">@kevinbackhouse (Kevin Backhouse)</a>.</p>

<h2 id="contact">Contact</h2>

<p>You can contact the GHSL team at <code class="language-plaintext highlighter-rouge">securitylab@github.com</code>, please include the relevant GHSL IDs in any communication regarding these iss