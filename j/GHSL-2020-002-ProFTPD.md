<header class="post-header d-block mb-6">
      <div class="date text-mono f5 my-3">March 12, 2020</div>
      <h1 class="my-2 h00-mktg lh-condensed">GHSL-2020-002: out-of-bounds (OOB) read in ProFTPD</h1>

      
      
      
      
      

      

      <a target="_blank" class="sc-frDJqD SgxRc d-inline-flex flex-row flex-items-center text-gray" href="https://github.com/antonio-morales">
        <img class="mr-3" src="https://avatars.githubusercontent.com/u/55253029?s=35" height="35" width="35">
        <span>Antonio Morales</span>
      </a>
    </header>

    <main id="content" class="markdown-body" aria-label="Content">
      <h2 id="summary">Summary</h2>

<p>An out-of-bounds (OOB) read vulnerability has been detected in <code class="language-plaintext highlighter-rouge">mod_cap</code>.</p>

<h2 id="product">Product</h2>
<p>ProFTPD</p>

<h2 id="tested-version">Tested Version</h2>
<p>Development version - master branch (Jan 10, 2020)</p>

<h2 id="details">Details</h2>

<h3 id="out-of-bound-read-in-getstateflags-function">Out-of-bound read in <code class="language-plaintext highlighter-rouge">getstateflags</code> function</h3>

<p>The <code class="language-plaintext highlighter-rouge">cap_to_text()</code> function on <code class="language-plaintext highlighter-rouge">cap_text.c</code> performs a call to <code class="language-plaintext highlighter-rouge">getstateflags(caps, n)</code> [line 255].</p>

<p>When <code class="language-plaintext highlighter-rouge">getstateflags(cap_t caps, int capno)</code> is called, <code class="language-plaintext highlighter-rouge">capno</code> is equal to <code class="language-plaintext highlighter-rouge">37</code> so <code class="language-plaintext highlighter-rouge">isset_cap((__cap_s *)(&amp;caps-&gt;set.inheritable),capno)</code> will expand to <code class="language-plaintext highlighter-rouge">&amp;((__cap_s *)(&amp;caps-&gt;set.inheritable))-&gt;_blk[(37)&gt;&gt;5]</code>, thus accessing <code class="language-plaintext highlighter-rouge">caps-&gt;set.inheritable[1]</code> which is outside of <code class="language-plaintext highlighter-rouge">caps</code> struct bounds (<code class="language-plaintext highlighter-rouge">0x603000001ae4</code> to <code class="language-plaintext highlighter-rouge">0x603000001af7</code> in our example). <a href="/assets/advisories-resources/GHSL-2020-002-Image1.png">Image 1: Debug information</a></p>

<p>As a result, OOB reads occur which result in access to memory outside of the boundaries of the <code class="language-plaintext highlighter-rouge">caps</code> <code class="language-plaintext highlighter-rouge">cap_t</code> struct instance.</p>

<p>Due to the relative offsets of the <code class="language-plaintext highlighter-rouge">permitted</code> and <code class="language-plaintext highlighter-rouge">inheritable</code> members in the <code class="language-plaintext highlighter-rouge">caps</code> struct, this bug does not affect <code class="language-plaintext highlighter-rouge">set.effective</code> or <code class="language-plaintext highlighter-rouge">set.permitted</code>.  <a href="/assets/advisories-resources/GHSL-2020-002-Image2.png">Image 2: Caps struct members</a></p>

<h4 id="proftpd-asan-build-instructions">ProFTPD ASAN build instructions</h4>
<div class="language-plaintext highlighter-rouge"><div class="highlight"><pre class="highlight"><code>CC="clang" CXX="clang++" CFLAGS="-fsanitize=address,undefined -g" CXXFLAGS="-fsanitize=address,undefined -g" LDFLAGS="-fsanitize=address,undefined" ./configure
</code></pre></div></div>
<div class="language-plaintext highlighter-rouge"><div class="highlight"><pre class="highlight"><code>LDFLAGS="-fsanitize=address,undefined" make -j4
</code></pre></div></div>

<h4 id="steps-to-reproduce">Steps to reproduce:</h4>
<ol>
  <li>Prepare a ProFTPD ASAN build.</li>
  <li>Run ProFTPD as root with the basic configuration and the following options: <code class="language-plaintext highlighter-rouge"># ./proftpd -n -c /home/antonio/Downloads/GCOV-proftpd/sample-configurations/basic.conf -d 10 -X</code></li>
  <li>Log in to the server with a valid user (<code class="language-plaintext highlighter-rouge">USER XXXX\r\nPASS XXXX\r\n</code>)</li>
  <li>FTP server should crash with an associated ASAN trace.</li>
</ol>

<h4 id="impact">Impact</h4>

<p>This issue may lead to Post-Auth OOB-Read</p>

<h2 id="remediation">Remediation</h2>

<p>The vulnerability was fixed by updating the libcap bundled, and to rely on the system libpcap.
More information on this <a href="https://github.com/proftpd/proftpd/issues/902">issue</a></p>

<h2 id="coordinated-disclosure-timeline">Coordinated Disclosure Timeline</h2>
<p>This report was subject to our <a href="https://securitylab.github.com/advisories/#policy">coordinated disclosure policy</a>.</p>
<ul>
  <li>01/10/2020: Report sent to Vendor</li>
  <li>01/21/2020: Vendor acknowledged report</li>
  <li>02/03/2020: Vendor proposed fixes</li>
  <li>02/04/2020: Fixes reviewed and verified</li>
  <li>02/18/2020: Vendor published fix</li>
</ul>

<h2 id="supporting-resources">Supporting Resources</h2>
<ul>
  <li><a href="/assets/advisories-resources/GHSL-2020-002-ASAN.txt">ASAN report</a></li>
  <li><a href="/assets/advisories-resources/GHSL-2020-002-Image1.png">Image 1: Debug information</a></li>
  <li><a href="/assets/advisories-resources/GHSL-2020-002-Image2.png">Image 2: Caps struct members</a></li>
</ul>

<h2 id="credit">Credit</h2>

<p>This issue was discovered and reported by GHSL team member <a href="https://github.com/antonio-morales">@antonio-morales (Antonio Morales)</a>.</p>

<h2 id="contact">Contact</h2>

<p>You can contact the GHSL team at <code class="language-plaintext highlighter-rouge">securitylab@github.com</code>, please include the <code class="language-plaintext highlighter-rouge">GHSL-YEAR-ID</code> in any communication regarding this issue.</p>

    