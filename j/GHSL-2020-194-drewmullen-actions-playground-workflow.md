<header class="post-header d-block mb-6">
      <div class="date text-mono f5 my-3">February 3, 2021</div>
      <h1 class="my-2 h00-mktg lh-condensed">GHSL-2020-194: Command injection in drewmullen/actions-playground workflows</h1>

      
      
      
      
      

      

      <a target="_blank" class="sc-frDJqD SgxRc d-inline-flex flex-row flex-items-center text-gray" href="https://github.com/jarlob">
        <img class="mr-3" src="https://avatars.githubusercontent.com/u/26652396?s=35" height="35" width="35">
        <span>Jaroslav Lobacevski</span>
      </a>
    </header>

    <main id="content" class="markdown-body" aria-label="Content">
      <h2 id="coordinated-disclosure-timeline">Coordinated Disclosure Timeline</h2>

<ul>
  <li>2020-10-16: Report sent to maintainers.</li>
  <li>2020-12-01: Maintainers acknowledged.</li>
  <li>2021-01-14: 90 days passed since report was sent.</li>
</ul>

<h2 id="summary">Summary</h2>

<p>The <a href="https://github.com/drewmullen/actions-playground/blob/master/.github/workflows/comment.yml">comment.yml</a> and <a href="https://github.com/drewmullen/actions-playground/blob/master/.github/workflows/output_comment.yml">output_comment.yml</a> GitHub workflows are vulnerable to arbitrary command injection.</p>

<h2 id="product">Product</h2>

<p><a href="https://github.com/drewmullen/actions-playground">drewmullen/actions-playground GitHub repository</a></p>

<h2 id="tested-version">Tested Version</h2>

<p><a href="https://github.com/drewmullen/actions-playground/blob/master/.github/workflows/comment.yml">comment.yml</a> and <a href="https://github.com/drewmullen/actions-playground/blob/master/.github/workflows/output_comment.yml">output_comment.yml</a> GitHub workflows from the master branch.</p>

<h2 id="details">Details</h2>

<h3 id="issue-the-pull-request-comment-is-used-to-format-a-shell-command">Issue: The Pull Request comment is used to format a shell command</h3>

<p>When a user comments on a Pull Request with <code class="language-plaintext highlighter-rouge">build</code> or <code class="language-plaintext highlighter-rouge">echo</code> it automatically starts the <a href="https://github.com/drewmullen/actions-playground/blob/master/.github/workflows/comment.yml">comment.yml</a> or <a href="https://github.com/drewmullen/actions-playground/blob/master/.github/workflows/output_comment.yml">output_comment.yml</a> GitHub workflows. The comment text is used to format a bash script.</p>

<div class="language-yaml highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="na">on</span><span class="pi">:</span>
  <span class="na">issue_comment</span><span class="pi">:</span>
    <span class="na">types</span><span class="pi">:</span> <span class="pi">[</span><span class="nv">created</span><span class="pi">]</span>
<span class="na">jobs</span><span class="pi">:</span>
  <span class="na">build</span><span class="pi">:</span>
    <span class="na">if</span><span class="pi">:</span> <span class="pi">&gt;</span>
      <span class="s">startsWith(github.event.comment.body, 'build')</span>
      <span class="s">&amp;&amp; startsWith(github.event.issue.pull_request.url, 'https://')</span>
    <span class="na">runs-on</span><span class="pi">:</span> <span class="s">ubuntu-latest</span>
    <span class="na">steps</span><span class="pi">:</span>
    <span class="pi">-</span> <span class="na">name</span><span class="pi">:</span> <span class="s">print comment body</span>
      <span class="na">run</span><span class="pi">:</span> <span class="s">echo ${{ github.event.comment.body }}</span>
  
    <span class="pi">-</span> <span class="na">name</span><span class="pi">:</span> <span class="s">set body comments</span>
      <span class="na">run</span><span class="pi">:</span> <span class="pi">|</span>
        <span class="s">set -eu</span>
        <span class="s">build_dir=$( cut -d ' ' -f 2 &lt;&lt;&lt; '${{ github.event.comment.body }}' )</span>
        <span class="s">buckets=$( cut -d ' ' -f 3- &lt;&lt;&lt; "${{ github.event.comment.body }}" )</span>
<span class="s">...</span>
</code></pre></div></div>
<p>and</p>
<div class="language-yaml highlighter-rouge"><div class="highlight"><pre class="highlight"><code>
<span class="na">on</span><span class="pi">:</span>
  <span class="na">issue_comment</span><span class="pi">:</span>
    <span class="na">types</span><span class="pi">:</span> <span class="pi">[</span><span class="nv">created</span><span class="pi">]</span>
<span class="na">jobs</span><span class="pi">:</span>
  <span class="na">echo-chamber</span><span class="pi">:</span>
    <span class="na">if</span><span class="pi">:</span> <span class="pi">&gt;</span>
      <span class="s">startsWith(github.event.comment.body, 'echo')</span>
      <span class="s">&amp;&amp; startsWith(github.event.issue.pull_request.url, 'https://')</span>
    <span class="na">runs-on</span><span class="pi">:</span> <span class="s">ubuntu-latest</span>
    <span class="na">steps</span><span class="pi">:</span>
    <span class="pi">-</span> <span class="na">uses</span><span class="pi">:</span> <span class="s">actions/checkout@v2</span>
<span class="nn">...</span>
    <span class="pi">-</span> <span class="na">name</span><span class="pi">:</span> <span class="s">set body comments</span>
      <span class="na">id</span><span class="pi">:</span> <span class="s">listen</span>
      <span class="na">run</span><span class="pi">:</span> <span class="pi">|</span>
        <span class="s">set -eu</span>
        <span class="s">content=$( cut -d ' ' -f 2 &lt;&lt;&lt; '${{ github.event.comment.body }}' )</span>
</code></pre></div></div>

<h4 id="impact">Impact</h4>

<p>The repository is vulnerable itself and demonstrates unsafe practices that allow for arbitrary command injection into a bash script. For a Proof of Concept comment with <code class="language-plaintext highlighter-rouge">build; exit 1</code>.<br />
This arbitrary command injection potentially allows exfiltration of secrets used by the build runner. To make the attack less visible the attacker may modify the comment later.</p>

<h2 id="credit">Credit</h2>

<p>This issue was discovered and reported by GHSL team member <a href="https://github.com/JarLob">@JarLob (Jaroslav Lobačevski)</a>.</p>

<h2 id="contact">Contact</h2>

<p>You can contact the GHSL team at <code class="language-plaintext highlighter-rouge">securitylab@github.com</code>, please include a reference to <code class="language-plaintext highlighter-rouge">GHSL-2020-194</code> in any communication regarding this issue.</p>

   