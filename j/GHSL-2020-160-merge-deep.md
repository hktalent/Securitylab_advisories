<header class="post-header d-block mb-6">
      <div class="date text-mono f5 my-3">January 26, 2021</div>
      <h1 class="my-2 h00-mktg lh-condensed">GHSL-2020-160: Prototype pollution in Merge-deep</h1>

      
      
      
      
      

      

      <a target="_blank" class="sc-frDJqD SgxRc d-inline-flex flex-row flex-items-center text-gray" href="https://github.com/ghsecuritylab">
        <img class="mr-3" src="https://avatars.githubusercontent.com/u/61799930?s=35" height="35" width="35">
        <span>GitHub Security Lab</span>
      </a>
    </header>

    <main id="content" class="markdown-body" aria-label="Content">
      <h2 id="coordinated-disclosure-timeline">Coordinated Disclosure Timeline</h2>

<ul>
  <li>09/30/2020: maintainer notified</li>
  <li>01/04/2021: disclosure deadline, no maintainer response</li>
  <li>01/04/2021: created issue on project as final attempt to notify maintainer</li>
  <li>01/05/2021: maintainer acknowledges report and is working on a patch</li>
  <li>01/13/2021: version 3.03 released to npm</li>
</ul>

<h2 id="summary">Summary</h2>

<p>Merge-deep actively attempts to prevent prototype pollution by blocking object property merges into <code class="language-plaintext highlighter-rouge">__proto__</code>, however it still allows for prototype pollution of <code class="language-plaintext highlighter-rouge">Object.prototype</code> via a <code class="language-plaintext highlighter-rouge">constructor</code> payload.</p>

<h2 id="product">Product</h2>

<p><a href="https://github.com/jonschlinkert/merge-deep">merge-deep</a> 3.0.2 (latest version)</p>

<h2 id="tested-version">Tested Version</h2>

<p>3.0.2</p>

<h2 id="details">Details</h2>

<p><code class="language-plaintext highlighter-rouge">merge-deep</code> can be tricked into overwriting properties of <code class="language-plaintext highlighter-rouge">Object.prototype</code> or adding new properties to it. These properties are then inherited by every object in the program.</p>

<p>Here is an example, in which we assume that <code class="language-plaintext highlighter-rouge">payload</code> is provided by an attacker, and <code class="language-plaintext highlighter-rouge">isAdmin</code> is a property that is later on used to check whether a user is authorized to perform some sensitive operation:</p>

<div class="language-js highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="kd">var</span> <span class="nx">mergeDeep</span> <span class="o">=</span> <span class="nx">require</span><span class="p">(</span><span class="dl">"</span><span class="s2">merge-deep</span><span class="dl">"</span><span class="p">);</span>
<span class="kd">var</span> <span class="nx">payload</span> <span class="o">=</span> <span class="dl">'</span><span class="s1">{"constructor": {"prototype": {"isAdmin": true}}}</span><span class="dl">'</span><span class="p">;</span>
<span class="nx">mergeDeep</span><span class="p">({},</span> <span class="nx">JSON</span><span class="p">.</span><span class="nx">parse</span><span class="p">(</span><span class="nx">payload</span><span class="p">));</span>
</code></pre></div></div>

<p>After this code has run, <code class="language-plaintext highlighter-rouge">Object.prototype.isAdmin</code> is <code class="language-plaintext highlighter-rouge">true</code>. But <code class="language-plaintext highlighter-rouge">Object.prototype</code> is on the prototype chain of most objects, so we also have <code class="language-plaintext highlighter-rouge">{}.isAdmin == true</code>, and indeed <code class="language-plaintext highlighter-rouge">u.isAdmin == true</code> for most other objects <code class="language-plaintext highlighter-rouge">u</code>, including, perhaps, objects used to represent users.</p>

<p>It is important to note that the above code snippet throws an exception (since <code class="language-plaintext highlighter-rouge">Object.prototype</code> cannot be reassigned), but it still sets the property (since it can be mutated). In some settings this might make the vulnerability difficult to exploit, but in others (for example web servers, which generally are written to be tolerant to route-handler crashes) it will still be easily exploitable.</p>

<h4 id="impact">Impact</h4>

<p>JavaScript prototype pollution can lead to a variety of application context specific impacts ranging from Denial of Service (DoS) to Remote Code Execution (RCE).</p>

<h2 id="credit">Credit</h2>

<p>This issue was discovered and reported by GitHub team member <a href="https://github.com/max-schaefer">@max-schaefer</a>.</p>

<h2 id="contact">Contact</h2>

<p>You can contact the GHSL team at <code class="language-plaintext highlighter-rouge">securitylab@github.com</code>, please include <code class="language-plaintext highlighter-rouge">GHSL-2020-160</code> in any communication regarding this issue.</p>

    