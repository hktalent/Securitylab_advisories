<header class="post-header d-block mb-6">
      <div class="date text-mono f5 my-3">July 22, 2020</div>
      <h1 class="my-2 h00-mktg lh-condensed">GHSL-2020-047: Server-side template injection in dotCMS</h1>

      
      
      
      
      

      

      <a target="_blank" class="sc-frDJqD SgxRc d-inline-flex flex-row flex-items-center text-gray" href="https://github.com/pwntester">
        <img class="mr-3" src="https://avatars.githubusercontent.com/u/125701?s=35" height="35" width="35">
        <span>Alvaro Munoz</span>
      </a>
    </header>

    <main id="content" class="markdown-body" aria-label="Content">
      <h2 id="summary">Summary</h2>

<p>A user with privileges to edit templates may execute arbitrary Java code or run arbitrary system commands with the same privileges as the account running dotCMS.</p>

<h2 id="product">Product</h2>

<p>dotCMS</p>

<h2 id="tested-version">Tested Version</h2>

<p>5.2.7 Release</p>

<h2 id="details">Details</h2>

<h3 id="server-side-template-injection-velocity">Server-Side Template Injection (Velocity)</h3>

<p>Even though dotCMS does a good job installing the Velocity SecureUberspector to sandbox the content templates, it stills exposes a number of objects through the Templating API that can be used to circumvent the sandbox and achieve remote code execution.</p>

<p>Deep inspection of the exposed objects’ object graph allows an attacker to get access to objects that allow them to instantiate arbitrary Java objects.</p>

<h3 id="impact">Impact</h3>

<p>This issue may lead to <code class="language-plaintext highlighter-rouge">Remote Code Execution</code>.</p>

<h2 id="coordinated-disclosure-timeline">Coordinated Disclosure Timeline</h2>
<p>This report was subject to the GHSL <a href="https://securitylab.github.com/advisories/#policy">coordinated disclosure policy</a>.</p>
<ul>
  <li>03/23/2020: Sent report to security@dotcms.com</li>
  <li>03/26/2020: Issue is acknowledged</li>
  <li>05/13/2020: Issue is fixed as part of the 5.3 release</li>
</ul>

<h2 id="credit">Credit</h2>

<p>This issue was discovered and reported by GHSL team member <a href="https://github.com/pwntester">@pwntester (Alvaro Munoz)</a>.</p>

<h2 id="contact">Contact</h2>

<p>You can contact the GHSL team at <code class="language-plaintext highlighter-rouge">securitylab@github.com</code>, please include a reference to <code class="language-plaintext highlighter-rouge">GHSL-2020-047</code> in any communication regarding this issue.</p>

  