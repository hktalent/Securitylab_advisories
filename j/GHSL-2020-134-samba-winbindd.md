>
    <header class="post-header d-block mb-6">
      <div class="date text-mono f5 my-3">October 29, 2020</div>
      <h1 class="my-2 h00-mktg lh-condensed">GHSL-2020-134: NULL dereference in Samba - CVE-2020-14323</h1>

      
      
      
      
      

      

      <a target="_blank" class="sc-frDJqD SgxRc d-inline-flex flex-row flex-items-center text-gray" href="https://github.com/anticomputer">
        <img class="mr-3" src="https://avatars.githubusercontent.com/u/13686387?s=35" height="35" width="35">
        <span>Bas Alberts</span>
      </a>
    </header>

    <main id="content" class="markdown-body" aria-label="Content">
      <h2 id="summary">Summary</h2>

<p>An unprivileged local user may trigger a NULL dereference bug in Samba’s Winbind service leading to Denial of Service (DoS).</p>

<h2 id="product">Product</h2>

<p>Samba</p>

<h2 id="tested-version">Tested Version</h2>

<p>samba-4.7.6+dfsg~ubuntu</p>

<h2 id="details">Details</h2>

<h3 id="issue-1-null-dereference-in-winbindd_lookupsids_recv">Issue 1: NULL dereference in winbindd_lookupsids_recv</h3>

<p>Samba’s Winbind service exposes two UNIX sockets through which winbind client requests are received and answered.</p>

<p>One of these sockets handles unprivileged commands and the other handles privileged commands.</p>

<p>The unprivileged socket is available to unprivileged local users. In our Samba installation this unprivileged socket could be reached via <code class="language-plaintext highlighter-rouge">/var/run/samba/winbindd/pipe</code> and does not require any special permissions to open.</p>

<div class="language-plaintext highlighter-rouge"><div class="highlight"><pre class="highlight"><code>anticomputer@dc1:~$ ls -alrt /var/run/samba/winbindd
total 0
drwxr-xr-x 7 root root 440 Jul  8 22:11 ..
srwxrwxrwx 1 root root   0 Jul  8 22:11 pipe
drwxr-xr-x 2 root root  60 Jul  8 22:11 .
anticomputer@dc1:~$
</code></pre></div></div>

<p>This presents an interesting attack surface from an attacker perspective as the Winbind service generally runs with root privileges. The available Winbind commands on the unprivileged socket are enumerated in <code class="language-plaintext highlighter-rouge">winbindd.c:async_nonpriv_table</code>. Requests for these commands are supplied in the form of a user supplied (thus attacker controlled) <code class="language-plaintext highlighter-rouge">winbind_request</code> data structure.</p>

<p>One of the available unprivileged commands is <code class="language-plaintext highlighter-rouge">WINBINDD_LOOKUPSIDS</code>. This command’s incoming request handler is defined in <code class="language-plaintext highlighter-rouge">winbindd_lookupsids.c:winbindd_lookupsids_send</code> as follows:</p>

<pre><code class="language-C">struct tevent_req *winbindd_lookupsids_send(TALLOC_CTX *mem_ctx,
					    struct tevent_context *ev,
					   struct winbindd_cli_state *cli,
					   struct winbindd_request *request)
{
	struct tevent_req *req, *subreq;
	struct winbindd_lookupsids_state *state;

	req = tevent_req_create(mem_ctx, &amp;state,
				struct winbindd_lookupsids_state);
	if (req == NULL) {
		return NULL;
	}

	DEBUG(3, ("lookupsids\n"));

	if (request-&gt;extra_len == 0) {
		tevent_req_done(req);
[1]
		return tevent_req_post(req, ev);
	}
	if (request-&gt;extra_data.data[request-&gt;extra_len-1] != '\0') {
		DEBUG(10, ("Got invalid sids list\n"));
		tevent_req_nterror(req, NT_STATUS_INVALID_PARAMETER);
		return tevent_req_post(req, ev);
	}
	if (!parse_sidlist(state, request-&gt;extra_data.data,
			   &amp;state-&gt;sids, &amp;state-&gt;num_sids)) {
		DEBUG(10, ("parse_sidlist failed\n"));
		tevent_req_nterror(req, NT_STATUS_INVALID_PARAMETER);
		return tevent_req_post(req, ev);
	}
[2]
	subreq = wb_lookupsids_send(state, ev, state-&gt;sids, state-&gt;num_sids);
	if (tevent_req_nomem(subreq, req)) {
		return tevent_req_post(req, ev);
	}
	tevent_req_set_callback(subreq, winbindd_lookupsids_done, req);
	return req;
}
</code></pre>

<p>We note that this command handler normally expects to receive an extra set of data tagged onto the client request, based on the <code class="language-plaintext highlighter-rouge">request-&gt;extra_len</code> variable. When this data is available, it is subsequently parsed via <code class="language-plaintext highlighter-rouge">parse_sidlist</code> and the result state for the client request is updated via <code class="language-plaintext highlighter-rouge">wb_lookupsids_send</code> at [2].</p>

<p><code class="language-plaintext highlighter-rouge">wb_lookupsids_send</code> will lookup any domains associated to the parsed sid list and subsequently update the request result state to include those domain results via the <code class="language-plaintext highlighter-rouge">state-&gt;domains</code> pointer. This occurs via a call to <code class="language-plaintext highlighter-rouge">wb_lookupsids_get_domain</code> which will allocate memory to store any domain results and initialize the <code class="language-plaintext highlighter-rouge">state-&gt;domains</code> pointer accordingly.</p>

<p>However, if there is no extra data available in the request, i.e. <code class="language-plaintext highlighter-rouge">request-&gt;extra_len</code> is 0, or there are no sids available in the sid list, i.e. <code class="language-plaintext highlighter-rouge">state-&gt;num_sids</code> is 0, then the <code class="language-plaintext highlighter-rouge">state-&gt;domains</code> pointer is not explicitly initialized.</p>

<p>In the case where there is extra data (i.e. <code class="language-plaintext highlighter-rouge">request-&gt;extra_len</code> != 0) but the resulting <code class="language-plaintext highlighter-rouge">state-&gt;num_sids</code> remains 0 this is alleviated by the fact that <code class="language-plaintext highlighter-rouge">wb_lookupsids_send</code> allocates memory into <code class="language-plaintext highlighter-rouge">state-&gt;res_domains</code>, which is moved into <code class="language-plaintext highlighter-rouge">state-&gt;domains</code> via a call to <code class="language-plaintext highlighter-rouge">talloc_move</code> in <code class="language-plaintext highlighter-rouge">wb_lookupsids_recv</code> by way of the <code class="language-plaintext highlighter-rouge">winbindd_lookupsids_done</code> callback prior to any dereference of the <code class="language-plaintext highlighter-rouge">state-&gt;domains</code> pointer.</p>

<p>However, when <code class="language-plaintext highlighter-rouge">request-&gt;extra_len</code> is 0, this code path is never invoked and <code class="language-plaintext highlighter-rouge">state-&gt;domains</code> remains <code class="language-plaintext highlighter-rouge">NULL</code>.</p>

<p>The initial memory for the state structure is allocated via <code class="language-plaintext highlighter-rouge">talloc_zero_size</code>, which provides memory allocations that are initialized to zero. This ensures that even when <code class="language-plaintext highlighter-rouge">state-&gt;domains</code> and <code class="language-plaintext highlighter-rouge">state-&gt;res_domains</code> are not properly initialized, they will always be <code class="language-plaintext highlighter-rouge">NULL</code>.</p>

<p>After the initial request has been parsed and the request state has been updated with any pending results, result delivery for the <code class="language-plaintext highlighter-rouge">WINBINDD_LOOKUPSIDS</code> is handled by <code class="language-plaintext highlighter-rouge">winbindd_lookupsids.c:winbindd_lookupsids_recv</code>:</p>

<pre><code class="language-C">NTSTATUS winbindd_lookupsids_recv(struct tevent_req *req,
				  struct winbindd_response *response)
{
	struct winbindd_lookupsids_state *state = tevent_req_data(
		req, struct winbindd_lookupsids_state);
	NTSTATUS status;
	char *result;
	uint32_t i;

	if (tevent_req_is_nterror(req, &amp;status)) {
		DEBUG(5, ("wb_lookupsids failed: %s\n", nt_errstr(status)));
		return status;
	}

[1]
	result = talloc_asprintf(response, "%d\n", (int)state-&gt;domains-&gt;count);
	if (result == NULL) {
		return NT_STATUS_NO_MEMORY;
	}

	for (i=0; i&lt;state-&gt;domains-&gt;count; i++) {
		fstring sid_str;

		result = talloc_asprintf_append_buffer(
			result, "%s %s\n",
			sid_to_fstring(sid_str,
				       state-&gt;domains-&gt;domains[i].sid),
			state-&gt;domains-&gt;domains[i].name.string);
		if (result == NULL) {
			return NT_STATUS_NO_MEMORY;
		}
	}

	result = talloc_asprintf_append_buffer(
		result, "%d\n", (int)state-&gt;names-&gt;count);
	if (result == NULL) {
		return NT_STATUS_NO_MEMORY;
	}

	for (i=0; i&lt;state-&gt;names-&gt;count; i++) {
		struct lsa_TranslatedName *name;

		name = &amp;state-&gt;names-&gt;names[i];

		result = talloc_asprintf_append_buffer(
			result, "%d %d %s\n",
			(int)name-&gt;sid_index, (int)name-&gt;sid_type,
			name-&gt;name.string);
		if (result == NULL) {
			return NT_STATUS_NO_MEMORY;
		}
	}

	response-&gt;extra_data.data = result;
	response-&gt;length += talloc_get_size(result);
	return NT_STATUS_OK;
}
</code></pre>

<p>At [1] we then notice a dereference of <code class="language-plaintext highlighter-rouge">state-&gt;domains</code>, which means that there exists an opportunity to trigger a NULL dereference, as we can craft a result state in which <code class="language-plaintext highlighter-rouge">state-&gt;domains</code> remains unitialized by sending a <code class="language-plaintext highlighter-rouge">WINBINDD_LOOKUPSIDS</code> command with <code class="language-plaintext highlighter-rouge">request-&gt;extra_len</code> set to 0.</p>

<p>Doing so results in the following crash:</p>

<div class="language-plaintext highlighter-rouge"><div class="highlight"><pre class="highlight"><code>Program received signal SIGSEGV, Segmentation fault.
0x000055687ae13f61 in winbindd_lookupsids_recv (req=0x55687cc3ccd0,
    response=0x55687d3c5470) at ../source3/winbindd/winbindd_lookupsids.c:103
103             result = talloc_asprintf(response, "%d\n", (int)state-&gt;domains-&gt;cou
nt);
(gdb) x/i$pc
=&gt; 0x55687ae13f61 &lt;winbindd_lookupsids_recv+177&gt;:       mov    (%rax),%edx
(gdb) i r rax
rax            0x0      0
(gdb) p state-&gt;domains
$5 = (struct lsa_RefDomainList *) 0x0
(gdb) bt
#0  0x0000561efefb6f61 in winbindd_lookupsids_recv (req=0x561f00f42930, response=0x561f018977d0)
    at ../source3/winbindd/winbindd_lookupsids.c:103
#1  0x0000561efef7d1dd in wb_request_done (req=0x561f00f42930)
    at ../source3/winbindd/winbindd.c:755
#2  0x00007facf6e191a4 in tevent_common_loop_immediate ()
</code></pre></div></div>

<p>On <code class="language-plaintext highlighter-rouge">NULL</code> dereference the Winbind service will segfault and its signal handling will then abort the process. This results in a Denial of Service against any functionality of the local system that depends on the Winbind service.</p>

<h4 id="impact">Impact</h4>

<p>This issue may lead to Denial of Service.</p>

<h4 id="remediation">Remediation</h4>

<p>Ensure the <code class="language-plaintext highlighter-rouge">state-&gt;domains</code> pointer is verified to be initialized prior to any use in <code class="language-plaintext highlighter-rouge">winbindd_lookupsids_recv</code>.</p>

<h2 id="cve">CVE</h2>

<ul>
  <li>CVE-2020-14323</li>
</ul>

<h2 id="coordinated-disclosure-timeline">Coordinated Disclosure Timeline</h2>

<ul>
  <li>07/09/2020: Vendor contacted</li>
  <li>07/09/2020: Vendor acknowledges report receipt</li>
  <li>09/30/2020: Vendor requests extension of embargo for October</li>
  <li>10/29/2020: Vendor published advisory and fixed releases</li>
</ul>

<h2 id="resources">Resources</h2>

<ul>
  <li>Vendor Advisory: https://www.samba.org/samba/security/CVE-2020-14323.html</li>
</ul>

<h2 id="credit">Credit</h2>

<p>This issue was discovered and reported by GHSL team member <a href="https://github.com/anticomputer">@anticomputer (Bas Alberts)</a>.</p>

<h2 id="contact">Contact</h2>

<p>You can contact the GHSL team at <code class="language-plaintext highlighter-rouge">securitylab@github.com</code>, please include a reference to <code class="language-plaintext highlighter-rouge">GHSL-2020-134</code> in any communication regarding this issu