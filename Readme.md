# GOL-PJs

gol-pjs (pronounced goal - pee jays) is a set of tools for [Conway's Game of
Life](https://en.wikipedia.org/wiki/Conway%27s_Game_of_Life).

This repo contains Javascript and Python implementations of the Game of Life
using the List Life algorithm.

## Start Page

To visit the start page, run a web server to host the pages in this directory.
For example, run this Python command:

<pre>
python -m http.server 8000
</pre>

and visit `http://localhost:8000` in your browser to view the page.

## Normal Life

"Normal" Life is a normal one-color Game of Life that uses the normal rules of Life.

## Binary Life

Binary Life is a two-color Game of Life. The game operates the same way as normal Life,
but when a new cell is born, it takes on the color of the majority of its parents.
This second layer of Life is what makes it possible to create the splort of golly
from the Game of Life.

