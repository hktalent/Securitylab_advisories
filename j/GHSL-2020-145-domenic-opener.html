<header class="post-header d-block mb-6">
      <div class="date text-mono f5 my-3">September 16, 2020</div>
      <h1 class="my-2 h00-mktg lh-condensed">GHSL-2020-145: Command injection on Windows in Opener</h1>

      
      
      
      
      

      

      <a target="_blank" class="sc-frDJqD SgxRc d-inline-flex flex-row flex-items-center text-gray" href="https://github.com/ghsecuritylab">
        <img class="mr-3" src="https://avatars.githubusercontent.com/u/61799930?s=35" height="35" width="35">
        <span>GitHub Security Lab</span>
      </a>
    </header>

    <main id="content" class="markdown-body" aria-label="Content">
      <h2 id="summary">Summary</h2>

<p>A typical usage of Opener is to open a url such as <code class="language-plaintext highlighter-rouge">https://google.com</code>. Opener will launch a browser and open that page. It can also be used to execute commands such as <code class="language-plaintext highlighter-rouge">npm run lint</code>. Although code execution is part of the intended purpose of Opener, we believe it is a security issue if, for example, a crafted url can run an arbitrary shell command rather than just launching a browser.</p>

<p>On Windows, in contrast to other platforms such as MacOS and Linux, Opener uses a shell (<code class="language-plaintext highlighter-rouge">cmd.exe</code>) to open links. This creates a risk that an attacker can execute arbitrary shell commands.</p>

<h2 id="product">Product</h2>

<p>Opener</p>

<h2 id="tested-version">Tested Version</h2>

<p>1.5.1</p>

<h2 id="details">Details</h2>

<h3 id="issue-1-command-injection-on-windows">Issue 1: Command injection on Windows</h3>

<p><code class="language-plaintext highlighter-rouge">lib/opener.js</code> has logic for three platforms: Linux, MacOS, and Windows. On Linux and MacOS, Opener uses <code class="language-plaintext highlighter-rouge">xdg-open</code> and <code class="language-plaintext highlighter-rouge">open</code>, respectively, to open the url. Those programs are specifically designed for opening links. On Windows, however, Opener uses <code class="language-plaintext highlighter-rouge">cmd.exe</code> to open the link. That means that special characters in the argument list could lead to the execution of arbitrary shell commands. The code already contains logic to handle the <code class="language-plaintext highlighter-rouge">&amp;</code> character, but it does not handle the <code class="language-plaintext highlighter-rouge">^</code> character, which has a similar effect.</p>

<p>Below is example of how a client of the Opener library might unwittingly expose themselves to this vulnerability. The value of <code class="language-plaintext highlighter-rouge">${user}</code> is attacker-controlled in this example, but you would not expect that to enable an attacker to run arbitrary shell commands.</p>

<div class="language-plaintext highlighter-rouge"><div class="highlight"><pre class="highlight"><code>const opener = require("opener");
opener(`https://github.com/${user}`);
</code></pre></div></div>

<p>If <code class="language-plaintext highlighter-rouge">${user}</code> is the string <code class="language-plaintext highlighter-rouge">^&amp;calc</code>, then on Windows this code will open the (meaningless) url <code class="language-plaintext highlighter-rouge">https://github.com/%5E</code> in a browser and launch <code class="language-plaintext highlighter-rouge">calc.exe</code>.</p>

<h4 id="impact">Impact</h4>

<p>On Windows, this issue may lead to remote code execution if a client of the library calls the vulnerable method with untrusted input. Other platforms (MacOS, Linux) are not vulnerable.</p>

<h4 id="remediation">Remediation</h4>

<p>We recommend adding logic to also escape <code class="language-plaintext highlighter-rouge">^</code> characters, as follows:</p>

<div class="language-plaintext highlighter-rouge"><div class="highlight"><pre class="highlight"><code>index 5fa88f3..08888c6 100644
--- a/lib/opener.js
+++ b/lib/opener.js
@@ -55,9 +55,9 @@ module.exports = function opener(args, options, callback) {
         // Furthermore, if "cmd /c" double-quoted the first parameter, then "start" will interpret it as a window title,
         // so we need to add a dummy empty-string window title: http://stackoverflow.com/a/154090/3191
         //
-        // Additionally, on Windows ampersand needs to be escaped when passed to "start"
+        // Additionally, on Windows ampersand and caret need to be escaped when passed to "start"
         args = args.map(function (value) {
-            return value.replace(/&amp;/g, "^&amp;");
+            return value.replace(/[&amp;^]/g, "^$&amp;");
         });
         args = ["/c", "start", "\"\""].concat(args);
     }
</code></pre></div></div>

<h4 id="resources">Resources</h4>

<p>We have written a <a href="https://codeql.com">CodeQL</a> query, which automatically detects this vulnerability. You can see the results of the query on Opener <a href="https://lgtm.com/query/54630250874580024/">here</a>.</p>

<h2 id="coordinated-disclosure-timeline">Coordinated Disclosure Timeline</h2>
<p>2020-08-26: Report sent to d@domenic.me
2020-08-26: Rejected as not-a-security-issue by d@domenic.me
2020-08-27: Posted PR to fix the issue: https://github.com/domenic/opener/pull/34</p>

<h2 id="credit">Credit</h2>

<p>This issue was discovered by GitHub Engineer <a href="https://github.com/max-schaefer">@max-schaefer (Max Schaefer)</a>.</p>

<h2 id="contact">Contact</h2>

<p>You can contact the GHSL team at <code class="language-plaintext highlighter-rouge">securitylab@github.com</code>, please include a reference to <code class="language-plaintext highlighter-rouge">GHSL-2020-145</code> in any communication regarding this issue.</p>

    