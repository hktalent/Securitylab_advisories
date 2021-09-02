<header class="post-header d-block mb-6">
      <div class="date text-mono f5 my-3">February 26, 2021</div>
      <h1 class="my-2 h00-mktg lh-condensed">GHSL-2020-335: Unauthorized repository modification or secrets exfiltration in a GitHub workflow of libpasta</h1>

      
      
      
      
      

      

      <a target="_blank" class="sc-frDJqD SgxRc d-inline-flex flex-row flex-items-center text-gray" href="https://github.com/jarlob">
        <img class="mr-3" src="https://avatars.githubusercontent.com/u/26652396?s=35" height="35" width="35">
        <span>Jaroslav Lobacevski</span>
      </a>
    </header>

    <main id="content" class="markdown-body" aria-label="Content">
      <h2 id="coordinated-disclosure-timeline">Coordinated Disclosure Timeline</h2>

<ul>
  <li>2020-12-11: Issue reported to maintainers</li>
  <li>2021-01-19: Report acknowledged</li>
  <li>2021-01-26: Issue fixed</li>
  <li>2021-02-23: Additional issue reported</li>
  <li>2021-02-23: Issue resolved</li>
</ul>

<h2 id="summary">Summary</h2>

<p>The <a href="https://github.com/libpasta/libpasta/blob/main/.github/workflows/ci.yml">ci.yml</a> GitHub workflow is vulnerable to unauthorized modification of the base repository or secrets exfiltration from a Pull Request.</p>

<h2 id="product">Product</h2>

<p><a href="https://github.com/libpasta/libpasta">libpasta/libpasta</a> GitHub repository</p>

<h2 id="tested-version">Tested Version</h2>

<p>The latest changeset <a href="https://github.com/libpasta/libpasta/blob/3921c89aa92a5510cc6c52d0ae4eafff51e51449/.github/workflows/ci.yml">3921c89</a> to the date.</p>

<h2 id="details">Details</h2>

<h3 id="issue-untrusted-code-is-explicitly-checked-out-and-run-on-a-pull-request-from-a-fork">Issue: Untrusted code is explicitly checked out and run on a Pull Request from a fork</h3>

<p><code class="language-plaintext highlighter-rouge">pull_request_target</code> was introduced to allow triggered workflows to comment on PRs, label them, assign people, etc.. In order to make this possible the triggered action runner has read/write token for the base repository and access to repository secrets. In order to prevent untrusted code from executing, it runs in the context of the base repository.</p>

<p>By explicitly checking out and running build scripts from a fork, untrusted code is running in a privileged environment that is able to push to the base repository and access repository secrets.</p>

<div class="language-yaml highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="na">on</span><span class="pi">:</span>
<span class="nn">...</span>
  <span class="na">pull_request_target</span><span class="pi">:</span>
<span class="nn">...</span>
      <span class="pi">-</span> <span class="na">uses</span><span class="pi">:</span> <span class="s">actions/checkout@v2</span>
        <span class="na">with</span><span class="pi">:</span>
          <span class="c1"># This prevents the Action from persisting the credentials it uses to</span>
          <span class="c1"># perform the fetch/checkout to the Runner's local Git config. On</span>
          <span class="c1"># `pull_request_target` events, the GITHUB_TOKEN provided to the</span>
          <span class="c1"># Runner has Write permissions to the base repository. We do **not**</span>
          <span class="c1"># want to allow untrusted code from forks to execute arbitrary Git</span>
          <span class="c1"># commands with those elevated permissions.</span>
          <span class="c1">#</span>
          <span class="c1"># More info:</span>
          <span class="c1"># https://github.blog/2020-08-03-github-actions-improvements-for-fork-and-pull-request-workflows/#improvements-for-public-repository-forks</span>
          <span class="na">persist-credentials</span><span class="pi">:</span> <span class="no">false</span>
          <span class="c1"># Explicitly setting the `repository` and `ref` inputs ensures that</span>
          <span class="c1"># `pull_request_target` events trigger CI runs against the code from</span>
          <span class="c1"># the HEAD branch. By default, this Action checks out code from the</span>
          <span class="c1"># BASE branch. On `push` events, the `github.event.pull_request` path</span>
          <span class="c1"># will yield a null value, and passing nulls to these inputs causes</span>
          <span class="c1"># them to fall back to the defaults</span>
          <span class="na">repository</span><span class="pi">:</span> <span class="s">${{ github.event.pull_request.head.repo.full_name }}</span>
          <span class="na">ref</span><span class="pi">:</span> <span class="s">${{ github.event.pull_request.head.sha }}</span>
<span class="nn">...</span>
      <span class="pi">-</span> <span class="na">name</span><span class="pi">:</span> <span class="s">Run test</span>
        <span class="na">run</span><span class="pi">:</span> <span class="s">cargo test --all-targets --features long_tests</span>
<span class="nn">...</span>
</code></pre></div></div>

<h4 id="impact">Impact</h4>

<p>The vulnerability allows for unauthorized modification of the base repository and secrets exfiltration.</p>

<h2 id="credit">Credit</h2>

<p>This issue was discovered and reported by GHSL team member <a href="https://github.com/JarLob">@JarLob (Jaroslav Lobačevski)</a>.</p>

<h2 id="contact">Contact</h2>

<p>You can contact the GHSL team at <code class="language-plaintext highlighter-rouge">securitylab@github.com</code>, please include a reference to <code class="language-plaintext highlighter-rouge">GHSL-2020-335</code> in any communication regarding this issue.</p>

   