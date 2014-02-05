<h1>Tumblr Display</h1>
<p>My intention is to create a lightweight framework for displaying a given tumblr nicely onscreen. It is written to be portable and easy to extend. My goal is run this software on a Raspberry Pi with a small lcd display, place a nice wooden frame around it and mount tumblr to my wall.</p>

<h2>Dependencies</h2>
<p>All available via easy_install or pip:</p>
<ul>
<li>pygame</li>
<li>pytumblr</li>
</ul>

<h2>Setup</h2>
<p>Sorry! You have to get an API key from tumblr to request post data. Maybe I will write a scraper to get around this in the future, but for now, you'll have to:</p>
<ol>
<li>Sign up with Tumblr</li>
<li>With newly created account, ask for an API key.</li>
<li>Open <code>src/Settings.py</code>, fill in the relevant string with your API key info.</li>
</ol>

<h2>Usage</h2>
<pre><code>cd src
python main.py</code></pre>
