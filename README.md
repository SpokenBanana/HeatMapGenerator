# HeatMapGenerator
Creates a keyboard heat map from comments scraped from reddit. Uses Praw and PIL to scrape reddit and generate the heat map

Example
# Bohemian Rhapsody Lyrics
![screenshot](http://i.imgur.com/e716f2A.png)

The image is generated using PIL, the more a key is pressed, the more red it is, the less the key is pressed, the more yellow it is. White keys represents keys that were never pressed. This uses reddit comments as the source text for generating a keyboard heat map.
