<header class="post-header d-block mb-6">
      <div class="date text-mono f5 my-3">April 28, 2020</div>
      <h1 class="my-2 h00-mktg lh-condensed">GHSL-2020-085: Open redirect vulnerability in Sourcegraph - CVE-2020-12283</h1>

      
      
      
      
      

      

      <a target="_blank" class="sc-frDJqD SgxRc d-inline-flex flex-row flex-items-center text-gray" href="https://github.com/pwntester">
        <img class="mr-3" src="https://avatars.githubusercontent.com/u/125701?s=35" height="35" width="35">
        <span>Alvaro Munoz</span>
      </a>
    </header>

    <main id="content" class="markdown-body" aria-label="Content">
      <h2 id="summary">Summary</h2>
<p>An open redirect vulnerability has been found on Sourcegraph due to improper validation in the <code class="language-plaintext highlighter-rouge">SafeRedirectURL</code> method, as a consequence an attacker could potentially redirect a victim to any arbitrary URL and access their OAUTH token.</p>

<h2 id="product">Product</h2>
<p>Sourcegraph</p>

<h2 id="cve">CVE</h2>
<p>CVE-2020-12283</p>

<h2 id="tested-version">Tested Version</h2>
<p>Tested on <a href="https://github.com/sourcegraph/sourcegraph">master</a> branch up to afcd7cf010d2508bfb8393fcf9c4497dc0099180</p>

<h2 id="details">Details</h2>

<p>An open redirect is a security vulnerability in which a website endpoint accepts a URL as input and and then redirects to the user-provided URL. This type of vulnerability can be used for e.g. phishing attacks in which an attacker abuses the trust relationship a victim has with the redirecting site to redirect to a malicious site. 
A more serious attack may occur when an application implements an oauth flow. In this scenario an attacker can abuse e.g. external service authentication (think “Login with Facebook/Google/GitHub/etc”) to redirect users to an attacker controlled site, where they will then steal the partial oauth token.</p>

<p>A good example of this type of vulnerability can be found in this <a href="https://github.com/oauth2-proxy/oauth2-proxy/security/advisories/GHSA-qqxw-m5fj-f7gv">OAuth2 advisory</a></p>

<p><code class="language-plaintext highlighter-rouge">SafeRedirectURL</code> relies on <code class="language-plaintext highlighter-rouge">url.Parse</code> and <code class="language-plaintext highlighter-rouge">u.Path</code> to extract the relative path. <code class="language-plaintext highlighter-rouge">SafeRedirectURL</code> will transform any absolute URLs starting with <code class="language-plaintext highlighter-rouge">//</code> into <code class="language-plaintext highlighter-rouge">/</code> and any absolute URLs starting with <code class="language-plaintext highlighter-rouge">/\\</code> will be URL encoded into <code class="language-plaintext highlighter-rouge">/%5C</code>. However, when <code class="language-plaintext highlighter-rouge">url.Parse</code> parses the URL it will NOT normalize double slashes (e.g: <code class="language-plaintext highlighter-rouge">u.Path</code> will return <code class="language-plaintext highlighter-rouge">//bar</code> for <code class="language-plaintext highlighter-rouge">http://foo.com//bar</code>). An attacker can abuse this behavior by crafting an URL like <code class="language-plaintext highlighter-rouge">//foo//example.com</code> so that <code class="language-plaintext highlighter-rouge">u.Path</code> will return <code class="language-plaintext highlighter-rouge">//example.com</code> which, when sent to the browser, will make it visit the absolute URL <code class="language-plaintext highlighter-rouge">http://example.com</code>.</p>

<div class="language-go highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="k">func</span> <span class="n">SafeRedirectURL</span><span class="p">(</span><span class="n">urlStr</span> <span class="kt">string</span><span class="p">)</span> <span class="kt">string</span> <span class="p">{</span>
        <span class="n">u</span><span class="p">,</span> <span class="n">err</span> <span class="o">:=</span> <span class="n">url</span><span class="o">.</span><span class="n">Parse</span><span class="p">(</span><span class="n">urlStr</span><span class="p">)</span>
        <span class="k">if</span> <span class="n">err</span> <span class="o">!=</span> <span class="no">nil</span> <span class="o">||</span> <span class="o">!</span><span class="n">strings</span><span class="o">.</span><span class="n">HasPrefix</span><span class="p">(</span><span class="n">u</span><span class="o">.</span><span class="n">Path</span><span class="p">,</span> <span class="s">"/"</span><span class="p">)</span> <span class="p">{</span>
                <span class="k">return</span> <span class="s">"/"</span>
        <span class="p">}</span>
</code></pre></div></div>
<p>The vulnerability was found using the following <a href="https://codeql.com">CodeQL</a> query:</p>

<pre><code class="language-ql">/**
 * @name Open redirect due to sanitzation bypass
 * @kind path-problem
 * @problem.severity medium
 * @id go/example/hasprefix
 */

import go
import DataFlow::PathGraph
 
 predicate prefixCheck(StringOps::HasPrefix call, DataFlow::Node checked, Variable v, string prefix) {
   checked = call.getBaseString() and
   prefix = call.getSubstring().getStringValue() and
   v.getARead() = checked 
 }

predicate insuffcientPrefixCheck(StringOps::HasPrefix call, DataFlow::Node checked, Variable v) {
    prefixCheck(call, checked, v, "/")  and
    (not prefixCheck(_, _, v, "//") or not prefixCheck(_, _, v, "/\\"))

}

class BadRedirectConfig extends TaintTracking::Configuration {
  BadRedirectConfig() { this = "BadRedirectConfig" }
  override predicate isSource(DataFlow::Node source) {
    source instanceof UntrustedFlowSource
  }
  override predicate isSink(DataFlow::Node sink) {
        insuffcientPrefixCheck(_, sink, _)
  }
}

from DataFlow::PathNode source, DataFlow::PathNode sink, BadRedirectConfig cfg
where cfg.hasFlowPath(source, sink)
select sink, source, sink, "Bad redirect check on untrusted data from $@", source, "this source"
</code></pre>

<h3 id="impact">Impact</h3>

<p>The full impact of this vulnerability depends on the context of use. While open redirect issues can aid phishing attacks, it also seems that <code class="language-plaintext highlighter-rouge">SafeRedirectURL</code> is used in Sourcegraph’s OAuth flow which may lead to token hijacks.</p>

<h3 id="remediation">Remediation</h3>

<p>The vulnerability has been fixed in Sourcegraph v3.14.4 and v3.15.1</p>

<h2 id="coordinated-disclosure-timeline">Coordinated Disclosure Timeline</h2>
<ul>
  <li>2020-04-23: reported to security@sourcegraph.com</li>
  <li>2020-04-23: acknowledge received from Sourcegraph security team</li>
  <li>2020-04-24: vulnerability fixed and deployed <a href="https://github.com/sourcegraph/sourcegraph/pull/10167">sourcegraph/sourcegraph#10167</a></li>
  <li>2020-04-27: CVE assigned CVE-2020-12283</li>
  <li>2020-04-28: Patch releases for version 3.14.4 and 3.15.1.</li>
  <li>2020-04-30: Sourcegraph issued a GitHub security advisory and notified all affected users.</li>
</ul>

<h2 id="references">References</h2>
<ul>
  <li><a href="https://github.com/sourcegraph/sourcegraph/security/advisories/GHSA-mx43-r985-5h4m">Sourcegraph advisory</a></li>
  <li><a href="https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2020-12283">CVE-2020-12283</a></li>
  <li><a href="https://github.com/sourcegraph/sourcegraph/pull/10167">Vulnerability fix</a></li>
</ul>

<h2 id="credit">Credit</h2>

<p>This issue was discovered and reported by GHSL team members <a href="https://github.com/nicowaisman">@nicowaisman (Nico Waisman)</a>, <a href="https://github.com/nicowaisman">@pwntester (Alvaro Munoz)</a> and <a href="https://github.com/sauyon">@sauyon (Sauyon Lee)</a>.</p>

<h2 id="contact">Contact</h2>

<p>You can contact the GHSL team at <code class="language-plaintext highlighter-rouge">securitylab@github.com</code>, please include the <code class="language-plaintext highlighter-rouge">GHSL-2020-085</code> in any communication regarding this issue.</p>