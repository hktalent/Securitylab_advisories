<header class="post-header d-block mb-6">
      <div class="date text-mono f5 my-3">February 3, 2021</div>
      <h1 class="my-2 h00-mktg lh-condensed">GHSL-2020-231: Command injection in graphql-dotnet workflows</h1>

      
      
      
      
      

      

      <a target="_blank" class="sc-frDJqD SgxRc d-inline-flex flex-row flex-items-center text-gray" href="https://github.com/jarlob">
        <img class="mr-3" src="https://avatars.githubusercontent.com/u/26652396?s=35" height="35" width="35">
        <span>Jaroslav Lobacevski</span>
      </a>
    </header>

    <main id="content" class="markdown-body" aria-label="Content">
      <h2 id="coordinated-disclosure-timeline">Coordinated Disclosure Timeline</h2>

<ul>
  <li>2020-11-23: Report sent to maintainers.</li>
  <li>2020-12-01: Maintainers acknowledged.</li>
  <li>2020-12-01: Issue resolved.</li>
</ul>

<h2 id="summary">Summary</h2>

<p>The <code class="language-plaintext highlighter-rouge">wipcheck.yml</code> GitHub workflow in <a href="https://github.com/graphql-dotnet/graphql-dotnet/blob/master/.github/workflows/wipcheck.yml">graphql-dotnet</a>, <a href="https://github.com/graphql-dotnet/server/blob/master/.github/workflows/wipcheck.yml">server</a>, <a href="https://github.com/graphql-dotnet/parser/blob/master/.github/workflows/wipcheck.yml">parser</a> and <a href="https://github.com/graphql-dotnet/authorization/blob/master/.github/workflows/wipcheck.yml">authorization</a> repositories is vulnerable to arbitrary command injection.</p>

<h2 id="product">Product</h2>

<p><a href="https://github.com/graphql-dotnet">graphql-dotnet GitHub repositories</a></p>

<h2 id="tested-version">Tested Version</h2>

<p><a href="https://github.com/graphql-dotnet/graphql-dotnet/blob/7cb40df2de0e6c088456ca5fd009ed0a1bab7838/.github/workflows/wipcheck.yml">graphql-dotnet</a><br />
<a href="https://github.com/graphql-dotnet/graphql-dotnet/blob/31d3858bb57f7b67beebcfdae4eeab9f8805811d/.github/workflows/wipcheck.yml">server</a><br />
<a href="https://github.com/graphql-dotnet/graphql-dotnet/blob/928ca933218501e9f4300007fd694f4fc95e5cbf/.github/workflows/wipcheck.yml">parser</a><br />
<a href="https://github.com/graphql-dotnet/graphql-dotnet/blob/e450dcf3828447e5d29595d9219fdffd9480464a/.github/workflows/wipcheck.yml">authorization</a></p>

<h2 id="details">Details</h2>

<h3 id="issue-the-title-of-public-github-pull-request-is-used-to-format-a-shell-command">Issue: The title of public GitHub pull request is used to format a shell command</h3>

<p>A Pull Request title is used to format a bash script:</p>

<div class="language-yaml highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="na">name</span><span class="pi">:</span> <span class="s">Check if PR title contains [WIP]</span>

<span class="na">on</span><span class="pi">:</span>
  <span class="na">pull_request</span><span class="pi">:</span>
    <span class="na">types</span><span class="pi">:</span>
      <span class="pi">-</span> <span class="s">opened</span>        <span class="c1"># when PR is opened</span>
      <span class="pi">-</span> <span class="s">edited</span>        <span class="c1"># when PR is edited</span>
      <span class="pi">-</span> <span class="s">synchronize</span>   <span class="c1"># when code is added</span>
      <span class="pi">-</span> <span class="s">reopened</span>      <span class="c1"># when a closed PR is reopened</span>

<span class="na">jobs</span><span class="pi">:</span>
  <span class="na">check-title</span><span class="pi">:</span>
    <span class="na">runs-on</span><span class="pi">:</span> <span class="s">ubuntu-latest</span>

    <span class="na">steps</span><span class="pi">:</span>
      <span class="pi">-</span> <span class="na">name</span><span class="pi">:</span> <span class="s">Fail build if pull request title contains [WIP]</span>
        <span class="na">if</span><span class="pi">:</span> <span class="s">${{ contains(github.event.pull_request.title, '[WIP]') }}</span> <span class="c1"># This function is case insensitive.</span>
        <span class="na">run</span><span class="pi">:</span> <span class="pi">|</span>
          <span class="s">echo Warning! PR title "${{ github.event.pull_request.title }}" contains [WIP]. Remove [WIP] from the title when PR is ready.</span>
          <span class="s">exit 1</span>
</code></pre></div></div>

<h4 id="impact">Impact</h4>

<p>This vulnerability allows for arbitrary command injection into the bash script. For a proof a concept a Pull Request with the following title <code class="language-plaintext highlighter-rouge">title"; sleep 10 #</code> will delay the action by ten seconds.</p>

<p>Workflows triggered by <code class="language-plaintext highlighter-rouge">pull_request</code> have limited repository token and no access to secrets. The attacker couldn’t do much except CI DoS attacks or running their own code in the context of the GitHub action runner.</p>

<h2 id="credit">Credit</h2>

<p>This issue was discovered and reported by GHSL team member <a href="https://github.com/JarLob">@JarLob (Jaroslav Lobačevski)</a>.</p>

<h2 id="contact">Contact</h2>

<p>You can contact the GHSL team at <code class="language-plaintext highlighter-rouge">securitylab@github.com</code>, please include a reference to <code class="language-plaintext highlighter-rouge">GHSL-2020-231</code> in any communication regarding this issue.</p>

 