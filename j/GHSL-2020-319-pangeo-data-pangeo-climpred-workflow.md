<header class="post-header d-block mb-6">
      <div class="date text-mono f5 my-3">February 3, 2021</div>
      <h1 class="my-2 h00-mktg lh-condensed">GHSL-2020-319: Arbitrary code execution in pangeo-data/climpred workflows</h1>

      
      
      
      
      

      

      <a target="_blank" class="sc-frDJqD SgxRc d-inline-flex flex-row flex-items-center text-gray" href="https://github.com/jarlob">
        <img class="mr-3" src="https://avatars.githubusercontent.com/u/26652396?s=35" height="35" width="35">
        <span>Jaroslav Lobacevski</span>
      </a>
    </header>

    <main id="content" class="markdown-body" aria-label="Content">
      <h2 id="coordinated-disclosure-timeline">Coordinated Disclosure Timeline</h2>

<ul>
  <li>2020-11-30-2020-12-01: Report sent to various maintainers.</li>
  <li>2021-01-22: No reply. Asked for the contact publicly.</li>
  <li>2021-01-22-23: Fix. Feedback. Additional fix.</li>
  <li>2021-01-23: Issue resolved.</li>
</ul>

<h2 id="summary">Summary</h2>

<p>The <code class="language-plaintext highlighter-rouge">climpred_installs.yml</code> and <code class="language-plaintext highlighter-rouge">climpred_testing.yml</code> GitHub workflows in <strong>multiple branches</strong> are vulnerable to unauthorized modification of the base repository or secrets exfiltration from a Pull Request.</p>

<h2 id="product">Product</h2>

<p><a href="https://github.com/pangeo-data/climpred">pangeo-data/climpred</a> GitHub repository</p>

<h2 id="tested-version">Tested Version</h2>

<p>For example, the latest changeset <a href="https://github.com/pangeo-data/climpred/blob/123e181eab171b633efaebb8e36c6d982b8b2bca/.github/workflows/climpred_installs.yml">123e181</a> and <a href="https://github.com/pangeo-data/climpred/blob/b47a7e40ddf49927b34c2262b871b37b4d30bfee/.github/workflows/climpred_testing.yml">b47a7e4</a> to the date.</p>

<h2 id="details">Details</h2>

<h3 id="issue-untrusted-code-is-explicitly-checked-out-and-run-on-a-pull-request-from-a-fork">Issue: Untrusted code is explicitly checked out and run on a Pull Request from a fork</h3>

<p>Workflows triggered on <code class="language-plaintext highlighter-rouge">pull_request_target</code> have read/write tokens for the base repository and the access to secrets. By explicitly checking out and running the build script from a fork the untrusted code is running in an environment that is able to push to the base repository and to access secrets. More details can be found in the article <a href="https://securitylab.github.com/research/github-actions-preventing-pwn-requests/">Keeping your GitHub Actions and workflows secure: Preventing pwn requests</a>.</p>

<p><em>climpred_installs.yml:</em></p>

<div class="language-yaml highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="na">on</span><span class="pi">:</span> <span class="s">pull_request_target</span>
<span class="nn">...</span>
    <span class="pi">-</span> <span class="na">uses</span><span class="pi">:</span> <span class="s">actions/checkout@v2</span>
      <span class="na">with</span><span class="pi">:</span>
        <span class="na">ref</span><span class="pi">:</span> <span class="s">${{github.event.pull_request.head.ref}}</span>
        <span class="na">repository</span><span class="pi">:</span> <span class="s">${{github.event.pull_request.head.repo.full_name}}</span>
<span class="nn">...</span>
      <span class="na">run</span><span class="pi">:</span> <span class="pi">|</span>
        <span class="s">python -m pip install --upgrade pip</span>
        <span class="s">pip install -e .</span>
<span class="s">...</span>
</code></pre></div></div>

<p>The <code class="language-plaintext highlighter-rouge">pip install -e .</code> runs <code class="language-plaintext highlighter-rouge">setup.py</code> which is controlled by attacker.</p>

<p><em>climpred_testing.yml:</em></p>
<div class="language-yaml highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="na">on</span><span class="pi">:</span> <span class="s">pull_request_target</span>
<span class="nn">...</span>
      <span class="pi">-</span> <span class="na">uses</span><span class="pi">:</span> <span class="s">actions/checkout@v2</span>
        <span class="na">with</span><span class="pi">:</span>
          <span class="na">ref</span><span class="pi">:</span> <span class="s">${{github.event.pull_request.head.ref}}</span>
          <span class="na">repository</span><span class="pi">:</span> <span class="s">${{github.event.pull_request.head.repo.full_name}}</span>
      <span class="pi">-</span> <span class="na">name</span><span class="pi">:</span> <span class="s">Install Conda environment</span>
        <span class="na">uses</span><span class="pi">:</span> <span class="s">conda-incubator/setup-miniconda@v1</span>
        <span class="na">with</span><span class="pi">:</span>
          <span class="na">auto-update-conda</span><span class="pi">:</span> <span class="no">true</span>
          <span class="na">activate-environment</span><span class="pi">:</span> <span class="s">climpred-minimum-tests</span>
          <span class="na">environment-file</span><span class="pi">:</span> <span class="s">ci/requirements/minimum-tests.yml</span>
          <span class="na">python-version</span><span class="pi">:</span> <span class="s">${{ matrix.python-version }}</span>
      <span class="pi">-</span> <span class="na">name</span><span class="pi">:</span> <span class="s">Conda info</span>
        <span class="na">shell</span><span class="pi">:</span> <span class="s">bash -l {0}</span>
        <span class="na">run</span><span class="pi">:</span> <span class="s">conda info</span>
      <span class="pi">-</span> <span class="na">name</span><span class="pi">:</span> <span class="s">Conda list</span>
        <span class="na">shell</span><span class="pi">:</span> <span class="s">bash -l {0}</span>
        <span class="na">run</span><span class="pi">:</span> <span class="s">conda list</span>
      <span class="pi">-</span> <span class="na">name</span><span class="pi">:</span> <span class="s">Run tests</span>
        <span class="na">shell</span><span class="pi">:</span> <span class="s">bash -l {0}</span>
        <span class="na">run</span><span class="pi">:</span> <span class="pi">|</span>
          <span class="s">conda activate climpred-minimum-tests</span>
          <span class="s">pytest --cov=climpred --cov-report=xml</span>
<span class="s">...</span>
</code></pre></div></div>

<p>The <code class="language-plaintext highlighter-rouge">ci/requirements/minimum-tests.yml</code> is controlled by attacker, but even the existing one contains <code class="language-plaintext highlighter-rouge">- -e ../..</code> which runs <code class="language-plaintext highlighter-rouge">setup.py</code> from pull request.</p>

<h4 id="impact">Impact</h4>

<p>The vulnerability allows for unauthorized modification of the base repository and secrets exfiltration.</p>

<h2 id="credit">Credit</h2>

<p>This issue was discovered and reported by GHSL team member <a href="https://github.com/JarLob">@JarLob (Jaroslav Lobačevski)</a>.</p>

<h2 id="contact">Contact</h2>

<p>You can contact the GHSL team at <code class="language-plaintext highlighter-rouge">securitylab@github.com</code>, please include a reference to <code class="language-plaintext highlighter-rouge">GHSL-2020-319</code> in any communication regarding this issue.</p>

   