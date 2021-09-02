<header class="post-header d-block mb-6">
      <div class="date text-mono f5 my-3">February 3, 2021</div>
      <h1 class="my-2 h00-mktg lh-condensed">GHSL-2020-146: Arbitrary file overwrite, Cross-Site Scripting (XSS) and Cross-Site Request Forgery (CSRF) in dotnet-architecture/eShopOnWeb</h1>

      
      
      
      
      

      

      <a target="_blank" class="sc-frDJqD SgxRc d-inline-flex flex-row flex-items-center text-gray" href="https://github.com/jarlob">
        <img class="mr-3" src="https://avatars.githubusercontent.com/u/26652396?s=35" height="35" width="35">
        <span>Jaroslav Lobacevski</span>
      </a>
    </header>

    <main id="content" class="markdown-body" aria-label="Content">
      <h2 id="coordinated-disclosure-timeline">Coordinated Disclosure Timeline</h2>

<ul>
  <li>09/11/2020: Report sent to vendor</li>
  <li>09/11/2020: Vendor acknowledges report receipt</li>
  <li>12/11/2020: Asked for update. No response.</li>
  <li>01/26/2021: Public issue created https://github.com/dotnet-architecture/eShopOnWeb/issues/500</li>
</ul>

<h2 id="summary">Summary</h2>

<p><a href="https://github.com/dotnet-architecture/eShopOnWeb">eShopOnWeb</a> is vulnerable to an Arbitrary File Overwrite, Cross-Site Scripting (XSS) and Cross-Site Request Forgery (CSRF) that may lead to the elevation of privileges, per-user denial of service (DoS) and Remote Code Execution (RCE).</p>

<h2 id="product">Product</h2>

<p><a href="https://github.com/dotnet-architecture/eShopOnWeb">eShopOnWeb</a></p>

<h2 id="tested-version">Tested Version</h2>

<p>Master branch.</p>

<h2 id="details">Details</h2>

<h3 id="issue-1-arbitrary-file-overwrite">Issue 1: Arbitrary file overwrite</h3>
<p><a href="https://github.com/dotnet-architecture/eShopOnWeb/blob/4e935df31150783d218e807ac6ed1a389b0b98cb/src/Web/Controllers/FileController.cs#L15">The <code class="language-plaintext highlighter-rouge">Upload</code> action in <code class="language-plaintext highlighter-rouge">FileController</code></a> doesn’t properly validate the <code class="language-plaintext highlighter-rouge">FileName</code> in <code class="language-plaintext highlighter-rouge">FileViewModel fileViewModel</code>. It is used later to build the destination path:</p>
<div class="language-cs highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="kt">var</span> <span class="n">fullPath</span> <span class="p">=</span> <span class="n">Path</span><span class="p">.</span><span class="nf">Combine</span><span class="p">(</span><span class="n">Directory</span><span class="p">.</span><span class="nf">GetCurrentDirectory</span><span class="p">(),</span> <span class="s">@"wwwroot/images/products"</span><span class="p">,</span> <span class="n">fileViewModel</span><span class="p">.</span><span class="n">FileName</span><span class="p">);</span>
</code></pre></div></div>
<p>This can be bypassed in multiple ways:</p>
<ol>
  <li>By using <code class="language-plaintext highlighter-rouge">../</code> in the <code class="language-plaintext highlighter-rouge">FileName</code>.</li>
  <li>By using full path in the <code class="language-plaintext highlighter-rouge">FileName</code>.</li>
</ol>

<p>As a result the attacker controls the file that will be ovewritten:</p>
<div class="language-cs highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="kt">var</span> <span class="n">fullPath</span> <span class="p">=</span> <span class="n">Path</span><span class="p">.</span><span class="nf">Combine</span><span class="p">(</span><span class="n">Directory</span><span class="p">.</span><span class="nf">GetCurrentDirectory</span><span class="p">(),</span> <span class="s">@"wwwroot/images/products"</span><span class="p">,</span> <span class="n">fileViewModel</span><span class="p">.</span><span class="n">FileName</span><span class="p">);</span>
<span class="k">if</span> <span class="p">(</span><span class="n">System</span><span class="p">.</span><span class="n">IO</span><span class="p">.</span><span class="n">File</span><span class="p">.</span><span class="nf">Exists</span><span class="p">(</span><span class="n">fullPath</span><span class="p">))</span>
<span class="p">{</span>
    <span class="n">System</span><span class="p">.</span><span class="n">IO</span><span class="p">.</span><span class="n">File</span><span class="p">.</span><span class="nf">Delete</span><span class="p">(</span><span class="n">fullPath</span><span class="p">);</span>
<span class="p">}</span>
<span class="n">System</span><span class="p">.</span><span class="n">IO</span><span class="p">.</span><span class="n">File</span><span class="p">.</span><span class="nf">WriteAllBytes</span><span class="p">(</span><span class="n">fullPath</span><span class="p">,</span> <span class="n">fileData</span><span class="p">);</span>
</code></pre></div></div>

<h4 id="impact">Impact</h4>

<p>This issue may lead to RCE as it is possible to overwrite executable files as long as the running application has sufficient privileges.</p>

<h3 id="issue-2-xss-cve-2018-0784">Issue 2: XSS (CVE-2018-0784)</h3>
<p>The application doesn’t have a fix for <a href="https://github.com/aspnet/Announcements/issues/285">CVE-2018-0784</a> that was found in ASP.NET Core templates. It is vulnerable to XSS if the logged-in user is tricked into clicking a malicious link like <code class="language-plaintext highlighter-rouge">https://localhost:44315/manage/enable-authenticator?AuthenticatorUri=%22%3E%3C/div%3E%00%00%00%00%00%00%00%3Cscript%3Ealert(%22XSS%22)%3C/script%3E</code> and enters an invalid verification code. More details are available in <a href="https://kevinchalet.com/2018/01/09/why-you-should-never-use-html-raw-in-your-razor-views/">this blog post</a>.</p>

<h4 id="impact-1">Impact</h4>

<p>This issue may lead to the elevation of privileges.</p>

<h3 id="issue-3-csrf-cve-2018-0785">Issue 3: CSRF (CVE-2018-0785)</h3>
<p>The application doesn’t have a fix for <a href="https://github.com/aspnet/Announcements/issues/284">CVE-2018-0785</a> that was found in ASP.NET Core templates. It is vulnerable to CSRF. A logged-in user with enabled Second Factor Authentication (2FA) may lose their recovery codes if they are tricked into clicking a link like <code class="language-plaintext highlighter-rouge">https://localhost:44315/manage/Generate-Recovery-Codes</code> or visit a malicious site that makes the request without the user’s consent. As a result the user may be permanently locked out of their account after losing access to their 2FA device, as the initial recovery codes would no longer be valid.</p>

<h4 id="impact-2">Impact</h4>

<p>This issue may lead to a per-user DoS.</p>

<h2 id="credit">Credit</h2>

<p>This issue was discovered and reported by GHSL team member <a href="https://github.com/JarLob">@JarLob (Jaroslav Lobačevski)</a>.</p>

<h2 id="contact">Contact</h2>

<p>You can contact the GHSL team at <code class="language-plaintext highlighter-rouge">securitylab@github.com</code>, please include a reference to <code class="language-plaintext highlighter-rouge">GHSL-2020-146</code> in any communication regarding this issue.<