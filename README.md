tumblr-display
==============

Tumblr Display

My intention is to create a lightweight framework for displaying a given tumblr nicely onscreen. It is written to be portable and easy to extend. My goal is run this software on a Raspberry Pi with a small lcd display, place a nice wooden frame around it and mount tumblr to my wall.

Dependencies:
All available via easy_install or pip:
pygame
pytumblr

Setup:
Sorry! You have to get an API key from tumblr to request post data. Maybe I will write a scraper to get around this in the future, but for now, you'll have to:
1) Sign up with Tumblr
2) With newly created account, ask for an API key.
3) Open src/Settings.py, fill in the relevant string with your API key info.

To run:
cd src
python main.py
