<header class="post-header d-block mb-6">
      <div class="date text-mono f5 my-3">December 16, 2020</div>
      <h1 class="my-2 h00-mktg lh-condensed">GHSL-2020-281: Unauthorized repository modification or secrets exfiltration in the GitHub workflow of tskit-dev/msprime</h1>

      
      
      
      
      

      

      <a target="_blank" class="sc-frDJqD SgxRc d-inline-flex flex-row flex-items-center text-gray" href="https://github.com/jarlob">
        <img class="mr-3" src="https://avatars.githubusercontent.com/u/26652396?s=35" height="35" width="35">
        <span>Jaroslav Lobacevski</span>
      </a>
    </header>

    <main id="content" class="markdown-body" aria-label="Content">
      <h2 id="summary">Summary</h2>

<p>The <a href="https://github.com/tskit-dev/msprime/blob/main/.github/workflows/docs.yml">docs.yml</a> GitHub workflow is vulnerable to unauthorized modification of the base repository or secrets exfiltration from a Pull Request.</p>

<h2 id="product">Product</h2>

<p><a href="https://github.com/tskit-dev/msprime">tskit-dev/msprime</a> GitHub repository</p>

<h2 id="tested-version">Tested Version</h2>

<p>The latest changeset <a href="https://github.com/tskit-dev/msprime/blob/e2a01e89c45579d9754163d829cb4c75dbf67545/.github/workflows/docs.yml">e2a01e8</a> to the date.</p>

<h2 id="details">Details</h2>

<h3 id="issue-untrusted-code-is-explicitly-checked-out-and-run-on-a-pull-request-from-a-fork">Issue: Untrusted code is explicitly checked out and run on a Pull Request from a fork</h3>

<p><code class="language-plaintext highlighter-rouge">pull_request_target</code> was introduced to allow triggered workflows to comment on PRs, label them, assign people, etc.. In order to make it possible the triggered action runner has read/write token for the base repository and the access to secrets. In order to prevent untrusted code from execution it runs in a context of the base repository.</p>

<p>By explicitly checking out and running build script from a fork the untrusted code is running in an environment that is able to push to the base repository and to access secrets.</p>

<div class="language-yaml highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="na">on</span><span class="pi">:</span>
  <span class="na">pull_request_target</span><span class="pi">:</span>
<span class="nn">...</span>
<span class="na">env</span><span class="pi">:</span>
<span class="nn">...</span>
  <span class="na">MAKE_TARGET</span><span class="pi">:</span> <span class="s">cmodule</span>
<span class="nn">...</span>
      <span class="pi">-</span> <span class="na">uses</span><span class="pi">:</span> <span class="s">actions/checkout@v2</span>
        <span class="c1"># As we are using pull-request-target which uses the workflow from the base</span>
        <span class="c1"># of the PR, we need to be specific</span>
        <span class="na">with</span><span class="pi">:</span>
            <span class="na">ref</span><span class="pi">:</span> <span class="s">${{ github.event.pull_request.head.ref }}</span>
            <span class="na">repository</span><span class="pi">:</span> <span class="s">${{ github.event.pull_request.head.repo.full_name }}</span>
            <span class="na">submodules</span><span class="pi">:</span> <span class="no">true</span>
<span class="nn">...</span>
      <span class="pi">-</span> <span class="na">name</span><span class="pi">:</span> <span class="s">Build virtualenv</span>
        <span class="na">if</span><span class="pi">:</span> <span class="s">steps.cache.outputs.cache-hit != 'true'</span>
        <span class="na">run</span><span class="pi">:</span> <span class="s">python -m venv venv</span>

      <span class="pi">-</span> <span class="na">name</span><span class="pi">:</span> <span class="s">Install deps</span>
        <span class="na">run</span><span class="pi">:</span> <span class="s">venv/bin/activate &amp;&amp; pip install -r requirements/CI-docs/requirements.txt</span>

      <span class="pi">-</span> <span class="na">name</span><span class="pi">:</span> <span class="s">Install GSL</span>
        <span class="na">if</span><span class="pi">:</span> <span class="s">env.BUILD_GSL == 'true'</span>
        <span class="na">run</span><span class="pi">:</span> <span class="s">sudo apt-get install -y libgsl0-dev</span>

      <span class="pi">-</span> <span class="na">name</span><span class="pi">:</span> <span class="s">Build C module</span>
        <span class="na">if</span><span class="pi">:</span> <span class="s">env.MAKE_TARGET</span>
        <span class="na">run</span><span class="pi">:</span> <span class="s">venv/bin/activate &amp;&amp; make $MAKE_TARGET</span>

      <span class="pi">-</span> <span class="na">name</span><span class="pi">:</span> <span class="s">Build Docs</span>
        <span class="na">run</span><span class="pi">:</span> <span class="s">venv/bin/activate &amp;&amp; make -C docs</span>
<span class="nn">...</span>
</code></pre></div></div>

<h4 id="impact">Impact</h4>

<p>The vulnerability allows for unauthorized modification of the base repository and secrets exfiltration.</p>

<h2 id="coordinated-disclosure-timeline">Coordinated Disclosure Timeline</h2>

<ul>
  <li>2020-11-30: Report sent to maintainers</li>
  <li>2020-11-30: Issue resolved</li>
</ul>

<h2 id="credit">Credit</h2>

<p>This issue was discovered and reported by GHSL team member <a href="https://github.com/JarLob">@JarLob (Jaroslav Loba??evski)</a>.</p>

<h2 id="contact">Contact</h2>

<p>You can contact the GHSL team at <code class="language-plaintext highlighter-rouge">securitylab@github.com</code>, please include a reference to <code class="language-plaintext highlighter-rouge">GHSL-2020-281</code> in any communication regarding this issue.</p>

   