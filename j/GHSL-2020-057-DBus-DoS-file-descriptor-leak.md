<header class="post-header d-block mb-6">
      <div class="date text-mono f5 my-3">June 17, 2020</div>
      <h1 class="my-2 h00-mktg lh-condensed">GHSL-2020-057: dbus file descriptor leak (DoS) - CVE-2020-12049</h1>

      
      
      
      
      

      

      <a target="_blank" class="sc-frDJqD SgxRc d-inline-flex flex-row flex-items-center text-gray" href="https://github.com/kevinbackhouse">
        <img class="mr-3" src="https://avatars.githubusercontent.com/u/4358136?s=35" height="35" width="35">
        <span>Kevin Backhouse</span>
      </a>
    </header>

    <main id="content" class="markdown-body" aria-label="Content">
      <h2 id="summary">Summary</h2>

<p>D-Bus has a file descriptor leak, which can lead to denial of service when the dbus-daemon runs out of file descriptors. An unprivileged local attacker can use this to attack the system dbus-daemon, leading to denial of service for all users of the machine.</p>

<h2 id="product">Product</h2>

<p>D-Bus (dbus-daemon)</p>

<h2 id="tested-version">Tested Version</h2>

<p>1.12.2-1ubuntu1.1 (tested on Ubuntu 18.04.4 LTS)</p>

<h2 id="details-file-descriptor-leak-in-_dbus_read_socket_with_unix_fds">Details: File descriptor leak in <code class="language-plaintext highlighter-rouge">_dbus_read_socket_with_unix_fds</code></h2>

<p>The function <code class="language-plaintext highlighter-rouge">_dbus_read_socket_with_unix_fds</code> contains the following code at
<a href="https://gitlab.freedesktop.org/dbus/dbus/-/blob/1530582863b801839bc57c9ec8bc9ca3d16f2a65/dbus/dbus-sysdeps-unix.c#L438">dbus-sysdeps-unix.c, line 438</a>:</p>

<div class="language-plaintext highlighter-rouge"><div class="highlight"><pre class="highlight"><code>if (m.msg_flags &amp; MSG_CTRUNC)
  {
    /* Hmm, apparently the control data was truncated. The bad
       thing is that we might have completely lost a couple of fds
       without chance to recover them. Hence let's treat this as a
       serious error. */

    errno = ENOSPC;
    _dbus_string_set_length (buffer, start);
    return -1;
  }
</code></pre></div></div>

<p>The intention of this code is to handle the case where too many file descriptors are sent over the unix socket, causing the control data to get truncated. That could be a deliberate attempt by an attacker to cause a denial of service. The problem with the code is that some file descriptors may still have been received, even though the message has been truncated. So we need to make sure that those file descriptors are closed. Otherwise an attacker can cause us to quickly run out of file descriptors.</p>

<h3 id="impact">Impact</h3>

<p>This issue can lead to a local denial of service attack: an unprivileged local attacker can make the system unusable for all users. For example, on Ubuntu 18.04.4 LTS, my proof-of-concept exploit prevents all users from logging in, because the login screen needs to send a D-Bus message, but the dbus-daemon is no longer able to send or receive any messages because it cannot create any new file descriptors.</p>

<h2 id="cve">CVE</h2>

<ul>
  <li>CVE-2020-12049</li>
</ul>

<h2 id="coordinated-disclosure-timeline">Coordinated Disclosure Timeline</h2>

<p>This report was subject to the GHSL <a href="https://securitylab.github.com/advisories/#policy">coordinated disclosure policy</a>.</p>

<ul>
  <li>04/09/2020: reported to maintainer</li>
  <li>06/04/2020: embargo lifted, issue public and fixed</li>
</ul>

<h2 id="resources">Resources</h2>

<ul>
  <li>https://gitlab.freedesktop.org/dbus/dbus/-/issues/294#note_522136</li>
  <li>https://github.com/github/securitylab/tree/c8db365b3258df1c6fd12ff0f818115f46423e25/SecurityExploits/freedesktop/DBus-CVE-2020-12049</li>
</ul>

<h2 id="credit">Credit</h2>

<p>This issue was discovered and reported by GHSL team member <a href="https://github.com/kevinbackhouse">@kevinbackhouse (Kevin Backhouse)</a>.</p>

<h2 id="contact">Contact</h2>

<p>You can contact the GHSL team at <code class="language-plaintext highlighter-rouge">securitylab@github.com</code>, please include the GHSL-ID: <code class="language-plaintext highlighter-rouge">GHSL-2020-057</code> in any communication regarding this issue.</p>

    