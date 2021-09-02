<header class="post-header d-block mb-6">
      <div class="date text-mono f5 my-3">May 11, 2020</div>
      <h1 class="my-2 h00-mktg lh-condensed">GHSL-2020-054: XSS in Apache Syncope - CVE-2020-1961</h1>

      
      
      
      
      

      

      <a target="_blank" class="sc-frDJqD SgxRc d-inline-flex flex-row flex-items-center text-gray" href="https://github.com/pwntester">
        <img class="mr-3" src="https://avatars.githubusercontent.com/u/125701?s=35" height="35" width="35">
        <span>Alvaro Munoz</span>
      </a>
    </header>

    <main id="content" class="markdown-body" aria-label="Content">
      <h2 id="summary">Summary</h2>

<p>An XSS issue in the EndUser login page was identified in Apache Syncope, combined with GHSL-2020-029 or GHSL-2020-055 this XSS may be escalated into RCE.</p>

<h2 id="product">Product</h2>

<p>Apache Syncope</p>

<h2 id="tested-version">Tested Version</h2>

<p>syncope-2.1.5</p>

<h2 id="details">Details</h2>

<h3 id="cross-site-scripting-on-enduser-login-page-ghsl-2020-054-cve-2020-17557">Cross-Site Scripting on EndUser login page (GHSL-2020-054, CVE-2020-17557)</h3>

<p>The EndUser login page reflects the <code class="language-plaintext highlighter-rouge">successMessage</code> parameters with some sanitization (app.js):</p>

<div class="language-plaintext highlighter-rouge"><div class="highlight"><pre class="highlight"><code>component.show(String(message).replace(/&lt;[^&gt;]+&gt;/gm, ''), "success");
</code></pre></div></div>

<p>However, this sanitization only accounts for closed tags. Unfortunately, most modern browsers will automatically close unclosed tags, thus enabling a bypass.</p>

<h4 id="impact">Impact</h4>

<p>Even though the XSS issue is on the login page, it will also trigger if the victim is already logged-in when clicking the malicious link. This is important because if different apps (enduser and core) have the same same origin (scheme+host+port), an attacker may use this XSS to attack a Syncope administrator and send arbitrary requests to the REST API. When mixed with GHSL-2020-029 or GHSL-2020-055, this would allow an attacker to escalate this XSS into RCE.</p>

<h4 id="remediation">Remediation</h4>

<p>Rather than trying to sanitize the user input, escape the <code class="language-plaintext highlighter-rouge">successMessage</code> parameter for HTML context.</p>

<p>This issue was addressed in the following <a href="https://github.com/apache/syncope/commit/23d7cf74b5a978673bc98043afebe48a60e2a78b">commit</a></p>

<h2 id="cve">CVE</h2>

<ul>
  <li>CVE-2020-17557</li>
</ul>

<h2 id="coordinated-disclosure-timeline">Coordinated Disclosure Timeline</h2>

<p>This report was subject to the GHSL <a href="https://securitylab.github.com/advisories/#policy">coordinated disclosure policy</a>.</p>

<ul>
  <li>04/01/2020: Report send to Apache</li>
  <li>04/02/2020: Issue acknowledged</li>
  <li>04/02/2020: Apache sends draft advisory</li>
  <li>05/11/2020: Public Advisory</li>
</ul>

<h2 id="resources">Resources</h2>

<ul>
  <li><a href="https://syncope.apache.org/security">Vendor Advisory</a></li>
</ul>

<h2 id="credit">Credit</h2>

<p>This issue was discovered and reported by GHSL team member <a href="https://github.com/pwntester">@pwntester (Alvaro Muñoz)</a>.</p>

<h2 id="contact">Contact</h2>

<p>You can contact the GHSL team at <code class="language-plaintext highlighter-rouge">securitylab@github.com</code>, please include the <code class="language-plaintext highlighter-rouge">GHSL-2020-054</code> in any communication regarding this issue.</p>

   