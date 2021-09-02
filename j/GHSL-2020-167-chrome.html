<header class="post-header d-block mb-6">
      <div class="date text-mono f5 my-3">March 8, 2021</div>
      <h1 class="my-2 h00-mktg lh-condensed">GHSL-2020-167: Use-after-free (UaF) in Chrome AudioHandler - CVE-2020-15972, CVE-2021-21114</h1>

      
      
      
      
      

      

      <a target="_blank" class="sc-frDJqD SgxRc d-inline-flex flex-row flex-items-center text-gray" href="https://github.com/m-y-mo">
        <img class="mr-3" src="https://avatars.githubusercontent.com/u/15773368?s=35" height="35" width="35">
        <span>Man Yue Mo</span>
      </a>
    </header>

    <main id="content" class="markdown-body" aria-label="Content">
      <h2 id="coordinated-disclosure-timeline">Coordinated Disclosure Timeline</h2>
<ul>
  <li>07/09/2020 Reported as <a href="https://bugs.chromium.org/p/chromium/issues/detail?id=1125635">Chromium Issue 1125635</a></li>
  <li>07/09/2020 Was told that it was a duplicate of issue 1115901.</li>
  <li>11/09/2020 Developers deduplicated due to differences with 1115901.</li>
  <li>29/09/2020 Was told it was a duplicate afterall.</li>
  <li>14/10/2020 Issue fixed in release <a href="https://chromereleases.googleblog.com/2020/10/stable-channel-update-for-desktop.html">86.0.4240.75</a> as CVE-2020-15972 by an anonymous researcher.</li>
  <li>03/11/2020 Fix of issue causes deadlock in some circumstances and patch was reverted as developers could no longer reproduced the issue.</li>
  <li>16/11/2020 Tested that the issue still reproduced after the patch reverted and informed Chromium security via the original ticket.</li>
  <li>17/11/2020 Helped developers to reproduce the issue and a new ticket opened as <a href="https://bugs.chromium.org/p/chromium/issues/detail?id=1150065">1150065</a>.</li>
  <li>Issue fixed again in release of <a href="https://chromereleases.googleblog.com/2021/01/stable-channel-update-for-desktop.html">87.0.4280.141</a> as CVE-2021-21114.</li>
</ul>

<h2 id="summary">Summary</h2>
<p>UaF in AudioHandler::ProcessIfNecessary</p>

<h2 id="product">Product</h2>
<p>Chrome</p>

<h2 id="tested-version">Tested Version</h2>
<ul>
  <li>Chrome version: master branch build 9dfba38, stable build 85.0.4183.83</li>
  <li>Operating System: Ubuntu 18.04</li>
</ul>

<h2 id="details">Details</h2>

<p>The tear down mutex removed in this commit [1] does not only protect against UaF issues with the BaseAudioContext (which is what the self-referencing patch fixed), but also race conditions where <code class="language-plaintext highlighter-rouge">AudioHandlers</code> may still be processing while the <code class="language-plaintext highlighter-rouge">ClearHandlersToBeDeleted</code> method is removing the <code class="language-plaintext highlighter-rouge">rendering_orphan_handlers_</code>. As various processing methods of the <code class="language-plaintext highlighter-rouge">AudioHandler</code> (e.g. <code class="language-plaintext highlighter-rouge">Process</code>, <code class="language-plaintext highlighter-rouge">ProcessIfNeccessary</code>) are not protected by any lock, it can race with <code class="language-plaintext highlighter-rouge">ClearHandlersToBeDeleted</code> (protected by GraphLock) and the <code class="language-plaintext highlighter-rouge">AudioHandler</code> can be deleted while <code class="language-plaintext highlighter-rouge">ClearHandlersToBeDeleted</code> clears it away. This causes UaF.</p>

<ol>
  <li>https://source.chromium.org/chromium/chromium/src/+/e4c27b508976fb751ccd4d34e52b70b668618271?originalUrl=https%2F:%2F%2F%2Fcs.chromium.org%2F</li>
</ol>

<h2 id="cve">CVE</h2>
<ul>
  <li>CVE-2020-15972 (credited to anonymous researcher)</li>
  <li>CVE-2021-21114 (regression credited to us)</li>
</ul>

<h4 id="impact">Impact</h4>

<p>Use-after-free in the sandboxed renderer process that can be triggered by visiting a malicious website.</p>

<h2 id="credit">Credit</h2>

<p>This issue was discovered and reported by GHSL team member <a href="https://github.com/m-y-mo">@m-y-mo (Man Yue Mo)</a>.</p>

<h2 id="contact">Contact</h2>

<p>You can contact the GHSL team at <code class="language-plaintext highlighter-rouge">securitylab@github.com</code>, please include the <code class="language-plaintext highlighter-rouge">GHSL-2020-167</code> in any communication regarding this issue.</p>

    