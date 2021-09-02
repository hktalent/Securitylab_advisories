<header class="post-header d-block mb-6">
      <div class="date text-mono f5 my-3">March 25, 2021</div>
      <h1 class="my-2 h00-mktg lh-condensed">GHSL-2021-045: Integer Overflow in GLib - CVE-2021-27219</h1>

      
      
      
      
      

      

      <a target="_blank" class="sc-frDJqD SgxRc d-inline-flex flex-row flex-items-center text-gray" href="https://github.com/kevinbackhouse">
        <img class="mr-3" src="https://avatars.githubusercontent.com/u/4358136?s=35" height="35" width="35">
        <span>Kevin Backhouse</span>
      </a>
    </header>

    <main id="content" class="markdown-body" aria-label="Content">
      <h2 id="coordinated-disclosure-timeline">Coordinated Disclosure Timeline</h2>
<ul>
  <li>2021-02-04: Reported as private issue: https://gitlab.gnome.org/GNOME/glib/-/issues/2319</li>
  <li>2021-02-04: Fix merged: https://gitlab.gnome.org/GNOME/glib/-/merge_requests/1926</li>
</ul>

<h2 id="summary">Summary</h2>

<p>The function <a href="https://gitlab.gnome.org/GNOME/glib/-/blob/2.67.2/glib/gbytes.c#L93"><code class="language-plaintext highlighter-rouge">g_bytes_new</code></a> has an integer overflow due to an implicit cast from 64 bits to 32 bits. The overflow could potentially lead to a memory corruption vulnerability.</p>

<h2 id="product">Product</h2>

<p>GLib</p>

<h2 id="tested-versions">Tested Versions</h2>

<ul>
  <li>Ubuntu 20.04 (x86_64): version 2.64.6-1</li>
  <li>CentOS Stream (x86_64): version 2.56.4-9</li>
  <li>archlinux (x86_64): 2.66.4-2</li>
</ul>

<h2 id="details">Details</h2>

<h3 id="issue-1-integer-overflow-in-g_bytes_new-ghsl-2021-045">Issue 1: Integer overflow in g_bytes_new (GHSL-2021-045)</h3>

<p>On 64-bit platforms, an integer overflow can occur in <code class="language-plaintext highlighter-rouge">g_bytes_new</code>, due to an implicit cast from <code class="language-plaintext highlighter-rouge">gsize</code> to <code class="language-plaintext highlighter-rouge">guint</code>. The overflow happens in the call to <code class="language-plaintext highlighter-rouge">g_memdup</code> (<a href="https://gitlab.gnome.org/GNOME/glib/-/blob/2.67.2/glib/gbytes.c#L98">gbytes.c, line 98</a>). The reason is that <code class="language-plaintext highlighter-rouge">size</code> is a 64-bit <code class="language-plaintext highlighter-rouge">gsize</code>, but <code class="language-plaintext highlighter-rouge">g_memdup</code> takes a 32-bit <code class="language-plaintext highlighter-rouge">guint</code>.</p>

<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="n">GBytes</span> <span class="o">*</span>
<span class="nf">g_bytes_new</span> <span class="p">(</span><span class="n">gconstpointer</span> <span class="n">data</span><span class="p">,</span>
             <span class="n">gsize</span>         <span class="n">size</span><span class="p">)</span>
<span class="p">{</span>
  <span class="n">g_return_val_if_fail</span> <span class="p">(</span><span class="n">data</span> <span class="o">!=</span> <span class="nb">NULL</span> <span class="o">||</span> <span class="n">size</span> <span class="o">==</span> <span class="mi">0</span><span class="p">,</span> <span class="nb">NULL</span><span class="p">);</span>

  <span class="k">return</span> <span class="n">g_bytes_new_take</span> <span class="p">(</span><span class="n">g_memdup</span> <span class="p">(</span><span class="n">data</span><span class="p">,</span> <span class="n">size</span><span class="p">),</span> <span class="n">size</span><span class="p">);</span>  <span class="o">&lt;===</span>  <span class="n">integer</span> <span class="n">overflow</span>
<span class="p">}</span>
</code></pre></div></div>

<p>When the overflow occurs, it does not cause the code to crash immediately. Instead, <code class="language-plaintext highlighter-rouge">g_memdup</code> creates a much smaller buffer than it should. This causes <code class="language-plaintext highlighter-rouge">g_bytes_new</code> to return a <code class="language-plaintext highlighter-rouge">GBytes</code> object containing a much smaller data buffer than it’s size would suggest. For example, if <code class="language-plaintext highlighter-rouge">size</code> is <code class="language-plaintext highlighter-rouge">0x100000008</code> then <code class="language-plaintext highlighter-rouge">g_bytes_new</code> will return a <code class="language-plaintext highlighter-rouge">GBytes</code> object that claims to contain a 4GB buffer, but actually contains an 8 byte buffer.</p>

<p>We have attached a proof-of-concept which demonstrates that it is possible to trigger the overflow. The proof-of-concept triggers the overflow via <code class="language-plaintext highlighter-rouge">polkit-agent-helper-1</code>, which is a SUID binary. Luckily the poc only causes <code class="language-plaintext highlighter-rouge">polkit-agent-helper-1</code> to crash with a <code class="language-plaintext highlighter-rouge">SIGABRT</code>, due to an assertion failure. However, GLib is a very widely used library, so it is possible that other attack vectors exist.</p>

<p>To run the poc:</p>

<div class="language-plaintext highlighter-rouge"><div class="highlight"><pre class="highlight"><code>gcc polkithelperabort.c -o polkithelperabort
./polkithelperabort &lt;username&gt;
</code></pre></div></div>

<p>The poc will ask for the user’s password, which is sent to <code class="language-plaintext highlighter-rouge">polkit-agent-helper-1</code> in the normal way, along with a 4GB “cookie”, which triggers the overflow. Although the poc will only work with a valid password, it will work for any user account. So if you are worried about plugging a genuine password into the poc, just create a temporary user account for running the poc, and delete it when you are done.</p>

<p>The poc should trigger an assertion failure, with an error message like this:</p>

<div class="language-plaintext highlighter-rouge"><div class="highlight"><pre class="highlight"><code>GLib-GIO:ERROR:../glib/gio/gdbusmessage.c:2399:append_value_to_blob: assertion failed: (g_utf8_validate (v, -1, &amp;end) &amp;&amp; (end == v + len))
Bail out! GLib-GIO:ERROR:../glib/gio/gdbusmessage.c:2399:append_value_to_blob: assertion failed: (g_utf8_validate (v, -1, &amp;end) &amp;&amp; (end == v + len))
</code></pre></div></div>

<h4 id="impact">Impact</h4>

<p>The poc which we have provided only causes a harmless crash. We are not currently aware of an exploitable attack vector for this issue. However, there is a risk that it could lead to memory corruption vulnerability, which could potentially be used to gain code execution in an application that uses GLib.</p>

<h2 id="cve">CVE</h2>
<ul>
  <li>CVE-2021-27219</li>
</ul>

<h2 id="credit">Credit</h2>

<p>This issue was discovered and reported by GHSL team member <a href="https://github.com/kevinbackhouse">@kevinbackhouse (Kevin Backhouse)</a>.</p>

<h2 id="contact">Contact</h2>

<p>You can contact the GHSL team at <code class="language-plaintext highlighter-rouge">securitylab@github.com</code>, please include a reference to <code class="language-plaintext highlighter-rouge">GHSL-2021-045</code> in any communication regarding this issue.</