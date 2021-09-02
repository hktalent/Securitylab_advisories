<header class="post-header d-block mb-6">
      <div class="date text-mono f5 my-3">April 3, 2020</div>
      <h1 class="my-2 h00-mktg lh-condensed">GHSL-2020-016: Persistent Cross-Site scripting in Nexus Repository Manager</h1>

      
      
      
      
      

      

      <a target="_blank" class="sc-frDJqD SgxRc d-inline-flex flex-row flex-items-center text-gray" href="https://github.com/pwntester">
        <img class="mr-3" src="https://avatars.githubusercontent.com/u/125701?s=35" height="35" width="35">
        <span>Alvaro Munoz</span>
      </a>
    </header>

    <main id="content" class="markdown-body" aria-label="Content">
      <h2 id="summary">Summary</h2>

<p>Persistent Cross—Site Scripting</p>

<h2 id="cve">CVE</h2>
<p>CVE-2020-10203</p>

<h2 id="product">Product</h2>
<p>Nexus Repository Manager</p>

<h2 id="tested-version">Tested Version</h2>
<p>3.20.1</p>

<h2 id="details">Details</h2>
<p>An attacker with elevated privileges can create content selectors with a specially crafted name using the REST API (not allowed by the UI) which when viewed by another user can execute arbitrary JavaScript in the context of the NXRM application.</p>

<h3 id="impact">Impact</h3>

<p>The identified vulnerability allows arbitrary JavaScript to run in an NXRM user’s browser in the context of the application.  In regards to XSS, it is common that the injected JavaScript could forge requests on behalf of the user, redirect the user to another site or modify the page content.</p>

<h3 id="remediation">Remediation</h3>

<p>Escape content selector names when rendered by the front-end</p>

<h2 id="coordinated-disclosure-timeline">Coordinated Disclosure Timeline</h2>
<ul>
  <li>02/03/2020: Report sent to Vendor</li>
  <li>02/03/2020: Sonatype acknowledged report</li>
  <li>02/14/2020: Sonatype raises questions about some of the issues</li>
  <li>02/17/2020: GHSL answers Sonatype questions</li>
  <li>02/19/2020: Sonatype agrees with GHSL comments</li>
</ul>

<h2 id="vendor-advisories">Vendor advisories</h2>
<p><a href="https://support.sonatype.com/hc/en-us/articles/360044361594-CVE-2020-10203-Nexus-Repository-Manager-3-Cross-Site-Scripting-XSS-2020-03-31">CVE-2020-10203 Nexus Repository Manager 3 - Cross Site Scripting XSS - 2020-03-31</a></p>

<h2 id="credit">Credit</h2>

<p>This issue was discovered and reported by GHSL team member <a href="https://github.com/pwntester">@pwntester (Alvaro Muñoz)</a>.</p>

<h2 id="contact">Contact</h2>

<p>You can contact the GHSL team at <code class="language-plaintext highlighter-rouge">securitylab@github.com</code>, please include the <code class="language-plaintext highlighter-rouge">GHSL-2020-016</code> in any communication regarding this issue.</p>
