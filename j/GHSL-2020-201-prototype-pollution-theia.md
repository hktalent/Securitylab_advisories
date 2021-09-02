<header class="post-header d-block mb-6">
      <div class="date text-mono f5 my-3">January 26, 2021</div>
      <h1 class="my-2 h00-mktg lh-condensed">GHSL-2020-201: Prototype pollution in theia/plugin-ext</h1>

      
      
      
      
      

      

      <a target="_blank" class="sc-frDJqD SgxRc d-inline-flex flex-row flex-items-center text-gray" href="https://github.com/ghsecuritylab">
        <img class="mr-3" src="https://avatars.githubusercontent.com/u/61799930?s=35" height="35" width="35">
        <span>GitHub Security Lab</span>
      </a>
    </header>

    <main id="content" class="markdown-body" aria-label="Content">
      <h2 id="coordinated-disclosure-timeline">Coordinated Disclosure Timeline</h2>
<ul>
  <li>10/19/2020: Report sent to Anton Kosyakov <a href="mailto:anton.kosyakov@typefox.io">anton.kosyakov@typefox.io</a></li>
  <li>10/20/2020: Report sent to project leads Sven Efftinge <a href="mailto:sven.efftinge@typefox.io">sven.efftinge@typefox.io</a> and Marc Dumais <a href="mailto:marc.dumais@ericsson.com">marc.dumais@ericsson.com</a></li>
  <li>10/21/2020: Report sent to Florent Benoit <a href="mailto:florent@redhat.com">florent@redhat.com</a></li>
  <li>10/28/2020: Proposed fix shared with GHSL</li>
  <li>10/30/2020: Fix is merged</li>
</ul>

<h2 id="summary">Summary</h2>

<p>Prototype pollution in <code class="language-plaintext highlighter-rouge">mergeContents</code> and <code class="language-plaintext highlighter-rouge">parseConfigurationData</code> functions.</p>

<h2 id="product">Product</h2>

<p>https://www.npmjs.com/package/@theia/plugin-ext</p>

<h2 id="tested-version">Tested Version</h2>

<p>Latest commit</p>

<h2 id="details">Details</h2>

<p>The package contains <a href="https://github.com/eclipse-theia/theia/blob/6bc8d7593822a30c02bbc725387da21c0ecbe554/packages/plugin-ext/src/plugin/preferences/configuration.ts#L144">a merge function</a> for recursively merging two configuration objects. It does not check for problematic properties like <code class="language-plaintext highlighter-rouge">__proto__</code>, and hence it is vulnerable to prototype pollution. Specifically, if the <code class="language-plaintext highlighter-rouge">target</code> parameter to this function is under the control of an attacker, they can supply a specially crafted object that causes the function to overwrite properties on <code class="language-plaintext highlighter-rouge">Object.prototype</code> or add new properties to it. These properties are then inherited by every object in the program.</p>

<p>Here is an example, in which we assume that <code class="language-plaintext highlighter-rouge">payload</code> is provided by an attacker, and <code class="language-plaintext highlighter-rouge">isAdmin</code> is a property that is later on used to check whether a user is authorized to perform some sensitive operation:</p>

<div class="language-js highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="kd">const</span> <span class="nx">ConfigurationModel</span> <span class="o">=</span> <span class="nx">require</span><span class="p">(</span><span class="dl">'</span><span class="s1">@theia/plugin-ext/lib/plugin/preferences/configuration</span><span class="dl">'</span><span class="p">).</span><span class="nx">ConfigurationModel</span><span class="p">;</span>
<span class="kd">var</span> <span class="nx">payload</span> <span class="o">=</span> <span class="nx">JSON</span><span class="p">.</span><span class="nx">parse</span><span class="p">(</span><span class="dl">'</span><span class="s1">{"__proto__":{"isAdmin": true}}</span><span class="dl">'</span><span class="p">);</span>
<span class="k">new</span> <span class="nx">ConfigurationModel</span><span class="p">().</span><span class="nx">merge</span><span class="p">(</span><span class="k">new</span> <span class="nx">ConfigurationModel</span><span class="p">(</span><span class="nx">payload</span><span class="p">));</span>
</code></pre></div></div>

<p>After this code has run, <code class="language-plaintext highlighter-rouge">Object.prototype.isAdmin</code> is true. But <code class="language-plaintext highlighter-rouge">Object.prototype</code> is on the prototype chain of most objects, so we also have <code class="language-plaintext highlighter-rouge">{}.isAdmin == true</code>, and indeed <code class="language-plaintext highlighter-rouge">u.isAdmin == true</code> for most other objects <code class="language-plaintext highlighter-rouge">u</code>, including, perhaps, objects used to represent users.</p>

<p>We haven’t been able to trace the provenance of the <code class="language-plaintext highlighter-rouge">target</code> parameter all the way back to its source, but looks to us like it may come from a configuration file. If that is true and a user’s IDE is set up to automatically import configuration files in projects that are opened in the IDE, then an attacker can exploit the vulnerability by putting a crafted configuration file into an otherwise innocuous open-source project.</p>

<p>In addition, <a href="https://github.com/eclipse-theia/theia/blob/6bc8d7593822a30c02bbc725387da21c0ecbe554/packages/plugin-ext/src/plugin/preference-registry.ts#L240">parseConfigurationData</a>  also seems to be vulnerable to prototype pollution: if <code class="language-plaintext highlighter-rouge">data</code> contains a property named <code class="language-plaintext highlighter-rouge">__proto__.isAdmin</code>, the function will overwrite the <code class="language-plaintext highlighter-rouge">Object.prototype.isAdmin</code> property with the value of that property.</p>

<h4 id="impact">Impact</h4>

<p>Information Disclosure, Escalation of Privileges</p>

<h2 id="credit">Credit</h2>

<p>This issue was discovered and reported by GitHub team member <a href="https://github.com/max-schaefer">@max-schaefer (Max Schaefer)</a>.</p>

<h2 id="contact">Contact</h2>

<p>You can contact the GHSL team at <code class="language-plaintext highlighter-rouge">securitylab@github.com</code>, please include <code class="language-plaintext highlighter-rouge">GHSL-2020-201</code> in any communication regarding this issue.</p>

