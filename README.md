# tiny-chess-01 entry

A chess engine in 3,956 bytes of Python (`main.py`). The file is an
lzma + base85 packed payload with a one-line unpacker; the unpacked
engine is original code written for this competition.

## The engine

- 0x88 board, fully legal move generation (perft-verified), make/unmake
  with incremental Zobrist hashing.
- Negamax alpha-beta with iterative deepening under a fixed budget of
  70,000 nodes per move (no clock anywhere: the same position always
  gets the same move, so replays match move for move).
- Transposition table, quiescence search (captures, promotions and
  check evasions), null-move pruning, late-move reductions, PVS.
- Evaluation: material plus piece-square tables with a separate
  endgame king table; repetition and the fifty-move rule score as
  draws inside the search.
- It plays the whole gauntlet through the env at `MAKEFUN_ENV_URL`
  (POST /game, /move), exactly as the starter did.

## Local practice results

Graded with the kit's own env and scorer on the 3 practice instances
(6 games each, against depth-2 .. nodes-500k):

- starter (greedy capture): Elo 0 on all three.
- this engine (final packed build): trial-0 **1,364** (3W-1D-2L),
  trial-1 **1,279** (3W-0D-3L), trial-2 **1,191** (2W-1D-3L);
  mean 1,278, above the floor on every instance. The dev-phase
  practice grade runs trial-0, where it matches the house
  baseline's own score on that instance (1,364).

The finals floor is 1,154; the house baseline (sunfish 4K) averages
about 1,365 on the same practice set.
