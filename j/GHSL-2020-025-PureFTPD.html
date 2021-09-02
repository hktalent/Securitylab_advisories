<header class="post-header d-block mb-6">
      <div class="date text-mono f5 my-3">March 12, 2020</div>
      <h1 class="my-2 h00-mktg lh-condensed">GHSL-2020-025: OOB read and DoS in PureFTPd</h1>

      
      
      
      
      

      

      <a target="_blank" class="sc-frDJqD SgxRc d-inline-flex flex-row flex-items-center text-gray" href="https://github.com/antonio-morales">
        <img class="mr-3" src="https://avatars.githubusercontent.com/u/55253029?s=35" height="35" width="35">
        <span>Antonio Morales</span>
      </a>
    </header>

    <main id="content" class="markdown-body" aria-label="Content">
      <h2 id="summary">Summary</h2>

<p>An uninitialized pointer vulnerability has been detected in PureFTPd which results in out-of-bounds (OOB) reads. It could also allow an attacker to trigger a Denial of Service against PureFTPD.</p>

<h2 id="product">Product</h2>
<p>PureFTPd</p>

<h2 id="tested-version">Tested Version</h2>
<p>Development version - master branch (Feb 7, 2020)</p>

<h2 id="details">Details</h2>

<h3 id="uninitialized-pointer-vulnerability-in-diraliases-linked-list-cve-2020-9274">Uninitialized pointer vulnerability in diraliases linked-list (CVE-2020-9274)</h3>

<p>A vulnerability has been detected in the way PureFTPD processes its <code class="language-plaintext highlighter-rouge">diraliases</code> linked-list.</p>

<p>The source of the problem comes from the <code class="language-plaintext highlighter-rouge">init_aliases</code> function in <code class="language-plaintext highlighter-rouge">diraliases.c</code> <a href="/assets/advisories-resources/GHSL-2020-025-BuggyCode.png">See the code</a>. In this function, the <code class="language-plaintext highlighter-rouge">next</code> member of the last item in the linked list is not set to <code class="language-plaintext highlighter-rouge">NULL</code>.</p>

<p>As a result, when the <code class="language-plaintext highlighter-rouge">lookup_alias(const char *alias)</code> or <code class="language-plaintext highlighter-rouge">print_aliases(void)</code> functions are called, they fail to correctly detect the end of the linked-list and try to access a non-existent list member.</p>

<h4 id="pureftpd-asan-build-instructions">PureFTPd ASAN build instructions</h4>
<div class="language-plaintext highlighter-rouge"><div class="highlight"><pre class="highlight"><code>CC="clang" CXX="clang++" CFLAGS="-fsanitize=address -g -O0" CXXFLAGS="-fsanitize=address -g -O0" LDFLAGS="-fsanitize=address" ./configure --without-privsep --with-diraliases
</code></pre></div></div>
<div class="language-plaintext highlighter-rouge"><div class="highlight"><pre class="highlight"><code>make -j4
</code></pre></div></div>

<h4 id="steps-to-reproduce">Steps to reproduce:</h4>
<ol>
  <li>Compile PureFTPD using ASAN as mentioned above. Note that you need to comment <code class="language-plaintext highlighter-rouge">setrlimit(RLIMIT_DATA)</code> to be able to use ASAN with PureFTPd (ASAN takes a lot of virtual memory) <a href="/assets/advisories-resources/GHSL-2020-025-RlimitAsan.png">See the code</a></li>
  <li>Copy the provided alias configuration file into <code class="language-plaintext highlighter-rouge">/[CONFDIR]/pureftpd-dir-aliases</code> (usually <code class="language-plaintext highlighter-rouge">/etc/pureftpd-dir-aliases</code>)</li>
  <li>Run PureFTPD as root with the <code class="language-plaintext highlighter-rouge">-S</code> parameter</li>
  <li>Connect to the FTP server and log in with a valid user and password</li>
  <li>Send the <code class="language-plaintext highlighter-rouge">SITE alias</code> command</li>
  <li>PureFTPD should crash</li>
</ol>

<h3 id="impact">Impact</h3>

<p>This issue may lead to an OOB read and post-auth DoS.</p>

<h3 id="remediation">Remediation</h3>

<p>Add <code class="language-plaintext highlighter-rouge">tail-&gt;next = NULL</code> for the last item of the linked list. Patch information can be found here <a href="https://github.com/jedisct1/pure-ftpd/commit/8d0d42542e2cb7a56d645fbe4d0ef436e38bcefa">https://github.com/jedisct1/pure-ftpd/commit/8d0d42542e2cb7a56d645fbe4d0ef436e38bcefa</a></p>

<h2 id="coordinated-disclosure-timeline">Coordinated Disclosure Timeline</h2>
<p>This report is subject to our <a href="https://securitylab.github.com/advisories/#policy">coordinated disclosure policy</a>.</p>
<ul>
  <li>02/18/2020: Report sent to Vendor</li>
  <li>02/18/2020: Vendor acknowledged report</li>
  <li>02/18/2020: Vendor published fix</li>
</ul>

<h2 id="supporting-resources">Supporting Resources</h2>
<ul>
  <li><a href="/assets/advisories-resources/GHSL-2020-025-BuggyCode.png">Vulnerable code snippet</a></li>
  <li><a href="/assets/advisories-resources/GHSL-2020-025-RlimitAsan.png">Code changes to use ASAN with PureFTPd</a></li>
  <li><a href="/assets/advisories-resources/GHSL-2020-025-pureftpd-dir-aliases">Example alias file</a></li>
</ul>

<h2 id="credit">Credit</h2>

<p>This issue was discovered and reported by GHSL team member <a href="https://github.com/antonio-morales">@antonio-morales (Antonio Morales)</a>.</p>

<h2 id="contact">Contact</h2>

<p>You can contact the GHSL team at <code class="language-plaintext highlighter-rouge">securitylab@github.com</code>, please include the <code class="language-plaintext highlighter-rouge">GHSL-YEAR-ID</code> in any communication regarding this issue.</p>

    