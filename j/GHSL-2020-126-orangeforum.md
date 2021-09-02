<header class="post-header d-block mb-6">
      <div class="date text-mono f5 my-3">September 8, 2020</div>
      <h1 class="my-2 h00-mktg lh-condensed">GHSL-2020-126: Open URL redirect in Orange Forum 1.x.x</h1>

      
      
      
      
      

      

      <a target="_blank" class="sc-frDJqD SgxRc d-inline-flex flex-row flex-items-center text-gray" href="https://github.com/ghsecuritylab">
        <img class="mr-3" src="https://avatars.githubusercontent.com/u/61799930?s=35" height="35" width="35">
        <span>GitHub Security Lab</span>
      </a>
    </header>

    <main id="content" class="markdown-body" aria-label="Content">
      <h2 id="summary">Summary</h2>

<p>There exists an <code class="language-plaintext highlighter-rouge">Open URL redirect</code> vulnerability in the 1.x.x branch of Orange Forum. An attacker can send an Orange Forum user a crafted link targeting the login page of Orange Forum, with a <code class="language-plaintext highlighter-rouge">next</code> query parameter of the form <code class="language-plaintext highlighter-rouge">//evil.com</code>. Having clicked the link and authenticated, the targeted user will then be redirected to <code class="language-plaintext highlighter-rouge">evil.com</code>.</p>

<p>After discussion with the maintainer they have discontinued the 1.x.x branch and do not intend to initiate a fix for this branch. If you are using 1.x.x please update to the 2.x branch.</p>

<h2 id="product">Product</h2>

<p>Orange Forum (https://github.com/s-gv/orangeforum)</p>

<h2 id="tested-version">Tested Version</h2>

<p>Versions from <a href="https://github.com/s-gv/orangeforum/tree/orangeforum-1.x.x">the 1.x.x branch</a> are affected (including the latest release, 1.4.0), <code class="language-plaintext highlighter-rouge">master</code> is not.</p>

<h2 id="details">Details</h2>

<p>The login handler <a href="https://github.com/s-gv/orangeforum/blob/orangeforum-1.x.x/views/auth.go#L23">tries</a> to verify that the URL to be redirected to after a successful login is a local URL. It does so by checking whether the URL starts with a slash, which is insufficient: URLs starting with two slashes are non-local.</p>

<h4 id="impact">Impact</h4>

<p>Information Disclosure and potential clientside exploitation.</p>

<h4 id="resources">Resources</h4>

<p>This issue was found by GitHub’s standard <a href="https://lgtm.com/rules/1511330907142">Bad Redirect Check</a> CodeQL query. It doesn’t show up on <a href="https://lgtm.com">LGTM.com</a> because the vulnerability only exists on a (non-master) branch.</p>

<h2 id="coordinated-disclosure-timeline">Coordinated Disclosure Timeline</h2>
<ul>
  <li>05/29/2020: report sent to maintainer</li>
  <li>06/16/2020: report acknowledged, maintainer says branch is no longer maintained and advises update to 2.x</li>
  <li>08/31/2020: disclosure deadline expired</li>
</ul>

<h2 id="credit">Credit</h2>

<p>This issue was discovered and reported by GitHub team members <a href="https://github.com/sauyon">@sauyon</a> and <a href="https://github.com/max-schaefer">@max-schaefer</a>.</p>

<h2 id="contact">Contact</h2>

<p>You can contact the GHSL team at <code class="language-plaintext highlighter-rouge">securitylab@github.com</code>, please include <code class="language-plaintext highlighter-rouge">GHSL-2020-126</code> in any communication regarding this issue.</p>

