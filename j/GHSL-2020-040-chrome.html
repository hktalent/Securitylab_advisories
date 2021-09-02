<header class="post-header d-block mb-6">
      <div class="date text-mono f5 my-3">April 16, 2020</div>
      <h1 class="my-2 h00-mktg lh-condensed">GHSL-2020-040: Use After Free in Chrome WebAudio</h1>

      
      
      
      
      

      

      <a target="_blank" class="sc-frDJqD SgxRc d-inline-flex flex-row flex-items-center text-gray" href="https://github.com/m-y-mo">
        <img class="mr-3" src="https://avatars.githubusercontent.com/u/15773368?s=35" height="35" width="35">
        <span>Man Yue Mo</span>
      </a>
    </header>

    <main id="content" class="markdown-body" aria-label="Content">
      <h2 id="summary">Summary</h2>
<p>UaF in <code class="language-plaintext highlighter-rouge">DeferredTaskHandler::BreakConnections(2)</code></p>

<h2 id="product">Product</h2>
<p>Chrome</p>

<h2 id="cve">CVE</h2>
<p>CVE-2020-6449</p>

<h2 id="tested-version">Tested Version</h2>
<p>Chrome version: master branch build 79956ba, asan build 80.3987.132
Operating System: Ubuntu 18.04</p>

<h2 id="details">Details</h2>

<p>This issue has the same crash site as 1057593, but the root cause and the fix is different.</p>

<p>Similar to 1057593, when a suspend of the <code class="language-plaintext highlighter-rouge">BaseAudioContext</code> and a stop of an <code class="language-plaintext highlighter-rouge">AudioScheduleSourceNode</code> happens in the same quantum, the <code class="language-plaintext highlighter-rouge">AudioScheduleSourceNode</code> can be destroyed while the <code class="language-plaintext highlighter-rouge">BaseAudioContext</code> is suspended. At this point, <code class="language-plaintext highlighter-rouge">active_source_handlers_</code> in <code class="language-plaintext highlighter-rouge">DeferredTaskHandler</code>[1] is responsible for keeping the corresponding <code class="language-plaintext highlighter-rouge">AudioScheduleSourceHandler</code> alive before it is used in <code class="language-plaintext highlighter-rouge">DeferredTaskHandler::BreakConnections</code>[2].</p>

<p>The code in <code class="language-plaintext highlighter-rouge">DeferredTaskHandler::BreakConnections</code> implicitly assumed that <code class="language-plaintext highlighter-rouge">finished_source_handlers_</code> is a subset of <code class="language-plaintext highlighter-rouge">active_source_handlers_</code> and hence <code class="language-plaintext highlighter-rouge">active_source_handlers_</code> is keeping the raw pointers in <code class="language-plaintext highlighter-rouge">finished_source_handlers_</code> alive. (as can be seen from the <code class="language-plaintext highlighter-rouge">active_source_handlers_.erase</code>, which assumes <code class="language-plaintext highlighter-rouge">finished</code> is contained in <code class="language-plaintext highlighter-rouge">active_source_handlers_</code>)</p>

<p>This problem, however, is that <code class="language-plaintext highlighter-rouge">active_source_handlers_</code> can be cleared by the <code class="language-plaintext highlighter-rouge">DeferredTaskHandler::ClearHandlersToBeDeleted</code> method[3] while <code class="language-plaintext highlighter-rouge">finished_source_handlers_</code> does not get cleared at the same time, leaving dangling pointers in <code class="language-plaintext highlighter-rouge">finished_source_handlers_</code>, which will then cause UaF in <code class="language-plaintext highlighter-rouge">BreakConnections</code>.</p>

<div class="language-cpp highlighter-rouge"><div class="highlight"><pre class="highlight"><code>    <span class="k">for</span> <span class="p">(</span><span class="k">auto</span><span class="o">*</span> <span class="n">finished</span> <span class="o">:</span> <span class="n">finished_source_handlers_</span><span class="p">)</span> <span class="p">{</span>
      <span class="c1">// Break connection first and then remove from the list because that can</span>
      <span class="c1">// cause the handler to be deleted.</span>
      <span class="n">finished</span><span class="o">-&gt;</span><span class="n">BreakConnectionWithLock</span><span class="p">();</span>     <span class="c1">//&lt;-- `active_source_handlers_` may have been cleared, and finished is already freed</span>
      <span class="n">active_source_handlers_</span><span class="p">.</span><span class="n">erase</span><span class="p">(</span><span class="n">finished</span><span class="p">);</span> <span class="c1">//&lt;-- assumes `active_source_handlers_` contains finished</span>
    <span class="p">}</span>
</code></pre></div></div>

<p>By destroying the context to trigger <code class="language-plaintext highlighter-rouge">BaseAudioContext::Uninitialize</code>, which will then call <code class="language-plaintext highlighter-rouge">ClearHandlersToBeDeleted</code>, it is possible to clear <code class="language-plaintext highlighter-rouge">active_source_handlers_</code> and then trigger <code class="language-plaintext highlighter-rouge">DeferredTaskHandler::BreakConnections</code> to cause a UaF.</p>

<ol>
  <li>
    <p>https://source.chromium.org/chromium/chromium/src/+/bf433ad6dcfcaac460512bb45a53d5a2ea5356f9:third_party/blink/renderer/modules/webaudio/deferred_task_handler.h;drc=67e598a2ae32101acac19318c0c56830c12a303f;bpv=1;bpt=1;l=255?originalUrl=https:%2F%2Fcs.chromium.org%2F</p>
  </li>
  <li>
    <p>https://source.chromium.org/chromium/chromium/src/+/bf433ad6dcfcaac460512bb45a53d5a2ea5356f9:third_party/blink/renderer/modules/webaudio/deferred_task_handler.cc;l=83;drc=67e598a2ae32101acac19318c0c56830c12a303f;bpv=1;bpt=1?originalUrl=https:%2F%2Fcs.chromium.org%2F</p>
  </li>
  <li>
    <p>https://source.chromium.org/chromium/chromium/src/+/bf433ad6dcfcaac460512bb45a53d5a2ea5356f9:third_party/blink/renderer/modules/webaudio/deferred_task_handler.cc;l=361;drc=67e598a2ae32101acac19318c0c56830c12a303f;bpv=1;bpt=1?originalUrl=https:%2F%2Fcs.chromium.org%2F</p>
  </li>
</ol>

<h3 id="impact">Impact</h3>

<p>Use-after-free in renderer.</p>

<h2 id="coordinated-disclosure-timeline">Coordinated Disclosure Timeline</h2>
<ul>
  <li>09/03/2020 Reported as <a href="https://bugs.chromium.org/p/chromium/issues/detail?id=1059686">Chromium Issue 1059686</a></li>
  <li>18/03/2020 <a href="https://chromereleases.googleblog.com/2020/03/stable-channel-update-for-desktop_18.html">Fixed in version 80.0.3987.149</a></li>
</ul>

<h2 id="credit">Credit</h2>

<p>This issue was discovered and reported by GHSL team member <a href="https://github.com/m-y-mo">@m-y-mo (Man Yue Mo)</a>.</p>

<h2 id="contact">Contact</h2>

<p>You can contact the GHSL team at <code class="language-plaintext highlighter-rouge">securitylab@github.com</code>, please include the <code class="language-plaintext highlighter-rouge">GHSL-2020-040</code> in any communication regarding this issue.</p>

    