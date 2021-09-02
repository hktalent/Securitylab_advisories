<header class="post-header d-block mb-6">
      <div class="date text-mono f5 my-3">March 25, 2021</div>
      <h1 class="my-2 h00-mktg lh-condensed">GHSL-2020-331: Unauthorized repository modification or secrets exfiltration in a GitHub workflow of appsmith</h1>

      
      
      
      
      

      

      <a target="_blank" class="sc-frDJqD SgxRc d-inline-flex flex-row flex-items-center text-gray" href="https://github.com/jarlob">
        <img class="mr-3" src="https://avatars.githubusercontent.com/u/26652396?s=35" height="35" width="35">
        <span>Jaroslav Lobacevski</span>
      </a>
    </header>

    <main id="content" class="markdown-body" aria-label="Content">
      <h2 id="coordinated-disclosure-timeline">Coordinated Disclosure Timeline</h2>

<ul>
  <li>2020-12-11: Issue reported to maintainers.</li>
  <li>2020-12-12: Issue acknowledged.</li>
  <li>2021-01-16: Asked the maintainers for update. No reply.</li>
  <li>2021-02-23: Asked the maintainers for update. No reply.</li>
  <li>2021-03-11: Partial fix was applied.</li>
  <li>2021-03-11: Disclosure deadline reached.</li>
  <li>2021-03-25: Publication as per our <a href="https://securitylab.github.com/advisories/#policy">disclosure policy</a>.</li>
  <li>2021-03-26: Maintainers notified GitHub Security Lab that the issue was mitigated.</li>
</ul>

<h2 id="summary">Summary</h2>

<p>The <a href="https://github.com/appsmithorg/appsmith/blob/release/.github/workflows/client.yml">client.yml</a> GitHub workflow is vulnerable to unauthorized modification of the base repository and secret exfiltration.</p>

<h2 id="product">Product</h2>

<p><a href="https://github.com/appsmithorg/appsmith">appsmithorg/appsmith</a> GitHub repository</p>

<h2 id="tested-version">Tested Version</h2>

<p>The latest changeset <a href="https://github.com/appsmithorg/appsmith/blob/75b3f18a928ca604dd20d9c3bb244dfc99d5fc3d/.github/workflows/client.yml">75b3f18</a> to the date.</p>

<h2 id="details">Details</h2>

<h3 id="issue-untrusted-code-is-explicitly-checked-out-and-run-on-a-pull-request-from-a-fork">Issue: Untrusted code is explicitly checked out and run on a Pull Request from a fork</h3>

<p><code class="language-plaintext highlighter-rouge">pull_request_target</code> was introduced to allow triggered workflows to comment on PRs, label them, assign people, etc. In order to make it possible the triggered action runner has read/write token for the base repository and access to secrets. In order to prevent untrusted code from execution, it runs in the context of the base repository.</p>

<p>By explicitly checking out and running the build script from a fork, the untrusted code will be able to push to the base repository and access its secrets.</p>

<div class="language-yaml highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="na">on</span><span class="pi">:</span>
<span class="nn">...</span>
  <span class="na">pull_request_target</span><span class="pi">:</span>
    <span class="na">branches</span><span class="pi">:</span> <span class="pi">[</span><span class="nv">release</span><span class="pi">,</span> <span class="nv">master</span><span class="pi">]</span>
    <span class="na">paths</span><span class="pi">:</span>
      <span class="pi">-</span> <span class="s1">'</span><span class="s">app/client/**'</span>
      <span class="pi">-</span> <span class="s1">'</span><span class="s">!app/client/cypress/manual_TestSuite/**'</span>
<span class="nn">...</span>
      <span class="c1"># Checkout the code</span>
      <span class="pi">-</span> <span class="na">name</span><span class="pi">:</span> <span class="s">Checkout the merged commit from PR and base branch</span>
        <span class="na">if</span><span class="pi">:</span> <span class="s">${{ github.event_name == 'pull_request_target' }}</span>
        <span class="na">uses</span><span class="pi">:</span> <span class="s">actions/checkout@v2</span>
        <span class="na">with</span><span class="pi">:</span>
          <span class="na">ref</span><span class="pi">:</span> <span class="s">refs/pull/${{ github.event.pull_request.number }}/merge</span>
<span class="nn">...</span>
      <span class="c1"># Install all the dependencies</span>
      <span class="pi">-</span> <span class="na">name</span><span class="pi">:</span> <span class="s">Install dependencies</span>
        <span class="na">run</span><span class="pi">:</span> <span class="s">yarn install</span>
<span class="nn">...</span>
      <span class="pi">-</span> <span class="na">name</span><span class="pi">:</span> <span class="s">Run the jest tests</span>
        <span class="na">run</span><span class="pi">:</span> <span class="s">REACT_APP_ENVIRONMENT=${{steps.vars.outputs.REACT_APP_ENVIRONMENT}} yarn run test:unit</span>
<span class="nn">...</span>
</code></pre></div></div>

<h4 id="impact">Impact</h4>

<p>The vulnerability allows for unauthorized modification of the base repository and secrets exfiltration.</p>

<h2 id="credit">Credit</h2>

<p>This issue was discovered and reported by GHSL team member <a href="https://github.com/JarLob">@JarLob (Jaroslav Lobačevski)</a>.</p>

<h2 id="contact">Contact</h2>

<p>You can contact the GHSL team at <code class="language-plaintext highlighter-rouge">securitylab@github.com</code>, please include a reference to <code class="language-plaintext highlighter-rouge">GHSL-2020-331</code> in any communication regarding this issue.</p>

   