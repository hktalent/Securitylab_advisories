>
    <header class="post-header d-block mb-6">
      <div class="date text-mono f5 my-3">June 17, 2020</div>
      <h1 class="my-2 h00-mktg lh-condensed">GHSL-2020-100: Out of Bounds (OOB) read vulnerability in FreeRDP - CVE-2020-13396</h1>

      
      
      
      
      

      

      <a target="_blank" class="sc-frDJqD SgxRc d-inline-flex flex-row flex-items-center text-gray" href="https://github.com/antonio-morales">
        <img class="mr-3" src="https://avatars.githubusercontent.com/u/55253029?s=35" height="35" width="35">
        <span>Antonio Morales</span>
      </a>
    </header>

    <main id="content" class="markdown-body" aria-label="Content">
      <h2 id="summary">Summary</h2>

<p>An out-of-bounds (OOB) read vulnerability has been detected in <code class="language-plaintext highlighter-rouge">ntlm_read_ChallengeMessage</code> due to a memcpy with an attacker-controlled size. This issue was addressed in FreeRDP version 2.1.1.</p>

<h2 id="product">Product</h2>

<p>FreeRDP</p>

<h2 id="tested-version">Tested Version</h2>

<p>Development version - master branch (May 14, 2020)</p>

<h2 id="details-out-of-bound-read-in-ntlm_read_challengemessage-function">Details: Out-of-bound read in <code class="language-plaintext highlighter-rouge">ntlm_read_ChallengeMessage</code> function</h2>

<p>The <code class="language-plaintext highlighter-rouge">ntlm_read_ChallengeMessage</code> function in <code class="language-plaintext highlighter-rouge">ntlm_message.c</code> performs a call to <code class="language-plaintext highlighter-rouge">CopyMemory(context-&gt;ChallengeMessage.pvBuffer, StartOffset, length)</code> (line 494), where <code class="language-plaintext highlighter-rouge">length</code> is a value that can be controlled indirectly by a potential attacker.</p>

<p><code class="language-plaintext highlighter-rouge">CopyMemory</code> function is nothing else than a <code class="language-plaintext highlighter-rouge">memcpy</code> wrapper defined as:</p>

<p><a href="https://github.com/FreeRDP/FreeRDP/blob/8515846317a210746a8d8316c2f99c652b357802/winpr/include/winpr/crt.h#L107">View on GitHub!</a></p>
<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="cp">#define CopyMemory(Destination, Source, Length) memcpy((Destination), (Source), (Length))
</span></code></pre></div></div>

<p>As we can see below, <code class="language-plaintext highlighter-rouge">length</code> is equal to the addition of <code class="language-plaintext highlighter-rouge">TargetName.Len</code> and <code class="language-plaintext highlighter-rouge">TargetInfo.Len</code>, both values being controlled by the remote input.</p>

<p><a href="https://github.com/FreeRDP/FreeRDP/blob/8241ab42fdf0cc89cf69fc574bf6360c9977a0d4/winpr/libwinpr/sspi/NTLM/ntlm_message.c#L486-L494">View on GitHub!</a></p>
<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="cm">/* ntlm_message.c : 486 */</span>

	<span class="n">length</span> <span class="o">=</span> <span class="p">(</span><span class="n">PayloadOffset</span> <span class="o">-</span> <span class="n">StartOffset</span><span class="p">)</span> <span class="o">+</span> <span class="n">message</span><span class="o">-&gt;</span><span class="n">TargetName</span><span class="p">.</span><span class="n">Len</span> <span class="o">+</span> <span class="n">message</span><span class="o">-&gt;</span><span class="n">TargetInfo</span><span class="p">.</span><span class="n">Len</span><span class="p">;</span>

	<span class="k">if</span> <span class="p">(</span><span class="o">!</span><span class="n">sspi_SecBufferAlloc</span><span class="p">(</span><span class="o">&amp;</span><span class="n">context</span><span class="o">-&gt;</span><span class="n">ChallengeMessage</span><span class="p">,</span> <span class="n">length</span><span class="p">))</span>
	<span class="p">{</span>
		<span class="n">Stream_Free</span><span class="p">(</span><span class="n">s</span><span class="p">,</span> <span class="n">FALSE</span><span class="p">);</span>
		<span class="k">return</span> <span class="n">SEC_E_INTERNAL_ERROR</span><span class="p">;</span>
	<span class="p">}</span>

	<span class="n">CopyMemory</span><span class="p">(</span><span class="n">context</span><span class="o">-&gt;</span><span class="n">ChallengeMessage</span><span class="p">.</span><span class="n">pvBuffer</span><span class="p">,</span> <span class="n">StartOffset</span><span class="p">,</span> <span class="n">length</span><span class="p">);</span>
</code></pre></div></div>

<p>And <code class="language-plaintext highlighter-rouge">StartOffset</code> is a pointer to <code class="language-plaintext highlighter-rouge">s</code> wStream*, which in turn points to <code class="language-plaintext highlighter-rouge">buffer-&gt;pvBuffer</code> array. But there is any statement for checking that <code class="language-plaintext highlighter-rouge">length</code> value is greater than <code class="language-plaintext highlighter-rouge">buffer-&gt;pvBuffer</code> size.</p>

<p><a href="https://github.com/FreeRDP/FreeRDP/blob/8241ab42fdf0cc89cf69fc574bf6360c9977a0d4/winpr/libwinpr/sspi/NTLM/ntlm_message.c#L370-L384">View on GitHub!</a></p>
<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="cm">/* ntlm_message.c : 370 */</span>

 <span class="n">PBYTE</span> <span class="n">StartOffset</span><span class="p">;</span>
 <span class="p">...</span>
 <span class="n">s</span> <span class="o">=</span> <span class="n">Stream_New</span><span class="p">((</span><span class="n">BYTE</span><span class="o">*</span><span class="p">)</span><span class="n">buffer</span><span class="o">-&gt;</span><span class="n">pvBuffer</span><span class="p">,</span> <span class="n">buffer</span><span class="o">-&gt;</span><span class="n">cbBuffer</span><span class="p">);</span>
 <span class="p">...</span>
 <span class="n">StartOffset</span> <span class="o">=</span> <span class="n">Stream_Pointer</span><span class="p">(</span><span class="n">s</span><span class="p">);</span>
</code></pre></div></div>
<p>As a result, OOB reads can occurs resulting in accessing a memory location that is outside of the boundaries of the <code class="language-plaintext highlighter-rouge">buffer-&gt;pvBuffer</code> array.</p>

<h3 id="impact">Impact</h3>

<p>This issue may lead to an Out-of-Bounds read.</p>

<h2 id="cve">CVE</h2>

<ul>
  <li>CVE-2020-13396</li>
</ul>

<h2 id="coordinated-disclosure-timeline">Coordinated Disclosure Timeline</h2>

<p>This report was subject to the GHSL <a href="https://securitylab.github.com/advisories/#policy">coordinated disclosure policy</a>.</p>

<ul>
  <li>05/14/2020: Vendor contacted</li>
  <li>05/15/2020: Vendor acknowledges report</li>
  <li>05/15/2020: Bug fixed and patch released by the vendor</li>
</ul>

<h2 id="resources">Resources</h2>

<ul>
  <li>https://github.com/FreeRDP/FreeRDP/commit/48361c411e50826cb602c7aab773a8a20e1da6bc</li>
  <li>https://github.com/FreeRDP/FreeRDP/commit/8fb6336a4072abcee8ce5bd6ae91104628c7bb69</li>
</ul>

<h2 id="credit">Credit</h2>

<p>This issue was discovered and reported by GHSL team member <a href="https://github.com/antonio-morales">@antonio-morales (Antonio Morales)</a>.</p>

<h2 id="contact">Contact</h2>

<p>You can contact the GHSL team at <code class="language-plaintext highlighter-rouge">securitylab@github.com</code>, please include <code class="language-plaintext highlighter-rouge">GHSL-2020-100</code> in any communication regarding this issue.</p>