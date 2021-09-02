<header class="post-header d-block mb-6">
      <div class="date text-mono f5 my-3">February 3, 2021</div>
      <h1 class="my-2 h00-mktg lh-condensed">GHSL-2020-240: Command injection in scikit-learn/scikit-learn workflow</h1>

      
      
      
      
      

      

      <a target="_blank" class="sc-frDJqD SgxRc d-inline-flex flex-row flex-items-center text-gray" href="https://github.com/jarlob">
        <img class="mr-3" src="https://avatars.githubusercontent.com/u/26652396?s=35" height="35" width="35">
        <span>Jaroslav Lobacevski</span>
      </a>
    </header>

    <main id="content" class="markdown-body" aria-label="Content">
      <h2 id="coordinated-disclosure-timeline">Coordinated Disclosure Timeline</h2>

<ul>
  <li>2020-11-26-2020-12-01: Report sent to various maintainers.</li>
  <li>2020-12-01: Report acknowledged.</li>
  <li>2020-12-01: Issue resolved.</li>
</ul>

<h2 id="summary">Summary</h2>

<p>The <a href="https://github.com/scikit-learn/scikit-learn/blob/master/.github/workflows/sync_pull_request.yml">‘sync_pull_request.yml’ GitHub workflow</a> is vulnerable to arbitrary command injection.</p>

<h2 id="product">Product</h2>

<p><a href="https://github.com/scikit-learn/scikit-learn">scikit-learn/scikit-learn GitHub repository</a></p>

<h2 id="tested-version">Tested Version</h2>

<p>The latest changeset <a href="https://github.com/scikit-learn/scikit-learn/blob/12f1521f1efefc3c24af59e842ad4294361f8e98/.github/workflows/sync_pull_request.yml">12f1521</a> to the date.</p>

<h2 id="details">Details</h2>

<h3 id="issue-the-forked-branch-name-is-used-to-format-a-shell-command">Issue: The forked branch name is used to format a shell command</h3>

<p>When a label <code class="language-plaintext highlighter-rouge">ci sync</code> is assigned to a PR it automatically starts the GitHub workflow. The forked branch name is used to format a bash script.</p>

<div class="language-yaml highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="na">name</span><span class="pi">:</span> <span class="s">Sync Pull Request</span>
<span class="na">on</span><span class="pi">:</span>
  <span class="na">pull_request_target</span><span class="pi">:</span>
    <span class="na">types</span><span class="pi">:</span> <span class="pi">[</span><span class="nv">labeled</span><span class="pi">]</span>

<span class="na">jobs</span><span class="pi">:</span>
  <span class="na">sync_pull_request</span><span class="pi">:</span>
    <span class="na">runs-on</span><span class="pi">:</span> <span class="s">ubuntu-latest</span>
    <span class="na">if</span><span class="pi">:</span> <span class="s">contains(github.event.pull_request.labels.*.name, 'ci sync')</span>
    <span class="na">steps</span><span class="pi">:</span>
<span class="nn">...</span>
      <span class="pi">-</span> <span class="na">name</span><span class="pi">:</span> <span class="s">Sync with master</span>
        <span class="na">run</span><span class="pi">:</span> <span class="pi">|</span>
          <span class="s">set -xe</span>
          <span class="s">git remote add pr_remote ${{ github.event.pull_request.head.repo.html_url }}</span>
          <span class="s">git fetch pr_remote ${{ github.event.pull_request.head.ref }}</span>
<span class="s">...</span>
</code></pre></div></div>

<p>If an authorized person is tricked into assigning the label on a specially crafted PR this vulnerability allows for arbitrary command injection into the bash script. For a Proof of Concept create a PR from branch named <code class="language-plaintext highlighter-rouge">main;echo${IFS}"abc";exit${IFS}0</code>.</p>

<h4 id="impact">Impact</h4>

<p>The injection allows for exfiltration of the temporary GitHub repository authorization token to the attacker controlled server. Although the token is not valid after the workflow finishes, since the attacker controls the execution of the workflow he or she can delay it to give the malicious server time to modify the repository.</p>

<h2 id="credit">Credit</h2>

<p>This issue was discovered and reported by GHSL team member <a href="https://github.com/JarLob">@JarLob (Jaroslav Lobačevski)</a>.</p>

<h2 id="contact">Contact</h2>

<p>You can contact the GHSL team at <code class="language-plaintext highlighter-rouge">securitylab@github.com</code>, please include a reference to <code class="language-plaintext highlighter-rouge">GHSL-2020-240</code> in any communication regarding this issue.</p>
