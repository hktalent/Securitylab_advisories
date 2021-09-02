<header class="post-header d-block mb-6">
      <div class="date text-mono f5 my-3">February 3, 2021</div>
      <h1 class="my-2 h00-mktg lh-condensed">GHSL-2020-239: Command injection in NVIDIA/spark-rapids workflow</h1>

      
      
      
      
      

      

      <a target="_blank" class="sc-frDJqD SgxRc d-inline-flex flex-row flex-items-center text-gray" href="https://github.com/jarlob">
        <img class="mr-3" src="https://avatars.githubusercontent.com/u/26652396?s=35" height="35" width="35">
        <span>Jaroslav Lobacevski</span>
      </a>
    </header>

    <main id="content" class="markdown-body" aria-label="Content">
      <h2 id="coordinated-disclosure-timeline">Coordinated Disclosure Timeline</h2>

<ul>
  <li>2020-11-26: Report sent to maintainers.</li>
  <li>2020-11-26:: Issue resolved.</li>
</ul>

<h2 id="summary">Summary</h2>

<p>The <a href="https://github.com/NVIDIA/spark-rapids/blob/branch-0.3/.github/workflows/blossom-ci.yml">‘blossom-ci.yml’ GitHub workflow</a> is vulnerable to arbitrary command injection.</p>

<h2 id="product">Product</h2>

<p><a href="https://github.com/NVIDIA/spark-rapids">NVIDIA/spark-rapids GitHub repository</a></p>

<h2 id="tested-version">Tested Version</h2>

<p>The latest changeset <a href="https://github.com/NVIDIA/spark-rapids/blob/6c020cca952f87ed35e7aae6be894f34987758a5/.github/workflows/blossom-ci.yml">6c020cc</a> to the date.</p>

<h2 id="details">Details</h2>

<h3 id="issue-the-forked-branch-name-is-used-to-format-a-shell-command">Issue: The forked branch name is used to format a shell command</h3>

<p>When an authorized user comments on a specially crafted pull request with <code class="language-plaintext highlighter-rouge">build</code> it automatically starts the GitHub workflow. The forked branch name is used to format a bash script.</p>

<div class="language-yaml highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="na">on</span><span class="pi">:</span>
  <span class="na">issue_comment</span><span class="pi">:</span>
    <span class="na">types</span><span class="pi">:</span> <span class="pi">[</span><span class="nv">created</span><span class="pi">]</span>

<span class="na">jobs</span><span class="pi">:</span>
  <span class="na">authorization</span><span class="pi">:</span>
    <span class="na">name</span><span class="pi">:</span> <span class="s">Authorization</span>
    <span class="c1"># trigger on pre-defined text</span>
    <span class="na">if</span><span class="pi">:</span> <span class="s">github.event.comment.body == 'build'</span>
    <span class="na">runs-on</span><span class="pi">:</span> <span class="pi">[</span><span class="nv">self-hosted</span><span class="pi">,</span> <span class="nv">linux</span><span class="pi">,</span> <span class="nv">blossom</span><span class="pi">]</span>
    <span class="na">steps</span><span class="pi">:</span>
      <span class="pi">-</span> <span class="na">name</span><span class="pi">:</span> <span class="s">Check if comment is issued by authorized person</span>
        <span class="na">run</span><span class="pi">:</span> <span class="s">blossom-ci</span>
<span class="nn">...</span>
  <span class="na">vulnerability-scan-job</span><span class="pi">:</span>
    <span class="na">name</span><span class="pi">:</span> <span class="s">Vulnerability scan job</span>
    <span class="na">needs</span><span class="pi">:</span> <span class="pi">[</span><span class="nv">authorization</span><span class="pi">]</span>
    <span class="na">runs-on</span><span class="pi">:</span> <span class="s">ubuntu-latest</span>
    <span class="na">steps</span><span class="pi">:</span>
      <span class="pi">-</span> <span class="na">name</span><span class="pi">:</span> <span class="s">Get pull request data</span>
        <span class="na">id</span><span class="pi">:</span> <span class="s">pull_request_data</span>
        <span class="na">uses</span><span class="pi">:</span> <span class="s">octokit/request-action@v2.x</span>
        <span class="na">with</span><span class="pi">:</span>
          <span class="na">route</span><span class="pi">:</span> <span class="s1">'</span><span class="s">GET</span><span class="nv"> </span><span class="s">/repos/:repository/pulls/:issue_id'</span>
          <span class="na">repository</span><span class="pi">:</span> <span class="s">${{ github.repository }}</span>
          <span class="na">issue_id</span><span class="pi">:</span> <span class="s">${{ github.event.issue.number }}</span>
        <span class="na">env</span><span class="pi">:</span>
          <span class="na">GITHUB_TOKEN</span><span class="pi">:</span> <span class="s2">"</span><span class="s">${{</span><span class="nv"> </span><span class="s">secrets.GITHUB_TOKEN</span><span class="nv"> </span><span class="s">}}"</span>

      <span class="pi">-</span> <span class="na">name</span><span class="pi">:</span> <span class="s">Set blackduck project version</span>
        <span class="na">id</span><span class="pi">:</span> <span class="s">blackduck-project-version</span>
        <span class="na">run</span><span class="pi">:</span> <span class="s">echo "${{ fromJson(steps.pull_request_data.outputs.data).head.ref }}-${{ github.run_id }}"</span>
</code></pre></div></div>

<p>It is assumed the <code class="language-plaintext highlighter-rouge">blossom-ci</code> doesn’t allow triggering the workflow for external users. If an authorized person is tricked into commenting <code class="language-plaintext highlighter-rouge">build</code> on a PR this vulnerability allows for arbitrary command injection into the bash script. For a Proof of Concept create a PR from branch named <code class="language-plaintext highlighter-rouge">a";echo${IFS}"hello"#</code>.</p>

<h4 id="impact">Impact</h4>

<p>The injection allows for exfiltration of secrets and the temporary GitHub repository authorization token to the attacker controlled server. Although the token is not valid after the workflow finishes, since the attacker controls the execution of the workflow he or she can delay it to give the malicious server time to modify the repository.</p>

<h2 id="credit">Credit</h2>

<p>This issue was discovered and reported by GHSL team member <a href="https://github.com/JarLob">@JarLob (Jaroslav Lobačevski)</a>.</p>

<h2 id="contact">Contact</h2>

<p>You can contact the GHSL team at <code class="language-plaintext highlighter-rouge">securitylab@github.com</code>, please include a reference to <code class="language-plaintext highlighter-rouge">GHSL-2020-239</code> in any communication regarding this issue.</p