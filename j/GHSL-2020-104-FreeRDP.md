>
    <header class="post-header d-block mb-6">
      <div class="date text-mono f5 my-3">July 1, 2020</div>
      <h1 class="my-2 h00-mktg lh-condensed">GHSL-2020-104: OOB read vulnerability in FreeRDP ntlm_av_pair_get - CVE-2020-11097</h1>

      
      
      
      
      

      

      <a target="_blank" class="sc-frDJqD SgxRc d-inline-flex flex-row flex-items-center text-gray" href="https://github.com/antonio-morales">
        <img class="mr-3" src="https://avatars.githubusercontent.com/u/55253029?s=35" height="35" width="35">
        <span>Antonio Morales</span>
      </a>
    </header>

    <main id="content" class="markdown-body" aria-label="Content">
      <h2 id="summary">Summary</h2>

<p>An out-of-bounds (OOB) read vulnerability has been detected in <code class="language-plaintext highlighter-rouge">ntlm_av_pair_get</code> function due to a corrupted <code class="language-plaintext highlighter-rouge">NTLM_AV_PAIR</code> linked-list.</p>

<h2 id="product">Product</h2>

<p>FreeRDP</p>

<h2 id="tested-version">Tested Version</h2>

<p>Development version - master branch (May 22, 2020)</p>

<h2 id="details-out-of-bound-read-in-ntlm_av_pair_get">Details: Out-of-bound read in <code class="language-plaintext highlighter-rouge">ntlm_av_pair_get</code></h2>

<p>The <code class="language-plaintext highlighter-rouge">ntlm_av_pair_get</code> function in <code class="language-plaintext highlighter-rouge">ntlm_av_pairs.c</code> performs a call to <code class="language-plaintext highlighter-rouge">ntlm_av_pair_get_id(pAvPair)</code> (line 173), where <code class="language-plaintext highlighter-rouge">pAvPair</code> is a pointer to a linked-list of <code class="language-plaintext highlighter-rouge">NTLM_AV_PAIR</code>. The problem here is that pAvPairList may be a corrupted linked-list:</p>

<p><a href="https://github.com/FreeRDP/FreeRDP/blob/057b6df4aebbe8e739139087dfaab15104ca5ba7/winpr/libwinpr/sspi/NTLM/ntlm_av_pairs.c#L162">View on GitHub!</a></p>
<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="cm">/* winpr/libwinpr/sspi/NTLM/ntlm_av_pairs.c */</span>

<span class="n">NTLM_AV_PAIR</span><span class="o">*</span> <span class="nf">ntlm_av_pair_get</span><span class="p">(</span><span class="n">NTLM_AV_PAIR</span><span class="o">*</span> <span class="n">pAvPairList</span><span class="p">,</span> <span class="kt">size_t</span> <span class="n">cbAvPairList</span><span class="p">,</span> <span class="n">NTLM_AV_ID</span> <span class="n">AvId</span><span class="p">,</span>
                               <span class="kt">size_t</span><span class="o">*</span> <span class="n">pcbAvPairListRemaining</span><span class="p">)</span>
<span class="p">{</span>
	<span class="kt">size_t</span> <span class="n">cbAvPair</span> <span class="o">=</span> <span class="n">cbAvPairList</span><span class="p">;</span>
	<span class="n">NTLM_AV_PAIR</span><span class="o">*</span> <span class="n">pAvPair</span> <span class="o">=</span> <span class="n">pAvPairList</span><span class="p">;</span>

	<span class="k">if</span> <span class="p">(</span><span class="o">!</span><span class="n">ntlm_av_pair_check</span><span class="p">(</span><span class="n">pAvPair</span><span class="p">,</span> <span class="n">cbAvPair</span><span class="p">))</span>
		<span class="n">pAvPair</span> <span class="o">=</span> <span class="nb">NULL</span><span class="p">;</span>

	<span class="k">while</span> <span class="p">(</span><span class="n">pAvPair</span><span class="p">)</span>
	<span class="p">{</span>
		<span class="n">UINT16</span> <span class="n">id</span> <span class="o">=</span> <span class="n">ntlm_av_pair_get_id</span><span class="p">(</span><span class="n">pAvPair</span><span class="p">);</span>
</code></pre></div></div>

<p>The corruption is a result of a previously read malformed linked-list member values. Let’s take a closer look at how this corruption occurs:</p>

<p><a href="https://github.com/FreeRDP/FreeRDP/blob/2eedede058f87f80839f54aeb897e4ad93b8270d/winpr/libwinpr/sspi/NTLM/ntlm_av_pairs.c#L528">View on GitHub!</a></p>
<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="cm">/* winpr/libwinpr/sspi/NTLM/ntlm_av_pairs.c */</span>

<span class="kt">int</span> <span class="nf">ntlm_construct_authenticate_target_info</span><span class="p">(</span><span class="n">NTLM_CONTEXT</span><span class="o">*</span> <span class="n">context</span><span class="p">)</span>
<span class="p">{</span>
 <span class="p">...</span>
 <span class="n">ChallengeTargetInfo</span> <span class="o">=</span> <span class="p">(</span><span class="n">NTLM_AV_PAIR</span><span class="o">*</span><span class="p">)</span><span class="n">context</span><span class="o">-&gt;</span><span class="n">ChallengeTargetInfo</span><span class="p">.</span><span class="n">pvBuffer</span><span class="p">;</span>
 <span class="p">...</span>
 <span class="n">AvEOL</span> <span class="o">=</span> <span class="n">ntlm_av_pair_get</span><span class="p">(</span><span class="n">ChallengeTargetInfo</span><span class="p">,</span> <span class="n">cbChallengeTargetInfo</span><span class="p">,</span> <span class="n">MsvAvEOL</span><span class="p">,</span> <span class="nb">NULL</span><span class="p">);</span>

</code></pre></div></div>

<p>As you can see above, <code class="language-plaintext highlighter-rouge">ChallengeTargetInfo</code> is the linked-list which is passed as an argument to <code class="language-plaintext highlighter-rouge">ntlm_av_pair_get</code> function, and that, in turn, is equal to <code class="language-plaintext highlighter-rouge">context-&gt;ChallengeTargetInfo.pvBuffer</code>. Next we will see how <code class="language-plaintext highlighter-rouge">context-&gt;ChallengeTargetInfo</code> is used in the <code class="language-plaintext highlighter-rouge">ntlm_read_message_fields_buffer</code> function:</p>

<p><a href="https://github.com/FreeRDP/FreeRDP/blob/2eedede058f87f80839f54aeb897e4ad93b8270d/winpr/libwinpr/sspi/NTLM/ntlm_message.c#L439">View on GitHub!</a></p>
<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="cm">/* winpr/libwinpr/sspi/NTLM/ntlm_message.c */</span>

<span class="n">ntlm_read_ChallengeMessage</span><span class="p">(</span><span class="n">NTLM_CONTEXT</span><span class="o">*</span> <span class="n">context</span><span class="p">,</span> <span class="n">PSecBuffer</span> <span class="n">buffer</span><span class="p">)</span>
<span class="p">{</span>
<span class="p">...</span>
 <span class="k">if</span> <span class="p">(</span><span class="n">ntlm_read_message_fields_buffer</span><span class="p">(</span><span class="n">s</span><span class="p">,</span> <span class="o">&amp;</span><span class="p">(</span><span class="n">message</span><span class="o">-&gt;</span><span class="n">TargetInfo</span><span class="p">))</span> <span class="o">&lt;</span> <span class="mi">0</span><span class="p">)</span>
 <span class="k">goto</span> <span class="n">fail</span><span class="p">;</span>

 <span class="n">context</span><span class="o">-&gt;</span><span class="n">ChallengeTargetInfo</span><span class="p">.</span><span class="n">pvBuffer</span> <span class="o">=</span> <span class="n">message</span><span class="o">-&gt;</span><span class="n">TargetInfo</span><span class="p">.</span><span class="n">Buffer</span><span class="p">;</span>
<span class="p">...</span>
</code></pre></div></div>

<p>At this point, the problem is that the FreeRDP client is reading these offsets directly from the server, without checking they are correct.</p>

<p>So, a malicious attacker could set a malicious offset and when <code class="language-plaintext highlighter-rouge">ntlm_av_pair_get_id</code> will be called, the program will try to access a non-existent list member:</p>

<p><a href="https://github.com/FreeRDP/FreeRDP/blob/057b6df4aebbe8e739139087dfaab15104ca5ba7/winpr/libwinpr/sspi/NTLM/ntlm_av_pairs.c#L73">View on GitHub!</a></p>
<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="cm">/* winpr/libwinpr/sspi/NTLM/ntlm_av_pairs.c */</span>

<span class="k">static</span> <span class="n">INLINE</span> <span class="n">UINT16</span> <span class="nf">ntlm_av_pair_get_id</span><span class="p">(</span><span class="k">const</span> <span class="n">NTLM_AV_PAIR</span><span class="o">*</span> <span class="n">pAvPair</span><span class="p">)</span>
<span class="p">{</span>
	<span class="n">UINT16</span> <span class="n">AvId</span><span class="p">;</span>

	<span class="n">Data_Read_UINT16</span><span class="p">(</span><span class="o">&amp;</span><span class="n">pAvPair</span><span class="o">-&gt;</span><span class="n">AvId</span><span class="p">,</span> <span class="n">AvId</span><span class="p">);</span>

	<span class="k">return</span> <span class="n">AvId</span><span class="p">;</span>
<span class="p">}</span>
</code></pre></div></div>

<p>As a result, OOB reads can occurs resulting in accessing memory that has not been allocated by FreeRDP process.</p>

<h3 id="impact">Impact</h3>

<p>This issue may lead to Out-of-Bounds read.</p>

<h2 id="cve">CVE</h2>
<ul>
  <li>CVE-2020-11097</li>
</ul>

<h2 id="coordinated-disclosure-timeline">Coordinated Disclosure Timeline</h2>

<p>This report was subject to the GHSL <a href="https://securitylab.github.com/advisories/#policy">coordinated disclosure policy</a>.</p>

<ul>
  <li>05/22/2020: Vendor contacted</li>
  <li>05/26/2020: Vendor acknowledges report</li>
  <li>06/22/2020: Bug fixed and patch released by the vendor</li>
</ul>

<h2 id="supporting-resources">Supporting Resources</h2>

<ul>
  <li>https://github.com/FreeRDP/FreeRDP/security/advisories/GHSA-c8x2-c3c9-9r3f</li>
  <li>https://github.com/FreeRDP/FreeRDP/commit/58a3122250d54de3a944c487776bcd4d1da4721e#diff-758f5a86ba21ec7cc3805bbc33db6fea</li>
</ul>

<h2 id="credit">Credit</h2>

<p>This issue was discovered and reported by GHSL team member <a href="https://github.com/antonio-morales">@antonio-morales (Antonio Morales)</a>.</p>

<h2 id="contact">Contact</h2>

<p>You can contact the GHSL team at <code class="language-plaintext highlighter-rouge">securitylab@github.com</code>, please include the <code class="language-plaintext highlighter-rouge">GHSL-2020-104</code> in any communication regarding this issue.</