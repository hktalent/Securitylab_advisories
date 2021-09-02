<header class="post-header d-block mb-6">
      <div class="date text-mono f5 my-3">June 17, 2020</div>
      <h1 class="my-2 h00-mktg lh-condensed">GHSL-2020-099: mXSS vulnerability in AngularJS</h1>

      
      
      
      
      

      

      <a target="_blank" class="sc-frDJqD SgxRc d-inline-flex flex-row flex-items-center text-gray" href="https://github.com/pwntester">
        <img class="mr-3" src="https://avatars.githubusercontent.com/u/125701?s=35" height="35" width="35">
        <span>Alvaro Munoz</span>
      </a>
    </header>

    <main id="content" class="markdown-body" aria-label="Content">
      <h2 id="summary">Summary</h2>

<p>Potential mXSS in AngularJS</p>

<h2 id="product">Product</h2>

<p>AngularJS</p>

<h2 id="tested-version">Tested Version</h2>

<p>Latest vulnerable version: 1.7.9 (master, 418355f1cf9a9a9827ae81d257966e6acfb5623a)</p>

<h2 id="details-potential-mxss">Details: Potential mXSS</h2>

<p>jQuery’s <code class="language-plaintext highlighter-rouge">htmlPrefilter</code> functionality is considered unsafe as of <a href="https://github.com/advisories/GHSA-gxr4-xjj5-5px2">CVE-2020-11022</a>, see additional details here: <a href="https://github.com/advisories/GHSA-gxr4-xjj5-5px2">GHSA-gxr4-xjj5-5px2</a>. The problem was that <code class="language-plaintext highlighter-rouge">htmlPrefilter</code> enabled new mXSS attacks when expanding self-closing tags (<code class="language-plaintext highlighter-rouge">&lt;tag/&gt;</code>). This function will apply a regular expression to convert <code class="language-plaintext highlighter-rouge">&lt;tag/&gt;</code> into <code class="language-plaintext highlighter-rouge">&lt;tag&gt;&lt;/tag&gt;</code>:</p>

<div class="language-javascript highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="nx">rxhtmlTag</span> <span class="o">=</span> <span class="sr">/&lt;</span><span class="se">(?!</span><span class="sr">area|br|col|embed|hr|img|input|link|meta|param</span><span class="se">)(([</span><span class="sr">a-z</span><span class="se">][^\/\0</span><span class="sr">&gt;</span><span class="se">\x</span><span class="sr">20</span><span class="se">\t\r\n\f]</span><span class="sr">*</span><span class="se">)[^</span><span class="sr">&gt;</span><span class="se">]</span><span class="sr">*</span><span class="se">)\/</span><span class="sr">&gt;/gi</span>
 <span class="p">...</span>

<span class="nx">htmlPrefilter</span><span class="p">:</span> <span class="kd">function</span><span class="p">(</span> <span class="nx">html</span> <span class="p">)</span> <span class="p">{</span>
    <span class="k">return</span> <span class="nx">html</span><span class="p">.</span><span class="nx">replace</span><span class="p">(</span> <span class="nx">rxhtmlTag</span><span class="p">,</span> <span class="dl">"</span><span class="s2">&lt;$1&gt;&lt;/$2&gt;</span><span class="dl">"</span> <span class="p">);</span>
    <span class="k">return</span> <span class="nx">html</span><span class="p">;</span>
<span class="p">}</span>
</code></pre></div></div>

<p>If developers sanitize untrusted HTML (e.g.: using DOMPurify) and then pass the clean HTML into this filter (e.g.: when calling <code class="language-plaintext highlighter-rouge">jQuery()</code>), the resulting HTML may mutate into dangerous HTML. For example, the following image tag with two string literal attributes:</p>

<div class="language-html highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="nt">&lt;img</span> <span class="na">alt=</span><span class="s">"&lt;x"</span> <span class="na">title=</span><span class="s">"/&gt;&lt;img src=url404 onerror=alert(0)&gt;"</span><span class="nt">&gt;</span>
</code></pre></div></div>

<p>will mutate into:</p>

<div class="language-html highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="nt">&lt;img</span> <span class="na">alt=</span><span class="s">"&lt;x"</span> <span class="na">title=</span><span class="s">"&gt;&lt;/x"</span><span class="nt">&gt;&lt;img</span> <span class="na">src=</span><span class="s">url404</span> <span class="na">onerror=</span><span class="s">alert(0)</span><span class="nt">&gt;</span>"&gt;
</code></pre></div></div>

<p>Additional attack vectors can be found in <a href="https://github.com/jquery/jquery/pull/4685/files#diff-328a9410239da61336e3662fdbfe9bf6R2950-R2962">jQuery tests</a>.</p>

<p>Note that while some of these test-strings seem suspicious, they will not actually cause code to be run unless they are transformed by the unsafe <code class="language-plaintext highlighter-rouge">htmlPrefilter</code>.</p>

<p>AngularJS’ jqLite contains a port of jQuery’s <code class="language-plaintext highlighter-rouge">htmlPrefilter</code> functionality, and is vulnerable to some of the same attack vectors. See this example which will show an alert:</p>

<div class="language-javascript highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="o">&lt;</span><span class="nx">html</span><span class="o">&gt;</span>
  <span class="o">&lt;</span><span class="nx">head</span><span class="o">&gt;</span>
    <span class="o">&lt;</span><span class="nx">script</span> <span class="nx">type</span><span class="o">=</span><span class="dl">"</span><span class="s2">text/javascript</span><span class="dl">"</span> <span class="nx">src</span><span class="o">=</span><span class="dl">"</span><span class="s2">./angular.js</span><span class="dl">"</span><span class="o">&gt;&lt;</span><span class="sr">/script&gt;&lt;/</span><span class="nx">head</span><span class="o">&gt;</span>
  <span class="o">&lt;</span><span class="nx">body</span><span class="o">&gt;</span>
    <span class="o">&lt;</span><span class="nx">script</span> <span class="nx">type</span><span class="o">=</span><span class="dl">"</span><span class="s2">text/javascript</span><span class="dl">"</span><span class="o">&gt;</span>
      <span class="nx">angular</span><span class="p">.</span><span class="nx">element</span><span class="p">(</span><span class="dl">"</span><span class="s2">&lt;noscript&gt;&lt;noscript/&gt;&lt;img src=url404 onerror=alert()&gt;</span><span class="dl">"</span><span class="p">);</span>
    <span class="o">&lt;</span><span class="sr">/script</span><span class="err">&gt;
</span>  <span class="o">&lt;</span><span class="sr">/body</span><span class="err">&gt;
</span><span class="o">&lt;</span><span class="sr">/html</span><span class="err">&gt;
</span></code></pre></div></div>

<h3 id="impact">Impact</h3>

<p>This issue may lead to a Cross-Site Scripting vulnerability (mXSS)</p>

<h2 id="cves">CVEs</h2>

<p>N/A at time of publication (3rd party applicant)</p>

<h2 id="coordinated-disclosure-timeline">Coordinated Disclosure Timeline</h2>

<p>This report was subject to the GHSL <a href="https://securitylab.github.com/advisories/#policy">coordinated disclosure policy</a>.</p>

<ul>
  <li>05/12/2020: Report sent to <code class="language-plaintext highlighter-rouge">security@angular.io</code></li>
  <li>06/05/2020: Maintainer updates GHSL with fixed release version and commit</li>
</ul>

<h2 id="resources">Resources</h2>

<ul>
  <li>Fixed in commit: https://github.com/angular/angular.js/commit/2df43c07779137d1bddf7f3b282a1287a8634acd</li>
  <li>Release notes: https://github.com/angular/angular.js/blob/master/CHANGELOG.md#180-nested-vaccination-2020-06-01</li>
</ul>

<h2 id="credit">Credit</h2>

<p>This issue was discovered by Esben Sparre Andreasen (<a href="https://github.com/esbena">@esbena</a>) performing a Variant Analysis of <a href="https://github.com/advisories/GHSA-gxr4-xjj5-5px2">CVE-2020-11022</a> which was found and reported by Masato Kinugawa (<a href="https://github.com/masatokinugawa">@masatokinugawa</a>).</p>

<h2 id="contact">Contact</h2>

<p>You can contact the GHSL team at <code class="language-plaintext highlighter-rouge">securitylab@github.com</code>, please include <code class="language-plaintext highlighter-rouge">GHSL-2020-099</code> in any communication regarding this issue.</p>