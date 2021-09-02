<header class="post-header d-block mb-6">
      <div class="date text-mono f5 my-3">July 6, 2020</div>
      <h1 class="my-2 h00-mktg lh-condensed">GHSL-2020-058: OOB read in Apache Guacamole prior to 1.2.0 - CVE-2020-9497</h1>

      
      
      
      
      

      

      <a target="_blank" class="sc-frDJqD SgxRc d-inline-flex flex-row flex-items-center text-gray" href="https://github.com/nicowaisman">
        <img class="mr-3" src="https://avatars.githubusercontent.com/u/17729105?s=35" height="35" width="35">
        <span>Nico Waisman</span>
      </a>
    </header>

    <main id="content" class="markdown-body" aria-label="Content">
      <h2 id="summary">Summary</h2>

<p>There is an out of bounds read in Apache Guacamole server’s RDP protocol. The vulnerability exists in the RDP Audio Output Virtual Channel Extension, while trying to parse a PDU of type <code class="language-plaintext highlighter-rouge">WaveInfo</code> which is used to transmit audio data through the channel.</p>

<h2 id="product">Product</h2>

<p>Apache Guacamole Server</p>

<h2 id="tested-version">Tested Version</h2>

<p>Apache Guacamole Server up to commit bbb7949</p>

<h2 id="details">Details</h2>

<h3 id="ghsl-2020-058-out-of-band-read-in-waveinfo-pdu-handler">GHSL-2020-058: Out of band read in WaveInfo PDU handler</h3>

<p>The WaveInfo PDU contains a 16-bit unsigned integer that represents an index into the list of audio formats exchanged between the client and server during the initialization phase. This list is maintained as a 16 member array in <code class="language-plaintext highlighter-rouge">struct guac_rdpsnd</code>. The 16-bit integer (<code class="language-plaintext highlighter-rouge">format</code>) is used to index this array without any boundary checks and as a result may trigger an out of bounds read.</p>

<p>The vulnerability is in <code class="language-plaintext highlighter-rouge">protocols/rdp/channels/rdpsnd/rdpsnd-message.c</code> [235-257]</p>

<div class="language-cpp highlighter-rouge"><div class="highlight"><pre class="highlight"><code>    <span class="cm">/* Read wave information */</span>
    <span class="n">Stream_Read_UINT16</span><span class="p">(</span><span class="n">input_stream</span><span class="p">,</span> <span class="n">rdpsnd</span><span class="o">-&gt;</span><span class="n">server_timestamp</span><span class="p">);</span>
    <span class="n">Stream_Read_UINT16</span><span class="p">(</span><span class="n">input_stream</span><span class="p">,</span> <span class="n">format</span><span class="p">);</span> <span class="p">[</span><span class="mi">1</span><span class="p">]</span>
    <span class="n">Stream_Read_UINT8</span><span class="p">(</span><span class="n">input_stream</span><span class="p">,</span> <span class="n">rdpsnd</span><span class="o">-&gt;</span><span class="n">waveinfo_block_number</span><span class="p">);</span>
    <span class="n">Stream_Seek</span><span class="p">(</span><span class="n">input_stream</span><span class="p">,</span> <span class="mi">3</span><span class="p">);</span>
    <span class="n">Stream_Read</span><span class="p">(</span><span class="n">input_stream</span><span class="p">,</span> <span class="n">rdpsnd</span><span class="o">-&gt;</span><span class="n">initial_wave_data</span><span class="p">,</span> <span class="mi">4</span><span class="p">);</span>

    <span class="cm">/*
     * Size of incoming wave data is equal to the body size field of this
     * header, less the size of a WaveInfo PDU (not including the header),
     * thus body_size - 12.
     */</span>
    <span class="n">rdpsnd</span><span class="o">-&gt;</span><span class="n">incoming_wave_size</span> <span class="o">=</span> <span class="n">header</span><span class="o">-&gt;</span><span class="n">body_size</span> <span class="o">-</span> <span class="mi">12</span><span class="p">;</span>

    <span class="cm">/* Read wave in next iteration */</span>
    <span class="n">rdpsnd</span><span class="o">-&gt;</span><span class="n">next_pdu_is_wave</span> <span class="o">=</span> <span class="n">TRUE</span><span class="p">;</span>

    <span class="cm">/* Reset audio stream if format has changed */</span>
    <span class="k">if</span> <span class="p">(</span><span class="n">audio</span> <span class="o">!=</span> <span class="nb">NULL</span><span class="p">)</span>
        <span class="n">guac_audio_stream_reset</span><span class="p">(</span><span class="n">audio</span><span class="p">,</span> <span class="nb">NULL</span><span class="p">,</span>
                <span class="n">rdpsnd</span><span class="o">-&gt;</span><span class="n">formats</span><span class="p">[</span><span class="n">format</span><span class="p">].</span><span class="n">rate</span><span class="p">,</span>  <span class="p">[</span><span class="mi">2</span><span class="p">]</span>
                <span class="n">rdpsnd</span><span class="o">-&gt;</span><span class="n">formats</span><span class="p">[</span><span class="n">format</span><span class="p">].</span><span class="n">channels</span><span class="p">,</span>
                <span class="n">rdpsnd</span><span class="o">-&gt;</span><span class="n">formats</span><span class="p">[</span><span class="n">format</span><span class="p">].</span><span class="n">bps</span><span class="p">);</span>
</code></pre></div></div>
<p>As can be seen in the above code snippet, at [1] <code class="language-plaintext highlighter-rouge">Stream_Read_UINT16</code> is used to read a 16-bit integer value from the network into the <code class="language-plaintext highlighter-rouge">format</code> variable and at [2] <code class="language-plaintext highlighter-rouge">rdpsnd-&gt;formats</code> is indexed with this remote controlled integer without ensuring that <code class="language-plaintext highlighter-rouge">format</code> does not index outside of the bounds of the array.</p>

<h4 id="impact">Impact</h4>

<p>An authenticated user may potentially leak information about the memory contents of the <code class="language-plaintext highlighter-rouge">guacd</code> process.</p>

<h2 id="cve">CVE</h2>

<ul>
  <li>CVE-2020-9497</li>
</ul>

<h2 id="coordinated-disclosure-timeline">Coordinated Disclosure Timeline</h2>

<p>This report was subject to the GHSL <a href="https://securitylab.github.com/advisories/#policy">coordinated disclosure policy</a>.</p>

<ul>
  <li>04/10/2020: vendor contacted</li>
  <li>04/10/2020: vendor acknowledges report</li>
  <li>05/14/2020: vendor confirms CVE-2020-9497 will be fixed in 1.2.0</li>
  <li>07/01/2020: vendor releases version 1.2.0</li>
</ul>

<h2 id="supporting-resources">Supporting Resources</h2>

<ul>
  <li>https://guacamole.apache.org/security/</li>
  <li>https://research.checkpoint.com/2020/apache-guacamole-rce/</li>
</ul>

<h2 id="credit">Credit</h2>

<p>This issue was discovered and reported by the <a href="https://securitylab.github.com">GitHub Security Lab</a>.</p>

<h2 id="contact">Contact</h2>

<p>You can contact the GHSL team at <code class="language-plaintext highlighter-rouge">securitylab@github.com</code>, please include the <code class="language-plaintext highlighter-rouge">GHSL-2020-058</code> in any communication regarding this issue.</p>

  