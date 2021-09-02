<header class="post-header d-block mb-6">
      <div class="date text-mono f5 my-3">March 8, 2021</div>
      <h1 class="my-2 h00-mktg lh-condensed">GHSL-2020-165: Use-after-free (UaF) in Chrome PaymentAppServiceBridge - CVE-2020-16045</h1>

      
      
      
      
      

      

      <a target="_blank" class="sc-frDJqD SgxRc d-inline-flex flex-row flex-items-center text-gray" href="https://github.com/m-y-mo">
        <img class="mr-3" src="https://avatars.githubusercontent.com/u/15773368?s=35" height="35" width="35">
        <span>Man Yue Mo</span>
      </a>
    </header>

    <main id="content" class="markdown-body" aria-label="Content">
      <h2 id="coordinated-disclosure-timeline">Coordinated Disclosure Timeline</h2>
<ul>
  <li>07/09/2020 Reported as <a href="https://bugs.chromium.org/p/chromium/issues/detail?id=1125614">Chromium Issue 1125614</a></li>
  <li>08/09/2020 Was told that it only affects the beta version of Chrome</li>
  <li>09/09/2020 Further investigation uncovered some more crashes that affected the stable version, although these crashes seems to be null pointer dereferences.</li>
  <li>17/11/2020 Issue fixed in the release of <a href="https://chromereleases.googleblog.com/2020/11/stable-channel-update-for-desktop_17.html">version 87</a>, although CVE not yet assigned due to error in automatic scripts.</li>
  <li>12/01/2021 CVE-2020-16045 assigned</li>
</ul>

<h2 id="summary">Summary</h2>
<p>UaF in PaymentAppServiceBridge</p>

<h2 id="product">Product</h2>
<p>Chrome</p>

<h2 id="tested-version">Tested Version</h2>
<p>Pixel 3a XL emulator on Android 10 with master branch commit dc7770f</p>

<h2 id="details">Details</h2>

<p>The <code class="language-plaintext highlighter-rouge">PaymentAppServiceBridge</code> stores a raw pointer to the <code class="language-plaintext highlighter-rouge">RenderFrameHostImpl</code> that is used to create the corresponding PaymentRequest in javascript [1].</p>

<p>This pointer is then used in a number of places, for example, it is used to create an <code class="language-plaintext highlighter-rouge">InternalAuthenticator</code> [2], in which the <code class="language-plaintext highlighter-rouge">render_frame_host_</code> is also passed to the <code class="language-plaintext highlighter-rouge">InternalAuthenticator</code> as a raw pointer. When <code class="language-plaintext highlighter-rouge">InternalAuthenticator</code> is destroyed, it also makes a virtual function call on this raw <code class="language-plaintext highlighter-rouge">render_frame_host_</code> [3].</p>

<p>As the lifespan of the <code class="language-plaintext highlighter-rouge">InternalAuthenticator</code> that holds this raw <code class="language-plaintext highlighter-rouge">RenderFrameHost</code> is tied to a callback [4], which eventually ended up in a callback queue in the Java code [5], by creating a large amount of <code class="language-plaintext highlighter-rouge">paymentRequest</code> in an <code class="language-plaintext highlighter-rouge">iframe</code> in javascript and then destroy the frame while these callbacks are still waiting in a queue, it is possible to cause a UaF.</p>

<ol>
  <li>https://source.chromium.org/chromium/chromium/src/+/69e8eedea08044b770bc6661ff805b804eda6465:chrome/browser/payments/android/payment_app_service_bridge.cc;l=201;drc=bb9e95d636a6fffa1f5300fb4fbbf3fba2ce3df2?originalUrl=%2F</li>
  <li>https://source.chromium.org/chromium/chromium/src/+/69e8eedea08044b770bc6661ff805b804eda6465:chrome/browser/payments/android/payment_app_service_bridge.cc;l=252;drc=bb9e95d636a6fffa1f5300fb4fbbf3fba2ce3df2;bpv=1;bpt=1?originalUrl=%2F</li>
  <li>https://source.chromium.org/chromium/chromium/src/+/69e8eedea08044b770bc6661ff805b804eda6465:chrome/browser/autofill/android/internal_authenticator_android.cc;l=42;drc=bb9e95d636a6fffa1f5300fb4fbbf3fba2ce3df2;bpv=1;bpt=1?originalUrl=%2F</li>
  <li>https://source.chromium.org/chromium/chromium/src/+/69e8eedea08044b770bc6661ff805b804eda6465:components/payments/content/secure_payment_confirmation_app_factory.cc;l=135;drc=bb9e95d636a6fffa1f5300fb4fbbf3fba2ce3df2;bpv=1;bpt=1?originalUrl=%2F</li>
  <li>https://source.chromium.org/chromium/chromium/src/+/master:chrome/android/java/src/org/chromium/chrome/browser/webauth/AuthenticatorImpl.java;l=186;drc=bb9e95d636a6fffa1f5300fb4fbbf3fba2ce3df2;bpv=1;bpt=1?originalUrl=%2F</li>
</ol>

<h2 id="cve">CVE</h2>
<ul>
  <li>CVE-2020-16045</li>
</ul>

<h4 id="impact">Impact</h4>

<p>Use-after-free in browser that requires a compromised renderer, which could result in a sandbox escape. The bug discovered originally only affected beta version of Chrome, although further investigation discovered other crashes that affected stable, which are most likely to be null pointer dereferences.</p>

<h2 id="credit">Credit</h2>

<p>This issue was discovered and reported by GHSL team member <a href="https://github.com/m-y-mo">@m-y-mo (Man Yue Mo)</a>.</p>

<h2 id="contact">Contact</h2>

<p>You can contact the GHSL team at <code class="language-plaintext highlighter-rouge">securitylab@github.com</code>, please include the <code class="language-plaintext highlighter-rouge">GHSL-2020-165</code> in any communication regarding this issue.</p>

    