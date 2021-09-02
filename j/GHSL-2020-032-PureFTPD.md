>
    <header class="post-header d-block mb-6">
      <div class="date text-mono f5 my-3">March 12, 2020</div>
      <h1 class="my-2 h00-mktg lh-condensed">GHSL-2020-032: out-of-bounds (OOB) read vulnerability in PureFTPd</h1>

      
      
      
      
      

      

      <a target="_blank" class="sc-frDJqD SgxRc d-inline-flex flex-row flex-items-center text-gray" href="https://github.com/antonio-morales">
        <img class="mr-3" src="https://avatars.githubusercontent.com/u/55253029?s=35" height="35" width="35">
        <span>Antonio Morales</span>
      </a>
    </header>

    <main id="content" class="markdown-body" aria-label="Content">
      <h2 id="summary">Summary</h2>

<p>An out-of-bounds (OOB) read vulnerability has been detected in the <code class="language-plaintext highlighter-rouge">pure_strcmp</code> function.</p>

<h2 id="product">Product</h2>
<p>PureFTPd</p>

<h2 id="tested-version">Tested Version</h2>
<p>Development version - master branch (Feb 24, 2020)</p>

<h2 id="details">Details</h2>

<h3 id="oob-read-in-pure_strcmp-cve-2020-9365">OOB read in pure_strcmp (CVE-2020-9365)</h3>

<p>The <code class="language-plaintext highlighter-rouge">pure_strcmp</code> and <code class="language-plaintext highlighter-rouge">pure_memcmp</code> functions in <code class="language-plaintext highlighter-rouge">utils.c</code> are affected by out-of-bounds read vulnerabilities.</p>

<p>As seen in <a href="/assets/advisories-resources/GHSL-2020-032-Bug.png">this code</a>, if the length of <code class="language-plaintext highlighter-rouge">s1</code> is greater than <code class="language-plaintext highlighter-rouge">s2</code> then the <code class="language-plaintext highlighter-rouge">for</code> loop will do <code class="language-plaintext highlighter-rouge">len-1</code> iterations, where <code class="language-plaintext highlighter-rouge">len-1 &gt; strlen(s2)</code>.</p>

<p>As a result, OOB reads occur from memory that is outside of the boundaries of the <code class="language-plaintext highlighter-rouge">s2</code> array.</p>

<p>Note that <code class="language-plaintext highlighter-rouge">pure_strcmp</code> is called from:</p>
<ul>
  <li><code class="language-plaintext highlighter-rouge">pw_mysql_check</code></li>
  <li><code class="language-plaintext highlighter-rouge">pw_pgsql_check</code></li>
  <li><code class="language-plaintext highlighter-rouge">pw_unix_check</code> (when shadow password support is not enabled)</li>
</ul>

<h4 id="pureftpd-asan-build-instructions">PureFTPD ASAN build instructions</h4>
<div class="language-plaintext highlighter-rouge"><div class="highlight"><pre class="highlight"><code>CC="clang" CXX="clang++" CFLAGS="-fsanitize=address -g -O0" CXXFLAGS="-fsanitize=address -g -O0" LDFLAGS="-fsanitize=address" ./configure --without-privsep --with-diraliases
</code></pre></div></div>
<div class="language-plaintext highlighter-rouge"><div class="highlight"><pre class="highlight"><code>make -j4
</code></pre></div></div>

<h4 id="steps-to-reproduce">Steps to reproduce:</h4>
<ol>
  <li>Compile PureFTPD using ASAN as mentioned above. Note that you need to comment <code class="language-plaintext highlighter-rouge">setrlimit(RLIMIT_DATA)</code> in order to be able to use ASAN with PureFTPd (ASAN takes a lot of virtual memory) <a href="/assets/advisories-resources/GHSL-2020-025-RlimitAsan.png">See the code</a></li>
  <li>Create a new user <code class="language-plaintext highlighter-rouge">fuzzing</code> with password <code class="language-plaintext highlighter-rouge">fuzzing</code>.</li>
  <li>Run PureFTPd server as root, enabling one of the affected login modules. For example <code class="language-plaintext highlighter-rouge"># ./pure-ftpd -S pgsql:/home/antonio/Downloads/pureftdp/pureftpd-pgsql.conf -l unix</code></li>
  <li>Connect to the FTP server and log in with user <code class="language-plaintext highlighter-rouge">fuzzing</code> and password <code class="language-plaintext highlighter-rouge">fuzzing</code></li>
  <li>PureFTPD should crash showing the ASAN trace.</li>
</ol>

<h2 id="impact">Impact</h2>

<p>This issue may allow attackers to leak sensitive information from PureFTPd process memory or crash the PureFTPD process itself.</p>

<h2 id="remediation">Remediation</h2>

<p>One way this issue may be resolved is by explicitly ensuring that <code class="language-plaintext highlighter-rouge">s1</code> is not longer than <code class="language-plaintext highlighter-rouge">s2</code> via e.g.:</p>

<p><code class="language-plaintext highlighter-rouge">(strlen(s1) &lt; strlen(s2)) ? strlen(s1) : strlen(s2)</code></p>

<p>Patch can be found here <a href="https://github.com/jedisct1/pure-ftpd/commit/36c6d268cb190282a2c17106acfd31863121b58e">https://github.com/jedisct1/pure-ftpd/commit/36c6d268cb190282a2c17106acfd31863121b58e</a></p>

<h2 id="coordinated-disclosure-timeline">Coordinated Disclosure Timeline</h2>
<p>This report is subject to our <a href="https://securitylab.github.com/advisories/#policy">coordinated disclosure policy</a>.</p>
<ul>
  <li>02/24/2020: Report sent to Vendor</li>
  <li>02/24/2020: Vendor acknowledged report</li>
  <li>02/24/2020: Vendor published fix</li>
</ul>

<h2 id="supporting-resources">Supporting Resources</h2>
<ul>
  <li><a href="/assets/advisories-resources/GHSL-2020-032-Bug.png">Vulnerable code snippet</a></li>
  <li><a href="/assets/advisories-resources/GHSL-2020-032-ASAN.txt">ASAN report</a></li>
</ul>

<h2 id="credit">Credit</h2>

<p>This issue was discovered and reported by GHSL team member <a href="https://github.com/antonio-morales">@antonio-morales (Antonio Morales)</a>.</p>

<h2 id="contact">Contact</h2>

<p>You can contact the GHSL team at <code class="language-plaintext highlighter-rouge">securitylab@github.com</code>, please include the <code class="language-plaintext highlighter-rouge">GHSL-YEAR-ID</code> in any communication regarding this issue.</p>