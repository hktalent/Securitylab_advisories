<header class="post-header d-block mb-6">
      <div class="date text-mono f5 my-3">July 27, 2020</div>
      <h1 class="my-2 h00-mktg lh-condensed">GHSL-2020-071: Server-side template injection in Lithium CMS</h1>

      
      
      
      
      

      

      <a target="_blank" class="sc-frDJqD SgxRc d-inline-flex flex-row flex-items-center text-gray" href="https://github.com/pwntester">
        <img class="mr-3" src="https://avatars.githubusercontent.com/u/125701?s=35" height="35" width="35">
        <span>Alvaro Munoz</span>
      </a>
    </header>

    <main id="content" class="markdown-body" aria-label="Content">
      <h2 id="summary">Summary</h2>

<p>A user with privileges to edit a FreeMarker template (e.g. a Component) may execute arbitrary Java code or run arbitrary system commands with the same privileges as the account running Lithium CMS.</p>

<h2 id="product">Product</h2>

<p>Lithium CMS</p>

<h2 id="tested-version">Tested Version</h2>

<p>Latest</p>

<h2 id="details">Details</h2>

<h3 id="server-side-template-injection">Server-Side Template Injection</h3>

<p>Even though Lithium CMS does a good job limiting what objects are available to FreeMarker templates and always wraps them with <code class="language-plaintext highlighter-rouge">TemplateModel</code>s, it is still possible to bypass the FreeMarker sandbox. Deep inspection of the exposed objects’ object graph allows an attacker to get access to objects that allow them to instantiate arbitrary Java objects. In particular:</p>

<div class="language-plaintext highlighter-rouge"><div class="highlight"><pre class="highlight"><code>${http.class.protectionDomain.classLoader}
</code></pre></div></div>

<p>Will return an instance of <code class="language-plaintext highlighter-rouge">sun.misc.Launcher$AppClassLoader</code>. Having access to a ClassLoader we can load arbitrary classes since FreeMarker <a href="https://github.com/apache/freemarker/blob/2.3-gae/src/main/resources/freemarker/ext/beans/unsafeMethods.properties">list of unsafe methods</a> does not disallow <code class="language-plaintext highlighter-rouge">ClassLoader.loadClass()</code>. However, FreeMarker’s deny list does disallow invoking <code class="language-plaintext highlighter-rouge">newInstance()</code> on both <code class="language-plaintext highlighter-rouge">java.lang.Class</code> and <code class="language-plaintext highlighter-rouge">java.lang.reflect.Constructor</code>, so there is no way for an attacker to instantiate arbitrary objects.</p>

<p>Even though FreeMarker also disallows setter methods on <code class="language-plaintext highlighter-rouge">java.lang.reflect.Field</code>, it does not forbid getter ones. We can use this gap in the blocklist to get <code class="language-plaintext highlighter-rouge">public</code>, <code class="language-plaintext highlighter-rouge">static</code> fields from any class which can be used to instantiate arbitrary objects.</p>

<h4 id="impact">Impact</h4>

<p>This issue leads to <code class="language-plaintext highlighter-rouge">Remote Code Execution</code>.</p>

<h2 id="coordinated-disclosure-timeline">Coordinated Disclosure Timeline</h2>
<p>This report was subject to the GHSL <a href="https://securitylab.github.com/advisories/#policy">coordinated disclosure policy</a>.</p>
<ul>
  <li>04/15/2020: Report sent to vendor</li>
  <li>05/13/2020: Issue is fixed on all production systems (version 20.5)</li>
</ul>

<h2 id="credit">Credit</h2>

<p>This issue was discovered and reported by GHSL team member <a href="https://github.com/pwntester">@pwntester (Alvaro Munoz)</a>.</p>

<h2 id="contact">Contact</h2>

<p>You can contact the GHSL team at <code class="language-plaintext highlighter-rouge">securitylab@github.com</code>, please include a reference to <code class="language-plaintext highlighter-rouge">GHSL-2020-071</code> in any communication regarding this issue.</p>

