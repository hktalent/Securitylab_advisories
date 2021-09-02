<header class="post-header d-block mb-6">
      <div class="date text-mono f5 my-3">April 20, 2020</div>
      <h1 class="my-2 h00-mktg lh-condensed">GHSL-2020-031: SQL injection in PureFTPd</h1>

      
      
      
      
      

      

      <a target="_blank" class="sc-frDJqD SgxRc d-inline-flex flex-row flex-items-center text-gray" href="https://github.com/antonio-morales">
        <img class="mr-3" src="https://avatars.githubusercontent.com/u/55253029?s=35" height="35" width="35">
        <span>Antonio Morales</span>
      </a>
    </header>

    <main id="content" class="markdown-body" aria-label="Content">
      <h2 id="summary">Summary</h2>

<p>The <code class="language-plaintext highlighter-rouge">pw_pgsql_connect</code> function does not properly sanitize SQL queries, leading to SQLi via the <code class="language-plaintext highlighter-rouge">pgsql</code> config file.</p>

<h2 id="product">Product</h2>
<p>PureFTPd</p>

<h2 id="cve">CVE</h2>
<p>No CVE assigned</p>

<h2 id="tested-version">Tested Version</h2>
<p>Development version - master branch (Feb 20, 2020)</p>

<h2 id="details-broken-sql-sanitizer-in-pw_pgsql_connect-sqli-via-config-file">Details: Broken SQL sanitizer in <code class="language-plaintext highlighter-rouge">pw_pgsql_connect</code> (SQLi via config file)</h2>

<p>Two different bugs have been detected:</p>
<ul>
  <li>There is a mistake in <code class="language-plaintext highlighter-rouge">pw_pgsql_escape_conninfo_</code> for the case ‘\’ <a href="/assets/advisories-resources/GHSL-2020-031-Bug1.png">here</a>. The current code snippet is re-introducing the single-quote.</li>
  <li>The <code class="language-plaintext highlighter-rouge">snprintf</code> function is called with non-escaped strings (<code class="language-plaintext highlighter-rouge">server</code>, <code class="language-plaintext highlighter-rouge">port</code>, <code class="language-plaintext highlighter-rouge">db</code>, <code class="language-plaintext highlighter-rouge">user</code>, <code class="language-plaintext highlighter-rouge">pw</code>), instead of using escaped strings (<code class="language-plaintext highlighter-rouge">escaped_server</code>, <code class="language-plaintext highlighter-rouge">escaped_db</code>, <code class="language-plaintext highlighter-rouge">escaped_user</code>, <code class="language-plaintext highlighter-rouge">escaped_pw</code>) <a href="/assets/advisories-resources/GHSL-2020-031-Bug2.png">here</a>.
As a result, <code class="language-plaintext highlighter-rouge">conninfo</code> string is not being properly sanitized and it is possible to inject SQL code into this query.</li>
</ul>

<h3 id="impact">Impact</h3>

<p>This issue may lead to a local SQLi via <code class="language-plaintext highlighter-rouge">pqsql</code> config file.</p>

<h3 id="remediation">Remediation</h3>

<ul>
  <li>Fix switch-case statement <a href="/assets/advisories-resources/GHSL-2020-031-Step1.png">here</a></li>
  <li>Use properly escaped strings <a href="/assets/advisories-resources/GHSL-2020-031-Step2.png">here</a></li>
</ul>

<h2 id="coordinated-disclosure-timeline">Coordinated Disclosure Timeline</h2>
<p>This report is subject to our coordinated disclosure policy.</p>

<ul>
  <li>20/02/2020: Report sent to Vendor</li>
  <li>16/03/2020: Vendor acknowledged report</li>
  <li>16/03/2020: Fixes reviewed and verified</li>
  <li>17/03/2020: Report published to public</li>
</ul>

<h3 id="resources">Resources</h3>
<ul>
  <li><a href="/assets/advisories-resources/GHSL-2020-031-Bug1.png">Bug1.png</a>: 1st Vulnerable code snippet</li>
  <li><a href="/assets/advisories-resources/GHSL-2020-031-Bug2.png">Bug2.png</a>: 2nd Vulnerable code snippet</li>
  <li><a href="/assets/advisories-resources/GHSL-2020-031-Step1.png">Step1.png</a>: Configuration file example</li>
  <li><a href="/assets/advisories-resources/GHSL-2020-031-Step2.png">Step2.png</a>: “conninfo” string value (GDB)</li>
</ul>

<h2 id="credit">Credit</h2>

<p>This issue was discovered and reported by GHSL team member <a href="https://github.com/antonio-morales">@antonio-morales (Antonio Morales)</a>.</p>

<h2 id="contact">Contact</h2>

<p>You can contact the GHSL team at <code class="language-plaintext highlighter-rouge">securitylab@github.com</code>, please include the <code class="language-plaintext highlighter-rouge">GHSL-2020-031</code> in any communication regarding this issue.</p