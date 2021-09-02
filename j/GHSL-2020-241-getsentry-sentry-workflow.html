<header class="post-header d-block mb-6">
      <div class="date text-mono f5 my-3">February 3, 2021</div>
      <h1 class="my-2 h00-mktg lh-condensed">GHSL-2020-241: Arbitrary code execution and shell command injection in getsentry/sentry workflow</h1>

      
      
      
      
      

      

      <a target="_blank" class="sc-frDJqD SgxRc d-inline-flex flex-row flex-items-center text-gray" href="https://github.com/jarlob">
        <img class="mr-3" src="https://avatars.githubusercontent.com/u/26652396?s=35" height="35" width="35">
        <span>Jaroslav Lobacevski</span>
      </a>
    </header>

    <main id="content" class="markdown-body" aria-label="Content">
      <h2 id="coordinated-disclosure-timeline">Coordinated Disclosure Timeline</h2>

<ul>
  <li>2020-11-26: Report sent to maintainer</li>
  <li>2020-11-26: Maintainer acknowledges</li>
  <li>2020-12-05: All issues resolved</li>
</ul>

<h2 id="summary">Summary</h2>

<p>The <a href="https://github.com/getsentry/sentry/blob/master/.github/workflows/acceptance.yml">‘acceptance.yml’ GitHub workflow</a> is vulnerable to arbitrary code execution and shell command injection.</p>

<h2 id="product">Product</h2>

<p><a href="https://github.com/getsentry/sentry">getsentry/sentry GitHub repository</a></p>

<h2 id="tested-version">Tested Version</h2>

<p>The latest changeset <a href="https://github.com/getsentry/sentry/blob/f325d54b5e0a06be52edef85e6e0781191b0984a/.github/workflows/acceptance.yml">f325d54</a> to the date.</p>

<h2 id="details">Details</h2>

<h3 id="issue-1-untrusted-code-is-explicitly-checked-out-and-run-on-a-pull-request-from-a-fork">Issue 1: Untrusted code is explicitly checked out and run on a Pull Request from a fork</h3>

<p><code class="language-plaintext highlighter-rouge">pull_request_target</code> was introduced to allow triggered workflows to comment on PRs, label them, assign people, etc.. In order to make it possible the triggered action runner has read/write token for the base repository and the access to secrets. In order to prevent untrusted code from execution it runs in a context of the base repository.</p>

<p>By explicitly checking out and running build script from a fork the untrusted code is running in an environment that is able to push to the base repository and to access secrets.</p>

<div class="language-yaml highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="na">on</span><span class="pi">:</span>
  <span class="na">push</span><span class="pi">:</span>
    <span class="na">branches</span><span class="pi">:</span>
      <span class="pi">-</span> <span class="s">master</span>
      <span class="pi">-</span> <span class="s">releases/**</span>
  <span class="c1"># XXX: We are using `pull_request_target` instead of `pull_request` because we want</span>
  <span class="c1"># Visual Snapshots to run on forks.  It allows forks to access secrets safely by</span>
  <span class="c1"># only running workflows from the main branch. Prefer to use `pull_request` when possible.</span>
  <span class="c1">#</span>
  <span class="c1"># See https://github.com/getsentry/sentry/pull/21600 for more details</span>
  <span class="na">pull_request_target</span><span class="pi">:</span>
<span class="nn">...</span>
    <span class="na">steps</span><span class="pi">:</span>
      <span class="pi">-</span> <span class="na">uses</span><span class="pi">:</span> <span class="s">actions/checkout@v2</span>
        <span class="na">name</span><span class="pi">:</span> <span class="s">Checkout sentry (pull_request_target)</span>
        <span class="na">if</span><span class="pi">:</span> <span class="s">github.event.pull_request.head.ref != ''</span>
        <span class="na">with</span><span class="pi">:</span>
          <span class="c1"># Note this is required because of `pull_request_target`, which allows</span>
          <span class="c1"># forks to access secrets safely by only running workflows from the main branch.</span>
          <span class="na">ref</span><span class="pi">:</span> <span class="s">${{ github.event.pull_request.head.ref }}</span>
          <span class="na">repository</span><span class="pi">:</span> <span class="s">${{ github.event.pull_request.head.repo.full_name }}</span>
<span class="nn">...</span>
      <span class="pi">-</span> <span class="na">name</span><span class="pi">:</span> <span class="s">Install dependencies</span>
        <span class="na">run</span><span class="pi">:</span> <span class="s">yarn install --frozen-lockfile</span>

      <span class="pi">-</span> <span class="na">name</span><span class="pi">:</span> <span class="s">jest</span>
        <span class="na">run</span><span class="pi">:</span> <span class="pi">|</span>
          <span class="s">NODE_ENV=production yarn build-css</span>
          <span class="s">yarn test-ci --forceExit</span>
</code></pre></div></div>

<h4 id="impact">Impact</h4>

<p>The vulnerability allows for unauthorized modification of the base repository and secrets exfiltration.</p>

<h3 id="issue-2-the-forked-branch-name-is-used-to-format-a-shell-command">Issue 2: The forked branch name is used to format a shell command</h3>

<p>The forked branch name is used to format a bash script.</p>

<div class="language-yaml highlighter-rouge"><div class="highlight"><pre class="highlight"><code>      <span class="pi">-</span> <span class="na">name</span><span class="pi">:</span> <span class="s">Get merge base</span>
        <span class="na">if</span><span class="pi">:</span> <span class="s">github.event.pull_request.head.ref != ''</span>
        <span class="na">id</span><span class="pi">:</span> <span class="s">merge-base</span>
        <span class="na">run</span><span class="pi">:</span> <span class="pi">|</span>
          <span class="s">echo "::set-output name=sha::$(git merge-base origin/master $)"</span>
</code></pre></div></div>

<p>This vulnerability allows for arbitrary command injection into the bash script. For a Proof of Concept create a PR from branch named <code class="language-plaintext highlighter-rouge">a";echo${IFS}"hello"#</code>.</p>

<h4 id="impact-1">Impact</h4>

<p>The injection allows for exfiltration of secrets and the temporary GitHub repository authorization token to the attacker controlled server. Although the token is not valid after the workflow finishes, since the attacker controls the execution of the workflow he or she can delay it to give the malicious server time to modify the repository.</p>

<h2 id="credit">Credit</h2>

<p>This issue was discovered and reported by GHSL team member <a href="https://github.com/JarLob">@JarLob (Jaroslav Lobačevski)</a>.</p>

<h2 id="contact">Contact</h2>

<p>You can contact the GHSL team at <code class="language-plaintext highlighter-rouge">securitylab@github.com</code>, please include a reference to <code class="language-plaintext highlighter-rouge">GHSL-2020-241</code> in any communication regarding this issue.</p>
