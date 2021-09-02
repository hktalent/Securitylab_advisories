<header class="post-header d-block mb-6">
      <div class="date text-mono f5 my-3">March 3, 2021</div>
      <h1 class="my-2 h00-mktg lh-condensed">GHSL-2020-048: Remote Code Execution in Apache Velocity - CVE-2020-13936</h1>

      
      
      
      
      

      

      <a target="_blank" class="sc-frDJqD SgxRc d-inline-flex flex-row flex-items-center text-gray" href="https://github.com/pwntester">
        <img class="mr-3" src="https://avatars.githubusercontent.com/u/125701?s=35" height="35" width="35">
        <span>Alvaro Munoz</span>
      </a>
    </header>

    <main id="content" class="markdown-body" aria-label="Content">
      <h2 id="coordinated-disclosure-timeline">Coordinated Disclosure Timeline</h2>
<ul>
  <li>03/23/2020: Sent report to security@apache.com</li>
  <li>03/24/2020: Received acknowledgement</li>
  <li>07/4/2020: Reported Uberspector bypass to Velocity security team</li>
  <li>07/15/2020: Received acknowledgement</li>
  <li>08/05/2020: <a href="https://github.com/apache/velocity-engine/pull/16/files">Public PR</a> containing the fix is submitted</li>
  <li>02/26/2021: <a href="https://github.com/apache/velocity-engine/pull/16">Fix</a> gets merged</li>
</ul>

<h2 id="summary">Summary</h2>

<ul>
  <li>Velocity Uberspector fails to prevent access to <code class="language-plaintext highlighter-rouge">java.lang.ClassLoader</code> methods.</li>
  <li>When Velocity templates are used in the context of a <a href="http://velocity.apache.org/tools/3.0/view.html">VelocityView</a> an attacker that is able to modify Template contents may execute arbitrary Java code or run arbitrary system commands with the same privileges as the account running the Servlet container.</li>
</ul>

<h2 id="product">Product</h2>

<p>Apache Velocity</p>

<h2 id="tested-version">Tested Version</h2>

<p>Apache Velocity 2.2</p>

<h2 id="details">Details</h2>

<h3 id="improper-blocklist-verification">Improper BlockList verification</h3>

<p>Velocity SecureUberspector prevents access to dangerous classes and packages by checking if any methods are invoked on the blocked classes. However Velocity fails to inspect the complete class hierarchy of the object where the method is invoked. This effectively means that if a method is called on an object of a given type that extends a class or implements an interface present in the BlockList, the invocation will not be blocked. As an example, the <code class="language-plaintext highlighter-rouge">java.lang.ClassLoader</code> abstract class is present in the Secure Uberspector default BlockList, however, as an abstract class, it cannot be instantiated, so any calls on a ClassLoader instance will happen to be in a class extending <code class="language-plaintext highlighter-rouge">java.lang.ClassLoader</code> which is not present in the BlockList.</p>

<p>For example, given the following template, the <code class="language-plaintext highlighter-rouge">ScriptEngineManager</code> class will be successfully loaded:</p>

<div class="language-plaintext highlighter-rouge"><div class="highlight"><pre class="highlight"><code>${request.servletContext.classLoader.loadClass("javax.script.ScriptEngineManager")}
</code></pre></div></div>

<h3 id="insufficient-sandbox-protection">Insufficient Sandbox Protection</h3>

<p>Even though Velocity offers a great sandbox that prevents dangerous methods from being invoked, exposing Servlet related objects (such as the Servlet context) may introduce a variaty of objects which can be used to bypass the Velocity sandbox. Deep inspection of the exposed objects’ object graph allows an attacker to get access to objects that allow them to instantiate arbitrary Java objects. According to the <a href="http://velocity.apache.org/tools/3.0/view.html">documentation</a>:</p>

<blockquote>
  <p>The HttpServletRequest, HttpSession, ServletContext, and their attributes are automatically available in your templates.</p>
</blockquote>

<p>There are different ways to access the Servlet context including:</p>
<ul>
  <li><code class="language-plaintext highlighter-rouge">$request.servletContext</code></li>
  <li><code class="language-plaintext highlighter-rouge">$application</code></li>
</ul>

<p>But if the application also exposes the context tool (which is the default), the Servlet context can also be accessed through:</p>

<ul>
  <li><code class="language-plaintext highlighter-rouge">$context.application</code></li>
  <li><code class="language-plaintext highlighter-rouge">$context.servletContext</code></li>
  <li><code class="language-plaintext highlighter-rouge">$context.request.servletContext</code></li>
</ul>

<p>On a Tomcat server the Servlet context will contain the <code class="language-plaintext highlighter-rouge">org.apache.tomcat.InstanceManager</code> which enables an attacker to instantiate arbitrary objects. Note that the same class (regardless of its name) is available on other servlet containers such as Jetty and similar classes are available in other servers. For example JBoss/WildFly exposes <code class="language-plaintext highlighter-rouge">org.wildfly.extension.undertow.deployment.UndertowJSPInstanceManage</code>.</p>

<p>We can then try to run arbitrary Java code using a <code class="language-plaintext highlighter-rouge">ScriptEngine</code>:</p>

<div class="language-plaintext highlighter-rouge"><div class="highlight"><pre class="highlight"><code>${req.getServletContext().getAttribute('org.apache.tomcat.InstanceManager').newInstance('javax.script.ScriptEngineManager').getEngineByName('js').eval("java.lang.Runtime.getRuntime().exec('touch /tmp/pwned')")}
</code></pre></div></div>

<p>In addition, on Spring applications a number of other Servlet context attributes may lead to remote code execution such as:</p>
<ul>
  <li>org.springframework.web.context.WebApplicationContext.ROOT</li>
  <li>org.springframework.web.servlet.FrameworkServlet.CONTEXT.dispatcherServlet</li>
  <li>org.springframework.web.context.support.ServletContextScope</li>
</ul>

<h4 id="impact">Impact</h4>

<p>This issue may lead to <code class="language-plaintext highlighter-rouge">Remote Code Execution</code>.</p>

<h2 id="cve">CVE</h2>
<p>CVE-2020-13936</p>

<h2 id="credit">Credit</h2>

<p>This issue was discovered and reported by GHSL team member <a href="https://github.com/pwntester">@pwntester (Alvaro Munoz)</a>.</p>

<h2 id="contact">Contact</h2>

<p>You can contact the GHSL team at <code class="language-plaintext highlighter-rouge">securitylab@github.com</code>, please include the <code class="language-plaintext highlighter-rouge">GHSL-2020-048</code> in any communication regarding this issue.</p>

  