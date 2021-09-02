<header class="post-header d-block mb-6">
      <div class="date text-mono f5 my-3">April 16, 2020</div>
      <h1 class="my-2 h00-mktg lh-condensed">GHSL-2020-035: Use after free in Chrome WebAudio</h1>

      
      
      
      
      

      

      <a target="_blank" class="sc-frDJqD SgxRc d-inline-flex flex-row flex-items-center text-gray" href="https://github.com/m-y-mo">
        <img class="mr-3" src="https://avatars.githubusercontent.com/u/15773368?s=35" height="35" width="35">
        <span>Man Yue Mo</span>
      </a>
    </header>

    <main id="content" class="markdown-body" aria-label="Content">
      <h2 id="summary">Summary</h2>

<p>UaP in <code class="language-plaintext highlighter-rouge">IIRFilterHandler::Process</code></p>

<h2 id="product">Product</h2>
<p>Chrome</p>

<h2 id="cve">CVE</h2>
<p>CVE-2020-6427</p>

<h2 id="tested-version">Tested Version</h2>
<p>Chrome version: master branch build 8f57323, release build.
Operating System: Ubuntu 18.04</p>

<h2 id="details">Details</h2>

<p>In the <code class="language-plaintext highlighter-rouge">IIRFilterHandler::Process</code> method, if an infinite output is encountered, the method <code class="language-plaintext highlighter-rouge">IIRFilterHandler::NotifyBadState</code> method will be posted to the main thread[1]:</p>

<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code>    <span class="k">if</span> <span class="p">(</span><span class="n">HasNonFiniteOutput</span><span class="p">())</span> <span class="p">{</span>
      <span class="n">did_warn_bad_filter_state_</span> <span class="o">=</span> <span class="nb">true</span><span class="p">;</span>

      <span class="n">PostCrossThreadTask</span><span class="p">(</span><span class="o">*</span><span class="n">task_runner_</span><span class="p">,</span> <span class="n">FROM_HERE</span><span class="p">,</span>
                          <span class="n">CrossThreadBindOnce</span><span class="p">(</span><span class="o">&amp;</span><span class="n">IIRFilterHandler</span><span class="o">::</span><span class="n">NotifyBadState</span><span class="p">,</span>
                                              <span class="n">WrapRefCounted</span><span class="p">(</span><span class="n">this</span><span class="p">)));</span>
    <span class="p">}</span>
</code></pre></div></div>
<p>The method <code class="language-plaintext highlighter-rouge">IIRFilterHandler::NotifyBadState</code> first checks for Context and then call <code class="language-plaintext highlighter-rouge">Context()-&gt;GetExecutionContext()</code>[2].</p>

<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="kt">void</span> <span class="n">IIRFilterHandler</span><span class="o">::</span><span class="n">NotifyBadState</span><span class="p">()</span> <span class="k">const</span> <span class="p">{</span>
  <span class="n">DCHECK</span><span class="p">(</span><span class="n">IsMainThread</span><span class="p">());</span>
  <span class="k">if</span> <span class="p">(</span><span class="o">!</span><span class="n">Context</span><span class="p">()</span> <span class="o">||</span> <span class="o">!</span><span class="n">Context</span><span class="p">()</span><span class="o">-&gt;</span><span class="n">GetExecutionContext</span><span class="p">())</span>
    <span class="k">return</span><span class="p">;</span>
</code></pre></div></div>

<p>However, as <code class="language-plaintext highlighter-rouge">Context</code> is an <code class="language-plaintext highlighter-rouge">UntracedMember</code>[3], it is possible to remove it while the <code class="language-plaintext highlighter-rouge">IIRFilterHandler::NotifyBadState</code> method is waiting in the main queue. This then causes UaP and subsequently UaF in <code class="language-plaintext highlighter-rouge">NotifyBadState</code>.</p>

<p>The <code class="language-plaintext highlighter-rouge">BiquadFilterHandler</code> also has an identical routine, so it probably is also vulnerable to this issue [4].</p>

<ol>
  <li>
    <p>https://source.chromium.org/chromium/chromium/src/+/b4c8e1370db91786c807e01ca6d56a88b4054070:third_party/blink/renderer/modules/webaudio/iir_filter_node.cc;l=108;bpv=1;bpt=1?originalUrl=https:%2F%2Fcs.chromium.org%2F</p>
  </li>
  <li>
    <p>https://source.chromium.org/chromium/chromium/src/+/b4c8e1370db91786c807e01ca6d56a88b4054070:third_party/blink/renderer/modules/webaudio/iir_filter_node.cc;l=117;bpv=1;bpt=1?originalUrl=https:%2F%2Fcs.chromium.org%2F</p>
  </li>
  <li>
    <p>https://source.chromium.org/chromium/chromium/src/+/b4c8e1370db91786c807e01ca6d56a88b4054070:third_party/blink/renderer/modules/webaudio/audio_node.h;drc=5cc67ce9c0e922a742dc0064ad38c4f8f9668aa9;bpv=1;bpt=1;l=291?originalUrl=https:%2F%2Fcs.chromium.org%2F</p>
  </li>
  <li>
    <p>https://source.chromium.org/chromium/chromium/src/+/b4c8e1370db91786c807e01ca6d56a88b4054070:third_party/blink/renderer/modules/webaudio/biquad_filter_node.cc;l=88;bpv=1;bpt=1?originalUrl=https:%2F%2Fcs.chromium.org%2F</p>
  </li>
</ol>

<h3 id="impact">Impact</h3>

<p>Use-after-free in renderer.</p>

<h2 id="coordinated-disclosure-timeline">Coordinated Disclosure Timeline</h2>
<ul>
  <li>25/02/2020 Reported as <a href="https://https://bugs.chromium.org/p/chromium/issues/detail?id=1055788">Chromium Issue 1055788</a></li>
  <li>18/03/2020 <a href="https://chromereleases.googleblog.com/2020/03/stable-channel-update-for-desktop_18.html">Fixed in version 80.0.3987.149</a></li>
</ul>

<h2 id="credit">Credit</h2>

<p>This issue was discovered and reported by GHSL team member <a href="https://github.com/m-y-mo">@m-y-mo (Man Yue Mo)</a>.</p>

<h2 id="contact">Contact</h2>

<p>You can contact the GHSL team at <code class="language-plaintext highlighter-rouge">securitylab@github.com</code>, please include the <code class="language-plaintext highlighter-rouge">GHSL-2020-035</code> in any communication regarding this issue.</p>

    