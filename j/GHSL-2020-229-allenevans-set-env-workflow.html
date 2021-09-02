<header class="post-header d-block mb-6">
      <div class="date text-mono f5 my-3">February 3, 2021</div>
      <h1 class="my-2 h00-mktg lh-condensed">GHSL-2020-229: Command injection in allenevans/set-env workflow</h1>

      
      
      
      
      

      

      <a target="_blank" class="sc-frDJqD SgxRc d-inline-flex flex-row flex-items-center text-gray" href="https://github.com/jarlob">
        <img class="mr-3" src="https://avatars.githubusercontent.com/u/26652396?s=35" height="35" width="35">
        <span>Jaroslav Lobacevski</span>
      </a>
    </header>

    <main id="content" class="markdown-body" aria-label="Content">
      <h2 id="coordinated-disclosure-timeline">Coordinated Disclosure Timeline</h2>

<ul>
  <li>2020-11-23: Report sent to maintainer</li>
  <li>2020-11-24: Issue resolved</li>
</ul>

<h2 id="summary">Summary</h2>

<p>The <a href="https://github.com/allenevans/set-env/blob/master/.github/workflows/release.yml">‘release.yml’ GitHub workflow</a> is vulnerable to arbitrary command injection.</p>

<h2 id="product">Product</h2>

<p><a href="https://github.com/allenevans/set-env">allenevans/set-env GitHub repository</a></p>

<h2 id="tested-version">Tested Version</h2>

<p><a href="https://github.com/allenevans/set-env/blob/f69c6b5dd25d0170bed3f414d9a779e744ce4928/.github/workflows/release.yml">release.yml</a></p>

<h2 id="details">Details</h2>

<h3 id="issue-a-commit-comment-is-used-to-format-a-shell-command">Issue: A commit comment is used to format a shell command</h3>

<p>A commit comment is used to format a bash script in step <code class="language-plaintext highlighter-rouge">Config</code>:</p>

<div class="language-yaml highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="na">on</span><span class="pi">:</span>
  <span class="na">push</span><span class="pi">:</span>
    <span class="na">branches</span><span class="pi">:</span>
      <span class="pi">-</span> <span class="s1">'</span><span class="s">master'</span>
<span class="nn">...</span>
        <span class="na">run</span><span class="pi">:</span> <span class="pi">|</span>
          <span class="s">echo "Release triggered by ${{github.actor}}"</span>
          <span class="s">echo "Commit ${{github.event.commits[0].message}}"</span>
<span class="s">...</span>
</code></pre></div></div>

<p>An attacker may put the payload in a commit description and make a valid pull request, that will be merged. It is likely that the reviewer will not notice it, especially if there are multiple commits in the single PR.</p>

<h4 id="impact">Impact</h4>

<p>This vulnerability allows for arbitrary command injection into the bash script. The attacker may exfiltrate secret tokens to the attacker controlled server, can make arbitrary commit to the repository or subvert the release step directly, that in turn will affect all repositories that depend on the action.</p>

<h2 id="credit">Credit</h2>

<p>This issue was discovered and reported by GHSL team member <a href="https://github.com/JarLob">@JarLob (Jaroslav Lobačevski)</a>.</p>

<h2 id="contact">Contact</h2>

<p>You can contact the GHSL team at <code class="language-plaintext highlighter-rouge">securitylab@github.com</code>, please include a reference to <code class="language-plaintext highlighter-rouge">GHSL-2020-229</code> in any communication regarding this issue.</p>
