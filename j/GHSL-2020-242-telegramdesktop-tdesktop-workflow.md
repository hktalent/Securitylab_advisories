<header class="post-header d-block mb-6">
      <div class="date text-mono f5 my-3">February 3, 2021</div>
      <h1 class="my-2 h00-mktg lh-condensed">GHSL-2020-242: Command injection in telegramdesktop/tdesktop workflow</h1>

      
      
      
      
      

      

      <a target="_blank" class="sc-frDJqD SgxRc d-inline-flex flex-row flex-items-center text-gray" href="https://github.com/jarlob">
        <img class="mr-3" src="https://avatars.githubusercontent.com/u/26652396?s=35" height="35" width="35">
        <span>Jaroslav Lobacevski</span>
      </a>
    </header>

    <main id="content" class="markdown-body" aria-label="Content">
      <h2 id="coordinated-disclosure-timeline">Coordinated Disclosure Timeline</h2>

<ul>
  <li>2020-11-26: Report sent to maintainer</li>
  <li>2020-11-26: Maintainer acknowledges</li>
  <li>2020-11-26: Issue resolved</li>
</ul>

<h2 id="summary">Summary</h2>

<p>The <a href="https://github.com/telegramdesktop/tdesktop/blob/dev/.github/workflows/user_agent_updater.yml">‘user_agent_updater.yml’ GitHub workflow</a> is vulnerable to arbitrary command injection.</p>

<h2 id="product">Product</h2>

<p><a href="https://github.com/telegramdesktop/tdesktop">telegramdesktop/tdesktop GitHub repository</a></p>

<h2 id="tested-version">Tested Version</h2>

<p>The latest changeset <a href="https://github.com/telegramdesktop/tdesktop/blob/1a2afda09ca38606fff897a89c03cfd296f72300/.github/workflows/user_agent_updater.yml">1a2afda</a> to the date.</p>

<h2 id="details">Details</h2>

<h3 id="issue-the-forked-branch-name-is-used-to-format-a-shell-command">Issue: The forked branch name is used to format a shell command</h3>

<p>When a PR is closed it automatically starts the GitHub workflow. The forked branch name is used to format a bash script.</p>

<div class="language-yaml highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="na">on</span><span class="pi">:</span>
<span class="nn">...</span>
  <span class="na">pull_request_target</span><span class="pi">:</span>
    <span class="na">types</span><span class="pi">:</span> <span class="pi">[</span><span class="nv">closed</span><span class="pi">]</span>
<span class="nn">...</span>
      <span class="pi">-</span> <span class="na">name</span><span class="pi">:</span> <span class="s">Delete branch.</span>
        <span class="na">if</span><span class="pi">:</span> <span class="pi">|</span>
          <span class="s">env.isPull == '1'</span>
            <span class="s">&amp;&amp; github.event.action == 'closed'</span>
            <span class="s">&amp;&amp; startsWith(github.head_ref, env.headBranchPrefix)</span>
        <span class="na">run</span><span class="pi">:</span> <span class="pi">|</span>
          <span class="s">git push origin --delete ${{ github.head_ref }}</span>
<span class="s">...</span>
</code></pre></div></div>

<p>An attacker can fork the repository, create a specially crafted branch name, make any commit, open a pull request and immediately close it to trigger the workflow. This vulnerability allows for arbitrary command injection into the bash script. For a Proof of Concept create a PR from branch named <code class="language-plaintext highlighter-rouge">chrome_`echo${IFS}"abc"`</code>.</p>

<h4 id="impact">Impact</h4>

<p>The injection allows for exfiltration of secrets and the temporary GitHub repository authorization token to the attacker controlled server. Although the token is not valid after the workflow finishes, since the attacker controls the execution of the workflow he or she can delay it to give the malicious server time to modify the repository.</p>

<h2 id="credit">Credit</h2>

<p>This issue was discovered and reported by GHSL team member <a href="https://github.com/JarLob">@JarLob (Jaroslav Lobačevski)</a>.</p>

<h2 id="contact">Contact</h2>

<p>You can contact the GHSL team at <code class="language-plaintext highlighter-rouge">securitylab@github.com</code>, please include a reference to <code class="language-plaintext highlighter-rouge">GHSL-2020-242</code> in any communication regarding this issue.</p>
