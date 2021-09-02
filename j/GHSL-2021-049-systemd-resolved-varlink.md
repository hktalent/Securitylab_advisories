<header class="post-header d-block mb-6">
      <div class="date text-mono f5 my-3">March 25, 2021</div>
      <h1 class="my-2 h00-mktg lh-condensed">GHSL-2021-049: Type confusion vulnerability in the varlink interface of systemd-resolved</h1>

      
      
      
      
      

      

      <a target="_blank" class="sc-frDJqD SgxRc d-inline-flex flex-row flex-items-center text-gray" href="https://github.com/kevinbackhouse">
        <img class="mr-3" src="https://avatars.githubusercontent.com/u/4358136?s=35" height="35" width="35">
        <span>Kevin Backhouse</span>
      </a>
    </header>

    <main id="content" class="markdown-body" aria-label="Content">
      <h2 id="coordinated-disclosure-timeline">Coordinated Disclosure Timeline</h2>
<ul>
  <li>2021-02-18: Emailed report and PoC to systemd-security@redhat.com</li>
  <li>2021-02-19: Reply from Lennart Poettering: <em>This issue was already <a href="https://github.com/systemd/systemd/pull/18248">reported</a> and <a href="https://github.com/systemd/systemd/pull/18328">fixed</a>, although it was not declared a security issue</em>.</li>
</ul>

<h2 id="summary">Summary</h2>

<p>There is a potential type confusion vulnerability in the varlink interface of systemd-resolved. This is due to the <code class="language-plaintext highlighter-rouge">userdata</code> field of the <code class="language-plaintext highlighter-rouge">Varlink</code> struct being used to store two unrelated datatypes: <code class="language-plaintext highlighter-rouge">Manager</code> and <code class="language-plaintext highlighter-rouge">DnsQuery</code>.</p>

<h2 id="product">Product</h2>

<p>systemd-resolved</p>

<h2 id="tested-version">Tested Version</h2>

<p>systemd v247.3-1  (tested on Arch Linux)</p>

<p>Note: the new varlink interface to systemd-resolved has only been added quite recently. Many Linux distributions ship with older versions of systemd which do not include the new interface. However, Arch Linux ships with v247, which includes it.</p>

<h2 id="details">Details</h2>

<h3 id="issue-1-type-confusion-in-systemd-resolved-varlink-interface-ghsl-2021-049">Issue 1: Type confusion in systemd-resolved varlink interface (<code class="language-plaintext highlighter-rouge">GHSL-2021-049</code>)</h3>

<p>The <code class="language-plaintext highlighter-rouge">Varlink</code> struct has a <code class="language-plaintext highlighter-rouge">void*</code> field named <a href="https://github.com/systemd/systemd/blob/4d484e14bb9864cef1d124885e625f33bf31e91c/src/shared/varlink.c#L142"><code class="language-plaintext highlighter-rouge">userdata</code></a>.
The varlink interface of systemd-resolved initially uses this field to store a pointer to the <code class="language-plaintext highlighter-rouge">Manager</code> object (<a href="https://github.com/systemd/systemd/blob/4d484e14bb9864cef1d124885e625f33bf31e91c/src/resolve/resolved-varlink.c#L515">resolved-varlink.c, line 515</a>):</p>

<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="n">varlink_server_set_userdata</span><span class="p">(</span><span class="n">s</span><span class="p">,</span> <span class="n">m</span><span class="p">);</span>
</code></pre></div></div>

<p>But, later, the <code class="language-plaintext highlighter-rouge">userdata</code> field is used to store a pointer to the <code class="language-plaintext highlighter-rouge">DnsQuery</code> object (<a href="https://github.com/systemd/systemd/blob/4d484e14bb9864cef1d124885e625f33bf31e91c/src/resolve/resolved-varlink.c#L318">resolved-varlink.c, line 318</a> and <a href="https://github.com/systemd/systemd/blob/4d484e14bb9864cef1d124885e625f33bf31e91c/src/resolve/resolved-varlink.c#L485">resolved-varlink.c, line 485</a>):</p>

<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="n">varlink_set_userdata</span><span class="p">(</span><span class="n">link</span><span class="p">,</span> <span class="n">q</span><span class="p">);</span>
</code></pre></div></div>

<p>It looks like the code was written with the assumption that the <code class="language-plaintext highlighter-rouge">Varlink</code> object will only survive for the duration of single request, so the change of the type of the <code class="language-plaintext highlighter-rouge">userdata</code> field won’t cause a problem. However, if two varlink requests are received in quick succession then the same <code class="language-plaintext highlighter-rouge">Varlink</code> object is reused, potentially leading to a type confusion vulnerability.</p>

<p>To reproduce the issue, please build the attached proof-of-concept as follows:</p>

<div class="language-bash highlighter-rouge"><div class="highlight"><pre class="highlight"><code>gcc varlink_resolve.c <span class="nt">-o</span> varlink_resolve
</code></pre></div></div>

<p>You might also need to start systemd-resolved if it isn’t already running:</p>

<div class="language-bash highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="nb">sudo </span>systemctl start systemd-resolved
</code></pre></div></div>

<p>The PoC has two modes, to test the <code class="language-plaintext highlighter-rouge">io.systemd.Resolve.ResolveHostname</code> and <code class="language-plaintext highlighter-rouge">io.systemd.Resolve.ResolveAddress</code> interfaces, respectively:</p>

<div class="language-bash highlighter-rouge"><div class="highlight"><pre class="highlight"><code>./varlink_resolve <span class="nb">hostname </span>www.github.com
./varlink_resolve address 127.0.0.1
</code></pre></div></div>

<p>Both those commands cause systemd-resolved to crash.</p>

<p>In our testing, systemd-resolved always crashes due to the <code class="language-plaintext highlighter-rouge">userdata</code> field containing a NULL pointer, which triggers an assertion failure at <a href="https://github.com/systemd/systemd/blob/4d484e14bb9864cef1d124885e625f33bf31e91c/src/resolve/resolved-varlink.c#L277">resolved-varlink.c, line 277</a> or <a href="https://github.com/systemd/systemd/blob/4d484e14bb9864cef1d124885e625f33bf31e91c/src/resolve/resolved-varlink.c#L455">resolved-varlink.c, line 455</a>. We are not sure why we have never seen a crash due to the <code class="language-plaintext highlighter-rouge">userdata</code> field containing a pointer to a <code class="language-plaintext highlighter-rouge">DnsQuery</code> object. The code is invoked by an epoll event handler, which suggests that the behavior should be non-deterministic, based on the order in which the events are received. If the events are handled in a different order then we believe it will lead to a type confusion rather than a NULL pointer error.</p>

<h4 id="impact">Impact</h4>

<p>This issue may lead to a memory corruption, which could enable a local attacker to gain code execution as the systemd-resolve user.</p>

<h2 id="credit">Credit</h2>

<p>This issue was discovered and reported by GHSL team member <a href="https://github.com/kevinbackhouse">@kevinbackhouse (Kevin Backhouse)</a>.</p>

<h2 id="contact">Contact</h2>

<p>You can contact the GHSL team at <code class="language-plaintext highlighter-rouge">securitylab@github.com</code>, please include a reference to <code class="language-plaintext highlighter-rouge">GHSL-2021-049</code> in any communication regarding this issue.</p>

