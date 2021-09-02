>
    <header class="post-header d-block mb-6">
      <div class="date text-mono f5 my-3">September 14, 2020</div>
      <h1 class="my-2 h00-mktg lh-condensed">GHSL-2020-140: Open redirect in Traefik - CVE-2020-15129</h1>

      
      
      
      
      

      

      <a target="_blank" class="sc-frDJqD SgxRc d-inline-flex flex-row flex-items-center text-gray" href="https://github.com/ghsecuritylab">
        <img class="mr-3" src="https://avatars.githubusercontent.com/u/61799930?s=35" height="35" width="35">
        <span>GitHub Security Lab</span>
      </a>
    </header>

    <main id="content" class="markdown-body" aria-label="Content">
      <h2 id="summary">Summary</h2>

<p>There exists a potential open redirect vulnerability in Traefik’s handling of the <code class="language-plaintext highlighter-rouge">X-Forwarded-Prefix</code> header. Active Exploitation of this issue is unlikely as it would require active header injection, however the Traefik team may want to address this issue nonetheless to prevent abuse in e.g. cache poisoning scenarios.</p>

<h2 id="product">Product</h2>

<p><a href="https://github.com/containous/traefik">Traefik</a></p>

<h2 id="tested-version">Tested Version</h2>

<p>v2.3.0-rc1</p>

<h2 id="details">Details</h2>

<p>The Traefik API dashboard component doesn’t validate that the value of the header <code class="language-plaintext highlighter-rouge">X-Forwarded-Prefix</code> is a site relative path and will redirect to any header provided URI.</p>

<p>e.g.</p>

<div class="language-plaintext highlighter-rouge"><div class="highlight"><pre class="highlight"><code>$ curl --header 'Host:docker.localhost' --header 'X-Forwarded-Prefix:https://foo.nl' 'http://localhost:8081'
&lt;a href="https://foo.nl/dashboard/"&gt;Found&lt;/a&gt;.`
</code></pre></div></div>

<h4 id="impact">Impact</h4>

<p>A successful exploitation of an open redirect can be used to entice victims to disclose sensitive information.</p>

<h4 id="resources">Resources</h4>

<ul>
  <li>https://github.com/containous/traefik/blob/8f2951b275d88312a1add5084fa985e5d878be7a/pkg/api/dashboard.go#L27</li>
</ul>

<h2 id="cve">CVE</h2>

<ul>
  <li>CVE-2020-15129</li>
</ul>

<h2 id="coordinated-disclosure-timeline">Coordinated Disclosure Timeline</h2>

<ul>
  <li>07/27/2020: vendor contacted</li>
  <li>07/30/2020: vendor publishes patches and GHSA</li>
</ul>

<h2 id="resources-1">Resources</h2>

<ul>
  <li>https://github.com/containous/traefik/security/advisories/GHSA-6qq8-5wq3-86rp</li>
</ul>

<h2 id="credit">Credit</h2>

<p>This issue was found by the GitHub Application Security Team and reported on behalf of the GHAS by the GitHub Security Lab Team.</p>

<h2 id="contact">Contact</h2>

<p>You can contact the GHSL team at <code class="language-plaintext highlighter-rouge">securitylab@github.com</code>, please include <code class="language-plaintext highlighter-rouge">GHSL-2020-140</code> in any communication regarding this issue.