<header class="post-header d-block mb-6">
      <div class="date text-mono f5 my-3">April 1, 2021</div>
      <h1 class="my-2 h00-mktg lh-condensed">GHSL-2021-031: Script injection in a GitHub workflow of hasura/graphql-engine</h1>

      
      
      
      
      

      

      <a target="_blank" class="sc-frDJqD SgxRc d-inline-flex flex-row flex-items-center text-gray" href="https://github.com/jarlob">
        <img class="mr-3" src="https://avatars.githubusercontent.com/u/26652396?s=35" height="35" width="35">
        <span>Jaroslav Lobacevski</span>
      </a>
    </header>

    <main id="content" class="markdown-body" aria-label="Content">
      
<h2 id="coordinated-disclosure-timeline">Coordinated Disclosure Timeline</h2>

<ul>
  <li>2021-01-28: Issue reported to maintainers</li>
  <li>2021-02-02: Maintainer acknowledged</li>
  <li>2021-02-04: Issue fixed</li>
</ul>

<h2 id="summary">Summary</h2>

<p>The <a href="https://github.com/hasura/graphql-engine/blob/master/.github/workflows/shadow-pr.yml">shadow-pr.yml</a> GitHub workflow is vulnerable to script injection.</p>

<h2 id="product">Product</h2>

<p><a href="https://github.com/hasura/graphql-engine">hasura/graphql-engine</a> repository</p>

<h2 id="tested-version">Tested Version</h2>

<p>The latest changeset of <a href="https://github.com/hasura/graphql-engine/blob/64a0a14fe2358aa790df7e371af98a411abc2319/.github/workflows/shadow-pr.yml">shadow-pr.yml</a> to date.</p>

<h2 id="details">Details</h2>

<h3 id="issue-a-pull-request-title-is-used-to-format-inline-script">Issue: A pull request title is used to format inline script</h3>

<div class="language-yaml highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="na">name</span><span class="pi">:</span> <span class="s">shadow pr</span>
<span class="na">on</span><span class="pi">:</span>
  <span class="na">pull_request_target</span><span class="pi">:</span>
    <span class="na">types</span><span class="pi">:</span> <span class="pi">[</span><span class="nv">opened</span><span class="pi">,</span> <span class="nv">synchronize</span><span class="pi">,</span> <span class="nv">reopened</span><span class="pi">]</span>

<span class="na">jobs</span><span class="pi">:</span>
  <span class="na">open-pr</span><span class="pi">:</span>
    <span class="na">if</span><span class="pi">:</span> <span class="s">${{ startsWith(github.event.pull_request.body, '&lt;!-- from mono --&gt;') != </span><span class="no">true</span><span class="s"> }}</span>
<span class="nn">...</span>
    <span class="pi">-</span> <span class="na">name</span><span class="pi">:</span> <span class="s2">"</span><span class="s">Open</span><span class="nv"> </span><span class="s">pull</span><span class="nv"> </span><span class="s">request"</span>
      <span class="na">uses</span><span class="pi">:</span> <span class="s">actions/github-script@v3</span>
      <span class="na">with</span><span class="pi">:</span>
        <span class="na">github-token</span><span class="pi">:</span> <span class="s">${{secrets.HASURA_BOT_GH_TOKEN}}</span>
        <span class="na">script</span><span class="pi">:</span> <span class="pi">|</span>
<span class="s">...</span>
          <span class="s">try {</span>
            <span class="s">const pr = await github.pulls.create({</span>
              <span class="s">owner</span><span class="pi">:</span> <span class="s1">'</span><span class="s">hasura'</span><span class="err">,</span>
              <span class="na">repo</span><span class="pi">:</span> <span class="s1">'</span><span class="s">graphql-engine-mono'</span><span class="err">,</span>
              <span class="na">head</span><span class="pi">:</span> <span class="s1">'</span><span class="s">oss_pr_refs/pull/${{</span><span class="nv"> </span><span class="s">github.event.number</span><span class="nv"> </span><span class="s">}}/head'</span><span class="err">,</span>
              <span class="na">base</span><span class="pi">:</span> <span class="s1">'</span><span class="s">main'</span><span class="err">,</span>
              <span class="na">title</span><span class="pi">:</span> <span class="s1">'</span><span class="s">${{</span><span class="nv"> </span><span class="s">steps.pr.outputs.ossPrTitle</span><span class="nv"> </span><span class="s">}}'</span><span class="err">,</span>
              <span class="s">body,</span>
            <span class="err">}</span><span class="s">);</span>
</code></pre></div></div>

<h4 id="impact">Impact</h4>

<p>The workflow is vulnerable to arbitrary script injection which enables un-authorized modification of the base repository and secrets exfiltration. For a PoC create a pull request with the title <code class="language-plaintext highlighter-rouge">a',body});console.log('test')/*</code>. The permissions of HASURA_BOT_GH_TOKEN do not matter as it is possible to get a read-write GITHUB_TOKEN in the <code class="language-plaintext highlighter-rouge">pull_request_target</code> case.</p>

<h2 id="credit">Credit</h2>

<p>This issue was discovered and reported by GHSL team member <a href="https://github.com/JarLob">@JarLob (Jaroslav Lobačevski)</a>.</p>

<h2 id="contact">Contact</h2>

<p>You can contact the GHSL team at <code class="language-plaintext highlighter-rouge">securitylab@github.com</code>, please include a reference to <code class="language-plaintext highlighter-rouge">GHSL-2021-031</code> in any communication regarding this issue.</p>


   