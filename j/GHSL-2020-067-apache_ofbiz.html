<header class="post-header d-block mb-6">
      <div class="date text-mono f5 my-3">January 26, 2021</div>
      <h1 class="my-2 h00-mktg lh-condensed">GHSL-2020-067: Server-Side Template Injection (SSTI) leading to Remote Code Execution (RCE) in Apache OfBiz</h1>

      
      
      
      
      

      

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

<h3 id="server-side-template-injection-on-renderlookupfield">Server-Side Template Injection on <code class="language-plaintext highlighter-rouge">renderLookupField</code></h3>

<p>Untrusted data flows from <a href="https://github.com/apache/ofbiz-framework/blob/trunk/framework/widget/src/main/java/org/apache/ofbiz/widget/renderer/macro/MacroFormRenderer.java#L2291"><code class="language-plaintext highlighter-rouge">request.getParameter("_LAST_VIEW_NAME_")</code></a> to a <a href="https://github.com/apache/ofbiz-framework/blob/trunk/framework/widget/src/main/java/org/apache/ofbiz/widget/renderer/macro/MacroFormRenderer.java#L2364">FreeMarker macro call definition</a>. An attacker with privileges to render any page containing a lookup field will be able to execute arbitrary system commands by sending a payload such as:</p>

<div class="language-plaintext highlighter-rouge"><div class="highlight"><pre class="highlight"><code>https://localhost:8443/ordermgr/control/FindQuote?_LAST_VIEW_NAME_=%22%2F%3E%24%7B%22freemarker.template.utility.Execute%22%3Fnew%28%29%28%22id%22%29%7D%3CFOO
</code></pre></div></div>

<p>Note that lookup fields are used in multiple modules of the backend application and they require different permissions.</p>

<h4 id="impact">Impact</h4>

<p>This issue leads to <code class="language-plaintext highlighter-rouge">Remote Code Execution</code></p>

<h2 id="cve">CVE</h2>
<p>Not assigned</p>

<h2 id="credit">Credit</h2>

<p>This issue was discovered and reported by GHSL team member <a href="https://github.com/pwntester">@pwntester (Alvaro Muñoz)</a>.</p>

<h2 id="contact">Contact</h2>

<p>You can contact the GHSL team at <code class="language-plaintext highlighter-rouge">securitylab@github.com</code>, please include the <code class="language-plaintext highlighter-rouge">GHSL-2020-067</code> in any communication regarding this issue.</p>

   