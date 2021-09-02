<header class="post-header d-block mb-6">
      <div class="date text-mono f5 my-3">February 3, 2021</div>
      <h1 class="my-2 h00-mktg lh-condensed">GHSL-2020-334: Arbitrary code execution in gsantner workflows</h1>

      
      
      
      
      

      

      <a target="_blank" class="sc-frDJqD SgxRc d-inline-flex flex-row flex-items-center text-gray" href="https://github.com/jarlob">
        <img class="mr-3" src="https://avatars.githubusercontent.com/u/26652396?s=35" height="35" width="35">
        <span>Jaroslav Lobacevski</span>
      </a>
    </header>

    <main id="content" class="markdown-body" aria-label="Content">
      <h2 id="coordinated-disclosure-timeline">Coordinated Disclosure Timeline</h2>

<ul>
  <li>2020-12-11: Report sent to maintainers.</li>
  <li>2020-12-22: Maintainers acknowledged.</li>
  <li>2020-12-22: Issue resolved.</li>
</ul>

<h2 id="summary">Summary</h2>

<p>The <a href="https://github.com/gsantner/markor/blob/6cc10bcc94a5d514c4ab084dc278103cec472403/.github/workflows/build-android-project.yml">markor/build-android-project.yml</a>, <a href="https://github.com/gsantner/memetastic/blob/3c270f30bb7fe973580d188aa8fd2562a06b3006/.github/workflows/build-android-project.yml">memetastic/build-android-project.yml</a> and <a href="https://github.com/gsantner/dandelion/blob/ff62aa5a07b69ac6cf69cbfb85610a57b1f8dd01/.github/workflows/build-android-project.yml">dandelion/link-validator.yml</a> GitHub workflows are vulnerable to unauthorized modification of the base repository or secrets exfiltration from a Pull Request.</p>

<h2 id="product">Product</h2>

<p><a href="https://github.com/gsantner/markor">gsantner/markor</a>, <a href="https://github.com/gsantner/memetastic">gsantner/memetastic</a> and <a href="https://github.com/gsantner/dandelion">gsantner/dandelion</a> GitHub repositories.</p>

<h2 id="tested-version">Tested Version</h2>

<p>The latest changesets <a href="https://github.com/gsantner/markor/blob/6cc10bcc94a5d514c4ab084dc278103cec472403/.github/workflows/build-android-project.yml">6cc10bc</a>, <a href="https://github.com/gsantner/memetastic/blob/3c270f30bb7fe973580d188aa8fd2562a06b3006/.github/workflows/build-android-project.yml">3c270f3</a> and <a href="https://github.com/gsantner/dandelion/blob/ff62aa5a07b69ac6cf69cbfb85610a57b1f8dd01/.github/workflows/build-android-project.yml">ff62aa5</a> to the date.</p>

<h2 id="details">Details</h2>

<h3 id="issue-untrusted-code-is-explicitly-checked-out-and-run-on-a-pull-request-from-a-fork">Issue: Untrusted code is explicitly checked out and run on a Pull Request from a fork</h3>

<p><code class="language-plaintext highlighter-rouge">pull_request_target</code> was introduced to allow triggered workflows to comment on PRs, label them, assign people, etc.. In order to make it possible the triggered action runner has read/write token for the base repository and the access to secrets. In order to prevent untrusted code from execution it runs in a context of the base repository.</p>

<p>By explicitly checking out and running build script from a fork the untrusted code is running in an environment that is able to push to the base repository and to access secrets.</p>

<div class="language-yaml highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="na">on</span><span class="pi">:</span> <span class="pi">[</span><span class="nv">push</span><span class="pi">,</span> <span class="nv">pull_request_target</span><span class="pi">]</span>

<span class="na">jobs</span><span class="pi">:</span>
  <span class="na">build</span><span class="pi">:</span>
    <span class="na">if</span><span class="pi">:</span> <span class="s2">"</span><span class="s">!contains(github.event.head_commit.message,</span><span class="nv"> </span><span class="s">'ci</span><span class="nv"> </span><span class="s">skip')</span><span class="nv"> </span><span class="s">&amp;&amp;</span><span class="nv"> </span><span class="s">(!contains(github.event_name,</span><span class="nv"> </span><span class="s">'pull_request')</span><span class="nv"> </span><span class="s">||</span><span class="nv"> </span><span class="s">(contains(github.event_name,</span><span class="nv"> </span><span class="s">'pull_request')</span><span class="nv"> </span><span class="s">&amp;&amp;</span><span class="nv"> </span><span class="s">github.event.pull_request.head.repo.full_name</span><span class="nv"> </span><span class="s">!=</span><span class="nv"> </span><span class="s">github.repository))"</span>
<span class="nn">...</span>
    <span class="pi">-</span> <span class="na">name</span><span class="pi">:</span> <span class="s2">"</span><span class="s">Checkout:</span><span class="nv"> </span><span class="s">Code</span><span class="nv"> </span><span class="s">(PR)"</span>
      <span class="na">uses</span><span class="pi">:</span> <span class="s">actions/checkout@v2</span>
      <span class="na">if</span><span class="pi">:</span> <span class="s2">"</span><span class="s">contains(github.event_name,</span><span class="nv"> </span><span class="s">'pull_request')"</span>
      <span class="na">with</span><span class="pi">:</span>
        <span class="na">ref</span><span class="pi">:</span> <span class="s">${{github.event.pull_request.head.ref}}</span>
        <span class="na">repository</span><span class="pi">:</span> <span class="s">${{github.event.pull_request.head.repo.full_name}}</span>
<span class="nn">...</span>
    <span class="pi">-</span> <span class="na">name</span><span class="pi">:</span> <span class="s2">"</span><span class="s">Build:</span><span class="nv"> </span><span class="s">Project</span><span class="nv"> </span><span class="s">with</span><span class="nv"> </span><span class="s">make"</span>
      <span class="na">run</span><span class="pi">:</span> <span class="s">make clean all</span>
<span class="nn">...</span>
</code></pre></div></div>

<h4 id="impact">Impact</h4>

<p>The vulnerability allows for unauthorized modification of the base repository and secrets exfiltration.</p>

<h2 id="credit">Credit</h2>

<p>This issue was discovered and reported by GHSL team member <a href="https://github.com/JarLob">@JarLob (Jaroslav Lobačevski)</a>.</p>

<h2 id="contact">Contact</h2>

<p>You can contact the GHSL team at <code class="language-plaintext highlighter-rouge">securitylab@github.com</code>, please include a reference to <code class="language-plaintext highlighter-rouge">GHSL-2020-334</code> in any communication regarding this issue.</p>

   