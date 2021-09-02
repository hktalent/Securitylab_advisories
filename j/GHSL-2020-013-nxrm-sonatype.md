<header class="post-header d-block mb-6">
      <div class="date text-mono f5 my-3">April 13, 2020</div>
      <h1 class="my-2 h00-mktg lh-condensed">GHSL-2020-013: Remote Code Execution - Dynamic Code Evaluation via Scripts in Nexus Repository Manager</h1>

      
      
      
      
      

      

      <a target="_blank" class="sc-frDJqD SgxRc d-inline-flex flex-row flex-items-center text-gray" href="https://github.com/pwntester">
        <img class="mr-3" src="https://avatars.githubusercontent.com/u/125701?s=35" height="35" width="35">
        <span>Alvaro Munoz</span>
      </a>
    </header>

    <main id="content" class="markdown-body" aria-label="Content">
      <h2 id="summary">Summary</h2>
<p>GHSL-2020-013 - Remote Code execution - Dynamic Code Evaluation via Scripts</p>

<h2 id="product">Product</h2>
<p>Nexus Repository Manager</p>

<h2 id="tested-version">Tested Version</h2>
<p>3.20.1</p>

<h2 id="cve">CVE</h2>
<p>No CVE was assigned</p>

<h2 id="details">Details</h2>
<p>It is possible for a user with the right permissions to execute arbitrary groovy or javascript scripts resulting in remote code execution.</p>

<p>For example, an attacker can create a script by using the following endpoint:</p>

<p>Endpoint: <code class="language-plaintext highlighter-rouge">src/main/java/org/sonatype/nexus/script/plugin/internal/rest/ScriptResource.groovy</code>
Persmissions: <code class="language-plaintext highlighter-rouge">nx-script-*-add</code></p>

<p>And later execute the script using the following endpoint:</p>

<p>Endpoint: <code class="language-plaintext highlighter-rouge">src/main/java/org/sonatype/nexus/script/plugin/internal/rest/ScriptResource.groovy</code>
Permissions: <code class="language-plaintext highlighter-rouge">nx-script-*-run</code></p>

<h3 id="impact">Impact</h3>

<p>This issue may lead to Remote Code execution by high-privilege users</p>

<h2 id="coordinated-disclosure-timeline">Coordinated Disclosure Timeline</h2>
<ul>
  <li>02/03/2020: Report sent to Sonatype</li>
  <li>02/03/2020: Sonatype acknowledged report</li>
  <li>02/14/2020: Sonatype raises questions about some of the issues</li>
  <li>02/17/2020: GHSL answers Sonatype questions</li>
  <li>02/19/2020: Sonatype agrees with GHSL comments</li>
</ul>

<h2 id="credit">Credit</h2>

<p>This issue was discovered and reported by GHSL team member <a href="https://github.com/pwntester">@pwntester (Alvaro Muñoz)</a>.</p>

<h2 id="contact">Contact</h2>

<p>You can contact the GHSL team at <code class="language-plaintext highlighter-rouge">securitylab@github.com</code>, please include the <code class="language-plaintext highlighter-rouge">GHSL-2020-013</code> in any communication regarding this issue.</p>

   