[[ PAGE 1 ]]

# GPGWrap - simple GUI for GPG

A few years ago I wrote a guide about using GPG from the command line. It explains how OpenPGP works, how keys work, and what is actually happening when you encrypt or sign data: [Easy GPG](../../../../2019/02/13/easy-gpg/index.html)

That part hasn’t changed. GPG is still the same — powerful, flexible, and a bit annoying to use on a daily basis.

This project is not about replacing GPG. It’s about removing friction.

![gpgwrap](gpgwrap.webp)

## Why I built this

GPG CLI is fine if you use it often. But in practice, most people don’t.

You forget flags. You copy commands from old notes. You re-check syntax every time you want to encrypt or sign something.

And for simple operations — encrypting a short message, verifying a signature, exporting a key — it just slows you down.

There are GUI tools already. I was using [Lock](https://github.com/konstantintutsch/Lock) for a while — clean, minimal, well-designed. But it’s written in C and the project is no longer actively developed. It also didn’t cover everything I needed.

Instead of trying to extend someone else’s codebase in a language I don’t work with, I built my own version in Python, focused only on the workflow I actually use.

## What GPGWrap is

GPGWrap is a thin GUI layer on top of system `gpg`. It does not implement cryptography. It does not replace GPG. It does not try to be smart.

It simply builds correct commands, runs them, and shows the result in a readable way.

Under the hood, everything is still handled by:

- `gpg`
- `gpg-agent`
- `pinentry`

So behavior is exactly the same as CLI. Same inputs, same outputs, same trust model.

![gpgwrap screen](screenshot.webp)

## How it is meant to be used

The goal is not to hide GPG, but to make common operations faster.

Instead of remembering flags, you:

- paste text
- pick recipients
- click encrypt

Instead of manually verifying signatures:

- paste message + signature
- click verify

Instead of dealing with key export/import commands:

- just select a key and export it

For repetitive, small tasks, GUI is simply faster.

## Security perspective

Nothing here changes how GPG works. All cryptographic operations are still performed by GPG itself. Keys are still stored in the same keyring. Passphrases are still handled by `pinentry`. GPGWrap does not store keys, does not manage secrets, and does not introduce any new trust model.

From a security standpoint, using this tool is equivalent to running the same commands manually.

If you don’t trust GUI tools, that’s a good instinct. You can verify everything:

- check the commands being executed
- reproduce them in CLI
- audit the code

There is no hidden logic.

Also, if your system is compromised, it doesn’t matter whether you use CLI or GUI. Security depends on your environment and how you handle your private keys, not on the interface.

## Why not just use CLI

You probably should use CLI if:

- you know it well
- you automate things
- you care about full control

But most real-world usage looks different:

- copy/paste encrypted messages
- quick verification
- one-off encryption

That’s where CLI becomes friction. This tool just removes that friction. Nothing more.

## Final thoughts

This is version 1.0. Built for my own workflow, but it might be useful for others who use GPG occasionally and don’t want to fight with flags every time.

If you want to understand how GPG actually works, read the original guide first: [Easy GPG](../../../../2019/02/13/easy-gpg/index.html)

If you just want a simple way to use it: <https://github.com/h0ek/gpgwrap>

There are also other GUI options depending on your workflow. You can use:  
- Lock → <https://github.com/konstantintutsch/Lock>  
- VSCode + GPG plugin → <https://github.com/jvalecillos/vscode-gpg>  
- Geany + GeanyPG → <https://plugins.geany.org/geanypg.html>  
- Kleopatra (Windows / Gpg4win) → <https://gpg4win.org/download.html>  
- Kleopatra (Linux) → <https://apps.kde.org/kleopatra/>

Use whatever fits you best. This is just my take on it.
