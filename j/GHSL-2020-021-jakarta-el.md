<header class="post-header d-block mb-6">
      <div class="date text-mono f5 my-3">April 1, 2021</div>
      <h1 class="my-2 h00-mktg lh-condensed">GHSL-2020-021: Bypass input sanitization of EL expressions in Eclipse-EE4J</h1>

      
      
      
      
      

      

      <a target="_blank" class="sc-frDJqD SgxRc d-inline-flex flex-row flex-items-center text-gray" href="https://github.com/pwntester">
        <img class="mr-3" src="https://avatars.githubusercontent.com/u/125701?s=35" height="35" width="35">
        <span>Alvaro Munoz</span>
      </a>
    </header>

    <main id="content" class="markdown-body" aria-label="Content">
      
<h2 id="coordinated-disclosure-timeline">Coordinated Disclosure Timeline</h2>
<ul>
  <li>02/07/2020: Report sent to Vendor (security@eclipse.org)</li>
  <li>03/12/2020: Ping them for acknowledgment</li>
  <li>04/14/2020: Sent report through Bugzilla (https://bugs.eclipse.org/bugs/show_bug.cgi?id=562121)</li>
  <li>03/26/2021: No response received from Eclipse. Disclosure deadline reached.</li>
  <li>04/01/2021: Publication as per our <a href="https://securitylab.github.com/advisories/#policy">disclosure policy</a></li>
</ul>

<h2 id="summary">Summary</h2>

<p>A bug in the <a href="https://github.com/eclipse-ee4j/el-ri/blob/master/impl/src/main/java/com/sun/el/parser/ELParserTokenManager.java"><code class="language-plaintext highlighter-rouge">ELParserTokenManager</code></a> enables invalid EL expressions to be evaluated as if they were valid. For example, the following message will evaluate an invalid EL expression and the interpolated message will be <code class="language-plaintext highlighter-rouge">1+1 = 2</code>:</p>

<div class="language-plaintext highlighter-rouge"><div class="highlight"><pre class="highlight"><code>1+1 = $\#{1+1}
</code></pre></div></div>
<p>(Note: EL expression delimiter is escaped and therefore it should be treated as a literal expression and not be evaluated)</p>

<p>This bug enables attackers to bypass input sanitization (escaping, stripping) controls that developers may have put in place when handling user-controlled data in error messages.</p>

<h2 id="product">Product</h2>
<p>Eclipse-EE4J Expression Language Reference Implementation</p>

<h2 id="tested-version">Tested Version</h2>
<p>3.0.3</p>

<h2 id="details">Details</h2>

<h3 id="incorrect-el-expression-tokenization">Incorrect EL expression tokenization</h3>

<p>EL expressions are used in many places. One of them is in <a href="https://docs.jboss.org/hibernate/validator/5.1/reference/en-US/html/chapter-message-interpolation.html#section-message-interpolation">Bean Validation constraint error messages</a> where it can take user-controlled data. As specified in <a href="https://docs.jboss.org/hibernate/stable/validator/reference/en-US/html_single/?v=6.1#_the_code_constraintvalidatorcontext_code">Hibernate Validator documentation</a>:</p>

<blockquote>
  <p>Note that the custom message template is passed directly to the Expression Language engine.
Thus, you should be very careful when integrating user input in a custom message template as it will be interpreted by the Expression Language engine, which is usually not the behavior you expect and could allow malicious users to leak sensitive data.
If you need to integrate user input, you should:</p>
  <ul>
    <li>either escape it by using the Jakarta Bean Validation message interpolation escaping rules;</li>
    <li>or, even better, pass it as message parameters or expression variables by unwrapping the context to HibernateConstraintValidatorContext.</li>
  </ul>
</blockquote>

<p>Several applications attempt to prevent such EL injections by replacing the EL opening delimiter <code class="language-plaintext highlighter-rouge">${</code> with just <code class="language-plaintext highlighter-rouge">{</code>. e.g.:</p>

<div class="language-plaintext highlighter-rouge"><div class="highlight"><pre class="highlight"><code>    public String replaceElDelimiter(final String value) {
        if (value != null) {
            return value.replaceAll("\\$+\\{", "{");
        }
        return null;
    }
</code></pre></div></div>

<p>This is seemingly a secure way to prevent injection attacks since all occurrences of <code class="language-plaintext highlighter-rouge">${</code> will be replaced with <code class="language-plaintext highlighter-rouge">{</code>, and since the regex matches repeating <code class="language-plaintext highlighter-rouge">$</code> it will also fix more intricate injection attempts that send e.g. <code class="language-plaintext highlighter-rouge">$${</code> in an attempt to arrive at the <code class="language-plaintext highlighter-rouge">${</code> delimiter to achieve EL execution.</p>

<p>A way of bypassing this control is trying to use deferred expressions instead (<code class="language-plaintext highlighter-rouge">#{expr}</code>) since they are not protected by this function. However, the bean validation specs do not allow the use of deferred expressions and Bean Validation implementations such as Apache BVal enforce this restriction by escaping them (<code class="language-plaintext highlighter-rouge">#{expr}</code> -&gt; <code class="language-plaintext highlighter-rouge">\#{expr}</code>). <a href="https://github.com/apache/bval/blob/master/bval-jsr/src/main/java/org/apache/bval/el/ELFacade.java#L75">For example</a>:</p>

<div class="language-java highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="c1">// Java Bean Validation does not support EL expressions that look like JSP "deferred" expressions</span>
<span class="k">return</span> <span class="n">expressionFactory</span><span class="o">.</span><span class="na">createValueExpression</span><span class="o">(</span><span class="n">context</span><span class="o">,</span>
    <span class="nc">EvaluationType</span><span class="o">.</span><span class="na">DEFERRED</span><span class="o">.</span><span class="na">regex</span><span class="o">.</span><span class="na">matcher</span><span class="o">(</span><span class="n">message</span><span class="o">).</span><span class="na">replaceAll</span><span class="o">(</span><span class="s">"\\$0"</span><span class="o">),</span> <span class="nc">String</span><span class="o">.</span><span class="na">class</span><span class="o">).</span><span class="na">getValue</span><span class="o">(</span><span class="n">context</span><span class="o">)</span>
    <span class="o">.</span><span class="na">toString</span><span class="o">();</span>
</code></pre></div></div>

<p>This way the underlying EL processor should ignore them and treat them as literal expressions.</p>

<p>However, a bug in the Eclipse EE4J EL implementation allows attackers to bypass this protection with a payload such as <code class="language-plaintext highlighter-rouge">FOO $\#{payload}</code>. This should be considered a literal expression and not be evaluated, however this is not the case.</p>

<p>The bug seems to be in the <a href="https://github.com/eclipse-ee4j/el-ri/blob/master/impl/src/main/java/com/sun/el/parser/ELParser.jjt">parser’s grammar</a>. Specifically in:</p>

<div class="language-plaintext highlighter-rouge"><div class="highlight"><pre class="highlight"><code>&lt;DEFAULT&gt; TOKEN :
{
  &lt; LITERAL_EXPRESSION:
    ((~["\\", "$", "#"])
      | ("\\" ("\\" | "$" | "#"))
      | ("$" ~["{", "$", "#"])
      | ("#" ~["{", "$", "#"])
    )+
    | "$"
    | "#"
  &gt;
|
  &lt; START_DYNAMIC_EXPRESSION: "${" &gt; {stack.push(DEFAULT);}: IN_EXPRESSION
|
  &lt; START_DEFERRED_EXPRESSION: "#{" &gt; {stack.push(DEFAULT);}: IN_EXPRESSION
}
</code></pre></div></div>

<p>A <code class="language-plaintext highlighter-rouge">$</code> or <code class="language-plaintext highlighter-rouge">#</code> followed by a character that is not <code class="language-plaintext highlighter-rouge">{</code>, <code class="language-plaintext highlighter-rouge">$</code> or <code class="language-plaintext highlighter-rouge">#</code> will be treated as a literal expression. The interesting case is where the character following the <code class="language-plaintext highlighter-rouge">$</code> or <code class="language-plaintext highlighter-rouge">#</code> chars is a backslash. The parser will consume the backslash as part of the literal expression and will leave the character that follows it unescaped.</p>

<h4 id="impact">Impact</h4>

<p>This issue may lead to mitigation bypasses that allow for remote code execution in affected applications.</p>

<h2 id="credit">Credit</h2>

<p>This issue was discovered and reported by GHSL team member <a href="https://github.com/pwntester">@pwntester (Alvaro Muñoz)</a>.</p>

<h2 id="contact">Contact</h2>

<p>You can contact the GHSL team at <code class="language-plaintext highlighter-rouge">securitylab@github.com</code>, please include the <code class="language-plaintext highlighter-rouge">GHSL-2020-021</code> in any communication regarding this issue.</p>


 