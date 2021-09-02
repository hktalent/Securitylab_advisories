<header class="post-header d-block mb-6">
      <div class="date text-mono f5 my-3">March 12, 2020</div>
      <h1 class="my-2 h00-mktg lh-condensed">GHSL-2020-001: Off-by-one heap overflow in Bftpd</h1>

      
      
      
      
      

      

      <a target="_blank" class="sc-frDJqD SgxRc d-inline-flex flex-row flex-items-center text-gray" href="https://github.com/antonio-morales">
        <img class="mr-3" src="https://avatars.githubusercontent.com/u/55253029?s=35" height="35" width="35">
        <span>Antonio Morales</span>
      </a>
    </header>

    <main id="content" class="markdown-body" aria-label="Content">
      <h2 id="summary">Summary</h2>

<p>Under certain circumstances, an off-by-one heap overflow can occur in the <code class="language-plaintext highlighter-rouge">command_retr</code> function.</p>

<h2 id="product">Product</h2>
<p>Bftpd</p>

<h2 id="tested-version">Tested Version</h2>
<p>Bftpd 5.3</p>

<h2 id="details">Details</h2>

<h3 id="multiple-int-to-bool-casting-vulnerabilities-leading-to-heap-overflow">Multiple int-to-bool casting vulnerabilities, leading to heap overflow</h3>

<p>The <code class="language-plaintext highlighter-rouge">command_retr</code> function in <code class="language-plaintext highlighter-rouge">commands.c</code> executes <code class="language-plaintext highlighter-rouge">while ((i = read(phile, buffer, my_buffer_size)))</code>, but under certain circumstances <code class="language-plaintext highlighter-rouge">read</code> can <a href="https://linux.die.net/man/2/read">return -1</a>.</p>

<p>In this case, the problem is that the <code class="language-plaintext highlighter-rouge">while</code> condition will be evaluated as true because in the C programming language all non-zero values are considered true.</p>

<p>As a result, an off-by-one out of bounds write into heap memory will be triggered when <code class="language-plaintext highlighter-rouge">buffer[-1] = '\0'</code> is executed.</p>

<p>This is a medium-low severity vulnerability.</p>

<h4 id="impact">Impact</h4>

<p>Heap memory corruption with a single nul byte.</p>

<h2 id="coordinated-disclosure-timeline">Coordinated Disclosure Timeline</h2>
<p>This report was subject to our <a href="https://securitylab.github.com/advisories/#policy">coordinated disclosure policy</a>.</p>
<ul>
  <li>01/09/2020: Report sent to Vendor</li>
  <li>01/09/2020: Vendor acknowledged report</li>
  <li>01/10/2020: Vendor published fix</li>
</ul>

<h2 id="supporting-resources">Supporting Resources</h2>
<ul>
  <li><a href="/assets/advisories-resources/GHSL-2020-001-ASAN.txt">ASAN report</a></li>
</ul>

<h2 id="credit">Credit</h2>

<p>This issue was discovered and reported by GHSL team member <a href="https://github.com/antonio-morales">@antonio-morales (Antonio Morales)</a>.</p>

<h2 id="contact">Contact</h2>

<p>You can contact the GHSL team at <code class="language-plaintext highlighter-rouge">securitylab@github.com</code>, please include the <code class="language-plaintext highlighter-rouge">GHSL-YEAR-ID</code> in any communication regarding this issue.</p>

    