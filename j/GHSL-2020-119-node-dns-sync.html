<header class="post-header d-block mb-6">
      <div class="date text-mono f5 my-3">June 17, 2020</div>
      <h1 class="my-2 h00-mktg lh-condensed">GHSL-2020-119: command injection vulnerability in node-dns-sync resolve method - CVE-2020-11079</h1>

      
      
      
      
      

      

      <a target="_blank" class="sc-frDJqD SgxRc d-inline-flex flex-row flex-items-center text-gray" href="https://github.com/kevinbackhouse">
        <img class="mr-3" src="https://avatars.githubusercontent.com/u/4358136?s=35" height="35" width="35">
        <span>Kevin Backhouse</span>
      </a>
    </header>

    <main id="content" class="markdown-body" aria-label="Content">
      <h2 id="summary">Summary</h2>

<p>The <code class="language-plaintext highlighter-rouge">resolve</code> method of the <a href="https://github.com/skoranga/node-dns-sync">node-dns-sync library</a> had a command injection vulnerability. Clients of the node-dns-sync library are unlikely to be aware of this, so they might unwittingly write code that contains a command injection vulnerability. This issue was resolved in version 0.2.1.</p>

<h2 id="product">Product</h2>

<p>node-dns-sync</p>

<h2 id="tested-version">Tested Version</h2>

<p>Commit <a href="https://github.com/skoranga/node-dns-sync/tree/93b8034e9475ae65102dac15fffe065616fede1b">93b8034</a></p>

<h2 id="details-command-injection-in-resolve">Details: Command injection in <code class="language-plaintext highlighter-rouge">resolve</code></h2>

<p>Node-dns-sync’s <code class="language-plaintext highlighter-rouge">resolve</code> method did not sufficiently sanitize user supplied input, which allowed for arbitrary shell command injection.</p>

<p>For example:</p>

<div class="language-plaintext highlighter-rouge"><div class="highlight"><pre class="highlight"><code>var dnsSync = require('dns-sync');
dnsSync.resolve('www.paypal.com', " &amp;&amp; touch exploit")
</code></pre></div></div>

<p>Would result in the <code class="language-plaintext highlighter-rouge">touch exploit</code> shell command being run on the system invoking the method.</p>

<h3 id="impact">Impact</h3>

<p>This issue may lead to remote code execution if a client of the library calls the vulnerable method with untrusted input.</p>

<h2 id="cves">CVEs</h2>

<ul>
  <li>CVE-2020-11079</li>
</ul>

<h2 id="coordinated-disclosure-timeline">Coordinated Disclosure Timeline</h2>

<p>This report was subject to the GHSL <a href="https://securitylab.github.com/advisories/#policy">coordinated disclosure policy</a>.</p>

<ul>
  <li>2020-05-19: Reported to maintainer</li>
  <li>2020-05-20: <a href="https://github.com/skoranga/node-dns-sync/pull/8">Pull request</a></li>
  <li>2020-05-20: Maintainer requests CVE through GHSA: https://github.com/skoranga/node-dns-sync/security/advisories/GHSA-wh69-wc6q-7888</li>
</ul>

<h2 id="resources">Resources</h2>

<ul>
  <li>https://github.com/skoranga/node-dns-sync/security/advisories/GHSA-wh69-wc6q-7888</li>
</ul>

<p>This vulnerability is similar to command injection vulnerabilities that have been found in other Javascript libraries. Here are some examples:</p>

<p><a href="https://github.com/advisories/GHSA-m8xj-5v73-3hh8">CVE-2020-7646</a>,
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

<p>We have written a <a href="https://codeql.com">CodeQL</a> query, which automatically detects this vulnerability. You can see the results of the query on the node-dns-sync project <a href="https://lgtm.com/query/7534921166252811038/">here</a>.</p>

<h2 id="credit">Credit</h2>

<p>This issue was discovered and reported by GitHub Engineer <a href="https://github.com/erik-krogh">@erik-krogh (Erik Krogh Kristensen)</a>.</p>

<h2 id="contact">Contact</h2>

<p>You can contact the GHSL team at <code class="language-plaintext highlighter-rouge">securitylab@github.com</code>, please include <code class="language-plaintext highlighter-rouge">GHSL-2020-119</code> in any communication regarding this issue.</p>

  