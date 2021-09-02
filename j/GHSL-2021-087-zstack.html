<header class="post-header d-block mb-6">
      <div class="date text-mono f5 my-3">August 30, 2021</div>
      <h1 class="my-2 h00-mktg lh-condensed">GHSL-2021-087: Pre-auth unsafe deserialization in ZStack - CVE-2021-32836</h1>

      
      
      
      
      

      

      <a target="_blank" class="sc-frDJqD SgxRc d-inline-flex flex-row flex-items-center text-gray" href="https://github.com/pwntester">
        <img class="mr-3" src="https://avatars.githubusercontent.com/u/125701?s=35" height="35" width="35">
        <span>Alvaro Munoz</span>
      </a>
    </header>

    <main id="content" class="markdown-body" aria-label="Content">
      
<h2 id="coordinated-disclosure-timeline">Coordinated Disclosure Timeline</h2>
<ul>
  <li>2021-06-04: Details reported to maintainers using private GHSA</li>
  <li>2021-07-30: Issue is fixed and <a href="https://github.com/zstackio/zstack/security/advisories/GHSA-jfvq-548h-342x">advisory is published</a></li>
</ul>

<h2 id="summary">Summary</h2>
<p>ZStack REST API is vulnerable to pre-auth unsafe deserialization</p>

<h2 id="product">Product</h2>
<p>ZStack (https://en.zstack.io/)</p>

<h2 id="tested-version">Tested Version</h2>
<p>3.10.7-c76 (ZStack-x86_64-DVD-3.10.7-c76.iso)</p>

<h2 id="details">Details</h2>
<p>POST requests to the REST API (<code class="language-plaintext highlighter-rouge">/api</code>) are handled by the <a href="https://github.com/zstackio/zstack/blob/a5a2ade166fc46e70fec9474d4f435b12521f04f/core/src/main/java/org/zstack/core/rest/RESTApiController.java#L70"><code class="language-plaintext highlighter-rouge">RESTApiController</code></a>:</p>

<div class="language-java highlighter-rouge"><div class="highlight"><pre class="highlight"><code>    <span class="nd">@RequestMapping</span><span class="o">(</span><span class="n">value</span> <span class="o">=</span> <span class="nc">RESTConstant</span><span class="o">.</span><span class="na">REST_API_CALL</span><span class="o">,</span> <span class="n">method</span> <span class="o">=</span> <span class="o">{</span><span class="nc">RequestMethod</span><span class="o">.</span><span class="na">POST</span><span class="o">,</span> <span class="nc">RequestMethod</span><span class="o">.</span><span class="na">PUT</span><span class="o">})</span>
    <span class="kd">public</span> <span class="kt">void</span> <span class="nf">post</span><span class="o">(</span><span class="nc">HttpServletRequest</span> <span class="n">request</span><span class="o">,</span> <span class="nc">HttpServletResponse</span> <span class="n">response</span><span class="o">)</span> <span class="kd">throws</span> <span class="nc">IOException</span> <span class="o">{</span>
        <span class="nc">HttpEntity</span><span class="o">&lt;</span><span class="nc">String</span><span class="o">&gt;</span> <span class="n">entity</span> <span class="o">=</span> <span class="n">restf</span><span class="o">.</span><span class="na">httpServletRequestToHttpEntity</span><span class="o">(</span><span class="n">request</span><span class="o">);</span>
        <span class="k">try</span> <span class="o">{</span>
            <span class="nc">String</span> <span class="n">ret</span> <span class="o">=</span> <span class="n">handleByMessageType</span><span class="o">(</span><span class="n">entity</span><span class="o">.</span><span class="na">getBody</span><span class="o">());</span>
            <span class="n">response</span><span class="o">.</span><span class="na">setStatus</span><span class="o">(</span><span class="nc">HttpStatus</span><span class="o">.</span><span class="na">SC_OK</span><span class="o">);</span>
            <span class="n">response</span><span class="o">.</span><span class="na">setCharacterEncoding</span><span class="o">(</span><span class="s">"UTF-8"</span><span class="o">);</span>
            <span class="nc">PrintWriter</span> <span class="n">writer</span> <span class="o">=</span> <span class="n">response</span><span class="o">.</span><span class="na">getWriter</span><span class="o">();</span>
            <span class="n">writer</span><span class="o">.</span><span class="na">write</span><span class="o">(</span><span class="n">ret</span><span class="o">);</span>
        <span class="o">}</span> <span class="k">catch</span> <span class="o">(</span><span class="nc">Throwable</span> <span class="n">t</span><span class="o">)</span> <span class="o">{</span>
            <span class="nc">StringBuilder</span> <span class="n">sb</span> <span class="o">=</span> <span class="k">new</span> <span class="nc">StringBuilder</span><span class="o">(</span><span class="nc">String</span><span class="o">.</span><span class="na">format</span><span class="o">(</span><span class="s">"Error when calling %s"</span><span class="o">,</span> <span class="n">request</span><span class="o">.</span><span class="na">getRequestURI</span><span class="o">()));</span>
            <span class="n">sb</span><span class="o">.</span><span class="na">append</span><span class="o">(</span><span class="nc">String</span><span class="o">.</span><span class="na">format</span><span class="o">(</span><span class="s">"\nheaders: %s"</span><span class="o">,</span> <span class="n">entity</span><span class="o">.</span><span class="na">getHeaders</span><span class="o">().</span><span class="na">toString</span><span class="o">()));</span>
            <span class="n">sb</span><span class="o">.</span><span class="na">append</span><span class="o">(</span><span class="nc">String</span><span class="o">.</span><span class="na">format</span><span class="o">(</span><span class="s">"\nbody: %s"</span><span class="o">,</span> <span class="n">entity</span><span class="o">.</span><span class="na">getBody</span><span class="o">()));</span>
            <span class="n">sb</span><span class="o">.</span><span class="na">append</span><span class="o">(</span><span class="nc">String</span><span class="o">.</span><span class="na">format</span><span class="o">(</span><span class="s">"\nexception message: %s"</span><span class="o">,</span> <span class="n">t</span><span class="o">.</span><span class="na">getMessage</span><span class="o">()));</span>
            <span class="n">logger</span><span class="o">.</span><span class="na">debug</span><span class="o">(</span><span class="n">sb</span><span class="o">.</span><span class="na">toString</span><span class="o">(),</span> <span class="n">t</span><span class="o">);</span>
            <span class="n">response</span><span class="o">.</span><span class="na">sendError</span><span class="o">(</span><span class="nc">HttpStatus</span><span class="o">.</span><span class="na">SC_INTERNAL_SERVER_ERROR</span><span class="o">,</span> <span class="n">sb</span><span class="o">.</span><span class="na">toString</span><span class="o">());</span>
        <span class="o">}</span>
    <span class="o">}</span>

</code></pre></div></div>

<p>This controller delegates the request body processing to <a href="https://github.com/zstackio/zstack/blob/a5a2ade166fc46e70fec9474d4f435b12521f04f/core/src/main/java/org/zstack/core/rest/RESTApiController.java#L55"><code class="language-plaintext highlighter-rouge">RESTApiController.handleByMessageType()</code></a>:</p>

<div class="language-java highlighter-rouge"><div class="highlight"><pre class="highlight"><code>   <span class="kd">private</span> <span class="nc">String</span> <span class="nf">handleByMessageType</span><span class="o">(</span><span class="nc">String</span> <span class="n">body</span><span class="o">)</span> <span class="o">{</span>
        <span class="nc">APIMessage</span> <span class="n">amsg</span> <span class="o">=</span> <span class="kc">null</span><span class="o">;</span>
        <span class="k">try</span> <span class="o">{</span>
            <span class="n">amsg</span> <span class="o">=</span> <span class="o">(</span><span class="nc">APIMessage</span><span class="o">)</span> <span class="nc">RESTApiDecoder</span><span class="o">.</span><span class="na">loads</span><span class="o">(</span><span class="n">body</span><span class="o">);</span>
        <span class="o">}</span> <span class="k">catch</span> <span class="o">(</span><span class="nc">Throwable</span> <span class="n">t</span><span class="o">)</span> <span class="o">{</span>
            <span class="k">return</span> <span class="n">t</span><span class="o">.</span><span class="na">getMessage</span><span class="o">();</span>
        <span class="o">}</span>

        <span class="nc">RestAPIResponse</span> <span class="n">rsp</span> <span class="o">=</span> <span class="kc">null</span><span class="o">;</span>
        <span class="k">if</span> <span class="o">(</span><span class="n">amsg</span> <span class="k">instanceof</span> <span class="nc">APISyncCallMessage</span><span class="o">)</span> <span class="o">{</span>
            <span class="n">rsp</span> <span class="o">=</span> <span class="n">restApi</span><span class="o">.</span><span class="na">call</span><span class="o">(</span><span class="n">amsg</span><span class="o">);</span>
        <span class="o">}</span> <span class="k">else</span> <span class="o">{</span>
            <span class="n">rsp</span> <span class="o">=</span> <span class="n">restApi</span><span class="o">.</span><span class="na">send</span><span class="o">(</span><span class="n">amsg</span><span class="o">);</span>
        <span class="o">}</span>
        <span class="k">return</span> <span class="nc">JSONObjectUtil</span><span class="o">.</span><span class="na">toJsonString</span><span class="o">(</span><span class="n">rsp</span><span class="o">);</span>
    <span class="o">}</span>
</code></pre></div></div>

<p>The request body is then parsed by the <a href="https://github.com/zstackio/zstack/blob/a5a2ade166fc46e70fec9474d4f435b12521f04f/core/src/main/java/org/zstack/core/rest/RESTApiDecoder.java"><code class="language-plaintext highlighter-rouge">RESTApiDecoder.loads</code></a> method:</p>

<div class="language-java highlighter-rouge"><div class="highlight"><pre class="highlight"><code>    <span class="kd">public</span> <span class="kd">static</span> <span class="nc">Message</span> <span class="nf">loads</span><span class="o">(</span><span class="nc">String</span> <span class="n">jsonStr</span><span class="o">)</span> <span class="o">{</span>
        <span class="nc">Message</span> <span class="n">msg</span> <span class="o">=</span> <span class="n">self</span><span class="o">.</span><span class="na">gsonDecoder</span><span class="o">.</span><span class="na">fromJson</span><span class="o">(</span><span class="n">jsonStr</span><span class="o">,</span> <span class="nc">Message</span><span class="o">.</span><span class="na">class</span><span class="o">);</span>
        <span class="k">return</span> <span class="n">msg</span><span class="o">;</span>
    <span class="o">}</span>
</code></pre></div></div>

<p>Which in turn, uses the custom <a href="https://github.com/zstackio/zstack/blob/a5a2ade166fc46e70fec9474d4f435b12521f04f/core/src/main/java/org/zstack/core/rest/RESTApiDecoder.java#L68"><code class="language-plaintext highlighter-rouge">Message</code> deserializer</a> to deserialize the request body:</p>

<div class="language-java highlighter-rouge"><div class="highlight"><pre class="highlight"><code>        <span class="nd">@Override</span>
        <span class="kd">public</span> <span class="nc">Message</span> <span class="nf">deserialize</span><span class="o">(</span><span class="nc">JsonElement</span> <span class="n">json</span><span class="o">,</span> <span class="nc">Type</span> <span class="n">typeOfT</span><span class="o">,</span> <span class="nc">JsonDeserializationContext</span> <span class="n">context</span><span class="o">)</span> <span class="kd">throws</span> <span class="nc">JsonParseException</span> <span class="o">{</span>
            <span class="nc">JsonObject</span> <span class="n">jObj</span> <span class="o">=</span> <span class="n">json</span><span class="o">.</span><span class="na">getAsJsonObject</span><span class="o">();</span>
            <span class="nc">Map</span><span class="o">.</span><span class="na">Entry</span><span class="o">&lt;</span><span class="nc">String</span><span class="o">,</span> <span class="nc">JsonElement</span><span class="o">&gt;</span> <span class="n">entry</span> <span class="o">=</span> <span class="n">jObj</span><span class="o">.</span><span class="na">entrySet</span><span class="o">().</span><span class="na">iterator</span><span class="o">().</span><span class="na">next</span><span class="o">();</span>
            <span class="nc">String</span> <span class="n">className</span> <span class="o">=</span> <span class="n">entry</span><span class="o">.</span><span class="na">getKey</span><span class="o">();</span>
            <span class="nc">Class</span><span class="o">&lt;?&gt;</span> <span class="n">clazz</span><span class="o">;</span>
            <span class="k">try</span> <span class="o">{</span>
                <span class="n">clazz</span> <span class="o">=</span> <span class="nc">Class</span><span class="o">.</span><span class="na">forName</span><span class="o">(</span><span class="n">className</span><span class="o">);</span>
            <span class="o">}</span> <span class="k">catch</span> <span class="o">(</span><span class="nc">ClassNotFoundException</span> <span class="n">e</span><span class="o">)</span> <span class="o">{</span>
                <span class="k">throw</span> <span class="k">new</span> <span class="nf">JsonParseException</span><span class="o">(</span><span class="s">"Unable to deserialize class "</span> <span class="o">+</span> <span class="n">className</span><span class="o">,</span> <span class="n">e</span><span class="o">);</span>
            <span class="o">}</span>
            <span class="nc">Message</span> <span class="n">msg</span> <span class="o">=</span> <span class="o">(</span><span class="nc">Message</span><span class="o">)</span> <span class="k">this</span><span class="o">.</span><span class="na">gson</span><span class="o">.</span><span class="na">fromJson</span><span class="o">(</span><span class="n">entry</span><span class="o">.</span><span class="na">getValue</span><span class="o">(),</span> <span class="n">clazz</span><span class="o">);</span>
            <span class="k">return</span> <span class="n">msg</span><span class="o">;</span>
        <span class="o">}</span>
</code></pre></div></div>

<p>An attacker in control of the request body will be able to provide both the class name and the data to be deserialized and therefore will be able to instantiate an arbitrary type and assign arbitrary values to its fields. Even though GSON does not call any setters on the attacker-controlled object since it uses reflection to set the values of the fields, an attack is still possible if the attacker can find a class with a <code class="language-plaintext highlighter-rouge">finalize()</code> method that can cause harm. Examples of such classes are <a href="https://blog.oversecured.com/Exploiting-memory-corruption-vulnerabilities-on-Android/">memory corruption gadgets</a> or any other classes with undesired side-effects. As an example, an attacker could send the following request:</p>

<div class="language-http highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="err">POST http://192.168.78.132:8080/zstack/api
{'java.net.PlainDatagramSocketImpl': {'fd': {'fd': 0,'closed':false}}}
</span></code></pre></div></div>

<p>ZStack will use GSON to create an instance of <code class="language-plaintext highlighter-rouge">PlainDatagramSocketImpl</code> where the socket file descriptor is controlled by the attacker (in this case the STDIN (0) file descriptor). Even though the application will throw a <code class="language-plaintext highlighter-rouge">ClassCastException</code> when casting the deserialized object to <code class="language-plaintext highlighter-rouge">Message</code> class, the garbage collector will still claim the memory of the allocated <code class="language-plaintext highlighter-rouge">PlainDatagramSocketImpl</code> object and will call its <code class="language-plaintext highlighter-rouge">finalize()</code> method. As described <a href="https://www.contrastsecurity.com/security-influencers/serialization-must-die-act-1-kryo-serialization">here</a>, the <code class="language-plaintext highlighter-rouge">AbstractPlainDatagramSocketImpl.finalize()</code> method will use a native function to close the attacker-controlled file descriptor. This can be used by the attacker to perform a Denial of Service attack by being able to close all the file descriptors used by the process (using the vulnerability to close all file descriptors in the range 0..20 will most likely cause ZStack to crash).</p>

<h3 id="impact">Impact</h3>
<p>This issue may lead to a Denial Of Service. If a suitable gadget is available, then an attacker may also be able to exploit this vulnerability to gain pre-auth remote code execution.</p>

<h2 id="cve">CVE</h2>

<ul>
  <li>CVE-2021-32836</li>
</ul>

<h2 id="resources">Resources</h2>
<p><a href="https://github.com/zstackio/zstack/security/advisories/GHSA-jfvq-548h-342x">GitHub Security Advisory</a></p>

<h2 id="credit">Credit</h2>
<p>This issue was discovered and reported by GHSL team member <a href="https://github.com/pwntester">@pwntester (Alvaro Muñoz)</a>.</p>

<h2 id="contact">Contact</h2>
<p>You can contact the GHSL team at <code class="language-plaintext highlighter-rouge">securitylab@github.com</code>, please include a reference to <code class="language-plaintext highlighter-rouge">GHSL-2021-087</code> in any communication regarding this issue.</p>


   