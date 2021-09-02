>
    <header class="post-header d-block mb-6">
      <div class="date text-mono f5 my-3">April 21, 2020</div>
      <h1 class="my-2 h00-mktg lh-condensed">GHSL-2020-010: Out-Of-Bounds write in Android Open Source Project - CVE-2020-0070</h1>

      
      
      
      
      

      

      <a target="_blank" class="sc-frDJqD SgxRc d-inline-flex flex-row flex-items-center text-gray" href="https://github.com/m-y-mo">
        <img class="mr-3" src="https://avatars.githubusercontent.com/u/15773368?s=35" height="35" width="35">
        <span>Man Yue Mo</span>
      </a>
    </header>

    <main id="content" class="markdown-body" aria-label="Content">
      <h2 id="summary">Summary</h2>

<p>An Out-of-Bounds write in Android’s <code class="language-plaintext highlighter-rouge">rw_t2t_update_lock_attributes</code> (NFC) could leads to remote code execution.</p>

<h2 id="product">Product</h2>
<p>Android Open Source Project</p>

<h2 id="cve">CVE</h2>
<p>CVE-2020-0070</p>

<h2 id="tested-version">Tested Version</h2>
<p>Pixel3a with build id: QQ1A.191205.011 (tag android-10.0.0_r16). (latest publicly available build as of the time of writing) Proxmark3 used is the RDV4.01</p>

<h2 id="details">Details</h2>

<p>In the <code class="language-plaintext highlighter-rouge">rw_t2t_update_lock_attributes</code> function, <code class="language-plaintext highlighter-rouge">p_t2t-&gt;lock_attr</code> is written with the index <code class="language-plaintext highlighter-rouge">block_count</code>. This index is incremented in a while loop every time <code class="language-plaintext highlighter-rouge">bits_covered</code> reaches <code class="language-plaintext highlighter-rouge">TAGS_BITS_PER_BYTE</code>(8)<sup id="fnref:2" role="doc-noteref"><a href="#fn:2" class="footnote" rel="footnote">1</a></sup>.</p>

<div class="language-plaintext highlighter-rouge"><div class="highlight"><pre class="highlight"><code>    if (bits_covered == TAG_BITS_PER_BYTE) {
      /* Move to next 8 bytes */
      bits_covered = 0;
      block_count++;
</code></pre></div></div>

<p>Now <code class="language-plaintext highlighter-rouge">bits_covered</code> is reset and incremented inside the while loop with condition <code class="language-plaintext highlighter-rouge">bytes_covered &lt; bytes_locked_per_lock_bit</code>, where <code class="language-plaintext highlighter-rouge">bytes_covered</code> is also incremented at the same time.</p>

<div class="language-plaintext highlighter-rouge"><div class="highlight"><pre class="highlight"><code>    while (bytes_covered &lt; bytes_locked_per_lock_bit) {
      if (p_t2t-&gt;lockbyte[num_dyn_lock_bytes].lock_byte &amp;
          rw_t2t_mask_bits[xx]) {
        /* If the bit is set then it is locked */
        p_t2t-&gt;lock_attr[block_count] |= 0x01 &lt;&lt; bits_covered;
      }
      bytes_covered++;
      bits_covered++;
</code></pre></div></div>

<p>This means <code class="language-plaintext highlighter-rouge">block_count</code> can be incremented to a maximum of (bytes_locked_per_lock_bit - 1)/8. This while loop is also enclosed in another while loop which repeats while <code class="language-plaintext highlighter-rouge">xx &lt; num_lock_bits</code><sup id="fnref:3" role="doc-noteref"><a href="#fn:3" class="footnote" rel="footnote">2</a></sup>, which can execute a maximum of 8 times<sup id="fnref:4" role="doc-noteref"><a href="#fn:4" class="footnote" rel="footnote">3</a></sup>.</p>

<div class="language-plaintext highlighter-rouge"><div class="highlight"><pre class="highlight"><code>  num_lock_bits =
      b_all_bits_are_locks
          ? TAG_BITS_PER_BYTE  //&lt;------ maximum |num_lock_bits| is 8.
          : p_t2t-&gt;lock_tlv[p_t2t-&gt;lockbyte[num_dyn_lock_bytes].tlv_index]
                    .num_bits %
                TAG_BITS_PER_BYTE;
  while (xx &lt; num_lock_bits) {
    bytes_covered = 0;
    while (bytes_covered &lt; bytes_locked_per_lock_bit) {
</code></pre></div></div>

<p>As <code class="language-plaintext highlighter-rouge">bytes_locked_per_lock_bit</code> is set here <sup id="fnref:5" role="doc-noteref"><a href="#fn:5" class="footnote" rel="footnote">4</a></sup> to <code class="language-plaintext highlighter-rouge">p_t2t-&gt;lock_tlv[p_t2t-&gt;lockbyte[num_dyn_lock_bytes].tlv_index].bytes_locked_per_bit</code></p>

<div class="language-plaintext highlighter-rouge"><div class="highlight"><pre class="highlight"><code> bytes_locked_per_lock_bit =
          p_t2t-&gt;lock_tlv[p_t2t-&gt;lockbyte[num_dyn_lock_bytes].tlv_index]
              .bytes_locked_per_bit;
</code></pre></div></div>

<p>and <code class="language-plaintext highlighter-rouge">p_t2t-&gt;lock_tlv[p_t2t-&gt;lockbyte[num_dyn_lock_bytes].tlv_index].bytes_locked_per_bit</code> takes its value from <code class="language-plaintext highlighter-rouge">p_t2t-&gt;tlv_value[2]</code> <sup id="fnref:6" role="doc-noteref"><a href="#fn:6" class="footnote" rel="footnote">5</a></sup>, which comes from data supplied by the tag <sup id="fnref:7" role="doc-noteref"><a href="#fn:7" class="footnote" rel="footnote">6</a></sup></p>

<div class="language-plaintext highlighter-rouge"><div class="highlight"><pre class="highlight"><code>            p_t2t-&gt;tlv_value[2 - p_t2t-&gt;bytes_count] = p_data[offset]; //&lt;-- data supplied by the tag
  if (p_t2t-&gt;bytes_count == 0) {
    ....
    p_t2t-&gt;lock_tlv[p_t2t-&gt;num_lock_tlvs].bytes_locked_per_bit =
        (uint8_t)tags_pow(2, ((p_t2t-&gt;tlv_value[2] &amp; 0xF0) &gt;&gt; 4));
</code></pre></div></div>

<p>by supplying a large enough <code class="language-plaintext highlighter-rouge">tlv_value[2]</code>, a malicious tag can cause OOB write during the detection stage.</p>

<h3 id="impact">Impact</h3>

<p>If succesfuly exploited, an attacker within NFC range could obtain remote code execution on android device’s NFC daemon.</p>

<h2 id="coordinated-disclosure-timeline">Coordinated Disclosure Timeline</h2>
<ul>
  <li>22/01/2020 Reported as <a href="https://issuetracker.google.com/issues/148063806">issue 148063806</a>, Android ID 148159613.</li>
  <li>06/04/2020 Fix published in <a href="https://source.android.com/security/bulletin/2020-04-01">2020-04-01 Andriod Security patch</a></li>
</ul>

<h2 id="credit">Credit</h2>

<p>This issue was discovered and reported by GHSL team member <a href="https://github.com/m-y-mo">@m-y-mo (Man Yue Mo)</a>.</p>

<h2 id="contact">Contact</h2>

<p>You can contact the GHSL team at <code class="language-plaintext highlighter-rouge">securitylab@github.com</code>, please include the <code class="language-plaintext highlighter-rouge">GHSL-2020-010</code> in any communication regarding this issue.</p>

<div class="footnotes" role="doc-endnotes">
  <ol>
    <li id="fn:2" role="doc-endnote">
      <p>https://android.googlesource.com/platform/system/nfc/+/6eb02b94a0b367a230ed8e41b0ac86652cbe76c8/src/nfc/tags/rw_t2t_ndef.cc#2260 <a href="#fnref:2" class="reversefootnote" role="doc-backlink">&#8617;</a></p>
    </li>
    <li id="fn:3" role="doc-endnote">
      <p>https://android.googlesource.com/platform/system/nfc/+/6eb02b94a0b367a230ed8e41b0ac86652cbe76c8/src/nfc/tags/rw_t2t_ndef.cc#2247 <a href="#fnref:3" class="reversefootnote" role="doc-backlink">&#8617;</a></p>
    </li>
    <li id="fn:4" role="doc-endnote">
      <p>https://android.googlesource.com/platform/system/nfc/+/6eb02b94a0b367a230ed8e41b0ac86652cbe76c8/src/nfc/tags/rw_t2t_ndef.cc#2240 <a href="#fnref:4" class="reversefootnote" role="doc-backlink">&#8617;</a></p>
    </li>
    <li id="fn:5" role="doc-endnote">
      <p>https://android.googlesource.com/platform/system/nfc/+/6eb02b94a0b367a230ed8e41b0ac86652cbe76c8/src/nfc/tags/rw_t2t_ndef.cc#2231 <a href="#fnref:5" class="reversefootnote" role="doc-backlink">&#8617;</a></p>
    </li>
    <li id="fn:6" role="doc-endnote">
      <p>https://android.googlesource.com/platform/system/nfc/+/6eb02b94a0b367a230ed8e41b0ac86652cbe76c8/src/nfc/tags/rw_t2t_ndef.cc#615 <a href="#fnref:6" class="reversefootnote" role="doc-backlink">&#8617;</a></p>
    </li>
    <li id="fn:7" role="doc-endnote">
      <p>https://android.googlesource.com/platform/system/nfc/+/6eb02b94a0b367a230ed8e41b0ac86652cbe76c8/src/nfc/tags/rw_t2t_ndef.cc#605 <a href="#fnref:7" class="reversefootnote" role="doc-backlink">&#8617;</a></p>
    </li>
  </