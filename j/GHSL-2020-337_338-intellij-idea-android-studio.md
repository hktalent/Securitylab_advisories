<header class="post-header d-block mb-6">
      <div class="date text-mono f5 my-3">May 12, 2021</div>
      <h1 class="my-2 h00-mktg lh-condensed">GHSL-2020-337_338: Arbitrary code execution when cloning/checking out a Gradle project - CVE-2021-29263</h1>

      
      
      
      
      

      

      <a target="_blank" class="sc-frDJqD SgxRc d-inline-flex flex-row flex-items-center text-gray" href="https://github.com/pwntester">
        <img class="mr-3" src="https://avatars.githubusercontent.com/u/125701?s=35" height="35" width="35">
        <span>Alvaro Munoz</span>
      </a>
    </header>

    <main id="content" class="markdown-body" aria-label="Content">
      
<h2 id="coordinated-disclosure-timeline">Coordinated Disclosure Timeline</h2>
<ul>
  <li>2020-12-17: Reported to security@jetbrains.com</li>
  <li>2020-12-18: The issue will be investigated by JetBrains team</li>
  <li>2021-02-02: JetBrains states that they have found an appropriate solution and have started implementing it.</li>
  <li>2021-03-25: Requested status update from JetBrains.</li>
  <li>2021-03-25: A fix was implemented in IntelliJ IDEA 2020.3.3, released on March 16, 2021</li>
</ul>

<h2 id="summary">Summary</h2>

<p>Upon cloning or checking out a Gradle project from an external repository (<code class="language-plaintext highlighter-rouge">Get from VCS</code>), both IntelliJ IDEA and Android Studio, run the gradle <code class="language-plaintext highlighter-rouge">build</code> task.</p>

<h2 id="products">Products</h2>

<ul>
  <li>IntelliJ IDEA</li>
  <li>Android Studio</li>
</ul>

<h2 id="tested-version">Tested Version</h2>

<ul>
  <li>IntelliJ IDEA 2020.3 (Community Edition)</li>
</ul>

<p>Build #IC-203.5981.155, built on November 30, 2020</p>

<ul>
  <li>Android Studio 4.1.1</li>
</ul>

<p>Build #AI-201.8743.12.41.6953283, built on November 5, 2020</p>

<h2 id="details">Details</h2>

<h3 id="issue-code-execution-when-cloningchecking-out-a-repository">Issue: Code execution when cloning/checking out a repository</h3>
<p>When cloning or checking out a repository containing a Gradle project, Android Studio and IntelliJ will try to run the <code class="language-plaintext highlighter-rouge">build</code> task immediately without asking for a user confirmation that would give them the opportunity to analyze the build script.</p>

<p>If an attacker fools a developer into cloning or checking out a malicious repository, they will be able to run arbitrary code as part of the repository clone or checkout operation. For example, an attacker could hide a malware dropper using the Gradle’s <a href="https://docs.gradle.org/current/dsl/org.gradle.api.tasks.Exec.html"><code class="language-plaintext highlighter-rouge">Exec</code></a> or try something more stealthy.</p>

<div class="language-plaintext highlighter-rouge"><div class="highlight"><pre class="highlight"><code>apply plugin: 'java'

sourceCompatibility = 1.8
targetCompatibility = 1.8

void checkRequirements(){
    exec {
      executable 'touch'
      args '/tmp/pwned_from_gradle'
    }

}

build{
    checkRequirements();
}
</code></pre></div></div>

<p>When searching for similar patterns I found the exact same issue being discussed as a <a href="https://github.com/vxunderground/MalwareSourceCode/tree/main/Java/Virus.Java.Cheshire.a">malware spread vector</a> which highlights why this issue should be addressed. In addition a similar vulnerability (<a href="https://msrc.microsoft.com/update-guide/vulnerability/CVE-2020-17156">CVE-2020-17156</a>) was recently fixed in MS Visual Studio.</p>

<h4 id="impact">Impact</h4>
<p>Arbitrary Code Execution on repository cloning/checkout.</p>

<h2 id="cve">CVE</h2>
<ul>
  <li>CVE-2021-29263</li>
</ul>

<h2 id="resources">Resources</h2>
<p><a href="https://blog.jetbrains.com/blog/2021/05/07/jetbrains-security-bulletin-q1-2021/">https://blog.jetbrains.com/blog/2021/05/07/jetbrains-security-bulletin-q1-2021/</a></p>

<h2 id="credit">Credit</h2>

<p>This issue was discovered and reported by GHSL team member <a href="https://github.com/pwntester">@pwntester (Alvaro Muñoz)</a>.</p>

<h2 id="contact">Contact</h2>

<p>You can contact the GHSL team at <code class="language-plaintext highlighter-rouge">securitylab@github.com</code>, please include a reference to <code class="language-plaintext highlighter-rouge">GHSL-2020-337</code>, <code class="language-plaintext highlighter-rouge">GHSL-2020-338</code> in any communication regarding this issue.</p>


 