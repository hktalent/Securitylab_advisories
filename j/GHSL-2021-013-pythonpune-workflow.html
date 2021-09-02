<header class="post-header d-block mb-6">
      <div class="date text-mono f5 my-3">February 3, 2021</div>
      <h1 class="my-2 h00-mktg lh-condensed">GHSL-2021-013: Command injection in pythonpune/meetup-talks workflow</h1>

      
      
      
      
      

      

      <a target="_blank" class="sc-frDJqD SgxRc d-inline-flex flex-row flex-items-center text-gray" href="https://github.com/jarlob">
        <img class="mr-3" src="https://avatars.githubusercontent.com/u/26652396?s=35" height="35" width="35">
        <span>Jaroslav Lobacevski</span>
      </a>
    </header>

    <main id="content" class="markdown-body" aria-label="Content">
      <h2 id="coordinated-disclosure-timeline">Coordinated Disclosure Timeline</h2>

<ul>
  <li>2021-01-18-2021-01-21: Report sent to various maintainers.</li>
  <li>2021-01-22: Maintainers acknowledged.</li>
  <li>2021-01-22: Issue resolved.</li>
</ul>

<h2 id="summary">Summary</h2>

<p>GitHub workflow in <a href="https://github.com/pythonpune/meetup-talks">pythonpune/meetup-talks GitHub repository</a> repository is vulnerable to arbitrary code execution from user comments.</p>

<h2 id="product">Product</h2>

<p><a href="https://github.com/pythonpune/meetup-talks">pythonpune/meetup-talks GitHub repository</a> repository</p>

<h2 id="tested-version">Tested Version</h2>

<p>The latest changeset <a href="https://github.com/pythonpune/meetup-talks/blob/4d8b6b85f86b0bc1e20a7a5aea62838e55e29e04/.github/workflows/notifications.yml">notifications.yml</a> to the date.</p>

<h2 id="details">Details</h2>

<h3 id="issue-a-comment-body-is-used-to-format-a-shell-command">Issue: A comment body is used to format a shell command</h3>

<div class="language-yaml highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="na">on</span><span class="pi">:</span>
  <span class="na">issue_comment</span><span class="pi">:</span>
    <span class="na">types</span><span class="pi">:</span> <span class="pi">[</span><span class="nv">created</span><span class="pi">]</span>
  <span class="na">issues</span><span class="pi">:</span>
    <span class="na">types</span><span class="pi">:</span> <span class="pi">[</span><span class="nv">opened</span><span class="pi">]</span>
<span class="nn">...</span>
      <span class="pi">-</span> <span class="na">name</span><span class="pi">:</span> <span class="s">comment</span>
        <span class="na">run</span><span class="pi">:</span> <span class="s">echo "${{ github.event.comment.body }}"</span>
</code></pre></div></div>

<h4 id="impact">Impact</h4>

<p>This vulnerability allows for arbitrary command injection into the bash script which allows for unauthorized modification of the base repository and secrets exfiltration. For a proof a concept comment on an issue with <code class="language-plaintext highlighter-rouge">a"; exit 1</code>.</p>

<h2 id="credit">Credit</h2>

<p>This issue was discovered and reported by GHSL team member <a href="https://github.com/JarLob">@JarLob (Jaroslav Lobačevski)</a>.</p>

<h2 id="contact">Contact</h2>

<p>You can contact the GHSL team at <code class="language-plaintext highlighter-rouge">securitylab@github.com</code>, please include a reference to <code class="language-plaintext highlighter-rouge">GHSL-2021-013</code> in any communication regarding this issue.</p>

   