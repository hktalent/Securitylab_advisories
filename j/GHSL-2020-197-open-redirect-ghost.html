<header class="post-header d-block mb-6">
      <div class="date text-mono f5 my-3">February 12, 2021</div>
      <h1 class="my-2 h00-mktg lh-condensed">GHSL-2020-197: Open redirect vulnerability in Ghost</h1>

      
      
      
      
      

      

      <a target="_blank" class="sc-frDJqD SgxRc d-inline-flex flex-row flex-items-center text-gray" href="https://github.com/ghsecuritylab">
        <img class="mr-3" src="https://avatars.githubusercontent.com/u/61799930?s=35" height="35" width="35">
        <span>GitHub Security Lab</span>
      </a>
    </header>

    <main id="content" class="markdown-body" aria-label="Content">
      <h2 id="coordinated-disclosure-timeline">Coordinated Disclosure Timeline</h2>
<ul>
  <li>10/19/2020: Report sent to: security@ghost.org</li>
  <li>10/20/2020: Ghost shares proposed fix</li>
  <li>01/18/2021: Request status update from maintainers</li>
  <li>2/11/2021: The fix is released in 3.41.1, and backported to the 2.x branch (2.38.3).</li>
</ul>

<h2 id="summary">Summary</h2>

<p>Ghost may be vulnerable to Open redirect attacks</p>

<h2 id="product">Product</h2>

<p><a href="https://github.com/TryGhost/Ghost">Ghost</a></p>

<h2 id="tested-version">Tested Version</h2>
<p>Latest commit at the date of reporting.</p>

<h2 id="details">Details</h2>

<p><a href="https://github.com/TryGhost/Ghost/blob/f81e0755cc7afcc9e2a85a56f031e106e155e16e/core/frontend/apps/private-blogging/lib/middleware.js#L151">This line</a> redirects to the path name of a redirect URL stored in <a href="https://github.com/TryGhost/Ghost/blob/f81e0755cc7afcc9e2a85a56f031e106e155e16e/core/frontend/apps/private-blogging/lib/middleware.js#L144">a query parameter</a>.</p>

<p>If the redirect URL is under the control of an attacker, they can provide a URL whose path name starts with a double slash (or double backslash, slash followed by backslash, etc.). This will then be interpreted as an absolute URL without a protocol, and will redirect to an external site of the attacker’s choosing.</p>

<h4 id="impact">Impact</h4>

<p>Open redirect. If the attacker can control the redirect URL, it could be possible to launch a phishing attack where the attacker sends a crafted link to someone with a Ghost blog that looks like it refers to one of their articles. When they click on the link, they’ll be taken to the login screen, enter their credentials, and then are redirected to wherever the attacker would like them to go.</p>

<h2 id="credit">Credit</h2>

<p>This issue was discovered and reported by GitHub team member <a href="https://github.com/max-schaefer">Max Schaefer</a>.</p>

<h2 id="contact">Contact</h2>

<p>You can contact the GHSL team at <code class="language-plaintext highlighter-rouge">securitylab@github.com</code>, please include <code class="language-plaintext highlighter-rouge">GHSL-2020-197</code> in any communication regarding this issue.</p>

