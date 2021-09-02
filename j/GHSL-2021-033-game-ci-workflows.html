<header class="post-header d-block mb-6">
      <div class="date text-mono f5 my-3">July 21, 2021</div>
      <h1 class="my-2 h00-mktg lh-condensed">GHSL-2021-033: Arbitrary code execution in GitHub workflows of game-ci</h1>

      
      
      
      
      

      

      <a target="_blank" class="sc-frDJqD SgxRc d-inline-flex flex-row flex-items-center text-gray" href="https://github.com/jarlob">
        <img class="mr-3" src="https://avatars.githubusercontent.com/u/26652396?s=35" height="35" width="35">
        <span>Jaroslav Lobacevski</span>
      </a>
    </header>

    <main id="content" class="markdown-body" aria-label="Content">
      
<h2 id="coordinated-disclosure-timeline">Coordinated Disclosure Timeline</h2>

<ul>
  <li>2021-02-04: Issue reported to maintainers.</li>
  <li>2021-02-04: Report acknowledged.</li>
  <li>2021-02-08: Issue fixed.</li>
  <li>2021-02-23: Additional issue reported.</li>
  <li>2021-03-24: Asked maintainers for status update.</li>
  <li>2021-03-24: Report acknowledged.</li>
  <li>2021-03-29: Issue fixed.</li>
</ul>

<h2 id="summary">Summary</h2>

<p>The <a href="https://github.com/game-ci/unity-test-runner/blob/main/.github/workflows/main.yml">main.yml</a>, <a href="https://github.com/game-ci/unity-builder/blob/main/.github/workflows/kubernetes-tests.yml">kubernetes-tests.yml</a>, <a href="https://github.com/game-ci/docker/blob/main/.github/workflows/test.yml">test.yml</a> and <a href="https://github.com/game-ci/unity-builder/blob/main/.github/workflows/build-tests.yml">build-tests.yml</a> GitHub workflows are vulnerable to arbitrary code execution.</p>

<h2 id="product">Product</h2>

<p><a href="https://github.com/game-ci/unity-test-runner">game-ci/unity-test-runner</a> repository<br />
<a href="https://github.com/game-ci/unity-builder">game-ci/unity-builder</a> repository<br />
<a href="https://github.com/game-ci/docker">game-ci/docker</a> repository</p>

<h2 id="tested-version">Tested Version</h2>

<p>The latest changeset of <a href="https://github.com/game-ci/unity-test-runner/blob/23b6b8f5f3ecc27b150cf7b645183c59ba9be418/.github/workflows/main.yml">main.yml</a>, <a href="https://github.com/game-ci/unity-builder/blob/c7c1841c97d06981bbb08a3a1a4235ebb69123fa/.github/workflows/kubernetes-tests.yml">kubernetes-tests.yml</a>, <a href="https://github.com/game-ci/docker/blob/684cb59a990d406088efc9f071c8b5dd8ace1636/.github/workflows/test.yml">test.yml</a> and <a href="https://github.com/game-ci/unity-builder/blob/c7c1841c97d06981bbb08a3a1a4235ebb69123fa/.github/workflows/build-tests.yml">build-tests.yml</a> to date.</p>

<h2 id="details">Details</h2>

<h3 id="issue-untrusted-code-is-explicitly-checked-out-and-run-on-a-pull-request-from-a-fork">Issue: Untrusted code is explicitly checked out and run on a Pull Request from a fork</h3>

<p>Workflows triggered on <code class="language-plaintext highlighter-rouge">pull_request_target</code> have read/write tokens for the base repository and access to repository secrets. By explicitly checking out and running the build script from a fork, the untrusted code is running in an environment that is able to push to the base repository and access secrets. More details can be found in <a href="https://securitylab.github.com/research/github-actions-preventing-pwn-requests/">Keeping your GitHub Actions and workflows secure: Preventing pwn requests</a>.</p>

<div class="language-yaml highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="na">on</span><span class="pi">:</span>
  <span class="na">push</span><span class="pi">:</span> <span class="pi">{</span> <span class="nv">branches</span><span class="pi">:</span> <span class="pi">[</span><span class="nv">main</span><span class="pi">]</span> <span class="pi">}</span>
  <span class="na">pull_request_target</span><span class="pi">:</span>
    <span class="na">paths-ignore</span><span class="pi">:</span>
      <span class="pi">-</span> <span class="s2">"</span><span class="s">.github/**"</span>
<span class="nn">...</span>
        <span class="na">uses</span><span class="pi">:</span> <span class="s">actions/checkout@v2</span>
        <span class="na">if</span><span class="pi">:</span> <span class="s">github.event.event_type == 'pull_request_target'</span>
        <span class="na">with</span><span class="pi">:</span>
          <span class="na">lfs</span><span class="pi">:</span> <span class="no">true</span>
          <span class="na">ref</span><span class="pi">:</span> <span class="s">${{ github.event.pull_request.head.ref }}</span>
          <span class="na">repository</span><span class="pi">:</span> <span class="s">${{ github.event.pull_request.head.repo.full_name }}</span>
<span class="nn">...</span>
      <span class="pi">-</span> <span class="na">uses</span><span class="pi">:</span> <span class="s">./</span>
<span class="nn">...</span>
</code></pre></div></div>

<p>The <code class="language-plaintext highlighter-rouge">action.yml</code> file from the root directory is attacker controlled.</p>

<h4 id="impact">Impact</h4>

<p>The vulnerability allows for unauthorized modification of the base repository and secrets exfiltration.</p>

<h2 id="credit">Credit</h2>

<p>This issue was discovered and reported by GHSL team member <a href="https://github.com/JarLob">@JarLob (Jaroslav Lobačevski)</a>.</p>

<h2 id="contact">Contact</h2>

<p>You can contact the GHSL team at <code class="language-plaintext highlighter-rouge">securitylab@github.com</code>, please include a reference to <code class="language-plaintext highlighter-rouge">GHSL-2021-033</code> in any communication regarding this issue.</p>


   