<header class="post-header d-block mb-6">
      <div class="date text-mono f5 my-3">September 2, 2020</div>
      <h1 class="my-2 h00-mktg lh-condensed">GHSL-2020-133: Path traversal vulnerability in Adobe git-server - CVE-2020-9708</h1>

      
      
      
      
      

      

      <a target="_blank" class="sc-frDJqD SgxRc d-inline-flex flex-row flex-items-center text-gray" href="https://github.com/jarlob">
        <img class="mr-3" src="https://avatars.githubusercontent.com/u/26652396?s=35" height="35" width="35">
        <span>Jaroslav Lobacevski</span>
      </a>
    </header>

    <main id="content" class="markdown-body" aria-label="Content">
      <h2 id="summary">Summary</h2>

<p>Malicious users may access any Git repository on the server even if it is outside the served root directory.</p>

<h2 id="product">Product</h2>
<p><a href="https://github.com/adobe/git-server">git-server</a></p>

<h2 id="tested-version">Tested Version</h2>
<p>Master branch. Windows OS (should work on Linux too).</p>

<h2 id="details">Details</h2>

<h3 id="function-resolverepositorypath-doesnt-validate-user-input">Function <a href="https://github.com/adobe/git-server/blob/31a5c5713e1b07d8f0a4c06427d43804973ca14b/lib/utils.js#L29">resolveRepositoryPath</a> doesn’t validate user input</h3>

<p><code class="language-plaintext highlighter-rouge">git-server</code> serves Git repositories over http(s) from a configured root directory <code class="language-plaintext highlighter-rouge">repoRoot</code>. The only option to access repositories outside the <code class="language-plaintext highlighter-rouge">repoRoot</code> is to set ‘virtual’ repository paths in the server configuration file.</p>

<p>However <code class="language-plaintext highlighter-rouge">resolveRepositoryPath</code> doesn’t properly validate user input and a malicious user may traverse to any valid Git repository outside the <code class="language-plaintext highlighter-rouge">repoRoot</code>.</p>

<h4 id="impact">Impact</h4>

<p>This issue may lead to an unauthorized access to private Git repositories.</p>

<h2 id="cve">CVE</h2>

<p>CVE-2020-9708</p>

<h2 id="coordinated-disclosure-timeline">Coordinated Disclosure Timeline</h2>
<ul>
  <li>09/07/2020: Report sent to Vendor</li>
  <li>09/07/2020: Vendor acknowledges</li>
  <li>23/07/2020: Fixed in v1.3.1</li>
  <li>11/08/2020: CVE-2020-9708 assigned.</li>
  <li>11/08/2020: <a href="https://github.com/adobe/git-server/security/advisories/GHSA-cgj4-x2hh-2x93">Advisory</a> released.</li>
</ul>

<h2 id="credit">Credit</h2>

<p>This issue was discovered and reported by GHSL team member <a href="https://github.com/JarLob">@JarLob (Jaroslav Lobačevski)</a>.</p>

<h2 id="contact">Contact</h2>

<p>You can contact the GHSL team at <code class="language-plaintext highlighter-rouge">securitylab@github.com</code>, please include a reference to <code class="language-plaintext highlighter-rouge">GHSL-2020-133</code> in any communication regarding this issue.<