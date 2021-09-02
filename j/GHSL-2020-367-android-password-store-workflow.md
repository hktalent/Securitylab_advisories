<header class="post-header d-block mb-6">
      <div class="date text-mono f5 my-3">February 3, 2021</div>
      <h1 class="my-2 h00-mktg lh-condensed">GHSL-2020-367: Arbitrary code execution in android-password-store/Android-Password-Store workflow</h1>

      
      
      
      
      

      

      <a target="_blank" class="sc-frDJqD SgxRc d-inline-flex flex-row flex-items-center text-gray" href="https://github.com/jarlob">
        <img class="mr-3" src="https://avatars.githubusercontent.com/u/26652396?s=35" height="35" width="35">
        <span>Jaroslav Lobacevski</span>
      </a>
    </header>

    <main id="content" class="markdown-body" aria-label="Content">
      <h2 id="coordinated-disclosure-timeline">Coordinated Disclosure Timeline</h2>

<ul>
  <li>2020-12-21: Report sent to maintainers.</li>
  <li>2020-12-22: Maintainers acknowledged.</li>
  <li>2020-12-22: Issue resolved.</li>
</ul>

<h2 id="summary">Summary</h2>

<p>The <a href="https://github.com/android-password-store/Android-Password-Store/blob/develop/.github/workflows/pull_request.yml">pull_request.yml</a> GitHub workflow is vulnerable to unauthorized modification of the base repository or secrets exfiltration from a Pull Request.</p>

<h2 id="product">Product</h2>

<p><a href="https://github.com/android-password-store/Android-Password-Store">android-password-store/Android-Password-Store</a> GitHub repository</p>

<h2 id="tested-version">Tested Version</h2>

<p>The latest changeset <a href="https://github.com/android-password-store/Android-Password-Store/blob/67393ef62d386d0ce61838fe1d2dff8d6cbae5ee/.github/workflows/pull_request.yml">67393ef</a> to the date.</p>

<h2 id="details">Details</h2>

<h3 id="issue-untrusted-code-is-explicitly-checked-out-and-run-on-a-pull-request-from-a-fork">Issue: Untrusted code is explicitly checked out and run on a Pull Request from a fork</h3>

<p>Workflows triggered on <code class="language-plaintext highlighter-rouge">pull_request_target</code> have read/write tokens for the base repository and the access to secrets. By explicitly checking out and running the build script from a fork the untrusted code is running in an environment that is able to push to the base repository and to access secrets. More details can be found in the article <a href="https://securitylab.github.com/research/github-actions-preventing-pwn-requests/">Keeping your GitHub Actions and workflows secure: Preventing pwn requests</a>.</p>

<div class="language-yaml highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="na">on</span><span class="pi">:</span> <span class="pi">[</span><span class="nv">pull_request_target</span><span class="pi">]</span>
<span class="nn">...</span>
<span class="s">      - name</span><span class="pi">:</span> <span class="s">Checkout code (pull_request)</span>
<span class="s">        if</span><span class="pi">:</span> <span class="s">github.event_name == 'pull_request' || github.event_name == 'pull_request_target'</span>
<span class="s">        uses</span><span class="pi">:</span> <span class="s">actions/checkout@v2</span>
<span class="s">        with</span><span class="pi">:</span>
<span class="s">          ref</span><span class="pi">:</span> <span class="s1">'</span><span class="s">refs/pull/${{</span><span class="nv"> </span><span class="s">github.event.number</span><span class="nv"> </span><span class="s">}}/merge'</span>
<span class="nn">...</span>
    <span class="pi">-</span> <span class="na">name</span><span class="pi">:</span> <span class="s">Checkout repository</span>
      <span class="na">if</span><span class="pi">:</span> <span class="s">${{ steps.service-changed.outputs.result == 'true' }}</span>
      <span class="na">uses</span><span class="pi">:</span> <span class="s">actions/checkout@5a4ac9002d0be2fb38bd78e4b4dbde5606d7042f</span>
      <span class="na">with</span><span class="pi">:</span>
        <span class="na">ref</span><span class="pi">:</span> <span class="s">refs/pull/${{ github.event.pull_request.number }}/merge</span>
<span class="nn">...</span>
    <span class="pi">-</span> <span class="na">name</span><span class="pi">:</span> <span class="s">Run unit tests</span>
      <span class="na">if</span><span class="pi">:</span> <span class="s">${{ steps.service-changed.outputs.result == 'true' }}</span>
      <span class="na">uses</span><span class="pi">:</span> <span class="s">burrunan/gradle-cache-action@03c71a8ba93d670980695505f48f49daf43704a6</span>
      <span class="na">with</span><span class="pi">:</span>
        <span class="na">arguments</span><span class="pi">:</span> <span class="s">apiCheck testFreeDebug lintFreeDebug</span>
<span class="nn">...</span>
</code></pre></div></div>

<h4 id="impact">Impact</h4>

<p>The vulnerability allows for unauthorized modification of the base repository and secrets exfiltration.</p>

<h2 id="credit">Credit</h2>

<p>This issue was discovered and reported by GHSL team member <a href="https://github.com/JarLob">@JarLob (Jaroslav Lobačevski)</a>.</p>

<h2 id="contact">Contact</h2>

<p>You can contact the GHSL team at <code class="language-plaintext highlighter-rouge">securitylab@github.com</code>, please include a reference to <code class="language-plaintext highlighter-rouge">GHSL-2020-367</code> in any communication regarding 