<header class="post-header d-block mb-6">
      <div class="date text-mono f5 my-3">August 12, 2020</div>
      <h1 class="my-2 h00-mktg lh-condensed">GHSL-2020-069: Unsafe deserialization of XMLRPC arguments in ApacheOfBiz - CVE-2020-9496</h1>

      
      
      
      
      

      

      <a target="_blank" class="sc-frDJqD SgxRc d-inline-flex flex-row flex-items-center text-gray" href="https://github.com/pwntester">
        <img class="mr-3" src="https://avatars.githubusercontent.com/u/125701?s=35" height="35" width="35">
        <span>Alvaro Munoz</span>
      </a>
    </header>

    <main id="content" class="markdown-body" aria-label="Content">
      <h2 id="summary">Summary</h2>
<p>Apache OfBiz is vulnerable to pre-auth Remote Code Execution (RCE) via unsafe deserialization.</p>

<h2 id="product">Product</h2>
<p>Apache Ofbiz</p>

<h2 id="tested-version">Tested Version</h2>
<p>17.12.01</p>

<h2 id="details">Details</h2>

<h3 id="unsafe-deserialization-of-xmlrpc-arguments">Unsafe deserialization of XMLRPC arguments</h3>

<p>OfBiz exposes an <code class="language-plaintext highlighter-rouge">XMLRPC</code> endpoint at <code class="language-plaintext highlighter-rouge">/webtools/control/xmlrpc</code>. This is an unauthenticated endpoint since authentication is applied on a per-service basis. However, the <code class="language-plaintext highlighter-rouge">XMLRPC</code> request is processed before authentication. As part of this processing, any serialized arguments for the remote invocation are deserialized, therefore if the classpath contains any classes that can be used as gadgets to achieve remote code execution, an attacker will be able to run arbitrary system commands on any OfBiz server with same privileges as the servlet container running OfBiz.</p>

<h4 id="impact">Impact</h4>

<p>This issue leads to pre-auth <code class="language-plaintext highlighter-rouge">Remote Code Execution</code></p>

<h2 id="cve">CVE</h2>
<ul>
  <li>CVE-2020-9496</li>
</ul>

<h2 id="coordinated-disclosure-timeline">Coordinated Disclosure Timeline</h2>
<ul>
  <li>04/13/2020: Report sent to vendor.</li>
  <li>04/23/2020: OfBiz maintainer acknowledges the issue.</li>
  <li>07/13/2020: Issue fixed <a href="https://ofbiz.apache.org/release-notes-17.12.04.html">Release note</a></li>
</ul>

<h2 id="credit">Credit</h2>

<p>This issue was discovered and reported by GHSL team member <a href="https://github.com/pwntester">@pwntester (Alvaro Muñoz)</a>.</p>

<h2 id="contact">Contact</h2>

<p>You can contact the GHSL team at <code class="language-plaintext highlighter-rouge">securitylab@github.com</code>, please include the <code class="language-plaintext highlighter-rouge">GHSL-2020-069</code> in any communication regarding this issue.</p>

   