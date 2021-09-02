<header class="post-header d-block mb-6">
      <div class="date text-mono f5 my-3">December 11, 2020</div>
      <h1 class="my-2 h00-mktg lh-condensed">GHSL-2020-168, GHSL-2020-169, GHSL-2020-170: Integer overflows and file descriptor leak in aptd - CVE-2020-27349, CVE-2020-27350, CVE-2020-27351</h1>

      
      
      
      
      

      

      <a target="_blank" class="sc-frDJqD SgxRc d-inline-flex flex-row flex-items-center text-gray" href="https://github.com/kevinbackhouse">
        <img class="mr-3" src="https://avatars.githubusercontent.com/u/4358136?s=35" height="35" width="35">
        <span>Kevin Backhouse</span>
      </a>
    </header>

    <main id="content" class="markdown-body" aria-label="Content">
      <h2 id="summary">Summary</h2>

<p>The aptd daemon is a system service for installing and updating packages. It is accessible via <a href="https://www.freedesktop.org/wiki/Software/dbus/">dbus</a> and has a method named “InstallFile” which is used for installing local <code class="language-plaintext highlighter-rouge">.deb</code> packages. Although polkit is used to prevent an unprivileged user from using “InstallFile” to install a malicious <code class="language-plaintext highlighter-rouge">.deb</code> package, it does not prevent aptd from parsing the contents of the <code class="language-plaintext highlighter-rouge">.deb</code> file. The parsing logic is provided by two packages, <a href="https://packages.ubuntu.com/focal/libapt-pkg-dev">libapt-pkg-dev</a> and <a href="https://packages.ubuntu.com/source/focal/python-apt">python-apt</a>, and is implemented in C. These two packages contain several bugs, which an unprivileged user can exploit to trigger a local denial of service attack.</p>

<h2 id="product">Product</h2>

<p>aptd</p>

<h2 id="tested-version">Tested Version</h2>

<ul>
  <li>libapt-pkg-dev: version 2.0.2ubuntu0.1</li>
  <li>python-apt: 2.0.0ubuntu0.20.04.1</li>
  <li>Tested on Ubuntu 20.04.1 LTS</li>
</ul>

<h2 id="details">Details</h2>

<h3 id="issue-1-aptd-crash-due-to-integer-overflow-in-arfilecc-ghsl-2020-168">Issue 1: aptd crash due to integer overflow in arfile.cc (GHSL-2020-168)</h3>

<p>A crafted <code class="language-plaintext highlighter-rouge">.deb</code> package can trigger a negative integer overflow at <a href="https://git.launchpad.net/ubuntu/+source/apt/tree/apt-pkg/contrib/arfile.cc?h=applied/ubuntu/focal-updates&amp;id=4c264e60b524855b211751e1632ba48526f6b44d#n116">arfile.cc, line 116</a>:</p>

<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="n">Memb</span><span class="o">-&gt;</span><span class="n">Size</span> <span class="o">-=</span> <span class="n">Len</span><span class="p">;</span>
</code></pre></div></div>

<p>Due to the integer overflow, the value of <code class="language-plaintext highlighter-rouge">Memb-&gt;Size</code> is <code class="language-plaintext highlighter-rouge">0xFFFFFFFFFFFFFFFF</code>. This leads to an out-of-memory error at <a href="https://git.launchpad.net/ubuntu/+source/python-apt/tree/python/arfile.cc?h=applied/ubuntu/focal-updates&amp;id=0f7cc93acdb51d943114f1cd79002288c4ca4d24#n602">arfile.cc, line 602</a>:</p>

<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="kt">char</span><span class="o">*</span> <span class="n">value</span> <span class="o">=</span> <span class="n">new</span> <span class="kt">char</span><span class="p">[</span><span class="n">member</span><span class="o">-&gt;</span><span class="n">Size</span><span class="p">];</span>
</code></pre></div></div>

<p>The out-of-memory error causes aptd to crash.</p>

<p>Please note that the source locations above refer to two separate files, both named <code class="language-plaintext highlighter-rouge">arfile.cc</code>. The first is from the libapt-pkg-dev package and the second is from the python-apt package.</p>

<p>To trigger the crash, you have first to generate a malicious <code class="language-plaintext highlighter-rouge">.deb</code> file, then use <code class="language-plaintext highlighter-rouge">dbus-send</code> to send the malicious <code class="language-plaintext highlighter-rouge">.deb</code> file to aptd:</p>

<div class="language-bash highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="nv">$ </span>dbus-send <span class="nt">--system</span> <span class="nt">--type</span><span class="o">=</span><span class="s2">"method_call"</span> <span class="nt">--print-reply</span> <span class="nt">--dest</span><span class="o">=</span>org.debian.apt /org/debian/apt org.debian.apt.InstallFile string:<span class="sb">`</span><span class="nb">realpath </span>test.deb<span class="sb">`</span> boolean:true
method <span class="k">return </span><span class="nb">time</span><span class="o">=</span>1602245339.731762 <span class="nv">sender</span><span class="o">=</span>:1.287 -&gt; <span class="nv">destination</span><span class="o">=</span>:1.288 <span class="nv">serial</span><span class="o">=</span>8 <span class="nv">reply_serial</span><span class="o">=</span>2
   string <span class="s2">"/org/debian/apt/transaction/90f29de930854568964af1918f6ca5eb"</span>
<span class="nv">$ </span>dbus-send <span class="nt">--system</span> <span class="nt">--type</span><span class="o">=</span><span class="s2">"method_call"</span> <span class="nt">--print-reply</span> <span class="nt">--dest</span><span class="o">=</span>org.debian.apt /org/debian/apt/transaction/90f29de930854568964af1918f6ca5eb org.debian.apt.transaction.Run
</code></pre></div></div>

<p>Note that you need to use the “transaction id” returned by the first <code class="language-plaintext highlighter-rouge">dbus-send</code> in the second <code class="language-plaintext highlighter-rouge">dbus-send</code> command.</p>

<h4 id="impact">Impact</h4>

<p>This issue may lead to local denial of service.</p>

<h3 id="issue-2-aptd-infinite-loop-due-to-integer-overflow-in-arfilecc-ghsl-2020-169">Issue 2: aptd infinite loop due to integer overflow in arfile.cc (GHSL-2020-169)</h3>

<p>This issue is very similar to issue 1, but is caused by a different bug. This bug occurs during the call to <code class="language-plaintext highlighter-rouge">StrToNum</code> at <a href="https://git.launchpad.net/ubuntu/+source/apt/tree/apt-pkg/contrib/arfile.cc?h=applied/ubuntu/focal-updates&amp;id=4c264e60b524855b211751e1632ba48526f6b44d#n92">arfile.cc, line 92</a>:</p>

<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="n">StrToNum</span><span class="p">(</span><span class="n">Head</span><span class="p">.</span><span class="n">Size</span><span class="p">,</span><span class="n">Memb</span><span class="o">-&gt;</span><span class="n">Size</span><span class="p">,</span><span class="k">sizeof</span><span class="p">(</span><span class="n">Head</span><span class="p">.</span><span class="n">Size</span><span class="p">))</span> <span class="o">==</span> <span class="nb">false</span><span class="p">)</span>
</code></pre></div></div>

<p>The bug is due to the use of <code class="language-plaintext highlighter-rouge">strtoul</code> in <a href="https://git.launchpad.net/ubuntu/+source/apt/tree/apt-pkg/contrib/strutl.cc?h=applied/ubuntu/focal-updates&amp;id=4c264e60b524855b211751e1632ba48526f6b44d#n1169">StrToNum</a>:</p>

<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="c1">// StrToNum - Convert a fixed length string to a number			/*{{{*/</span>
<span class="c1">// ---------------------------------------------------------------------</span>
<span class="cm">/* This is used in decoding the crazy fixed length string headers in
   tar and ar files. */</span>
<span class="n">bool</span> <span class="nf">StrToNum</span><span class="p">(</span><span class="k">const</span> <span class="kt">char</span> <span class="o">*</span><span class="n">Str</span><span class="p">,</span><span class="kt">unsigned</span> <span class="kt">long</span> <span class="o">&amp;</span><span class="n">Res</span><span class="p">,</span><span class="kt">unsigned</span> <span class="n">Len</span><span class="p">,</span><span class="kt">unsigned</span> <span class="n">Base</span><span class="p">)</span>
<span class="p">{</span>
   <span class="kt">char</span> <span class="n">S</span><span class="p">[</span><span class="mi">30</span><span class="p">];</span>
   <span class="k">if</span> <span class="p">(</span><span class="n">Len</span> <span class="o">&gt;=</span> <span class="k">sizeof</span><span class="p">(</span><span class="n">S</span><span class="p">))</span>
      <span class="k">return</span> <span class="nb">false</span><span class="p">;</span>
   <span class="n">memcpy</span><span class="p">(</span><span class="n">S</span><span class="p">,</span><span class="n">Str</span><span class="p">,</span><span class="n">Len</span><span class="p">);</span>
   <span class="n">S</span><span class="p">[</span><span class="n">Len</span><span class="p">]</span> <span class="o">=</span> <span class="mi">0</span><span class="p">;</span>

   <span class="c1">// All spaces is a zero</span>
   <span class="n">Res</span> <span class="o">=</span> <span class="mi">0</span><span class="p">;</span>
   <span class="kt">unsigned</span> <span class="n">I</span><span class="p">;</span>
   <span class="k">for</span> <span class="p">(</span><span class="n">I</span> <span class="o">=</span> <span class="mi">0</span><span class="p">;</span> <span class="n">S</span><span class="p">[</span><span class="n">I</span><span class="p">]</span> <span class="o">==</span> <span class="sc">' '</span><span class="p">;</span> <span class="n">I</span><span class="o">++</span><span class="p">);</span>
   <span class="k">if</span> <span class="p">(</span><span class="n">S</span><span class="p">[</span><span class="n">I</span><span class="p">]</span> <span class="o">==</span> <span class="mi">0</span><span class="p">)</span>
      <span class="k">return</span> <span class="nb">true</span><span class="p">;</span>

   <span class="kt">char</span> <span class="o">*</span><span class="n">End</span><span class="p">;</span>
   <span class="n">Res</span> <span class="o">=</span> <span class="n">strtoul</span><span class="p">(</span><span class="n">S</span><span class="p">,</span><span class="o">&amp;</span><span class="n">End</span><span class="p">,</span><span class="n">Base</span><span class="p">);</span>  <span class="o">&lt;======</span> <span class="n">negative</span> <span class="n">numbers</span> <span class="n">accepted</span>
   <span class="k">if</span> <span class="p">(</span><span class="n">End</span> <span class="o">==</span> <span class="n">S</span><span class="p">)</span>
      <span class="k">return</span> <span class="nb">false</span><span class="p">;</span>

   <span class="k">return</span> <span class="nb">true</span><span class="p">;</span>
<span class="p">}</span>
</code></pre></div></div>

<p>The bug is that <code class="language-plaintext highlighter-rouge">strtoul</code> allows the number to be negative. For example, it will accept the string “-60”. I have written a proof-of-concept exploit which uses this to put the parser into an infinite loop.</p>

<p>To run the proof-of-concept, first generate a malicious <code class="language-plaintext highlighter-rouge">.deb</code> file, then use <code class="language-plaintext highlighter-rouge">dbus-send</code> to send the malicious <code class="language-plaintext highlighter-rouge">.deb</code> file to aptd:</p>

<div class="language-bash highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="nv">$ </span>dbus-send <span class="nt">--system</span> <span class="nt">--type</span><span class="o">=</span><span class="s2">"method_call"</span> <span class="nt">--print-reply</span> <span class="nt">--dest</span><span class="o">=</span>org.debian.apt /org/debian/apt org.debian.apt.InstallFile string:<span class="sb">`</span><span class="nb">realpath </span>test.deb<span class="sb">`</span> boolean:true
method <span class="k">return </span><span class="nb">time</span><span class="o">=</span>1602245339.731762 <span class="nv">sender</span><span class="o">=</span>:1.287 -&gt; <span class="nv">destination</span><span class="o">=</span>:1.288 <span class="nv">serial</span><span class="o">=</span>8 <span class="nv">reply_serial</span><span class="o">=</span>2
   string <span class="s2">"/org/debian/apt/transaction/90f29de930854568964af1918f6ca5eb"</span>
<span class="nv">$ </span>dbus-send <span class="nt">--system</span> <span class="nt">--type</span><span class="o">=</span><span class="s2">"method_call"</span> <span class="nt">--print-reply</span> <span class="nt">--dest</span><span class="o">=</span>org.debian.apt /org/debian/apt/transaction/90f29de930854568964af1918f6ca5eb org.debian.apt.transaction.Run
</code></pre></div></div>

<p>Note that you need to use the “transaction id” returned by the first <code class="language-plaintext highlighter-rouge">dbus-send</code> in the second <code class="language-plaintext highlighter-rouge">dbus-send</code> command.</p>

<h4 id="impact-1">Impact</h4>

<p>This issue may lead to local denial of service.</p>

<h3 id="issue-3-aptd-file-descriptor-leak-ghsl-2020-170">Issue 3: aptd file descriptor leak (GHSL-2020-170)</h3>

<p>There is a file descriptor leak in <code class="language-plaintext highlighter-rouge">debfile_new</code> at <a href="https://git.launchpad.net/ubuntu/+source/python-apt/tree/python/arfile.cc?h=applied/ubuntu/focal-updates&amp;id=0f7cc93acdb51d943114f1cd79002288c4ca4d24#n588">arfile.cc, line 588</a>:</p>

<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="k">static</span> <span class="n">PyObject</span> <span class="o">*</span><span class="nf">debfile_new</span><span class="p">(</span><span class="n">PyTypeObject</span> <span class="o">*</span><span class="n">type</span><span class="p">,</span> <span class="n">PyObject</span> <span class="o">*</span><span class="n">args</span><span class="p">,</span> <span class="n">PyObject</span> <span class="o">*</span><span class="n">kwds</span><span class="p">)</span>
<span class="p">{</span>
    <span class="n">PyDebFileObject</span> <span class="o">*</span><span class="n">self</span> <span class="o">=</span> <span class="p">(</span><span class="n">PyDebFileObject</span><span class="o">*</span><span class="p">)</span><span class="n">ararchive_new</span><span class="p">(</span><span class="n">type</span><span class="p">,</span> <span class="n">args</span><span class="p">,</span> <span class="n">kwds</span><span class="p">);</span>
    <span class="k">if</span> <span class="p">(</span><span class="n">self</span> <span class="o">==</span> <span class="nb">NULL</span><span class="p">)</span>
        <span class="k">return</span> <span class="nb">NULL</span><span class="p">;</span>

    <span class="c1">// DebFile</span>
    <span class="n">self</span><span class="o">-&gt;</span><span class="n">control</span> <span class="o">=</span> <span class="n">debfile_get_tar</span><span class="p">(</span><span class="n">self</span><span class="p">,</span> <span class="s">"control.tar"</span><span class="p">);</span>
    <span class="k">if</span> <span class="p">(</span><span class="n">self</span><span class="o">-&gt;</span><span class="n">control</span> <span class="o">==</span> <span class="nb">NULL</span><span class="p">)</span>
        <span class="k">return</span> <span class="nb">NULL</span><span class="p">;</span>  <span class="o">&lt;=====</span> <span class="n">self</span> <span class="n">is</span> <span class="n">not</span> <span class="n">freed</span><span class="p">,</span> <span class="n">so</span> <span class="n">a</span> <span class="n">file</span> <span class="n">descriptor</span> <span class="n">is</span> <span class="n">leaked</span>
</code></pre></div></div>

<p>If the <code class="language-plaintext highlighter-rouge">.deb</code> file is invalid, then <code class="language-plaintext highlighter-rouge">debfile_new()</code> returns <code class="language-plaintext highlighter-rouge">NULL</code>, forgetting to free <code class="language-plaintext highlighter-rouge">self</code>. This means that the file descriptor for the <code class="language-plaintext highlighter-rouge">.deb</code> file is not closed. An attacker could use this to exhaust the system’s file descriptors, causing a local denial of service.</p>

<p>To run the proof-of-concept, first generate the malicious <code class="language-plaintext highlighter-rouge">.deb</code> file, then use <code class="language-plaintext highlighter-rouge">dbus-send</code> to send the malicious <code class="language-plaintext highlighter-rouge">.deb</code> file to aptd:</p>

<div class="language-bash highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="nv">$ </span>dbus-send <span class="nt">--system</span> <span class="nt">--type</span><span class="o">=</span><span class="s2">"method_call"</span> <span class="nt">--print-reply</span> <span class="nt">--dest</span><span class="o">=</span>org.debian.apt /org/debian/apt org.debian.apt.InstallFile string:<span class="sb">`</span><span class="nb">realpath </span>test.deb<span class="sb">`</span> boolean:true
method <span class="k">return </span><span class="nb">time</span><span class="o">=</span>1602245339.731762 <span class="nv">sender</span><span class="o">=</span>:1.287 -&gt; <span class="nv">destination</span><span class="o">=</span>:1.288 <span class="nv">serial</span><span class="o">=</span>8 <span class="nv">reply_serial</span><span class="o">=</span>2
   string <span class="s2">"/org/debian/apt/transaction/90f29de930854568964af1918f6ca5eb"</span>
<span class="nv">$ </span>dbus-send <span class="nt">--system</span> <span class="nt">--type</span><span class="o">=</span><span class="s2">"method_call"</span> <span class="nt">--print-reply</span> <span class="nt">--dest</span><span class="o">=</span>org.debian.apt /org/debian/apt/transaction/90f29de930854568964af1918f6ca5eb org.debian.apt.transaction.Run
</code></pre></div></div>

<p>Note that you need to use the “transaction id” returned by the first <code class="language-plaintext highlighter-rouge">dbus-send</code> in the second <code class="language-plaintext highlighter-rouge">dbus-send</code> command. Every time you run the PoC, aptd will open another file descriptor to the <code class="language-plaintext highlighter-rouge">.deb</code> file, which you can observe by running <code class="language-plaintext highlighter-rouge">lsof -p &lt;pid of aptd&gt;</code>.</p>

<h4 id="impact-2">Impact</h4>

<p>This issue may lead to local denial of service by exhausting the supply of file descriptors.</p>

<h2 id="cve">CVE</h2>
<ul>
  <li>CVE-2020-27349</li>
  <li>CVE-2020-27350</li>
  <li>CVE-2020-27351</li>
</ul>

<h2 id="coordinated-disclosure-timeline">Coordinated Disclosure Timeline</h2>
<ul>
  <li>2020-10-09: Created bug report: https://bugs.launchpad.net/ubuntu/+source/apt/+bug/1899193</li>
  <li>2020-10-10: Reply from Seth Arnold.</li>
  <li>2020-10-10: Reply from Julian Andres Klode.</li>
  <li>2020-10-19: Patch for first 2 issues (out of 3) posted by Julian Andres Klode.</li>
  <li>2020-11-20: CVEs <a href="https://bugs.launchpad.net/ubuntu/+source/apt/+bug/1899193/comments/16">assigned</a>: CVE– 2020-27349, CVE-2020-27350, CVE-2020-27351.</li>
  <li>2020-12-01: Patch which adds an extra policykit check in aptdaemon, posted by Julian Andres Klode.</li>
  <li>2020-12-09: Fixes released.</li>
</ul>

<h2 id="resources">Resources</h2>
<p>https://ubuntu.com/security/notices/USN-4668-1
https://ubuntu.com/security/notices/USN-4667-1
https://ubuntu.com/security/notices/USN-4664-1</p>

<h2 id="credit">Credit</h2>

<p>These issues were discovered and reported by GHSL team member <a href="https://github.com/kevinbackhouse">@kevinbackhouse (Kevin Backhouse)</a>.</p>

<h2 id="contact">Contact</h2>

<p>You can contact the GHSL team at <code class="language-plaintext highlighter-rouge">securitylab@github.com</code>, please include a reference to <code class="language-plaintext highlighter-rouge">GHSL-2020-168</code>, <code class="language-plaintext highlighter-rouge">GHSL-2020-169</code>, or <code class="language-plaintext highlighter-rouge">GHSL-2020-170</code> in any communication regar