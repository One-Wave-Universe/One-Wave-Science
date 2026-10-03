# Modules

Pieces of the first sim. Each writes one thing. The page only combines them.

| Module | Writes |
|---|---|
| wake.js | kernel(r, sigma) |
| lattice.js | hex sites |
| energy.js | chi and field energy from the parent wake |
| motion.js | children down the gradient |
| view.js | draw |

Bus is `{ parent, sites, kids, energy }`. Drop parent sets amplitude to 0. Camera does not change the step.
