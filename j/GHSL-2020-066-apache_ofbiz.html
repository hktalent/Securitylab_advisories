<header class="post-header d-block mb-6">
      <div class="date text-mono f5 my-3">January 26, 2021</div>
      <h1 class="my-2 h00-mktg lh-condensed">GHSL-2020-066: Server-Side Template Injection (SSTI) leading to Remote Code Execution (RCE) in Apache OfBiz</h1>

      
      
      
      
      

      

      <a target="_blank" class="sc-frDJqD SgxRc d-inline-flex flex-row flex-items-center text-gray" href="https://github.com/pwntester">
        <img class="mr-3" src="https://avatars.githubusercontent.com/u/125701?s=35" height="35" width="35">
        <span>Alvaro Munoz</span>
      </a>
    </header>

    <main id="content" class="markdown-body" aria-label="Content">
      <h2 id="coordinated-disclosure-timeline">Coordinated Disclosure Timeline</h2>
<ul>
  <li>04/13/2020: Report sent to vendor.</li>
  <li>04/23/2020: OfBiz maintainer acknowledges the issue.</li>
  <li>04/23/2020: As per Apache policy, no CVE will be issued for post-authentication vulnerabilities no matter if they are privilege escalations or XSS issues (including this one that can be triggered via XSS reported in GHSL-2020-068)</li>
  <li>01/10/2021: Addressed in 17.12.05</li>
</ul>

<h2 id="summary">Summary</h2>
<p>Apache OfBiz is vulnerable to Server-Side Template Injection (SSTI) leading to Remote Code Execution (RCE)</p>

<h2 id="product">Product</h2>
<p>Apache Ofbiz</p>

<h2 id="tested-version">Tested Version</h2>
<p>17.12.01</p>

<h2 id="details">Details</h2>

<h3 id="server-side-template-injection-on-rendersortfield">Server-Side Template Injection on <code class="language-plaintext highlighter-rouge">renderSortField</code></h3>

<p>A Server-Side Template Injection (SSTI) was reported back in 2016 which was assigned <a href="https://insinuator.net/2016/07/dilligent-bug/">CVE-2016-4462</a>.
The commited <a href="https://github.com/apache/ofbiz/commit/a44162e6701488e3bde60990c61316f3a3d054f1">fix</a> was two fold:</p>
<ul>
  <li><code class="language-plaintext highlighter-rouge">linkUrl = URLEncoder.encode(linkUrl, "UTF-8");</code></li>
  <li><code class="language-plaintext highlighter-rouge">sr.append("\" linkUrl=r\"");</code></li>
</ul>

<p>However, the second part of the fix was not effective, since the attacker can close the <code class="language-plaintext highlighter-rouge">raw string</code> context with a double quote and write a new attribute or even close the macro tag and write arbitrary FreeMarker code.</p>

<p>Unfortunately, the first part of the fix was removed at a <a href="https://github.com/apache/ofbiz/commit/865b17422104a0d1091c18e75cccf96fd8baad1d#diff-505d8fb1ede9a7ac8bb03b175bec4256">later stage</a> enabling the SSTI again and leaving OfBiz vulnerable to remote code execution (RCE).</p>

<p>The following link will execute the <code class="language-plaintext highlighter-rouge">id</code> command and print it along each sortable filed in the page:</p>

<div class="language-plaintext highlighter-rouge"><div class="highlight"><pre class="highlight"><code>https://localhost/ordermgr/control/FindRequest?foo=bar%22ajaxEnabled=false/%3E%24%7b%22freemarker%2etemplate%2eutility%2eExecute%22%3fnew%28%29%28%22id%22%29%7d%3CFOO
</code></pre></div></div>

<p>Note that sortable fields are used in multiple modules of the backend application and they require different permissions.</p>

<h4 id="impact">Impact</h4>

<p>This issue leads to <code class="language-plaintext highlighter-rouge">Remote Code Execution</code></p>

<h2 id="cve">CVE</h2>
<p>Not assigned</p>

<h2 id="resources">Resources</h2>
<p><a href="https://github.com/apache/ofbiz-framework/commit/cd242ea/">fix commit</a></p>

<h2 id="credit">Credit</h2>

<p>This issue was discovered and reported by GHSL team member <a href="https://github.com/pwntester">@pwntester (Alvaro Muñoz)</a>.</p>

<h2 id="contact">Contact</h2>

<p>You can contact the GHSL team at <code class="language-plaintext highlighter-rouge">securitylab@github.com</code>, please include the <code class="language-plaintext highlighter-rouge">GHSL-2020-066</code> in any communication regarding this issue.</p>

   