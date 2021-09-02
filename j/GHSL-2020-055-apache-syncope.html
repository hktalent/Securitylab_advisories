<header class="post-header d-block mb-6">
      <div class="date text-mono f5 my-3">May 11, 2020</div>
      <h1 class="my-2 h00-mktg lh-condensed">GHSL-2020-055: Server-Side Template Injection in Apache Syncope (RCE) - CVE-2019-17557</h1>

      
      
      
      
      

      

      <a target="_blank" class="sc-frDJqD SgxRc d-inline-flex flex-row flex-items-center text-gray" href="https://github.com/pwntester">
        <img class="mr-3" src="https://avatars.githubusercontent.com/u/125701?s=35" height="35" width="35">
        <span>Alvaro Munoz</span>
      </a>
    </header>

    <main id="content" class="markdown-body" aria-label="Content">
      <h2 id="summary">Summary</h2>

<p>A Server-Side Template Injection in the Mail templates was identified in Apache Syncope enabling attackers to inject arbitrary JEXL expressions, leading to a Remote Code Execution (RCE) vulnerability.</p>

<h2 id="product">Product</h2>

<p>Apache Syncope</p>

<h2 id="tested-version">Tested Version</h2>

<p>syncope-2.1.5</p>

<h2 id="details">Details</h2>

<h3 id="server-side-template-injection-on-mail-templates-ghsl-2020-055-cve-2019-1961">Server-Side Template Injection on Mail templates (GHSL-2020-055, CVE-2019-1961)</h3>

<p>Mail templates use JEXL expressions. Even though Syncope applies a Uberspector (<code class="language-plaintext highlighter-rouge">org.apache.syncope.core.provisioning.api.jexl.ClassFreeUberspect</code>) to prevent access to <code class="language-plaintext highlighter-rouge">java.lang.Object.getClass</code> and <code class="language-plaintext highlighter-rouge">java.lang.Object.class</code>, it is still possible to get a <code class="language-plaintext highlighter-rouge">Class</code> instance via other means. For example, an attacker could get a <code class="language-plaintext highlighter-rouge">Class</code> instance by accessing the <code class="language-plaintext highlighter-rouge">TYPE</code> field of boxed classes such as <code class="language-plaintext highlighter-rouge">Integer</code>, <code class="language-plaintext highlighter-rouge">Long</code>, <code class="language-plaintext highlighter-rouge">Boolean</code>, etc.</p>

<p>e.g.:</p>

<div class="language-plaintext highlighter-rouge"><div class="highlight"><pre class="highlight"><code>(1).TYPE
</code></pre></div></div>

<p>From there, an attacker could use Java reflection to instantiate arbitrary objects.</p>

<p>Note that since Core and EndUser are normally deployed with the same origin, a XSS issue allows an attacker to send such malicious requests by fooling the administrator into clicking a malicious link.</p>

<h4 id="impact">Impact</h4>

<p>This issue may lead to <code class="language-plaintext highlighter-rouge">Remote Code Execution</code></p>

<h4 id="remediation">Remediation</h4>

<p>Use the <a href="https://github.com/apache/commons-jexl/blob/master/src/main/java/org/apache/commons/jexl3/internal/introspection/SandboxUberspect.java">Sandboxed Uberspector</a> or customize a whitelist-based one.</p>

<p>This issue was addressed in the following <a href="https://github.com/apache/syncope/commit/def78270623d03a0c0086d22be410d7e0d765da3">commit</a></p>

<h2 id="cve">CVE</h2>

<ul>
  <li>CVE-2019-1961</li>
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

<p>You can contact the GHSL team at <code class="language-plaintext highlighter-rouge">securitylab@github.com</code>, please include the <code class="language-plaintext highlighter-rouge">GHSL-2020-055</code> in any communication regarding this issue.</p>

   