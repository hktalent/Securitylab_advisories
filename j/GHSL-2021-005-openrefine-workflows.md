<header class="post-header d-block mb-6">
      <div class="date text-mono f5 my-3">May 4, 2021</div>
      <h1 class="my-2 h00-mktg lh-condensed">GHSL-2021-005: Unauthorized repository modification or secrets exfiltration in GitHub workflows of OpenRefine</h1>

      
      
      
      
      

      

      <a target="_blank" class="sc-frDJqD SgxRc d-inline-flex flex-row flex-items-center text-gray" href="https://github.com/jarlob">
        <img class="mr-3" src="https://avatars.githubusercontent.com/u/26652396?s=35" height="35" width="35">
        <span>Jaroslav Lobacevski</span>
      </a>
    </header>

    <main id="content" class="markdown-body" aria-label="Content">
      
<h2 id="coordinated-disclosure-timeline">Coordinated Disclosure Timeline</h2>

<ul>
  <li>2021-01-18: Issue reported to maintainers</li>
  <li>2021-01-18: Issue acknowledged</li>
  <li>2021-01-23: Asked the maintainers for status update</li>
  <li>2021-04-21: Asked the maintainers for status update</li>
  <li>2021-04-22: Partial mitigation applied</li>
</ul>

<h2 id="summary">Summary</h2>

<p>The <a href="https://github.com/OpenRefine/OpenRefine/blob/master/.github/workflows/pull_request.yml">pull_request.yml</a> GitHub workflow is vulnerable to unauthorized modification of the base repository or secrets exfiltration from a Pull Request.</p>

<h2 id="product">Product</h2>

<p><a href="https://github.com/OpenRefine/OpenRefine">OpenRefine/OpenRefine</a> repository</p>

<h2 id="tested-version">Tested Version</h2>

<p>The latest changeset of <a href="https://github.com/OpenRefine/OpenRefine/blob/ab91d8adcf44104e311dc25a2ad3413e32a11aed/.github/workflows/pull_request.yml">pull_request.yml</a> to the date.</p>

<h2 id="details">Details</h2>

<h3 id="issue-untrusted-code-is-explicitly-checked-out-and-run-on-a-pull-request-from-a-fork">Issue: Untrusted code is explicitly checked out and run on a Pull Request from a fork</h3>

<p>Workflows triggered on <code class="language-plaintext highlighter-rouge">pull_request_target</code> have read/write tokens for the base repository and the access to secrets. By explicitly checking out and running the build script from a fork the untrusted code is running in an environment that is able to push to the base repository and to access secrets. More details can be found in the article <a href="https://securitylab.github.com/research/github-actions-preventing-pwn-requests/">Keeping your GitHub Actions and workflows secure: Preventing pwn requests</a>.</p>

<div class="language-yaml highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="na">on</span><span class="pi">:</span>
  <span class="na">pull_request_target</span><span class="pi">:</span>
    <span class="na">paths-ignore</span><span class="pi">:</span>
      <span class="pi">-</span> <span class="s1">'</span><span class="s">docs/**'</span>
<span class="nn">...</span>
    <span class="pi">-</span> <span class="na">uses</span><span class="pi">:</span> <span class="s">actions/checkout@v2.3.4</span>
      <span class="na">with</span><span class="pi">:</span>
        <span class="na">ref</span><span class="pi">:</span> <span class="s">${{ github.event.pull_request.head.ref }}</span>
        <span class="na">repository</span><span class="pi">:</span> <span class="s">${{ github.event.pull_request.head.repo.full_name }}</span>
<span class="nn">...</span>
    <span class="pi">-</span> <span class="na">name</span><span class="pi">:</span> <span class="s">Build and test with Maven</span>
      <span class="na">run</span><span class="pi">:</span> <span class="s">mvn jacoco:prepare-agent test</span>
<span class="nn">...</span>
    <span class="pi">-</span> <span class="na">uses</span><span class="pi">:</span> <span class="s">actions/checkout@v2.3.4</span>
      <span class="na">with</span><span class="pi">:</span>
        <span class="na">ref</span><span class="pi">:</span> <span class="s">${{ github.event.pull_request.head.ref }}</span>
        <span class="na">repository</span><span class="pi">:</span> <span class="s">${{ github.event.pull_request.head.repo.full_name }}</span>
<span class="nn">...</span>
    <span class="pi">-</span> <span class="na">name</span><span class="pi">:</span> <span class="s">Build OpenRefine</span>
      <span class="na">run</span><span class="pi">:</span> <span class="s">./refine build</span>
</code></pre></div></div>

<h4 id="impact">Impact</h4>

<p>The vulnerability allows for unauthorized modification of the base repository and secrets exfiltration.</p>

<h2 id="credit">Credit</h2>

<p>This issue was discovered and reported by GHSL team member <a href="https://github.com/JarLob">@JarLob (Jaroslav Loba??evski)</a>.</p>

<h2 id="contact">Contact</h2>

<p>You can contact the GHSL team at <code class="language-plaintext highlighter-rouge">securitylab@github.com</code>, please include a reference to <code class="language-plaintext highlighter-rouge">GHSL-2021-005</code> in any communication regarding this issue.</p>


   