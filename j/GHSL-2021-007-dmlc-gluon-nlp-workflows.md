<header class="post-header d-block mb-6">
      <div class="date text-mono f5 my-3">February 3, 2021</div>
      <h1 class="my-2 h00-mktg lh-condensed">GHSL-2021-007: Arbitrary code execution and shell command injection in dmlc/gluon-nlp workflows</h1>

      
      
      
      
      

      

      <a target="_blank" class="sc-frDJqD SgxRc d-inline-flex flex-row flex-items-center text-gray" href="https://github.com/jarlob">
        <img class="mr-3" src="https://avatars.githubusercontent.com/u/26652396?s=35" height="35" width="35">
        <span>Jaroslav Lobacevski</span>
      </a>
    </header>

    <main id="content" class="markdown-body" aria-label="Content">
      <h2 id="coordinated-disclosure-timeline">Coordinated Disclosure Timeline</h2>

<ul>
  <li>2021-01-18: Report sent to maintainers.</li>
  <li>2021-01-18: Maintainers acknowledged.</li>
  <li>2021-01-18: Issue resolved.</li>
</ul>

<h2 id="summary">Summary</h2>

<p>The <a href="https://github.com/dmlc/gluon-nlp/blob/master/.github/workflows/buildwebsite.yml">buildwebsite.yml</a> and <a href="https://github.com/dmlc/gluon-nlp/blob/master/.github/workflows/unittests-gpu.yml">unittests-gpu.yml</a> GitHub workflows are vulnerable to unauthorized modification of the base repository or secrets exfiltration from a Pull Request.</p>

<h2 id="product">Product</h2>

<p><a href="https://github.com/dmlc/gluon-nlp">dmlc/gluon-nlp</a> repository</p>

<h2 id="tested-version">Tested Version</h2>

<p>The latest changeset of <a href="https://github.com/dmlc/gluon-nlp/blob/d4a1d5d0167e4ce0d149a8079b762b633d2642bd/.github/workflows/buildwebsite.yml">buildwebsite.yml</a> and <a href="https://github.com/dmlc/gluon-nlp/blob/47fccc381b7966a36fbbf1ef10e8f97adf0c4620/.github/workflows/unittests-gpu.yml">unittests-gpu.yml</a> to the date.</p>

<h2 id="details">Details</h2>

<h3 id="issue-1-untrusted-code-is-explicitly-checked-out-and-run-on-a-pull-request-from-a-fork">Issue 1: Untrusted code is explicitly checked out and run on a Pull Request from a fork</h3>

<p>Workflows triggered on <code class="language-plaintext highlighter-rouge">pull_request_target</code> have read/write tokens for the base repository and the access to secrets. By explicitly checking out and running the build script from a fork the untrusted code is running in an environment that is able to push to the base repository and to access secrets. More details can be found in the article <a href="https://securitylab.github.com/research/github-actions-preventing-pwn-requests/">Keeping your GitHub Actions and workflows secure: Preventing pwn requests</a>.</p>

<p><em>buildwebsite.yml:</em></p>

<div class="language-yaml highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="na">on</span><span class="pi">:</span> <span class="pi">[</span><span class="nv">push</span><span class="pi">,</span> <span class="nv">pull_request_target</span><span class="pi">]</span>
<span class="nn">...</span>
      <span class="pi">-</span> <span class="na">name</span><span class="pi">:</span> <span class="s">Checkout Pull Request Repository(For pull request)</span>
        <span class="na">if</span><span class="pi">:</span> <span class="s">${{ github.event_name == 'pull_request' || github.event_name == 'pull_request_target' }}</span>
        <span class="na">uses</span><span class="pi">:</span> <span class="s">actions/checkout@v2</span>
        <span class="na">with</span><span class="pi">:</span>
          <span class="na">repository</span><span class="pi">:</span> <span class="s">${{ github.event.pull_request.head.repo.full_name }}</span>
          <span class="na">ref</span><span class="pi">:</span> <span class="s">${{ github.event.pull_request.head.ref }}</span>

      <span class="pi">-</span> <span class="na">name</span><span class="pi">:</span> <span class="s">Compile Notebooks(For pull request)</span>
        <span class="na">if</span><span class="pi">:</span> <span class="s">${{ github.event_name == 'pull_request' || github.event_name == 'pull_request_target' }}</span>
        <span class="na">run</span><span class="pi">:</span> <span class="pi">|</span>
          <span class="s">python -m pip install --quiet -e .[extras]</span>
          <span class="s">./tools/batch/batch_states/compile_notebooks.sh \</span>
<span class="s">...</span>
</code></pre></div></div>

<p>_unittests-gpu.yml:__</p>

<div class="language-yaml highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="na">on</span><span class="pi">:</span> <span class="pi">[</span><span class="nv">push</span><span class="pi">,</span> <span class="nv">pull_request_target</span><span class="pi">]</span>
<span class="nn">...</span>
      <span class="pi">-</span> <span class="na">name</span><span class="pi">:</span> <span class="s">Test project on AWS Batch(For pull request)</span>
        <span class="na">if</span><span class="pi">:</span> <span class="s">${{ github.event_name == 'pull_request' || github.event_name == 'pull_request_target' }}</span>
        <span class="na">run</span><span class="pi">:</span> <span class="pi">|</span>
          <span class="s">echo "Start submitting job"</span>
          <span class="s">python ./tools/batch/submit-job.py --region us-east-1 \</span>
                                             <span class="s">--job-type g4dn.4x \</span>
                                             <span class="s">--name GluonNLP-GPU-Test-PR#${{ github.event.number }} \</span>
                                             <span class="s">--source-ref ${{ github.event.pull_request.head.ref }} \</span>
<span class="s">...</span>
</code></pre></div></div>

<h4 id="impact">Impact</h4>

<p>The vulnerability allows for unauthorized modification of the base repository and secrets exfiltration.</p>

<h3 id="issue-2-a-branch-name-from-the-pull-request-is-used-to-format-a-shell-command">Issue 2: A branch name from the pull request is used to format a shell command</h3>

<p><em>buildwebsite.yml:</em></p>

<div class="language-yaml highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="na">on</span><span class="pi">:</span> <span class="pi">[</span><span class="nv">push</span><span class="pi">,</span> <span class="nv">pull_request_target</span><span class="pi">]</span>
<span class="nn">...</span>
      <span class="pi">-</span> <span class="na">name</span><span class="pi">:</span> <span class="s">Checkout Pull Request Repository(For pull request)</span>
        <span class="na">if</span><span class="pi">:</span> <span class="s">${{ github.event_name == 'pull_request' || github.event_name == 'pull_request_target' }}</span>
        <span class="na">uses</span><span class="pi">:</span> <span class="s">actions/checkout@v2</span>
        <span class="na">with</span><span class="pi">:</span>
          <span class="na">repository</span><span class="pi">:</span> <span class="s">${{ github.event.pull_request.head.repo.full_name }}</span>
          <span class="na">ref</span><span class="pi">:</span> <span class="s">${{ github.event.pull_request.head.ref }}</span>

      <span class="pi">-</span> <span class="na">name</span><span class="pi">:</span> <span class="s">Compile Notebooks(For pull request)</span>
        <span class="na">if</span><span class="pi">:</span> <span class="s">${{ github.event_name == 'pull_request' || github.event_name == 'pull_request_target' }}</span>
        <span class="na">run</span><span class="pi">:</span> <span class="pi">|</span>
          <span class="s">python -m pip install --quiet -e .[extras]</span>
          <span class="s">./tools/batch/batch_states/compile_notebooks.sh \</span>
                 <span class="s">"#PR-${{ github.event.number }}" "${{ github.run_number }}" \</span>
                 <span class="s">"${{ github.event.pull_request.head.repo.full_name }}" "${{ github.event.pull_request.head.ref }}"</span>
          <span class="s">exit $?</span>
<span class="s">...</span>
      <span class="s">- name</span><span class="pi">:</span> <span class="s">Copy docs to AWS S3(For pull request)</span>
        <span class="s">if</span><span class="pi">:</span> <span class="s">${{ (failure() || success()) &amp;&amp; (github.event_name == 'pull_request' || github.event_name == 'pull_request_target') }}</span>
        <span class="s">run</span><span class="pi">:</span> <span class="pi">|</span>
          <span class="s">echo "Uploading docs to s3://gluon-nlp-staging/PR${{ github.event.number }}/${{ github.event.pull_request.head.ref }}/"</span>
          <span class="s">aws s3 sync --delete ./docs/_build/html/ s3://gluon-nlp-staging/PR${{ github.event.number }}/${{ github.event.pull_request.head.ref }}/ --acl public-read</span>
</code></pre></div></div>

<p>_unittests-gpu.yml:__</p>

<div class="language-yaml highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="na">on</span><span class="pi">:</span> <span class="pi">[</span><span class="nv">push</span><span class="pi">,</span> <span class="nv">pull_request_target</span><span class="pi">]</span>
<span class="nn">...</span>
      <span class="pi">-</span> <span class="na">name</span><span class="pi">:</span> <span class="s">Test project on AWS Batch(For pull request)</span>
        <span class="na">if</span><span class="pi">:</span> <span class="s">${{ github.event_name == 'pull_request' || github.event_name == 'pull_request_target' }}</span>
        <span class="na">run</span><span class="pi">:</span> <span class="pi">|</span>
          <span class="s">echo "Start submitting job"</span>
          <span class="s">python ./tools/batch/submit-job.py --region us-east-1 \</span>
                                             <span class="s">--job-type g4dn.4x \</span>
                                             <span class="s">--name GluonNLP-GPU-Test-PR#${{ github.event.number }} \</span>
                                             <span class="s">--source-ref ${{ github.event.pull_request.head.ref }} \</span>
<span class="s">...</span>
</code></pre></div></div>

<h4 id="impact-1">Impact</h4>

<p>This vulnerability allows for arbitrary command injection into the bash script which allows for unauthorized modification of the base repository and secrets exfiltration. For a Proof of Concept create a PR from branch named <code class="language-plaintext highlighter-rouge">a";echo${IFS}"hello"#</code>.</p>

<h2 id="credit">Credit</h2>

<p>This issue was discovered and reported by GHSL team member <a href="https://github.com/JarLob">@JarLob (Jaroslav Lobačevski)</a>.</p>

<h2 id="contact">Contact</h2>

<p>You can contact the GHSL team at <code class="language-plaintext highlighter-rouge">securitylab@github.com</code>, please include a reference to <code class="language-plaintext highlighter-rouge">GHSL-2021-007</code> in any communication regarding this issue.</p>

   