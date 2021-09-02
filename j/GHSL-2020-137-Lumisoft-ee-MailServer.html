<header class="post-header d-block mb-6">
      <div class="date text-mono f5 my-3">December 3, 2020</div>
      <h1 class="my-2 h00-mktg lh-condensed">GHSL-2020-137: Unsafe deserialization in Lumisoft Mail Server</h1>

      
      
      
      
      

      

      <a target="_blank" class="sc-frDJqD SgxRc d-inline-flex flex-row flex-items-center text-gray" href="https://github.com/jarlob">
        <img class="mr-3" src="https://avatars.githubusercontent.com/u/26652396?s=35" height="35" width="35">
        <span>Jaroslav Lobacevski</span>
      </a>
    </header>

    <main id="content" class="markdown-body" aria-label="Content">
      <h2 id="summary">Summary</h2>

<p>Lumisoft MailServer is extensively using deserialization of user supplied data into a <code class="language-plaintext highlighter-rouge">DataSet</code> object.</p>

<p>Microsoft recently released a security patch CVE-2020-1147 to limit the impact of reading untrusted XML into a <code class="language-plaintext highlighter-rouge">DataSet</code>. However its <a href="https://docs.microsoft.com/en-us/dotnet/framework/data/adonet/dataset-datatable-dataview/security-guidance">official statement</a> is:</p>
<blockquote>
  <p>The DataSet.ReadXml and DataTable.ReadXml methods are not safe when used with untrusted input. We strongly recommend that consumers instead consider using one of the alternatives outlined later in this document.
…and…
.NET has released security updates to mitigate some issues such as information disclosure or remote code execution in DataSet.ReadXml and DataTable.ReadXml. The .NET security updates may not provide complete protection against these threat categories. Consumers should assess their individual scenarios and consider their potential exposure to these risks.</p>
</blockquote>

<h2 id="product">Product</h2>

<p>Lumisoft Mail Server</p>

<h2 id="tested-version">Tested Version</h2>

<p><a href="http://www.lumisoft.ee/lswww/download/downloads/MailServer/MailServer_devel.zip">The latest development snapshot to the date</a> from downloads section.</p>

<h2 id="details">Details</h2>

<h3 id="issue-1-deserialization-of-user-supplied-data-in-monitoringserversessionupdatesettings">Issue 1: Deserialization of user supplied data in <code class="language-plaintext highlighter-rouge">MonitoringServerSession.UpdateSettings</code></h3>

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

<p>Lumisoft User API libraries deserialize data returned from a server in multiple places like <code class="language-plaintext highlighter-rouge">Utils.DecompressDataSet</code>, <code class="language-plaintext highlighter-rouge">RecyleBin.Bind</code>, <code class="language-plaintext highlighter-rouge">System_Settings.Bind</code>, etc.</p>

<h4 id="impact-1">Impact</h4>

<p>This issue may lead to pre-auth Remote Code Execution (RCE) on the client side in a Person in the Middle (PitM) scenario or if the user is tricked into connecting to a malicious server.</p>

<h2 id="coordinated-disclosure-timeline">Coordinated Disclosure Timeline</h2>

<ul>
  <li>2020-07-21: Report sent to maintainer. No reply.</li>
  <li>2020-07-28: Notification sent to maintainer.</li>
  <li>2020-10-19: 90 days from when the report was sent, disclosure deadline expires.</li>
  <li>2020-10-29: Notification sent to maintainer.</li>
</ul>

<h2 id="credit">Credit</h2>

<p>This issue was discovered and reported by GHSL team member <a href="https://github.com/JarLob">@JarLob (Jaroslav Lobačevski)</a>.</p>

<h2 id="contact">Contact</h2>

<p>You can contact the GHSL team at <code class="language-plaintext highlighter-rouge">securitylab@github.com</code>, please include a reference to <code class="language-plaintext highlighter-rouge">GHSL-2020-137</code> in any communication regarding this issue.</p>
