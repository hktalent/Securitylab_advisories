<header class="post-header d-block mb-6">
      <div class="date text-mono f5 my-3">April 16, 2020</div>
      <h1 class="my-2 h00-mktg lh-condensed">GHSL-2020-038: Use after free in Chrome WebAudio</h1>

      
      
      
      
      

      

      <a target="_blank" class="sc-frDJqD SgxRc d-inline-flex flex-row flex-items-center text-gray" href="https://github.com/m-y-mo">
        <img class="mr-3" src="https://avatars.githubusercontent.com/u/15773368?s=35" height="35" width="35">
        <span>Man Yue Mo</span>
      </a>
    </header>

    <main id="content" class="markdown-body" aria-label="Content">
      <h2 id="summary">Summary</h2>
<p>UaP in <code class="language-plaintext highlighter-rouge">AudioScheduledSourceHandler::NotifyEnded</code></p>

<h2 id="product">Product</h2>
<p>Chrome</p>

<h2 id="cve">CVE</h2>
<p>CVE-2020-6429</p>

<h2 id="tested-version">Tested Version</h2>
<p>Chrome version: master branch build e577636, release build 80.3987.122
Operating System: Ubuntu 18.04</p>

<h2 id="details">Details</h2>

<p>This issue is similar to 1055788, in that an <code class="language-plaintext highlighter-rouge">AudioHandler</code> is being posted to a task queue as a <code class="language-plaintext highlighter-rouge">scoped_refptr</code> and the <code class="language-plaintext highlighter-rouge">context_ UntracedMember</code> is destroyed while it is waiting in the task queue.</p>

<p>The <code class="language-plaintext highlighter-rouge">AudioScheduledSourceHandler::Finish</code> method is called in the pre-rendering stage when <code class="language-plaintext highlighter-rouge">DeferredTaskHandler::HandlePreRenderTask</code> is called and a stop is scheduled. (<code class="language-plaintext highlighter-rouge">OfflineAudioContext::HandlePreRenderTasks</code> -&gt; <code class="language-plaintext highlighter-rouge">HandleStoppableSourceNodes</code> -&gt; <code class="language-plaintext highlighter-rouge">AudioScheduledSourceHandler::HandleStoppableSourceNode</code> -&gt; <code class="language-plaintext highlighter-rouge">AudioScheduledSourceHandler::Finish</code>)</p>

<p>This method posts a task to the main thread, wrapping the handler as a <code class="language-plaintext highlighter-rouge">scoped_refptr</code>:</p>

<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="kt">void</span> <span class="n">AudioScheduledSourceHandler</span><span class="o">::</span><span class="n">Finish</span><span class="p">()</span> <span class="p">{</span>
  <span class="n">FinishWithoutOnEnded</span><span class="p">();</span>

  <span class="n">PostCrossThreadTask</span><span class="p">(</span>
      <span class="o">*</span><span class="n">task_runner_</span><span class="p">,</span> <span class="n">FROM_HERE</span><span class="p">,</span>
      <span class="n">CrossThreadBindOnce</span><span class="p">(</span><span class="o">&amp;</span><span class="n">AudioScheduledSourceHandler</span><span class="o">::</span><span class="n">NotifyEnded</span><span class="p">,</span>
                          <span class="n">WrapRefCounted</span><span class="p">(</span><span class="n">this</span><span class="p">)));</span>
<span class="p">}</span>
</code></pre></div></div>

<p>The <code class="language-plaintext highlighter-rouge">AudioScheduledSourceHandler::NotifyEnded</code> method then calls <code class="language-plaintext highlighter-rouge">GetExecutionContext</code>. However, it is possible for <code class="language-plaintext highlighter-rouge">context_</code> to be destroyed while <code class="language-plaintext highlighter-rouge">NotifyEnded</code> is waiting in the queue. This will cause UaP/UaF when <code class="language-plaintext highlighter-rouge">Context()-&gt;GetExecutionContext()</code> is called in <code class="language-plaintext highlighter-rouge">NotifyEnded</code>.</p>

<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="kt">void</span> <span class="n">AudioScheduledSourceHandler</span><span class="o">::</span><span class="n">NotifyEnded</span><span class="p">()</span> <span class="p">{</span>
  <span class="n">DCHECK</span><span class="p">(</span><span class="n">IsMainThread</span><span class="p">());</span>
  <span class="k">if</span> <span class="p">(</span><span class="o">!</span><span class="n">Context</span><span class="p">()</span> <span class="o">||</span> <span class="o">!</span><span class="n">Context</span><span class="p">()</span><span class="o">-&gt;</span><span class="n">GetExecutionContext</span><span class="p">())</span> 
    <span class="k">return</span><span class="p">;</span>
  <span class="k">if</span> <span class="p">(</span><span class="n">GetNode</span><span class="p">())</span>
    <span class="n">GetNode</span><span class="p">()</span><span class="o">-&gt;</span><span class="n">DispatchEvent</span><span class="p">(</span><span class="o">*</span><span class="n">Event</span><span class="o">::</span><span class="n">Create</span><span class="p">(</span><span class="n">event_type_names</span><span class="o">::</span><span class="n">kEnded</span><span class="p">));</span>
<span class="p">}</span>
</code></pre></div></div>

<p>A more detailed analysis can be found in ticket 1055788.</p>

<h3 id="impact">Impact</h3>

<p>Use-after-free in renderer.</p>

<h2 id="coordinated-disclosure-timeline">Coordinated Disclosure Timeline</h2>
<ul>
  <li>02/03/2020 Reported as <a href="https://bugs.chromium.org/p/chromium/issues/detail?id=1057627">Chromium Issue 1057627</a></li>
  <li>18/03/2020 <a href="https://chromereleases.googleblog.com/2020/03/stable-channel-update-for-desktop_18.html">Fixed in version 80.0.3987.149</a></li>
</ul>

<h2 id="credit">Credit</h2>

<p>This issue was discovered and reported by GHSL team member <a href="https://github.com/m-y-mo">@m-y-mo (Man Yue Mo)</a>.</p>

<h2 id="contact">Contact</h2>

<p>You can contact the GHSL team at <code class="language-plaintext highlighter-rouge">securitylab@github.com</code>, please include the <code class="language-plaintext highlighter-rouge">GHSL-2020-038</code> in any communication regarding this issue.</p>

    