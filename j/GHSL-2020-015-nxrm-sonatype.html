<header class="post-header d-block mb-6">
      <div class="date text-mono f5 my-3">April 13, 2020</div>
      <h1 class="my-2 h00-mktg lh-condensed">GHSL-2020-015: Remote Code Execution - Bypass of CVE-2018-16621 mitigations in Nexus Repository Manager</h1>

      
      
      
      
      

      

      <a target="_blank" class="sc-frDJqD SgxRc d-inline-flex flex-row flex-items-center text-gray" href="https://github.com/pwntester">
        <img class="mr-3" src="https://avatars.githubusercontent.com/u/125701?s=35" height="35" width="35">
        <span>Alvaro Munoz</span>
      </a>
    </header>

    <main id="content" class="markdown-body" aria-label="Content">
      <h2 id="summary">Summary</h2>

<p>GHSL-2020-015 - Remote Code Execution - Bypass of CVE-2018-16621 mitigations</p>

<h2 id="product">Product</h2>
<p>Nexus Repository Manager</p>

<h2 id="tested-version">Tested Version</h2>
<p>3.20.1</p>

<h2 id="cve">CVE</h2>
<p><a href="https://support.sonatype.com/hc/en-us/articles/360044356194-CVE-2020-10204-Nexus-Repository-Manager-3-Remote-Code-Execution-2020-03-31">CVE-2020-10204</a></p>

<h2 id="details">Details</h2>

<p>The current mitigation for the EL injections reported in CVE-2018-16621 involves striping out the EL delimiters of the user-controlled data by using <code class="language-plaintext highlighter-rouge">stripJavaEL</code> method:</p>

<div class="language-java highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="kd">public</span> <span class="nc">String</span> <span class="nf">stripJavaEl</span><span class="o">(</span><span class="kd">final</span> <span class="nc">String</span> <span class="n">value</span><span class="o">)</span> <span class="o">{</span>
	<span class="k">if</span> <span class="o">(</span><span class="n">value</span> <span class="o">!=</span> <span class="kc">null</span><span class="o">)</span> <span class="o">{</span>
		<span class="k">return</span> <span class="n">value</span><span class="o">.</span><span class="na">replaceAll</span><span class="o">(</span><span class="err">“\\$</span><span class="o">+</span><span class="err">\\</span><span class="o">{</span><span class="err">“</span><span class="o">,</span> <span class="err">“</span><span class="o">{</span><span class="err">“</span><span class="o">);</span>
	<span class="o">}</span>
	<span class="k">return</span> <span class="kc">null</span><span class="o">;</span>
<span class="o">}</span>
</code></pre></div></div>

<p>However, several bugs were found in <strong>Hibernate-Validation</strong> and <strong>Java EL</strong> which enable the EL expression engine to process EL expressions not wrapped by the standard delimiters <code class="language-plaintext highlighter-rouge">${}</code>. The regular expression used in <code class="language-plaintext highlighter-rouge">stripJavaEL</code> will not match these delimiters and therefore it is possible to re-enable CVE-2018-16621.</p>

<p>These bugs have been reported to the corresponding vendors and will be fixed in future releases.</p>

<p>What follows is a list of all endpoints affected by this vulnerability:</p>

<ul>
  <li>CronExpressionValidator (@CronExpression)
    <ul>
      <li>TaskXO.groovy [cronExpression]
        <ul>
          <li>TaskComponent
            <ul>
              <li><code class="language-plaintext highlighter-rouge">TaskComponent.create(final @NotNull @Valid TaskXO taskXO)</code></li>
              <li><code class="language-plaintext highlighter-rouge">TaskComponent.update(final @NotNull @Valid TaskXO taskXO)</code></li>
            </ul>
          </li>
        </ul>
      </li>
    </ul>
  </li>
  <li>RolesExistValidator (@RolesExist)
    <ul>
      <li>UserXO.groovy [roles]
        <ul>
          <li>UserComponent
            <ul>
              <li><code class="language-plaintext highlighter-rouge">UserComponent.create(@NotNull @Valid final UserXO userXO)</code></li>
              <li><code class="language-plaintext highlighter-rouge">UserComponent.update(@NotNull @Valid final UserXO userXO)</code></li>
            </ul>
          </li>
        </ul>
      </li>
      <li>RoleXO.groovy [roles]
        <ul>
          <li>RoleComponent.groovy
            <ul>
              <li><code class="language-plaintext highlighter-rouge">RoleComponent.create(@NotNull @Valid final RoleXO roleXO)</code></li>
              <li><code class="language-plaintext highlighter-rouge">RoleComponent.update(@NotNull @Valid final RoleXO roleXO)</code></li>
            </ul>
          </li>
        </ul>
      </li>
      <li>UserRoleMappingsXO.groovy [roles]
        <ul>
          <li>UserComponent
            <ul>
              <li>see above</li>
            </ul>
          </li>
        </ul>
      </li>
    </ul>
  </li>
  <li>PrivilegesExistValidator (@PrivilegesExist)
    <ul>
      <li>RoleXO.groovy
        <ul>
          <li>RoleComponent.groovy
            <ul>
              <li><code class="language-plaintext highlighter-rouge">RoleComponent.create(@NotNull @Valid final RoleXO roleXO)</code></li>
              <li><code class="language-plaintext highlighter-rouge">RoleComponent.update(@NotNull @Valid final RoleXO roleXO)</code></li>
            </ul>
          </li>
        </ul>
      </li>
    </ul>
  </li>
</ul>

<h3 id="impact">Impact</h3>

<p>This issue may lead to Remote Code execution by high-privilege users</p>

<h2 id="coordinated-disclosure-timeline">Coordinated Disclosure Timeline</h2>
<ul>
  <li>02/03/2020: Report sent to Sonatype</li>
  <li>02/03/2020: Sonatype acknowledged report</li>
  <li>02/14/2020: Sonatype raises questions about some of the issues</li>
  <li>02/17/2020: GHSL answers Sonatype questions</li>
  <li>02/19/2020: Sonatype agrees with GHSL comments</li>
</ul>

<h2 id="credit">Credit</h2>

<p>This issue was discovered and reported by GHSL team member <a href="https://github.com/pwntester">@pwntester (Alvaro Muñoz)</a>.</p>

<h2 id="contact">Contact</h2>

<p>You can contact the GHSL team at <code class="language-plaintext highlighter-rouge">securitylab@github.com</code>, please include the <code class="language-plaintext highlighter-rouge">GHSL-2020-015</code> in any communication regarding this issue.</