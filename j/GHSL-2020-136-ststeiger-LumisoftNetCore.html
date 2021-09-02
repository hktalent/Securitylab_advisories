<header class="post-header d-block mb-6">
      <div class="date text-mono f5 my-3">December 3, 2020</div>
      <h1 class="my-2 h00-mktg lh-condensed">GHSL-2020-136: Unsafe deserialization vulnerabilties in Lumisoft .NET and Lumisoft MailServer</h1>

      
      
      
      
      

      

      <a target="_blank" class="sc-frDJqD SgxRc d-inline-flex flex-row flex-items-center text-gray" href="https://github.com/jarlob">
        <img class="mr-3" src="https://avatars.githubusercontent.com/u/26652396?s=35" height="35" width="35">
        <span>Jaroslav Lobacevski</span>
      </a>
    </header>

    <main id="content" class="markdown-body" aria-label="Content">
      <h2 id="summary">Summary</h2>

<p>Lumisoft .NET &amp; Lumisoft MailServer is extensively using deserialization of user supplied data into a <code class="language-plaintext highlighter-rouge">DataSet</code> object.</p>

<p>Microsoft recently released a security patch CVE-2020-1147 to limit the impact of reading untrusted XML into a <code class="language-plaintext highlighter-rouge">DataSet</code>. However its <a href="https://docs.microsoft.com/en-us/dotnet/framework/data/adonet/dataset-datatable-dataview/security-guidance">official statement</a> is:</p>

<blockquote>
  <p>The DataSet.ReadXml and DataTable.ReadXml methods are not safe when used with untrusted input. We strongly recommend that consumers instead consider using one of the alternatives outlined later in this document.
…and…
.NET has released security updates to mitigate some issues such as information disclosure or remote code execution in DataSet.ReadXml and DataTable.ReadXml. The .NET security updates may not provide complete protection against these threat categories. Consumers should assess their individual scenarios and consider their potential exposure to these risks.</p>
</blockquote>

<h2 id="product">Product</h2>

<p>Lumisoft .NET &amp; Lumisoft MailServer for .NET Core 2.0.</p>

<h2 id="tested-version">Tested Version</h2>

<p>The latest changeset to the date <a href="https://github.com/ststeiger/Lumisoft.Net.Core/tree/7a3a66ecec30114bdd305bc0e91a95ca7f4282d0">7a3a66e</a>.</p>

<h2 id="details">Details</h2>

<h3 id="issue-1-deserialization-of-user-supplied-data-in-updatesettings-handler">Issue 1: Deserialization of user supplied data in <a href="https://github.com/ststeiger/Lumisoft.Net.Core/blob/7a3a66ecec30114bdd305bc0e91a95ca7f4282d0/CoreMail/ManagementServer/MonitoringServerSession.cs#L2072">UpdateSettings handler</a></h3>

<p>Lumisoft MailServer is listening on all network interfaces on port 5252 for incoming connections. The default configuration allows only localhost connections.<br />
One of the supported unauthenticated commands is <code class="language-plaintext highlighter-rouge">UPDATESETTINGS</code> in a form of:<br />
<code class="language-plaintext highlighter-rouge">UPDATESETTINGS &lt;virtualServerID&gt; &lt;dataLength&gt;&lt;CRLF&gt;&lt;xml&gt;</code> that is handled by the following code:</p>

<div class="language-cs highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="n">MemoryStream</span> <span class="n">ms</span> <span class="p">=</span> <span class="k">new</span> <span class="nf">MemoryStream</span><span class="p">();</span>
<span class="k">this</span><span class="p">.</span><span class="n">TcpStream</span><span class="p">.</span><span class="nf">ReadFixedCount</span><span class="p">(</span><span class="n">ms</span><span class="p">,</span><span class="n">Convert</span><span class="p">.</span><span class="nf">ToInt32</span><span class="p">(</span><span class="n">args</span><span class="p">[</span><span class="m">1</span><span class="p">]));</span>
<span class="n">ms</span><span class="p">.</span><span class="n">Position</span> <span class="p">=</span> <span class="m">0</span><span class="p">;</span>
<span class="n">DataSet</span> <span class="n">ds</span> <span class="p">=</span> <span class="k">new</span> <span class="nf">DataSet</span><span class="p">();</span>
<span class="p">...</span>
<span class="n">ds</span><span class="p">.</span><span class="nf">ReadXml</span><span class="p">(</span><span class="n">ms</span><span class="p">);</span>
</code></pre></div></div>

<h4 id="impact">Impact</h4>

<p>This issue may lead to pre-auth Remote Code Execution (RCE). If the endpoint is not accessible from remote addresses and the server is running as a privileged process it may lead to Local Privilege Escalation (LPE).</p>

<h3 id="issue-2-unsafe-deserialization-of-data-returned-by-the-server">Issue 2: Unsafe deserialization of data returned by the server</h3>

<p>Lumisoft User API libraries deserialize data returned from a server in multiple places like <a href="https://github.com/ststeiger/Lumisoft.Net.Core/blob/7a3a66ecec30114bdd305bc0e91a95ca7f4282d0/UserAPI/Utils.cs#L40">DecompressDataSet</a>, <a href="https://github.com/ststeiger/Lumisoft.Net.Core/blob/7a3a66ecec30114bdd305bc0e91a95ca7f4282d0/UserAPI/RecycleBin.cs#L178">RecyleBin.Bind</a>, <a href="https://github.com/ststeiger/Lumisoft.Net.Core/blob/7a3a66ecec30114bdd305bc0e91a95ca7f4282d0/UserAPI/System_Settings.cs#L1061">System_Settings.Bind</a>, etc.</p>

<h4 id="impact-1">Impact</h4>

<p>This issue may lead to pre-auth Remote Code Execution (RCE) on the client side in a Person in the Middle (PitM) scenario or if the user is tricked into connecting to a malicious server.</p>

<h2 id="coordinated-disclosure-timeline">Coordinated Disclosure Timeline</h2>

<ul>
  <li>2020-07-28: Report sent to maintainer.</li>
  <li>2020-07-28: Maintainer acknowledges.</li>
  <li>2020-10-26: 90 days from when the report was sent, disclosure deadline expires.</li>
  <li>2020-10-29: Notification sent to maintainer. No reply.</li>
</ul>

<h2 id="credit">Credit</h2>

<p>This issue was discovered and reported by GHSL team member <a href="https://github.com/JarLob">@JarLob (Jaroslav Lobačevski)</a>.</p>

<h2 id="contact">Contact</h2>

<p>You can contact the GHSL team at <code class="language-plaintext highlighter-rouge">securitylab@github.com</code>, please include a reference to <code class="language-plaintext highlighter-rouge">GHSL-2020-136</code> in any communication regarding this issue.</p>
