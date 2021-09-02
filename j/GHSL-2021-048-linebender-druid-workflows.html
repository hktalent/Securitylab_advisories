<header class="post-header d-block mb-6">
      <div class="date text-mono f5 my-3">February 24, 2021</div>
      <h1 class="my-2 h00-mktg lh-condensed">GHSL-2021-048: Unauthorized repository modification or secrets exfiltration in several GitHub workflows of linebender</h1>

      
      
      
      
      

      

      <a target="_blank" class="sc-frDJqD SgxRc d-inline-flex flex-row flex-items-center text-gray" href="https://github.com/jarlob">
        <img class="mr-3" src="https://avatars.githubusercontent.com/u/26652396?s=35" height="35" width="35">
        <span>Jaroslav Lobacevski</span>
      </a>
    </header>

    <main id="content" class="markdown-body" aria-label="Content">
      <h2 id="coordinated-disclosure-timeline">Coordinated Disclosure Timeline</h2>

<ul>
  <li>2021-02-04: Issue reported to maintainers</li>
  <li>2021-02-04: Report acknowledged</li>
  <li>2021-02-23: Issue fixed</li>
</ul>

<h2 id="summary">Summary</h2>

<p>The <code class="language-plaintext highlighter-rouge">bloat.yml</code> GitHub workflow in <a href="https://github.com/linebender/druid/blob/master/.github/workflows/bloat.yml">linebender/druid</a>, <a href="https://github.com/linebender/runebender/blob/master/.github/workflows/bloat.yml">linebender/runebender</a> and <a href="https://github.com/linebender/norad/blob/master/.github/workflows/bloat.yml">linebender/norad</a> is vulnerable to unauthorized modification of the base repository or secrets exfiltration.</p>

<h2 id="product">Product</h2>

<p><a href="https://github.com/linebender/druid">linebender/druid</a> repository<br />
<a href="https://github.com/linebender/runebender">linebender/runebender</a> repository<br />
<a href="https://github.com/linebender/norad">linebender/norad</a> repository</p>

<h2 id="tested-version">Tested Version</h2>

<p>The latest version of <code class="language-plaintext highlighter-rouge">bloat.yml</code> to the date.</p>

<h2 id="details">Details</h2>

<h3 id="issue-a-specific-comment-triggers-a-potentially-untrusted-pull-request-build-in-a-privileged-environment">Issue: A specific comment triggers a potentially untrusted pull request build in a privileged environment</h3>

<p>When a user comments on a pull request it triggers the following workflow, that checks out the pull request and builds the potentially untrusted code:</p>

<div class="language-yaml highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="na">on</span><span class="pi">:</span>
  <span class="na">issue_comment</span><span class="pi">:</span>
    <span class="na">types</span><span class="pi">:</span> <span class="pi">[</span><span class="nv">created</span><span class="pi">,</span> <span class="nv">edited</span><span class="pi">]</span>
<span class="nn">...</span>
    <span class="c1"># if it isn't an issue comment run every time, otherwise only run if the comment starts with '/bloat'</span>
    <span class="na">if</span><span class="pi">:</span> <span class="s">(!startsWith(github.event_name, 'issue_comment') || startsWith(github.event.comment.body, '/bloat'))</span>
    <span class="na">steps</span><span class="pi">:</span>
<span class="nn">...</span>
      <span class="pi">-</span> <span class="na">name</span><span class="pi">:</span> <span class="s">build head</span>
        <span class="na">if</span><span class="pi">:</span> <span class="s">steps.get_revs.outputs.base != steps.get_revs.outputs.head</span>
        <span class="na">uses</span><span class="pi">:</span> <span class="s">actions-rs/cargo@v1</span>
        <span class="na">with</span><span class="pi">:</span>
          <span class="na">command</span><span class="pi">:</span> <span class="s">build</span>
          <span class="na">args</span><span class="pi">:</span> <span class="s">--release --examples</span>
</code></pre></div></div>

<h4 id="impact">Impact</h4>

<p>The triggered workflow has access to the write repository token and secrets. The vulnerability allows for unauthorized modification of the base repository and secrets exfiltration.</p>

<h2 id="credit">Credit</h2>

<p>This issue was discovered and reported by GHSL team member <a href="https://github.com/JarLob">@JarLob (Jaroslav Lobačevski)</a>.</p>

<h2 id="contact">Contact</h2>

<p>You can contact the GHSL team at <code class="language-plaintext highlighter-rouge">securitylab@github.com</code>, please include a reference to <code class="language-plaintext highlighter-rouge">GHSL-2021-048</code> in any communication regarding this issue.</p>

   