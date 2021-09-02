<header class="post-header d-block mb-6">
      <div class="date text-mono f5 my-3">February 3, 2021</div>
      <h1 class="my-2 h00-mktg lh-condensed">GHSL-2021-011: Command injection in itpp-labs workflows</h1>

      
      
      
      
      

      

      <a target="_blank" class="sc-frDJqD SgxRc d-inline-flex flex-row flex-items-center text-gray" href="https://github.com/jarlob">
        <img class="mr-3" src="https://avatars.githubusercontent.com/u/26652396?s=35" height="35" width="35">
        <span>Jaroslav Lobacevski</span>
      </a>
    </header>

    <main id="content" class="markdown-body" aria-label="Content">
      <h2 id="coordinated-disclosure-timeline">Coordinated Disclosure Timeline</h2>

<ul>
  <li>2021-01-18: Report sent to maintainers.</li>
  <li>2021-01-18: Issue resolved.</li>
</ul>

<h2 id="summary">Summary</h2>

<p>The <code class="language-plaintext highlighter-rouge">DINAR-PORT.yml</code> GitHub workflow in <code class="language-plaintext highlighter-rouge">itpp-labs/misc-addons</code>, <code class="language-plaintext highlighter-rouge">itpp-labs/website-addons</code>, <code class="language-plaintext highlighter-rouge">itpp-labs/access-addons</code>, <code class="language-plaintext highlighter-rouge">itpp-labs/l10n-addons</code>, <code class="language-plaintext highlighter-rouge">itpp-labs/mail-addons</code>, <code class="language-plaintext highlighter-rouge">itpp-labs/pos-addons</code> and <code class="language-plaintext highlighter-rouge">itpp-labs/sync-addons</code> repositories is vulnerable to arbitrary command injection.</p>

<h2 id="product">Product</h2>

<p><code class="language-plaintext highlighter-rouge">itpp-labs/misc-addons</code>, <code class="language-plaintext highlighter-rouge">itpp-labs/website-addons</code>, <code class="language-plaintext highlighter-rouge">itpp-labs/access-addons</code>, <code class="language-plaintext highlighter-rouge">itpp-labs/l10n-addons</code>, <code class="language-plaintext highlighter-rouge">itpp-labs/mail-addons</code>, <code class="language-plaintext highlighter-rouge">itpp-labs/pos-addons</code> and <code class="language-plaintext highlighter-rouge">itpp-labs/sync-addons</code> repositories.</p>

<h2 id="tested-version">Tested Version</h2>

<p>The latest version to the date.</p>

<h2 id="details">Details</h2>

<h3 id="issue-the-issue-title-is-used-to-format-a-shell-command">Issue: The issue title is used to format a shell command</h3>

<p>An issue title is used to format a bash script:</p>

<div class="language-yaml highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="na">on</span><span class="pi">:</span>
  <span class="na">issues</span><span class="pi">:</span>
    <span class="na">types</span><span class="pi">:</span>
      <span class="pi">-</span> <span class="s">opened</span>
      <span class="pi">-</span> <span class="s">reopened</span>
<span class="nn">...</span>
      <span class="pi">-</span> <span class="na">name</span><span class="pi">:</span> <span class="s">Analyze request</span>
        <span class="na">run</span><span class="pi">:</span> <span class="pi">|</span>
          <span class="s"># sets environment variables that available in next steps via $ {{ env.PORT_... }} notation</span>
          <span class="s">python DINAR/workflow-files/analyze_port_trigger.py "${{ github.event.issue.title }}"</span>
<span class="s">...</span>
</code></pre></div></div>

<h4 id="impact">Impact</h4>

<p>This vulnerability allows for arbitrary command injection into the bash script which allows for unauthorized modification of the base repository and secrets exfiltration. For a proof a concept create an issue with the following title <code class="language-plaintext highlighter-rouge">DINAR-PORT "; echo "test"; #</code>.</p>

<h2 id="credit">Credit</h2>

<p>This issue was discovered and reported by GHSL team member <a href="https://github.com/JarLob">@JarLob (Jaroslav Lobačevski)</a>.</p>

<h2 id="contact">Contact</h2>

<p>You can contact the GHSL team at <code class="language-plaintext highlighter-rouge">securitylab@github.com</code>, please include a reference to <code class="language-plaintext highlighter-rouge">GHSL-2021-011</code> in any communication regarding this issue.</p>

   