<header class="post-header d-block mb-6">
      <div class="date text-mono f5 my-3">February 24, 2021</div>
      <h1 class="my-2 h00-mktg lh-condensed">GHSL-2020-228: Weak JSON Web Token (JWT) signing secret in YApi - CVE-2021-27884</h1>

      
      
      
      
      

      

      <a target="_blank" class="sc-frDJqD SgxRc d-inline-flex flex-row flex-items-center text-gray" href="https://github.com/jarlob">
        <img class="mr-3" src="https://avatars.githubusercontent.com/u/26652396?s=35" height="35" width="35">
        <span>Jaroslav Lobacevski</span>
      </a>
    </header>

    <main id="content" class="markdown-body" aria-label="Content">
      <h2 id="coordinated-disclosure-timeline">Coordinated Disclosure Timeline</h2>

<ul>
  <li>2020-11-18: Report sent to maintainer</li>
  <li>2020-12-01: Created a <a href="https://github.com/YMFE/yapi/pull/2011">public pull request</a> asking for a contact</li>
  <li>2021-02-16: Disclosure deadline reached</li>
  <li>2021-02-23: <a href="https://github.com/YMFE/yapi/issues/2117">Public issue</a> was created</li>
</ul>

<h2 id="summary">Summary</h2>

<p>Weak random number generator is used to sign JSON Web Token (JWT).</p>

<h2 id="product">Product</h2>

<p><a href="https://github.com/YMFE/yapi">YApi</a></p>

<h2 id="tested-version">Tested Version</h2>

<p>The latest commit to the date: <a href="https://github.com/YMFE/yapi/tree/8e1f6546d52ad6a3f8d3ce3325eb1d0276209f4c">8e1f654</a>.</p>

<h2 id="details">Details</h2>

<h3 id="jwt-signing">JWT signing</h3>

<p>Function <a href="https://github.com/YMFE/yapi/blob/8e1f6546d52ad6a3f8d3ce3325eb1d0276209f4c/server/utils/commons.js#L155-L159">randStr</a> is using a cryptographically insecure pseudo-random number generator <code class="language-plaintext highlighter-rouge">Math.random</code> to create a randomly looking string that later is used to sign and verify issued tokens:</p>

<div class="language-js highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="nx">exports</span><span class="p">.</span><span class="nx">randStr</span> <span class="o">=</span> <span class="p">()</span> <span class="o">=&gt;</span> <span class="p">{</span>
  <span class="k">return</span> <span class="nb">Math</span><span class="p">.</span><span class="nx">random</span><span class="p">()</span>
    <span class="p">.</span><span class="nx">toString</span><span class="p">(</span><span class="mi">36</span><span class="p">)</span>
    <span class="p">.</span><span class="nx">substr</span><span class="p">(</span><span class="mi">2</span><span class="p">);</span>
<span class="p">};</span>
</code></pre></div></div>

<p>When a new user is created the <code class="language-plaintext highlighter-rouge">randStr</code> function is used to generate a <code class="language-plaintext highlighter-rouge">passsalt</code>. It is used as a salt to hash the password and as the secret to sign a JWT that authenticates the user:</p>
<div class="language-js highlighter-rouge"><div class="highlight"><pre class="highlight"><code>  <span class="k">async</span> <span class="nx">reg</span><span class="p">(</span><span class="nx">ctx</span><span class="p">)</span> <span class="p">{</span>
<span class="p">...</span>
    <span class="kd">let</span> <span class="nx">passsalt</span> <span class="o">=</span> <span class="nx">yapi</span><span class="p">.</span><span class="nx">commons</span><span class="p">.</span><span class="nx">randStr</span><span class="p">();</span>
    <span class="kd">let</span> <span class="nx">data</span> <span class="o">=</span> <span class="p">{</span>
      <span class="na">username</span><span class="p">:</span> <span class="nx">params</span><span class="p">.</span><span class="nx">username</span><span class="p">,</span>
      <span class="na">password</span><span class="p">:</span> <span class="nx">yapi</span><span class="p">.</span><span class="nx">commons</span><span class="p">.</span><span class="nx">generatePassword</span><span class="p">(</span><span class="nx">params</span><span class="p">.</span><span class="nx">password</span><span class="p">,</span> <span class="nx">passsalt</span><span class="p">),</span> <span class="c1">//加密</span>
      <span class="na">email</span><span class="p">:</span> <span class="nx">params</span><span class="p">.</span><span class="nx">email</span><span class="p">,</span>
      <span class="na">passsalt</span><span class="p">:</span> <span class="nx">passsalt</span><span class="p">,</span>
<span class="p">...</span>
      <span class="k">this</span><span class="p">.</span><span class="nx">setLoginCookie</span><span class="p">(</span><span class="nx">user</span><span class="p">.</span><span class="nx">_id</span><span class="p">,</span> <span class="nx">user</span><span class="p">.</span><span class="nx">passsalt</span><span class="p">);</span>
<span class="p">...</span>
  <span class="p">}</span>
<span class="p">...</span>
  <span class="nx">setLoginCookie</span><span class="p">(</span><span class="nx">uid</span><span class="p">,</span> <span class="nx">passsalt</span><span class="p">)</span> <span class="p">{</span>
    <span class="kd">let</span> <span class="nx">token</span> <span class="o">=</span> <span class="nx">jwt</span><span class="p">.</span><span class="nx">sign</span><span class="p">({</span> <span class="na">uid</span><span class="p">:</span> <span class="nx">uid</span> <span class="p">},</span> <span class="nx">passsalt</span><span class="p">,</span> <span class="p">{</span> <span class="na">expiresIn</span><span class="p">:</span> <span class="dl">'</span><span class="s1">7 days</span><span class="dl">'</span> <span class="p">});</span>
    <span class="k">this</span><span class="p">.</span><span class="nx">ctx</span><span class="p">.</span><span class="nx">cookies</span><span class="p">.</span><span class="kd">set</span><span class="p">(</span><span class="dl">'</span><span class="s1">_yapi_token</span><span class="dl">'</span><span class="p">,</span> <span class="nx">token</span><span class="p">,</span> <span class="p">{</span>
      <span class="na">expires</span><span class="p">:</span> <span class="nx">yapi</span><span class="p">.</span><span class="nx">commons</span><span class="p">.</span><span class="nx">expireDate</span><span class="p">(</span><span class="mi">7</span><span class="p">),</span>
      <span class="na">httpOnly</span><span class="p">:</span> <span class="kc">true</span>
    <span class="p">});</span>
<span class="p">...</span>
  <span class="p">}</span>
</code></pre></div></div>

<p>The <code class="language-plaintext highlighter-rouge">Math.random</code> returns a floating-point number that is more than or equal to 0.0 and less than 1.0. The call to <code class="language-plaintext highlighter-rouge">toString(36)</code> formats the number as base36. For example, <code class="language-plaintext highlighter-rouge">0.19280841320093556</code> gets encoded as <code class="language-plaintext highlighter-rouge">0.6xvo3g36129</code>. The first two characters are trimmed and the result is <code class="language-plaintext highlighter-rouge">6xvo3g36129</code>. The generated secret is mostly 10-12 characters long and consists of numbers and lowercase Latin alphabet characters only. Since the trimmed part is always <code class="language-plaintext highlighter-rouge">0.</code> the calculation is completely reversible.</p>

<p>The weakness of cryptographically insecure pseudo-random number generators is that given some number of observed values the internal state of the generator can be recreated that reveals the numbers generated in the past or allows calculation of the future outputs. The internal state of the current implementation of <code class="language-plaintext highlighter-rouge">Math.random</code> in Node.js (a modification of XorShift128+ algorithm) can be recreated from three observed consecutive values.</p>

<p>To get the values an attacker may automate the user creation process to get three new user tokens rapidly, then run a brute force attack on the JWT HMAC signatures. This still should not be feasible to do in a reasonable time on a single machine like:</p>

<div class="language-plaintext highlighter-rouge"><div class="highlight"><pre class="highlight"><code>- Hashcat version: 6.1.1
- Nvidia GPUs: 4 * Tesla V100

Hashmode: 16500 - JWT (JSON Web Token)

Speed.#1.........:  1368.5 MH/s (244.80ms) @ Accel:32 Loops:128 Thr:1024 Vec:1
Speed.#2.........:  1368.9 MH/s (244.65ms) @ Accel:32 Loops:128 Thr:1024 Vec:1
Speed.#3.........:  1368.2 MH/s (244.80ms) @ Accel:32 Loops:128 Thr:1024 Vec:1
Speed.#4.........:  1368.3 MH/s (244.74ms) @ Accel:32 Loops:128 Thr:1024 Vec:1
Speed.#*.........:  5473.9 MH/s
</code></pre></div></div>

<p>However a very rough estimation shows that by using cloud computing the attack could cost from 8 000$ to 24 000$ to break the tokens (Cracking three values versus one value has very little penalty as cracking machines are optimized for multiple hashes and cracking a single hash doesn’t fully utilize computer resources). Please notice that the token’s 7 days expiration time doesn’t put a limit on the attack as the target is the <code class="language-plaintext highlighter-rouge">passsalt</code> value used to sign the token.</p>

<h4 id="impact">Impact</h4>

<p>After successfully brute forcing the three pseudo-random values the attacker may recreate the <code class="language-plaintext highlighter-rouge">passsalt</code> values that are used to sign tokens of other users. It may be argued if there is an incentive to spend this amount of resources, but GPUs get better all the time.</p>

<h2 id="cve">CVE</h2>
<ul>
  <li>CVE-2021-27884</li>
</ul>

<h2 id="credit">Credit</h2>

<p>This issue was discovered and reported by GHSL team member <a href="https://github.com/JarLob">@JarLob (Jaroslav Lobačevski)</a>.</p>

<h2 id="contact">Contact</h2>

<p>You can contact the GHSL team at <code class="language-plaintext highlighter-rouge">securitylab@github.com</code>, please include a reference to <code class="language-plaintext highlighter-rouge">GHSL-2020-228</code> in any communication regarding this issue