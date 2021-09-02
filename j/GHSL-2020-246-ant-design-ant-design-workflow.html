<header class="post-header d-block mb-6">
      <div class="date text-mono f5 my-3">March 3, 2021</div>
      <h1 class="my-2 h00-mktg lh-condensed">GHSL-2020-246: Unauthorized repository modification or secrets exfiltration in GitHub workflows of ant-design</h1>

      
      
      
      
      

      

      <a target="_blank" class="sc-frDJqD SgxRc d-inline-flex flex-row flex-items-center text-gray" href="https://github.com/jarlob">
        <img class="mr-3" src="https://avatars.githubusercontent.com/u/26652396?s=35" height="35" width="35">
        <span>Jaroslav Lobacevski</span>
      </a>
    </header>

    <main id="content" class="markdown-body" aria-label="Content">
      <h2 id="coordinated-disclosure-timeline">Coordinated Disclosure Timeline</h2>

<ul>
  <li>2020-11-26: Report sent to maintainer</li>
  <li>2021-02-23: Issue fixed</li>
</ul>

<h2 id="summary">Summary</h2>

<p>The <a href="https://github.com/ant-design/ant-design/blob/master/.github/workflows/ui.yml">ant-design/ui.yml</a>, <a href="https://github.com/ant-design/ant-design-pro/blob/master/.github/workflows/preview.yml">ant-design-pro/preview.yml</a> and <a href="https://github.com/ant-design/pro-components/blob/master/.github/workflows/preview.yml">pro-components/preview.yml</a> GitHub workflows are vulnerable to arbitrary code execution.</p>

<h2 id="product">Product</h2>

<p><a href="https://github.com/ant-design/ant-design">ant-design/ant-design GitHub repository</a><br />
<a href="https://github.com/ant-design/ant-design-pro">ant-design/ant-design-pro GitHub repository</a><br />
<a href="https://github.com/ant-design/pro-components">ant-design/pro-components GitHub repository</a></p>

<h2 id="tested-version">Tested Version</h2>

<p>The latest changesets <a href="https://github.com/ant-design/ant-design/blob/3f126f116ffd38d2b8f14467f6f291bdbe40b87c/.github/workflows/ui.yml">3f126f1</a>, <a href="https://github.com/ant-design/ant-design-pro/blob/e451d76b981e43cf8a85517be9f36b1960f6c695/.github/workflows/preview.yml">e451d76</a> and <a href="https://github.com/ant-design/pro-components/blob/fb2245e41d99401ba7c00c71d42a8e2200cf5fe1/.github/workflows/preview.yml">fb2245e</a> to the date.</p>

<h2 id="details">Details</h2>

<h3 id="issue-untrusted-code-is-explicitly-checked-out-and-run-on-a-pull-request-from-a-fork">Issue: Untrusted code is explicitly checked out and run on a Pull Request from a fork</h3>

<p><code class="language-plaintext highlighter-rouge">pull_request_target</code> was introduced to allow triggered workflows to comment on PRs, label them, assign people, etc.. In order to make it possible the triggered action runner has read/write token for the base repository and the access to secrets. In order to prevent untrusted code from execution it runs in a context of the base repository.</p>

<p>By explicitly checking out and running build script from a fork the untrusted code is running in an environment that is able to push to the base repository and to access secrets.</p>

<p>From preview.yml:</p>

<div class="language-yaml highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="na">on</span><span class="pi">:</span>
  <span class="na">pull_request_target</span><span class="pi">:</span>
<span class="nn">...</span>
      <span class="pi">-</span> <span class="na">name</span><span class="pi">:</span> <span class="s">checkout</span>
        <span class="na">if</span><span class="pi">:</span> <span class="s">github.event_name == 'pull_request_target'</span>
        <span class="na">uses</span><span class="pi">:</span> <span class="s">actions/checkout@master</span>
        <span class="na">with</span><span class="pi">:</span>
          <span class="na">ref</span><span class="pi">:</span> <span class="s">refs/pull/${{ github.event.pull_request.number }}/head</span>
<span class="nn">...</span>
      <span class="pi">-</span> <span class="na">name</span><span class="pi">:</span> <span class="s">install</span>
        <span class="na">run</span><span class="pi">:</span> <span class="s">npm install</span>
</code></pre></div></div>

<p>From ui.yml:</p>
<div class="language-yaml highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="na">on</span><span class="pi">:</span> <span class="s">pull_request_target</span>
<span class="nn">...</span>
      <span class="pi">-</span> <span class="na">uses</span><span class="pi">:</span> <span class="s">actions/checkout@v2</span>
        <span class="na">with</span><span class="pi">:</span>
          <span class="na">ref</span><span class="pi">:</span> <span class="s">refs/pull/${{ github.event.pull_request.number }}/merge</span>
      <span class="pi">-</span> <span class="na">uses</span><span class="pi">:</span> <span class="s">afc163/surge-preview@v1</span>
        <span class="na">with</span><span class="pi">:</span>
          <span class="na">surge_token</span><span class="pi">:</span> <span class="s">${{ secrets.SURGE_TOKEN }}</span>
          <span class="na">github_token</span><span class="pi">:</span> <span class="s">${{ secrets.GITHUB_TOKEN }}</span>
          <span class="na">build</span><span class="pi">:</span> <span class="pi">|</span>
            <span class="s">npm install</span>
            <span class="s">npm install umi-plugin-pro --save</span>
            <span class="s">npm run build</span>
<span class="s">...</span>
</code></pre></div></div>

<h4 id="impact">Impact</h4>

<p>The vulnerability allows for unauthorized modification of the base repository and secrets exfiltration.</p>

<h2 id="credit">Credit</h2>

<p>This issue was discovered and reported by GHSL team member <a href="https://github.com/JarLob">@JarLob (Jaroslav Lobačevski)</a>.</p>

<h2 id="contact">Contact</h2>

<p>You can contact the GHSL team at <code class="language-plaintext highlighter-rouge">securitylab@github.com</code>, please include a reference to <code class="language-plaintext highlighter-rouge">GHSL-2020-246</code> in any communication regarding this issue.</p>

   