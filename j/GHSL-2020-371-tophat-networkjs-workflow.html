<header class="post-header d-block mb-6">
      <div class="date text-mono f5 my-3">February 3, 2021</div>
      <h1 class="my-2 h00-mktg lh-condensed">GHSL-2020-371: Arbitrary code execution in tophat workflows</h1>

      
      
      
      
      

      

      <a target="_blank" class="sc-frDJqD SgxRc d-inline-flex flex-row flex-items-center text-gray" href="https://github.com/jarlob">
        <img class="mr-3" src="https://avatars.githubusercontent.com/u/26652396?s=35" height="35" width="35">
        <span>Jaroslav Lobacevski</span>
      </a>
    </header>

    <main id="content" class="markdown-body" aria-label="Content">
      <h2 id="coordinated-disclosure-timeline">Coordinated Disclosure Timeline</h2>

<ul>
  <li>2020-12-22: Report sent to vendor.</li>
  <li>2021-01-18: Issue partially fixed.</li>
  <li>2021-01-25: Vendor acknowledges report receipt and informs about the fix.</li>
  <li>2021-01-25: Information about the not fixed parts sent.</li>
  <li>2021-01-25: Issue resolved.</li>
</ul>

<h2 id="summary">Summary</h2>

<p>The GitHub workflows <code class="language-plaintext highlighter-rouge">pull-request.yml</code> in multiple branches of <a href="https://github.com/tophat/networkjs">tophat/networkjs</a>, <a href="https://github.com/tophat/commit-utils">tophat/commit-utils</a>, <a href="https://github.com/tophat/commit-watch">tophat/commit-watch</a>, <a href="https://github.com/tophat/sanity-runner">tophat/sanity-runner</a> and <code class="language-plaintext highlighter-rouge">commit-watch.yml</code> in <a href="https://github.com/tophat/commit-watch">tophat/commit-watch</a> are vulnerable to unauthorized modification of the base repository or secrets exfiltration from a Pull Request.</p>

<h2 id="product">Product</h2>

<p><a href="https://github.com/tophat/networkjs">tophat/networkjs</a> GitHub repository<br />
<a href="https://github.com/tophat/commit-utils">tophat/commit-utils</a> GitHub repository<br />
<a href="https://github.com/tophat/commit-watch">tophat/commit-watch</a> GitHub repository<br />
<a href="https://github.com/tophat/sanity-runner">tophat/sanity-runner</a> GitHub repository</p>

<h2 id="tested-version">Tested Version</h2>

<p>The latest versions to the date.</p>

<h2 id="details">Details</h2>

<h3 id="issue-untrusted-code-is-explicitly-checked-out-and-run-on-a-pull-request-from-a-fork">Issue: Untrusted code is explicitly checked out and run on a Pull Request from a fork</h3>

<p>Workflows triggered on <code class="language-plaintext highlighter-rouge">pull_request_target</code> have read/write tokens for the base repository and the access to secrets. By explicitly checking out and running the build script from a fork the untrusted code is running in an environment that is able to push to the base repository and to access secrets. More details can be found in the article <a href="https://securitylab.github.com/research/github-actions-preventing-pwn-requests/">Keeping your GitHub Actions and workflows secure: Preventing pwn requests</a>.</p>

<div class="language-yaml highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="na">on</span><span class="pi">:</span>
  <span class="pi">-</span> <span class="s">pull_request_target</span>
<span class="nn">...</span>
        <span class="pi">-</span> <span class="na">uses</span><span class="pi">:</span> <span class="s">actions/checkout@v2</span>
          <span class="na">with</span><span class="pi">:</span>
            <span class="na">ref</span><span class="pi">:</span> <span class="s">${{ github.event.pull_request.head.sha }}</span>
        <span class="pi">-</span> <span class="na">uses</span><span class="pi">:</span> <span class="s">./.github/actions/detect-node</span>
<span class="nn">...</span>
        <span class="pi">-</span> <span class="na">name</span><span class="pi">:</span> <span class="s">Install dependencies</span>
          <span class="na">run</span><span class="pi">:</span> <span class="s">yarn install --immutable</span>
        <span class="pi">-</span> <span class="na">name</span><span class="pi">:</span> <span class="s">Linting</span>
          <span class="na">run</span><span class="pi">:</span> <span class="s">yarn lint:ci</span>
        <span class="pi">-</span> <span class="na">name</span><span class="pi">:</span> <span class="s">Tests</span>
          <span class="na">run</span><span class="pi">:</span> <span class="s">yarn test:ci</span>
<span class="nn">...</span>
</code></pre></div></div>

<h4 id="impact">Impact</h4>

<p>The vulnerability allows for unauthorized modification of the base repository and secrets exfiltration.</p>

<h2 id="credit">Credit</h2>

<p>This issue was discovered and reported by GHSL team member <a href="https://github.com/JarLob">@JarLob (Jaroslav Lobačevski)</a>.</p>

<h2 id="contact">Contact</h2>

<p>You can contact the GHSL team at <code class="language-plaintext highlighter-rouge">securitylab@github.com</code>, please include a reference to <code class="language-plaintext highlighter-rouge">GHSL-2020-371</code> in any communication regarding this issue.</p>

   