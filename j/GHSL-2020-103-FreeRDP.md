>
    <header class="post-header d-block mb-6">
      <div class="date text-mono f5 my-3">July 1, 2020</div>
      <h1 class="my-2 h00-mktg lh-condensed">GHSL-2020-103: OOB read vulnerability in FreeRDP license_read_new_or_upgrade_license_packet - CVE-2020-11099</h1>

      
      
      
      
      

      

      <a target="_blank" class="sc-frDJqD SgxRc d-inline-flex flex-row flex-items-center text-gray" href="https://github.com/antonio-morales">
        <img class="mr-3" src="https://avatars.githubusercontent.com/u/55253029?s=35" height="35" width="35">
        <span>Antonio Morales</span>
      </a>
    </header>

    <main id="content" class="markdown-body" aria-label="Content">
      <h2 id="summary">Summary</h2>

<p>An out-of-bounds (OOB) read vulnerability has been detected in FreeRDP’s <code class="language-plaintext highlighter-rouge">license_read_new_or_upgrade_license_packet</code> function due to an incorrect handling of data blob sizes.</p>

<h2 id="product">Product</h2>

<p>FreeRDP</p>

<h2 id="tested-version">Tested Version</h2>

<p>Development version - master branch (May 21, 2020)</p>

<h2 id="details-out-of-bound-read-in-license_read_new_or_upgrade_license_packet">Details: Out-of-bound read in <code class="language-plaintext highlighter-rouge">license_read_new_or_upgrade_license_packet</code></h2>

<p>The <code class="language-plaintext highlighter-rouge">license_read_new_or_upgrade_license_packet</code> function in <code class="language-plaintext highlighter-rouge">license.c</code> performs a call to <code class="language-plaintext highlighter-rouge">Stream_Read_UINT16(licenseStream, os_minor)</code> (line 1255), where <code class="language-plaintext highlighter-rouge">licenseStream</code> is a wStream* whose size can be controlled indirectly by a potential attacker.</p>

<p><code class="language-plaintext highlighter-rouge">Stream_Read_</code> are a family of macros that read the given amount of bits from the specified <code class="language-plaintext highlighter-rouge">wStream</code> and then move the stream’s current position that many bits forward:</p>

<p><a href="https://github.com/FreeRDP/FreeRDP/blob/fd925009386bd9321496b16acb46c2efc2ecebd7/winpr/include/winpr/stream.h#L77">View on GitHub!</a></p>
<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="cm">/* winpr/include/winpr/stream.h */</span>

<span class="cp">#define _stream_read_n16_le(_t, _s, _v, _p)                                      \
	do                                                                           \
	{                                                                            \
		(_v) = (_t)((*(_s)-&gt;pointer) + (((UINT16)(*((_s)-&gt;pointer + 1))) &lt;&lt; 8)); \
		if (_p)                                                                  \
			Stream_Seek(_s, sizeof(_t));                                         \
	} while (0)
</span>
<span class="p">...</span>

<span class="cp">#define Stream_Read_UINT16(_s, _v) _stream_read_n16_le(UINT16, _s, _v, TRUE)
</span></code></pre></div></div>

<p>As we mentioned before, the <code class="language-plaintext highlighter-rouge">licenseStream</code> size can be controlled by an attacker. This is because in the RDP protocol, a data blob’s length is read as a separate field:</p>

<p><a href="https://github.com/FreeRDP/FreeRDP/blob/c7187928e9373d68476e6e7989336956c5dfa30d/libfreerdp/core/license.c#L1182">View on GitHub!</a></p>
<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="cm">/* libfreerdp/core/license.c */</span>

<span class="k">static</span> <span class="n">BOOL</span> <span class="nf">license_read_encrypted_blob</span><span class="p">(</span><span class="k">const</span> <span class="n">rdpLicense</span><span class="o">*</span> <span class="n">license</span><span class="p">,</span> <span class="n">wStream</span><span class="o">*</span> <span class="n">s</span><span class="p">,</span> <span class="n">LICENSE_BLOB</span><span class="o">*</span> <span class="n">target</span><span class="p">)</span>
<span class="p">{</span>
<span class="p">...</span>

  <span class="n">Stream_Read_UINT16</span><span class="p">(</span><span class="n">s</span><span class="p">,</span> <span class="n">wBlobLen</span><span class="p">);</span>

<span class="p">...</span>
<span class="p">}</span>
</code></pre></div></div>

<p>Since there is no logic that range checks <code class="language-plaintext highlighter-rouge">wBlobLen</code>, a malicious server could send a small value (even zero). This would result in an abnormally small “Stream_New” allocation (calBlob-&gt;length = wBlobLen):</p>

<p><a href="https://github.com/FreeRDP/FreeRDP/blob/c7187928e9373d68476e6e7989336956c5dfa30d/libfreerdp/core/license.c#L1251">View on GitHub!</a></p>
<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="cm">/* libfreerdp/core/license.c */</span>

<span class="n">licenseStream</span> <span class="o">=</span> <span class="n">Stream_New</span><span class="p">(</span><span class="n">calBlob</span><span class="o">-&gt;</span><span class="n">data</span><span class="p">,</span> <span class="n">calBlob</span><span class="o">-&gt;</span><span class="n">length</span><span class="p">);</span>

</code></pre></div></div>

<p>As seen above <code class="language-plaintext highlighter-rouge">licenseStream</code> points to <code class="language-plaintext highlighter-rouge">calBlob-&gt;data</code>, and given that <code class="language-plaintext highlighter-rouge">Stream_Read_</code> functions seek the read pointer, the subsequent calls to <code class="language-plaintext highlighter-rouge">Stream_Read_</code> could move the pointer far beyond the array’s limits:</p>

<p><a href="https://github.com/FreeRDP/FreeRDP/blob/c7187928e9373d68476e6e7989336956c5dfa30d/libfreerdp/core/license.c#L1255">View on GitHub!</a></p>
<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="cm">/* libfreerdp/core/license.c */</span>

<span class="p">...</span>

 <span class="n">Stream_Read_UINT16</span><span class="p">(</span><span class="n">licenseStream</span><span class="p">,</span> <span class="n">os_minor</span><span class="p">);</span>
 <span class="n">Stream_Read_UINT16</span><span class="p">(</span><span class="n">licenseStream</span><span class="p">,</span> <span class="n">os_major</span><span class="p">);</span>

 <span class="cm">/* Scope */</span>
 <span class="n">Stream_Read_UINT32</span><span class="p">(</span><span class="n">licenseStream</span><span class="p">,</span> <span class="n">cbScope</span><span class="p">);</span>
<span class="p">...</span>

</code></pre></div></div>

<p>As a result, OOB reads can occur resulting in accessing a memory location that is outside of the boundaries of the <code class="language-plaintext highlighter-rouge">calBlob-&gt;data</code> memory region.</p>

<h3 id="impact">Impact</h3>

<p>This issue may lead to Out-of-Bounds read.</p>

<h2 id="cve">CVE</h2>

<ul>
  <li>CVE-2020-11099</li>
</ul>

<h2 id="coordinated-disclosure-timeline">Coordinated Disclosure Timeline</h2>

<p>This report was subject to the GHSL <a href="https://securitylab.github.com/advisories/#policy">coordinated disclosure policy</a>.</p>

<ul>
  <li>05/21/2020: Vendor contacted</li>
  <li>05/26/2020: Vendor acknowledges report</li>
  <li>06/22/2020: Bug fixed and patch released by the vendor</li>
</ul>

<h2 id="supporting-resources">Supporting Resources</h2>

<ul>
  <li>https://github.com/FreeRDP/FreeRDP/security/advisories/GHSA-977w-866x-4v5h</li>
  <li>https://github.com/FreeRDP/FreeRDP/commit/6ade7b4cbfd71c54b3d724e8f2d6ac76a58e879a</li>
</ul>

<h2 id="credit">Credit</h2>

<p>This issue was discovered and reported by GHSL team member <a href="https://github.com/antonio-morales">@antonio-morales (Antonio Morales)</a>.</p>

<h2 id="contact">Contact</h2>

<p>You can contact the GHSL team at <code class="language-plaintext highlighter-rouge">securitylab@github.com</code>, please include the <code class="language-plaintext highlighter-rouge">GHSL-2020-103</code> in any communication regarding thi