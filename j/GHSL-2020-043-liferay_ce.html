<header class="post-header d-block mb-6">
      <div class="date text-mono f5 my-3">July 15, 2020</div>
      <h1 class="my-2 h00-mktg lh-condensed">GHSL-2020-043: Server-side template injection in Liferay - CVE-2020-13445</h1>

      
      
      
      
      

      

      <a target="_blank" class="sc-frDJqD SgxRc d-inline-flex flex-row flex-items-center text-gray" href="https://github.com/pwntester">
        <img class="mr-3" src="https://avatars.githubusercontent.com/u/125701?s=35" height="35" width="35">
        <span>Alvaro Munoz</span>
      </a>
    </header>

    <main id="content" class="markdown-body" aria-label="Content">
      <h2 id="summary">Summary</h2>

<p>A user with privileges to edit FreeMarker or Velocity templates may execute arbitrary Java code or run arbitrary system commands with the same privileges as the account running Liferay.</p>

<p>Note: The follwing sandbox escape techniques have been tested on Liferay Portal WebContent templates and Liferay Portal Dynamic Data List Display templates, but it should work on other FreeMarker/Velocity templates used across all Liferay products (eg: DXP, Commerce, etc.)</p>

<h2 id="product">Product</h2>

<p>Liferay Portal CE</p>

<h2 id="tested-version">Tested Version</h2>

<p>Liferay Portal CE, version 7.3 GA1</p>

<h2 id="details">Details</h2>

<h3 id="server-side-template-injection-freemarker">Server-Side Template Injection (FreeMarker)</h3>

<p>Even though Liferay does a good job extending the FreeMarker sandbox with a custom ObjectWrapper (<code class="language-plaintext highlighter-rouge">com.liferay.portal.template.freemarker.internal.RestrictedLiferayObjectWrapper.java</code>) which enhances which objects can be accessed from a Template, and also disables insecure defaults such as the <code class="language-plaintext highlighter-rouge">?new</code> built-in to prevent instantiation of arbitrary classes, it stills exposes a number of objects through the Templating API that can be used to circumvent the sandbox and achieve remote code execution.</p>

<p>Deep inspection of the exposed objects’ object graph allows an attacker to get access to objects that allow them to instantiate arbitrary Java objects.</p>

<h3 id="server-side-template-injection-velocity">Server-Side Template Injection (Velocity)</h3>
<p>Liferay also uses Velocity templates for Dynamic Data Lists Display. We can use similar vectors on Velocity templates.</p>

<h3 id="impact">Impact</h3>

<p>This issue may lead to <code class="language-plaintext highlighter-rouge">Remote Code Execution</code>.</p>

<h2 id="cve">CVE</h2>

<p>CVE-2020-13445</p>

<h2 id="coordinated-disclosure-timeline">Coordinated Disclosure Timeline</h2>
<p>This report was subject to the GHSL <a href="https://securitylab.github.com/advisories/#policy">coordinated disclosure policy</a>.</p>

<ul>
  <li>03/23/2020: Sent report to security@liferay.com</li>
  <li>03/25/2020: Issue is acknowledged</li>
  <li>05/27/2020: Fix is released as part of Liferay Portal 7.3.2</li>
</ul>

<h2 id="credit">Credit</h2>

<p>This issue was discovered and reported by GHSL team member <a href="https://github.com/pwntester">@pwntester (Alvaro Munoz)</a>.</p>

<h2 id="contact">Contact</h2>

<p>You can contact the GHSL team at <code class="language-plaintext highlighter-rouge">securitylab@github.com</code>, please include a reference to <code class="language-plaintext highlighter-rouge">GHSL-2020-043</code> in any communication regarding this issue.</p>

  