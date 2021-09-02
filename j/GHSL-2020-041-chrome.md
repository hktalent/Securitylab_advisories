<header class="post-header d-block mb-6">
      <div class="date text-mono f5 my-3">April 16, 2020</div>
      <h1 class="my-2 h00-mktg lh-condensed">GHSL-2020-041: Use After Free in Chrome WebAudio</h1>

      
      
      
      
      

      

      <a target="_blank" class="sc-frDJqD SgxRc d-inline-flex flex-row flex-items-center text-gray" href="https://github.com/m-y-mo">
        <img class="mr-3" src="https://avatars.githubusercontent.com/u/15773368?s=35" height="35" width="35">
        <span>Man Yue Mo</span>
      </a>
    </header>

    <main id="content" class="markdown-body" aria-label="Content">
      <h2 id="summary">Summary</h2>
<p>UaF in <code class="language-plaintext highlighter-rouge">DeferredTaskHandler::ProcessAutomaticPullNodes</code></p>

<h2 id="product">Product</h2>
<p>Chrome</p>

<h2 id="cve">CVE</h2>
<p>CVE-2020-6451</p>

<h2 id="tested-version">Tested Version</h2>
<p>Chrome version: master branch build 79956ba, asan build 80.3987.132
Operating System: Ubuntu 18.04</p>

<h2 id="details">Details</h2>

<p>This vulnerability can be triggered on both the master branch and on 80.0.3987.132, however, the removal of the <a href="https://chromium.googlesource.com/chromium/src.git/+/e4c27b508976fb751ccd4d34e52b70b668618271"><code class="language-plaintext highlighter-rouge">tear_down_mutex_</code></a> affects the way it is triggered. The issue itself is not so much to do with the <code class="language-plaintext highlighter-rouge">tear_down_mutex_</code>, but rather a race condition between accesses to the <code class="language-plaintext highlighter-rouge">rendering_automatic_pull_handlers_</code> of <code class="language-plaintext highlighter-rouge">DeferredTaskHandler</code>.</p>

<p>The root cause of the problem is that, in the <code class="language-plaintext highlighter-rouge">DeferredTaskHandler::ProcessAutomaticPullNodes</code> method, <code class="language-plaintext highlighter-rouge">rendering_automatic_pull_handlers_</code> is accessed without an appropriate lock[1]. This method is called in <code class="language-plaintext highlighter-rouge">OfflineAudioDestinationHandler::RenderIfNotSuspended</code> and the behaviour differs between the master branch and 80.0.3987.132.</p>

<p>On the master branch, because <code class="language-plaintext highlighter-rouge">tear_down_mutex_</code> is removed, this call is not protected by any lock at all[2] and it is running on the audio thread. As <code class="language-plaintext highlighter-rouge">rendering_automatic_pull_handlers_</code> gets cleared in <code class="language-plaintext highlighter-rouge">ClearHandlersToBeDeleted</code>[3], which is running on the main thread, this can cause UaF if <code class="language-plaintext highlighter-rouge">ClearHandlersToBeDeleted</code> clears the AudioHandler in <code class="language-plaintext highlighter-rouge">rendering_automatic_pull_handlers_</code> while <code class="language-plaintext highlighter-rouge">ProcessAutomaticPullNodes</code> is being accessed.</p>

<p>On 80.0.3987.132, <code class="language-plaintext highlighter-rouge">ProcessAutomaticPullNodes</code> is called within the scope of <code class="language-plaintext highlighter-rouge">tear_down_mutex_</code>[4]:</p>

<div class="language-cpp highlighter-rouge"><div class="highlight"><pre class="highlight"><code>  <span class="p">{</span>
    <span class="n">MutexTryLocker</span> <span class="n">try_locker</span><span class="p">(</span><span class="n">Context</span><span class="p">()</span><span class="o">-&gt;</span><span class="n">GetTearDownMutex</span><span class="p">());</span>
    <span class="k">if</span> <span class="p">(</span><span class="n">try_locker</span><span class="p">.</span><span class="n">Locked</span><span class="p">())</span> <span class="p">{</span>
      <span class="p">...</span>
    <span class="p">}</span>
    <span class="p">...</span>
    <span class="n">Context</span><span class="p">()</span><span class="o">-&gt;</span><span class="n">GetDeferredTaskHandler</span><span class="p">().</span><span class="n">ProcessAutomaticPullNodes</span><span class="p">(</span>
        <span class="n">number_of_frames</span><span class="p">);</span>
  <span class="p">}</span>
</code></pre></div></div>

<p>However, the function is called even if <code class="language-plaintext highlighter-rouge">try_locker.Locked</code> failed. This means that if <code class="language-plaintext highlighter-rouge">BaseAudioContext::Uninitialize</code> had already obtained the <code class="language-plaintext highlighter-rouge">tear_down_mutex_</code> at this point[5], <code class="language-plaintext highlighter-rouge">ProcessAutomaticPullNodes</code> will still be called without any protection from the <code class="language-plaintext highlighter-rouge">tear_down_mutex_</code>. This again can lead to a race condition where <code class="language-plaintext highlighter-rouge">ClearHandlersToBeDeleted</code> destroys the handler while <code class="language-plaintext highlighter-rouge">ProcessAutomaticPullNodes</code> is accessing it and causes UaF.</p>

<h3 id="impact">Impact</h3>

<p>Use-after-free in renderer.</p>

<h2 id="coordinated-disclosure-timeline">Coordinated Disclosure Timeline</h2>
<ul>
  <li>12/03/2020 Reported as <a href="https://bugs.chromium.org/p/chromium/issues/detail?id=1061018">Chromium Issue 1061018</a></li>
  <li>31/03/2020 <a href="https://chromereleases.googleblog.com/2020/03/stable-channel-update-for-desktop_31.html">Fixed in 80.0.3987.162</a></li>
</ul>

<h2 id="credit">Credit</h2>

<p>This issue was discovered and reported by GHSL team member <a href="https://github.com/m-y-mo">@m-y-mo (Man Yue Mo)</a>.</p>

<h2 id="contact">Contact</h2>

<p>You can contact the GHSL team at <code class="language-plaintext highlighter-rouge">securitylab@github.com</code>, please include the <code class="language-plaintext highlighter-rouge">GHSL-2020-041</code> in any communication regarding this issue.</p>

    