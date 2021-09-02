<header class="post-header d-block mb-6">
      <div class="date text-mono f5 my-3">July 15, 2020</div>
      <h1 class="my-2 h00-mktg lh-condensed">GHSL-2020-039: Server-side template injection in Alfresco - CVE-2020-12873</h1>

      
      
      
      
      

      

      <a target="_blank" class="sc-frDJqD SgxRc d-inline-flex flex-row flex-items-center text-gray" href="https://github.com/pwntester">
        <img class="mr-3" src="https://avatars.githubusercontent.com/u/125701?s=35" height="35" width="35">
        <span>Alvaro Munoz</span>
      </a>
    </header>

    <main id="content" class="markdown-body" aria-label="Content">
      <h2 id="summary">Summary</h2>

<p>A user with privileges to edit a FreeMarker template (e.g. a webscript) may execute arbitrary Java code or run arbitrary system commands with the same privileges as the account running Alfresco.</p>

<h2 id="product">Product</h2>

<p>Alfresco Community</p>

<h2 id="tested-version">Tested Version</h2>

<p>Alfresco Community 6.2.0-GA (Released: 28 Nov, 2019)</p>

<h2 id="details">Details</h2>

<p>Even though Alfresco does a good job limiting what objects are available to FreeMarker templates, it is still possible to find objects which can be used to bypass the FreeMarker sandbox. Deep inspection of the exposed objects’ object graph allows an attacker to get access to objects that allow them to instantiate arbitrary Java objects.</p>

<h4 id="impact">Impact</h4>

<p>This issue may lead to <code class="language-plaintext highlighter-rouge">Remote Code Execution</code>.</p>

<h2 id="cve">CVE</h2>
<p>CVE-2020-12873</p>

<h2 id="coordinated-disclosure-timeline">Coordinated Disclosure Timeline</h2>
<p>This report was subject to the GHSL <a href="https://securitylab.github.com/advisories/#policy">coordinated disclosure policy</a>.</p>

<ul>
  <li>03/23/2020: Email sent to allreplies@alfresco.com to get security contact</li>
  <li>03/23/2020: Created <a href="https://issues.alfresco.com/jira/browse/ALF-22118">Jira issue</a> asking for security contact</li>
  <li>04/15/2020: Got an answser from allreplies@alfresco.com asking to report the issue to security@alfresco.com</li>
  <li>04/15/2020: Report sent to security@alfresco.com</li>
  <li>05/13/2020: Issue is fixed</li>
</ul>

<h2 id="credit">Credit</h2>

<p>This issue was discovered and reported by GHSL team member <a href="https://github.com/pwntester">@pwntester (Alvaro Munoz)</a>.</p>

<h2 id="contact">Contact</h2>

<p>You can contact the GHSL team at <code class="language-plaintext highlighter-rouge">securitylab@github.com</code>, please include a reference to <code class="language-plaintext highlighter-rouge">GHSL-2020-039</code> in any communication regarding this issue.</p>

  