>
    <header class="post-header d-block mb-6">
      <div class="date text-mono f5 my-3">November 2, 2020</div>
      <h1 class="my-2 h00-mktg lh-condensed">GHSL-2020-141: Arbitrary code execution in DatabaseSchemaReader - CVE-2020-26207</h1>

      
      
      
      
      

      

      <a target="_blank" class="sc-frDJqD SgxRc d-inline-flex flex-row flex-items-center text-gray" href="https://github.com/jarlob">
        <img class="mr-3" src="https://avatars.githubusercontent.com/u/26652396?s=35" height="35" width="35">
        <span>Jaroslav Lobacevski</span>
      </a>
    </header>

    <main id="content" class="markdown-body" aria-label="Content">
      <h2 id="summary">Summary</h2>

<p>DatabaseSchemaViewer is vulnerable to arbitrary code execution if a user is tricked into opening a specially crafted <code class="language-plaintext highlighter-rouge">.dbschema</code> file.</p>

<h2 id="product">Product</h2>

<p><a href="https://github.com/martinjw/dbschemareader">DatabaseSchemaReader</a></p>

<h2 id="tested-version">Tested Version</h2>

<p>Master branch.</p>

<h2 id="details">Details</h2>

<h3 id="issue-databaseschemareader-is-using-an-unsafe-serializer-to-open-dbschema-files">Issue: DatabaseSchemaReader is <a href="https://github.com/martinjw/dbschemareader/blob/9ee9a38be73ec375d23fae70eec2e7a1c30445ba/DatabaseSchemaViewer/Form1.cs#L527">using an unsafe serializer</a> to open <code class="language-plaintext highlighter-rouge">.dbschema</code> files.</h3>

<p>The user should be careful not to open <code class="language-plaintext highlighter-rouge">.dbschema</code> files from untrusted sources. See the Proof of Concept below.</p>

<h4 id="impact">Impact</h4>

<p>While the file is opened as data, any arbitrary code defined in the file is executed without user consent.</p>

<h4 id="remediation">Remediation</h4>

<p>Use a safer serializer, <code class="language-plaintext highlighter-rouge">XmlSerializer</code> for example, that performs expected type checks. See <a href="https://www.blackhat.com/docs/us-17/thursday/us-17-Munoz-Friday-The-13th-Json-Attacks.pdf">Alvaro and Oleksandr slides</a> for other safer serializer options.</p>

<h2 id="cve">CVE</h2>

<ul>
  <li>CVE-2020-26207</li>
</ul>

<h2 id="coordinated-disclosure-timeline">Coordinated Disclosure Timeline</h2>

<ul>
  <li>31/07/2020: Attempt to contact Vendor</li>
  <li>29/10/2020: Asked publicly for the security contact</li>
  <li>29/10/2020: Vendor acknowledges</li>
  <li>29/10/2020: The issue is remediated in v2.7.4.3</li>
  <li>30/10/2020: CVE-2020-26207 got assigned</li>
  <li>31/10/2020: <a href="https://github.com/martinjw/dbschemareader/security/advisories/GHSA-rfjh-m356-mpqf">Advisory</a> published</li>
</ul>

<h2 id="resources">Resources</h2>

<p><a href="https://github.com/github/securitylab-vulnerabilities/blob/main/vendor_reports/resources/GHSL-2020-141/evil.dbschema">PoC</a></p>

<h2 id="credit">Credit</h2>

<p>This issue was discovered and reported by GHSL team member <a href="https://github.com/JarLob">@JarLob (Jaroslav Lobačevski)</a>.</p>

<h2 id="contact">Contact</h2>

<p>You can contact the GHSL team at <code class="language-plaintext highlighter-rouge">securitylab@github.com</code>, please include a reference to <code class="language-plaintext highlighter-rouge">GHSL-2020-141</code> in any communication regarding this issue.</p