<header class="post-header d-block mb-6">
      <div class="date text-mono f5 my-3">May 11, 2020</div>
      <h1 class="my-2 h00-mktg lh-condensed">GHSL-2020-020: EL expression input sanitation bypass in Hibernate Validator - CVE-2020-10693</h1>

      
      
      
      
      

      

      <a target="_blank" class="sc-frDJqD SgxRc d-inline-flex flex-row flex-items-center text-gray" href="https://github.com/pwntester">
        <img class="mr-3" src="https://avatars.githubusercontent.com/u/125701?s=35" height="35" width="35">
        <span>Alvaro Munoz</span>
      </a>
    </header>

    <main id="content" class="markdown-body" aria-label="Content">
      <h2 id="summary">Summary</h2>

<p>A bug in Hibernate Validator’s <a href="https://docs.jboss.org/hibernate/validator/5.1/reference/en-US/html/chapter-message-interpolation.html#section-message-interpolation">interpolation of constraint error messages</a> enables invalid EL expressions to be evaluated as if they were valid.</p>

<p>This bug enables attackers to bypass input sanitation (escaping, stripping) controls that developers may have put in place when handling user-controlled data in error messages.</p>

<h2 id="product">Product</h2>

<p>Hibernate Validator</p>

<h2 id="tested-version">Tested Version</h2>

<p>6.1.2.Final</p>

<h2 id="details">Details</h2>

<h3 id="incorrect-el-expression-tokenization-ghsl-2020-020-cve-2020-10693">Incorrect EL expression tokenization (GHSL-2020-020, CVE-2020-10693)</h3>

<p>The <a href="https://docs.jboss.org/hibernate/stable/validator/reference/en-US/html_single/?v=6.1#_the_code_constraintvalidatorcontext_code"><code class="language-plaintext highlighter-rouge">ConstraintValidatorContext</code> documentation</a> specifies that developers should be very careful when integrating user input into a custom message template as it will be interpreted by the Expression Language engine, which may allow attackers to run arbitrary Java code.</p>

<p>Several applications attempt to prevent such EL injections by replacing the EL opening delimiter <code class="language-plaintext highlighter-rouge">${</code> with just <code class="language-plaintext highlighter-rouge">{</code> e.g.:</p>

<div class="language-plaintext highlighter-rouge"><div class="highlight"><pre class="highlight"><code>    public String replaceElDelimiter(final String value) {
        if (value != null) {
            return value.replaceAll("\\$+\\{", "{");
        }
        return null;
    }
</code></pre></div></div>

<p>This is seemingly a secure way to prevent injection attacks since all occurrences of <code class="language-plaintext highlighter-rouge">${</code> will be replaced with <code class="language-plaintext highlighter-rouge">{</code>, and since the regex matches repeating <code class="language-plaintext highlighter-rouge">$</code> it will also fix more intricate injection attempts that send e.g. <code class="language-plaintext highlighter-rouge">$${</code> in an attempt to arrive at the <code class="language-plaintext highlighter-rouge">${</code> delimiter to achieve EL execution.</p>

<p>However, a bug in the Hibernate message interpolation parser (<a href="https://github.com/hibernate/hibernate-validator/blob/master/engine/src/main/java/org/hibernate/validator/internal/engine/messageinterpolation/parser/TokenCollector.java">org.hibernate.validator.internal.engine.messageinterpolation.parser.TokenCollector</a>), allows attackers to bypass this protection with a payload such as <code class="language-plaintext highlighter-rouge">FOO $\A{payload}</code>. The reason is the following:</p>
<ul>
  <li>When the parser encounters <code class="language-plaintext highlighter-rouge">$</code> we move to <code class="language-plaintext highlighter-rouge">handleELDesignator</code> and due to <code class="language-plaintext highlighter-rouge">tokenCollector.getInterpolationType().equals(InterpolationTermType.EL)</code> we skip the character and move to <code class="language-plaintext highlighter-rouge">ELState</code> state.</li>
  <li>When the parser encounters <code class="language-plaintext highlighter-rouge">\</code> in the <code class="language-plaintext highlighter-rouge">ELState</code>, we skip the character and move to <code class="language-plaintext highlighter-rouge">EscapedState</code></li>
  <li>When the parser encounters <code class="language-plaintext highlighter-rouge">A</code> in the <code class="language-plaintext highlighter-rouge">EscapedState</code>, we append it to the current token (<code class="language-plaintext highlighter-rouge">FOO A</code>) and move back to <code class="language-plaintext highlighter-rouge">ELState</code></li>
  <li>When the parser encounters <code class="language-plaintext highlighter-rouge">{</code> in the <code class="language-plaintext highlighter-rouge">ELState</code>, we terminate the current token, which will remain as <code class="language-plaintext highlighter-rouge">FOO A</code>, and then we create a new empty token and append <code class="language-plaintext highlighter-rouge">${</code> to it, so it is basically replacing <code class="language-plaintext highlighter-rouge">{</code> with <code class="language-plaintext highlighter-rouge">${</code> and then it marks the new token as an EL token and moves to the <code class="language-plaintext highlighter-rouge">InterpolationTermState</code></li>
</ul>

<h4 id="impact">Impact</h4>

<p>This issue may lead to mitigation bypasses that allow for remote code execution in affected applications.</p>

<h2 id="cve">CVE</h2>

<ul>
  <li>CVE-2020-10693</li>
</ul>

<h2 id="coordinated-disclosure-timeline">Coordinated Disclosure Timeline</h2>

<ul>
  <li>02/05/2020: Report sent to Vendor</li>
  <li>02/05/2020: Assigned INC1163499 internal ID</li>
  <li>03/06/2020: RedHat asks for reproducer PoC</li>
  <li>03/10/2020: Sent PoC to RedHat</li>
  <li>03/13/2020: RedHat asks for EL payload to run arbitrary commands</li>
  <li>03/13/2020: Sent arbitrary command execution payload to RedHat</li>
  <li>04/14/2020: Issue is assigned CVE-2020-10693 and moved to EMBARGOED status</li>
  <li>05/05/2020: Embargo is lifted</li>
  <li>05/11/2020: Public Advisory</li>
</ul>

<h2 id="supporting-resources">Supporting Resources</h2>

<ul>
  <li>https://access.redhat.com/security/cve/CVE-2020-10693</li>
  <li>https://bugzilla.redhat.com/show_bug.cgi?id=1805501</li>
</ul>

<h2 id="credit">Credit</h2>

<p>This issue was discovered and reported by GHSL team member <a href="https://github.com/pwntester">@pwntester (Alvaro Muñoz)</a>.</p>

<h2 id="contact">Contact</h2>

<p>You can contact the GHSL team at <code class="language-plaintext highlighter-rouge">securitylab@github.com</code>, please include the <code class="language-plaintext highlighter-rouge">GHSL-2020-020</code> in any communication regarding this issue.</p>

 