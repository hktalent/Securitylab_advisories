<header class="post-header d-block mb-6">
      <div class="date text-mono f5 my-3">April 13, 2021</div>
      <h1 class="my-2 h00-mktg lh-condensed">GHSL-2020-336: reflected Cross-Site scripting (XSS) in analytics-quarry-web - CVE-2020-36324</h1>

      
      
      
      
      

      

      <a target="_blank" class="sc-frDJqD SgxRc d-inline-flex flex-row flex-items-center text-gray" href="https://github.com/ghsecuritylab">
        <img class="mr-3" src="https://avatars.githubusercontent.com/u/61799930?s=35" height="35" width="35">
        <span>GitHub Security Lab</span>
      </a>
    </header>

    <main id="content" class="markdown-body" aria-label="Content">
      
<h2 id="coordinated-disclosure-timeline">Coordinated Disclosure Timeline</h2>

<ul>
  <li>2020-12-15: Reported to security@wikimedia.org</li>
  <li>2020-12-15: ​Issue acknowledged</li>
  <li>2020-12-15: Issue is <a href="https://github.com/wikimedia/analytics-quarry-web/commit/4b7e1d6a3a52ec6cf826a971135a38b0f74785d2">fixed</a></li>
</ul>

<h2 id="summary">Summary</h2>

<p>A reflected Cross-Site scripting (XSS) vulnerability has been found in analytics-quarry-web</p>

<h2 id="product">Product</h2>

<p>https://github.com/wikimedia/analytics-quarry-web</p>

<h2 id="tested-version">Tested Version</h2>

<p>Latest commit at the time of reporting (December 14, 2020).</p>

<h2 id="details">Details</h2>

<p>The server responds with <code class="language-plaintext highlighter-rouge">return Response(json.dumps(...))</code> without setting proper mime-type (<code class="language-plaintext highlighter-rouge">application/json</code>).</p>

<p>This becomes problematic for the preference handling defined here: https://github.com/wikimedia/analytics-quarry-web/blob/085a51b2dee8b58882276d9fe090174252edb85e/quarry/web/app.py#L395-L412</p>

<p>You can exploit this vulnerability by tricking a logged in user to visit vulnerable URL.</p>

<p>PoC:</p>

<ol>
  <li>Visit official Quarry site https://quarry.wmflabs.org/ or follow setup instructions on repo. (I found official site from here)</li>
  <li>Log in with a wiki-media acocunt</li>
  <li>Visit vulnerable URL: https://quarry.wmflabs.org/api/preferences/get/%3Cimg%20src=0%20onerror=alert(0)%3E</li>
</ol>

<h4 id="impact">Impact</h4>

<p>XSS can cause a variety of problems for the end user that range in severity from an annoyance to complete account compromise. The most severe XSS attacks involve disclosure of the user’s session cookie, allowing an attacker to hijack the user’s session and take over the account.</p>

<h2 id="cve">CVE</h2>

<ul>
  <li>CVE-2020-36324</li>
</ul>

<h2 id="credit">Credit</h2>

<p>This issue was discovered and reported by Rasmus Wriedt Larsen of the CodeQL Python team.</p>

<h2 id="contact">Contact</h2>

<p>You can contact the GHSL team at <code class="language-plaintext highlighter-rouge">securitylab@github.com</code>, please include <code class="language-plaintext highlighter-rouge">GHSL-2020-336</code> in any communication regarding this issue.</p>
