# Task: Terminal Snake in C++17

Implement the classic Snake game as a single C++17 program. The program
has two modes: an interactive terminal mode for humans, and a headless
test mode used by other tooling to exercise the game logic. The test
mode is the interface everything downstream depends on, so its behavior
must match this specification exactly, byte for byte where output is
concerned.

## Build constraints

- The entire game lives in one translation unit named `snake.cpp`, at
  the top level of this directory.
- It must compile, with no warnings required but no errors, via
  exactly:

      c++ -std=c++17 -O2 -o snake snake.cpp

- C++17 standard library only. No ncurses, no third-party libraries,
  no platform-exclusive APIs that would break either macOS or Linux
  under clang++ or g++. Interactive rendering may use ANSI escape
  sequences and `termios` for raw keyboard input; the test mode must
  not touch the terminal at all.

## Game rules

- The grid is 20 cells wide and 15 cells tall. Coordinates are
  0-based: `(0, 0)` is the top-left cell, `x` grows rightward
  (0..19), `y` grows downward (0..14).
- The snake starts with length 3, moving right: head at `(10, 7)`,
  body segments at `(9, 7)` and `(8, 7)`.
- Exactly one food item is on the grid at all times, never on a cell
  occupied by the snake. The initial food is placed before the first
  tick.
- Each tick, the game:
  1. Reads one direction input (a key in interactive mode, one move
     character in test mode). If the input is the exact opposite of
     the current direction (e.g. left while moving right), it is
     ignored and the current direction is kept — the snake can never
     reverse into itself. Otherwise the input becomes the current
     direction.
  2. Advances the head one cell in the current direction.
  3. If the new head position is outside the grid, the game ends with
     status `DEAD_WALL`. The tick still counts; the reported head
     position stays at the last in-bounds cell.
  4. Otherwise, if the new head position holds the food, the snake
     grows: length increases by 1, score increases by 1, the tail does
     not move this tick, and a new food is placed. If it does not hold
     food, the tail advances (the last segment is removed).
  5. If the new head position coincides with any body cell occupied
     after the tail movement of this tick, the game ends with status
     `DEAD_SELF`. (Entering the cell the tail just vacated is legal,
     because the tail moved away in the same tick. On a growth tick
     the tail did not move, so its cell still counts.)
- Score is the number of food items eaten. Length is always
  3 + score.

## Food placement and determinism

Food positions are drawn from a pseudo-random generator seeded from
the `--seed` argument (default seed 0 when the flag is absent). The
same seed must always produce the same food sequence for the same
sequence of moves: running the program twice with identical `--seed`
and `--moves` must produce byte-identical output. The choice of PRNG
and placement scheme is yours as long as food never appears on the
snake and the run is fully reproducible from the seed.

## Test mode (the contract)

    ./snake --test --seed <N> --moves <string>

- `<string>` is a sequence of the characters `U`, `D`, `L`, `R`, e.g.
  `UULLDDRR`. Each character is one tick's direction input, applied in
  order under the rules above (including the no-reverse rule).
- Test mode performs no rendering, no delays, no reads from stdin, and
  no terminal control of any kind. It runs the ticks and exits.
- The run stops as soon as the game ends (wall or self collision) or
  the move string is exhausted, whichever comes first. `TICKS` is the
  number of ticks actually executed, counting the fatal tick.
- At the end, print exactly these five lines to stdout, in this order,
  with single spaces and nothing else before, between, or after them:

      TICKS <int>
      LENGTH <int>
      SCORE <int>
      HEAD <x> <y>
      STATUS <ALIVE|DEAD_WALL|DEAD_SELF>

  `STATUS` is `ALIVE` when the move string ran out with the snake
  still alive. Exit code 0 in every case that isn't a usage error.

Example: `./snake --test --seed 5 --moves UU` moves the snake up twice
from the start position, so it prints `HEAD 10 5`, `TICKS 2`, and
`STATUS ALIVE` (length and score depend on whether food was eaten
along the way for that seed).

## Interactive mode

Running `./snake` with no `--test` flag on a terminal plays the game
live: draw the grid (ANSI escapes are fine), move with WASD or the
arrow keys, `q` quits. The snake advances on a timer even without
input; the interval starts around 200 ms and shortens as the score
grows, so the game speeds up. Show the current score during play and
a game-over message with the final score at the end. Keep it simple —
correctness of the shared game logic matters more than presentation,
and the test mode is what the automation drives.

## Deliverable

`snake.cpp` at the top level of this directory, buildable with the
exact command above. No other build artifacts are required; do not
commit a compiled binary.
