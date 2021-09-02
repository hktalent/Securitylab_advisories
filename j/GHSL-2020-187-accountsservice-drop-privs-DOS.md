<header class="post-header d-block mb-6">
      <div class="date text-mono f5 my-3">November 9, 2020</div>
      <h1 class="my-2 h00-mktg lh-condensed">GHSL-2020-187: Denial of Service (DoS) in Ubuntu accountsservice - CVE-2020-16126 - CVE-2020-16127</h1>

      
      
      
      
      

      

      <a target="_blank" class="sc-frDJqD SgxRc d-inline-flex flex-row flex-items-center text-gray" href="https://github.com/kevinbackhouse">
        <img class="mr-3" src="https://avatars.githubusercontent.com/u/4358136?s=35" height="35" width="35">
        <span>Kevin Backhouse</span>
      </a>
    </header>

    <main id="content" class="markdown-body" aria-label="Content">
      <h2 id="summary">Summary</h2>

<p>The accountsservice daemon drops privileges to perform certain operations. For example while performing the <code class="language-plaintext highlighter-rouge">org.freedesktop.Accounts.User.SetLanguage</code> D-Bus method, which can be triggered by an unprivileged user, accounts-daemon temporarily drops privileges to the same UID as the user, to avoid being tricked into opening a file which the unprivileged user should not be able to access. Unfortunately, by changing its <a href="https://en.wikipedia.org/wiki/User_identifier#Real_user_ID">RUID</a> it has given the user permission to send it signals. This means that the unprivileged user can send accounts-daemon a <code class="language-plaintext highlighter-rouge">SIGSTOP</code> signal, which stops the process and causes a denial of service.</p>

<h2 id="product">Product</h2>

<p><a href="https://git.launchpad.net/ubuntu/+source/accountsservice/">accountsservice</a></p>

<h2 id="tested-version">Tested Version</h2>

<ul>
  <li>accountsservice, version 0.6.55-0ubuntu12~20.04.1</li>
  <li>Tested on Ubuntu 20.04.1 LTS</li>
</ul>

<p>Note: I believe these issues only exist in Ubuntu’s version of accountsservice. I couldn’t find the vulnerable functions in the git repos maintained by <a href="https://gitlab.freedesktop.org/accountsservice/accountsservice">freedesktop</a> or <a href="https://salsa.debian.org/freedesktop-team/accountsservice">debian</a>. I originally discovered the vulnerable code in the version of the code that I had obtained by running <code class="language-plaintext highlighter-rouge">apt-get source accountsservice</code>, but I struggled to figure out where it came from when I started searching the official repositories. I eventually tracked it down to this patch file: <a href="https://git.launchpad.net/ubuntu/+source/accountsservice/tree/debian/patches/0010-set-language.patch?h=ubuntu/focal-updates&amp;id=e0347185d4c5554b026c13ccca691577c239afd5">0010-set-language.patch</a>.</p>

<h2 id="details">Details</h2>

<h3 id="issue-1-accountsservice-drop-privileges-sigstop-denial-of-service-ghsl-2020-187-cve-2020-16126">Issue 1: accountsservice drop privileges <code class="language-plaintext highlighter-rouge">SIGSTOP</code> denial of service (<code class="language-plaintext highlighter-rouge">GHSL-2020-187</code>, <code class="language-plaintext highlighter-rouge">CVE-2020-16126</code>)</h3>

<p>A <a href="https://git.launchpad.net/ubuntu/+source/accountsservice/tree/debian/patches/0010-set-language.patch?h=ubuntu/focal-updates&amp;id=e0347185d4c5554b026c13ccca691577c239afd5">source code patch</a> that (as far as I know) only exists in Ubuntu’s version of accountsservice, adds a function named <a href="https://git.launchpad.net/ubuntu/+source/accountsservice/tree/debian/patches/0010-set-language.patch?h=ubuntu/focal-updates&amp;id=e0347185d4c5554b026c13ccca691577c239afd5#n66"><code class="language-plaintext highlighter-rouge">user_drop_privileges_to_user</code></a>:</p>

<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="k">static</span> <span class="n">gboolean</span>
<span class="nf">user_drop_privileges_to_user</span> <span class="p">(</span><span class="n">User</span> <span class="o">*</span><span class="n">user</span><span class="p">)</span>
<span class="p">{</span>
        <span class="k">if</span> <span class="p">(</span><span class="n">setresgid</span> <span class="p">(</span><span class="n">user</span><span class="o">-&gt;</span><span class="n">gid</span><span class="p">,</span> <span class="n">user</span><span class="o">-&gt;</span><span class="n">gid</span><span class="p">,</span> <span class="o">-</span><span class="mi">1</span><span class="p">)</span> <span class="o">!=</span> <span class="mi">0</span><span class="p">)</span> <span class="p">{</span>
                <span class="n">g_warning</span> <span class="p">(</span><span class="s">"setresgid() failed"</span><span class="p">);</span>
                <span class="k">return</span> <span class="n">FALSE</span><span class="p">;</span>
        <span class="p">}</span>
        <span class="k">if</span> <span class="p">(</span><span class="n">setresuid</span> <span class="p">(</span><span class="n">accounts_user_get_uid</span> <span class="p">(</span><span class="n">ACCOUNTS_USER</span> <span class="p">(</span><span class="n">user</span><span class="p">)),</span> <span class="n">accounts_user_get_uid</span> <span class="p">(</span><span class="n">ACCOUNTS_USER</span> <span class="p">(</span><span class="n">user</span><span class="p">)),</span> <span class="o">-</span><span class="mi">1</span><span class="p">)</span> <span class="o">!=</span> <span class="mi">0</span><span class="p">)</span> <span class="p">{</span>
                <span class="n">g_warning</span> <span class="p">(</span><span class="s">"setresuid() failed"</span><span class="p">);</span>
                <span class="k">return</span> <span class="n">FALSE</span><span class="p">;</span>
        <span class="p">}</span>
        <span class="k">return</span> <span class="n">TRUE</span><span class="p">;</span>
<span class="p">}</span>
</code></pre></div></div>

<p>This function is used to drop privileges while doing operations on behalf of an unprivileged user. Dropping the <a href="https://en.wikipedia.org/wiki/User_identifier#Effective_user_ID">EUID</a> is a sensible precaution, which prevents accountsservice from accessing a file which the unprivileged user cannot access themselves. Unfortunately, dropping the <a href="https://en.wikipedia.org/wiki/User_identifier#Real_user_ID">RUID</a> has the opposite effect of making security worse, because it enables the unprivileged user to send signals to accountsservice. For example, they can send a <code class="language-plaintext highlighter-rouge">SIGSTOP</code> which stops the accountsservice daemon and causes a denial of service.</p>

<p>The vulnerability can be triggered via multiple different D-Bus methods. Many of them involve precise timing to send the <code class="language-plaintext highlighter-rouge">SIGSTOP</code> signal at just the right moment. But there is a much simpler and more reliable way to reproduce the vulnerability by combining the privilege dropping vulnerability (<code class="language-plaintext highlighter-rouge">GHSL-2020-187</code>) with the infinite loop vulnerability (<code class="language-plaintext highlighter-rouge">GHSL-2020-188</code>), which is described next. So please see the description of <code class="language-plaintext highlighter-rouge">GHSL-2020-188</code>, below, for a proof-of-concept that triggers both vulnerabilities.</p>

<h4 id="impact">Impact</h4>

<p>An unprivileged local user can cause a local denial of service that affects all users of the system. Stopping the accountsservice daemon prevents the login screen from working, because <code class="language-plaintext highlighter-rouge">gdm3</code> needs to talk to accounts-daemon (via D-Bus).</p>

<p>Unfortunately, the impact is worse than just local denial of service, because this vulnerability can be chained with a separate vulnerability in gdm3 to achieve privilege escalation. Please see the description of <code class="language-plaintext highlighter-rouge">GHSL-2020-188</code>, below, for a proof-of-concept of the privilege escalation vulnerability.</p>

<h3 id="issue-2-accountsservice-pam_environment-infinite-loop-ghsl-2020-188-cve-2020-16127">Issue 2: accountsservice <code class="language-plaintext highlighter-rouge">.pam_environment</code> infinite loop (<code class="language-plaintext highlighter-rouge">GHSL-2020-188</code>, <code class="language-plaintext highlighter-rouge">CVE-2020-16127</code>)</h3>

<p>A <a href="https://git.launchpad.net/ubuntu/+source/accountsservice/tree/debian/patches/0010-set-language.patch?h=ubuntu/focal-updates&amp;id=e0347185d4c5554b026c13ccca691577c239afd5">source code patch</a> that (as far as I know) only exists in Ubuntu’s version of accountsservice, adds a function named <a href="https://git.launchpad.net/ubuntu/+source/accountsservice/tree/debian/patches/0010-set-language.patch?h=ubuntu/focal-updates&amp;id=e0347185d4c5554b026c13ccca691577c239afd5#n366"><code class="language-plaintext highlighter-rouge">is_in_pam_environment</code></a>:</p>

<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="k">static</span> <span class="n">gboolean</span>
<span class="nf">is_in_pam_environment</span> <span class="p">(</span><span class="n">User</span>        <span class="o">*</span><span class="n">user</span><span class="p">,</span>
                       <span class="k">const</span> <span class="n">gchar</span> <span class="o">*</span><span class="n">property</span><span class="p">)</span>
<span class="p">{</span>
        <span class="n">gboolean</span> <span class="n">ret</span> <span class="o">=</span> <span class="n">FALSE</span><span class="p">;</span>
        <span class="k">const</span> <span class="n">gchar</span> <span class="o">*</span><span class="n">prefix</span><span class="p">;</span>
        <span class="kt">FILE</span> <span class="o">*</span><span class="n">fp</span><span class="p">;</span>
        <span class="n">g_autofree</span> <span class="n">gchar</span> <span class="o">*</span><span class="n">pam_env</span> <span class="o">=</span> <span class="nb">NULL</span><span class="p">;</span>

        <span class="k">if</span> <span class="p">(</span><span class="n">g_strcmp0</span> <span class="p">(</span><span class="n">property</span><span class="p">,</span> <span class="s">"Language"</span><span class="p">)</span> <span class="o">==</span> <span class="mi">0</span><span class="p">)</span>
                <span class="n">prefix</span> <span class="o">=</span> <span class="s">"LANG"</span><span class="p">;</span>
        <span class="k">else</span> <span class="k">if</span> <span class="p">(</span><span class="n">g_strcmp0</span> <span class="p">(</span><span class="n">property</span><span class="p">,</span> <span class="s">"FormatsLocale"</span><span class="p">)</span> <span class="o">==</span> <span class="mi">0</span><span class="p">)</span>
                <span class="n">prefix</span> <span class="o">=</span> <span class="s">"LC_TIME"</span><span class="p">;</span>
        <span class="k">else</span>
                <span class="k">return</span> <span class="n">FALSE</span><span class="p">;</span>

        <span class="n">pam_env</span> <span class="o">=</span> <span class="n">g_build_path</span> <span class="p">(</span><span class="s">"/"</span><span class="p">,</span> <span class="n">accounts_user_get_home_directory</span> <span class="p">(</span><span class="n">ACCOUNTS_USER</span> <span class="p">(</span><span class="n">user</span><span class="p">)),</span> <span class="s">".pam_environment"</span><span class="p">,</span> <span class="nb">NULL</span><span class="p">);</span>

        <span class="k">if</span> <span class="p">(</span><span class="o">!</span><span class="n">user_drop_privileges_to_user</span> <span class="p">(</span><span class="n">user</span><span class="p">))</span>
                <span class="k">return</span> <span class="n">FALSE</span><span class="p">;</span>
        <span class="k">if</span> <span class="p">((</span><span class="n">fp</span> <span class="o">=</span> <span class="n">fopen</span> <span class="p">(</span><span class="n">pam_env</span><span class="p">,</span> <span class="s">"r"</span><span class="p">)))</span> <span class="p">{</span>
                <span class="n">gchar</span> <span class="n">line</span><span class="p">[</span><span class="mi">50</span><span class="p">];</span>
                <span class="k">while</span> <span class="p">((</span><span class="n">fgets</span> <span class="p">(</span><span class="n">line</span><span class="p">,</span> <span class="mi">50</span><span class="p">,</span> <span class="n">fp</span><span class="p">))</span> <span class="o">!=</span> <span class="nb">NULL</span><span class="p">)</span> <span class="p">{</span>
                        <span class="k">if</span> <span class="p">(</span><span class="n">g_str_has_prefix</span> <span class="p">(</span><span class="n">line</span><span class="p">,</span> <span class="n">prefix</span><span class="p">))</span> <span class="p">{</span>
                                <span class="n">ret</span> <span class="o">=</span> <span class="n">TRUE</span><span class="p">;</span>
                                <span class="k">break</span><span class="p">;</span>
                        <span class="p">}</span>
                <span class="p">}</span>
                <span class="n">fclose</span> <span class="p">(</span><span class="n">fp</span><span class="p">);</span>
        <span class="p">}</span>
        <span class="n">user_regain_privileges</span> <span class="p">();</span>

        <span class="k">return</span> <span class="n">ret</span><span class="p">;</span>
<span class="p">}</span>
</code></pre></div></div>

<p>This function parses the contents of a file named <code class="language-plaintext highlighter-rouge">.pam_environment</code> in the (unprivileged) user’s home directory. The user can trigger an infinite loop by creating a symlink to <code class="language-plaintext highlighter-rouge">/dev/zero</code>:</p>

<div class="language-bash highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="nb">ln</span> <span class="nt">-s</span> /dev/zero ~/.pam_environment
</code></pre></div></div>

<p>The infinite loop can then be triggered by sending a D-Bus message to the accountsservice daemon:</p>

<div class="language-bash highlighter-rouge"><div class="highlight"><pre class="highlight"><code>dbus-send <span class="nt">--system</span> <span class="nt">--dest</span><span class="o">=</span>org.freedesktop.Accounts <span class="nt">--type</span><span class="o">=</span>method_call <span class="nt">--print-reply</span><span class="o">=</span>literal /org/freedesktop/Accounts/User<span class="sb">`</span><span class="nb">id</span> <span class="nt">-u</span><span class="sb">`</span> org.freedesktop.Accounts.User.SetLanguage string:kevwozere &amp;
</code></pre></div></div>

<p>Because the accountsservice daemon is now stuck in an infinite loop, and has dropped privileges, it is now easy to also demonstrate <code class="language-plaintext highlighter-rouge">GHSL-2020-187</code>:</p>

<div class="language-bash highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="nb">kill</span> <span class="nt">-SIGSTOP</span> <span class="sb">`</span>pidof accounts-daemon<span class="sb">`</span>
</code></pre></div></div>

<p>The accountsservice daemon is now unresponsive, which means that the GNOME login screen no longer works. Unfortunately, this vulnerability can be chained with a separate vulnerability in gdm3 (which I have reported simultaneously to GNOME) to get privilege escalation. The steps (tested on Ubuntu Desktop 20.04.1 LTS) are as follows:</p>

<ul>
  <li>An unprivileged user logs into their account.</li>
  <li>They send a <code class="language-plaintext highlighter-rouge">SIGSTOP</code> to accountsservice, using the instructions above.</li>
  <li>They log out of their account.</li>
  <li>They open a text console (usually with a key combination such as Ctrl-Alt-F3).</li>
  <li>They login to the text console.</li>
  <li>They send accounts-daemon a <code class="language-plaintext highlighter-rouge">SIGSEGV</code>, followed by a <code class="language-plaintext highlighter-rouge">SIGCONT</code>, which causes accounts-daemon to crash.</li>
  <li>Because the accountsservice daemon was unresponsive, gdm3 is under the mistaken impression that there are zero user accounts on the system. So it triggers <code class="language-plaintext highlighter-rouge">gnome-initial-setup</code>, because it thinks this is a first-time installation.</li>
  <li>The user clicks through the <code class="language-plaintext highlighter-rouge">gnome-initial-setup</code> dialog boxes and creates a new account for themselves. The new account is a member of the <code class="language-plaintext highlighter-rouge">sudo</code> group.</li>
</ul>

<p>I have made a video of this proof-of-concept, which you can see <a href="https://drive.google.com/file/d/1rpRbXW1PRKMKRcxft3x-9tprjEbHLgOQ/view?usp=sharing">here</a>. The video is only visible to people who have the link, so it as safe as long as you are careful who you share the link with.</p>

<h4 id="impact-1">Impact</h4>

<p>An unprivileged local user can cause a local denial of service that affects all users of the system. Making the accountsservice daemon unresponsive prevents the login screen from working, because <code class="language-plaintext highlighter-rouge">gdm3</code> needs to talk to accounts-daemon (via D-Bus).</p>

<p>Unfortunately, the impact is worse than just local denial of service, because this vulnerability can be chained with a separate vulnerability in gdm3 to achieve privilege escalation, as explained in the proof-of-concept above.</p>

<h2 id="cve">CVE</h2>
<ul>
  <li>CVE-2020-16126</li>
  <li>CVE-2020-16127</li>
</ul>

<h2 id="coordinated-disclosure-timeline">Coordinated Disclosure Timeline</h2>
<ul>
  <li>2020-10-17: reported to Ubuntu: https://bugs.launchpad.net/ubuntu/+source/accountsservice/+bug/1900255</li>
  <li>2020-10-19: Reply from Marc Deslauriers.</li>
  <li>2020-10-20: CVE-2020-16126 and CVE-2020-16127 assigned.</li>
  <li>2020-10-27: Disclosure date agreed: 2020-11-03</li>
  <li>2020-11-03: Issue disclosed by Ubuntu: https://ubuntu.com/security/notices/USN-4616-1</li>
  <li>2020-11-05: Bug report made publicly visible: https://bugs.launchpad.net/ubuntu/+source/accountsservice/+bug/1900255</li>
  <li>2020-11-06: Bugs explained by Alex Murray on the <a href="https://ubuntusecuritypodcast.org/episode-95/">Ubuntu Security Podcast</a>.</li>
</ul>

<h2 id="credit">Credit</h2>

<p>These issues were discovered and reported by GHSL team member <a href="https://github.com/kevinbackhouse">@kevinbackhouse (Kevin Backhouse)</a>.</p>

<h2 id="contact">Contact</h2>

<p>You can contact the GHSL team at <code class="language-plaintext highlighter-rouge">securitylab@github.com</code>, please include a reference to <code class="language-plaintext highlighter-rouge">GHSL-2020-187</code> or <code class="language-plaintext highlighter-rouge">GHSL-2020-188</code>in any communication regarding this issue.