<header class="post-header d-block mb-6">
      <div class="date text-mono f5 my-3">June 22, 2021</div>
      <h1 class="my-2 h00-mktg lh-condensed">GHSL-2021-074: Local privilege escalation on any Linux system that uses polkit - CVE-2021-3560</h1>

      
      
      
      
      

      

      <a target="_blank" class="sc-frDJqD SgxRc d-inline-flex flex-row flex-items-center text-gray" href="https://github.com/kevinbackhouse">
        <img class="mr-3" src="https://avatars.githubusercontent.com/u/4358136?s=35" height="35" width="35">
        <span>Kevin Backhouse</span>
      </a>
    </header>

    <main id="content" class="markdown-body" aria-label="Content">
      
<h2 id="coordinated-disclosure-timeline">Coordinated Disclosure Timeline</h2>
<ul>
  <li>2021-05-04: Reported as a <a href="https://gitlab.freedesktop.org/polkit/polkit/-/issues/140">private issue</a>.</li>
  <li>2021-05-07: No response yet, so I added a <a href="https://gitlab.freedesktop.org/polkit/polkit/-/issues/140#note_909484">comment</a> to the issue, asking for somebody to acknowledge receipt of the report.</li>
  <li>2021-05-09: Emailed Red Hat (secalert@redhat.com) to notify them of the vulnerability. Some of the polkit engineers are Red Hat employees, so I asked if they could check that the polkit team have received my report.</li>
  <li>2021-05-10: Reply from Red Hat (secalert@redhat.com): they have assigned tracking number INC1755546 and will investigate.</li>
  <li>2021-05-18: Reply from Red Hat (secalert@redhat.com): “We got in touch with people inside the upstream community. They will now be looking at it.”</li>
  <li>2021-05-19: Message from Red Hat: “Although the PoC does not appear to be working in my RHEL test machine (the <code class="language-plaintext highlighter-rouge">Elapsed time</code> is an order of magnitude lower that in your example, so it may be that the disconnect happens too late?), but upstream appears to have validated it.”</li>
  <li>2021-05-19: I investigate why the PoC doesn’t work on RHEL. It turns out that the PoC <a href="https://gitlab.freedesktop.org/polkit/polkit/-/issues/140#note_925776">depends on <code class="language-plaintext highlighter-rouge">gnome-control-center</code> being installed</a>.</li>
  <li>2021-05-20: Red Hat confirm that the PoC is working for them after installing <code class="language-plaintext highlighter-rouge">gnome-control-center</code>.</li>
  <li>2021-05-20: Red Hat assigns CVE-2021-3560.</li>
  <li>2021-05-25: I develop a second PoC that uses the vulnerability to exploit <a href="https://packagekit.freedesktop.org/">packagekit</a>. This can be used to install <code class="language-plaintext highlighter-rouge">gnome-control-center</code> on RHEL.</li>
  <li>2021-05-26: Message from Red Hat: “I have sent a private disclosure notice to other distros ( https://oss-security.openwall.org/wiki/mailing-lists/distros ) The current tentative disclosure is Thursday 3rd of June (~7:00 AM UTC).”</li>
  <li>2021-06-03: <a href="https://gitlab.freedesktop.org/polkit/polkit/-/commit/a04d13affe0fa53ff618e07aa8f57f4c0e3b9b81">Bug fix</a></li>
  <li>2021-06-03: Vulnerability disclosed: <a href="https://access.redhat.com/security/cve/cve-2021-3560">Red Hat</a>, <a href="https://security-tracker.debian.org/tracker/CVE-2021-3560">Debian</a>, <a href="https://ubuntu.com/security/CVE-2021-3560">Ubuntu</a>, <a href="https://security.archlinux.org/CVE-2021-3560">Arch Linux</a></li>
</ul>

<h2 id="summary">Summary</h2>

<p>There is an authentication bypass vulnerability in polkit, which enables an unprivileged user to get authorization from polkit to perform a privileged action.</p>

<h2 id="product">Product</h2>

<p><a href="https://gitlab.freedesktop.org/polkit/polkit">polkit</a></p>

<h2 id="tested-versions">Tested Versions</h2>

<ul>
  <li>policykit-1, 0.105-26ubuntu1 (tested on Ubuntu 20.04.2 LTS)</li>
  <li>policykit-1, 0.105-30 (tested on Ubuntu 21.04)</li>
  <li>polkit, 0.116-7 (tested on Fedora 32)</li>
</ul>

<h2 id="details">Details</h2>

<h3 id="issue-1-authentication-bypass-in-polkit-ghsl-2021-074">Issue 1: Authentication bypass in polkit (<code class="language-plaintext highlighter-rouge">GHSL-2021-074</code>)</h3>

<p>The function <a href="https://gitlab.freedesktop.org/polkit/polkit/-/blob/0.116/src/polkit/polkitsystembusname.c#L388"><code class="language-plaintext highlighter-rouge">polkit_system_bus_name_get_creds_sync</code></a> is used to get the uid and pid of the process requesting the action. It does this by sending the unique bus name of the requesting process, which is typically something like “:1.96”, to <code class="language-plaintext highlighter-rouge">dbus-daemon</code>. These unique names are assigned and managed by <code class="language-plaintext highlighter-rouge">dbus-daemon</code> and cannot be forged, so this is a good way to check the privileges of the requesting process.</p>

<p>The vulnerability happens when the requesting process disconnects from <code class="language-plaintext highlighter-rouge">dbus-daemon</code> just before the call to <code class="language-plaintext highlighter-rouge">polkit_system_bus_name_get_creds_sync</code> starts. In this scenario, the unique bus name is no longer valid, so <code class="language-plaintext highlighter-rouge">dbus-daemon</code> sends back an error reply. This error case is handled in <code class="language-plaintext highlighter-rouge">polkit_system_bus_name_get_creds_sync</code> by setting the value of the <code class="language-plaintext highlighter-rouge">error</code> parameter, but it still returns <code class="language-plaintext highlighter-rouge">TRUE</code>, rather than <code class="language-plaintext highlighter-rouge">FALSE</code>. We are not sure whether it’s a bug that the return value is TRUE when this error happens, but this behavior certainly means that all callers of <code class="language-plaintext highlighter-rouge">polkit_system_bus_name_get_creds_sync</code> need to carefully check whether an error was set. If the calling function forgets to check for errors then it will think that the uid of the requesting process is 0 (because the <code class="language-plaintext highlighter-rouge">AsyncGetBusNameCredsData</code> struct is zero initialized). In other words, it will think that the action was requested by a root process, and will therefore allow it.</p>

<p>Most of the callers of <code class="language-plaintext highlighter-rouge">polkit_system_bus_name_get_creds_sync</code> check the error value correctly, and are therefore not vulnerable. But the error value is not checked in the following stack trace:</p>

<div class="language-plaintext highlighter-rouge"><div class="highlight"><pre class="highlight"><code>0  in polkit_system_bus_name_get_creds_sync of polkitsystembusname.c:393
1  in polkit_system_bus_name_get_user_sync of polkitsystembusname.c:511
2  in polkit_backend_session_monitor_get_user_for_subject of polkitbackendsessionmonitor-systemd.c:303
3  in check_authorization_sync of polkitbackendinteractiveauthority.c:1113
4  in check_authorization_sync of polkitbackendinteractiveauthority.c:1223
5  in polkit_backend_interactive_authority_check_authorization of polkitbackendinteractiveauthority.c:971
6  in server_handle_check_authorization of polkitbackendauthority.c:795
7  in server_handle_method_call of polkitbackendauthority.c:1274
</code></pre></div></div>

<p>The bug is in this snippet of code in <a href="https://gitlab.freedesktop.org/polkit/polkit/-/blob/0.116/src/polkitbackend/polkitbackendinteractiveauthority.c#L1121"><code class="language-plaintext highlighter-rouge">check_authorization_sync</code></a>:</p>

<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="cm">/* every subject has a user; this is supplied by the client, so we rely
 * on the caller to validate its acceptability. */</span>
<span class="n">user_of_subject</span> <span class="o">=</span> <span class="n">polkit_backend_session_monitor_get_user_for_subject</span> <span class="p">(</span><span class="n">priv</span><span class="o">-&gt;</span><span class="n">session_monitor</span><span class="p">,</span>
                                                                       <span class="n">subject</span><span class="p">,</span> <span class="nb">NULL</span><span class="p">,</span>
                                                                       <span class="n">error</span><span class="p">);</span>
<span class="k">if</span> <span class="p">(</span><span class="n">user_of_subject</span> <span class="o">==</span> <span class="nb">NULL</span><span class="p">)</span>
    <span class="k">goto</span> <span class="n">out</span><span class="p">;</span>

<span class="cm">/* special case: uid 0, root, is _always_ authorized for anything */</span>
<span class="k">if</span> <span class="p">(</span><span class="n">POLKIT_IS_UNIX_USER</span> <span class="p">(</span><span class="n">user_of_subject</span><span class="p">)</span> <span class="o">&amp;&amp;</span> <span class="n">polkit_unix_user_get_uid</span> <span class="p">(</span><span class="n">POLKIT_UNIX_USER</span> <span class="p">(</span><span class="n">user_of_subject</span><span class="p">))</span> <span class="o">==</span> <span class="mi">0</span><span class="p">)</span>
  <span class="p">{</span>
    <span class="n">result</span> <span class="o">=</span> <span class="n">polkit_authorization_result_new</span> <span class="p">(</span><span class="n">TRUE</span><span class="p">,</span> <span class="n">FALSE</span><span class="p">,</span> <span class="nb">NULL</span><span class="p">);</span>
    <span class="k">goto</span> <span class="n">out</span><span class="p">;</span>
  <span class="p">}</span>
</code></pre></div></div>

<p>Notice that the value of <code class="language-plaintext highlighter-rouge">error</code> is not checked.</p>

<h4 id="impact">Impact</h4>

<p>This issue may lead to local privilege escalation on any Linux system that uses polkit.</p>

<h4 id="resources">Resources</h4>

<p>Proof of concept exploit: <code class="language-plaintext highlighter-rouge">GHSL-2021-074-polkit.bundle</code></p>

<h2 id="cve">CVE</h2>
<ul>
  <li>CVE-2021-3560</li>
</ul>

<h2 id="credit">Credit</h2>

<p>This issue was discovered and reported by GHSL team member <a href="https://github.com/kevinbackhouse">@kevinbackhouse (Kevin Backhouse)</a>.</p>

<h2 id="contact">Contact</h2>

<p>You can contact the GHSL team at <code class="language-plaintext highlighter-rouge">securitylab@github.com</code>, please include a reference to <code class="language-plaintext highlighter-rouge">GHSL-2021-074</code> in any communication regarding th