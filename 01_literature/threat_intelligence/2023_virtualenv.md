[[ PAGE 1 ]]

# Virtualenv

Everyone who is using Kali Linux, also uses a lot of Python tools. If you have recently installed or updated something in the last few days you might have received an error like:

```bash
error: externally-managed-environment
...
```

I received similar and now I will explain you how to fix it.

![virtualenv](virtualenv.png)

Before we start fixing anything a bit of theory. And since someone already wrote a good theory, I’ll throw in a bunch of quotes.

What is virtualenv?

> [virtualenv](https://virtualenv.pypa.io/en/latest/) is a tool to create isolated Python environments. virtualenv creates a folder which contains all the necessary executables to use the packages that a Python project would need.
> 
> –[source](https://docs.python-guide.org/dev/virtualenvs/)

What about error itself?

> As the message you’re getting explains, ***this is actually not an issue with Python itself***, but rather your Linux distribution (Kali, Debian, etc.) implementing a deliberate policy to ensure you don’t break your operating system and system packages by using `pip` (or Poetry, Hatch, PDM or another non-OS package manager) outside the protection of a [virtual environment](https://docs.python.org/3/library/venv.html).
> 
> This has been a long-standing recommendation from both the Python team and Linux distros, due to the severe problems that frequently occur for people as a result of using `pip` or other package managers directly with your system Python.
> 
> –[source](https://github.com/python/cpython/issues/102134)

And if you want to go deeper you can check [PEP 668 – Marking Python base environments as “externally managed”](https://peps.python.org/pep-0668/)

What error suggest to do?

> Like the error message says, you have a few options:
> 
> - To **install dependencies required by your/others’ Python code**, [create and activate a virtual environment](https://packaging.python.org/en/latest/tutorials/installing-packages/#creating-virtual-environments) for your project, and then use pip (or another non-system package manager, like Poetry, Hatch or PDM) to install the packages you need.
> - For **command-line applications and tools you want to be available system-wide**, install and run them with a tool like [pipx](https://pypa.github.io/pipx/).
> - To **install and manage your own version of Python** separate from the one bundled with your operating system, try a tool like [Pyenv](https://github.com/pyenv/pyenv).
> - If **the packages provided by your distribution meet your needs**, install the software you want with your system package manager (`apt`, `dnf`/`yum`, `pacman`, etc) instead. See your distro’s documentation for more information.
> 
> –[source](https://github.com/python/cpython/issues/102134)

## Fix

In simple words, and step by step instruction, here is what you can do.

In my other article about [useful Linux commands](https://0ut3r.space/2021/10/30/useful-linux-commands/) I described [GitHub-Repo-Updater](https://github.com/earwig/git-repo-updater) tool which is helpful, to keep up to date all GitHub repos you ever pulled. So I will describe this tool as example of fixing issue.

So, simply try to install something using pip in Kali (or any Debian based distro).

```bash
pip install gitup
```

you will get error:

```bash
error: externally-managed-environment

× This environment is externally managed
╰─> To install Python packages system-wide, try apt install
    python3-xyz, where xyz is the package you are trying to
    install.
    
    If you wish to install a non-Debian-packaged Python package,
    create a virtual environment using python3 -m venv path/to/venv.
    Then use path/to/venv/bin/python and path/to/venv/bin/pip. Make
    sure you have python3-full installed.
    
    If you wish to install a non-Debian packaged Python application,
    it may be easiest to use pipx install xyz, which will manage a
    virtual environment for you. Make sure you have pipx installed.
    
    See /usr/share/doc/python3.11/README.venv for more information.

note: If you believe this is a mistake, please contact your Python installation or OS distribution provider. You can override this, at the risk of breaking your Python installation or OS, by passing --break-system-packages.
hint: See PEP 668 for the detailed specification.
```

Install virtualenv:

```bash
sudo pip3 install virtualenv 
```

Create virtual environment:

```bash
virtualenv venv
```

I called mine `venv`. You can set up as many virtual environment as you want, or create one for all tools and call it for example `venv` or whatever you want.

if you use `ls` command you will see new folder `venv` is created and with the whole structure inside prepared.

If you checked links I provided above, in theory part, you know, you can set up specific Python interpreter for virtual environment:

```bash
virtualenv -p /usr/bin/python2.7 test-venv
```

Activate your virtual environment:

```bash
source venv/bin/activate
```

Once activated, you are inside virtual environment, and you can now install whatever you want using pip, and use it without any error.

To deactivate simply type:

```bash
deactivate
```

Other option to create virtual environment is using Python3:

```bash
virtualenv -p python3 myenv
```

Instead of using virtualenv you can use this command in Python3

```plaintext
python3 -m venv myenv
```

These simple steps allows you to use virtual environments.

Maybe not the greatest article, but solved my issues. I hope it will be helpful for you too.
