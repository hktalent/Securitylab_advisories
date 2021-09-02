>
    <header class="post-header d-block mb-6">
      <div class="date text-mono f5 my-3">June 17, 2020</div>
      <h1 class="my-2 h00-mktg lh-condensed">GHSL-2020-101: NULL dereference in FreeRDP FIPS routines - CVE-2020-13397</h1>

      
      
      
      
      

      

      <a target="_blank" class="sc-frDJqD SgxRc d-inline-flex flex-row flex-items-center text-gray" href="https://github.com/antonio-morales">
        <img class="mr-3" src="https://avatars.githubusercontent.com/u/55253029?s=35" height="35" width="35">
        <span>Antonio Morales</span>
      </a>
    </header>

    <main id="content" class="markdown-body" aria-label="Content">
      <h2 id="summary">Summary</h2>

<p>A NULL dereference vulnerability has been detected in FreeRDP’s <code class="language-plaintext highlighter-rouge">security_fips_decrypt</code> routine due to use of uninitialized pointer values. This issue has been addressed in FreeRDP 2.1.1.</p>

<h2 id="product">Product</h2>

<p>FreeRDP</p>

<h2 id="tested-version">Tested Version</h2>

<p>Development version - master branch (May 18, 2020)</p>

<h2 id="details-null-dereference-in-security_fips_decrypt">Details: NULL dereference in <code class="language-plaintext highlighter-rouge">security_fips_decrypt</code></h2>

<p>It is possible for a malicious FreeRDP server to confuse FreeRDP client state and make it enter Federal Information Processing Standard (FIPS) specific program logic at a point where the client session context has not been properly initialized for FIPS use.</p>

<p>More specifically, if a FreeRDP server claims <code class="language-plaintext highlighter-rouge">ENCRYPTION_METHOD_FIPS</code> (0x00000010) for a FreeRDP client session that expects to be operating under a Network Layer Authentication (NLA) Security session context, the client may be tricked into following FIPS specific code paths based on session state checks such as:</p>

<div class="language-plaintext highlighter-rouge"><div class="highlight"><pre class="highlight"><code>libfreerdp/core/rdp.c:
...
 if (rdp-&gt;settings-&gt;EncryptionMethods == ENCRYPTION_METHOD_FIPS)
...
</code></pre></div></div>

<p>Which are directly controlled by remote input from the FreeRDP server into the <code class="language-plaintext highlighter-rouge">serverEncryptionmethod</code> variable, e.g.:</p>

<div class="language-plaintext highlighter-rouge"><div class="highlight"><pre class="highlight"><code>libfreerdp/core/gcc.c:
...
( Stream_Read_UINT32(s, serverEncryptionMethod))
...
</code></pre></div></div>

<p>As a result the <code class="language-plaintext highlighter-rouge">security_fips_decrypt</code> function may be called at a point where the <code class="language-plaintext highlighter-rouge">rdp</code> structure contains an uninitialized <code class="language-plaintext highlighter-rouge">rdp-&gt;fips_decrypt</code> pointer value. Since the <code class="language-plaintext highlighter-rouge">rdp</code> structure itself is allocated through <code class="language-plaintext highlighter-rouge">calloc</code> it is initialized with zeroed memory, thus resulting in a NULL pointer dereference in the following code path:</p>

<div class="language-plaintext highlighter-rouge"><div class="highlight"><pre class="highlight"><code>libfreerdp/core/security.c:security_fips_decrypt:
...
if (!winpr_Cipher_Update(rdp-&gt;fips_decrypt, data, length, data, &amp;olen))
...
</code></pre></div></div>

<h3 id="impact">Impact</h3>

<p>This issue may lead to NULL pointer dereference.</p>

<h2 id="cve">CVE</h2>

<ul>
  <li>CVE-2020-13397</li>
</ul>

<h2 id="coordinated-disclosure-timeline">Coordinated Disclosure Timeline</h2>

<p>This report was subject to the GHSL <a href="https://securitylab.github.com/advisories/#policy">coordinated disclosure policy</a>.</p>

<ul>
  <li>05/18/2020: Vendor contacted</li>
  <li>05/19/2020: Vendor acknowledges report</li>
  <li>05/19/2020: Bug fixed and patch released by the vendor</li>
</ul>

<h2 id="resources">Resources</h2>

<ul>
  <li>https://github.com/FreeRDP/FreeRDP/commit/8fb6336a4072abcee8ce5bd6ae91104628c7bb69</li>
  <li>https://github.com/FreeRDP/FreeRDP/commit/d6cd14059b257318f176c0ba3ee0a348826a9ef8</li>
</ul>

<h2 id="credit">Credit</h2>

<p>This issue was discovered and reported by GHSL team member <a href="https://github.com/antonio-morales">@antonio-morales (Antonio Morales)</a>.</p>

<h2 id="contact">Contact</h2>

<p>You can contact the GHSL team at <code class="language-plaintext highlighter-rouge">securitylab@github.com</code>, please include the <code class="language-plaintext highlighter-rouge">GHSL-2020-101</code> in any communication regarding this issue.</