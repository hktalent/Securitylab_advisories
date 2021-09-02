<header class="post-header d-block mb-6">
      <div class="date text-mono f5 my-3">February 3, 2021</div>
      <h1 class="my-2 h00-mktg lh-condensed">GHSL-2020-234: Command injection in DataBiosphere/terra-workspace-manager workflow</h1>

      
      
      
      
      

      

      <a target="_blank" class="sc-frDJqD SgxRc d-inline-flex flex-row flex-items-center text-gray" href="https://github.com/jarlob">
        <img class="mr-3" src="https://avatars.githubusercontent.com/u/26652396?s=35" height="35" width="35">
        <span>Jaroslav Lobacevski</span>
      </a>
    </header>

    <main id="content" class="markdown-body" aria-label="Content">
      <h2 id="coordinated-disclosure-timeline">Coordinated Disclosure Timeline</h2>

<ul>
  <li>2020-11-23-2020-12-01: Report sent to various maintainers.</li>
  <li>2020-12-01: Report acknowledged.</li>
  <li>2020-12-07: Issue resolved.</li>
</ul>

<h2 id="summary">Summary</h2>

<p>The <a href="https://github.com/DataBiosphere/terra-workspace-manager/blob/dev/.github/workflows/preview-manage.yml">‘preview-manage.yml’ GitHub workflow</a> is vulnerable to arbitrary command injection.</p>

<h2 id="product">Product</h2>

<p><a href="https://github.com/DataBiosphere/terra-workspace-manager">DataBiosphere/terra-workspace-manager GitHub repository</a></p>

<h2 id="tested-version">Tested Version</h2>

<p><a href="https://github.com/DataBiosphere/terra-workspace-manager/blob/00ce0674be3f9270c69bf527096aafcbb164324e/.github/workflows/preview-manage.yml">preview-manage.yml</a></p>

<h2 id="details">Details</h2>

<h3 id="issue-the-body-of-issue-comment-is-used-to-format-a-shell-command">Issue: The body of issue comment is used to format a shell command</h3>

<p>An issue comment is used to format a bash script like:</p>

<div class="language-yaml highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="na">on</span><span class="pi">:</span>
  <span class="na">issue_comment</span><span class="pi">:</span>
    <span class="na">types</span><span class="pi">:</span> <span class="pi">[</span><span class="nv">created</span><span class="pi">]</span>
<span class="nn">...</span>
    <span class="pi">-</span> <span class="na">name</span><span class="pi">:</span> <span class="s">Construct version override JSON</span>
      <span class="na">id</span><span class="pi">:</span> <span class="s">versions-override</span>
      <span class="na">run</span><span class="pi">:</span> <span class="pi">|</span>
        <span class="s">comment='${{ github.event.comment.body }}'</span>
<span class="s">...</span>
</code></pre></div></div>

<h4 id="impact">Impact</h4>

<p>This vulnerability allows for arbitrary command injection into the bash script that may allow exfiltration of the secret tokens to the attacker controlled server. For a proof a concept an issue comment with the following title <code class="language-plaintext highlighter-rouge">preview-create'; echo "test" #</code> will print <code class="language-plaintext highlighter-rouge">test</code> in the log.</p>

<h2 id="credit">Credit</h2>

<p>This issue was discovered and reported by GHSL team member <a href="https://github.com/JarLob">@JarLob (Jaroslav Lobačevski)</a>.</p>

<h2 id="contact">Contact</h2>

<p>You can contact the GHSL team at <code class="language-plaintext highlighter-rouge">securitylab@github.com</code>, please include a reference to <code class="language-plaintext highlighter-rouge">GHSL-2020-234</code> in any communication regarding this issue.</p>
