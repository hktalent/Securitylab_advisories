<header class="post-header d-block mb-6">
      <div class="date text-mono f5 my-3">February 12, 2021</div>
      <h1 class="my-2 h00-mktg lh-condensed">GHSL-2020-199: Open redirect vulnerability in Slashify - CVE-2021-3189</h1>

      
      
      
      
      

      

      <a target="_blank" class="sc-frDJqD SgxRc d-inline-flex flex-row flex-items-center text-gray" href="https://github.com/ghsecuritylab">
        <img class="mr-3" src="https://avatars.githubusercontent.com/u/61799930?s=35" height="35" width="35">
        <span>GitHub Security Lab</span>
      </a>
    </header>

    <main id="content" class="markdown-body" aria-label="Content">
      <h2 id="coordinated-disclosure-timeline">Coordinated Disclosure Timeline</h2>
<ul>
  <li>10/19/2020: Report sent to scottcorgan@gmail.com (https://registry.npmjs.org/slashify/latest)</li>
  <li>01/20/2021: Issue reported to affected projects: <code class="language-plaintext highlighter-rouge">uktrade/data-hub-frontend</code> and <code class="language-plaintext highlighter-rouge">ministryofjustice/hmpps-book-secure-move-frontend</code></li>
  <li>01/20/2021: Issue gets fixed in <a href="https://github.com/ministryofjustice/hmpps-book-secure-move-frontend/commit/fcfb47349ab31353caf3588a8f9c750f7064652d">ministryofjustice/hmpps-book-secure-move-frontend</a></li>
  <li>01/21/2021: MITRE assigns CVE-2021-3189</li>
  <li>02/02/2021: Issue gets fixed in <a href="https://github.com/uktrade/data-hub-frontend/blob/c6c52047d13047fdcc69cc4788d81bacdb5bdbc2/src/middleware/fix-slashes.js">uktrade/data-hub-frontend</a></li>
</ul>

<h2 id="summary">Summary</h2>

<p>Open redirect in Slashify</p>

<h2 id="product">Product</h2>

<p>The <a href="https://www.npmjs.com/package/slashify">slashify</a> npm package.</p>

<h2 id="tested-version">Tested Version</h2>

<p>Latest commit at the date of reporting.</p>

<h2 id="details">Details</h2>

<p>The package is an Express middleware that normalises routes by stripping any final slash, redirecting, for example, <code class="language-plaintext highlighter-rouge">bookings/latest/</code> to <code class="language-plaintext highlighter-rouge">bookings/latest</code>. However, it does not validate the path it redirects to in any way. In particular, if the path starts with two slashes (or two backslashes, or a slash and a backslash, etc.) it may redirect to a different domain.</p>

<p>Consider the <a href="https://www.npmjs.com/package/slashify#usage">example from the docs</a>. Assume we have run it and started a server on <code class="language-plaintext highlighter-rouge">localhost:3000</code>, then visiting <code class="language-plaintext highlighter-rouge">localhost:3000///github.com/</code> redirects you to https://github.com.</p>

<h4 id="impact">Impact</h4>

<p>Open redirect</p>

<h2 id="cve">CVE</h2>
<ul>
  <li>CVE-2021-3189</li>
</ul>

<h2 id="credit">Credit</h2>

<p>This issue was discovered and reported by GitHub team member <a href="https://github.com/max-schaefer">@max-schaefer (Max Schaefer)</a>.</p>

<h2 id="contact">Contact</h2>

<p>You can contact the GHSL team at <code class="language-plaintext highlighter-rouge">securitylab@github.com</code>, please include <code class="language-plaintext highlighter-rouge">GHSL-2020-199</code> in any communication regarding this issue.</p>

    