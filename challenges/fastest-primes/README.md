# fastest-primes
Entry: primes.js — odd-only bitset sieve of Eratosthenes.
Run command: `node primes.js` (reads N on stdin, prints pi(N)).
Verified: pi(10)=4, pi(100000)=9592, pi(1000000)=78498,
pi(5000000)=348513 in ~0.13s wall including Node startup (v2: synchronous stdin read, index-space marking, single counting pass; re-verified on all public cases plus edge cases 0..5).
