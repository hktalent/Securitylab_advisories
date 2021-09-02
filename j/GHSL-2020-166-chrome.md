<header class="post-header d-block mb-6">
      <div class="date text-mono f5 my-3">March 8, 2021</div>
      <h1 class="my-2 h00-mktg lh-condensed">GHSL-2020-166: Use-after-free (UaF) in Chrome PaymentCredential - CVE-2020-16018</h1>

      
      
      
      
      

      

      <a target="_blank" class="sc-frDJqD SgxRc d-inline-flex flex-row flex-items-center text-gray" href="https://github.com/m-y-mo">
        <img class="mr-3" src="https://avatars.githubusercontent.com/u/15773368?s=35" height="35" width="35">
        <span>Man Yue Mo</span>
      </a>
    </header>

    <main id="content" class="markdown-body" aria-label="Content">
      <h2 id="coordinated-disclosure-timeline">Coordinated Disclosure Timeline</h2>

<ul>
  <li>07/10/2020 Reported as <a href="https://bugs.chromium.org/p/chromium/issues/detail?id=1136078">Chromium Issue 1136078</a></li>
  <li>17/11/2020 Issue fixed in the release of <a href="https://chromereleases.googleblog.com/2020/11/stable-channel-update-for-desktop_17.html">version 87</a>.</li>
</ul>

<h2 id="summary">Summary</h2>
<p>UaF in PaymentCredential::DidDownloadFavicon</p>

<h2 id="product">Product</h2>
<p>Chrome</p>

<h2 id="tested-version">Tested Version</h2>
<p>Tested on master branch commit 775b30d and also 86.0.4240.75 on Ubuntu 18.04.2 LTS.</p>

<h2 id="details">Details</h2>

<p>In the <code class="language-plaintext highlighter-rouge">PaymentCredential::DidDownloadFavicon</code> function, the <code class="language-plaintext highlighter-rouge">this</code> pointer is passed into <code class="language-plaintext highlighter-rouge">AddSecurePaymentConfirmationInstrument</code> [1]. This is then passed to a callback as a raw pointer (consumer). As <code class="language-plaintext highlighter-rouge">PaymentCredential</code> is re-created every time <code class="language-plaintext highlighter-rouge">PaymentRequestWebContentsManager::CreatePaymentCredential</code> is called [3], a compromised renderer can create multiple <code class="language-plaintext highlighter-rouge">PaymentCredential</code> bindings to destroy <code class="language-plaintext highlighter-rouge">PaymentCredential</code> on the browser side. If the destruction of <code class="language-plaintext highlighter-rouge">PaymentCredential</code> happens while it is waiting inside the callback in [2], a use after free will happen when the callback is executed.</p>

<ol>
  <li>https://source.chromium.org/chromium/chromium/src/+/a5ae714863136d65c56547f8f733bc1a7a1ea089:components/payments/content/payment_credential.cc;l=105</li>
  <li>https://source.chromium.org/chromium/chromium/src/+/a5ae714863136d65c56547f8f733bc1a7a1ea089:components/payments/content/payment_manifest_web_data_service.cc;l=124;drc=5cf19d56421cf1c08f91d1bcdf919268275fd8d6</li>
  <li>https://source.chromium.org/chromium/chromium/src/+/a5ae714863136d65c56547f8f733bc1a7a1ea089:components/payments/content/payment_credential.cc;l=105</li>
</ol>

<h2 id="cve">CVE</h2>
<p>= CVE-2020-16018</p>

<h4 id="impact">Impact</h4>

<p>Use-after-free in browser that requires a compromised renderer, which could result in a sandbox escape.</p>

<h2 id="credit">Credit</h2>

<p>This issue was discovered and reported by GHSL team member <a href="https://github.com/m-y-mo">@m-y-mo (Man Yue Mo)</a>.</p>

<h2 id="contact">Contact</h2>

<p>You can contact the GHSL team at <code class="language-plaintext highlighter-rouge">securitylab@github.com</code>, please include the <code class="language-plaintext highlighter-rouge">GHSL-2020-166</code> in any communication regarding this issue.</p>

    