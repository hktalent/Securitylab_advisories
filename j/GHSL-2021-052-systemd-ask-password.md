<header class="post-header d-block mb-6">
      <div class="date text-mono f5 my-3">March 25, 2021</div>
      <h1 class="my-2 h00-mktg lh-condensed">GHSL-2021-052: Potential local Denial of Service in systemd</h1>

      
      
      
      
      

      

      <a target="_blank" class="sc-frDJqD SgxRc d-inline-flex flex-row flex-items-center text-gray" href="https://github.com/kevinbackhouse">
        <img class="mr-3" src="https://avatars.githubusercontent.com/u/4358136?s=35" height="35" width="35">
        <span>Kevin Backhouse</span>
      </a>
    </header>

    <main id="content" class="markdown-body" aria-label="Content">
      <h2 id="coordinated-disclosure-timeline">Coordinated Disclosure Timeline</h2>
<ul>
  <li>2021-03-12: Emailed report, PoC, and suggested fix to systemd-security@redhat.com</li>
  <li>2021-03-12: Reply from Zbigniew Jędrzejewski-Szmek: <em>Low impact, because: “systemd-ask-password normally runs privileged and only accepts input from privileged clients. So this forms a self-DoS.</em>”</li>
  <li>2021-03-12: Our suggested fix is merged: https://github.com/systemd/systemd/pull/18985</li>
</ul>

<h2 id="summary">Summary</h2>

<p>There is an infinite loop in systemd-ask-password, due to an integer overflow in an error handling code path. The bug can be triggered by entering an invalid unicode character followed by backspace.</p>

<h2 id="product">Product</h2>

<p>systemd</p>

<h2 id="tested-version">Tested Version</h2>

<p>systemd v247.3-1  (tested on Arch Linux)</p>

<h2 id="details">Details</h2>

<h3 id="issue-1-infinite-loop-in-systemd-ask-password-ghsl-2021-052">Issue 1: Infinite loop in systemd-ask-password (<code class="language-plaintext highlighter-rouge">GHSL-2021-052</code>)</h3>

<p>The function <code class="language-plaintext highlighter-rouge">ask_password_tty</code> (src/shared/ask-password-api.c, lines 391-678) has an integer overflow bug at <a href="https://github.com/systemd/systemd/blob/c99c197d07da13649269a24a9a50107d16b5b784/src/shared/ask-password-api.c#L586">line 586</a>:</p>

<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="k">for</span> <span class="p">(;;)</span> <span class="p">{</span>
  <span class="kt">size_t</span> <span class="n">z</span><span class="p">;</span>

  <span class="n">z</span> <span class="o">=</span> <span class="n">utf8_encoded_valid_unichar</span><span class="p">(</span><span class="n">passphrase</span> <span class="o">+</span> <span class="n">q</span><span class="p">,</span> <span class="n">SIZE_MAX</span><span class="p">);</span>  <span class="o">&lt;===</span> <span class="n">integer</span> <span class="n">overflow</span>
  <span class="k">if</span> <span class="p">(</span><span class="n">z</span> <span class="o">==</span> <span class="mi">0</span><span class="p">)</span> <span class="p">{</span>
    <span class="n">q</span> <span class="o">=</span> <span class="n">SIZE_MAX</span><span class="p">;</span> <span class="cm">/* Invalid UTF8! */</span>
    <span class="k">break</span><span class="p">;</span>
  <span class="p">}</span>

  <span class="k">if</span> <span class="p">(</span><span class="n">q</span> <span class="o">+</span> <span class="n">z</span> <span class="o">&gt;=</span> <span class="n">p</span><span class="p">)</span> <span class="cm">/* This one brings us over the edge */</span>
    <span class="k">break</span><span class="p">;</span>

  <span class="n">q</span> <span class="o">+=</span> <span class="n">z</span><span class="p">;</span>  <span class="o">&lt;===</span> <span class="n">subtracts</span> <span class="mi">22</span> <span class="n">from</span> <span class="n">q</span><span class="p">,</span> <span class="n">causing</span> <span class="n">infinite</span> <span class="n">loop</span>
<span class="p">}</span>
</code></pre></div></div>

<p>The integer overflow happens when <code class="language-plaintext highlighter-rouge">utf8_encoded_valid_unichar</code> returns an error code. The error code is a negative number: -22. This overflows when it is assigned to <code class="language-plaintext highlighter-rouge">z</code> (type <code class="language-plaintext highlighter-rouge">size_t</code>). This can cause an infinite loop if the value of <code class="language-plaintext highlighter-rouge">q</code> is 22 or larger.</p>

<p>To reproduce the bug, you need to run <code class="language-plaintext highlighter-rouge">systemd-ask-password</code> and enter an invalid unicode character, followed by a backspace character. The reproduction steps below use a simple C program to generate the sequence of characters and <code class="language-plaintext highlighter-rouge">ssh</code> to feed them into the tty.</p>

<p>First build the C program:</p>

<div class="language-bash highlighter-rouge"><div class="highlight"><pre class="highlight"><code>gcc print_passphrase.c <span class="nt">-o</span> print_passphrase
</code></pre></div></div>

<p>Now use <code class="language-plaintext highlighter-rouge">ssh</code> to feed the malicious passphrase into <code class="language-plaintext highlighter-rouge">systemd-ask-password</code> via a tty:</p>

<div class="language-bash highlighter-rouge"><div class="highlight"><pre class="highlight"><code>./print_passphrase | ssh <span class="nt">-tt</span> localhost systemd-ask-password
</code></pre></div></div>

<p>Now run <code class="language-plaintext highlighter-rouge">top</code>. If the proof of concept is successful then it will show that <code class="language-plaintext highlighter-rouge">systemd-ask-password</code> is consuming 100% of a CPU core. Note: the reproduction steps work best if you have <code class="language-plaintext highlighter-rouge">ssh-agent</code> or another key manager running so that <code class="language-plaintext highlighter-rouge">ssh</code> doesn’t need to ask you for your password.</p>

<h4 id="impact">Impact</h4>

<p>This issue may lead to local denial of service.</p>

<h2 id="credit">Credit</h2>

<p>This issue was discovered and reported by GHSL team member <a href="https://github.com/kevinbackhouse">@kevinbackhouse (Kevin Backhouse)</a>.</p>

<h2 id="contact">Contact</h2>

<p>You can contact the GHSL team at <code class="language-plaintext highlighter-rouge">securitylab@github.com</code>, please include a reference to <code class="language-plaintext highlighter-rouge">GHSL-2021-052</code> in any communication regarding this issue.</p