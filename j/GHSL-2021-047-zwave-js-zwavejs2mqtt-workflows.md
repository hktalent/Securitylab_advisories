<header class="post-header d-block mb-6">
      <div class="date text-mono f5 my-3">April 1, 2021</div>
      <h1 class="my-2 h00-mktg lh-condensed">GHSL-2021-047: unauthorized repository modification or secrets exfiltration in GitHub workflows of zwavejs2mqtt</h1>

      
      
      
      
      

      

      <a target="_blank" class="sc-frDJqD SgxRc d-inline-flex flex-row flex-items-center text-gray" href="https://github.com/jarlob">
        <img class="mr-3" src="https://avatars.githubusercontent.com/u/26652396?s=35" height="35" width="35">
        <span>Jaroslav Lobacevski</span>
      </a>
    </header>

    <main id="content" class="markdown-body" aria-label="Content">
      
<h2 id="coordinated-disclosure-timeline">Coordinated Disclosure Timeline</h2>

<ul>
  <li>2021-02-04: Issue reported to maintainers</li>
  <li>2021-02-04: Report acknowledged</li>
  <li>2021-02-12: Issue fixed</li>
</ul>

<h2 id="summary">Summary</h2>

<p>The <a href="https://github.com/zwave-js/zwavejs2mqtt/blob/master/.github/workflows/zwave-js-bot.yml">zwave-js-bot.yml</a> GitHub workflow is vulnerable to unauthorized modification of the base repository or secrets exfiltration.</p>

<h2 id="product">Product</h2>

<p><a href="https://github.com/zwave-js/zwavejs2mqtt">zwave-js/zwavejs2mqtt</a> repository</p>

<h2 id="tested-version">Tested Version</h2>

<p>The latest changeset of <a href="https://github.com/zwave-js/zwavejs2mqtt/blob/e758e76c3a7015d9a8cbb901e344dfba00a25d82/.github/workflows/zwave-js-bot.yml">zwave-js-bot.yml</a> to the date.</p>

<h2 id="details">Details</h2>

<h3 id="issue-1-a-specific-comment-triggers-a-potentially-untrusted-pull-request-build-in-a-privileged-environment">Issue 1: A specific comment triggers a potentially untrusted pull request build in a privileged environment</h3>

<p>When a user comments on a pull request with <code class="language-plaintext highlighter-rouge">@zwave-js-bot fix lint</code> it triggers the following workflow which checks out the pull request and builds the potentially untrusted code:</p>

<div class="language-yaml highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="na">on</span><span class="pi">:</span>
  <span class="na">issue_comment</span><span class="pi">:</span>
    <span class="na">types</span><span class="pi">:</span> <span class="pi">[</span><span class="nv">created</span><span class="pi">]</span> <span class="c1"># edited, deleted</span>
<span class="nn">...</span>
  <span class="c1"># Fix lint errors when an authorized person posts "@zwave-js-bot fix lint"</span>
  <span class="na">fix-lint</span><span class="pi">:</span>
    <span class="na">if</span><span class="pi">:</span> <span class="pi">|</span>
      <span class="s">contains(github.event.issue.html_url, '/pull/') &amp;&amp;</span>
      <span class="s">contains(github.event.comment.body, '@zwave-js-bot fix lint') &amp;&amp;</span>
      <span class="s">(github.event.comment.user.login != 'zwave-js-bot') &amp;&amp; github.event.comment.user.login != 'zwave-js-assistant[bot]'</span>
<span class="s">...</span>
      <span class="s">- name</span><span class="pi">:</span> <span class="s">Check user's permissions to do this</span>
        <span class="s">id</span><span class="pi">:</span> <span class="s">check</span>
        <span class="s">uses</span><span class="pi">:</span> <span class="s">actions/github-script@v3</span>
        <span class="s">with</span><span class="pi">:</span>
          <span class="na">github-token</span><span class="pi">:</span> <span class="s">${{secrets.BOT_TOKEN}}</span>
          <span class="na">result-encoding</span><span class="pi">:</span> <span class="s">string</span>
          <span class="na">script</span><span class="pi">:</span> <span class="pi">|</span>
            <span class="s">const bot = require(`${process.env.GITHUB_WORKSPACE}/.github/bot-scripts/index.js`);</span>
            <span class="s">return await bot.checkAuthorized({github, context});</span>
<span class="s">...</span>
      <span class="s">- name</span><span class="pi">:</span> <span class="s">Checkout pull request</span>
        <span class="s">if</span><span class="pi">:</span> <span class="s">steps.check.outputs.result == 'true'</span>
        <span class="s">uses</span><span class="pi">:</span> <span class="s">actions/checkout@v2</span>
        <span class="s">with</span><span class="pi">:</span>
          <span class="na">token</span><span class="pi">:</span> <span class="s">${{secrets.BOT_TOKEN}}</span>
          <span class="na">repository</span><span class="pi">:</span> <span class="s">${{ fromJSON(steps.get-pr.outputs.result).head.repo.full_name }}</span>
          <span class="na">ref</span><span class="pi">:</span> <span class="s">${{ fromJSON(steps.get-pr.outputs.result).head.ref }}</span>
<span class="nn">...</span>
      <span class="pi">-</span> <span class="na">name</span><span class="pi">:</span> <span class="s">Install dependencies</span>
        <span class="na">if</span><span class="pi">:</span> <span class="s">steps.check.outputs.result == 'true'</span>
        <span class="na">run</span><span class="pi">:</span> <span class="s">npm install</span>
</code></pre></div></div>

<p>The <code class="language-plaintext highlighter-rouge">checkAuthorized</code> script verifies that the user is authorized to trigger the workflow. However it also allows the pull request author to trigger the workflow:</p>

<div class="language-javascript highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="k">if</span> <span class="p">(</span><span class="nx">context</span><span class="p">.</span><span class="nx">payload</span><span class="p">.</span><span class="nx">issue</span><span class="p">.</span><span class="nx">html_url</span><span class="p">.</span><span class="nx">includes</span><span class="p">(</span><span class="dl">"</span><span class="s2">/pull/</span><span class="dl">"</span><span class="p">))</span> <span class="p">{</span>
  <span class="nx">console</span><span class="p">.</span><span class="nx">log</span><span class="p">(</span><span class="dl">"</span><span class="s2">Comment appears in a PR, retrieving PR info...</span><span class="dl">"</span><span class="p">);</span>
  <span class="c1">// Only the pull request author and authorized users may execute this command</span>
  <span class="kd">const</span> <span class="p">{</span> <span class="na">data</span><span class="p">:</span> <span class="nx">pull</span> <span class="p">}</span> <span class="o">=</span> <span class="k">await</span> <span class="nx">github</span><span class="p">.</span><span class="nx">pulls</span><span class="p">.</span><span class="kd">get</span><span class="p">({</span>
    <span class="p">...</span><span class="nx">options</span><span class="p">,</span>
    <span class="na">pull_number</span><span class="p">:</span> <span class="nx">context</span><span class="p">.</span><span class="nx">payload</span><span class="p">.</span><span class="nx">issue</span><span class="p">.</span><span class="nx">number</span><span class="p">,</span>
  <span class="p">});</span>

  <span class="kd">const</span> <span class="nx">allowed</span> <span class="o">=</span> <span class="p">[...</span><span class="nx">authorizedUsers</span><span class="p">,</span> <span class="nx">pull</span><span class="p">.</span><span class="nx">user</span><span class="p">.</span><span class="nx">login</span><span class="p">];</span>
  <span class="kd">const</span> <span class="nx">commenting</span> <span class="o">=</span> <span class="nx">context</span><span class="p">.</span><span class="nx">payload</span><span class="p">.</span><span class="nx">comment</span><span class="p">.</span><span class="nx">user</span><span class="p">.</span><span class="nx">login</span><span class="p">;</span>
  <span class="nx">console</span><span class="p">.</span><span class="nx">log</span><span class="p">(</span><span class="s2">`Authorized users: </span><span class="p">${</span><span class="nx">allowed</span><span class="p">.</span><span class="nx">join</span><span class="p">(</span><span class="dl">"</span><span class="s2">, </span><span class="dl">"</span><span class="p">)}</span><span class="s2">`</span><span class="p">);</span>
  <span class="nx">console</span><span class="p">.</span><span class="nx">log</span><span class="p">(</span><span class="s2">`Commenting user: </span><span class="p">${</span><span class="nx">commenting</span><span class="p">}</span><span class="s2">`</span><span class="p">);</span>
  <span class="kd">const</span> <span class="nx">isAuthorized</span> <span class="o">=</span> <span class="nx">allowed</span><span class="p">.</span><span class="nx">includes</span><span class="p">(</span><span class="nx">commenting</span><span class="p">);</span>
  <span class="nx">console</span><span class="p">.</span><span class="nx">log</span><span class="p">(</span><span class="s2">`Is authorized: </span><span class="p">${</span><span class="nx">isAuthorized</span><span class="p">}</span><span class="s2">`</span><span class="p">);</span>

  <span class="k">if</span> <span class="p">(</span><span class="o">!</span><span class="nx">isAuthorized</span><span class="p">)</span> <span class="k">return</span> <span class="kc">false</span><span class="p">;</span>
<span class="p">}</span> <span class="k">else</span> <span class="p">{</span>
  <span class="c1">// In issues, only the authorized users may execute any commands</span>
</code></pre></div></div>

<h4 id="impact">Impact</h4>

<p>The triggered workflow has access to the write repository token and secrets. The vulnerability allows for unauthorized modification of the base repository and secrets exfiltration.</p>

<h3 id="issue-2-a-branch-name-and-title-from-pull-request-are-used-to-format-inline-script">Issue 2: A branch name and title from pull request are used to format inline script</h3>

<div class="language-yaml highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="na">on</span><span class="pi">:</span>
  <span class="na">issue_comment</span><span class="pi">:</span>
    <span class="na">types</span><span class="pi">:</span> <span class="pi">[</span><span class="nv">created</span><span class="pi">]</span> <span class="c1"># edited, deleted</span>
<span class="nn">...</span>
      <span class="pi">-</span> <span class="na">name</span><span class="pi">:</span> <span class="s">Rebase the branch</span>
        <span class="na">if</span><span class="pi">:</span> <span class="s">steps.check-permissions.outputs.result == 'true'</span>
        <span class="na">id</span><span class="pi">:</span> <span class="s">fix</span>
        <span class="na">run</span><span class="pi">:</span> <span class="pi">|</span>
          <span class="s"># Try to rebase</span>
          <span class="s">if git rebase "${{ fromJSON(steps.get-pr.outputs.result).base.ref }}"" ; then</span>
<span class="s">...</span>
      <span class="s">- name</span><span class="pi">:</span> <span class="s">Rebase the branch</span>
        <span class="s">if</span><span class="pi">:</span> <span class="s">steps.check-permissions.outputs.result == 'true'</span>
        <span class="s">id</span><span class="pi">:</span> <span class="s">fix</span>
        <span class="s">run</span><span class="pi">:</span> <span class="pi">|</span>
          <span class="s"># Try to reword the commit</span>
          <span class="s">git config user.email "bot@zwave.js"</span>
          <span class="s">git config user.name "Z-Wave JS Bot"</span>
          <span class="s">if git commit --amend -m "${{ fromJSON(steps.get-pr.outputs.result).title }}" ; then</span>
</code></pre></div></div>

<p>The expression evaluation is vulnerable to <a href="https://securitylab.github.com/research/github-actions-untrusted-input/">inline script injection</a>.</p>

<h4 id="impact-1">Impact</h4>

<p>The triggered workflow has access to the write repository token and secrets. The vulnerability allows for unauthorized modification of the base repository and secrets exfiltration.</p>

<h2 id="credit">Credit</h2>

<p>This issue was discovered and reported by GHSL team member <a href="https://github.com/JarLob">@JarLob (Jaroslav Lobačevski)</a>.</p>

<h2 id="contact">Contact</h2>

<p>You can contact the GHSL team at <code class="language-plaintext highlighter-rouge">securitylab@github.com</code>, please include a reference to <code class="language-plaintext highlighter-rouge">GHSL-2021-047</code> in any communication regarding this issue.</p>


   