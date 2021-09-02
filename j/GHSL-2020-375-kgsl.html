<header class="post-header d-block mb-6">
      <div class="date text-mono f5 my-3">March 8, 2021</div>
      <h1 class="my-2 h00-mktg lh-condensed">GHSL-2020-375: Use-after-free (UaF) in Qualcomm kgsl driver - CVE-2020-11239</h1>

      
      
      
      
      

      

      <a target="_blank" class="sc-frDJqD SgxRc d-inline-flex flex-row flex-items-center text-gray" href="https://github.com/m-y-mo">
        <img class="mr-3" src="https://avatars.githubusercontent.com/u/15773368?s=35" height="35" width="35">
        <span>Man Yue Mo</span>
      </a>
    </header>

    <main id="content" class="markdown-body" aria-label="Content">
      <h2 id="coordinated-disclosure-timeline">Coordinated Disclosure Timeline</h2>
<ul>
  <li>16/07/2020 Reported to Android security team as <a href="https://issuetracker.google.com/issues/161467620">Issue 161467620</a>, later assigned Android ID 161544755</li>
  <li>20/07/2020 Realised it was a Qualcomm issue and asked if I should report directly it to Qualcomm instead, but was told not to.</li>
  <li>22/07/2020 Was told the ticket was forwarded to Qualcomm.</li>
  <li>11/08/2020 Was told that Qualcomm had successfully reproduced the issue.</li>
  <li>01/01/2021 <a href="https://source.android.com/security/bulletin/2021-01-01">Fixed in January bulletin</a> as CVE-2020-11239 and Android ID A-168722551. No credit given.</li>
  <li>05/01/2021 As both the reported date from Qualcomm (26/07/2020) and the Android ID from the bulletin (168722551) indicated that we reported the issue before the one acknowledged in the bulletin, I asked if Android security team can confirm that it is the case.</li>
  <li>05/01/2021 Android security team responded saying that they would investigate.</li>
  <li>25/01/2021 Android security team confirmed that I will be acknowledged as the original reporter of the issue.</li>
</ul>

<h2 id="summary">Summary</h2>

<p>Use-after-free in <code class="language-plaintext highlighter-rouge">kgsl_ioctl_gpuobj_import</code> and <code class="language-plaintext highlighter-rouge">kgsl_ioctl_map_user_mem</code> of the Qualcomm kgsl driver</p>

<h2 id="product">Product</h2>
<p>msm kernel</p>

<h2 id="tested-version">Tested Version</h2>
<p>Pixel 4 QQ3A.200705.002 build</p>

<h2 id="details">Details</h2>

<p>The code references here is in the coral-4.14 branch of the kernel. The use-after-free issue seems to only affect this branch (after the new ION ABI is introduced in 4.12). In the <code class="language-plaintext highlighter-rouge">kgsl_ioctl_gpuobj_import</code> function, if the parameter type is set to <code class="language-plaintext highlighter-rouge">KGSL_USER_MEM_TYPE_ADDR</code>, then the function <code class="language-plaintext highlighter-rouge">_gpuobj_map_useraddr</code> will be used to create the memory mapping [1]. This function will call <code class="language-plaintext highlighter-rouge">kgsl_setup_useraddr</code> [2] and try to create a mapping with dma first [3]. If a valid dma buffer is found, it will then use it to create the mapping, and attach the dma buffer to the device [4], [5]</p>

<div class="language-plaintext highlighter-rouge"><div class="highlight"><pre class="highlight"><code>static int kgsl_setup_dma_buf(struct kgsl_device *device,
                                struct kgsl_pagetable *pagetable,
                                struct kgsl_mem_entry *entry,
                                struct dma_buf *dmabuf)
{
        int ret = 0;
        struct scatterlist *s;
        struct sg_table *sg_table;
        struct dma_buf_attachment *attach = NULL;
        struct kgsl_dma_buf_meta *meta;
        meta = kzalloc(sizeof(*meta), GFP_KERNEL);
        if (!meta)
                return -ENOMEM;
        attach = dma_buf_attach(dmabuf, device-&gt;dev);  //&lt;------- a.
    ...
        sg_table = dma_buf_map_attachment(attach, DMA_TO_DEVICE);
    ...
        meta-&gt;table = sg_table;
        entry-&gt;priv_data = meta;
        entry-&gt;memdesc.sgt = sg_table;           //&lt;------- b.
</code></pre></div></div>

<p>This will create a <code class="language-plaintext highlighter-rouge">sg_table</code> for the attachment by duplicating the one from the <code class="language-plaintext highlighter-rouge">dma_buf</code> (a. and [6], see below)</p>

<p>The ion implementation of <code class="language-plaintext highlighter-rouge">dma_buf_attach</code> in (a.) is as follows:</p>

<div class="language-plaintext highlighter-rouge"><div class="highlight"><pre class="highlight"><code>static int ion_dma_buf_attach(struct dma_buf *dmabuf, struct device *dev,
                                struct dma_buf_attachment *attachment)
{
    ...
        table = dup_sg_table(buffer-&gt;sg_table);
    ...
        a-&gt;table = table;                          //&lt;---- c. duplicated table stored in attachment, which is the output of dma_buf_attach in a.
    ...
        mutex_lock(&amp;buffer-&gt;lock);
        list_add(&amp;a-&gt;list, &amp;buffer-&gt;attachments);  //&lt;---- d. attachment got added to dma_buf::attachments
        mutex_unlock(&amp;buffer-&gt;lock);
        return 0;
}
</code></pre></div></div>

<p>This stores the duplicated table in an <code class="language-plaintext highlighter-rouge">ion_dma_buf_attachment</code> as raw pointer, while at the same time, the table is also stored in <code class="language-plaintext highlighter-rouge">entry-&gt;memdesc.sgt</code> in (b) and the <code class="language-plaintext highlighter-rouge">ion_dma_buf_attachment</code> is also stored in the attachment list of <code class="language-plaintext highlighter-rouge">dma_buf</code>.</p>

<table>
  <tbody>
    <tr>
      <td>If the ioctl call then failed at the</td>
      <td>kgsl_mem_entry_attach_process</td>
      <td>call, it will go to unmap [7]</td>
    </tr>
  </tbody>
</table>

<div class="language-plaintext highlighter-rouge"><div class="highlight"><pre class="highlight"><code>unmap:
        if (param-&gt;type == KGSL_USER_MEM_TYPE_DMABUF) {
                kgsl_destroy_ion(entry-&gt;priv_data);
                entry-&gt;memdesc.sgt = NULL;
        }
        kgsl_sharedmem_free(&amp;entry-&gt;memdesc);  //&lt;---- deletes |table| in c.
</code></pre></div></div>

<p>As <code class="language-plaintext highlighter-rouge">param-&gt;type</code> in this case is <code class="language-plaintext highlighter-rouge">KGSL_USER_MEM_TYPE_ADDR</code>, <code class="language-plaintext highlighter-rouge">kgsl_destroy_ion</code> will not be called, which means that the <code class="language-plaintext highlighter-rouge">dma_buf</code> will remain attached to the gpu, and more importantly, the <code class="language-plaintext highlighter-rouge">ion_dma_buf_attachment</code> created in <code class="language-plaintext highlighter-rouge">ion_dma_buf_attach</code> will remain in the attachment list of the buffer. Now <code class="language-plaintext highlighter-rouge">kgsl_sharedmem_free</code> that follows will delete <code class="language-plaintext highlighter-rouge">memdesc.sgt</code>, which is the same as <code class="language-plaintext highlighter-rouge">table</code> in (c):</p>

<div class="language-plaintext highlighter-rouge"><div class="highlight"><pre class="highlight"><code>void kgsl_sharedmem_free(struct kgsl_memdesc *memdesc)
{
    ....
        if (memdesc-&gt;sgt) {
                sg_free_table(memdesc-&gt;sgt);
                kfree(memdesc-&gt;sgt);
        }
    ...
}
</code></pre></div></div>

<p>After this point, the <code class="language-plaintext highlighter-rouge">dma_buf</code>, which the user holds a reference to and can call its ioctl at any time, will contain a reference to an <code class="language-plaintext highlighter-rouge">ion_dma_buf_attachment</code> in its <code class="language-plaintext highlighter-rouge">attachments</code> list, and this attachment holds a reference to a free’d <code class="language-plaintext highlighter-rouge">sg_table</code>. A use-after-free can then be triggered, for example, by using the <code class="language-plaintext highlighter-rouge">DMA_BUF_IOCTL_SYNC</code> ioctl call on this <code class="language-plaintext highlighter-rouge">dma_buf</code>, which is implemented by <code class="language-plaintext highlighter-rouge">__ion_dma_buf_begin_cpu_access</code>:</p>

<div class="language-plaintext highlighter-rouge"><div class="highlight"><pre class="highlight"><code>static int __ion_dma_buf_begin_cpu_access(struct dma_buf *dmabuf,
                                          enum dma_data_direction direction,
                                          bool sync_only_mapped)
{
    ...
        list_for_each_entry(a, &amp;buffer-&gt;attachments, list) {
        ...
                if (sync_only_mapped)
                        tmp = ion_sgl_sync_mapped(a-&gt;dev, a-&gt;table-&gt;sgl,        //&lt;--- use-after-free of a-&gt;table
                                                  a-&gt;table-&gt;nents,
                                                  &amp;buffer-&gt;vmas,
                                                  direction, true);
                else
                        dma_sync_sg_for_cpu(a-&gt;dev, a-&gt;table-&gt;sgl,              //&lt;--- use-after-free of a-&gt;table
                                            a-&gt;table-&gt;nents, direction);
            ...
                }
        }
...
}
</code></pre></div></div>

<p>The <code class="language-plaintext highlighter-rouge">kgsl_ioctl_map_user_mem</code> system call also has a similar problem.</p>

<h2 id="cve">CVE</h2>
<ul>
  <li>CVE-2020-11239</li>
</ul>

<h4 id="impact">Impact</h4>

<p>Can be exploited from the application sandbox to achieve arbitrary kernel code execution in many devices.</p>

<h2 id="credit">Credit</h2>

<p>This issue was discovered and reported by GHSL team member <a href="https://github.com/m-y-mo">@m-y-mo (Man Yue Mo)</a>.</p>

<h2 id="contact">Contact</h2>

<p>You can contact the GHSL team at <code class="language-plaintext highlighter-rouge">securitylab@github.com</code>, please include the <code class="language-plaintext highlighter-rouge">GHSL-2020-375</code> in any communication regarding this issue.</p>

  