<header class="post-header d-block mb-6">
      <div class="date text-mono f5 my-3">February 3, 2021</div>
      <h1 class="my-2 h00-mktg lh-condensed">GHSL-2020-370: Arbitrary code execution and shell command injection in rhinstaller/anaconda workflows</h1>

      
      
      
      
      

      

      <a target="_blank" class="sc-frDJqD SgxRc d-inline-flex flex-row flex-items-center text-gray" href="https://github.com/jarlob">
        <img class="mr-3" src="https://avatars.githubusercontent.com/u/26652396?s=35" height="35" width="35">
        <span>Jaroslav Lobacevski</span>
      </a>
    </header>

    <main id="content" class="markdown-body" aria-label="Content">
      <h2 id="coordinated-disclosure-timeline">Coordinated Disclosure Timeline</h2>

<ul>
  <li>2020-12-22: Report sent to maintainer.</li>
  <li>2020-12-23: Vendor acknowledges report receipt.</li>
  <li>2020-12-23-2021-01-22: Conversation about possible remediation.</li>
  <li>2021-01-22: Issue resolved.</li>
</ul>

<h2 id="summary">Summary</h2>

<p>The <a href="https://github.com/rhinstaller/anaconda/blob/master/.github/workflows/validate.yml">validate.yml</a>and <a href="https://github.com/rhinstaller/anaconda/blob/master/.github/workflows/kickstart-tests.yml">kickstart-tests.yml</a> GitHub workflows are vulnerable to unauthorized modification of the base repository or secrets exfiltration from a Pull Request.</p>

<h2 id="product">Product</h2>

<p><a href="https://github.com/rhinstaller/anaconda">rhinstaller/anaconda</a> GitHub repository</p>

<h2 id="tested-version">Tested Version</h2>

<p>The latest changesets <a href="https://github.com/rhinstaller/anaconda/blob/c0044f04e768e5356321e1b829f1a6c9a53bc8c5/.github/workflows/validate.yml">c0044f0</a> and <a href="https://github.com/rhinstaller/anaconda/blob/9be8294344529475fbd01a867fba2120642ecb02/.github/workflows/kickstart-tests.yml">9be8294</a> to the date.</p>

<h2 id="details">Details</h2>

<h3 id="issue-1-untrusted-code-is-explicitly-checked-out-and-run-on-a-pull-request-from-a-fork">Issue 1: Untrusted code is explicitly checked out and run on a Pull Request from a fork</h3>

<p>Workflows triggered on <code class="language-plaintext highlighter-rouge">pull_request_target</code> have read/write tokens for the base repository and the access to secrets. By explicitly checking out and running the build script from a fork the untrusted code is running in an environment that is able to push to the base repository and to access secrets. More details can be found in the article <a href="https://securitylab.github.com/research/github-actions-preventing-pwn-requests/">Keeping your GitHub Actions and workflows secure: Preventing pwn requests</a>.</p>

<div class="language-yaml highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="na">on</span><span class="pi">:</span> <span class="pi">[</span><span class="nv">push</span><span class="pi">,</span> <span class="nv">pull_request_target</span><span class="pi">]</span>
<span class="nn">...</span>
      <span class="pi">-</span> <span class="na">name</span><span class="pi">:</span> <span class="s">Clone repository</span>
        <span class="na">uses</span><span class="pi">:</span> <span class="s">actions/checkout@v2</span>
        <span class="na">with</span><span class="pi">:</span>
          <span class="c1"># otherwise we are testing target branch instead of the PR branch (see pull_request_target trigger)</span>
          <span class="na">ref</span><span class="pi">:</span> <span class="s">${{ github.event.pull_request.head.sha }}</span>
          <span class="na">fetch-depth</span><span class="pi">:</span> <span class="m">0</span>
<span class="nn">...</span>
      <span class="pi">-</span> <span class="na">name</span><span class="pi">:</span> <span class="s">Build anaconda-ci container</span>
        <span class="c1"># FIXME: always build ELN container, until we publish it to quay.io</span>
        <span class="na">if</span><span class="pi">:</span> <span class="s">steps.check-dockerfile-changed.outputs.changed || matrix.release == 'eln'</span>
        <span class="na">run</span><span class="pi">:</span> <span class="s">make -f Makefile.am anaconda-ci-build</span>
<span class="nn">...</span>
</code></pre></div></div>

<h4 id="impact">Impact</h4>

<p>The vulnerability allows for unauthorized modification of the base repository and secrets exfiltration.</p>

<h3 id="issue-2-a-comment-body-is-used-to-format-a-shell-command">Issue 2: A comment body is used to format a shell command</h3>

<div class="language-yaml highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="na">on</span><span class="pi">:</span>
  <span class="na">issue_comment</span><span class="pi">:</span>
    <span class="na">types</span><span class="pi">:</span> <span class="pi">[</span><span class="nv">created</span><span class="pi">]</span>
<span class="nn">...</span>
    <span class="na">if</span><span class="pi">:</span> <span class="s">startsWith(github.event.comment.body, '/kickstart-test')</span>
<span class="nn">...</span>
      <span class="pi">-</span> <span class="na">name</span><span class="pi">:</span> <span class="s">Parse launch arguments</span>
        <span class="na">id</span><span class="pi">:</span> <span class="s">parse_launch_args</span>
        <span class="na">run</span><span class="pi">:</span> <span class="pi">|</span>
          <span class="s"># extract first line and cut out the "/kickstart-tests" first word</span>
          <span class="s">LAUNCH_ARGS=$(echo '$' | sed -n '1 s/^[^ ]* *//p')</span>
          <span class="s">echo "::set-output name=launch_args::${LAUNCH_ARGS}"</span>
</code></pre></div></div>

<h4 id="impact-1">Impact</h4>

<p>This vulnerability allows for arbitrary command injection into the bash script which allows for unauthorized modification of the base repository and secrets exfiltration. For a proof a concept comment on an issue with <code class="language-plaintext highlighter-rouge">/kickstart-test'); echo 'test' #</code>.</p>

<h2 id="credit">Credit</h2>

<p>This issue was discovered and reported by GHSL team member <a href="https://github.com/JarLob">@JarLob (Jaroslav Lobačevski)</a>.</p>

<h2 id="contact">Contact</h2>

<p>You can contact the GHSL team at <code class="language-plaintext highlighter-rouge">securitylab@github.com</code>, please include a reference to <code class="language-plaintext highlighter-rouge">GHSL-2020-370</code> in any communication regarding this issue.</p>

   