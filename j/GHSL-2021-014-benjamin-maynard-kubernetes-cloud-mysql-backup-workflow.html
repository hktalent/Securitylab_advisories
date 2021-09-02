<header class="post-header d-block mb-6">
      <div class="date text-mono f5 my-3">February 3, 2021</div>
      <h1 class="my-2 h00-mktg lh-condensed">GHSL-2021-014: Command injection in benjamin-maynard/kubernetes-cloud-mysql-backup workflow</h1>

      
      
      
      
      

      

      <a target="_blank" class="sc-frDJqD SgxRc d-inline-flex flex-row flex-items-center text-gray" href="https://github.com/jarlob">
        <img class="mr-3" src="https://avatars.githubusercontent.com/u/26652396?s=35" height="35" width="35">
        <span>Jaroslav Lobacevski</span>
      </a>
    </header>

    <main id="content" class="markdown-body" aria-label="Content">
      <h2 id="coordinated-disclosure-timeline">Coordinated Disclosure Timeline</h2>

<ul>
  <li>2021-01-18: Report sent to maintainers.</li>
  <li>2021-01-21: Maintainers acknowledged.</li>
  <li>2021-01-21: Issue resolved.</li>
</ul>

<h2 id="summary">Summary</h2>

<p>GitHub workflow in <a href="https://github.com/benjamin-maynard/kubernetes-cloud-mysql-backup">benjamin-maynard/kubernetes-cloud-mysql-backup GitHub repository</a> repository is vulnerable to arbitrary code execution from user comments.</p>

<h2 id="product">Product</h2>

<p><a href="https://github.com/benjamin-maynard/kubernetes-cloud-mysql-backup">benjamin-maynard/kubernetes-cloud-mysql-backup GitHub repository</a> repository</p>

<h2 id="tested-version">Tested Version</h2>

<p>The latest changeset <a href="https://github.com/benjamin-maynard/kubernetes-cloud-mysql-backup/blob/7511b2809d8a79df027bfe2e672b0dbb015067bc/.github/workflows/run-pr-tests.yaml">run-pr-tests.yaml</a> to the date.</p>

<h2 id="details">Details</h2>

<h3 id="issue-a-comment-body-is-used-to-format-a-shell-command">Issue: A comment body is used to format a shell command</h3>

<div class="language-yaml highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="na">on</span><span class="pi">:</span> 
  <span class="na">issue_comment</span><span class="pi">:</span>
    <span class="na">types</span><span class="pi">:</span> <span class="pi">[</span><span class="nv">created</span><span class="pi">]</span>
<span class="nn">...</span>
        <span class="na">run</span><span class="pi">:</span> <span class="pi">|</span>
          <span class="s">echo "Comment Creator: ${{ github.event.comment.user.login }}"</span>
          <span class="s">echo "Comment Body: ${{ github.event.comment.body }}"</span>
          <span class="s">exit 1</span>
</code></pre></div></div>

<h4 id="impact">Impact</h4>

<p>This vulnerability allows for arbitrary command injection into the bash script which allows for unauthorized modification of the base repository and secrets exfiltration. For a proof a concept on a pull request with <code class="language-plaintext highlighter-rouge">a"; exit 0</code>.</p>

<h2 id="credit">Credit</h2>

<p>This issue was discovered and reported by GHSL team member <a href="https://github.com/JarLob">@JarLob (Jaroslav Lobačevski)</a>.</p>

<h2 id="contact">Contact</h2>

<p>You can contact the GHSL team at <code class="language-plaintext highlighter-rouge">securitylab@github.com</code>, please include a reference to <code class="language-plaintext highlighter-rouge">GHSL-2021-014</code> in any communication regarding this issue.</p>

   