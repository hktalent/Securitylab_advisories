<header class="post-header d-block mb-6">
      <div class="date text-mono f5 my-3">August 26, 2020</div>
      <h1 class="my-2 h00-mktg lh-condensed">GHSL-2020-095 : Monster in the middle attack in em-imap - CVE-2020-13163</h1>

      
      
      
      
      

      

      <a target="_blank" class="sc-frDJqD SgxRc d-inline-flex flex-row flex-items-center text-gray" href="https://github.com/agustingianni">
        <img class="mr-3" src="https://avatars.githubusercontent.com/u/102623?s=35" height="35" width="35">
        <span>Agustin Gianni</span>
      </a>
    </header>

    <main id="content" class="markdown-body" aria-label="Content">
      <h2 id="summary">Summary</h2>

<p>Missing hostname validation allows an attacker to perform a monster in the middle attack against users of the library.</p>

<h2 id="product">Product</h2>

<p>em-imap</p>

<h2 id="tested-version">Tested Version</h2>

<p>v0.5</p>

<h2 id="details">Details</h2>

<h3 id="missing-ssltls-certificate-hostname-validation">Missing SSL/TLS certificate hostname validation</h3>

<p><a href="https://github.com/ConradIrwin/em-imap">em-imap</a> uses the library <a href="https://github.com/eventmachine/eventmachine">eventmachine</a> in an insecure way that allows an attacker to perform a monster in the middle attack against users of the library.</p>

<h4 id="impact">Impact</h4>

<p>An attacker can assume the identity of a trusted server and introduce malicious data in an otherwise trusted place.</p>

<h4 id="remediation">Remediation</h4>

<p>Implement hostname validation.</p>

<h4 id="references">References</h4>

<p><a href="https://cwe.mitre.org/data/definitions/297.html">CWE-297: Improper Validation of Certificate with Host Mismatch</a></p>

<h2 id="cve">CVE</h2>

<p>CVE-2020-13163</p>

<h2 id="timeline">Timeline</h2>
<ul>
  <li>18/05/2020: Report sent to Vendor</li>
  <li>18/05/2020: Vendor acknowledged report</li>
  <li>19/05/2020: Report published to public</li>
</ul>

<h2 id="resources">Resources</h2>
<ul>
  <li><a href="https://github.com/ConradIrwin/em-imap/issues/25">ConradIrwin/em-imap#25</a></li>
</ul>

<h2 id="credit">Credit</h2>

<p>This issue was discovered and reported by GHSL team member <a href="https://github.com/agustingianni">@agustingianni (Agustin Gianni)</a>.</p>

<h2 id="contact">Contact</h2>

<p>You can contact the GHSL team at <code class="language-plaintext highlighter-rouge">securitylab@github.com</code>, please include the <code class="language-plaintext highlighter-rouge">GHSL-2020-095</code> in any communication regarding this issue.</p>

    