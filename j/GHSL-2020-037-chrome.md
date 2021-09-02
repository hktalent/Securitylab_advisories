<header class="post-header d-block mb-6">
      <div class="date text-mono f5 my-3">April 16, 2020</div>
      <h1 class="my-2 h00-mktg lh-condensed">GHSL-2020-037: Use after free in Chrome WebAudio</h1>

      
      
      
      
      

      

      <a target="_blank" class="sc-frDJqD SgxRc d-inline-flex flex-row flex-items-center text-gray" href="https://github.com/m-y-mo">
        <img class="mr-3" src="https://avatars.githubusercontent.com/u/15773368?s=35" height="35" width="35">
        <span>Man Yue Mo</span>
      </a>
    </header>

    <main id="content" class="markdown-body" aria-label="Content">
      <h2 id="summary">Summary</h2>

<p>UaF in <code class="language-plaintext highlighter-rouge">DeferredTaskHandler::BreakConnections</code></p>

<h2 id="product">Product</h2>
<p>Chrome</p>

<h2 id="cve">CVE</h2>
<p>CVE-2020-6428</p>

<h2 id="tested-version">Tested Version</h2>
<p>Chromium version: master branch build e577636
Also tested on release google Chrome 80.3987.122
Operating System: linux 18.04</p>

<h2 id="details">Details</h2>

<p>When <code class="language-plaintext highlighter-rouge">HandlePreRenderTask</code> is called during the rendering, it will check whether any source node should be stopped[1]. If an <code class="language-plaintext highlighter-rouge">AudioScheduleSourceNode</code>, (e.g. <code class="language-plaintext highlighter-rouge">ConstantSourceNode</code>) is to be stopped at or before the frame [2], it will then call the <code class="language-plaintext highlighter-rouge">AudioScheduledSourceHandler::Finish()</code> method, which calls <code class="language-plaintext highlighter-rouge">FinishWithoutOnEnded</code>. This has 2 effects:</p>

<ol>
  <li>
    <table>
      <tbody>
        <tr>
          <td>It calls <code class="language-plaintext highlighter-rouge">BaseAudioContext::NotifySourceNodeFinishedProcessing</code>[3], which will add the <code class="language-plaintext highlighter-rouge">AudioScheduledSourceHandler</code> in the</td>
          <td><code class="language-plaintext highlighter-rouge">finished_source_handlers_</code></td>
          <td>vector, as raw pointer.</td>
        </tr>
      </tbody>
    </table>
  </li>
</ol>

<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="kt">void</span> <span class="n">BaseAudioContext</span><span class="o">::</span><span class="n">NotifySourceNodeFinishedProcessing</span><span class="p">(</span>
    <span class="n">AudioHandler</span><span class="o">*</span> <span class="n">handler</span><span class="p">)</span> <span class="p">{</span>
  <span class="n">DCHECK</span><span class="p">(</span><span class="n">IsAudioThread</span><span class="p">());</span>

  <span class="n">GetDeferredTaskHandler</span><span class="p">().</span><span class="n">GetFinishedSourceHandlers</span><span class="p">()</span><span class="o">-&gt;</span><span class="n">push_back</span><span class="p">(</span><span class="n">handler</span><span class="p">);</span>
<span class="p">}</span>
</code></pre></div></div>

<ol>
  <li>It sets the playback state of the <code class="language-plaintext highlighter-rouge">AudioScheduledSourceHandler</code> to <code class="language-plaintext highlighter-rouge">FINISHED_STATE</code>, allowing the <code class="language-plaintext highlighter-rouge">AudioScheduledSourceNode</code> to be deleted[4].</li>
</ol>

<table>
  <tbody>
    <tr>
      <td>If a suspend is also scheduled at the same frame, we can then return to main thread and delete the <code class="language-plaintext highlighter-rouge">AudioScheduleSourceNode</code>. This is ok as the <code class="language-plaintext highlighter-rouge">AudioScheduleSourceHandler</code> is also being kept alive in</td>
      <td><code class="language-plaintext highlighter-rouge">active_source_handlers_</code></td>
      <td>when the start method of the source node is called[5], which is held in the <code class="language-plaintext highlighter-rouge">BaseAudioContext</code>.</td>
    </tr>
  </tbody>
</table>

<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="kt">void</span> <span class="n">BaseAudioContext</span><span class="o">::</span><span class="n">NotifySourceNodeStartedProcessing</span><span class="p">(</span><span class="n">AudioNode</span><span class="o">*</span> <span class="n">node</span><span class="p">)</span> <span class="p">{</span>
  <span class="n">DCHECK</span><span class="p">(</span><span class="n">IsMainThread</span><span class="p">());</span>
  <span class="n">GraphAutoLocker</span> <span class="n">locker</span><span class="p">(</span><span class="n">this</span><span class="p">);</span>

  <span class="n">GetDeferredTaskHandler</span><span class="p">().</span><span class="n">GetActiveSourceHandlers</span><span class="p">()</span><span class="o">-&gt;</span><span class="n">insert</span><span class="p">(</span><span class="o">&amp;</span><span class="n">node</span><span class="o">-&gt;</span><span class="n">Handler</span><span class="p">());</span>
  <span class="n">node</span><span class="o">-&gt;</span><span class="n">Handler</span><span class="p">().</span><span class="n">MakeConnection</span><span class="p">();</span>
<span class="p">}</span>
</code></pre></div></div>

<p>When the <code class="language-plaintext highlighter-rouge">BaseAudioContext</code> is resumed, it will call the <code class="language-plaintext highlighter-rouge">DeferredTaskHandler::BreakConnection</code> method in the <code class="language-plaintext highlighter-rouge">HandlePostRenderTasks</code> method[6] to finish off with the <code class="language-plaintext highlighter-rouge">AudioScheduleSourceNode</code>:</p>

<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="kt">void</span> <span class="n">DeferredTaskHandler</span><span class="o">::</span><span class="n">BreakConnections</span><span class="p">()</span> <span class="p">{</span>
  <span class="p">...</span>
  <span class="n">wtf_size_t</span> <span class="n">size</span> <span class="o">=</span> <span class="n">finished_source_handlers_</span><span class="p">.</span><span class="n">size</span><span class="p">();</span>
  <span class="k">if</span> <span class="p">(</span><span class="n">size</span> <span class="o">&gt;</span> <span class="mi">0</span><span class="p">)</span> <span class="p">{</span>
    <span class="k">for</span> <span class="p">(</span><span class="k">auto</span><span class="o">*</span> <span class="n">finished</span> <span class="o">:</span> <span class="n">finished_source_handlers_</span><span class="p">)</span> <span class="p">{</span>
      <span class="n">active_source_handlers_</span><span class="p">.</span><span class="n">erase</span><span class="p">(</span><span class="n">finished</span><span class="p">);</span>          <span class="c1">//&lt;-- finished is now free'd</span>
      <span class="n">finished</span><span class="o">-&gt;</span><span class="n">BreakConnectionWithLock</span><span class="p">();</span>              <span class="c1">//&lt;-- UaF</span>
    <span class="p">}</span>
    <span class="n">finished_source_handlers_</span><span class="p">.</span><span class="n">clear</span><span class="p">();</span>
  <span class="p">}</span>
<span class="p">}</span>
</code></pre></div></div>

<table>
  <tbody>
    <tr>
      <td>The problem, however, is that <code class="language-plaintext highlighter-rouge">BreakConnections</code> first erase the handler before using it in the next line. As the handler is now only kept alive by</td>
      <td><code class="language-plaintext highlighter-rouge">active_source_handlers_</code></td>
      <td>, this deletes the handler and causes UaF.</td>
    </tr>
  </tbody>
</table>

<ol>
  <li>
    <p>https://source.chromium.org/chromium/chromium/src/+/71825939c432c440fa53ef4016372076e2c6114a:third_party/blink/renderer/modules/webaudio/offline_audio_context.cc;l=413;drc=b892cf58e162a8f66cd76d7472f129fe0fb6a7d1;bpv=1;bpt=1?originalUrl=https:%2F%2Fcs.chromium.org%2F</p>
  </li>
  <li>
    <p>https://source.chromium.org/chromium/chromium/src/+/71825939c432c440fa53ef4016372076e2c6114a:third_party/blink/renderer/modules/webaudio/constant_source_node.cc;l=117;bpv=1;bpt=1?originalUrl=https:%2F%2Fcs.chromium.org%2F</p>
  </li>
  <li>
    <p>https://source.chromium.org/chromium/chromium/src/+/71825939c432c440fa53ef4016372076e2c6114a:third_party/blink/renderer/modules/webaudio/audio_scheduled_source_node.cc;l=242;bpv=1;bpt=1?originalUrl=https:%2F%2Fcs.chromium.org%2F</p>
  </li>
  <li>
    <p>https://source.chromium.org/chromium/chromium/src/+/71825939c432c440fa53ef4016372076e2c6114a:third_party/blink/renderer/modules/webaudio/audio_scheduled_source_node.cc;l=243;bpv=1;bpt=1?originalUrl=https:%2F%2Fcs.chromium.org%2F</p>
  </li>
  <li>
    <p>https://source.chromium.org/chromium/chromium/src/+/71825939c432c440fa53ef4016372076e2c6114a:third_party/blink/renderer/modules/webaudio/audio_scheduled_source_node.cc;l=199;drc=b892cf58e162a8f66cd76d7472f129fe0fb6a7d1;bpv=1;bpt=1?originalUrl=https:%2F%2Fcs.chromium.org%2F</p>
  </li>
  <li>
    <p>https://source.chromium.org/chromium/chromium/src/+/71825939c432c440fa53ef4016372076e2c6114a:third_party/blink/renderer/modules/webaudio/offline_audio_context.cc;l=426;drc=b892cf58e162a8f66cd76d7472f129fe0fb6a7d1;bpv=1;bpt=1?originalUrl=https:%2F%2Fcs.chromium.org%2F</p>
  </li>
</ol>

<h3 id="impact">Impact</h3>

<p>Use-after-free in renderer.</p>

<h2 id="coordinated-disclosure-timeline">Coordinated Disclosure Timeline</h2>
<ul>
  <li>02/03/2020 Reported as <a href="https://bugs.chromium.org/p/chromium/issues/detail?id=1057593">Chromium Issue 1057593</a></li>
  <li>18/03/2020 <a href="https://chromereleases.googleblog.com/2020/03/stable-channel-update-for-desktop_18.html">Fixed in version 80.0.3987.149</a></li>
</ul>

<h2 id="credit">Credit</h2>

<p>This issue was discovered and reported by GHSL team member <a href="https://github.com/m-y-mo">@m-y-mo (Man Yue Mo)</a>.</p>

<h2 id="contact">Contact</h2>

<p>You can contact the GHSL team at <code class="language-plaintext highlighter-rouge">securitylab@github.com</code>, please include the <code class="language-plaintext highlighter-rouge">GHSL-2020-037</code> in any communication regarding this issue.</p>

    