>
    <header class="post-header d-block mb-6">
      <div class="date text-mono f5 my-3">April 21, 2020</div>
      <h1 class="my-2 h00-mktg lh-condensed">GHSL-2020-006: Out-Of-Bounds write in Android Open Source Project - CVE-2020-0073</h1>

      
      
      
      
      

      

      <a target="_blank" class="sc-frDJqD SgxRc d-inline-flex flex-row flex-items-center text-gray" href="https://github.com/m-y-mo">
        <img class="mr-3" src="https://avatars.githubusercontent.com/u/15773368?s=35" height="35" width="35">
        <span>Man Yue Mo</span>
      </a>
    </header>

    <main id="content" class="markdown-body" aria-label="Content">
      <h2 id="summary">Summary</h2>

<p>Out-of-Bounds write in Android’s <code class="language-plaintext highlighter-rouge">rw_t2t_handle_tlv_detect_rsp</code> (NFC) could allow an attacker at NFC range to obtain remote code execution</p>

<h2 id="product">Product</h2>
<p>Android Open Source Project</p>

<h2 id="cve">CVE</h2>
<p>CVE-2020-0073</p>

<h2 id="tested-version">Tested Version</h2>
<p>Pixel3a with build id: QQ1A.191205.011 (tag android-10.0.0_r16). (latest publicly available build as of the time of writing) Proxmark3 used is the RDV4.01</p>

<h2 id="details">Details</h2>

<p>In the <code class="language-plaintext highlighter-rouge">rw_t2t_handle_tlv_detect_rsp</code> function, <code class="language-plaintext highlighter-rouge">p_t2t-&gt;lockbyte</code> is accessed with the index <code class="language-plaintext highlighter-rouge">p_t2t-&gt;num_lockbytes</code> <sup id="fnref:1" role="doc-noteref"><a href="#fn:1" class="footnote" rel="footnote">1</a></sup>, while <code class="language-plaintext highlighter-rouge">p_t2t-&gt;num_lockbytes</code> increases during the loop. Although there is a check <sup id="fnref:2" role="doc-noteref"><a href="#fn:2" class="footnote" rel="footnote">2</a></sup> to ensure that <code class="language-plaintext highlighter-rouge">p_t2t-&gt;num_lockbytes</code> cannot be increased more than <code class="language-plaintext highlighter-rouge">RW_T2T_MAX_LOCK_BYTES</code> (length of <code class="language-plaintext highlighter-rouge">p_t2t-&gt;lockbytes</code>) number of times during the loop, this is not sufficient to prevent overflow as the loop can be triggered multiple times during the detection sequence by repeatedly sending the following response:</p>

<div class="language-plaintext highlighter-rouge"><div class="highlight"><pre class="highlight"><code>  {0x00, 0x00, 0x01, 0x03,
   0x00, 0xf6, 0x00, 0x00,
   0x00, 0x00, 0x00, 0x00,
   0x0a, 0x00, 0x00, 0x00}
</code></pre></div></div>

<p>This will lead to a stack OOB write, which, due to the layout of the object <code class="language-plaintext highlighter-rouge">rw_cb</code> (type <code class="language-plaintext highlighter-rouge">tRW_CB</code>) <sup id="fnref:3" role="doc-noteref"><a href="#fn:3" class="footnote" rel="footnote">3</a></sup> and <code class="language-plaintext highlighter-rouge">p_t2t</code> (type <code class="language-plaintext highlighter-rouge">tRW_T2T_CB</code>, which is <code class="language-plaintext highlighter-rouge">tcb</code> in <code class="language-plaintext highlighter-rouge">rw_cb</code>) <sup id="fnref:4" role="doc-noteref"><a href="#fn:4" class="footnote" rel="footnote">4</a></sup>, will ended up overwriting the function pointer <code class="language-plaintext highlighter-rouge">p_cback</code> <sup id="fnref:5" role="doc-noteref"><a href="#fn:5" class="footnote" rel="footnote">5</a></sup>, that is executed in the end of the detection.</p>

<h3 id="impact">Impact</h3>

<p>If succesfuly exploited, an attacker within NFC range could obtain remote code execution on android device’s NFC daemon.</p>

<h2 id="coordinated-disclosure-timeline">Coordinated Disclosure Timeline</h2>
<ul>
  <li>07/01/2020 Reported as <a href="https://issuetracker.google.com/issues/147259758">issue 147259758</a>, Android ID 147309942.</li>
  <li>06/04/2020 Fix published in <a href="https://source.android.com/security/bulletin/2020-04-01">2020-04-01 Andriod Security patch</a></li>
</ul>

<h2 id="credit">Credit</h2>

<p>This issue was discovered and reported by GHSL team member <a href="https://github.com/m-y-mo">@m-y-mo (Man Yue Mo)</a>.</p>

<h2 id="contact">Contact</h2>

<p>You can contact the GHSL team at <code class="language-plaintext highlighter-rouge">securitylab@github.com</code>, please include the <code class="language-plaintext highlighter-rouge">GHSL-2020-006</code> in any communication regarding this issue.</p>

<div class="footnotes" role="doc-endnotes">
  <ol>
    <li id="fn:1" role="doc-endnote">
      <p>https://android.googlesource.com/platform/system/nfc/+/a581069b8f449f5e5d7804ac70fa4d9d57a2b94e/src/nfc/tags/rw_t2t_ndef.cc#629 <a href="#fnref:1" class="reversefootnote" role="doc-backlink">&#8617;</a></p>
    </li>
    <li id="fn:2" role="doc-endnote">
      <p>https://android.googlesource.com/platform/system/nfc/+/a581069b8f449f5e5d7804ac70fa4d9d57a2b94e/src/nfc/tags/rw_t2t_ndef.cc#624 <a href="#fnref:2" class="reversefootnote" role="doc-backlink">&#8617;</a></p>
    </li>
    <li id="fn:3" role="doc-endnote">
      <p>https://android.googlesource.com/platform/system/nfc/+/a581069b8f449f5e5d7804ac70fa4d9d57a2b94e/src/nfc/include/rw_int.h#743 <a href="#fnref:3" class="reversefootnote" role="doc-backlink">&#8617;</a></p>
    </li>
    <li id="fn:4" role="doc-endnote">
      <p>https://android.googlesource.com/platform/system/nfc/+/a581069b8f449f5e5d7804ac70fa4d9d57a2b94e/src/nfc/include/rw_int.h#460 <a href="#fnref:4" class="reversefootnote" role="doc-backlink">&#8617;</a></p>
    </li>
    <li id="fn:5" role="doc-endnote">
      <p>https://android.googlesource.com/platform/system/nfc/+/a581069b8f449f5e5d7804ac70fa4d9d57a2b94e/src/nfc/include/rw_int.h#745 <a href="#fnref:5" class="reversefootnote" role="doc-backlink">&#8617;</a></p>
    </li>
  </o