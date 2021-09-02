<header class="post-header d-block mb-6">
      <div class="date text-mono f5 my-3">April 1, 2021</div>
      <h1 class="my-2 h00-mktg lh-condensed">GHSL-2021-046: Command injection in a GitHub workflow of AmazeFileManager</h1>

      
      
      
      
      

      

      <a target="_blank" class="sc-frDJqD SgxRc d-inline-flex flex-row flex-items-center text-gray" href="https://github.com/jarlob">
        <img class="mr-3" src="https://avatars.githubusercontent.com/u/26652396?s=35" height="35" width="35">
        <span>Jaroslav Lobacevski</span>
      </a>
    </header>

    <main id="content" class="markdown-body" aria-label="Content">
      
<h2 id="coordinated-disclosure-timeline">Coordinated Disclosure Timeline</h2>

<ul>
  <li>2021-02-04: Issue reported to maintainers</li>
  <li>2021-02-04: Issue fixed</li>
</ul>

<h2 id="summary">Summary</h2>

<p>The <a href="https://github.com/TeamAmaze/AmazeFileManager/blob/release/3.6/.github/workflows/android-debug-artifact-ondemand.yml">android-debug-artifact-ondemand.yml</a> GitHub workflow is vulnerable to command injection.</p>

<h2 id="product">Product</h2>

<p><a href="https://github.com/TeamAmaze/AmazeFileManager">TeamAmaze/AmazeFileManager</a> repository</p>

<h2 id="tested-version">Tested Version</h2>

<p>The latest changeset of <a href="https://github.com/TeamAmaze/AmazeFileManager/blob/2d0c8eccc1c77f4cd7d5cc287b771c2b05ddcb08/.github/workflows/android-debug-artifact-ondemand.yml">android-debug-artifact-ondemand.yml</a> to the date.</p>

<h2 id="details">Details</h2>

<h3 id="issue-a-branch-name-from-pull-request-is-used-to-format-inline-script">Issue: A branch name from pull request is used to format inline script</h3>

<div class="language-yaml highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="na">on</span><span class="pi">:</span>
<span class="nn">...</span>
  <span class="na">issue_comment</span><span class="pi">:</span>
    <span class="na">types</span><span class="pi">:</span> <span class="pi">[</span><span class="nv">created</span><span class="pi">]</span>

<span class="na">jobs</span><span class="pi">:</span>
  <span class="na">apk</span><span class="pi">:</span>
    <span class="na">runs-on</span><span class="pi">:</span> <span class="s">ubuntu-latest</span>
    <span class="na">if</span><span class="pi">:</span> <span class="s">github.event.comment.body == 'Build test apk' &amp;&amp; github.actor == 'VishalNehra' || github.actor == 'TranceLove' || github.actor == 'EmmanuelMess'</span>
    <span class="na">steps</span><span class="pi">:</span>
<span class="nn">...</span>
      <span class="pi">-</span> <span class="na">name</span><span class="pi">:</span> <span class="s">Get PR informations</span>
        <span class="na">id</span><span class="pi">:</span> <span class="s">pr_data</span>
        <span class="na">run</span><span class="pi">:</span> <span class="pi">|</span>
          <span class="s">echo "::set-output name=branch::${{ fromJson(steps.request.outputs.data).head.ref }}"</span>
</code></pre></div></div>

<p>A potentially untrusted branch name is used to format a shell script. As a safeguard, the workflow runs only if one of the three selected users comment on the pull request with “Build test apk”. However because of a mistake in the condition (logical <code class="language-plaintext highlighter-rouge">AND</code> operation has higher priority than logical <code class="language-plaintext highlighter-rouge">OR</code>) any comment by two of the three owners actually triggers the workflow.</p>

<h4 id="impact">Impact</h4>

<p>If the owners are tricked to comment on an especially crafted pull request, it may lead to arbitrary script injection which enables un-authorized modification of the base repository and secrets exfiltration. For a PoC create a pull request from a forked repository with branch name <code class="language-plaintext highlighter-rouge">";echo${IFS}test;#</code>.</p>

<h2 id="credit">Credit</h2>

<p>This issue was discovered and reported by GHSL team member <a href="https://github.com/JarLob">@JarLob (Jaroslav Lobačevski)</a>.</p>

<h2 id="contact">Contact</h2>

<p>You can contact the GHSL team at <code class="language-plaintext highlighter-rouge">securitylab@github.com</code>, please include a reference to <code class="language-plaintext highlighter-rouge">GHSL-2021-046</code> in any communication regarding this issue.</p>

