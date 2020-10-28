# GOL-PJs

gol-pjs (pronounced goal - pee jays) is a set of tools for [Conway's Game of
Life](https://en.wikipedia.org/wiki/Conway%27s_Game_of_Life).

The Python representation of the Game of Life in this repo is intended to initialize
and run the Game of Life, and to allow an import or export of its state at any given point.
This can then be loaded into the Javascript representation to use it as a viewer.

The Javascript representation of the Game of Life in this repo can be used in two ways:

* As a standalone Game of Life simulator, advancing the state of the game and
  applying the rules itself to evolve the state (and providing a way of exporting
  the state of the game at a given point, to share later)

* As a viewer for a particular state of a particular game that was generated
  using the Python Game of Life simulator

## Javascript


