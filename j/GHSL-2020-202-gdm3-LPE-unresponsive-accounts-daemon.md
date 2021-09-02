<header class="post-header d-block mb-6">
      <div class="date text-mono f5 my-3">November 9, 2020</div>
      <h1 class="my-2 h00-mktg lh-condensed">GHSL-2020-202: Local Privilege Escalation (LPE) in Ubuntu gdm3 - CVE-2020-16125</h1>

      
      
      
      
      

      

      <a target="_blank" class="sc-frDJqD SgxRc d-inline-flex flex-row flex-items-center text-gray" href="https://github.com/kevinbackhouse">
        <img class="mr-3" src="https://avatars.githubusercontent.com/u/4358136?s=35" height="35" width="35">
        <span>Kevin Backhouse</span>
      </a>
    </header>

    <main id="content" class="markdown-body" aria-label="Content">
      <h2 id="summary">Summary</h2>

<p>gdm3 can be tricked into launching <code class="language-plaintext highlighter-rouge">gnome-initial-setup</code>, enabling an unprivileged user to create a new user account for themselves. The new account is a member of the <code class="language-plaintext highlighter-rouge">sudo</code> group, so this enables the unprivileged user to obtain admin privileges.</p>

<p>The vulnerability in gdm3 is triggered when the accountsservice daemon is unresponsive. I have simultaneously reported a separate denial-of-service vulnerability in accountsservice to Ubuntu. On Ubuntu 20.04.1 LTS, I am able to use the vulnerability in accountsservice to trigger the vulnerability in gdm3 and escalate privileges. As far as I know, the vulnerability in accountsservice only exists on Ubuntu. The freedesktop and debian versions of accountsservice do not contain the vulnerable code. However, gdm3 may also be vulnerable on other systems if a different way can be found to block D-Bus communication with the accountsservice daemon.</p>

<h2 id="product">Product</h2>

<p>gdm3</p>

<h2 id="tested-version">Tested Version</h2>

<ul>
  <li>gdm3, version 3.36.3-0ubuntu0.20.04.1</li>
  <li>Tested on Ubuntu 20.04.1 LTS</li>
  <li>Tested with accountsservice, version 0.6.55-0ubuntu12~20.04.1</li>
</ul>

<h2 id="details">Details</h2>

<h3 id="issue-1-gdm3-lpe-due-to-unresponsive-accounts-daemon-ghsl-2020-202-cve-2020-16125">Issue 1: gdm3 LPE due to unresponsive accounts-daemon (<code class="language-plaintext highlighter-rouge">GHSL-2020-202</code>, <code class="language-plaintext highlighter-rouge">CVE-2020-16125</code>)</h3>

<p><a href="https://gitlab.gnome.org/GNOME/gnome-initial-setup">gnome-initial-setup</a> is an application that is run on freshly installed systems. It presents a series of dialog boxes to the user, enabling them to create a new account on the machine. The newly created account is an admin account (it is a member of the <code class="language-plaintext highlighter-rouge">sudo</code> group). gnome-initial-setup is invoked by gdm3 when there are no user accounts on the machine. Therefore, if we can trick gdm3 into thinking that there are no user accounts, then it will launch gnome-initial-setup, enabling us to gain root privileges.</p>

<p>gdm3 uses a D-Bus method call to get the list of existing users from the accountsservice daemon, in <a href="https://gitlab.gnome.org/GNOME/gdm/-/blob/3.36.3/daemon/gdm-display.c#L513"><code class="language-plaintext highlighter-rouge">look_for_existing_users_sync</code></a>:</p>

<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="k">static</span> <span class="kt">void</span>
<span class="nf">look_for_existing_users_sync</span> <span class="p">(</span><span class="n">GdmDisplay</span> <span class="o">*</span><span class="n">self</span><span class="p">)</span>
<span class="p">{</span>
        <span class="n">GdmDisplayPrivate</span> <span class="o">*</span><span class="n">priv</span><span class="p">;</span>
        <span class="n">GError</span> <span class="o">*</span><span class="n">error</span> <span class="o">=</span> <span class="nb">NULL</span><span class="p">;</span>
        <span class="n">GVariant</span> <span class="o">*</span><span class="n">call_result</span><span class="p">;</span>
        <span class="n">GVariant</span> <span class="o">*</span><span class="n">user_list</span><span class="p">;</span>

        <span class="n">priv</span> <span class="o">=</span> <span class="n">gdm_display_get_instance_private</span> <span class="p">(</span><span class="n">self</span><span class="p">);</span>
        <span class="n">priv</span><span class="o">-&gt;</span><span class="n">accountsservice_proxy</span> <span class="o">=</span> <span class="n">g_dbus_proxy_new_sync</span> <span class="p">(</span><span class="n">priv</span><span class="o">-&gt;</span><span class="n">connection</span><span class="p">,</span>
                                                             <span class="mi">0</span><span class="p">,</span> <span class="nb">NULL</span><span class="p">,</span>
                                                             <span class="s">"org.freedesktop.Accounts"</span><span class="p">,</span>
                                                             <span class="s">"/org/freedesktop/Accounts"</span><span class="p">,</span>
                                                             <span class="s">"org.freedesktop.Accounts"</span><span class="p">,</span>
                                                             <span class="nb">NULL</span><span class="p">,</span>
                                                             <span class="o">&amp;</span><span class="n">error</span><span class="p">);</span>

        <span class="k">if</span> <span class="p">(</span><span class="o">!</span><span class="n">priv</span><span class="o">-&gt;</span><span class="n">accountsservice_proxy</span><span class="p">)</span> <span class="p">{</span>
                <span class="n">g_warning</span> <span class="p">(</span><span class="s">"Failed to contact accountsservice: %s"</span><span class="p">,</span> <span class="n">error</span><span class="o">-&gt;</span><span class="n">message</span><span class="p">);</span>
                <span class="k">goto</span> <span class="n">out</span><span class="p">;</span>
        <span class="p">}</span>

        <span class="n">call_result</span> <span class="o">=</span> <span class="n">g_dbus_proxy_call_sync</span> <span class="p">(</span><span class="n">priv</span><span class="o">-&gt;</span><span class="n">accountsservice_proxy</span><span class="p">,</span>
                                              <span class="s">"ListCachedUsers"</span><span class="p">,</span>
                                              <span class="nb">NULL</span><span class="p">,</span>
                                              <span class="mi">0</span><span class="p">,</span>
                                              <span class="o">-</span><span class="mi">1</span><span class="p">,</span>
                                              <span class="nb">NULL</span><span class="p">,</span>
                                              <span class="o">&amp;</span><span class="n">error</span><span class="p">);</span>

        <span class="k">if</span> <span class="p">(</span><span class="o">!</span><span class="n">call_result</span><span class="p">)</span> <span class="p">{</span>
                <span class="n">g_warning</span> <span class="p">(</span><span class="s">"Failed to list cached users: %s"</span><span class="p">,</span> <span class="n">error</span><span class="o">-&gt;</span><span class="n">message</span><span class="p">);</span>
                <span class="k">goto</span> <span class="n">out</span><span class="p">;</span>
        <span class="p">}</span>

        <span class="n">g_variant_get</span> <span class="p">(</span><span class="n">call_result</span><span class="p">,</span> <span class="s">"(@ao)"</span><span class="p">,</span> <span class="o">&amp;</span><span class="n">user_list</span><span class="p">);</span>
        <span class="n">priv</span><span class="o">-&gt;</span><span class="n">have_existing_user_accounts</span> <span class="o">=</span> <span class="n">g_variant_n_children</span> <span class="p">(</span><span class="n">user_list</span><span class="p">)</span> <span class="o">&gt;</span> <span class="mi">0</span><span class="p">;</span>
        <span class="n">g_variant_unref</span> <span class="p">(</span><span class="n">user_list</span><span class="p">);</span>
        <span class="n">g_variant_unref</span> <span class="p">(</span><span class="n">call_result</span><span class="p">);</span>
<span class="nl">out:</span>
        <span class="n">g_clear_error</span> <span class="p">(</span><span class="o">&amp;</span><span class="n">error</span><span class="p">);</span>
<span class="p">}</span>
</code></pre></div></div>

<p>It seems that the value of <code class="language-plaintext highlighter-rouge">priv-&gt;have_existing_user_accounts</code> is false by default, so if the D-Bus method call fails (due to a timeout) then it will remain false. You will see the message “Failed to list cached users” in the system log.</p>

<p><code class="language-plaintext highlighter-rouge">look_for_existing_users_sync</code> is called from <a href="https://gitlab.gnome.org/GNOME/gdm/-/blob/3.36.3/daemon/gdm-display.c#L557"><code class="language-plaintext highlighter-rouge">gdm_display_prepare</code></a>:</p>

<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="n">gboolean</span>
<span class="nf">gdm_display_prepare</span> <span class="p">(</span><span class="n">GdmDisplay</span> <span class="o">*</span><span class="n">self</span><span class="p">)</span>
<span class="p">{</span>
        <span class="n">GdmDisplayPrivate</span> <span class="o">*</span><span class="n">priv</span><span class="p">;</span>
        <span class="n">gboolean</span> <span class="n">ret</span><span class="p">;</span>

        <span class="n">g_return_val_if_fail</span> <span class="p">(</span><span class="n">GDM_IS_DISPLAY</span> <span class="p">(</span><span class="n">self</span><span class="p">),</span> <span class="n">FALSE</span><span class="p">);</span>

        <span class="n">priv</span> <span class="o">=</span> <span class="n">gdm_display_get_instance_private</span> <span class="p">(</span><span class="n">self</span><span class="p">);</span>

        <span class="n">g_debug</span> <span class="p">(</span><span class="s">"GdmDisplay: Preparing display: %s"</span><span class="p">,</span> <span class="n">priv</span><span class="o">-&gt;</span><span class="n">id</span><span class="p">);</span>

        <span class="cm">/* FIXME: we should probably do this in a more global place,
         * asynchronously
         */</span>
        <span class="n">look_for_existing_users_sync</span> <span class="p">(</span><span class="n">self</span><span class="p">);</span>

        <span class="n">priv</span><span class="o">-&gt;</span><span class="n">doing_initial_setup</span> <span class="o">=</span> <span class="n">wants_initial_setup</span> <span class="p">(</span><span class="n">self</span><span class="p">);</span>

        <span class="n">g_object_ref</span> <span class="p">(</span><span class="n">self</span><span class="p">);</span>
        <span class="n">ret</span> <span class="o">=</span> <span class="n">GDM_DISPLAY_GET_CLASS</span> <span class="p">(</span><span class="n">self</span><span class="p">)</span><span class="o">-&gt;</span><span class="n">prepare</span> <span class="p">(</span><span class="n">self</span><span class="p">);</span>
        <span class="n">g_object_unref</span> <span class="p">(</span><span class="n">self</span><span class="p">);</span>

        <span class="k">return</span> <span class="n">ret</span><span class="p">;</span>
<span class="p">}</span>
</code></pre></div></div>

<p>If <code class="language-plaintext highlighter-rouge">priv-&gt;have_existing_user_accounts</code> is false, then <code class="language-plaintext highlighter-rouge">wants_initial_setup</code> returns true, leading to the invocation of gnome-initial-setup.</p>

<h4 id="impact">Impact</h4>

<p>This issue may lead to local privilege escalation, where an unprivileged user is able to gain root privileges.</p>

<h4 id="remediation">Remediation</h4>

<p>I recommend making the default value of <code class="language-plaintext highlighter-rouge">priv-&gt;have_existing_user_accounts</code> true.</p>

<h2 id="cve">CVE</h2>
<ul>
  <li>CVE-2020-16125</li>
</ul>

<h2 id="coordinated-disclosure-timeline">Coordinated Disclosure Timeline</h2>
<ul>
  <li>2020-10-17: Reported to GNOME gdm: https://gitlab.gnome.org/GNOME/gdm/-/issues/642</li>
  <li>2020-10-18: Also reported to gdm3 package on Ubuntu: https://bugs.launchpad.net/ubuntu/+source/gdm3/+bug/1900314</li>
  <li>2020-10-19: Acknowledged by Marc Deslauriers (Ubuntu). No response yet from GNOME.</li>
  <li>2020-10-20: CVE-2020-16125 assigned by Seth Arnold (Ubuntu).</li>
  <li>2020-10-26: Marc Deslauriers (Ubuntu) asked if I had heard from GNOME yet.</li>
  <li>2020-10-26: I email security@gnome.org to ask about the status of <a href="https://gitlab.gnome.org/GNOME/gdm/-/issues/642">issue 642</a>.</li>
  <li>2020-10-26: Replies received from Tobias Mueller and Ray Strode at GNOME.</li>
  <li>2020-10-27: Fix implemented by Marco Trevisan (GNOME): https://gitlab.gnome.org/GNOME/gdm/-/merge_requests/117</li>
  <li>2020-10-27: Disclosure date agreed with GNOME and Ubuntu: 2020-11-03</li>
  <li>2020-11-03: Issue disclosed by Ubuntu: https://ubuntu.com/security/notices/USN-4614-1</li>
  <li>2020-11-03: GNOME bug report made publicly visible: https://gitlab.gnome.org/GNOME/gdm/-/issues/642</li>
  <li>2020-11-06: Exploit explained by Alex Murray on the <a href="https://ubuntusecuritypodcast.org/episode-95/">Ubuntu Security Podcast</a>.</li>
</ul>

<h2 id="credit">Credit</h2>

<p>This issue was discovered and reported by GHSL team member <a href="https://github.com/kevinbackhouse">@kevinbackhouse (Kevin Backhouse)</a>.</p>

<h2 id="contact">Contact</h2>

<p>You can contact the GHSL team at <code class="language-plaintext highlighter-rouge">securitylab@github.com</code>, please include a reference to <code class="language-plaintext highlighter-rouge">GHSL-2020-202</code> in any communication regarding this issue.</p>

