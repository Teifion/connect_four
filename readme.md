This is the 2nd game I've had a go at making for work. It's a lot simpler than
Wordy because I want to practice:

1 - a more decoupled design
2 - a more functional programming style
3 - making it easier to test
4 - working with multiple developers (assuming any join in)

A more decoupled design
---
By placing as little logic in Pyramid specific locations we should make it
easier to port to other frameworks or even other languages. Additionally I'm
trying to allow a different user system from the one in my current system.

A more functional programming style
---
Having recently been trying to learn Haskell I'm seeing that part of my issue
is I can't find anything to write in it. If I write this in a Pure vs Impure
setup then I hope to make it easier to re-write in Haskell later.

Making it easier to test
---
Granted this is more a by-product of the above; but I'd love to have a better
tested product.

Working with multiple developers
---
Does what it says on the tin
