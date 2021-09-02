<header class="post-header d-block mb-6">
      <div class="date text-mono f5 my-3">December 11, 2020</div>
      <h1 class="my-2 h00-mktg lh-condensed">GHSL-2020-205: Remote Code Execution in Apache Struts 2 - S2-061 - CVE-2020-17530</h1>

      
      
      
      
      

      

      <a target="_blank" class="sc-frDJqD SgxRc d-inline-flex flex-row flex-items-center text-gray" href="https://github.com/pwntester">
        <img class="mr-3" src="https://avatars.githubusercontent.com/u/125701?s=35" height="35" width="35">
        <span>Alvaro Munoz</span>
      </a>
    </header>

    <main id="content" class="markdown-body" aria-label="Content">
      <h2 id="summary">Summary</h2>

<p>Double evaluation of Struts tag dynamic attributes leads to Remote Code Execution</p>

<h2 id="product">Product</h2>

<p>Apache Struts 2</p>

<h2 id="tested-version">Tested Version</h2>

<p>Latest commit to the date of reporting: 62424ef30c39167df493522286e8bb73d3fdcc4a</p>

<h2 id="details">Details</h2>

<h3 id="issue-1-double-evaluation-of-jsp-tags-dynamic-attributes">Issue 1: Double evaluation of JSP tag’s dynamic attributes.</h3>

<p>Struts performs a double or triple OGNL evaluation of dynamic attributes (those not defined in the TLD specification such as <a href="https://developer.mozilla.org/en-US/docs/Web/HTML/Global_attributes/data-*">HTML5 <code class="language-plaintext highlighter-rouge">data-*</code> attributes</a>).</p>

<p>Struts JSTL tags use FreeMarker templates to render the tag so the process normally involves three different layers:</p>
<ol>
  <li>Tag classes (eg: <code class="language-plaintext highlighter-rouge">org.apache.struts2.views.jsp.ui.AbstractUITag</code>)</li>
  <li>Components (<code class="language-plaintext highlighter-rouge">org.apache.struts2.components.UIBean</code>)</li>
  <li>FTL templates</li>
</ol>

<p>In the first step (<code class="language-plaintext highlighter-rouge">AbstractUITag</code>), dynamic attributes will be evaluated once by <code class="language-plaintext highlighter-rouge">findValue</code>:</p>

<div class="language-java highlighter-rouge"><div class="highlight"><pre class="highlight"><code>    <span class="kd">public</span> <span class="kt">void</span> <span class="nf">setDynamicAttribute</span><span class="o">(</span><span class="nc">String</span> <span class="n">uri</span><span class="o">,</span> <span class="nc">String</span> <span class="n">localName</span><span class="o">,</span> <span class="nc">Object</span> <span class="n">value</span><span class="o">)</span> <span class="kd">throws</span> <span class="nc">JspException</span> <span class="o">{</span>
        <span class="k">if</span> <span class="o">(</span><span class="nc">ComponentUtils</span><span class="o">.</span><span class="na">altSyntax</span><span class="o">(</span><span class="n">getStack</span><span class="o">())</span> <span class="o">&amp;&amp;</span> <span class="nc">ComponentUtils</span><span class="o">.</span><span class="na">isExpression</span><span class="o">(</span><span class="n">value</span><span class="o">.</span><span class="na">toString</span><span class="o">()))</span> <span class="o">{</span>
            <span class="n">dynamicAttributes</span><span class="o">.</span><span class="na">put</span><span class="o">(</span><span class="n">localName</span><span class="o">,</span> <span class="nc">String</span><span class="o">.</span><span class="na">valueOf</span><span class="o">(</span><span class="nc">ObjectUtils</span><span class="o">.</span><span class="na">defaultIfNull</span><span class="o">(</span><span class="n">findValue</span><span class="o">(</span><span class="n">value</span><span class="o">.</span><span class="na">toString</span><span class="o">()),</span> <span class="n">value</span><span class="o">)));</span>
        <span class="o">}</span> <span class="k">else</span> <span class="o">{</span>
            <span class="n">dynamicAttributes</span><span class="o">.</span><span class="na">put</span><span class="o">(</span><span class="n">localName</span><span class="o">,</span> <span class="n">value</span><span class="o">);</span>
        <span class="o">}</span>
    <span class="o">}</span>
</code></pre></div></div>

<p>In the second step, there are no additional evaluations and dynamic properties are just passed around as <code class="language-plaintext highlighter-rouge">parameters.dynamicattributes</code>.</p>

<p>In the third step, the component will merge and render the corresponding FTL template. For example <code class="language-plaintext highlighter-rouge">&lt;s:textfield&gt;</code> will use the <code class="language-plaintext highlighter-rouge">text.ftl</code> template:</p>

<div class="language-plaintext highlighter-rouge"><div class="highlight"><pre class="highlight"><code>&lt;input&lt;#rt/&gt;
 type="${(parameters.type!"text")?html}"&lt;#rt/&gt;
 name="${(parameters.name!"")?html}"&lt;#rt/&gt;
&lt;#if parameters.get("size")?has_content&gt;
 size="${parameters.get("size")?html}"&lt;#rt/&gt;
&lt;/#if&gt;
&lt;#if parameters.maxlength?has_content&gt;
 maxlength="${parameters.maxlength?html}"&lt;#rt/&gt;
&lt;/#if&gt;
&lt;#if parameters.nameValue??&gt;
 value="${parameters.nameValue?html}"&lt;#rt/&gt;
&lt;/#if&gt;
&lt;#if parameters.disabled!false&gt;
 disabled="disabled"&lt;#rt/&gt;
&lt;/#if&gt;
&lt;#if parameters.readonly!false&gt;
 readonly="readonly"&lt;#rt/&gt;
&lt;/#if&gt;
&lt;#if parameters.tabindex?has_content&gt;
 tabindex="${parameters.tabindex?html}"&lt;#rt/&gt;
&lt;/#if&gt;
&lt;#if parameters.id?has_content&gt;
 id="${parameters.id?html}"&lt;#rt/&gt;
&lt;/#if&gt;
&lt;#include "/${parameters.templateDir}/${parameters.expandTheme}/css.ftl" /&gt;
&lt;#if parameters.title?has_content&gt;
 title="${parameters.title?html}"&lt;#rt/&gt;
&lt;/#if&gt;
&lt;#include "/${parameters.templateDir}/${parameters.expandTheme}/scripting-events.ftl" /&gt;
&lt;#include "/${parameters.templateDir}/${parameters.expandTheme}/common-attributes.ftl" /&gt;
&lt;#include "/${parameters.templateDir}/${parameters.expandTheme}/dynamic-attributes.ftl" /&gt;
/&gt;
</code></pre></div></div>

<p>Right before closing the tag, it renders scripting, common and dynamic attributes. The last one being:</p>

<div class="language-plaintext highlighter-rouge"><div class="highlight"><pre class="highlight"><code>&lt;#if (parameters.dynamicAttributes?? &amp;&amp; parameters.dynamicAttributes?size &gt; 0)&gt;&lt;#rt/&gt;
&lt;#assign aKeys = parameters.dynamicAttributes.keySet()&gt;&lt;#rt/&gt;
&lt;#list aKeys as aKey&gt;&lt;#rt/&gt;
  &lt;#assign keyValue = parameters.dynamicAttributes.get(aKey)/&gt;
  &lt;#if keyValue?is_string&gt;
      &lt;#assign value = struts.translateVariables(keyValue)!keyValue/&gt;
  &lt;#else&gt;
      &lt;#assign value = keyValue?string/&gt;
  &lt;/#if&gt;
 ${aKey}="${value?html}"&lt;#rt/&gt;
&lt;/#list&gt;&lt;#rt/&gt;
&lt;/#if&gt;&lt;#rt/&gt;
</code></pre></div></div>

<p>The dynamic attributes are evaluated once again by <code class="language-plaintext highlighter-rouge">translateVariables</code>.</p>

<p>Therefore dynamic attributes are evaluated twice when OGNL forced evaluation is used (<code class="language-plaintext highlighter-rouge">&lt;s:textfield data-value="%{message}"&gt;</code>):
For example, for the case where <code class="language-plaintext highlighter-rouge">message</code> is an action property under user control, visiting the URL <code class="language-plaintext highlighter-rouge">https:/foo.com/action?message%25{1%2b1}</code> will result in a double evaluation:</p>
<ul>
  <li><code class="language-plaintext highlighter-rouge">AbstractUITag.java</code>: <code class="language-plaintext highlighter-rouge">%{message}</code> -&gt; <code class="language-plaintext highlighter-rouge">%{1+1}</code></li>
  <li><code class="language-plaintext highlighter-rouge">dynamic-attributes.ftl</code>: <code class="language-plaintext highlighter-rouge">%{1+1}</code> -&gt; <code class="language-plaintext highlighter-rouge">2</code></li>
</ul>

<p>If JSTL EL is enabled and the page uses <code class="language-plaintext highlighter-rouge">${}</code> expressions (eg: <code class="language-plaintext highlighter-rouge">&lt;s:textfield data-value="${message}"&gt;</code>), the attribute will get evaluated three times.</p>

<p>Visiting <code class="language-plaintext highlighter-rouge">https:/foo.com/action?message=%25{%23parameters.foo[0]}&amp;foo=%25{1%2b1}</code> will result in the following evaluations:</p>
<ul>
  <li>JSTL evaluation: <code class="language-plaintext highlighter-rouge">${message}</code> -&gt; <code class="language-plaintext highlighter-rouge">%{parameters.foo[0]}</code> (This is possible since dynamic attributes are not declared in the TLD and therefore they lack the <code class="language-plaintext highlighter-rouge">rtexprvalue=false</code> value)</li>
  <li><code class="language-plaintext highlighter-rouge">AbstractUITag.java</code>: <code class="language-plaintext highlighter-rouge">%{#parameters.foo[0]}</code> -&gt; <code class="language-plaintext highlighter-rouge">%{1+1}</code></li>
  <li><code class="language-plaintext highlighter-rouge">dynamic-attributes.ftl</code>: <code class="language-plaintext highlighter-rouge">%{1+1}</code> -&gt; <code class="language-plaintext highlighter-rouge">2</code></li>
</ul>

<p>We can tell it is a bug since there is either no evaluation when the attribute does not use delimiters (eg: <code class="language-plaintext highlighter-rouge">data-value="message"</code>) or double/triple evaluation when it forces the evaluation with the delimiters (eg: <code class="language-plaintext highlighter-rouge">data-value="%{message}"</code>)</p>

<h4 id="impact">Impact</h4>

<p>This issue may lead to <code class="language-plaintext highlighter-rouge">RCE</code>.</p>

<h3 id="issue-2-additional-evaluation-on-freemarker-tags">Issue 2: Additional evaluation on FreeMarker tags</h3>

<p>This issue is basically the same as <a href="https://cwiki.apache.org/confluence/display/WW/S2-053">S2-053</a> which describes a double evaluation where the first evaluation is a <code class="language-plaintext highlighter-rouge">${}</code> FreeMarker evaluation in <a href="https://github.com/apache/freemarker/blob/2.3-gae/src/main/java/freemarker/core/UnifiedCall.java#L95">UnifiedCall</a> and the second evaluation is an OGNL evaluation (normally in <a href="https://github.com/apache/struts/blob/master/core/src/main/java/org/apache/struts2/components/UIBean.java#L795">UIBean</a>). When I verified the examples described in the security bulletin, both the insecure constructions (eg: <code class="language-plaintext highlighter-rouge">&lt;@s.hidden name="${message}"/&gt;</code>) and the secure proposed ones (eg: <code class="language-plaintext highlighter-rouge">&lt;@s.hidden name="%{message}"/&gt;</code>) were found to be vulnerable in 2.5.12 (first version where they should be fixed) and also in latest 2.5.22 version.</p>

<p>For example, given the following example that includes the insecure examples described in the bulletin:</p>

<div class="language-plaintext highlighter-rouge"><div class="highlight"><pre class="highlight"><code>&lt;@s.hidden name="redirectUri" value=message /&gt;
&lt;@s.hidden name="redirectUri" value="${message}" /&gt;
&lt;@s.hidden name="${message}"/&gt;
</code></pre></div></div>

<p>We can trigger double evaluations by providing <code class="language-plaintext highlighter-rouge">%{}</code> delimited expressions, eg: <code class="language-plaintext highlighter-rouge">http://localhost:8080/test?message=%25%7B1%2b1%7D</code> (<code class="language-plaintext highlighter-rouge">%{1+1}</code>) even in the latest versions of Struts. Therefore S2-053 fix doesn’t seem to be working as intended.</p>

<p>The examples proposed as secure alternatives in the same bulletin are also vulnerable:</p>
<div class="language-plaintext highlighter-rouge"><div class="highlight"><pre class="highlight"><code>&lt;@s.hidden name="redirectUri" value="%{message}" /&gt;
&lt;@s.hidden name="%{message}"/&gt;
</code></pre></div></div>

<p>We can trigger double evaluations by providing <strong>NO</strong> delimited expressions, eg: <code class="language-plaintext highlighter-rouge">http://localhost:8080/test?message=1%2b1 1+1</code></p>

<p>Please note that these are much more critical than the JSP tag ones (S2-059) since in this case all OGNL evaluations are evaluated an additional time. Thats it, single evaluations such as the <code class="language-plaintext highlighter-rouge">value</code> attribute ones are now evaluated twice, and double evaluations such as the <code class="language-plaintext highlighter-rouge">id</code> or <code class="language-plaintext highlighter-rouge">name</code> ones are now evaluated three times!</p>

<p><code class="language-plaintext highlighter-rouge">name</code>/<code class="language-plaintext highlighter-rouge">value</code> attribute double evaluation is the most concerning one since they may contain user-controlled data as in:</p>

<div class="language-plaintext highlighter-rouge"><div class="highlight"><pre class="highlight"><code>Change your username: &lt;@s.textfield value="${username}"/&gt;
</code></pre></div></div>

<p>or with <code class="language-plaintext highlighter-rouge">%{}</code> delimiters:</p>

<div class="language-plaintext highlighter-rouge"><div class="highlight"><pre class="highlight"><code>Change your username: &lt;@s.textfield name="%{username}"/&gt;
</code></pre></div></div>

<p>The recommendations from S2-053 suggest using <code class="language-plaintext highlighter-rouge">%{}</code> expressions rather than <code class="language-plaintext highlighter-rouge">${}</code> but since the latter are the ones that developers use in FTL templates, it is error-prone and may easily lead to critical bugs.</p>

<h4 id="impact-1">Impact</h4>

<p>This issue may lead to <code class="language-plaintext highlighter-rouge">RCE</code>.</p>

<h3 id="issue-3-additional-evaluation-on-velocity-tags">Issue 3: Additional evaluation on Velocity tags</h3>

<p>Similarly to the issue described above, When using <code class="language-plaintext highlighter-rouge">${}</code> delimited expressions, Velocity templates also perform an additional evaluation to the ones performed by the Component and FTL template layers.</p>

<p>Velocity Struts tags are implemented as Velocity Directives and all of them extend from <code class="language-plaintext highlighter-rouge">org.apache.struts2.views.velocity.components.AbstractDirective</code>. They all work in a similar way where tag parameters are passed in the form of <code class="language-plaintext highlighter-rouge">key=value</code> strings, eg:</p>

<div class="language-plaintext highlighter-rouge"><div class="highlight"><pre class="highlight"><code>#stextfield ("label=First name" "name=John")
</code></pre></div></div>

<p>Directive parameters are parsed by <code class="language-plaintext highlighter-rouge">AbstractDirective</code> render method and then added as tag parameters by <a href="https://github.com/apache/struts/blob/master/plugins/velocity/src/main/java/org/apache/struts2/views/velocity/components/AbstractDirective.java#L147"><code class="language-plaintext highlighter-rouge">putProperty</code></a>). In this method, the directive parameters are evaluated before splitting them by <code class="language-plaintext highlighter-rouge">=</code>. This means that there is an additional evaluation to the ones performed later by the Component and FTL template layers which causes simple evaluated attributes to be evaluated twice. Eg:</p>

<div class="language-plaintext highlighter-rouge"><div class="highlight"><pre class="highlight"><code>#stextfield ("label=First name" "value=${username}")
</code></pre></div></div>

<p>Note that even if the <code class="language-plaintext highlighter-rouge">value</code> attribute is only evaluated once when using JSP tags, in the case above, there will still be a second evaluation.</p>

<h4 id="impact-2">Impact</h4>
<p>This issue may lead to <code class="language-plaintext highlighter-rouge">RCE</code>.</p>

<h2 id="cve">CVE</h2>
<p>CVE-2020-17530</p>

<h2 id="coordinated-disclosure-timeline">Coordinated Disclosure Timeline</h2>
<ul>
  <li>08/28/2020: Initial report sent to Apache Security Team</li>
  <li>10/13/2020: Issue is acknowledged.</li>
  <li>11/07/2020: A first patch is shared for evaluation.</li>
  <li>11/11/2020: A second patch is shared addressing a missed case.</li>
  <li>11/13/2020: A new patch is proposed to address new RCE payloads in the packages blocklist.</li>
  <li>12/08/2020: Fix is released as part of <a href="https://struts.apache.org/announce#a20201208">2.5.26</a>
    <h2 id="credit">Credit</h2>
    <p>This issue was discovered and reported by GHSL team member <a href="https://github.com/pwntester">@pwntester (Alvaro Muñoz)</a>.</p>
  </li>
</ul>

<h2 id="resources">Resources</h2>
<ul>
  <li>https://struts.apache.org/announce#a20201208</li>
  <li>https://cwiki.apache.org/confluence/display/WW/S2-061</li>
</ul>

<h2 id="contact">Contact</h2>
<p>You can contact the GHSL team at <code class="language-plaintext highlighter-rouge">securitylab@github.com</code>, please include a reference to <code class="language-plaintext highlighter-rouge">GHSL-2020-205</code> in any communication regarding this issue.</p>
