<header class="post-header d-block mb-6">
      <div class="date text-mono f5 my-3">March 25, 2021</div>
      <h1 class="my-2 h00-mktg lh-condensed">GHSL-2020-235: Arbitrary command injection in wayou/turn-issues-to-posts-action</h1>

      
      
      
      
      

      

      <a target="_blank" class="sc-frDJqD SgxRc d-inline-flex flex-row flex-items-center text-gray" href="https://github.com/jarlob">
        <img class="mr-3" src="https://avatars.githubusercontent.com/u/26652396?s=35" height="35" width="35">
        <span>Jaroslav Lobacevski</span>
      </a>
    </header>

    <main id="content" class="markdown-body" aria-label="Content">
      <h2 id="coordinated-disclosure-timeline">Coordinated Disclosure Timeline</h2>

<ul>
  <li>2020-11-23: Report sent to maintainer.</li>
  <li>2020-12-09: Maintainer acknowledges.</li>
  <li>2021-02-23: Email sent to the maintainer, no response.</li>
  <li>2021-02-23: Disclosure deadline reached.</li>
  <li>2021-03-25: Publication as per our <a href="https://securitylab.github.com/advisories/#policy">disclosure policy</a>.</li>
</ul>

<h2 id="summary">Summary</h2>

<p>The <a href="https://github.com/wayou/turn-issues-to-posts-action/blob/f726de2eb1774398a20db79d3d4e90977cf8944c/action.yml">turn-issues-to-posts action</a> is vulnerable to arbitrary command injection.</p>

<h2 id="product">Product</h2>

<p><a href="https://github.com/wayou/turn-issues-to-posts-action">turn-issues-to-posts action</a></p>

<h2 id="tested-version">Tested Version</h2>

<p>The latest <a href="https://github.com/wayou/turn-issues-to-posts-action/blob/f726de2eb1774398a20db79d3d4e90977cf8944c/action.yml">changeset</a> to the date.</p>

<h2 id="details">Details</h2>

<h3 id="issue-the-title-of-an-issue-is-used-to-format-a-shell-command">Issue: The title of an issue is used to format a shell command</h3>

<p>The title of an issue is used to format a bash script like:</p>

<div class="language-yaml highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="nn">...</span>
      <span class="na">run</span><span class="pi">:</span> <span class="pi">|</span>
        <span class="s">DATE="${{ inputs.created_at }}"</span>
        <span class="s">mkdir -p ${{ inputs.dir }}</span>
        <span class="s">cat &lt;&lt;'EOF' &gt; _posts/"${DATE:0:10}-${{ github.event.issue.title }}".md</span>
<span class="s">...</span>
</code></pre></div></div>

<h4 id="impact">Impact</h4>

<p>This vulnerability allows for arbitrary command injection into the bash script. As a consequence, attackers may be able to exfiltrate secret tokens. As a proof of concept, an issue with the following title <code class="language-plaintext highlighter-rouge">a".md; echo "test" #</code> will print <code class="language-plaintext highlighter-rouge">test</code> in the action log.</p>

<h2 id="credit">Credit</h2>

<p>This issue was discovered and reported by GHSL team member <a href="https://github.com/JarLob">@JarLob (Jaroslav Lobačevski)</a>.</p>

<h2 id="contact">Contact</h2>

<p>You can contact the GHSL team at <code class="language-plaintext highlighter-rouge">securitylab@github.com</code>, please include a reference to <code class="language-plaintext highlighter-rouge">GHSL-2020-235</code> in any communication regarding this issue.</p>

   