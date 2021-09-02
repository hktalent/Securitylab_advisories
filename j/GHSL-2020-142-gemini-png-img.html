<header class="post-header d-block mb-6">
      <div class="date text-mono f5 my-3">November 17, 2020</div>
      <h1 class="my-2 h00-mktg lh-condensed">GHSL-2020-142: Heap memory corruption in png-img - CVE-2020-28248</h1>

      
      
      
      
      

      

      <a target="_blank" class="sc-frDJqD SgxRc d-inline-flex flex-row flex-items-center text-gray" href="https://github.com/anticomputer">
        <img class="mr-3" src="https://avatars.githubusercontent.com/u/13686387?s=35" height="35" width="35">
        <span>Bas Alberts</span>
      </a>
    </header>

    <main id="content" class="markdown-body" aria-label="Content">
      <h2 id="summary">Summary</h2>

<p>The <a href="https://www.npmjs.com/package/png-img">png-img</a> package provides NAN bindings for libpng. These bindings are vulnerable to an integer overflow which results in an underallocation of heap memory and subsequent heap memory corruption.</p>

<p>Additionally, the png-img package currently ships with libpng version 1.6.14 which contains several known and potentially exploitable vulnerabilities. The <a href="http://www.libpng.org/pub/png/libpng.html">current public release version</a> of libpng is 1.6.37.</p>

<h2 id="product">Product</h2>

<p><a href="https://www.npmjs.com/package/png-img">png-img</a></p>

<h2 id="tested-version">Tested Version</h2>

<p>2.3.0</p>

<h2 id="details">Details</h2>

<h3 id="issue-1-integer-overflow-resulting-in-heap-overflow-in-pngimgccpngimginitstorage_">Issue 1: Integer overflow resulting in heap overflow in <code class="language-plaintext highlighter-rouge">PngImg.cc:PngImg::InitStorage_()</code></h3>

<p>When loading a PNG image for processing by libpng the png-img bindings employ the <code class="language-plaintext highlighter-rouge">PngImg::InitStorage</code> function to allocate the initial memory required for the user supplied PNG data.</p>

<pre><code class="language-C">void PngImg::InitStorage_() {
    rowPtrs_.resize(info_.height, nullptr);
[1]
    data_ = new png_byte[info_.height * info_.rowbytes];

[2]
    for(size_t i = 0; i &lt; info_.height; ++i) {
        rowPtrs_[i] = data_ + i * info_.rowbytes;
    }
}
</code></pre>

<p>At [1] we observe the allocation of a <code class="language-plaintext highlighter-rouge">png_byte</code> array of size <code class="language-plaintext highlighter-rouge">info_.height * info_.rowbytes</code>. Both the height and rowbytes structure members are of type <code class="language-plaintext highlighter-rouge">png_uint_32</code>, which implies the integer arithmetic expression here is explicitly an unsigned 32bit integer operation.</p>

<p><code class="language-plaintext highlighter-rouge">info_.height</code> may be directly supplied from a PNG file as a 32bit integer and <code class="language-plaintext highlighter-rouge">info_.rowbytes</code> is derived from the PNG data as well.</p>

<p>This multiplication may trigger an integer overwrap which results in an underallocation of the <code class="language-plaintext highlighter-rouge">data_</code> memory region.</p>

<p>For example, if we set <code class="language-plaintext highlighter-rouge">info_.height</code> to 0x01000001 with an <code class="language-plaintext highlighter-rouge">info_.rowbytes</code> value of 0x100, the resulting expression would be (0x01000001 * 0x100) &amp; 0xffffffff == 0x100, and as a result <code class="language-plaintext highlighter-rouge">_data</code> would underallocated as a 0x100 sized png_byte array.</p>

<p>As a consequence, at [2], the <code class="language-plaintext highlighter-rouge">rowPtrs_</code> array will be populated with row-data pointers that point outside of the bounds of the allocated memory region since the for loop conditional operates on the original <code class="language-plaintext highlighter-rouge">info_.height</code> value.</p>

<p>Subsequently, once the actual row data is read from the PNG file, any adjacent memory to the <code class="language-plaintext highlighter-rouge">data_</code> region may be overwritten with attacker controlled row-data up to <code class="language-plaintext highlighter-rouge">info_.height * info_.rowbytes</code> bytes, affording a great deal of process memory control to any would-be attacker.</p>

<p>Note that this overwrite may be halted early according to attacker wishes by simply not supplying sufficient amounts of row-data from the PNG itself, at which point libpng error routines would kick in. Any subsequent program logic handling the error paths would then operate on corrupted heap memory. This results in a highly controlled heap overflow in terms of both contents and size.</p>

<h4 id="impact">Impact</h4>

<p>This issue may lead to arbitrary code execution if png-img is used to operate on untrusted PNG files.</p>

<h3 id="issue-2-vulnerable-version-of-libpng-shipped-with-png-img">Issue 2: vulnerable version of libpng shipped with png-img</h3>

<p>The png-img package currently ships with libpng version 1.6.14 which contains several known and potentially exploitable vulnerabilities. The <a href="http://www.libpng.org/pub/png/libpng.html">current public release version</a> of libpng is 1.6.37.</p>

<p>It is recommended to update to the latest release version of libpng to prevent future abuse of known libpng vulnerabilities exposed via the png-img package.</p>

<h2 id="cve">CVE</h2>

<ul>
  <li>CVE-2020-28248</li>
</ul>

<h2 id="coordinated-disclosure-timeline">Coordinated Disclosure Timeline</h2>

<ul>
  <li>08/05/2020: Maintainer notified</li>
  <li>08/06/2020: Maintainer acknowledges report</li>
  <li>10/05/2020: Maintainer prepares PR that fixes integer overflow and upgrades libpng version</li>
  <li>11/03/2020: Maintainer releases version 3.1.0 to npm.</li>
</ul>

<h2 id="resources">Resources</h2>

<ul>
  <li>https://github.com/github/securitylab-vulnerabilities/blob/main/vendor_reports/resources/GHSL-2020-142/x.png</li>
</ul>

<h2 id="credit">Credit</h2>

<p>This issue was discovered and reported by GHSL team member <a href="https://github.com/anticomputer">@anticomputer (Bas Alberts)</a>.</p>

<h2 id="contact">Contact</h2>

<p>You can contact the GHSL team at <code class="language-plaintext highlighter-rouge">securitylab@github.com</code>, please include a reference to <code class="language-plaintext highlighter-rouge">GHSL-2020-142</code> in any communication regarding this issue.</p>

    