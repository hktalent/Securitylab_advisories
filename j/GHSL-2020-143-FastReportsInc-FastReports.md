<header class="post-header d-block mb-6">
      <div class="date text-mono f5 my-3">October 30, 2020</div>
      <h1 class="my-2 h00-mktg lh-condensed">GHSL-2020-143: Arbitrary Code Execution in FastReports - CVE-2020-27998</h1>

      
      
      
      
      

      

      <a target="_blank" class="sc-frDJqD SgxRc d-inline-flex flex-row flex-items-center text-gray" href="https://github.com/jarlob">
        <img class="mr-3" src="https://avatars.githubusercontent.com/u/26652396?s=35" height="35" width="35">
        <span>Jaroslav Lobacevski</span>
      </a>
    </header>

    <main id="content" class="markdown-body" aria-label="Content">
      <h2 id="summary">Summary</h2>

<p>FastReports is vulnerable to arbitrary code execution because it compiles and runs C# code from a report template.</p>

<h2 id="product">Product</h2>

<p><a href="https://github.com/FastReports/FastReport">FastReports</a></p>

<h2 id="tested-version">Tested Version</h2>

<p>Master branch.</p>

<h2 id="details">Details</h2>

<h3 id="issue-compilation-of-user-supplied-expressions-into-a-net-assembly">Issue: <a href="https://github.com/FastReports/FastReport/blob/93ed08cbee374b952721ee5251323e23d3fa9f9f/FastReport.Base/Report.cs#L1214">Compilation</a> of user supplied expressions into a .NET assembly.</h3>

<p>While the dynamic data transformation into a compiled .NET code could be acceptable if the report template and the data from data source are trusted, the advertised <a href="https://www.fast-report.com/en/product/fast-report-online-designer/">Online Designer</a> <a href="https://www.fast-report.com:2015/razor/Home/Designer">demonstrates</a> that this assumption does not hold true.<br />
Any user may run arbitrary remote code on the server by creating a new expression or editing an existing one into, for example <code class="language-plaintext highlighter-rouge">[System.String.Join(",", System.IO.Directory.GetDirectories(@"c:/"))]</code>.</p>
<blockquote>
  <p>Side Note: The forward slash ‘/’ is used instead of the back slash ‘\’ because FastReports library fails to recognize a string literal if the last character is ‘\’.</p>
</blockquote>

<p>After the user clicks <code class="language-plaintext highlighter-rouge">Preview</code> the code is executed on the server.</p>

<h4 id="impact">Impact</h4>

<p>Arbitrary code execution on the report template processing host.</p>

<h4 id="remediation">Remediation</h4>

<p>The allowed expressions should be restricted to an acceptable subset. The compiled code should be run in a sandboxed process.</p>

<h2 id="cve">CVE</h2>

<ul>
  <li>CVE-2020-27998</li>
</ul>

<h2 id="coordinated-disclosure-timeline">Coordinated Disclosure Timeline</h2>

<ul>
  <li>24/08/2020: Report sent to Vendor</li>
  <li>26/08/2020: Vendor acknowledges</li>
  <li>28/08/2020: Vendor implements a filtering to remediate the issue</li>
  <li>07/09/2020: Vendor publishes an <a href="https://fast-report.com/en/blog/360/show/">announcement</a></li>
  <li>29/10/2020: CVE-2020-27998 got assigned</li>
</ul>

<h2 id="resources">Resources</h2>

<ul>
  <li>The fix - https://github.com/FastReports/FastReport/pull/206</li>
  <li>Vendor advisories:
    <ul>
      <li>https://opensource.fast-report.com/2020/09/report-script-security.html</li>
      <li>https://fast-report.com/en/blog/360/show/</li>
    </ul>
  </li>
</ul>

<h2 id="credit">Credit</h2>

<p>This issue was discovered and reported by GHSL team member <a href="https://github.com/JarLob">@JarLob (Jaroslav Lobačevski)</a>.</p>

<h2 id="contact">Contact</h2>

<p>You can contact the GHSL team at <code class="language-plaintext highlighter-rouge">securitylab@github.com</code>, please include a reference to <code class="language-plaintext highlighter-rouge">GHSL-2020-143</code> in any communication regarding this iss