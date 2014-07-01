<h1>Tumblr Display</h1>
<p>My intention is to create a lightweight framework for displaying a given tumblr nicely onscreen. It is written to be portable and easy to extend. My goal is run this software on a Raspberry Pi with a small lcd display, place a nice wooden frame around it and mount tumblr to my wall.</p>

<h2>Python Dependencies</h2>
<p>All available via easy_install or pip:</p>
<ul>
<li>pygame</li>
<li>pytumblr</li>
<li>Python Image Library (Pillow)</li>
</ul>

<h2>Binary Dependencies</h2>
<p><a href="http://www.lcdf.org/gifsicle/">Gifsicle</a>, a really great command-line tool for manipulating GIF images, is used for parsing animated GIFs. If <code>gifsicle</code> is not found in your PATH at runtime, then animated GIFs will not be displayed.</p>

<h2>Tumblr API Setup - IMPORTANT</h2>
<p>Sorry! You have to get an API key from tumblr to request other user's tumblr post data. Maybe I will write a scraper to get around this in the future, but for now, you'll have to:</p>
<ol>
<li>Sign up with Tumblr</li>
<li>With newly created account, sign in and ask for an API key in the account dashboard.</li>
<li>Open <code>src/Settings.py</code>, fill in the relevant string with your API key info.</li>
</ol>

<h2>Usage</h2>
<pre><code>cd src
python main.py</code></pre>
