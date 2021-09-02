<header class="post-header d-block mb-6">
      <div class="date text-mono f5 my-3">July 1, 2020</div>
      <h1 class="my-2 h00-mktg lh-condensed">GHSL-2020-106: integer signedness mismatch leading to OOB read in FreeRDP - CVE-2020-4030</h1>

      
      
      
      
      

      

      <a target="_blank" class="sc-frDJqD SgxRc d-inline-flex flex-row flex-items-center text-gray" href="https://github.com/antonio-morales">
        <img class="mr-3" src="https://avatars.githubusercontent.com/u/55253029?s=35" height="35" width="35">
        <span>Antonio Morales</span>
      </a>
    </header>

    <main id="content" class="markdown-body" aria-label="Content">
      <h2 id="summary">Summary</h2>

<p>An integer signedness mismatch vulnerability has been detected in the <code class="language-plaintext highlighter-rouge">trio_length_max</code> function in <code class="language-plaintext highlighter-rouge">triostr.c</code>.</p>

<h2 id="product">Product</h2>

<p>FreeRDP</p>

<h2 id="tested-version">Tested Version</h2>

<p>Development version - master branch (May 25, 2020)</p>

<h2 id="details-integer-casting-vulnerability-in-trio_length_max">Details: Integer casting vulnerability in <code class="language-plaintext highlighter-rouge">trio_length_max</code></h2>

<p>Under certain circumstances (mainly when /log-level:TRACE is enabled and WLog_PrintMessage is called) the <code class="language-plaintext highlighter-rouge">TrioParse</code> parse function in <code class="language-plaintext highlighter-rouge">trio.c</code> returns <code class="language-plaintext highlighter-rouge">parameters.precision = -1</code>. This value is subsequently passed as the <code class="language-plaintext highlighter-rouge">max</code> parameter to the <code class="language-plaintext highlighter-rouge">trio_length_max</code> function.</p>

<p>So, the problem is that the <code class="language-plaintext highlighter-rouge">size_t max</code> argument in the <code class="language-plaintext highlighter-rouge">trio_length_max</code> function is an unsigned integer, but <code class="language-plaintext highlighter-rouge">precision</code> is a signed integer. For this reason, when <code class="language-plaintext highlighter-rouge">precision = -1</code> is passed to the function <code class="language-plaintext highlighter-rouge">trio_lenght_max</code>, the <code class="language-plaintext highlighter-rouge">max</code> parameter is converted to <code class="language-plaintext highlighter-rouge">SIZE_MAX</code> which on e.g. 64bit Linux is <code class="language-plaintext highlighter-rouge">18446744073709551615UL</code>.</p>

<p><a href="https://github.com/FreeRDP/FreeRDP/blob/b8beb55913471952f92770c90c372139d78c16c0/winpr/libwinpr/utils/trio/trio.c#L2756">View on GitHub!</a></p>
<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="cm">/* winpr/libwinpr/utils/trio/trio.c */</span>

<span class="n">TRIO_PRIVATE</span> <span class="kt">void</span> <span class="n">TrioWriteString</span> <span class="nf">TRIO_ARGS5</span><span class="p">((</span><span class="n">self</span><span class="p">,</span> <span class="n">string</span><span class="p">,</span> <span class="n">flags</span><span class="p">,</span> <span class="n">width</span><span class="p">,</span> <span class="n">precision</span><span class="p">),</span> <span class="n">trio_class_t</span><span class="o">*</span> <span class="n">self</span><span class="p">,</span> <span class="n">TRIO_CONST</span> <span class="kt">char</span><span class="o">*</span> <span class="n">string</span><span class="p">,</span> <span class="n">trio_flags_t</span> <span class="n">flags</span><span class="p">,</span> <span class="kt">int</span> <span class="n">width</span><span class="p">,</span> <span class="kt">int</span> <span class="n">precision</span><span class="p">)</span>
<span class="p">...</span>
<span class="n">length</span> <span class="o">=</span> <span class="n">trio_length_max</span><span class="p">(</span><span class="n">string</span><span class="p">,</span> <span class="n">precision</span><span class="p">);</span> <span class="c1">// precision = -1</span>
<span class="p">...</span>
</code></pre></div></div>

<p><a href="https://github.com/FreeRDP/FreeRDP/blob/b8beb55913471952f92770c90c372139d78c16c0/winpr/libwinpr/utils/trio/triostr.c#L345">View on GitHub!</a></p>
<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="cm">/* winpr/libwinpr/utils/trio/triostr.c */</span>

<span class="n">TRIO_PUBLIC_STRING</span> <span class="kt">size_t</span> <span class="n">trio_length_max</span> <span class="nf">TRIO_ARGS2</span><span class="p">((</span><span class="n">string</span><span class="p">,</span> <span class="n">max</span><span class="p">),</span> <span class="n">TRIO_CONST</span> <span class="kt">char</span><span class="o">*</span> <span class="n">string</span><span class="p">,</span> <span class="kt">size_t</span> <span class="n">max</span><span class="p">)</span> <span class="c1">// max = 18446744073709551615</span>
<span class="p">{</span>
	<span class="kt">size_t</span> <span class="n">i</span><span class="p">;</span>

	<span class="k">for</span> <span class="p">(</span><span class="n">i</span> <span class="o">=</span> <span class="mi">0</span><span class="p">;</span> <span class="n">i</span> <span class="o">&lt;</span> <span class="n">max</span><span class="p">;</span> <span class="o">++</span><span class="n">i</span><span class="p">)</span>
	<span class="p">{</span>
		<span class="k">if</span> <span class="p">(</span><span class="n">string</span><span class="p">[</span><span class="n">i</span><span class="p">]</span> <span class="o">==</span> <span class="mi">0</span><span class="p">)</span>
			<span class="k">break</span><span class="p">;</span>
	<span class="p">}</span>
	<span class="k">return</span> <span class="n">i</span><span class="p">;</span>
<span class="p">}</span>

</code></pre></div></div>

<h3 id="impact">Impact</h3>

<p>This issue may lead to Out-of-Bounds read.</p>

<h2 id="cve">CVE</h2>

<ul>
  <li>CVE-2020-4030</li>
</ul>

<h2 id="coordinated-disclosure-timeline">Coordinated Disclosure Timeline</h2>

<p>This report was subject to the GHSL <a href="https://securitylab.github.com/advisories/#policy">coordinated disclosure policy</a>.</p>

<ul>
  <li>05/25/2020: Report sent to Vendor</li>
  <li>05/26/2020: Vendor acknowledges report</li>
  <li>06/22/2020: Patch published</li>
</ul>

<h2 id="supporting-resources">Supporting Resources</h2>

<ul>
  <li>https://github.com/FreeRDP/FreeRDP/security/advisories/GHSA-fjr5-97f5-qq98</li>
  <li>https://github.com/FreeRDP/FreeRDP/commit/05cd9ea2290d23931f615c1b004d4b2e69074e27</li>
</ul>

<h2 id="credit">Credit</h2>

<p>This issue was discovered and reported by GHSL team member <a href="https://github.com/antonio-morales">@antonio-morales (Antonio Morales)</a>.</p>

<h2 id="contact">Contact</h2>

<p>You can contact the GHSL team at <code class="language-plaintext highlighter-rouge">securitylab@github.com</code>, please include the <code class="language-plaintext highlighter-rouge">GHSL-2020-106</code> in any communication regarding this issue.</p>

    