<header class="post-header d-block mb-6">
      <div class="date text-mono f5 my-3">February 3, 2021</div>
      <h1 class="my-2 h00-mktg lh-condensed">GHSL-2020-182: Code injection in JonathanGin52/JonathanGin52 workflow</h1>

      
      
      
      
      

      

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
  <li>10/15/2020: Issue fixed</li>
</ul>

<h2 id="summary">Summary</h2>

<p>The <a href="https://github.com/JonathanGin52/JonathanGin52/blob/master/.github/workflows/connect4.yml">‘Connect4’ GitHub workflow</a> is vulnerable to arbitrary code execution.</p>

<h2 id="product">Product</h2>

<p><a href="https://github.com/JonathanGin52/JonathanGin52">JonathanGin52 GitHub repository</a></p>

<h2 id="tested-version">Tested Version</h2>

<p><a href="https://github.com/JonathanGin52/JonathanGin52/blob/master/.github/workflows/connect4.yml">connect4.yml</a> from the Master branch.</p>

<h2 id="details">Details</h2>

<h3 id="issue-the-title-of-a-public-github-issue-is-used-to-format-ruby-code-before-it-runs">Issue: The title of a public GitHub Issue is used to format Ruby code before it runs</h3>

<p>When a user creates an Issue with a special title it automatically starts the <a href="https://github.com/JonathanGin52/JonathanGin52/blob/master/.github/workflows/connect4.yml">connect4.yml</a> GitHub workflow. The title of the public issue is used without sanitization to format Ruby code:</p>

<div class="language-bash highlighter-rouge"><div class="highlight"><pre class="highlight"><code>    - name: Play
      run: |
        ruby <span class="o">&lt;&lt;-</span> <span class="no">EORUBY</span><span class="sh">
          require './connect4/runner'
          
          Connect4::Runner.new(
            github_token: '</span><span class="k">${</span><span class="p">{ secrets.GITHUB_TOKEN </span><span class="k">}</span><span class="sh">}',
            issue_number: ENV.fetch('EVENT_ISSUE_NUMBER'),
            issue_title: '</span><span class="k">${</span><span class="p">{ github.event.issue.title </span><span class="k">}</span><span class="sh">}',
            repository: ENV.fetch('REPOSITORY'),
            user: ENV.fetch('EVENT_USER_LOGIN'),
          ).run
</span><span class="no">        EORUBY
</span></code></pre></div></div>

<h4 id="impact">Impact</h4>

<p>This vulnerability allows for arbitrary Ruby code execution. The injected code may exfiltrate the temporary GitHub repository authorization token from <code class="language-plaintext highlighter-rouge">.git/config</code> to the attacker controlled server. Although the token is not valid after the workflow finishes, since the attacker controls the execution of the workflow he or she can delay it to give the malicious server time to modify the repository.<br />
For a proof of concept create an issue with a title <code class="language-plaintext highlighter-rouge">Iconnect4|' + raise('asdf') + '</code>. Observe the thrown <code class="language-plaintext highlighter-rouge">asdf</code> exception in the action log.</p>

<h2 id="credit">Credit</h2>

<p>This issue was discovered and reported by GHSL team member <a href="https://github.com/JarLob">@JarLob (Jaroslav Lobačevski)</a>.</p>

<h2 id="contact">Contact</h2>

<p>You can contact the GHSL team at <code class="language-plaintext highlighter-rouge">securitylab@github.com</code>, please include a reference to <code class="language-plaintext highlighter-rouge">GHSL-2020-182</code> in any communication regarding this issue.</p>
