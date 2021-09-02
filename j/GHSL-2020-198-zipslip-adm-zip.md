<header class="post-header d-block mb-6">
      <div class="date text-mono f5 my-3">February 3, 2021</div>
      <h1 class="my-2 h00-mktg lh-condensed">GHSL-2020-198: Path manipulation via Zip entry files (ZipSlip) in adm-zip</h1>

      
      
      
      
      

      

      <a target="_blank" class="sc-frDJqD SgxRc d-inline-flex flex-row flex-items-center text-gray" href="https://github.com/ghsecuritylab">
        <img class="mr-3" src="https://avatars.githubusercontent.com/u/61799930?s=35" height="35" width="35">
        <span>GitHub Security Lab</span>
      </a>
    </header>

    <main id="content" class="markdown-body" aria-label="Content">
      <h2 id="coordinated-disclosure-timeline">Coordinated Disclosure Timeline</h2>
<ul>
  <li>10/19/2020: Report sent to iacob.campia@gmail.com and sy@another-d-mention.ro as per https://registry.npmjs.org/adm-zip/latest</li>
  <li>01/18/2021: Sent request for status update to maintainers. Created <a href="https://github.com/cthackers/adm-zip/issues/343">public issue to request security contact</a></li>
  <li>01/27/2021: <a href="https://github.com/cthackers/adm-zip/commit/119dcad6599adccc77982feb14a0c7440fa63013">Fix published</a></li>
</ul>

<h2 id="summary">Summary</h2>

<p>Path manipulation via Zip entry files (ZipSlip)</p>

<h2 id="product">Product</h2>

<p>https://www.npmjs.com/package/adm-zip</p>

<h2 id="tested-version">Tested Version</h2>

<p>Latest commit</p>

<h2 id="details">Details</h2>

<p>The <a href="https://github.com/cthackers/adm-zip/wiki/ADM-ZIP#void-extractalltostring-targetpath-boolean-overwrite--false"><code class="language-plaintext highlighter-rouge">extractAllTo</code></a> method allows extracting all files in a zip file to a specified target folder. It tries to ensure that no files are extracted outside this folder, so even if zip file entries have paths containing <code class="language-plaintext highlighter-rouge">..</code> elements the files should still end up in the target folder.</p>

<p>However, the code to enforce this leaves a loophole: it is possible to extract files to a different folder as long as the path of the target folder is a prefix of the path of that other folder. For example, when extracting a specially crafted zip file to target folder <code class="language-plaintext highlighter-rouge">contents</code>, some files could end up in a sibling folder called <code class="language-plaintext highlighter-rouge">contents2</code>, or some other folder whose path starts with the string <code class="language-plaintext highlighter-rouge">contents</code>, as shown in this example:</p>

<div class="language-js highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="kd">const</span> <span class="nx">AdmZip</span> <span class="o">=</span> <span class="nx">require</span><span class="p">(</span><span class="dl">'</span><span class="s1">adm-zip</span><span class="dl">'</span><span class="p">)</span>
<span class="kd">const</span> <span class="nx">zip</span> <span class="o">=</span> <span class="k">new</span> <span class="nx">AdmZip</span><span class="p">()</span>
<span class="nx">zip</span><span class="p">.</span><span class="nx">addFile</span><span class="p">(</span><span class="dl">"</span><span class="s2">test.txt</span><span class="dl">"</span><span class="p">,</span> <span class="nx">Buffer</span><span class="p">.</span><span class="k">from</span><span class="p">(</span><span class="dl">"</span><span class="s2">hi</span><span class="dl">"</span><span class="p">))</span>
<span class="nx">zip</span><span class="p">.</span><span class="nx">addFile</span><span class="p">(</span><span class="dl">"</span><span class="s2">../contents2/test2.txt</span><span class="dl">"</span><span class="p">,</span> <span class="nx">Buffer</span><span class="p">.</span><span class="k">from</span><span class="p">(</span><span class="dl">"</span><span class="s2">there</span><span class="dl">"</span><span class="p">))</span>
<span class="nx">zip</span><span class="p">.</span><span class="nx">extractAllTo</span><span class="p">(</span><span class="dl">"</span><span class="s2">contents</span><span class="dl">"</span><span class="p">)</span> <span class="c1">// `test.txt` is extracted to `contents`, `test2.txt` to `contents2`</span>
</code></pre></div></div>

<p>Client code of adm-zip would probably assume that the check does not allow this cross-folder extraction, and might use it to extract even untrusted zip files. If an attacker can provide a crafted zip file, they might then be able to overwrite files outside the intended target folder.</p>

<p>In practice this is probably difficult to exploit since the paths have to match up as explained above but we think that even if this is arguably a relatively low-severity vulnerability, it is still worth fixing.</p>

<h4 id="impact">Impact</h4>

<p>File system manipulation, Data corruption</p>

<h2 id="credit">Credit</h2>

<p>This issue was discovered and reported by GitHub team member <a href="https://github.com/max-schaefer">@max-schaefer (Max Schaefer)</a>.</p>

<h2 id="contact">Contact</h2>

<p>You can contact the GHSL team at <code class="language-plaintext highlighter-rouge">securitylab@github.com</code>, please include <code class="language-plaintext highlighter-rouge">GHSL-2020-198</code> in any communication regarding this issue.</p>

    