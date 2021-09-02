<header class="post-header d-block mb-6">
      <div class="date text-mono f5 my-3">March 3, 2021</div>
      <h1 class="my-2 h00-mktg lh-condensed">GHSL-2021-008: Unauthorized repository modification or secrets exfiltration in a GitHub workflow of actions-cool/issue-helper</h1>

      
      
      
      
      

      

      <a target="_blank" class="sc-frDJqD SgxRc d-inline-flex flex-row flex-items-center text-gray" href="https://github.com/jarlob">
        <img class="mr-3" src="https://avatars.githubusercontent.com/u/26652396?s=35" height="35" width="35">
        <span>Jaroslav Lobacevski</span>
      </a>
    </header>

    <main id="content" class="markdown-body" aria-label="Content">
      <h2 id="coordinated-disclosure-timeline">Coordinated Disclosure Timeline</h2>

<ul>
  <li>2021-01-18: Issue reported to maintainers</li>
  <li>2021-02-23: Issue fixed</li>
</ul>

<h2 id="summary">Summary</h2>

<p>The <a href="https://github.com/actions-cool/issues-helper/blob/main/.github/workflows/surge-preview.yml">surge-preview.yml</a> GitHub workflow is vulnerable to unauthorized modification of the base repository or secrets exfiltration from a Pull Request.</p>

<h2 id="product">Product</h2>

<p><a href="https://github.com/actions-cool/issues-helper">actions-cool/issues-helper GitHub repository</a></p>

<h2 id="tested-version">Tested Version</h2>

<p>The latest changeset <a href="https://github.com/actions-cool/issues-helper/blob/5e251408e143a394b6cb09545111463a5b6d9656/.github/workflows/surge-preview.yml">surge-preview.yml</a> to the date.</p>

<h2 id="details">Details</h2>

<h3 id="issue-untrusted-code-is-explicitly-checked-out-and-run-on-a-pull-request-from-a-fork">Issue: Untrusted code is explicitly checked out and run on a Pull Request from a fork</h3>

<p>Workflows triggered on <code class="language-plaintext highlighter-rouge">pull_request_target</code> have read/write tokens for the base repository and the access to secrets. By explicitly checking out and running the build script from a fork the untrusted code is running in an environment that is able to push to the base repository and to access secrets. More details can be found in the article <a href="https://securitylab.github.com/research/github-actions-preventing-pwn-requests/">Keeping your GitHub Actions and workflows secure: Preventing pwn requests</a>.</p>

<div class="language-yaml highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="na">on</span><span class="pi">:</span> <span class="s">pull_request_target</span>
<span class="nn">...</span>
      <span class="pi">-</span> <span class="na">uses</span><span class="pi">:</span> <span class="s">actions/checkout@v2</span>
        <span class="na">with</span><span class="pi">:</span>
          <span class="na">ref</span><span class="pi">:</span> <span class="s">refs/pull/${{ github.event.pull_request.number }}/merge</span>
      <span class="pi">-</span> <span class="na">uses</span><span class="pi">:</span> <span class="s">afc163/surge-preview@v1</span>
        <span class="na">with</span><span class="pi">:</span>
          <span class="na">surge_token</span><span class="pi">:</span> <span class="s">${{ secrets.SURGE_TOKEN }}</span>
          <span class="na">github_token</span><span class="pi">:</span> <span class="s">${{ secrets.GITHUB_TOKEN }}</span>
          <span class="na">build</span><span class="pi">:</span> <span class="pi">|</span>
            <span class="s">yarn</span>
            <span class="s">yarn docs-dev:build</span>
          <span class="na">dist</span><span class="pi">:</span> <span class="s">docs-dist</span>
          <span class="na">teardown</span><span class="pi">:</span> <span class="s1">'</span><span class="s">true'</span>
<span class="nn">...</span>
</code></pre></div></div>

<h4 id="impact">Impact</h4>

<p>The vulnerability allows for unauthorized modification of the base repository and secrets exfiltration.</p>

<h2 id="credit">Credit</h2>

<p>This issue was discovered and reported by GHSL team member <a href="https://github.com/JarLob">@JarLob (Jaroslav Lobačevski)</a>.</p>

<h2 id="contact">Contact</h2>

<p>You can contact the GHSL team at <code class="language-plaintext highlighter-rouge">securitylab@github.com</code>, please include a reference to <code class="language-plaintext highlighter-rouge">GHSL-2021-008</code> in any communication regarding this issue.</p>

   