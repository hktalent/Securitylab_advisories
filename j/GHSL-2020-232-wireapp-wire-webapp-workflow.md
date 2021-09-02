<header class="post-header d-block mb-6">
      <div class="date text-mono f5 my-3">February 3, 2021</div>
      <h1 class="my-2 h00-mktg lh-condensed">GHSL-2020-232: Command injection in wireapp/wire-webapp workflow</h1>

      
      
      
      
      

      

      <a target="_blank" class="sc-frDJqD SgxRc d-inline-flex flex-row flex-items-center text-gray" href="https://github.com/jarlob">
        <img class="mr-3" src="https://avatars.githubusercontent.com/u/26652396?s=35" height="35" width="35">
        <span>Jaroslav Lobacevski</span>
      </a>
    </header>

    <main id="content" class="markdown-body" aria-label="Content">
      <h2 id="coordinated-disclosure-timeline">Coordinated Disclosure Timeline</h2>

<ul>
  <li>2020-11-23: Report sent to maintainer</li>
  <li>2020-11-23: Maintainer acknowledges</li>
  <li>2020-11-24: Issue resolved</li>
</ul>

<h2 id="summary">Summary</h2>

<p>The <a href="https://github.com/wireapp/wire-webapp/blob/dev/.github/workflows/test_build_deploy.yml">‘test_build_deploy.yml’ GitHub workflow</a> is vulnerable to arbitrary command injection.</p>

<h2 id="product">Product</h2>

<p><a href="https://github.com/wireapp/wire-webapp">wireapp/wire-webapp GitHub repository</a></p>

<h2 id="tested-version">Tested Version</h2>

<p><a href="https://github.com/wireapp/wire-webapp/blob/5bdd49291b278d6d3d5fe89f1e656a556bd6db8e/.github/workflows/test_build_deploy.yml">test_build_deploy.yml</a></p>

<h2 id="details">Details</h2>

<h3 id="issue-the-title-of-public-github-pull-request-and-last-commit-message-are-used-to-format-a-shell-command">Issue: The title of public GitHub pull request and last commit message are used to format a shell command</h3>

<p>A Pull Request title is used to format a bash script:</p>

<div class="language-yaml highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="na">on</span><span class="pi">:</span>
<span class="nn">...</span>
  <span class="na">pull_request</span><span class="pi">:</span>
    <span class="na">branches</span><span class="pi">:</span> <span class="pi">[</span><span class="nv">master</span><span class="pi">,</span> <span class="nv">dev</span><span class="pi">,</span> <span class="nv">edge</span><span class="pi">,</span> <span class="nv">avs</span><span class="pi">]</span>
<span class="nn">...</span>
      <span class="pi">-</span> <span class="na">name</span><span class="pi">:</span> <span class="s">Set environment variables</span>
        <span class="na">run</span><span class="pi">:</span> <span class="pi">|</span>
<span class="s">...</span>
          <span class="s">echo "PR_LAST_COMMIT_MESSAGE=$(git log --format=%B -n 1 ${{github.event.after}} | head -n 1)" &gt;&gt; $GITHUB_ENV</span>
<span class="nn">...</span>

      <span class="pi">-</span> <span class="na">name</span><span class="pi">:</span> <span class="s">Set TITLE</span>
        <span class="na">run</span><span class="pi">:</span> <span class="s">echo "TITLE=${{github.event.pull_request.title || env.PR_LAST_COMMIT_MESSAGE}}" &gt;&gt; $GITHUB_ENV</span>
<span class="nn">...</span>
</code></pre></div></div>

<h4 id="impact">Impact</h4>

<p>This vulnerability allows for arbitrary command injection into the bash script. For a proof a concept a Pull Request with the following title <code class="language-plaintext highlighter-rouge">title"; sleep 10 #</code> will delay the action by ten seconds.</p>

<p>Workflows triggered by <code class="language-plaintext highlighter-rouge">pull_request</code> have limited repository token and no access to secrets. The attacker couldn’t do much except CI DoS attacks or running their own code in the context of the GitHub action runner.</p>

<h2 id="credit">Credit</h2>

<p>This issue was discovered and reported by GHSL team member <a href="https://github.com/JarLob">@JarLob (Jaroslav Lobačevski)</a>.</p>

<h2 id="contact">Contact</h2>

<p>You can contact the GHSL team at <code class="language-plaintext highlighter-rouge">securitylab@github.com</code>, please include a reference to <code class="language-plaintext highlighter-rouge">GHSL-2020-232</code> in any communication regarding this issue.</p