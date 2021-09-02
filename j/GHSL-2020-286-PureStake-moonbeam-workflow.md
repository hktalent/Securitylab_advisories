<header class="post-header d-block mb-6">
      <div class="date text-mono f5 my-3">December 16, 2020</div>
      <h1 class="my-2 h00-mktg lh-condensed">GHSL-2020-286: Unauthorized repository modification or secrets exfiltration in the GitHub workflow of PureStake/moonbeam</h1>

      
      
      
      
      

      

      <a target="_blank" class="sc-frDJqD SgxRc d-inline-flex flex-row flex-items-center text-gray" href="https://github.com/jarlob">
        <img class="mr-3" src="https://avatars.githubusercontent.com/u/26652396?s=35" height="35" width="35">
        <span>Jaroslav Lobacevski</span>
      </a>
    </header>

    <main id="content" class="markdown-body" aria-label="Content">
      <h2 id="summary">Summary</h2>

<p>The <a href="https://github.com/PureStake/moonbeam/blob/master/.github/workflows/release.yml">release.yml</a> GitHub workflow is vulnerable to unauthorized modification of the base repository or secrets exfiltration from a Pull Request.</p>

<h2 id="product">Product</h2>

<p><a href="https://github.com/PureStake/moonbeam">PureStake/moonbeam</a> GitHub repository</p>

<h2 id="tested-version">Tested Version</h2>

<p>The latest changeset <a href="https://github.com/PureStake/moonbeam/blob/994ad70e1f8b797453b21a171728a330dcf1120e/.github/workflows/release.yml">994ad70</a> to the date.</p>

<h2 id="details">Details</h2>

<h3 id="issue-untrusted-code-is-explicitly-checked-out-and-run-on-a-pull-request-from-a-fork">Issue: Untrusted code is explicitly checked out and run on a Pull Request from a fork</h3>

<p><code class="language-plaintext highlighter-rouge">pull_request_target</code> was introduced to allow triggered workflows to comment on PRs, label them, assign people, etc.. In order to make it possible the triggered action runner has read/write token for the base repository and the access to secrets. In order to prevent untrusted code from execution it runs in a context of the base repository.</p>

<p>By explicitly checking out and running build script from a fork the untrusted code is running in an environment that is able to push to the base repository and to access secrets.</p>

<div class="language-yaml highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="c1"># This is only allowing pushes on the moonbeam repo or pull request.</span>
<span class="c1"># In the case of pull request, the CI executes the workflow from</span>
<span class="c1"># the commit the **PR is merging into**. This prevents malicious attack trying</span>
<span class="c1"># to change the CI in the PR.</span>
<span class="c1">####### DO NOT CHANGE THIS !! #######</span>
<span class="na">on</span><span class="pi">:</span> <span class="pi">[</span><span class="s2">"</span><span class="s">push"</span><span class="pi">,</span> <span class="s2">"</span><span class="s">pull_request_target"</span><span class="pi">]</span>

<span class="nn">...</span>
    <span class="na">if</span><span class="pi">:</span> <span class="s">${{ github.repository == 'PureStake/moonbeam' }}</span>
<span class="nn">...</span>
    <span class="na">steps</span><span class="pi">:</span>
      <span class="pi">-</span> <span class="na">name</span><span class="pi">:</span> <span class="s">Checkout</span>
        <span class="na">if</span><span class="pi">:</span> <span class="s">github.event_name == 'pull_request_target'</span>
        <span class="na">uses</span><span class="pi">:</span> <span class="s">actions/checkout@v2</span>
        <span class="na">with</span><span class="pi">:</span>
          <span class="na">fetch-depth</span><span class="pi">:</span> <span class="m">0</span>
          <span class="na">ref</span><span class="pi">:</span> <span class="s">refs/pull/${{ github.event.pull_request.number }}/merge</span>
<span class="nn">...</span>
      <span class="pi">-</span> <span class="na">name</span><span class="pi">:</span> <span class="s">Build Parachain Node</span>
        <span class="na">run</span><span class="pi">:</span> <span class="s">cargo build --release --verbose --all</span>
</code></pre></div></div>

<h4 id="impact">Impact</h4>

<p>The vulnerability allows for unauthorized modification of the base repository and secrets exfiltration.</p>

<h2 id="coordinated-disclosure-timeline">Coordinated Disclosure Timeline</h2>

<ul>
  <li>2020-11-30: Report sent to maintainers</li>
  <li>2020-11-30: Maintainers acknowledges</li>
  <li>2020-12-01: Issue resolved</li>
</ul>

<h2 id="credit">Credit</h2>

<p>This issue was discovered and reported by GHSL team member <a href="https://github.com/JarLob">@JarLob (Jaroslav Lobačevski)</a>.</p>

<h2 id="contact">Contact</h2>

<p>You can contact the GHSL team at <code class="language-plaintext highlighter-rouge">securitylab@github.com</code>, please include a reference to <code class="language-plaintext highlighter-rouge">GHSL-2020-286</code> in any communication regarding this issue.</p>

   