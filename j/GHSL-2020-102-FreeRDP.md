>
    <header class="post-header d-block mb-6">
      <div class="date text-mono f5 my-3">June 17, 2020</div>
      <h1 class="my-2 h00-mktg lh-condensed">GHSL-2020-102: Heap overflow in FreeRDP crypto_rsa_common - CVE-2020-13398</h1>

      
      
      
      
      

      

      <a target="_blank" class="sc-frDJqD SgxRc d-inline-flex flex-row flex-items-center text-gray" href="https://github.com/antonio-morales">
        <img class="mr-3" src="https://avatars.githubusercontent.com/u/55253029?s=35" height="35" width="35">
        <span>Antonio Morales</span>
      </a>
    </header>

    <main id="content" class="markdown-body" aria-label="Content">
      <h2 id="summary">Summary</h2>

<p>An out-of-bounds (OOB) write vulnerability has been detected in FreeRDP’s <code class="language-plaintext highlighter-rouge">crypto_rsa_common</code> (heap overflow).</p>

<h2 id="product">Product</h2>

<p>FreeRDP</p>

<h2 id="tested-version">Tested Version</h2>

<p>Development version - master branch (May 19, 2020)</p>

<h2 id="details-out-of-bound-write-in-crypto_rsa_common">Details: Out-of-bound write in <code class="language-plaintext highlighter-rouge">crypto_rsa_common</code></h2>

<p>The <code class="language-plaintext highlighter-rouge">crypto_rsa_common</code> function in <code class="language-plaintext highlighter-rouge">crypto.c</code> performs the following call to <code class="language-plaintext highlighter-rouge">memcpy</code>:</p>

<div class="language-plaintext highlighter-rouge"><div class="highlight"><pre class="highlight"><code>crypto.c:crypto_rsa_common:
...
static int crypto_rsa_common(const BYTE* input, int length, UINT32 key_length, const BYTE* modulus,
                             const BYTE* exponent, int exponent_size, BYTE* output)
{
...
memcpy(input_reverse, input, length)
...
</code></pre></div></div>

<p>The <code class="language-plaintext highlighter-rouge">input_reverse</code> buffer is allocated as:</p>

<div class="language-plaintext highlighter-rouge"><div class="highlight"><pre class="highlight"><code>input_reverse = (BYTE*)malloc(2 * key_length + exponent_size);
</code></pre></div></div>

<p>So we notice a classic pattern in which there’s a disjointed relationship between an integer that influences the POPULATION of a memory region (<code class="language-plaintext highlighter-rouge">length</code>) and an integer that influences the ALLOCATION of a memory region (<code class="language-plaintext highlighter-rouge">key_length</code>).</p>

<p>While in many of the paths to this code there exists some loose sanity checking logic that is supposed to ensure there is a logical relationship between these two variables, this logic can often be circumvented to subsequently trigger heap overflow due to an underallocation based on control of the <code class="language-plaintext highlighter-rouge">key_length</code> variable.</p>

<p>There exist multiple paths to trigger this scenario throughout the codebase since <code class="language-plaintext highlighter-rouge">crypto_rsa_common</code> is used as the underlying API for most all encrypt/decrypt operations, and many of them may be influenced by remotely controlled input.</p>

<p>For example:</p>

<div class="language-plaintext highlighter-rouge"><div class="highlight"><pre class="highlight"><code>BOOL license_encrypt_premaster_secret(rdpLicense* license)
{
	BYTE* EncryptedPremasterSecret;
	if (!license_get_server_rsa_public_key(license))
		return FALSE;
#ifdef WITH_DEBUG_LICENSE
	WLog_DBG(TAG, "Modulus (%" PRIu32 " bits):", license-&gt;ModulusLength * 8);
	winpr_HexDump(TAG, WLOG_DEBUG, license-&gt;Modulus, license-&gt;ModulusLength);
	WLog_DBG(TAG, "Exponent:");
	winpr_HexDump(TAG, WLOG_DEBUG, license-&gt;Exponent, 4);
#endif
	EncryptedPremasterSecret = (BYTE*)calloc(1, license-&gt;ModulusLength);
	if (!EncryptedPremasterSecret)
		return FALSE;
	license-&gt;EncryptedPremasterSecret-&gt;type = BB_RANDOM_BLOB;
	license-&gt;EncryptedPremasterSecret-&gt;length = PREMASTER_SECRET_LENGTH;
#ifndef LICENSE_NULL_PREMASTER_SECRET
	license-&gt;EncryptedPremasterSecret-&gt;length = crypto_rsa_public_encrypt(
	    license-&gt;PremasterSecret, PREMASTER_SECRET_LENGTH, license-&gt;ModulusLength, license-&gt;Modulus,
	    license-&gt;Exponent, EncryptedPremasterSecret);
</code></pre></div></div>

<p>In this code path <code class="language-plaintext highlighter-rouge">crypto_rsa_public_encrypt</code> calls through to <code class="language-plaintext highlighter-rouge">crypto_rsa_common</code>. We note that the <code class="language-plaintext highlighter-rouge">length</code> variable is set to a static value <code class="language-plaintext highlighter-rouge">PREMASTER_SECRET_LENGTH</code> (48), yet the <code class="language-plaintext highlighter-rouge">key_length</code> variable is set via the server-side public key controlled <code class="language-plaintext highlighter-rouge">license-&gt;ModulusLength</code>, so in this case any <code class="language-plaintext highlighter-rouge">key_length</code> value that results in an allocation smaller than 48 bytes would be sufficient to trigger heap overflow.</p>

<h3 id="impact">Impact</h3>

<p>This issue may lead to remote heap overflow and potentially Remote Code Execution (RCE).</p>

<h2 id="cve">CVE</h2>

<ul>
  <li>CVE-2020-13398</li>
</ul>

<h2 id="coordinated-disclosure-timeline">Coordinated Disclosure Timeline</h2>

<ul>
  <li>05/19/2020: Vendor contacted</li>
  <li>05/19/2020: Vendor acknowledges report</li>
  <li>05/19/2020: Bug fixed and patch released by the vendor</li>
</ul>

<h2 id="resources">Resources</h2>

<ul>
  <li>https://github.com/FreeRDP/FreeRDP/commit/8305349a943c68b1bc8c158f431dc607655aadea</li>
  <li>https://github.com/FreeRDP/FreeRDP/commit/8fb6336a4072abcee8ce5bd6ae91104628c7bb69</li>
</ul>

<h2 id="credit">Credit</h2>

<p>This issue was discovered and reported by GHSL team member <a href="https://github.com/antonio-morales">@antonio-morales (Antonio Morales)</a>.</p>

<h2 id="contact">Contact</h2>

<p>You can contact the GHSL team at <code class="language-plaintext highlighter-rouge">securitylab@github.com</code>, please include <code class="language-plaintext highlighter-rouge">GHSL-2020-102</code> in any communication regarding this issue.