<header class="post-header d-block mb-6">
      <div class="date text-mono f5 my-3">April 7, 2020</div>
      <h1 class="my-2 h00-mktg lh-condensed">GHSL-2020-009: UAF leads to RCE in ProFTPD</h1>

      
      
      
      
      

      

      <a target="_blank" class="sc-frDJqD SgxRc d-inline-flex flex-row flex-items-center text-gray" href="https://github.com/antonio-morales">
        <img class="mr-3" src="https://avatars.githubusercontent.com/u/55253029?s=35" height="35" width="35">
        <span>Antonio Morales</span>
      </a>
    </header>

    <main id="content" class="markdown-body" aria-label="Content">
      <h2 id="summary">Summary</h2>

<p>A use-after-free vulnerability exists in ProFTPD. Successful exploitation of this vulnerability could allow a remote attacker to execute arbitrary code on the affected system.</p>

<h2 id="product">Product</h2>
<p>ProFTPD</p>

<h2 id="tested-version">Tested Version</h2>
<p>Development version - master branch (Jan 22, 2020)</p>

<h2 id="details">Details</h2>

<h3 id="use-after-free-vulnerability-in-memory-pool-allocator-cve-2020-9273">Use-after-free vulnerability in memory pool allocator (CVE-2020-9273)</h3>

<p>It is possible to corrupt the ProFTPd memory pool by interrupting current data transfer (PoC Exploit Demo Video.webm). This can be done for example, by sending an interrupt order to the command channel while a transfer is active in the data channel.</p>

<p>In our PoC, the program crashes on the <code class="language-plaintext highlighter-rouge">alloc_pool</code> function (<code class="language-plaintext highlighter-rouge">pool.c</code>) when executing <code class="language-plaintext highlighter-rouge">first_avail = blok-&gt;h.first_avail</code>.</p>

<p>As you can see, the right side operand of the assignment in <code class="language-plaintext highlighter-rouge">pool.c:569</code> is <code class="language-plaintext highlighter-rouge">p-&gt;last</code> (See <a href="/assets/advisories-resources/GHSL-2020-009-Image1.png">Image 1</a>). However, the problem is that <code class="language-plaintext highlighter-rouge">p</code> is a corrupted pool (<a href="/assets/advisories-resources/GHSL-2020-009-Image2.png">See Image 2</a>).</p>

<p>The source of the problem comes from the <code class="language-plaintext highlighter-rouge">pcalloc</code> call in <code class="language-plaintext highlighter-rouge">netio.c:1066</code> (<a href="/assets/advisories-resources/GHSL-2020-009-Image3.png">See Image 3</a>). This function calls the <code class="language-plaintext highlighter-rouge">alloc_pool</code> function again which in turn calls <code class="language-plaintext highlighter-rouge">new_block</code> to obtain a new freed memory block (<a href="/assets/advisories-resources/GHSL-2020-009-Image4.png">See Image 4</a>). But the memory block returned by <code class="language-plaintext highlighter-rouge">new_block</code> is still referenced by the <code class="language-plaintext highlighter-rouge">p</code> pool.</p>

<p>The problem is that <code class="language-plaintext highlighter-rouge">new_block</code> function is not concurrently-secure, and under certain circumstances, the <code class="language-plaintext highlighter-rouge">new_block</code> function can return as a free block a block already present in the pool, causing the corruption of the pool list.</p>

<p>So, in short, <code class="language-plaintext highlighter-rouge">p</code> is a dangling pointer due to an use-after-free vulnerability.</p>

<p>It’s important to note that our tests show that this vulnerability can also lead to other primitives such as OOB writes, which increases the severity of the vulnerability.</p>

<h4 id="proftpd-asan-build-instructions">ProFTPD ASAN build instructions</h4>
<div class="language-plaintext highlighter-rouge"><div class="highlight"><pre class="highlight"><code>CC="clang" CXX="clang++" CFLAGS="-fsanitize=address,undefined -g" CXXFLAGS="-fsanitize=address,undefined -g" LDFLAGS="-fsanitize=address,undefined" ./configure
</code></pre></div></div>
<div class="language-plaintext highlighter-rouge"><div class="highlight"><pre class="highlight"><code>LDFLAGS="-fsanitize=address,undefined" make -j4
</code></pre></div></div>

<h4 id="steps-to-reproduce">Steps to reproduce:</h4>
<ol>
  <li>Create a new user <code class="language-plaintext highlighter-rouge">fuzzing</code> with password <code class="language-plaintext highlighter-rouge">fuzzing</code> and extract <code class="language-plaintext highlighter-rouge">Compressed_Dir.tar.gz</code> dir in their home folder.</li>
  <li>Compile ProFTPD using ASAN as mentioned above.</li>
  <li>Run ProFTPD as root with the basic configuration and and following options: <code class="language-plaintext highlighter-rouge">ASAN_OPTIONS=verbosity=3,detect_leaks=0,abort_on_error=1,debug=true,check_initialization_order=true,detect_stack_use_after_return=true,strict_string_checks=true,detect_invalid_pointer_pairs=2 ./proftpd -n -c basic.conf -d 10 -X</code></li>
  <li>Run a netcat listener on port 1055 (PORT 127,0,0,1,4,31 in our PoC).</li>
  <li>Send the PoC trigger to the running ProFTPD server using telnet (assuming that it is running on port 21/TCP): <code class="language-plaintext highlighter-rouge">telnet 127.0.0.1 21 &lt; test.txt</code></li>
  <li>ProFTPD should crash showing the relevant ASAN trace</li>
</ol>

<h2 id="impact">Impact</h2>

<p>This issue may lead to Post-Auth RCE.</p>

<h2 id="remediation">Remediation</h2>
<p>The issue has been fixed here <a href="https://github.com/proftpd/proftpd/commit/929d6c5a107ad92705555a87c386abd8bdce5d0d">https://github.com/proftpd/proftpd/commit/929d6c5a107ad92705555a87c386abd8bdce5d0d</a></p>

<h2 id="coordinated-disclosure-timeline">Coordinated Disclosure Timeline</h2>
<p>This report is subject to our <a href="https://securitylab.github.com/advisories/#policy">coordinated disclosure policy</a>.</p>
<ul>
  <li>01/22/2020: Report sent to Vendor</li>
  <li>01/25/2020: Vendor acknowledged report</li>
  <li>02/16/2020: Vendor proposed fixes</li>
  <li>02/17/2020: Fixes reviewed and verified</li>
  <li>02/18/2020: Report published to public</li>
</ul>

<h2 id="supporting-resources">Supporting Resources</h2>
<ul>
  <li><a href="/assets/advisories-resources/GHSL-2020-009-Image1.png">Image 1</a></li>
  <li><a href="/assets/advisories-resources/GHSL-2020-009-Image2.png">Image 2</a></li>
  <li><a href="/assets/advisories-resources/GHSL-2020-009-Image3.png">Image 3</a></li>
  <li><a href="/assets/advisories-resources/GHSL-2020-009-Image4.png">Image 4</a></li>
  <li><a href="/assets/advisories-resources/GHSL-2020-009-ASAN.txt">ASAN report</a></li>
</ul>

<h2 id="credit">Credit</h2>

<p>This issue was discovered and reported by GHSL team member <a href="https://github.com/antonio-morales">@antonio-morales (Antonio Morales)</a>.</p>

<h2 id="contact">Contact</h2>

<p>You can contact the GHSL team at <code class="language-plaintext highlighter-rouge">securitylab@github.com</code>, please include the <code class="language-plaintext highlighter-rouge">GHSL-2020-009</code> in any communication regarding this issue.</p>

  