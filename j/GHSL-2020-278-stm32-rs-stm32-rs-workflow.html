<header class="post-header d-block mb-6">
      <div class="date text-mono f5 my-3">December 16, 2020</div>
      <h1 class="my-2 h00-mktg lh-condensed">GHSL-2020-278: Unauthorized repository modification or secrets exfiltration in the GitHub workflow of stm32-rs/stm32-rs</h1>

      
      
      
      
      

      

      <a target="_blank" class="sc-frDJqD SgxRc d-inline-flex flex-row flex-items-center text-gray" href="https://github.com/jarlob">
        <img class="mr-3" src="https://avatars.githubusercontent.com/u/26652396?s=35" height="35" width="35">
        <span>Jaroslav Lobacevski</span>
      </a>
    </header>

    <main id="content" class="markdown-body" aria-label="Content">
      <h2 id="summary">Summary</h2>

<p>The <a href="https://github.com/stm32-rs/stm32-rs/blob/master/.github/workflows/mmaps_pr.yaml">mmaps_pr.yaml</a> GitHub workflow is vulnerable to unauthorized modification of the base repository or secrets exfiltration from a Pull Request.</p>

<h2 id="product">Product</h2>

<p><a href="https://github.com/stm32-rs/stm32-rs">stm32-rs/stm32-rs</a> GitHub repository</p>

<h2 id="tested-version">Tested Version</h2>

<p>The latest changeset <a href="https://github.com/stm32-rs/stm32-rs/blob/d04725f9a8f738fdcb550b57411288fa4aaa87f2/.github/workflows/mmaps_pr.yaml">d04725f</a> to the date.</p>

<h2 id="details">Details</h2>

<h3 id="issue-untrusted-code-is-explicitly-checked-out-and-run-on-a-pull-request-from-a-fork">Issue: Untrusted code is explicitly checked out and run on a Pull Request from a fork</h3>

<p><code class="language-plaintext highlighter-rouge">pull_request_target</code> was introduced to allow triggered workflows to comment on PRs, label them, assign people, etc.. In order to make it possible the triggered action runner has read/write token for the base repository and the access to secrets. In order to prevent untrusted code from execution it runs in a context of the base repository.</p>

<p>By explicitly checking out and running build script from a fork the untrusted code is running in an environment that is able to push to the base repository and to access secrets.</p>

<div class="language-yaml highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="na">on</span><span class="pi">:</span>
  <span class="na">pull_request_target</span><span class="pi">:</span>
<span class="nn">...</span>
      <span class="pi">-</span> <span class="na">name</span><span class="pi">:</span> <span class="s">Checkout master</span>
        <span class="na">uses</span><span class="pi">:</span> <span class="s">actions/checkout@v2</span>
        <span class="na">with</span><span class="pi">:</span>
          <span class="na">path</span><span class="pi">:</span> <span class="s">master</span>
      <span class="pi">-</span> <span class="na">name</span><span class="pi">:</span> <span class="s">Checkout pull request</span>
        <span class="na">uses</span><span class="pi">:</span> <span class="s">actions/checkout@v2</span>
        <span class="na">with</span><span class="pi">:</span>
          <span class="na">ref</span><span class="pi">:</span> <span class="s">refs/pull/${{ github.event.number }}/head</span>
          <span class="na">path</span><span class="pi">:</span> <span class="s">stm32-rs</span>
<span class="nn">...</span>
      <span class="pi">-</span> <span class="na">name</span><span class="pi">:</span> <span class="s">Build and publish</span>
        <span class="na">run</span><span class="pi">:</span> <span class="pi">|</span>
          <span class="s">cd stm32-rs</span>
          <span class="s">COMMIT=$(git rev-parse --short HEAD)</span>
          <span class="s">BRANCH=pr-${{ github.event.number }}-$COMMIT</span>
          <span class="s">echo "BRANCH=$BRANCH" &gt;&gt; $GITHUB_ENV</span>
          <span class="s">cp ../master/Makefile .</span>
          <span class="s">make -j2 mmaps</span>
<span class="s">...</span>
</code></pre></div></div>

<p>The build script overwrites the makefile with a file from the base repository. However it still calls other scripts from the PR, for example the <code class="language-plaintext highlighter-rouge">extract.sh</code>:</p>

<pre><code class="language-Makefile">...
# Each yaml file also corresponds to a mmap in mmaps/
MMAPS := $(patsubst devices/%.yaml, mmaps/%.mmap, $(YAMLS))
...
# Turn a devices/device.yaml and svd/device.svd into svd/device.svd.patched
svd/%.svd.patched: devices/%.yaml svd/%.svd .deps/%.d
  svd patch $&lt;
...
# Generate mmap from patched SVD
mmaps/%.mmap: svd/%.svd.patched
  @mkdir -p mmaps
  svd mmap $&lt; &gt; $@
...
svd/%.svd: svd/.extracted ;

svd/.extracted:
  cd svd &amp;&amp; ./extract.sh &amp;&amp; touch .extracted
...
mmaps: $(MMAPS)
</code></pre>

<h4 id="impact">Impact</h4>

<p>The vulnerability allows for unauthorized modification of the base repository and secrets exfiltration.</p>

<h2 id="coordinated-disclosure-timeline">Coordinated Disclosure Timeline</h2>

<ul>
  <li>2020-11-30: Report sent to maintainers</li>
  <li>2020-11-30: Maintainers acknowledged</li>
  <li>2020-11-30: Issue resolved</li>
</ul>

<h2 id="credit">Credit</h2>

<p>This issue was discovered and reported by GHSL team member <a href="https://github.com/JarLob">@JarLob (Jaroslav Lobačevski)</a>.</p>

<h2 id="contact">Contact</h2>

<p>You can contact the GHSL team at <code class="language-plaintext highlighter-rouge">securitylab@github.com</code>, please include a reference to <code class="language-plaintext highlighter-rouge">GHSL-2020-278</code> in any communication regarding this issue.</p>

   