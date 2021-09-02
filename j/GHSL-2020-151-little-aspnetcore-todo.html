<header class="post-header d-block mb-6">
      <div class="date text-mono f5 my-3">November 5, 2020</div>
      <h1 class="my-2 h00-mktg lh-condensed">GHSL-2020-151: Cross-Site Scripting (XSS) and Cross-Site Request Forgery (CSRF) in little-aspnetcore-todo</h1>

      
      
      
      
      

      

      <a target="_blank" class="sc-frDJqD SgxRc d-inline-flex flex-row flex-items-center text-gray" href="https://github.com/jarlob">
        <img class="mr-3" src="https://avatars.githubusercontent.com/u/26652396?s=35" height="35" width="35">
        <span>Jaroslav Lobacevski</span>
      </a>
    </header>

    <main id="content" class="markdown-body" aria-label="Content">
      <h2 id="summary">Summary</h2>

<p><a href="https://github.com/nbarbettini/little-aspnetcore-todo">little-aspnetcore-todo</a> is vulnerable to Cross-Site Scripting (XSS) and Cross-Site Request Forgery (CSRF) that may lead to the elevation of privileges and per-user denial of service (DoS).</p>

<h2 id="product">Product</h2>

<p><a href="https://github.com/nbarbettini/little-aspnetcore-todo">little-aspnetcore-todo</a></p>

<h2 id="tested-version">Tested Version</h2>

<p>Master branch.</p>

<h2 id="details">Details</h2>

<h3 id="issue-1-xss-cve-2018-0784">Issue 1: XSS (CVE-2018-0784)</h3>
<p>The application doesn’t have a fix for <a href="https://github.com/aspnet/Announcements/issues/285">CVE-2018-0784</a> that was found in ASP.NET Core templates. It is vulnerable to XSS if the logged-in user is tricked into clicking a malicious link like <code class="language-plaintext highlighter-rouge">https://localhost:44315/manage/EnableAuthenticator?AuthenticatorUri=%22%3E%3C/div%3E%00%00%00%00%00%00%00%3Cscript%3Ealert(%22XSS%22)%3C/script%3E</code> and enters an invalid verification code. More details are available in <a href="https://kevinchalet.com/2018/01/09/why-you-should-never-use-html-raw-in-your-razor-views/">this blog post</a>.</p>

<h4 id="impact">Impact</h4>

<p>This issue may lead to the elevation of privileges.</p>

<h4 id="remediation">Remediation</h4>

<p>Modify the code according to the instructions from <a href="https://github.com/aspnet/Announcements/issues/285">the ASP.NET advisory</a>.</p>

<h3 id="issue-2-csrf-cve-2018-0785">Issue 2: CSRF (CVE-2018-0785)</h3>
<p>The application doesn’t have a fix for <a href="https://github.com/aspnet/Announcements/issues/284">CVE-2018-0785</a> that was found in ASP.NET Core templates. It is vulnerable to CSRF. A logged-in user with enabled Second Factor Authentication (2FA) may lose their recovery codes if they are tricked into clicking a link like <code class="language-plaintext highlighter-rouge">https://localhost:44315/manage/GenerateRecoveryCodes</code> or visit a malicious site that makes the request without the user’s consent. As a result the user may be permanently locked out of their account after losing access to their 2FA device, as the initial recovery codes would no longer be valid.</p>

<h4 id="impact-1">Impact</h4>

<p>This issue may lead to a per-user DoS.</p>

<h4 id="remediation-1">Remediation</h4>

<p>Modify the code according to the instructions from <a href="https://github.com/aspnet/Announcements/issues/284">the ASP.NET advisory</a>.</p>

<h2 id="coordinated-disclosure-timeline">Coordinated Disclosure Timeline</h2>

<ul>
  <li>09/11/2020: Report sent to owner</li>
  <li>11/04/2020: No response, created a public issue https://github.com/nbarbettini/little-aspnetcore-todo/issues/24</li>
</ul>

<h2 id="credit">Credit</h2>

<p>This issue was discovered and reported by GHSL team member <a href="https://github.com/JarLob">@JarLob (Jaroslav Lobačevski)</a>.</p>

<h2 id="contact">Contact</h2>

<p>You can contact the GHSL team at <code class="language-plaintext highlighter-rouge">securitylab@github.com</code>, please include a reference to <code class="language-plaintext highlighter-rouge">GHSL-2020-151</code> in any communication regarding this issue.</p