<header class="post-header d-block mb-6">
      <div class="date text-mono f5 my-3">August 3, 2021</div>
      <h1 class="my-2 h00-mktg lh-condensed">GHSL-2021-098: ReDoS in OpenProject - CVE-2021-32763</h1>

      
      
      
      
      

      

      <a target="_blank" class="sc-frDJqD SgxRc d-inline-flex flex-row flex-items-center text-gray" href="https://github.com/ghsecuritylab">
        <img class="mr-3" src="https://avatars.githubusercontent.com/u/61799930?s=35" height="35" width="35">
        <span>GitHub Security Lab</span>
      </a>
    </header>

    <main id="content" class="markdown-body" aria-label="Content">
      
<h2 id="coordinated-disclosure-timeline">Coordinated Disclosure Timeline</h2>

<ul>
  <li>2021/07/12: Report sent to maintainers</li>
  <li>2021/07/12: Report acknowledged</li>
  <li>2021/07/13: Maintainers proposed a patch</li>
  <li>2021/07/13: Issue was fixed</li>
</ul>

<h2 id="summary">Summary</h2>

<p>A user of the system can post a message on a forum containing a specifically crafted string that will trigger a <a href="https://en.wikipedia.org/wiki/ReDoS">ReDoS</a> vulnerability.</p>

<h2 id="product">Product</h2>

<p>OpenProject</p>

<h2 id="tested-version">Tested Version</h2>

<p>OpenProject 11.3.2</p>

<h2 id="issue-details">Issue details</h2>

<p>The <code class="language-plaintext highlighter-rouge">MessagesController</code> class has a <code class="language-plaintext highlighter-rouge">quote</code> method that implements the logic behind the Quote button in the discussion forums, and it uses the following regex to strip <code class="language-plaintext highlighter-rouge">&lt;pre&gt;</code> tags from the message being quoted (<a href="https://github.com/opf/openproject/blob/0981c65582d734cc8cf2c37f192b42341a11cb0e/app/controllers/messages_controller.rb#L147">app/controllers/messages_controller.rb#L147</a>):</p>

<div class="language-rb highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="n">text</span><span class="p">.</span><span class="nf">to_s</span><span class="p">.</span><span class="nf">strip</span><span class="p">.</span><span class="nf">gsub</span><span class="p">(</span><span class="sr">%r{&lt;pre&gt;((.|</span><span class="se">\s</span><span class="sr">)*?)&lt;/pre&gt;}m</span><span class="p">,</span> <span class="s1">'[...]'</span><span class="p">)</span>
</code></pre></div></div>

<p>The <code class="language-plaintext highlighter-rouge">(.|\s)</code> part can match a space character in two ways, so an unterminated <code class="language-plaintext highlighter-rouge">&lt;pre&gt;</code> tag containing <code class="language-plaintext highlighter-rouge">n</code> spaces will cause Ruby’s regex engine to backtrack to try 2<sup>n</sup> states in the NFA. For example:</p>

<div class="language-plaintext highlighter-rouge"><div class="highlight"><pre class="highlight"><code>irb(main):009:0&gt; text = '&lt;pre&gt;                           &lt;/pre'
processing time: 0.000026s
=&gt; "&lt;pre&gt;                           &lt;/pre"
irb(main):010:0&gt; text.to_s.strip.gsub(%r{&lt;pre&gt;((.|\s)*?)&lt;/pre&gt;}m, '[...]')
processing time: 21.166936s
=&gt; "&lt;pre&gt;                           &lt;/pre"
</code></pre></div></div>

<h3 id="impact">Impact</h3>

<p>Denial of Service</p>

<h2 id="credit">Credit</h2>

<p>This issue was discovered by <a href="https://github.com/nickrolfe">@nickrolfe (Nick Rolfe)</a> from the GitHub CodeQL team.</p>

<h2 id="contact">Contact</h2>

<p>You can contact the GHSL team at <code class="language-plaintext highlighter-rouge">securitylab@github.com</code>. Please include <code class="language-plaintext highlighter-rouge">GHSL-2021-098</code> in any communication regarding this issue.</p>


  