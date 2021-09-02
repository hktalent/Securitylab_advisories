>
    <header class="post-header d-block mb-6">
      <div class="date text-mono f5 my-3">April 21, 2020</div>
      <h1 class="my-2 h00-mktg lh-condensed">GHSL-2020-007: Out-of-bounds write in Android Open Source Project - CVE-2020-0072</h1>

      
      
      
      
      

      

      <a target="_blank" class="sc-frDJqD SgxRc d-inline-flex flex-row flex-items-center text-gray" href="https://github.com/m-y-mo">
        <img class="mr-3" src="https://avatars.githubusercontent.com/u/15773368?s=35" height="35" width="35">
        <span>Man Yue Mo</span>
      </a>
    </header>

    <main id="content" class="markdown-body" aria-label="Content">
      <h2 id="summary">Summary</h2>

<p>An Out-Of-Bounds write of <code class="language-plaintext highlighter-rouge">lock_tlv</code> in Android’s <code class="language-plaintext highlighter-rouge">rw_t2t_handle_tlv_detect_rsp</code> (NFC) could leads to remote code execution.</p>

<h2 id="product">Product</h2>
<p>Android Open Source Project</p>

<h2 id="cve">CVE</h2>
<p>CVE-2020-0072</p>

<h2 id="tested-version">Tested Version</h2>
<p>Pixel3a with build id: QQ1A.191205.011 (tag android-10.0.0_r16). (latest publicly available build as of the time of writing) Proxmark3 used is the RDV4.01</p>

<h2 id="details">Details</h2>

<p>In the <code class="language-plaintext highlighter-rouge">rw_t2t_handle_tlv_detect_rsp</code> function, <code class="language-plaintext highlighter-rouge">p_t2t-&gt;lock_tlv</code> is written to with index <code class="language-plaintext highlighter-rouge">p_t2t-&gt;num_lock_tlvs</code> <sup id="fnref:1" role="doc-noteref"><a href="#fn:1" class="footnote" rel="footnote">1</a></sup>. As <code class="language-plaintext highlighter-rouge">p_t2t-&gt;num_lock_tlvs</code> is incremented here <sup id="fnref:2" role="doc-noteref"><a href="#fn:2" class="footnote" rel="footnote">2</a></sup>, by repeatedly triggering this branch, it is possible to increase the value of <code class="language-plaintext highlighter-rouge">p_t2t-&gt;num_lock_tlvs</code> beyond the size of <code class="language-plaintext highlighter-rouge">p_t2t-&gt;lock_tlv</code> (<code class="language-plaintext highlighter-rouge">RW_T2T_MAX_LOCK_TLVS</code>), causing an OOB write.</p>

<h3 id="impact">Impact</h3>

<p>If succesfuly exploited, an attacker within NFC range could obtain remote code execution on android device’s NFC daemon.</p>

<h2 id="coordinated-disclosure-timeline">Coordinated Disclosure Timeline</h2>
<ul>
  <li>07/01/2020 Reported as <a href="https://issuetracker.google.com/issues/147259760">issue 147259760</a>, Android ID 147310271.</li>
  <li>06/04/2020 Fix published in <a href="https://source.android.com/security/bulletin/2020-04-01">2020-04-01 Andriod Security patch</a></li>
</ul>

<h2 id="credit">Credit</h2>

<p>This issue was discovered and reported by GHSL team member <a href="https://github.com/m-y-mo">@m-y-mo (Man Yue Mo)</a>.</p>

<h2 id="contact">Contact</h2>

<p>You can contact the GHSL team at <code class="language-plaintext highlighter-rouge">securitylab@github.com</code>, please include the <code class="language-plaintext highlighter-rouge">GHSL-2020-007</code> in any communication regarding this issue.</p>

<div class="footnotes" role="doc-endnotes">
  <ol>
    <li id="fn:1" role="doc-endnote">
      <p>https://android.googlesource.com/platform/system/nfc/+/a581069b8f449f5e5d7804ac70fa4d9d57a2b94e/src/nfc/tags/rw_t2t_ndef.cc#609 <a href="#fnref:1" class="reversefootnote" role="doc-backlink">&#8617;</a></p>
    </li>
    <li id="fn:2" role="doc-endnote">
      <p>https://android.googlesource.com/platform/system/nfc/+/a581069b8f449f5e5d7804ac70fa4d9d57a2b94e/src/nfc/tags/rw_t2t_ndef.cc#636 <a href="#fnref:2" class="reversefootnote" role="doc-backlink">&#8617;</a></p>
    </li>
  </ol>
