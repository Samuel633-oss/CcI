Alara Core integration/staging tree
=====================================

Alara is a fully decentralized blockchain with Bitcoin 2009-style Proof-of-Work consensus.

What is Alara Core?
---------------------

Alara Core connects to the Alara peer-to-peer network to download and fully
validate blocks and transactions. It also includes a wallet and graphical user
interface, which can be optionally built.

Further information about Alara Core is available in the [doc folder](/doc).

License
-------

Alara Core is released under the terms of the MIT license. See [COPYING](COPYING) for more
information or see https://opensource.org/license/MIT.

Development Process
-------------------

The `master` branch is regularly built and tested, but it is not guaranteed to be
completely stable. Tags are created regularly from release branches to indicate new official, stable release versions of Alara Core.

The contribution workflow is described in [CONTRIBUTING.md](CONTRIBUTING.md)
and useful hints for developers can be found in [doc/developer-notes.md](doc/developer-notes.md).

Testing
-------

Testing and code review is the bottleneck for development; we get more pull
requests than we can review and test on short notice. Please be patient and help out by testing
other people's pull requests, and remember this is a security-critical project where any mistake might cost people
lots of money.

### Automated Testing

Developers are strongly encouraged to write unit tests for new code, and to
submit new unit tests for old code. Unit tests can be compiled and run
using `make check`.

Alara Specific Features
-----------------------

- **Fixed Supply**: 21,000,000 ALA (no ability to mint/print new tokens beyond this cap)
- **5% Transaction Fee**: Every transaction includes a mandatory 5% fee on the transaction value
- **Proof-of-Work**: SHA-256 mining algorithm, Bitcoin 2009 style
- **Fully Decentralized**: No admin controls, no central authority, no special privileges
- **Free to Start**: Like Bitcoin in 2009, anyone can run a node and mine

## Quick Start

To build and run Alara:

```bash
# Clone the repository
git clone https://github.com/Samuel633-oss/CcI.git
cd CcI

# Build (requires dependencies)
./autogen.sh
./configure
make

# Run a node
./src/alarad

# Or use the wrapper
./src/alara node
```

## Network Parameters

- **Ticker**: ALA
- **Total Supply**: 21,000,000 ALA
- **Block Reward**: Follows Bitcoin halving schedule
- **Transaction Fee**: 5% of transaction value (mandatory)
- **Algorithm**: SHA-256 Proof-of-Work
- **Block Time**: 10 minutes (target)

## Important Notes

- This is a **fork of Bitcoin Core** modified for Alara specifications
- **No minting functions** exist - supply is strictly capped at 21M ALA
- **5% fee is enforced at consensus level** - transactions with insufficient fees are rejected
- **Completely open source** - MIT licensed, no proprietary code
- **Decentralized** - no admin keys, no backdoors, no central control
