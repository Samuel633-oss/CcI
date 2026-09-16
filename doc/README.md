Alara Core
=============

Setup
---------------------
Alara Core is the original Alara client and it builds the backbone of the network. It downloads and, by default, stores the entire history of Alara transactions, which requires several hundred gigabytes or more of disk space. Depending on the speed of your computer and network connection, the synchronization process can take anywhere from a few hours to several days or more.

To download Alara Core, visit the Alara project page.

Running
---------------------
The following are some helpful notes on how to run Alara Core on your native platform.

### Unix

Unpack the files into a directory and run:

- `bin/alara-qt` (GUI) or
- `bin/alarad` (headless)
- `bin/alara` (wrapper command)

The `alara` command supports subcommands like `alara gui`, `alara node`, and `alara rpc` exposing different functionality. Subcommands can be listed with `alara help`.

### Windows

Unpack the files into a directory, and then run alara-qt.exe.

### macOS

Drag Alara Core to your applications folder, and then run Alara Core.

### Need Help?

* See the documentation at the Alara Wiki for help and more information.
* Ask for help on Alara community channels.

Building
---------------------
The following are developer notes on how to build Alara Core on your native platform. They are not complete guides, but include notes on the necessary libraries, compile flags, etc.

- [Dependencies](dependencies.md)
- [macOS Build Notes](build-osx.md)
- [Unix Build Notes](build-unix.md)
- [Windows Build Notes](build-windows-msvc.md)
- [FreeBSD Build Notes](build-freebsd.md)
- [OpenBSD Build Notes](build-openbsd.md)
- [NetBSD Build Notes](build-netbsd.md)

Development
---------------------
The Alara repo's [root README](/README.md) contains relevant information on the development process and automated testing.

- [Developer Notes](developer-notes.md)
- [Productivity Notes](productivity.md)
- [Release Process](release-process.md)
- [Translation Process](translation_process.md)
- [Translation Strings Policy](translation_strings_policy.md)
- [JSON-RPC Interface](JSON-RPC-interface.md)
- [Unauthenticated REST Interface](REST-interface.md)
- [BIPS](bips.md)
- [Dnsseed Policy](dnsseed-policy.md)
- [Benchmarking](benchmarking.md)
- [Internal Design Docs](design/)

### Resources
* Discuss on the Alara community forums.

### Miscellaneous
- [Assets Attribution](assets-attribution.md)
- [alara.conf Configuration File](alara-conf.md)
- [CJDNS Support](cjdns.md)
- [Files](files.md)
- [Fuzz-testing](fuzzing.md)
- [I2P Support](i2p.md)
- [Init Scripts (systemd/upstart/openrc)](init.md)
- [Managing Wallets](managing-wallets.md)
- [Multisig Tutorial](multisig-tutorial.md)
- [Offline Signing Tutorial](offline-signing-tutorial.md)
- [P2P bad ports definition and list](p2p-bad-ports.md)
- [PSBT support](psbt.md)
- [Reduce Memory](reduce-memory.md)
- [Reduce Traffic](reduce-traffic.md)
- [Tor Support](tor.md)
- [Transaction Relay Policy](policy/README.md)
- [ZMQ](zmq.md)

License
---------------------
Distributed under the [MIT software license](/COPYING).

## Alara Specific Features

- **Fixed Supply**: 21,000,000 ALA (no minting/printing beyond this cap)
- **5% Transaction Fee**: Every transaction includes a mandatory 5% fee
- **Proof-of-Work**: SHA-256 mining, Bitcoin 2009 style
- **Fully Decentralized**: No admin controls, no central authority
