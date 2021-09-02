<header class="post-header d-block mb-6">
      <div class="date text-mono f5 my-3">February 3, 2021</div>
      <h1 class="my-2 h00-mktg lh-condensed">GHSL-2020-280: Arbitrary code execution in deislabs/akri workflows</h1>

      
      
      
      
      

      

      <a target="_blank" class="sc-frDJqD SgxRc d-inline-flex flex-row flex-items-center text-gray" href="https://github.com/jarlob">
        <img class="mr-3" src="https://avatars.githubusercontent.com/u/26652396?s=35" height="35" width="35">
        <span>Jaroslav Lobacevski</span>
      </a>
    </header>

    <main id="content" class="markdown-body" aria-label="Content">
      <h2 id="coordinated-disclosure-timeline">Coordinated Disclosure Timeline</h2>

<ul>
  <li>2020-11-30-2020-12-01: Report sent to various maintainers.</li>
  <li>2020-12-02: Report acknowledged.</li>
  <li>2020-12-05: Issue resolved.</li>
</ul>

<h2 id="summary">Summary</h2>

<p>Multiple workflows are vulnerable to unauthorized modification of the base repository or secrets exfiltration from a Pull Request.</p>

<h2 id="product">Product</h2>

<p><a href="https://github.com/deislabs/akri">deislabs/akri</a> GitHub repository</p>

<h2 id="tested-version">Tested Version</h2>

<p>The latest changeset <a href="https://github.com/deislabs/akri/tree/f023a3d96a8aeb3bbe7c19b915754cd486d3f147">f023a3d</a> to the date.</p>

<h2 id="details">Details</h2>

<h3 id="issue-untrusted-code-is-explicitly-checked-out-and-run-on-a-pull-request-from-a-fork">Issue: Untrusted code is explicitly checked out and run on a Pull Request from a fork</h3>

<p><code class="language-plaintext highlighter-rouge">pull_request_target</code> was introduced to allow triggered workflows to comment on PRs, label them, assign people, etc.. In order to make it possible the triggered action runner has read/write token for the base repository and the access to secrets. In order to prevent untrusted code from execution it runs in a context of the base repository.</p>

<p>By explicitly checking out and running build script from a fork the untrusted code is running in an environment that is able to push to the base repository and to access secrets.</p>

<p>For example <a href="https://github.com/deislabs/akri/blob/744f4ce5ad7c890a346401392a6b3db14082bfc8/.github/workflows/check-rust.yml">check-rust.yml</a>:</p>

<div class="language-yaml highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="na">on</span><span class="pi">:</span>
<span class="nn">...</span>
  <span class="na">pull_request_target</span><span class="pi">:</span>
    <span class="na">branches</span><span class="pi">:</span> <span class="pi">[</span> <span class="nv">main</span> <span class="pi">]</span>
    <span class="na">paths</span><span class="pi">:</span>
    <span class="pi">-</span> <span class="s">.github/workflows/check-rust.yml</span>
    <span class="pi">-</span> <span class="s1">'</span><span class="s">**.rs'</span>
    <span class="pi">-</span> <span class="s1">'</span><span class="s">**/Cargo.toml'</span>
    <span class="pi">-</span> <span class="s1">'</span><span class="s">**/Cargo.lock'</span>
    <span class="pi">-</span> <span class="s">build/setup.sh</span>
<span class="nn">...</span>
    <span class="na">steps</span><span class="pi">:</span>
    <span class="pi">-</span> <span class="na">name</span><span class="pi">:</span> <span class="s">Checkout the merged commit from PR and base branch</span>
      <span class="na">uses</span><span class="pi">:</span> <span class="s">actions/checkout@v2</span>
      <span class="na">if</span><span class="pi">:</span> <span class="s">github.event_name == 'pull_request_target'</span>
      <span class="na">with</span><span class="pi">:</span>
        <span class="c1"># pull_request_target is run in the context of the base repository</span>
        <span class="c1"># of the pull request, so the default ref is master branch and</span>
        <span class="c1"># ref should be manually set to the head of the PR</span>
        <span class="na">ref</span><span class="pi">:</span> <span class="s">refs/pull/${{ github.event.pull_request.number }}/head</span>
<span class="nn">...</span>
    <span class="pi">-</span> <span class="na">name</span><span class="pi">:</span> <span class="s">Install linux requirement</span>
      <span class="na">run</span><span class="pi">:</span> <span class="s">./build/setup.sh</span>
<span class="nn">...</span>
</code></pre></div></div>

<h4 id="impact">Impact</h4>

<p>The vulnerability allows for unauthorized modification of the base repository and secrets exfiltration.</p>

<h2 id="credit">Credit</h2>

<p>This issue was discovered and reported by GHSL team member <a href="https://github.com/JarLob">@JarLob (Jaroslav Lobačevski)</a>.</p>

<h2 id="contact">Contact</h2>

<p>You can contact the GHSL team at <code class="language-plaintext highlighter-rouge">securitylab@github.com</code>, please include a reference to <code class="language-plaintext highlighter-rouge">GHSL-2020-280</code> in any communication regarding this issue.</p>

   