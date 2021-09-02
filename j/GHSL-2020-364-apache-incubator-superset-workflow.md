<header class="post-header d-block mb-6">
      <div class="date text-mono f5 my-3">July 21, 2021</div>
      <h1 class="my-2 h00-mktg lh-condensed">GHSL-2020-364: Unauthorized repository modification or secrets exfiltration in GitHub workflows of apache/camel-website</h1>

      
      
      
      
      

      

      <a target="_blank" class="sc-frDJqD SgxRc d-inline-flex flex-row flex-items-center text-gray" href="https://github.com/jarlob">
        <img class="mr-3" src="https://avatars.githubusercontent.com/u/26652396?s=35" height="35" width="35">
        <span>Jaroslav Lobacevski</span>
      </a>
    </header>

    <main id="content" class="markdown-body" aria-label="Content">
      
<h2 id="coordinated-disclosure-timeline">Coordinated Disclosure Timeline</h2>

<ul>
  <li>2020-12-21: Issue reported to the Apache security team.</li>
  <li>2021-01-25: Issue acknowledged.</li>
  <li>2021-01-25: Apache/Camel-Website was added to the report.</li>
  <li>2021-02-23: Asked for status update. Notified that Camel-Website repo is not fixed.</li>
  <li>2021-03-22: Disclosure deadline reached.</li>
  <li>2021-03-24: Asked for status update.</li>
  <li>2021-04-29: The Camel team responded they just received the report 2021-04-28 6:58UTC</li>
  <li>2021-04-29: Issue was fixed.</li>
</ul>

<h2 id="summary">Summary</h2>

<p>The <a href="https://github.com/apache/camel-website/blob/pr/image-optimization/.github/workflows/pr.yaml">pr.yaml</a> GitHub workflow is vulnerable to unauthorized modification of the base repository or secrets exfiltration from a Pull Request.</p>

<h2 id="product">Product</h2>

<p><a href="https://github.com/apache/camel-website">apache/camel-website</a> GitHub repository</p>

<h2 id="tested-version">Tested Version</h2>

<p>The latest changeset <a href="https://github.com/apache/camel-website/blob/52c23b5b8320967736ebfbc200c4f31fa3658067/.github/workflows/pr.yaml">52c23b5</a> to the date.</p>

<h2 id="details">Details</h2>

<h3 id="issue-untrusted-code-is-explicitly-checked-out-and-run-on-a-pull-request-from-a-fork">Issue: Untrusted code is explicitly checked out and run on a Pull Request from a fork</h3>

<p>Workflows triggered on <code class="language-plaintext highlighter-rouge">pull_request_target</code> have read/write tokens for the base repository and access to secrets. By explicitly checking out and running the build script from a fork the untrusted code is running in an environment that is able to push to the base repository and to access secrets. More details can be found in the article <a href="https://securitylab.github.com/research/github-actions-preventing-pwn-requests/">Keeping your GitHub Actions and workflows secure: Preventing pwn requests</a>.</p>

<p><em>pr.yaml:</em></p>
<div class="language-yaml highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="na">on</span><span class="pi">:</span> <span class="s">pull_request_target</span>
<span class="nn">...</span>
      <span class="pi">-</span> <span class="na">uses</span><span class="pi">:</span> <span class="s">actions/checkout@v2</span>
        <span class="na">with</span><span class="pi">:</span>
          <span class="na">ref</span><span class="pi">:</span> <span class="s">${{ github.event.pull_request.head.sha }}</span>
          <span class="na">persist-credentials</span><span class="pi">:</span> <span class="no">false</span>
      <span class="pi">-</span> <span class="na">name</span><span class="pi">:</span> <span class="s">Build</span>
        <span class="na">run</span><span class="pi">:</span> <span class="s">yarn build-all</span>
</code></pre></div></div>

<p>Since the used package.json is controlled by the Pull Request creator it allows arbitrary code execution.</p>

<h4 id="impact">Impact</h4>

<p>The vulnerability allows for unauthorized modification of the base repository and secrets exfiltration.</p>

<h2 id="credit">Credit</h2>

<p>This issue was discovered and reported by GHSL team member <a href="https://github.com/JarLob">@JarLob (Jaroslav Lobačevski)</a>.</p>

<h2 id="contact">Contact</h2>

<p>You can contact the GHSL team at <code class="language-plaintext highlighter-rouge">securitylab@github.com</code>, please include a reference to <code class="language-plaintext highlighter-rouge">GHSL-2020-364</code> in any communication regarding this issue.</p>


   