<header class="post-header d-block mb-6">
      <div class="date text-mono f5 my-3">April 21, 2020</div>
      <h1 class="my-2 h00-mktg lh-condensed">GHSL-2020-051, GHSL-2020-052: Multiple vulnerabilities in NTOP nDPI</h1>

      
      
      
      
      

      

      <a target="_blank" class="sc-frDJqD SgxRc d-inline-flex flex-row flex-items-center text-gray" href="https://github.com/anticomputer">
        <img class="mr-3" src="https://avatars.githubusercontent.com/u/13686387?s=35" height="35" width="35">
        <span>Bas Alberts</span>
      </a>
    </header>

    <main id="content" class="markdown-body" aria-label="Content">
      <h2 id="summary">Summary</h2>

<p>The <a href="https://github.com/ntop">NTOP</a> Deep Packet Inspection Toolkit is driven in large part by the nDPI library. This library contains a large set of network protocol dissectors intended to parse and analyze packet-captured network traffic.</p>

<p>The nDPI SSH protocol dissector suffers from multiple integer overflow vulnerabilities which result in a controlled remote heap overflow. Due to the granular nature of the overflow primitive and the ability to control both the contents and layout of the nDPI library’s heap memory through remote input, this vulnerability may be abused to achieve full Remote Code Execution (RCE) against any network inspection stack that is linked against nDPI and uses it to perform network traffic analysis.</p>

<p>The nDPI SSH protocol dissector also suffers from an Out Of Bounds (OOB) read vulnerability which may result in a Denial of Service (DoS).</p>

<p>These specific vulnerabilities were introduced in the 3.0-stable release of nDPI.</p>

<h2 id="cve">CVE</h2>

<ul>
  <li>CVE-2020-11939</li>
  <li>CVE-2020-11940</li>
</ul>

<h2 id="product">Product</h2>

<p>NTOP nDPI (https://github.com/ntop/nDPI)</p>

<h2 id="tested-version">Tested Version</h2>

<p>The development branch of nDPI as of Mar 23, 2020 and commit https://github.com/ntop/nDPI/commit/c6acf97bfbe5ad26db3c2f5dd4d379ac674d6fb3#diff-a3a2b66d47ec1a3eab1b650f55f68ab7</p>

<h2 id="details">Details</h2>

<h3 id="multiple-integer-overflows-in-sshcconcat_hash_string-ghsl-2020-051-cve-2020-11939">Multiple integer overflows in <code class="language-plaintext highlighter-rouge">ssh.c:concat_hash_string</code> (GHSL-2020-051, CVE-2020-11939)</h3>

<p>NOTE: annotated source code based on: https://github.com/ntop/nDPI/blob/c6acf97bfbe5ad26db3c2f5dd4d379ac674d6fb3/src/lib/protocols/ssh.c</p>

<p>When dissecting the SSH protocol the nDPI library will actively parse KEXINIT (type: 20) messages in both the server-to-client and client-to-server directions and attempts to extract various descriptive string sets from SSH KEXINIT packets. These string sets include e.g. the key exchange algorithms supported by the client and the server.</p>

<p>The SSH protocol handles string data based on the common <code class="language-plaintext highlighter-rouge">[length][data]</code> format, where length is a 32bit integer value. As such nDPI extracts these length values, and uses them to pull the actual string data from the SSH KEXINIT packets. nDPI also uses these length values to calculate and maintain a running offset in the captured packet data. This offset is maintained as a 16bit unsigned integer variable.</p>

<p>For example, to pull the key exchange algorithms out of a SSH KEXINIT packet, nDPI performs the following operations:</p>

<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="n">ssh</span><span class="p">.</span><span class="n">c</span><span class="o">:</span><span class="n">ndpi_search_ssh_tcp</span>
<span class="p">...</span>
    <span class="k">if</span><span class="p">(</span><span class="n">msgcode</span> <span class="o">==</span> <span class="mi">20</span> <span class="cm">/* key exchange init */</span><span class="p">)</span> <span class="p">{</span>
      <span class="kt">char</span> <span class="o">*</span><span class="n">hassh_buf</span> <span class="o">=</span> <span class="n">calloc</span><span class="p">(</span><span class="n">packet</span><span class="o">-&gt;</span><span class="n">payload_packet_len</span><span class="p">,</span> <span class="k">sizeof</span><span class="p">(</span><span class="kt">char</span><span class="p">));</span>
<span class="p">...</span>
    	  <span class="n">len</span> <span class="o">=</span> <span class="n">concat_hash_string</span><span class="p">(</span><span class="n">packet</span><span class="p">,</span> <span class="n">hassh_buf</span><span class="p">,</span> <span class="mi">0</span> <span class="cm">/* server */</span><span class="p">);</span>
<span class="p">...</span>

<span class="n">ssh</span><span class="p">.</span><span class="n">c</span><span class="o">:</span><span class="n">concat_hash_string</span>
<span class="p">...</span>
  <span class="n">u_int16_t</span> <span class="n">offset</span> <span class="o">=</span> <span class="mi">22</span><span class="p">,</span> <span class="n">buf_out_len</span> <span class="o">=</span> <span class="mi">0</span><span class="p">;</span>

  <span class="k">if</span><span class="p">(</span><span class="n">offset</span><span class="o">+</span><span class="k">sizeof</span><span class="p">(</span><span class="n">u_int32_t</span><span class="p">)</span> <span class="o">&gt;=</span> <span class="n">packet</span><span class="o">-&gt;</span><span class="n">payload_packet_len</span><span class="p">)</span>
    <span class="k">goto</span> <span class="n">invalid_payload</span><span class="p">;</span>

  <span class="n">u_int32_t</span> <span class="n">len</span> <span class="o">=</span> <span class="n">ntohl</span><span class="p">(</span><span class="o">*</span><span class="p">(</span><span class="n">u_int32_t</span><span class="o">*</span><span class="p">)</span><span class="o">&amp;</span><span class="n">packet</span><span class="o">-&gt;</span><span class="n">payload</span><span class="p">[</span><span class="n">offset</span><span class="p">]);</span>
  <span class="n">offset</span> <span class="o">+=</span> <span class="mi">4</span><span class="p">;</span>

  <span class="cm">/* -1 for ';' */</span>
  <span class="k">if</span><span class="p">((</span><span class="n">offset</span> <span class="o">&gt;=</span> <span class="n">packet</span><span class="o">-&gt;</span><span class="n">payload_packet_len</span><span class="p">)</span> <span class="o">||</span> <span class="p">(</span><span class="n">len</span> <span class="o">&gt;=</span> <span class="n">packet</span><span class="o">-&gt;</span><span class="n">payload_packet_len</span><span class="o">-</span><span class="n">offset</span><span class="o">-</span><span class="mi">1</span><span class="p">))</span>
    <span class="k">goto</span> <span class="n">invalid_payload</span><span class="p">;</span>

  <span class="cm">/* ssh.kex_algorithms [C/S] */</span>
  <span class="n">strncpy</span><span class="p">(</span><span class="n">buf</span><span class="p">,</span> <span class="p">(</span><span class="k">const</span> <span class="kt">char</span> <span class="o">*</span><span class="p">)</span><span class="o">&amp;</span><span class="n">packet</span><span class="o">-&gt;</span><span class="n">payload</span><span class="p">[</span><span class="n">offset</span><span class="p">],</span> <span class="n">buf_out_len</span> <span class="o">=</span> <span class="n">len</span><span class="p">);</span>
  <span class="n">buf</span><span class="p">[</span><span class="n">buf_out_len</span><span class="o">++</span><span class="p">]</span> <span class="o">=</span> <span class="sc">';'</span><span class="p">;</span>
  <span class="n">offset</span> <span class="o">+=</span> <span class="n">len</span><span class="p">;</span>
</code></pre></div></div>

<p>We initially make 2 observations. First, that the destination buffer <code class="language-plaintext highlighter-rouge">buf</code> was previously allocated with a <code class="language-plaintext highlighter-rouge">calloc</code> call that is sized according to <code class="language-plaintext highlighter-rouge">packet-&gt;payload_packet_len</code>, which represents the actual size of the captured SSH packet. Second, that nDPI attempts to make sure that the <code class="language-plaintext highlighter-rouge">offset</code> and subsequently the <code class="language-plaintext highlighter-rouge">len</code> variables do not result in data accesses beyond <code class="language-plaintext highlighter-rouge">packet-&gt;payload_packet_len</code>. The intent here is to prevent read or write access outside of the bounds of the allocated <code class="language-plaintext highlighter-rouge">buf</code> memory region.</p>

<p>However, when examining the <code class="language-plaintext highlighter-rouge">concat_hash_string</code> function in greater detail, we note the following pattern:</p>

<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="n">ssh</span><span class="p">.</span><span class="n">c</span><span class="o">:</span><span class="n">concat_hash_string</span>
<span class="p">...</span>
<span class="p">[</span><span class="mi">1</span><span class="p">]</span>
  <span class="cm">/* ssh.encryption_algorithms_client_to_server [C] */</span>
  <span class="n">len</span> <span class="o">=</span> <span class="n">ntohl</span><span class="p">(</span><span class="o">*</span><span class="p">(</span><span class="n">u_int32_t</span><span class="o">*</span><span class="p">)</span><span class="o">&amp;</span><span class="n">packet</span><span class="o">-&gt;</span><span class="n">payload</span><span class="p">[</span><span class="n">offset</span><span class="p">]);</span>

  <span class="k">if</span><span class="p">(</span><span class="n">client_hash</span><span class="p">)</span> <span class="p">{</span>
    <span class="n">offset</span> <span class="o">+=</span> <span class="mi">4</span><span class="p">;</span>

    <span class="k">if</span><span class="p">((</span><span class="n">offset</span> <span class="o">&gt;=</span> <span class="n">packet</span><span class="o">-&gt;</span><span class="n">payload_packet_len</span><span class="p">)</span> <span class="o">||</span> <span class="p">(</span><span class="n">len</span> <span class="o">&gt;=</span> <span class="n">packet</span><span class="o">-&gt;</span><span class="n">payload_packet_len</span><span class="o">-</span><span class="n">offset</span><span class="o">-</span><span class="mi">1</span><span class="p">))</span>
      <span class="k">goto</span> <span class="n">invalid_payload</span><span class="p">;</span>

    <span class="n">strncpy</span><span class="p">(</span><span class="o">&amp;</span><span class="n">buf</span><span class="p">[</span><span class="n">buf_out_len</span><span class="p">],</span> <span class="p">(</span><span class="k">const</span> <span class="kt">char</span> <span class="o">*</span><span class="p">)</span><span class="o">&amp;</span><span class="n">packet</span><span class="o">-&gt;</span><span class="n">payload</span><span class="p">[</span><span class="n">offset</span><span class="p">],</span> <span class="n">len</span><span class="p">);</span>
    <span class="n">buf_out_len</span> <span class="o">+=</span> <span class="n">len</span><span class="p">;</span>
    <span class="n">buf</span><span class="p">[</span><span class="n">buf_out_len</span><span class="o">++</span><span class="p">]</span> <span class="o">=</span> <span class="sc">';'</span><span class="p">;</span>
    <span class="n">offset</span> <span class="o">+=</span> <span class="n">len</span><span class="p">;</span>
  <span class="p">}</span> <span class="k">else</span>
<span class="p">[</span><span class="mi">2</span><span class="p">]</span>
    <span class="n">offset</span> <span class="o">+=</span> <span class="mi">4</span> <span class="o">+</span> <span class="n">len</span><span class="p">;</span>

  <span class="cm">/* ssh.encryption_algorithms_server_to_client [S] */</span>
  <span class="n">len</span> <span class="o">=</span> <span class="n">ntohl</span><span class="p">(</span><span class="o">*</span><span class="p">(</span><span class="n">u_int32_t</span><span class="o">*</span><span class="p">)</span><span class="o">&amp;</span><span class="n">packet</span><span class="o">-&gt;</span><span class="n">payload</span><span class="p">[</span><span class="n">offset</span><span class="p">]);</span>

  <span class="k">if</span><span class="p">(</span><span class="o">!</span><span class="n">client_hash</span><span class="p">)</span> <span class="p">{</span>
    <span class="n">offset</span> <span class="o">+=</span> <span class="mi">4</span><span class="p">;</span>

    <span class="k">if</span><span class="p">((</span><span class="n">offset</span> <span class="o">&gt;=</span> <span class="n">packet</span><span class="o">-&gt;</span><span class="n">payload_packet_len</span><span class="p">)</span> <span class="o">||</span> <span class="p">(</span><span class="n">len</span> <span class="o">&gt;=</span> <span class="n">packet</span><span class="o">-&gt;</span><span class="n">payload_packet_len</span><span class="o">-</span><span class="n">offset</span><span class="o">-</span><span class="mi">1</span><span class="p">))</span>
      <span class="k">goto</span> <span class="n">invalid_payload</span><span class="p">;</span>

    <span class="n">strncpy</span><span class="p">(</span><span class="o">&amp;</span><span class="n">buf</span><span class="p">[</span><span class="n">buf_out_len</span><span class="p">],</span> <span class="p">(</span><span class="k">const</span> <span class="kt">char</span> <span class="o">*</span><span class="p">)</span><span class="o">&amp;</span><span class="n">packet</span><span class="o">-&gt;</span><span class="n">payload</span><span class="p">[</span><span class="n">offset</span><span class="p">],</span> <span class="n">len</span><span class="p">);</span>
    <span class="n">buf_out_len</span> <span class="o">+=</span> <span class="n">len</span><span class="p">;</span>
    <span class="n">buf</span><span class="p">[</span><span class="n">buf_out_len</span><span class="o">++</span><span class="p">]</span> <span class="o">=</span> <span class="sc">';'</span><span class="p">;</span>
    <span class="n">offset</span> <span class="o">+=</span> <span class="n">len</span><span class="p">;</span>
  <span class="p">}</span> <span class="k">else</span>
    <span class="n">offset</span> <span class="o">+=</span> <span class="mi">4</span> <span class="o">+</span> <span class="n">len</span><span class="p">;</span>

<span class="p">[</span><span class="mi">3</span><span class="p">]</span>
  <span class="cm">/* ssh.mac_algorithms_client_to_server [C] */</span>
  <span class="n">len</span> <span class="o">=</span> <span class="n">ntohl</span><span class="p">(</span><span class="o">*</span><span class="p">(</span><span class="n">u_int32_t</span><span class="o">*</span><span class="p">)</span><span class="o">&amp;</span><span class="n">packet</span><span class="o">-&gt;</span><span class="n">payload</span><span class="p">[</span><span class="n">offset</span><span class="p">]);</span>

  <span class="k">if</span><span class="p">(</span><span class="n">client_hash</span><span class="p">)</span> <span class="p">{</span>
    <span class="n">offset</span> <span class="o">+=</span> <span class="mi">4</span><span class="p">;</span>

<span class="p">[</span><span class="mi">4</span><span class="p">]</span>
    <span class="k">if</span><span class="p">((</span><span class="n">offset</span> <span class="o">&gt;=</span> <span class="n">packet</span><span class="o">-&gt;</span><span class="n">payload_packet_len</span><span class="p">)</span> <span class="o">||</span> <span class="p">(</span><span class="n">len</span> <span class="o">&gt;=</span> <span class="n">packet</span><span class="o">-&gt;</span><span class="n">payload_packet_len</span><span class="o">-</span><span class="n">offset</span><span class="o">-</span><span class="mi">1</span><span class="p">))</span>
      <span class="k">goto</span> <span class="n">invalid_payload</span><span class="p">;</span>
<span class="p">[</span><span class="mi">5</span><span class="p">]</span>
    <span class="n">strncpy</span><span class="p">(</span><span class="o">&amp;</span><span class="n">buf</span><span class="p">[</span><span class="n">buf_out_len</span><span class="p">],</span> <span class="p">(</span><span class="k">const</span> <span class="kt">char</span> <span class="o">*</span><span class="p">)</span><span class="o">&amp;</span><span class="n">packet</span><span class="o">-&gt;</span><span class="n">payload</span><span class="p">[</span><span class="n">offset</span><span class="p">],</span> <span class="n">len</span><span class="p">);</span>
    <span class="n">buf_out_len</span> <span class="o">+=</span> <span class="n">len</span><span class="p">;</span>
    <span class="n">buf</span><span class="p">[</span><span class="n">buf_out_len</span><span class="o">++</span><span class="p">]</span> <span class="o">=</span> <span class="sc">';'</span><span class="p">;</span>
    <span class="n">offset</span> <span class="o">+=</span> <span class="n">len</span><span class="p">;</span>
  <span class="p">}</span> <span class="k">else</span>
<span class="p">[</span><span class="mi">6</span><span class="p">]</span>
    <span class="n">offset</span> <span class="o">+=</span> <span class="mi">4</span> <span class="o">+</span> <span class="n">len</span><span class="p">;</span>
</code></pre></div></div>

<p>The <code class="language-plaintext highlighter-rouge">client_hash</code> variable decides whether the packet direction is server-to-client or client-to-server, but since the parsing pattern is the same for either direction it does not matter much for the sake of our discussion. For the sake of convenience we will examine the <code class="language-plaintext highlighter-rouge">!client_hash</code> case, but the same logic holds for the inverse.</p>

<p>At [1] we see that we have full control over a 32bit unsigned length integer. At [2] we see that <code class="language-plaintext highlighter-rouge">offset</code> is updated according to this controlled length variable based on an integer addition operation (<code class="language-plaintext highlighter-rouge">offset + 4 + len</code>). This arithmetic expression expands to 32bit integer values and is then truncated back to a 16bit integer value on the final assignment back into <code class="language-plaintext highlighter-rouge">offset</code>. This means that, given we have full control of the <code class="language-plaintext highlighter-rouge">len</code> variable, we can effectively integer wrap <code class="language-plaintext highlighter-rouge">offset</code> to be any value we wish it to be.</p>

<p>For example, to make <code class="language-plaintext highlighter-rouge">offset</code> become <code class="language-plaintext highlighter-rouge">n</code> where <code class="language-plaintext highlighter-rouge">n</code> is any desired 16bit integer value, we would simply set <code class="language-plaintext highlighter-rouge">len</code> to <code class="language-plaintext highlighter-rouge">0 - offset - 4 + n</code>.</p>

<p>The practical implication here is that, given at [4] the <code class="language-plaintext highlighter-rouge">offset</code> variable is used to ensure no out of bounds accesses occur, and given our ability to effectively set (and RESET) <code class="language-plaintext highlighter-rouge">offset</code> to any desired 16bit integer value, we can pass the intended bounds checks by resetting <code class="language-plaintext highlighter-rouge">offset</code> to a small enough value.</p>

<p>This integer overflow is the core issue resulting in what ultimately becomes a controlled remote heap overflow. However, to mold this scenario into a RCE-viable situation, some additional context is required.</p>

<p>We’ve established that we can effectively reset <code class="language-plaintext highlighter-rouge">offset</code> in-between the <code class="language-plaintext highlighter-rouge">strncpy</code> operations that copy remote controlled data into <code class="language-plaintext highlighter-rouge">buf</code>. When we examine the copy operation at [5], we note that that destination offset into <code class="language-plaintext highlighter-rouge">buf</code> is controlled by <code class="language-plaintext highlighter-rouge">buf_out_len</code>. We also note that <code class="language-plaintext highlighter-rouge">buf_out_len</code> is adjusted upward based on the <code class="language-plaintext highlighter-rouge">len</code> variable, which is the length of our remote controlled string.</p>

<p>For practical exploitation of this issue, the fact that <code class="language-plaintext highlighter-rouge">buf_out_len</code> is maintained as it’s own independent offset into the destination buffer becomes relevant.</p>

<p>Let’s recap:</p>

<ul>
  <li>We control <code class="language-plaintext highlighter-rouge">offset</code> through an integer overflow</li>
  <li>We can repeat a pattern of: <code class="language-plaintext highlighter-rouge">strncpy(&amp;buf[buf_out_len], controlled_data, controlled_len)</code>, adjust <code class="language-plaintext highlighter-rouge">buf_out_len</code> up by <code class="language-plaintext highlighter-rouge">controlled_len</code>, reset <code class="language-plaintext highlighter-rouge">offset</code> to any desired <code class="language-plaintext highlighter-rouge">n</code></li>
  <li>We can not directly overflow <code class="language-plaintext highlighter-rouge">buf</code> based on this controlled len due to the <code class="language-plaintext highlighter-rouge">controlled_len &gt;= packet-&gt;payload_packet_len-offset-1</code> check</li>
</ul>

<p>Because <code class="language-plaintext highlighter-rouge">packet-&gt;payload_packet_len</code> controls the <code class="language-plaintext highlighter-rouge">buf</code> memory allocation size, and is directly influenced by our packet size, the intuition that we can simply pack repeated large strings to trigger an offset overwrap here is less than ideal from an attacker perspective. However, what we CAN do is pack a single string into the KEXINIT SSH packet and then copy that string repeatedly. A single string will result in a <code class="language-plaintext highlighter-rouge">calloc</code> based on the string’s size + some minor SSH protocol overhead and since <code class="language-plaintext highlighter-rouge">buf_out_len</code> is not bounds checked at any point, we can reset the <code class="language-plaintext highlighter-rouge">offset</code> variable to point at that initial string data for each subsequent <code class="language-plaintext highlighter-rouge">strncpy</code> operation.</p>

<p>In other words, using the <code class="language-plaintext highlighter-rouge">offset</code> integer overflow primitive, we can trick the nDPI SSH dissector into repeatedly copying the same data into <code class="language-plaintext highlighter-rouge">&amp;buf[buf_out_len]</code>. Since <code class="language-plaintext highlighter-rouge">buf_out_len</code> is adjusted based on our controlled string length, and not otherwise sanity checked, we can write out of bounds as early as the 2nd repeat of the <code class="language-plaintext highlighter-rouge">strncpy</code> operation, pending string size vs protocol overhead (which you fully control).</p>

<p>This then becomes a controlled remote heap overflow primitive. Since the nDPI lib has a direct relationship to remotely controlled input, and it will allocate, deallocate, and populate heap memory in a direct 1:1 relationship to said remotely controlled input, this becomes a viable primitive to achieve remote code execution.</p>

<h3 id="out-of-bounds-read-in-sshcconcat_hash_string-ghsl-2020-052-cve-2020-11940">Out of bounds read in <code class="language-plaintext highlighter-rouge">ssh.c:concat_hash_string</code> (GHSL-2020-052, CVE-2020-11940)</h3>

<p>A comparatively minor, but related, repeating issue exists in the form of an OOB read, e.g. when examining the following snippet:</p>

<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="n">ssh</span><span class="p">.</span><span class="n">c</span><span class="o">:</span><span class="n">concat_hash_string</span>
<span class="p">...</span>
  <span class="cm">/* ssh.server_host_key_algorithms [None] */</span>
  <span class="n">len</span> <span class="o">=</span> <span class="n">ntohl</span><span class="p">(</span><span class="o">*</span><span class="p">(</span><span class="n">u_int32_t</span><span class="o">*</span><span class="p">)</span><span class="o">&amp;</span><span class="n">packet</span><span class="o">-&gt;</span><span class="n">payload</span><span class="p">[</span><span class="n">offset</span><span class="p">]);</span>
<span class="p">[</span><span class="mi">1</span><span class="p">]</span>
  <span class="n">offset</span> <span class="o">+=</span> <span class="mi">4</span> <span class="o">+</span> <span class="n">len</span><span class="p">;</span>

  <span class="cm">/* ssh.encryption_algorithms_client_to_server [C] */</span>
<span class="p">[</span><span class="mi">2</span><span class="p">]</span>
  <span class="n">len</span> <span class="o">=</span> <span class="n">ntohl</span><span class="p">(</span><span class="o">*</span><span class="p">(</span><span class="n">u_int32_t</span><span class="o">*</span><span class="p">)</span><span class="o">&amp;</span><span class="n">packet</span><span class="o">-&gt;</span><span class="n">payload</span><span class="p">[</span><span class="n">offset</span><span class="p">]);</span>
<span class="p">...</span>
</code></pre></div></div>

<p>We note that at [1], <code class="language-plaintext highlighter-rouge">offset</code> is calculated per the previously discussed integer arithmetic, which is susceptible to integer overflow. However, beyond that, we also note that at [2] the resulting <code class="language-plaintext highlighter-rouge">offset</code> value is immediately used as an index into packet data without any bounds check. This may result in an OOB read due to <code class="language-plaintext highlighter-rouge">offset</code> being fully user controlled.</p>

<p>A very similar pattern is repeated any time a new <code class="language-plaintext highlighter-rouge">offset</code> is calculated in a path that does not perform an explicit check against the resulting <code class="language-plaintext highlighter-rouge">offset</code> value, e.g.:</p>

<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code>  <span class="cm">/* ssh.encryption_algorithms_client_to_server [C] */</span>
  <span class="n">len</span> <span class="o">=</span> <span class="n">ntohl</span><span class="p">(</span><span class="o">*</span><span class="p">(</span><span class="n">u_int32_t</span><span class="o">*</span><span class="p">)</span><span class="o">&amp;</span><span class="n">packet</span><span class="o">-&gt;</span><span class="n">payload</span><span class="p">[</span><span class="n">offset</span><span class="p">]);</span>

  <span class="k">if</span><span class="p">(</span><span class="n">client_hash</span><span class="p">)</span> <span class="p">{</span>
    <span class="n">offset</span> <span class="o">+=</span> <span class="mi">4</span><span class="p">;</span>

    <span class="k">if</span><span class="p">((</span><span class="n">offset</span> <span class="o">&gt;=</span> <span class="n">packet</span><span class="o">-&gt;</span><span class="n">payload_packet_len</span><span class="p">)</span> <span class="o">||</span> <span class="p">(</span><span class="n">len</span> <span class="o">&gt;=</span> <span class="n">packet</span><span class="o">-&gt;</span><span class="n">payload_packet_len</span><span class="o">-</span><span class="n">offset</span><span class="o">-</span><span class="mi">1</span><span class="p">))</span>
      <span class="k">goto</span> <span class="n">invalid_payload</span><span class="p">;</span>

    <span class="n">strncpy</span><span class="p">(</span><span class="o">&amp;</span><span class="n">buf</span><span class="p">[</span><span class="n">buf_out_len</span><span class="p">],</span> <span class="p">(</span><span class="k">const</span> <span class="kt">char</span> <span class="o">*</span><span class="p">)</span><span class="o">&amp;</span><span class="n">packet</span><span class="o">-&gt;</span><span class="n">payload</span><span class="p">[</span><span class="n">offset</span><span class="p">],</span> <span class="n">len</span><span class="p">);</span>
    <span class="n">buf_out_len</span> <span class="o">+=</span> <span class="n">len</span><span class="p">;</span>
    <span class="n">buf</span><span class="p">[</span><span class="n">buf_out_len</span><span class="o">++</span><span class="p">]</span> <span class="o">=</span> <span class="sc">';'</span><span class="p">;</span>
    <span class="n">offset</span> <span class="o">+=</span> <span class="n">len</span><span class="p">;</span>
  <span class="p">}</span> <span class="k">else</span>
<span class="p">[</span><span class="mi">1</span><span class="p">]</span>
    <span class="n">offset</span> <span class="o">+=</span> <span class="mi">4</span> <span class="o">+</span> <span class="n">len</span><span class="p">;</span>

  <span class="cm">/* ssh.encryption_algorithms_server_to_client [S] */</span>
<span class="p">[</span><span class="mi">2</span><span class="p">]</span>
  <span class="n">len</span> <span class="o">=</span> <span class="n">ntohl</span><span class="p">(</span><span class="o">*</span><span class="p">(</span><span class="n">u_int32_t</span><span class="o">*</span><span class="p">)</span><span class="o">&amp;</span><span class="n">packet</span><span class="o">-&gt;</span><span class="n">payload</span><span class="p">[</span><span class="n">offset</span><span class="p">]);</span>
</code></pre></div></div>

<p>Again, at [1] the initial remote controlled <code class="language-plaintext highlighter-rouge">len</code> variable is used to set <code class="language-plaintext highlighter-rouge">offset</code>, immediately after at [2] the resulting <code class="language-plaintext highlighter-rouge">offset</code> is used as an index into packet data without any bounds check. This may result in an OOB read due to <code class="language-plaintext highlighter-rouge">offset</code> being fully user controlled.</p>

<h3 id="impact">Impact</h3>

<p>These issues may lead to <code class="language-plaintext highlighter-rouge">Remote Code Execution</code> in the case of <code class="language-plaintext highlighter-rouge">GHSL-2020-051</code> and <code class="language-plaintext highlighter-rouge">Denial of Service</code> in the case of <code class="language-plaintext highlighter-rouge">GHSL-2020-052</code>.</p>

<h2 id="remediation">Remediation</h2>

<p>These issues were addressed in the following commit:</p>

<p><a href="https://github.com/ntop/nDPI/commit/c120cca66272646c4277d71fa769d020b1026b28">https://github.com/ntop/nDPI/commit/c120cca66272646c4277d71fa769d020b1026b28</a></p>

<h2 id="coordinated-disclosure-timeline">Coordinated Disclosure Timeline</h2>

<p>This report was subject to the GHSL <a href="https://securitylab.github.com/advisories/#policy">coordinated disclosure policy</a>.</p>

<ul>
  <li>03/23/2020: initial report sent to ntop team</li>
  <li>03/24/2020: maintainer acknowledges report receipt and begins triage process</li>
  <li>03/30/2020: additional findings sent to maintainer</li>
  <li>04/05/2020: maintainer merges fixes for initial findings</li>
  <li>04/15/2020: maintainer merges fixes for additional findings</li>
  <li>04/21/2020: public advisory</li>
  <li>04/29/2020: additional integer overflow for 32bit systems reported by @rhuizer</li>
  <li>04/30/2020: revised patch committed by maintainer</li>
</ul>

<h2 id="credit">Credit</h2>

<p>This issue was discovered and reported by GHSL team member <a href="https://github.com/anticomputer">@anticomputer (Bas Alberts)</a>.</p>

<p>An additional integer overflow issue affecting 32bit platforms was reported by <a href="https://github.com/rhuizer">@rhuizer (Ronald Huizer)</a>.</p>

<h2 id="contact">Contact</h2>

<p>You can contact the GHSL team at <code class="language-plaintext highlighter-rouge">securitylab@github.com</code>, please include <code class="language-plaintext highlighter-rouge">GHSL-2020-051</code> or <code class="language-plaintext highlighter-rouge">GHSL-2020-052</code> in any communication regarding this issue.