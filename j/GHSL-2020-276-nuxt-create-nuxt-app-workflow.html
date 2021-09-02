<header class="post-header d-block mb-6">
      <div class="date text-mono f5 my-3">December 16, 2020</div>
      <h1 class="my-2 h00-mktg lh-condensed">GHSL-2020-276: Unauthorized repository modification or secrets exfiltration in nuxt repositories</h1>

      
      
      
      
      

      

      <a target="_blank" class="sc-frDJqD SgxRc d-inline-flex flex-row flex-items-center text-gray" href="https://github.com/jarlob">
        <img class="mr-3" src="https://avatars.githubusercontent.com/u/26652396?s=35" height="35" width="35">
        <span>Jaroslav Lobacevski</span>
      </a>
    </header>

    <main id="content" class="markdown-body" aria-label="Content">
      <h2 id="summary">Summary</h2>

<p><a href="https://github.com/nuxt/create-nuxt-app/blob/master/.github/workflows/snapshot.yml">snapshot.yml</a> and <a href="https://github.com/nuxt/modules/blob/master/.github/workflows/sync.yml">sync.yml</a> GitHub workflows are vulnerable to unauthorized modification of the base repository or secrets exfiltration from a Pull Request.</p>

<h2 id="product">Product</h2>

<p><a href="https://github.com/nuxt/create-nuxt-app">nuxt/create-nuxt-app</a> GitHub repository<br />
<a href="https://github.com/nuxt/modules">nuxt/modules</a> GitHub repository</p>

<h2 id="tested-version">Tested Version</h2>

<p>The latest changesets to the date <a href="https://github.com/nuxt/create-nuxt-app/blob/1aa53fd846e0d0390f0407653b624b1e46ef1d6e/.github/workflows/snapshot.yml">1aa53fd</a> and <a href="https://github.com/nuxt/modules/blob/2ae2a0c2fcb1869153b658522340d0b5b24b3376/.github/workflows/sync.yml">2ae2a0c</a>.</p>

<h2 id="details">Details</h2>

<h3 id="issue-untrusted-code-is-explicitly-checked-out-and-run-on-a-pull-request-from-a-fork">Issue: Untrusted code is explicitly checked out and run on a Pull Request from a fork</h3>

<p><code class="language-plaintext highlighter-rouge">pull_request_target</code> was introduced to allow triggered workflows to comment on PRs, label them, assign people, etc.. In order to make it possible the triggered action runner has read/write token for the base repository and the access to secrets. In order to prevent untrusted code from execution it runs in a context of the base repository.</p>

<p>By explicitly checking out and running build script from a fork the untrusted code is running in an environment that is able to push to the base repository and to access secrets.</p>

<div class="language-yaml highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="na">on</span><span class="pi">:</span> <span class="pi">[</span><span class="nv">pull_request</span><span class="pi">,</span> <span class="nv">pull_request_target</span><span class="pi">]</span>
<span class="nn">...</span>
    <span class="na">if</span><span class="pi">:</span> <span class="s">${{ contains(github.actor, 'renovate') }}</span>
<span class="nn">...</span>
      <span class="pi">-</span> <span class="na">name</span><span class="pi">:</span> <span class="s">Checkout</span>
        <span class="na">uses</span><span class="pi">:</span> <span class="s">actions/checkout@v2</span>
        <span class="na">with</span><span class="pi">:</span>
          <span class="na">ref</span><span class="pi">:</span> <span class="s">${{ github.head_ref }}</span>
<span class="nn">...</span>
      <span class="pi">-</span> <span class="na">name</span><span class="pi">:</span> <span class="s">Install dependencies</span>
        <span class="na">if</span><span class="pi">:</span> <span class="s">steps.cache.outputs.cache-hit != 'true'</span>
        <span class="na">run</span><span class="pi">:</span> <span class="s">yarn --frozen-lockfile --non-interactive</span>

      <span class="pi">-</span> <span class="na">name</span><span class="pi">:</span> <span class="s">Test with update-snapshots</span>
        <span class="na">run</span><span class="pi">:</span> <span class="s">AVA_FORCE_CI="not-ci" yarn ava --verbose --update-snapshots</span>
<span class="nn">...</span>
</code></pre></div></div>

<p>There is a check supposed to trigger the workflow only for <code class="language-plaintext highlighter-rouge">renovate</code> actor. However it is bypassable with a user name like <code class="language-plaintext highlighter-rouge">renovate2</code>, <code class="language-plaintext highlighter-rouge">notrenovate</code>, etc.</p>

<div class="language-yaml highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="na">on</span><span class="pi">:</span> <span class="pi">[</span><span class="nv">pull_request</span><span class="pi">,</span> <span class="nv">pull_request_target</span><span class="pi">]</span>
<span class="nn">...</span>
      <span class="pi">-</span> <span class="na">name</span><span class="pi">:</span> <span class="s">Checkout</span>
        <span class="na">uses</span><span class="pi">:</span> <span class="s">actions/checkout@v2</span>
        <span class="na">with</span><span class="pi">:</span>
          <span class="na">ref</span><span class="pi">:</span> <span class="s">${{ github.head_ref }}</span>
<span class="nn">...</span>
      <span class="pi">-</span> <span class="na">name</span><span class="pi">:</span> <span class="s">Install dependencies</span>
        <span class="na">if</span><span class="pi">:</span> <span class="s">steps.cache.outputs.cache-hit != 'true'</span>
        <span class="na">run</span><span class="pi">:</span> <span class="s">yarn --frozen-lockfile --non-interactive</span>

      <span class="pi">-</span> <span class="na">name</span><span class="pi">:</span> <span class="s">Sync</span>
        <span class="na">run</span><span class="pi">:</span> <span class="s">yarn sync</span>
</code></pre></div></div>

<h4 id="impact">Impact</h4>

<p>Currently, because of a mistake, the script doesn’t checkout the Pull Request, but a branch from the base repository named as the branch from the PR. If there is no branch with the same name the script fails. However it is likely the bug to be fixed to <code class="language-plaintext highlighter-rouge">ref: refs/pull/${{ github.event.pull_request.number }}/merge</code> and the vulnerabilty to be made exploitable.</p>

<p>The vulnerability allows for unauthorized modification of the base repository and secrets exfiltration.</p>

<h2 id="coordinated-disclosure-timeline">Coordinated Disclosure Timeline</h2>

<ul>
  <li>2020-11-30: Report sent to maintainers</li>
  <li>2020-12-01: Maintainers acknowledged</li>
  <li>2020-12-02: Issue resolved</li>
</ul>

<h2 id="credit">Credit</h2>

<p>This issue was discovered and reported by GHSL team member <a href="https://github.com/JarLob">@JarLob (Jaroslav Lobačevski)</a>.</p>

<h2 id="contact">Contact</h2>

<p>You can contact the GHSL team at <code class="language-plaintext highlighter-rouge">securitylab@github.com</code>, please include a reference to <code class="language-plaintext highlighter-rouge">GHSL-2020-276</code> in any communication regarding this issue.</p>

 