<header class="post-header d-block mb-6">
      <div class="date text-mono f5 my-3">February 3, 2021</div>
      <h1 class="my-2 h00-mktg lh-condensed">GHSL-2021-012: Command injection in alan-turing-institute/binderhub-deploy workflow</h1>

      
      
      
      
      

      

      <a target="_blank" class="sc-frDJqD SgxRc d-inline-flex flex-row flex-items-center text-gray" href="https://github.com/jarlob">
        <img class="mr-3" src="https://avatars.githubusercontent.com/u/26652396?s=35" height="35" width="35">
        <span>Jaroslav Lobacevski</span>
      </a>
    </header>

    <main id="content" class="markdown-body" aria-label="Content">
      <h2 id="coordinated-disclosure-timeline">Coordinated Disclosure Timeline</h2>

<ul>
  <li>2021-01-18: Report sent to maintainers.</li>
  <li>2021-01-19: Issue resolved.</li>
</ul>

<h2 id="summary">Summary</h2>

<p>GitHub workflow in <a href="https://github.com/alan-turing-institute/binderhub-deploy">alan-turing-institute/binderhub-deploy GitHub repository</a> repository is vulnerable to arbitrary code execution from user comments.</p>

<h2 id="product">Product</h2>

<p><a href="https://github.com/alan-turing-institute/binderhub-deploy">alan-turing-institute/binderhub-deploy GitHub repository</a> repository</p>

<h2 id="tested-version">Tested Version</h2>

<p>The latest changeset <a href="https://github.com/alan-turing-institute/binderhub-deploy/blob/7cb770e9d5bdc947dce623273301c9127774c97b/.github/workflows/auto-version-bump.yml">auto-version-bump.yml</a> to the date.</p>

<h2 id="details">Details</h2>

<h3 id="issue-a-comment-body-is-used-to-format-a-shell-command">Issue: A comment body is used to format a shell command</h3>

<div class="language-yaml highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="na">on</span><span class="pi">:</span>
  <span class="na">issue_comment</span><span class="pi">:</span>
    <span class="na">types</span><span class="pi">:</span> <span class="pi">[</span><span class="s2">"</span><span class="s">created"</span><span class="pi">]</span>

<span class="na">jobs</span><span class="pi">:</span>
  <span class="na">bump-version</span><span class="pi">:</span>
    <span class="na">if</span><span class="pi">:</span> <span class="s">(</span>
          <span class="s">(github.event.issue.pull_request != </span><span class="no">null</span><span class="s">) &amp;&amp;</span>
          <span class="s">contains(github.event.comment.body, '/bump-version')</span>
        <span class="s">)</span>
<span class="nn">...</span>
      <span class="pi">-</span> <span class="na">name</span><span class="pi">:</span> <span class="s">Pull version from comment body</span>
        <span class="na">run</span><span class="pi">:</span> <span class="pi">|</span>
          <span class="s">NEW_VERSION=$(echo ${{ github.event.comment.body }} | grep '/bump-version' | cut -d" " -f2)</span>
</code></pre></div></div>

<h4 id="impact">Impact</h4>

<p>This vulnerability allows for arbitrary command injection into the bash script which allows for unauthorized modification of the base repository and secrets exfiltration. For a proof a concept create comment on an issue with <code class="language-plaintext highlighter-rouge">/bump-version); echo "test"; #</code>.</p>

<h2 id="credit">Credit</h2>

<p>This issue was discovered and reported by GHSL team member <a href="https://github.com/JarLob">@JarLob (Jaroslav Lobačevski)</a>.</p>

<h2 id="contact">Contact</h2>

<p>You can contact the GHSL team at <code class="language-plaintext highlighter-rouge">securitylab@github.com</code>, please include a reference to <code class="language-plaintext highlighter-rouge">GHSL-2021-012</code> in any communication regarding this issue.</p>

   