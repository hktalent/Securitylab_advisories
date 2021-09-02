<header class="post-header d-block mb-6">
      <div class="date text-mono f5 my-3">April 2, 2021</div>
      <h1 class="my-2 h00-mktg lh-condensed">GHSL-2020-372: Unauthorized repository modification or secrets exfiltration in GitHub workflows of 418sec/huntr</h1>

      
      
      
      
      

      

      <a target="_blank" class="sc-frDJqD SgxRc d-inline-flex flex-row flex-items-center text-gray" href="https://github.com/jarlob">
        <img class="mr-3" src="https://avatars.githubusercontent.com/u/26652396?s=35" height="35" width="35">
        <span>Jaroslav Lobacevski</span>
      </a>
    </header>

    <main id="content" class="markdown-body" aria-label="Content">
      
<h2 id="coordinated-disclosure-timeline">Coordinated Disclosure Timeline</h2>

<ul>
  <li>2020-12-22: Report sent to maintainers.</li>
  <li>2020-12-22: Maintainers acknowledged.</li>
  <li>2021-01-26: Asked maintainers for status update.</li>
  <li>2021-01-26: Maintainers asked for more details about the vulnerability.</li>
  <li>2021-01-26/27: Provided additional explanation.</li>
  <li>2021-02-23: Asked maintainers for status update.</li>
  <li>2021-02-23: Maintainers responded that they work on rewriting the code, but “in the mean time have to run this risk”.</li>
  <li>2021-02-23: Notified maintainers, that disclosure deadline is in a month.</li>
  <li>2021-02-23: Maintainers responded stating they do not consent to public advisory publication.</li>
  <li>2021-02-23: Security Lab replied with a reference to our <a href="https://securitylab.github.com/advisories#policy">disclosure policy</a>, and by stating that since there is no redistributable software we will not issue any GHSA or request a CVE.</li>
  <li>2021-03-22: Disclosure deadline reached.</li>
  <li>2021-04-01: Asked maintainers for status update and notified that more than 90 days have passed.</li>
  <li>2021-04-01: <a href="https://github.com/418sec/huntr/commit/3a78be77d70026cb89fb222fe22e5fbdf224800e">A fix</a> is applied to remove vulnerable workflows.</li>
  <li>2021-04-01: Publication as per our <a href="https://securitylab.github.com/advisories#policy">policy</a>.</li>
</ul>

<h2 id="summary">Summary</h2>

<p>The <a href="https://github.com/418sec/huntr/blob/staging/.github/workflows/process-disclosure.yml">process-disclosure.yml</a> GitHub workflow is vulnerable to unauthorized modification of the base repository or secrets exfiltration from a Pull Request.</p>

<h2 id="product">Product</h2>

<p><a href="https://github.com/418sec/huntr">418sec/huntr</a> GitHub repository</p>

<h2 id="tested-version">Tested Version</h2>

<p>The latest changeset <a href="https://github.com/418sec/huntr/blob/be289b12bb5a01c02864b5082437dc047ce88c1e/.github/workflows/process-disclosure.yml">be289b1</a> to the date.</p>

<h2 id="details">Details</h2>

<h3 id="issue-untrusted-code-is-explicitly-checked-out-and-run-on-a-pull-request-from-a-fork">Issue: Untrusted code is explicitly checked out and run on a Pull Request from a fork</h3>

<p>Workflows triggered on <code class="language-plaintext highlighter-rouge">pull_request_target</code> have read/write tokens for the base repository and the access to secrets. By explicitly checking out and running the build script from a fork, the untrusted code is running in an environment that is able to push to the base repository and to access secrets. More details can be found in the article <a href="https://securitylab.github.com/research/github-actions-preventing-pwn-requests/">Keeping your GitHub Actions and workflows secure: Preventing pwn requests</a>.</p>

<div class="language-yaml highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="na">on</span><span class="pi">:</span>
  <span class="pi">-</span> <span class="s">pull_request_target</span>
<span class="nn">...</span>
      <span class="pi">-</span> <span class="na">id</span><span class="pi">:</span> <span class="s">checkout</span>
        <span class="na">uses</span><span class="pi">:</span> <span class="s">actions/checkout@v2</span>
        <span class="na">with</span><span class="pi">:</span>
          <span class="na">fetch-depth</span><span class="pi">:</span> <span class="m">0</span>
          <span class="na">ref</span><span class="pi">:</span> <span class="s">refs/pull/${{ github.event.number }}/merge</span>
<span class="nn">...</span>
      <span class="pi">-</span> <span class="na">id</span><span class="pi">:</span> <span class="s">dependency-install</span>
        <span class="na">name</span><span class="pi">:</span> <span class="s">Install npm dependencies</span>
        <span class="na">run</span><span class="pi">:</span> <span class="s">npm ci</span>
      <span class="pi">-</span> <span class="na">id</span><span class="pi">:</span> <span class="s">generate-diff</span>
        <span class="na">name</span><span class="pi">:</span> <span class="s">Generate the diff</span>
        <span class="na">env</span><span class="pi">:</span>
          <span class="na">PR_NUMBER</span><span class="pi">:</span> <span class="s">${{ github.event.pull_request.number }}</span>
          <span class="na">GITHUB_TOKEN</span><span class="pi">:</span> <span class="s">${{ secrets.HUNTR_HELPER_TOKEN }}</span>
        <span class="na">run</span><span class="pi">:</span> <span class="s">node ./generate-diff.js</span>
<span class="nn">...</span>
</code></pre></div></div>

<h4 id="impact">Impact</h4>

<p>The vulnerability allows for unauthorized modification of the base repository and secrets exfiltration.</p>

<h2 id="credit">Credit</h2>

<p>This issue was discovered and reported by GHSL team member <a href="https://github.com/JarLob">@JarLob (Jaroslav Lobačevski)</a>.</p>

<h2 id="contact">Contact</h2>

<p>You can contact the GHSL team at <code class="language-plaintext highlighter-rouge">securitylab@github.com</code>, please include a reference to <code class="language-plaintext highlighter-rouge">GHSL-2020-372</code> in any communication regarding this issue.</p>

