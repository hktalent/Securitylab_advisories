<header class="post-header d-block mb-6">
      <div class="date text-mono f5 my-3">February 3, 2021</div>
      <h1 class="my-2 h00-mktg lh-condensed">GHSL-2020-195: Arbitrary file write in dd-center/vdb workflow</h1>

      
      
      
      
      

      

      <a target="_blank" class="sc-frDJqD SgxRc d-inline-flex flex-row flex-items-center text-gray" href="https://github.com/jarlob">
        <img class="mr-3" src="https://avatars.githubusercontent.com/u/26652396?s=35" height="35" width="35">
        <span>Jaroslav Lobacevski</span>
      </a>
    </header>

    <main id="content" class="markdown-body" aria-label="Content">
      <h2 id="coordinated-disclosure-timeline">Coordinated Disclosure Timeline</h2>

<ul>
  <li>10/16/2020: Report sent to vendor</li>
  <li>10/19/2020: Issue fixed</li>
</ul>

<h2 id="summary">Summary</h2>

<p>The <a href="https://github.com/dd-center/vdb/blob/main/.github/workflows/submit.yml">‘Submit.yml’ GitHub workflow</a> is vulnerable to arbitrary file write, that may lead to the repository being compromised.</p>

<h2 id="product">Product</h2>

<p><a href="https://github.com/dd-center/vdb">dd-center/vdb GitHub repository</a></p>

<h2 id="tested-version">Tested Version</h2>

<p><a href="https://github.com/dd-center/vdb/blob/main/.github/workflows/submit.yml">submit.yml</a> from the master branch.</p>

<h2 id="details">Details</h2>

<h3 id="issue-the-body-of-a-public-github-issue-is-parsed-and-used-to-define-the-path-and-the-content-of-file-write-operation">Issue: The body of a public GitHub issue is parsed and used to define the path and the content of file write operation</h3>

<p>When a user creates a public issue it automatically starts the <a href="https://github.com/dd-center/vdb/blob/main/.github/workflows/submit.yml">submit.yml</a> GitHub workflow. The body of the issue is used without validation in the <a href="https://github.com/dd-center/vdb/blob/master/submitPr.js">submitPr.js</a> action.</p>

<div class="language-bash highlighter-rouge"><div class="highlight"><pre class="highlight"><code>    - name: Commit Branch
      run: node submitPr.js
      <span class="nb">env</span>:
        ISSUE_NUMBER: <span class="k">${</span><span class="p">{ github.event.issue.number </span><span class="k">}</span><span class="o">}</span>
        ISSUE_BODY: <span class="k">${</span><span class="p">{ github.event.issue.body </span><span class="k">}</span><span class="o">}</span>
        GITHUB_TOKEN: <span class="k">${</span><span class="p">{ secrets.gtoken </span><span class="k">}</span><span class="o">}</span>
</code></pre></div></div>

<div class="language-js highlighter-rouge"><div class="highlight"><pre class="highlight"><code>  <span class="kd">const</span> <span class="nx">block</span> <span class="o">=</span> <span class="nx">ISSUE_BODY</span><span class="p">.</span><span class="nx">split</span><span class="p">(</span><span class="dl">'</span><span class="s1">-----END SUBMIT BLOCK-----</span><span class="dl">'</span><span class="p">)[</span><span class="mi">0</span><span class="p">].</span><span class="nx">split</span><span class="p">(</span><span class="dl">'</span><span class="s1">-----BEGIN SUBMIT BLOCK-----</span><span class="dl">'</span><span class="p">)[</span><span class="mi">1</span><span class="p">]</span>
  <span class="k">if</span> <span class="p">(</span><span class="nx">block</span><span class="p">)</span> <span class="p">{</span>
    <span class="k">await</span> <span class="nx">decodeBase64</span><span class="p">(</span><span class="nx">block</span><span class="p">)</span>
      <span class="p">.</span><span class="nx">split</span><span class="p">(</span><span class="dl">'</span><span class="se">\n</span><span class="dl">'</span><span class="p">)</span>
      <span class="p">.</span><span class="nx">map</span><span class="p">(</span><span class="nx">command</span> <span class="o">=&gt;</span> <span class="nx">command</span><span class="p">.</span><span class="nx">split</span><span class="p">(</span><span class="dl">'</span><span class="s1">:</span><span class="dl">'</span><span class="p">))</span>
      <span class="p">.</span><span class="nx">map</span><span class="p">(([</span><span class="nx">command</span><span class="p">,</span> <span class="nx">arg</span><span class="p">,</span> <span class="nx">extra</span> <span class="o">=</span> <span class="dl">''</span><span class="p">])</span> <span class="o">=&gt;</span> <span class="p">[</span><span class="nx">command</span><span class="p">,</span> <span class="nx">decodeBase64</span><span class="p">(</span><span class="nx">arg</span><span class="p">),</span> <span class="nx">decodeBase64</span><span class="p">(</span><span class="nx">extra</span><span class="p">)])</span>
      <span class="p">.</span><span class="nx">map</span><span class="p">(([</span><span class="nx">command</span><span class="p">,</span> <span class="nx">arg</span><span class="p">,</span> <span class="nx">content</span><span class="p">])</span> <span class="o">=&gt;</span> <span class="k">async</span> <span class="p">()</span> <span class="o">=&gt;</span> <span class="p">{</span>
        <span class="kd">const</span> <span class="nx">path</span> <span class="o">=</span> <span class="nx">join</span><span class="p">(</span><span class="dl">'</span><span class="s1">vtbs</span><span class="dl">'</span><span class="p">,</span> <span class="nx">arg</span><span class="p">)</span>
        <span class="k">if</span> <span class="p">(</span><span class="nx">command</span> <span class="o">===</span> <span class="dl">'</span><span class="s1">delete</span><span class="dl">'</span><span class="p">)</span> <span class="p">{</span>
          <span class="k">await</span> <span class="nx">unlink</span><span class="p">(</span><span class="nx">path</span><span class="p">)</span>
          <span class="nx">console</span><span class="p">.</span><span class="nx">log</span><span class="p">(</span><span class="dl">'</span><span class="s1">delete</span><span class="dl">'</span><span class="p">,</span> <span class="nx">path</span><span class="p">)</span>
        <span class="p">}</span>
        <span class="k">if</span> <span class="p">(</span><span class="nx">command</span> <span class="o">===</span> <span class="dl">'</span><span class="s1">put</span><span class="dl">'</span><span class="p">)</span> <span class="p">{</span>
          <span class="k">await</span> <span class="nx">writeFile</span><span class="p">(</span><span class="nx">path</span><span class="p">,</span> <span class="nx">content</span><span class="p">)</span>
          <span class="nx">console</span><span class="p">.</span><span class="nx">log</span><span class="p">(</span><span class="dl">'</span><span class="s1">put</span><span class="dl">'</span><span class="p">,</span> <span class="nx">path</span><span class="p">)</span>
        <span class="p">}</span>
<span class="p">...</span>
  <span class="p">}</span>
</code></pre></div></div>

<h4 id="impact">Impact</h4>

<p>This vulnerability allows for arbitrary file overwrite, that may lead to the repository being compromised. For example an attacker may create an issue with a command to write into <code class="language-plaintext highlighter-rouge">.git/config</code> the attacker controlled proxy server address which will exfiltrate the temporary GitHub repository authorization token to the proxy server on the next git command in the same <code class="language-plaintext highlighter-rouge">submitPr.js</code> script. Although the token is not valid after the workflow finishes, the proxy may timeout the connection to give the malicious server time to modify the repository.</p>

<h2 id="credit">Credit</h2>

<p>This issue was discovered and reported by GHSL team member <a href="https://github.com/JarLob">@JarLob (Jaroslav Lobačevski)</a>.</p>

<h2 id="contact">Contact</h2>

<p>You can contact the GHSL team at <code class="language-plaintext highlighter-rouge">securitylab@github.com</code>, please include a reference to <code class="language-plaintext highlighter-rouge">GHSL-2020-195</code> in any communication regarding this issue.</p>
