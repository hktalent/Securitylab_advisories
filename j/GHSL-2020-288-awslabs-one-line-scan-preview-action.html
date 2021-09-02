<header class="post-header d-block mb-6">
      <div class="date text-mono f5 my-3">December 16, 2020</div>
      <h1 class="my-2 h00-mktg lh-condensed">GHSL-2020-288: Unauthorized repository modification or secrets exfiltration in GitHub workflows comsuming awslabs/one-line-scan</h1>

      
      
      
      
      

      

      <a target="_blank" class="sc-frDJqD SgxRc d-inline-flex flex-row flex-items-center text-gray" href="https://github.com/jarlob">
        <img class="mr-3" src="https://avatars.githubusercontent.com/u/26652396?s=35" height="35" width="35">
        <span>Jaroslav Lobacevski</span>
      </a>
    </header>

    <main id="content" class="markdown-body" aria-label="Content">
      <h2 id="summary">Summary</h2>

<p>The design and promoted usage examples of <a href="https://github.com/awslabs/one-line-scan">awslabs/one-line-scan</a> makes consuming workflows vulnerable to arbitrary code execution.</p>

<h2 id="product">Product</h2>

<ul>
  <li><a href="https://github.com/awslabs/one-line-scan">awslabs/one-line-scan</a> tool</li>
  <li><a href="https://github.com/awslabs/ktf">awslabs/ktf</a> repository</li>
</ul>

<h2 id="tested-version">Tested Version</h2>

<p>The latest changesets to the date <a href="https://github.com/awslabs/one-line-scan/tree/be492f8996397e5314339f3420455ce1231312a2">be492f8</a> and <a href="https://github.com/awslabs/ktf/blob/19c8bfe91cbb750934b8c2edf626e4d48b8a16c1/.github/workflows/one-line-cr-bot.yml">19c8bfe</a>.</p>

<h2 id="details">Details</h2>

<p><code class="language-plaintext highlighter-rouge">pull_request_target</code> was introduced to allow triggered workflows to comment on PRs, label them, assign people, etc.. In order to make it possible the triggered action runner has read/write token for the base repository and the access to secrets. In order to prevent untrusted code from execution it runs in a context of the base repository.</p>

<p>By explicitly checking out and running build script from a fork the untrusted code is running in an environment that is able to push to the base repository and to access secrets.</p>

<h3 id="issue-awslabsone-line-scan-is-designed-to-run-potentially-untrusted-code-from-a-pull-request-on-pull_request_target">Issue: <a href="https://github.com/awslabs/one-line-scan">awslabs/one-line-scan</a> is designed to run potentially untrusted code from a Pull Request on <code class="language-plaintext highlighter-rouge">pull_request_target</code></h3>

<p>Below is an excerpt from an example of usage in the documentation:</p>

<div class="language-yaml highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="na">on</span><span class="pi">:</span>
<span class="na">pull_request_target</span><span class="pi">:</span>
  <span class="c1"># [ACTION REQUIRED] Set the branch you want to analyze PRs for</span>
  <span class="na">branches</span><span class="pi">:</span>
    <span class="pi">-</span> <span class="s1">'</span><span class="s">**'</span>
<span class="nn">...</span>
    <span class="c1"># Get the code, fetch the full history to make sure we have the compare commit as well</span>
    <span class="na">steps</span><span class="pi">:</span>
    <span class="pi">-</span> <span class="na">uses</span><span class="pi">:</span> <span class="s">actions/checkout@v2</span>
    <span class="na">with</span><span class="pi">:</span>
        <span class="na">fetch-depth</span><span class="pi">:</span> <span class="m">0</span>
<span class="nn">...</span>
    <span class="c1"># Get the reference remote</span>
    <span class="pi">-</span> <span class="na">name</span><span class="pi">:</span> <span class="s">Setup Reference Commit Remote</span>
    <span class="c1"># [ACTION REQUIRED] Add the https URL of your repository</span>
    <span class="na">run</span><span class="pi">:</span> <span class="s">git remote add reference https://github.com/awslabs/ktf.git</span>
    <span class="pi">-</span> <span class="na">name</span><span class="pi">:</span> <span class="s">Fetch Reference Commit Remote</span>
    <span class="na">run</span><span class="pi">:</span> <span class="s">git fetch reference</span>

    <span class="c1"># Get one-line-scan, the tool we will use for analysis</span>
    <span class="pi">-</span> <span class="na">name</span><span class="pi">:</span> <span class="s">Get OneLineScan</span>
    <span class="na">run</span><span class="pi">:</span>  <span class="s">git clone -b one-line-cr-bot https://github.com/awslabs/one-line-scan.git ../one-line-scan</span>
<span class="nn">...</span>
    <span class="c1"># Run the analysis, parameterized for this package</span>
    <span class="pi">-</span> <span class="na">name</span><span class="pi">:</span> <span class="s">one-line-cr-analysis</span>
    <span class="na">env</span><span class="pi">:</span>
        <span class="c1"># [ACTION REQUIRED] Adapt the values below accordingly</span>
        <span class="c1"># 'reference' is the name of the remote to use</span>
        <span class="c1"># PR local: ${{github.event.pull_request.head.repo.full_name}}/${{github.event.pull_request.head.ref}}</span>
        <span class="na">BASE_COMMIT</span><span class="pi">:</span> <span class="s2">"</span><span class="s">reference/mainline"</span>
        <span class="na">BUILD_COMMAND</span><span class="pi">:</span> <span class="s2">"</span><span class="s">make</span><span class="nv"> </span><span class="s">-B</span><span class="nv"> </span><span class="s">all"</span>
        <span class="na">CLEAN_COMMAND</span><span class="pi">:</span> <span class="s2">"</span><span class="s">make</span><span class="nv"> </span><span class="s">clean"</span>
<span class="nn">...</span>
    <span class="c1"># Be explicit about the tools to be used</span>
    <span class="na">run</span><span class="pi">:</span> <span class="s">../one-line-scan/one-line-cr-bot.sh -E infer -E cppcheck</span>
<span class="nn">...</span>
</code></pre></div></div>

<p>Since the action needs repository write token for functioning and worklows triggered on <code class="language-plaintext highlighter-rouge">pull_request</code> do not have the access to secrets it promotes using <code class="language-plaintext highlighter-rouge">pull_request_target</code> and explicitly checking out the code from the Pull Request. Even though the example by mistake checks out not the PR branch, but the base, the affected <a href="https://github.com/awslabs/ktf">awslabs/ktf</a> has fixed the error and actually checks out the PR:</p>

<div class="language-yaml highlighter-rouge"><div class="highlight"><pre class="highlight"><code>    <span class="c1"># Get the code, fetch the full history to make sure we have the compare commit as well</span>
    <span class="pi">-</span> <span class="na">uses</span><span class="pi">:</span> <span class="s">actions/checkout@v2</span>
      <span class="na">with</span><span class="pi">:</span>
        <span class="na">fetch-depth</span><span class="pi">:</span> <span class="m">0</span>
        <span class="na">ref</span><span class="pi">:</span> <span class="s">${{github.event.pull_request.head.ref}}</span>
        <span class="na">repository</span><span class="pi">:</span> <span class="s">${{github.event.pull_request.head.repo.full_name}}</span>
</code></pre></div></div>

<p>One of the tool’s arguments is a <code class="language-plaintext highlighter-rouge">BUILD_COMMAND</code> script. A potentially untrusted Pull Request may execute an arbitrary script in a workflow that has read/write repository access and potentially can access secrets.</p>

<h4 id="impact">Impact</h4>

<p>The vulnerability allows for unauthorized modification of the using repository and secrets exfiltration.</p>

<h2 id="coordinated-disclosure-timeline">Coordinated Disclosure Timeline</h2>

<ul>
  <li>2020-11-30: Report sent to maintainers</li>
  <li>2020-11-30: Maintainers acknowledged</li>
  <li>2020-11-30: Issue resolved</li>
  <li>2020-11-30: The internal investigation concluded that the vulnerability has not been exploited</li>
</ul>

<h2 id="credit">Credit</h2>

<p>This issue was discovered and reported by GHSL team member <a href="https://github.com/JarLob">@JarLob (Jaroslav Lobačevski)</a>.</p>

<h2 id="contact">Contact</h2>

<p>You can contact the GHSL team at <code class="language-plaintext highlighter-rouge">securitylab@github.com</code>, please include a reference to <code class="language-plaintext highlighter-rouge">GHSL-2020-288</code> in any communication regarding this issue.</p>

 