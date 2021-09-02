<header class="post-header d-block mb-6">
      <div class="date text-mono f5 my-3">March 3, 2021</div>
      <h1 class="my-2 h00-mktg lh-condensed">GHSL-2020-266: Unauthorized repository modification or secrets exfiltration in a GitHub workflow of afc163/surge-preview</h1>

      
      
      
      
      

      

      <a target="_blank" class="sc-frDJqD SgxRc d-inline-flex flex-row flex-items-center text-gray" href="https://github.com/jarlob">
        <img class="mr-3" src="https://avatars.githubusercontent.com/u/26652396?s=35" height="35" width="35">
        <span>Jaroslav Lobacevski</span>
      </a>
    </header>

    <main id="content" class="markdown-body" aria-label="Content">
      <h2 id="coordinated-disclosure-timeline">Coordinated Disclosure Timeline</h2>

<ul>
  <li>2020-11-30: Report sent to maintainer.</li>
  <li>2021-01-23: Issue resolved.</li>
</ul>

<h2 id="summary">Summary</h2>

<p>The design and promoted usage examples of <a href="https://github.com/afc163/surge-preview">afc163/surge-preview GitHub action</a> makes the consuming workflows vulnerable to arbitrary code execution. The repository of <a href="https://github.com/afc163/surge-preview">afc163/surge-preview GitHub action</a> falls into the same trap and is vulnerable to arbitrary code execution.</p>

<h2 id="product">Product</h2>

<p><a href="https://github.com/afc163/surge-preview">afc163/surge-preview action and GitHub repository</a></p>

<h2 id="tested-version">Tested Version</h2>

<p>The latest changeset <a href="https://github.com/afc163/surge-preview/tree/33b194bf1788adbff6938d401405d190a77d211e">33b194b</a> to the date.</p>

<h2 id="details">Details</h2>

<p><code class="language-plaintext highlighter-rouge">pull_request_target</code> was introduced to allow triggered workflows to comment on PRs, label them, assign people, etc.. In order to make it possible the triggered action runner has read/write token for the base repository and the access to secrets. In order to prevent untrusted code from execution it runs in a context of the base repository.</p>

<p>By explicitly checking out and running build script from a fork the untrusted code is running in an environment that is able to push to the base repository and to access secrets.</p>

<h3 id="issue-1-afc163surge-preview--github-action-is-designed-to-run-potentially-untrusted-code-from-a-pull-request-on-pull_request_target">Issue 1: <a href="https://github.com/afc163/surge-preview">afc163/surge-preview</a>  GitHub action is designed to run potentially untrusted code from a Pull Request on <code class="language-plaintext highlighter-rouge">pull_request_target</code></h3>

<p>Below is an excerpt from an example of usage in the documentation:</p>

<div class="language-yaml highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="na">on</span><span class="pi">:</span> <span class="s">pull_request_target</span>
<span class="nn">...</span>
      <span class="pi">-</span> <span class="na">uses</span><span class="pi">:</span> <span class="s">actions/checkout@v2</span>
        <span class="na">with</span><span class="pi">:</span>
          <span class="na">ref</span><span class="pi">:</span> <span class="s">refs/pull/${{ github.event.pull_request.number }}/merge</span>
      <span class="pi">-</span> <span class="na">uses</span><span class="pi">:</span> <span class="s">afc163/surge-preview@v1</span>
        <span class="na">id</span><span class="pi">:</span> <span class="s">preview_step</span>
        <span class="na">with</span><span class="pi">:</span>
          <span class="na">surge_token</span><span class="pi">:</span> <span class="s">${{ secrets.SURGE_TOKEN }}</span>
          <span class="na">github_token</span><span class="pi">:</span> <span class="s">${{ secrets.GITHUB_TOKEN }}</span>
          <span class="na">dist</span><span class="pi">:</span> <span class="s">public</span>
          <span class="na">build</span><span class="pi">:</span> <span class="pi">|</span>
            <span class="s">npm install</span>
            <span class="s">npm run build</span>
<span class="s">...</span>
</code></pre></div></div>

<p>Since the action needs the <code class="language-plaintext highlighter-rouge">SURGE_TOKEN</code> for functioning and worklows triggered on <code class="language-plaintext highlighter-rouge">pull_request</code> do not have the access to secrets it promotes using <code class="language-plaintext highlighter-rouge">pull_request_target</code> and explicitly checking out the code from the Pull Request. One of the action’s arguments is a <code class="language-plaintext highlighter-rouge">build</code> script that instructs the action how to build the source. If the argument is not provided it uses <code class="language-plaintext highlighter-rouge">npm install &amp; npm run build</code> by default:</p>

<div class="language-yaml highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="nn">...</span>
  <span class="na">build</span><span class="pi">:</span>
    <span class="na">description</span><span class="pi">:</span> <span class="s1">'</span><span class="s">build</span><span class="nv"> </span><span class="s">scripts'</span>
    <span class="na">default</span><span class="pi">:</span> <span class="pi">|</span>
      <span class="s">npm install</span>
      <span class="s">npm run build</span>
    <span class="na">required</span><span class="pi">:</span> <span class="no">false</span>
<span class="nn">...</span>
</code></pre></div></div>

<p>A potentially untrusted Pull Request may execute an arbitrary script in a workflow that has read/write repository access and potentially can access secrets.</p>

<h4 id="impact">Impact</h4>

<p>The vulnerability allows for unauthorized modification of the using repository and secrets exfiltration.</p>

<h3 id="issue-2-untrusted-code-is-explicitly-checked-out-and-run-on-a-pull-request-from-a-fork">Issue 2: Untrusted code is explicitly checked out and run on a Pull Request from a fork</h3>

<p>The action’s repositry itself has a Pull Request <a href="https://github.com/afc163/surge-preview/blob/b19206c3ef321d6511a9fdbb079a4dfe8e786aa4/.github/workflows/preview.yml">workflow</a>:</p>

<div class="language-yaml highlighter-rouge"><div class="highlight"><pre class="highlight"><code>  <span class="na">pull_request_target</span><span class="pi">:</span>
    <span class="c1"># use default types + closed event type</span>
    <span class="na">types</span><span class="pi">:</span> <span class="pi">[</span><span class="nv">opened</span><span class="pi">,</span> <span class="nv">synchronize</span><span class="pi">,</span> <span class="nv">reopened</span><span class="pi">,</span> <span class="nv">closed</span><span class="pi">]</span>
<span class="nn">...</span>
      <span class="pi">-</span> <span class="na">uses</span><span class="pi">:</span> <span class="s">actions/checkout@v2</span>
        <span class="na">with</span><span class="pi">:</span>
          <span class="na">ref</span><span class="pi">:</span> <span class="s">refs/pull/${{ github.event.pull_request.number }}/merge</span>
      <span class="pi">-</span> <span class="na">uses</span><span class="pi">:</span> <span class="s">./</span>
        <span class="na">id</span><span class="pi">:</span> <span class="s">preview_step</span>
        <span class="na">name</span><span class="pi">:</span> <span class="s">test afc163/surge-preview</span>
        <span class="na">with</span><span class="pi">:</span>
          <span class="na">surge_token</span><span class="pi">:</span> <span class="s">${{ secrets.SURGE_TOKEN }}</span>
          <span class="na">github_token</span><span class="pi">:</span> <span class="s">${{ secrets.GITHUB_TOKEN }}</span>
          <span class="na">teardown</span><span class="pi">:</span> <span class="s1">'</span><span class="s">true'</span>
          <span class="na">dist</span><span class="pi">:</span> <span class="s">public/preview</span>
          <span class="na">build</span><span class="pi">:</span> <span class="pi">|</span>
            <span class="s">mkdir -p public/preview</span>
            <span class="s">npm install</span>
            <span class="s">npm run build-preview -- public/preview</span>
<span class="s">...</span>
</code></pre></div></div>

<h4 id="impact-1">Impact</h4>

<p>The vulnerability allows for unauthorized modification of the base repository and secrets exfiltration.</p>

<h2 id="credit">Credit</h2>

<p>This issue was discovered and reported by GHSL team member <a href="https://github.com/JarLob">@JarLob (Jaroslav Lobačevski)</a>.</p>

<h2 id="contact">Contact</h2>

<p>You can contact the GHSL team at <code class="language-plaintext highlighter-rouge">securitylab@github.com</code>, please include a reference to <code class="language-plaintext highlighter-rouge">GHSL-2020-266</code> in any communication regarding this issue.</p>
