---
id: ckb-570f23a5149b
title: GNU nano
category: foundations-and-systems
format: guide
language: en
tags: [bash, linux]
summary: This guide provides instructions for installing the GNU nano text editor from source and includes a comprehensive reference of its keyboard shortcuts.
authors: [unknown]
license: NOASSERTION
added: 2026-10-04
classification:
  method: llm
  model: gemini-3.1-flash-lite
  confidence: 1.0
classified_by: google:gemini-3.1-flash-lite@2026-10-08T00:15:21Z
---

# GNU nano

GNU [nano](https://www.nano-editor.org/) is a small and friendly text editor. Besides basic text editing, nano offers many extra features like an interactive search and replace, go to line and column number, auto-indentation, feature toggles, internationalization support, and filename tab completion. This is my favorite console text editor.

![Gnu Nano Editor](gnunano.jpg)

Here are some tips on how to install the latest version and how to use this editor.

## Latest version

In most of the distribution [nano](https://www.nano-editor.org/) is in a fairly old version, it is functional and works correctly but if you wanted to use the latest version I recommend downloading and installing from the official site the latest version.

### Download

Get latest version of source code from [official website](https://www.nano-editor.org/download.php).

At the moment of writing this article it is 4.6

```bash
wget https://www.nano-editor.org/dist/v4/nano-4.6.tar.xz
```

and extract it:

```bash
tar xf nano-4.6.tar.xz
```

### Install dependencies

```bash
sudo apt install libncursesw5-dev
```

### Configure & make

```bash
./configure --prefix=/usr --sysconfdir=/etc --enable-utf8 --docdir=/usr/share/doc/nano-4.6 && make
```

### Install

```bash
make install && install -v -m644 doc/{nano.html,sample.nanorc} /usr/share/doc/nano-4.6
```

### Configuration

Example configuration (create as a system-wide `/etc/nanorc` or a personal `~/.nanorc` file)

```bash
set autoindent
set historylog
set locking
set nowrap
set quickblank 
set regexp
set smooth
set suspend
set mouse
set speller "path to ispell or aspell"
```

All option are described at [nanorc](https://www.nano-editor.org/dist/v2.1/nanorc.5.html) configuration website.

## Shortcuts

**File handling**
Ctrl+S - Save current file
Ctrl+O - Offer to write file (“Save as”)
Ctrl+R - Insert a file into current one
Ctrl+X - Close buffer, exit from nano

**Editing**
Ctrl+K - Cut current line into cutbuffer
Alt+6 - Copy current line into cutbuffer
Ctrl+U - Paste contents of cutbuffer
Alt+T - Cut until end of buffer
Ctrl+] - Complete current word
Alt+3 - Comment/uncomment line/region
Alt+U - Undo last action
Alt+E - Redo last undone action

**Search and replace**
Ctrl+Q - Start backward search
Ctrl+W - Start forward search
Alt+Q - Find next occurrence backward
Alt+W - Find next occurrence forward
Alt+R - Start a replacing session

**Deletion**
Ctrl+H -Delete character before cursor
Ctrl+D - Delete character under cursor
Ctrl+Shift+Del - Delete word to the left
Ctrl+Del - Delete word to the right
Alt+Del - Delete current line

**Operations**
Ctrl+T - Run a spell check
Ctrl+J - Justify paragraph or region
Alt+J - Justify entire buffer
Alt+B - Run a syntax check
Alt+F - Run a formatter/fixer/arranger
Alt+: - Start/stop recording of macro
Alt+; - Replay macro

**Moving around**
Ctrl+B - One character backward
Ctrl+F - One character forward
Ctrl+⯇ - One word backward
Ctrl+⯈ - One word forward
Ctrl+A - To start of line
Ctrl+E - To end of line
Ctrl+P - One line up
Ctrl+N - One line down
Ctrl+⯅ - To previous block
Ctrl+⯆ - To next block
Ctrl+Y - One page up (pgup)
Ctrl+V - One page down (pgdn)
Alt+\ - To top of buffer
Alt+/ - To end of buffer

**Special movement**
Alt+G - Go to specified line
Alt+] - Go to complementary bracket
Alt+⯅ - Scroll viewport up
Alt+⯆ - Scroll viewport down
Alt+< - Switch to preceding buffer
Alt+> - Switch to succeeding buffer

**Information**
Ctrl+C - Report cursor position
Alt+D - Report word/line/char count
Ctrl+G - Display help text

**Various**
Alt+A - Turn the mark on/off
Tab - Indent marked region
Shift+Tab - Unindent marked region
Alt+N - Turn line numbers on/off
Alt+P - Turn visible whitespace on/off
Alt+V - Enter next keystroke verbatim
Ctrl+L - Refresh the screen
Ctrl+Z - Suspend nanos
