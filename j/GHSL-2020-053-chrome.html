<header class="post-header d-block mb-6">
      <div class="date text-mono f5 my-3">April 16, 2020</div>
      <h1 class="my-2 h00-mktg lh-condensed">GHSL-2020-053: Use After Free in Chrome WebAudio</h1>

      
      
      
      
      

      

      <a target="_blank" class="sc-frDJqD SgxRc d-inline-flex flex-row flex-items-center text-gray" href="https://github.com/m-y-mo">
        <img class="mr-3" src="https://avatars.githubusercontent.com/u/15773368?s=35" height="35" width="35">
        <span>Man Yue Mo</span>
      </a>
    </header>

    <main id="content" class="markdown-body" aria-label="Content">
      <h2 id="summary">Summary</h2>
<p>Incomplete fix of the vulnerabilities reported in <a href="GHSL-2020-035-chrome">GHSL-2020-035</a> and <a href="GHSL-2020-038-chrome">GHSL-2020-038</a></p>

<h2 id="product">Product</h2>
<p>Chrome</p>

<h2 id="cve">CVE</h2>
<p>CVE-2020-6450</p>

<h2 id="tested-version">Tested Version</h2>
<p>Chrome version: master branch build 3bdff94, asan build 80.3987.132
Operating System: Ubuntu 18.04</p>

<h2 id="details">Details</h2>

<p>The fix suggested for <a href="GHSL-2020-035-chrome">GHSL-2020-035</a> and <a href="GHSL-2020-038-chrome">GHSL-2020-038</a> did not fix the problem completely and it is still possible to trigger UaP in those cases, although the fix did prevent UaF.</p>

<p>The fix in those issues prevents UaF of <code class="language-plaintext highlighter-rouge">BaseAudioContext</code> by making the <code class="language-plaintext highlighter-rouge">AudioHandlers</code> in the relevant callbacks (<code class="language-plaintext highlighter-rouge">AudioScheduledSourceHandler::NotifyEnded</code> and <code class="language-plaintext highlighter-rouge">IIRFilterHandler::NotifyBadState</code>) weak pointers. Take <code class="language-plaintext highlighter-rouge">IIRFilterHandler::NotifyBadState</code> for example:</p>

<div class="language-cpp highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="err">@@</span> <span class="o">-</span><span class="mi">105</span><span class="p">,</span><span class="mi">9</span> <span class="o">+</span><span class="mi">105</span><span class="p">,</span><span class="mi">9</span> <span class="err">@@</span>
     <span class="k">if</span> <span class="p">(</span><span class="n">HasNonFiniteOutput</span><span class="p">())</span> <span class="p">{</span>
       <span class="n">did_warn_bad_filter_state_</span> <span class="o">=</span> <span class="nb">true</span><span class="p">;</span>
 
<span class="o">-</span>      <span class="n">PostCrossThreadTask</span><span class="p">(</span><span class="o">*</span><span class="n">task_runner_</span><span class="p">,</span> <span class="n">FROM_HERE</span><span class="p">,</span>
<span class="o">-</span>                          <span class="n">CrossThreadBindOnce</span><span class="p">(</span><span class="o">&amp;</span><span class="n">IIRFilterHandler</span><span class="o">::</span><span class="n">NotifyBadState</span><span class="p">,</span>
<span class="o">-</span>                                              <span class="n">WrapRefCounted</span><span class="p">(</span><span class="k">this</span><span class="p">)));</span>
<span class="o">+</span>      <span class="n">PostCrossThreadTask</span><span class="p">(</span>
<span class="o">+</span>          <span class="o">*</span><span class="n">task_runner_</span><span class="p">,</span> <span class="n">FROM_HERE</span><span class="p">,</span>
<span class="o">+</span>          <span class="n">CrossThreadBindOnce</span><span class="p">(</span><span class="o">&amp;</span><span class="n">IIRFilterHandler</span><span class="o">::</span><span class="n">NotifyBadState</span><span class="p">,</span> <span class="n">AsWeakPtr</span><span class="p">()));</span>
     <span class="p">}</span>
   <span class="err">}</span>
 <span class="err">}</span>
</code></pre></div></div>

<p>This prevents <code class="language-plaintext highlighter-rouge">IIRFilterHandler</code> from outliving <code class="language-plaintext highlighter-rouge">BaseAudioContext</code> as a cross thread task. As explained in 1055788, in order to destroy <code class="language-plaintext highlighter-rouge">BaseAudioContext</code> while <code class="language-plaintext highlighter-rouge">IIRFilterHandler::NotifyBadState</code> is waiting in the task queue, the <code class="language-plaintext highlighter-rouge">IIRFilterNode</code> that owns the <code class="language-plaintext highlighter-rouge">IIRFilterHandler</code> first needs to be destroyed, and this can only happen while the graph is being pulled, otherwise you won’t arrive at the code that posts <code class="language-plaintext highlighter-rouge">IIRFilterHandler::NotifyBadState</code>. This will cause the ownership of <code class="language-plaintext highlighter-rouge">IIRFilterHandler</code> to be transferred to <code class="language-plaintext highlighter-rouge">rendering_orphan_handlers_</code> in <code class="language-plaintext highlighter-rouge">DeferredTaskHandlers</code>. [1]</p>

<p>When <code class="language-plaintext highlighter-rouge">BaseAudioContext</code> is <em>destroyed</em>, it clears itself out of the handlers in <code class="language-plaintext highlighter-rouge">rendering_orphan_handlers_</code> by calling <code class="language-plaintext highlighter-rouge">DeferredTaskHandler::ContextWillBeDestroyed</code> in the destructor [2].</p>

<div class="language-cpp highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="kt">void</span> <span class="n">DeferredTaskHandler</span><span class="o">::</span><span class="n">ContextWillBeDestroyed</span><span class="p">()</span> <span class="p">{</span>
  <span class="k">for</span> <span class="p">(</span><span class="k">auto</span><span class="o">&amp;</span> <span class="n">handler</span> <span class="o">:</span> <span class="n">rendering_orphan_handlers_</span><span class="p">)</span>
    <span class="n">handler</span><span class="o">-&gt;</span><span class="n">ClearContext</span><span class="p">();</span>
  <span class="k">for</span> <span class="p">(</span><span class="k">auto</span><span class="o">&amp;</span> <span class="n">handler</span> <span class="o">:</span> <span class="n">deletable_orphan_handlers_</span><span class="p">)</span>
    <span class="n">handler</span><span class="o">-&gt;</span><span class="n">ClearContext</span><span class="p">();</span>
  <span class="n">ClearHandlersToBeDeleted</span><span class="p">();</span>
  <span class="c1">// Some handlers might live because of their cross thread tasks.</span>
<span class="p">}</span>
</code></pre></div></div>

<p>This means that to cause a UaF of <code class="language-plaintext highlighter-rouge">AudioHandler</code> using BAC after it is destroyed, the <code class="language-plaintext highlighter-rouge">AudioHandler</code> needs to be removed from <code class="language-plaintext highlighter-rouge">rendering_orphan_handlers_</code> at this point to prevent <code class="language-plaintext highlighter-rouge">context_</code> from being cleared. In the test cases of 1055788 and 1057627, this was done by first destroying the <code class="language-plaintext highlighter-rouge">ExecutionContext</code> and cause <code class="language-plaintext highlighter-rouge">BaseAudioContext::Uninitialize</code> to run, which calls <code class="language-plaintext highlighter-rouge">ClearHandlersToBeDeleted</code> to be called to clear out <code class="language-plaintext highlighter-rouge">rendering_orphan_handlers_</code>.</p>

<p>By making the callbacks holding weak pointers instead of scoped_refptr, the fix ensures that <code class="language-plaintext highlighter-rouge">rendering_orphan_handlers_</code> is the sole owner of the <code class="language-plaintext highlighter-rouge">AudioHandlers</code> after <code class="language-plaintext highlighter-rouge">AudioNode</code> is disposed of and hence the <code class="language-plaintext highlighter-rouge">AudioHandlers</code> cannot outlive <code class="language-plaintext highlighter-rouge">BaseAudioContext</code>. (because when <code class="language-plaintext highlighter-rouge">BaseAudioContext</code> is destroyed, it clears <code class="language-plaintext highlighter-rouge">rendering_orphan_handlers_</code>, causing the handlers to be destroyed) This prevents UaF of BAC from happening.</p>

<p>Use-after-poison, however, can still happen after the object is GCed and before it is destroyed (when destructor is called). As the BAC only cleans itself up from <code class="language-plaintext highlighter-rouge">rendering_orphan_handlers_</code> and <code class="language-plaintext highlighter-rouge">deletable_orphan_handlers_</code> when it is destroyed, by triggering the callbacks in the window after BAC is garbage collected and before it is destroyed (destructor called), it is still possible to cause UaP. At this point, <code class="language-plaintext highlighter-rouge">rendering_orphan_handlers_</code> will still be keeping the <code class="language-plaintext highlighter-rouge">AudioHandler</code> alive while the <code class="language-plaintext highlighter-rouge">AudioHandler</code> still holds BAC as an <code class="language-plaintext highlighter-rouge">UntraceMember</code>, but because BAC is already garbage collected, a UaP will happen when the callback is run and trying to access BAC by calling <code class="language-plaintext highlighter-rouge">Context()-&gt;GetExecutionContext()</code>:</p>

<div class="language-cpp highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="kt">void</span> <span class="n">IIRFilterHandler</span><span class="o">::</span><span class="n">NotifyBadState</span><span class="p">()</span> <span class="k">const</span> <span class="p">{</span>
  <span class="n">DCHECK</span><span class="p">(</span><span class="n">IsMainThread</span><span class="p">());</span>
  <span class="k">if</span> <span class="p">(</span><span class="o">!</span><span class="n">Context</span><span class="p">()</span> <span class="o">||</span> <span class="o">!</span><span class="n">Context</span><span class="p">()</span><span class="o">-&gt;</span><span class="n">GetExecutionContext</span><span class="p">())</span> <span class="c1">//&lt;-- UaP can still happen when Context()-&gt;GetExecutionContext is accessed.</span>
    <span class="k">return</span><span class="p">;</span>
  <span class="p">....</span>
</code></pre></div></div>

<p>To prevent this, and other cases that are fixed here: https://source.chromium.org/chromium/chromium/src/+/b75436e554d54b2d8d3590d7e61607e1ce67a2fe?originalUrl=https:%2F%2Fcs.chromium.org%2F I’d suggest adding a prefinalizer to <code class="language-plaintext highlighter-rouge">BaseAudioContext</code> and clean itself up from <code class="language-plaintext highlighter-rouge">rendering_orphan_handlers_</code> and <code class="language-plaintext highlighter-rouge">deletable_orphan_handlers_</code> there:</p>

<div class="language-cpp highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="kt">void</span> <span class="n">BaseAudioContext</span><span class="o">::</span><span class="n">Dispose</span><span class="p">()</span> <span class="p">{</span>
  <span class="k">for</span> <span class="p">(</span><span class="k">auto</span><span class="o">&amp;</span> <span class="n">handler</span> <span class="o">:</span> <span class="n">rendering_orphan_handlers_</span><span class="p">)</span>
    <span class="n">handler</span><span class="o">-&gt;</span><span class="n">ClearContext</span><span class="p">();</span>
  <span class="k">for</span> <span class="p">(</span><span class="k">auto</span><span class="o">&amp;</span> <span class="n">handler</span> <span class="o">:</span> <span class="n">deletable_orphan_handlers_</span><span class="p">)</span>
    <span class="n">handler</span><span class="o">-&gt;</span><span class="n">ClearContext</span><span class="p">();</span>
<span class="p">}</span>
</code></pre></div></div>

<p>as <code class="language-plaintext highlighter-rouge">AudioHandler</code> should not hold on to a reference of <code class="language-plaintext highlighter-rouge">BaseAudioContext</code> after it is garbage collected, this should have little side effect. The previous fixes in those issues, however, are still necessary to prevent UaF and should not be removed.</p>

<ol>
  <li>https://source.chromium.org/chromium/chromium/src/+/129460b86794115e96b5ec4ee724f7ac971d1f41:third_party/blink/renderer/modules/webaudio/audio_node.cc;l=619;bpv=1;bpt=1?originalUrl=https:%2F%2Fcs.chromium.org%2F</li>
  <li>https://source.chromium.org/chromium/chromium/src/+/129460b86794115e96b5ec4ee724f7ac971d1f41:third_party/blink/renderer/modules/webaudio/base_audio_context.cc;l=112;bpv=1;bpt=1?originalUrl=https:%2F%2Fcs.chromium.org%2F</li>
</ol>

<h3 id="impact">Impact</h3>

<p>Use-after-free in renderer.</p>

<h2 id="coordinated-disclosure-timeline">Coordinated Disclosure Timeline</h2>
<ul>
  <li>17/03/2020 Reported as <a href="https://bugs.chromium.org/p/chromium/issues/detail?id=1062247">Chromium Issue 1062247</a></li>
  <li>31/03/2020 <a href="https://chromereleases.googleblog.com/2020/03/stable-channel-update-for-desktop_31.html">Fixed in 80.0.3987.162</a></li>
</ul>

<h2 id="credit">Credit</h2>

<p>This issue was discovered and reported by GHSL team member <a href="https://github.com/m-y-mo">@m-y-mo (Man Yue Mo)</a>.</p>

<h2 id="contact">Contact</h2>

<p>You can contact the GHSL team at <code class="language-plaintext highlighter-rouge">securitylab@github.com</code>, please include the <code class="language-plaintext highlighter-rouge">GHSL-2020-053</code> in any communication regarding this issue.</p>

