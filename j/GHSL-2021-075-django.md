<header class="post-header d-block mb-6">
      <div class="date text-mono f5 my-3">June 8, 2021</div>
      <h1 class="my-2 h00-mktg lh-condensed">GHSL-2021-075: Path injection in Django - CVE-2021-33203</h1>

      
      
      
      
      

      

      <a target="_blank" class="sc-frDJqD SgxRc d-inline-flex flex-row flex-items-center text-gray" href="https://github.com/ghsecuritylab">
        <img class="mr-3" src="https://avatars.githubusercontent.com/u/61799930?s=35" height="35" width="35">
        <span>GitHub Security Lab</span>
      </a>
    </header>

    <main id="content" class="markdown-body" aria-label="Content">
      
<h2 id="coordinated-disclosure-timeline">Coordinated Disclosure Timeline</h2>

<ul>
  <li>2021-05-13: Report sent to maintainers</li>
  <li>2021-05-13: Report is acknowledged</li>
  <li>2021-05-17: A patch for the issue is proposed</li>
  <li>2021-06-02: Vulnerability was made public</li>
</ul>

<h2 id="summary">Summary</h2>

<p>A Path Injection issue was found in <code class="language-plaintext highlighter-rouge">django</code> that allows a malicious admin user to disclose the presence of files on the file-system if the module <code class="language-plaintext highlighter-rouge">django.contrib.admindocs</code> is enabled.</p>

<h2 id="product">Product</h2>

<p>django</p>

<h2 id="tested-version">Tested Version</h2>

<p>3.2.2</p>

<h2 id="details">Details</h2>

<p>There is an unsafe <code class="language-plaintext highlighter-rouge">Path</code> join operation in <a href="https://github.com/django/django/blob/e1e81aa1c4427411e3c68facdd761229ffea6f6f/django/contrib/admindocs/views.py#L336">views.py</a> that allows an attacker to supply paths that are outside the templates directory (1).</p>

<div class="language-python highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="k">class</span> <span class="nc">TemplateDetailView</span><span class="p">(</span><span class="n">BaseAdminDocsView</span><span class="p">):</span>
    <span class="n">template_name</span> <span class="o">=</span> <span class="s">'admin_doc/template_detail.html'</span>

    <span class="k">def</span> <span class="nf">get_context_data</span><span class="p">(</span><span class="bp">self</span><span class="p">,</span> <span class="o">**</span><span class="n">kwargs</span><span class="p">):</span>
        <span class="n">template</span> <span class="o">=</span> <span class="bp">self</span><span class="p">.</span><span class="n">kwargs</span><span class="p">[</span><span class="s">'template'</span><span class="p">]</span>
        <span class="n">templates</span> <span class="o">=</span> <span class="p">[]</span>
        <span class="k">try</span><span class="p">:</span>
            <span class="n">default_engine</span> <span class="o">=</span> <span class="n">Engine</span><span class="p">.</span><span class="n">get_default</span><span class="p">()</span>
        <span class="k">except</span> <span class="n">ImproperlyConfigured</span><span class="p">:</span>
            <span class="c1"># Non-trivial TEMPLATES settings aren't supported (#24125).
</span>            <span class="k">pass</span>
        <span class="k">else</span><span class="p">:</span>
            <span class="c1"># This doesn't account for template loaders (#24128).
</span>            <span class="k">for</span> <span class="n">index</span><span class="p">,</span> <span class="n">directory</span> <span class="ow">in</span> <span class="nb">enumerate</span><span class="p">(</span><span class="n">default_engine</span><span class="p">.</span><span class="n">dirs</span><span class="p">):</span>
                <span class="c1"># NOTE(1): `template` is controled by an attacker.
</span>                <span class="n">template_file</span> <span class="o">=</span> <span class="n">Path</span><span class="p">(</span><span class="n">directory</span><span class="p">)</span> <span class="o">/</span> <span class="n">template</span>
                <span class="k">if</span> <span class="n">template_file</span><span class="p">.</span><span class="n">exists</span><span class="p">():</span>
                    <span class="c1"># NOTE(2)
</span>                    <span class="n">template_contents</span> <span class="o">=</span> <span class="n">template_file</span><span class="p">.</span><span class="n">read_text</span><span class="p">()</span>
                <span class="k">else</span><span class="p">:</span>
                    <span class="n">template_contents</span> <span class="o">=</span> <span class="s">''</span>
                <span class="n">templates</span><span class="p">.</span><span class="n">append</span><span class="p">({</span>
                    <span class="s">'file'</span><span class="p">:</span> <span class="n">template_file</span><span class="p">,</span>
                    <span class="s">'exists'</span><span class="p">:</span> <span class="n">template_file</span><span class="p">.</span><span class="n">exists</span><span class="p">(),</span>
                    <span class="s">'contents'</span><span class="p">:</span> <span class="n">template_contents</span><span class="p">,</span>
                    <span class="s">'order'</span><span class="p">:</span> <span class="n">index</span><span class="p">,</span>
                <span class="p">})</span>
        <span class="k">return</span> <span class="nb">super</span><span class="p">().</span><span class="n">get_context_data</span><span class="p">(</span><span class="o">**</span><span class="p">{</span>
            <span class="o">**</span><span class="n">kwargs</span><span class="p">,</span>
            <span class="s">'name'</span><span class="p">:</span> <span class="n">template</span><span class="p">,</span>
            <span class="s">'templates'</span><span class="p">:</span> <span class="n">templates</span><span class="p">,</span>
        <span class="p">})</span>
</code></pre></div></div>

<p>By logging in as an admin and requesting the following page, an attacker can detect the presence of arbitrary files in the filesystem, in this case the presence of <code class="language-plaintext highlighter-rouge">/etc/passwd</code>:</p>

<p>http://localhost:8000/admin/doc/templates//etc/passwd/</p>

<p>In (2) we see that the file is read and its contents are passed to the rendering method. We could not find a way to display the results but a more in depth look into this seems advisable.</p>

<h4 id="impact">Impact</h4>

<p>An authenticated malicious admin can disclose the presence of arbitrary files.</p>

<h4 id="resources">Resources</h4>

<ul>
  <li><a href="https://github.com/django/django/blob/e1e81aa1c4427411e3c68facdd761229ffea6f6f/django/contrib/admindocs/views.py#L336">https://github.com/django/django/blob/e1e81aa1c4427411e3c68facdd761229ffea6f6f/django/contrib/admindocs/views.py#L336</a></li>
  <li><a href="https://www.djangoproject.com/weblog/2021/jun/02/security-releases/">https://www.djangoproject.com/weblog/2021/jun/02/security-releases/</a></li>
</ul>

<h2 id="cve">CVE</h2>

<ul>
  <li>CVE-2021-33203</li>
</ul>

<h2 id="credit">Credit</h2>

<p>This issue was discovered by <a href="https://github.com/RasmusSemmle">Rasmus Lerchedahl Petersen</a> and <a href="https://github.com/RasmusWL">Rasmus Wriedt Larsen</a> from the CodeQL Python team.</p>

<h2 id="contact">Contact</h2>

<p>You can contact the GHSL team at <code class="language-plaintext highlighter-rouge">securitylab@github.com</code>, please include <code class="language-plaintext highlighter-rouge">GHSL-2021-075</code> in any communication regarding this issue.</p>


    