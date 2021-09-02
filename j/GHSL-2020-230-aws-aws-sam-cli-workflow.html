<header class="post-header d-block mb-6">
      <div class="date text-mono f5 my-3">February 3, 2021</div>
      <h1 class="my-2 h00-mktg lh-condensed">GHSL-2020-230: Command injection in aws/aws-sam-cli worflow</h1>

      
      
      
      
      

      

      <a target="_blank" class="sc-frDJqD SgxRc d-inline-flex flex-row flex-items-center text-gray" href="https://github.com/jarlob">
        <img class="mr-3" src="https://avatars.githubusercontent.com/u/26652396?s=35" height="35" width="35">
        <span>Jaroslav Lobacevski</span>
      </a>
    </header>

    <main id="content" class="markdown-body" aria-label="Content">
      <h2 id="coordinated-disclosure-timeline">Coordinated Disclosure Timeline</h2>

<ul>
  <li>2020-11-23: Report sent to maintainers.</li>
  <li>2020-11-24: Maintainers acknowledged.</li>
  <li>2020-11-24: Issue resolved.</li>
</ul>

<h2 id="summary">Summary</h2>

<p>The <a href="https://github.com/aws/aws-sam-cli/blob/develop/.github/workflows/pr_title.yml">‘pr_title.yml’ GitHub workflow</a> is vulnerable to arbitrary command injection.</p>

<h2 id="product">Product</h2>

<p><a href="https://github.com/aws/aws-sam-cli">aws/aws-sam-cli GitHub repository</a></p>

<h2 id="tested-version">Tested Version</h2>

<p><a href="https://github.com/aws/aws-sam-cli/blob/8435b574aa0c30abb68730575463693c2361b783/.github/workflows/pr_title.yml">pr_title.yml</a></p>

<h2 id="details">Details</h2>

<h3 id="issue-the-title-of-public-github-pull-request-is-used-to-format-a-shell-command">Issue: The title of public GitHub pull request is used to format a shell command</h3>

<p>A Pull Request title is used to format a bash script:</p>

<div class="language-yaml highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="na">name</span><span class="pi">:</span> <span class="s">Check PR title</span>
<span class="na">on</span><span class="pi">:</span>
  <span class="na">pull_request</span><span class="pi">:</span>
    <span class="na">types</span><span class="pi">:</span> <span class="pi">[</span><span class="nv">opened</span><span class="pi">,</span> <span class="nv">edited</span><span class="pi">]</span>
<span class="na">jobs</span><span class="pi">:</span>
  <span class="na">check</span><span class="pi">:</span>
    <span class="na">runs-on</span><span class="pi">:</span> <span class="s">ubuntu-latest</span>
    <span class="na">steps</span><span class="pi">:</span>
      <span class="pi">-</span> <span class="na">name</span><span class="pi">:</span> <span class="s">Check PR title</span>
        <span class="na">run</span><span class="pi">:</span> <span class="pi">|</span>
          <span class="s">title="${{ github.event.pull_request.title }}"</span>
          <span class="s">if [[ ! $title =~ ^.*:\ .*$ ]]; then</span>
            <span class="s">echo "Pull request titles must adhere to Conventional Commits: https://www.conventionalcommits.org"</span>
            <span class="s">exit 1</span>
          <span class="s">fi</span>
</code></pre></div></div>

<h4 id="impact">Impact</h4>

<p>This vulnerability allows for arbitrary command injection into the bash script. For a proof a concept a Pull Request with the following title <code class="language-plaintext highlighter-rouge">title"; exit 0 #</code> would return early.</p>

<p>Workflows triggered by <code class="language-plaintext highlighter-rouge">pull_request</code> have limited repository token and no access to secrets. The attacker couldn’t do much except CI DoS attacks or running their own code in the context of the GitHub action runner.</p>

<h2 id="credit">Credit</h2>

<p>This issue was discovered and reported by GHSL team member <a href="https://github.com/JarLob">@JarLob (Jaroslav Lobačevski)</a>.</p>

<h2 id="contact">Contact</h2>

<p>You can contact the GHSL team at <code class="language-plaintext highlighter-rouge">securitylab@github.com</code>, please include a reference to <code class="language-plaintext highlighter-rouge">GHSL-2020-230</code> in any communication regarding this issue.</p