---
title: Introducing Genma
date: 14.07.2013, 00:19
---

## I Need Isolated Workspace

While learning [Go][], i found myself missing Python [virtualenv][].
If you're not familiar with it, just imagine an isolated workspace for your development
(for convenience, we'll call it virtualenv).

Surprisingly, creating this virtualenv is pretty easy in Go.
By reading the [documentation][], you'll know that you only need to
customize Go environment variables.
Let say, if i want to create a workspace located at
`~/workspaces/foobar` and install 3rd party packages,
all i need to do is simply typing following command:

```sh
$ GOPATH=~/workspaces/foobar GOBIN=~/workspaces/foobar/bin go get github.com/user/repo
```

Go will takes care everything, including creating a bunch of directories:

```sh
$ tree ~/workspaces
/home/iromli/workspaces
└── foobar
    ├── bin
    ├── pkg
    └── src
```

Now, the question is when i have lot of virtualenv,
how do i manage them without having to type repetitive commands?
Enter [Genma][].

## Genma The Virtualenv Manager

Genma is heavily inspired by [virtualenvwrapper][].
Hence the main goals are:

* creating and deleting virtualenv should be easy
* switching between virtualenv back and forth should not PITA

At the time i wrote this blog post, [v0.2.0][] has been released.
So let's have a quick tour, shall we?

### Installing Genma

First things first, ensure you have a working Go installation
(i'm using [goenv][] by the way) and Bash.
Afterwards, you need to grab a copy of Genma.
According to its `README.md` file, the preferred setup is to use `git`.

```sh
$ git clone git://github.com/iromli/genma.git ~/.genma
$ cd ~/.genma
$ git tag -l | tail -1 | xargs git checkout
$ source ~/.genma/genma.sh
```

Confirm that the installation process is completed:

```sh
$ genma -h
Go (virtual) ENvironment MAnager v0.2.0

Usage: genma <command> [<args>]

Commands:
  deactivate              Disable active virtualenv.
  lsvirtualenv            List available virtualenv.
  mkvirtualenv <name>     Create and activate new virtualenv.
  rmvirtualenv <name>     Delete existing virtualenv.
  workon <name>           Activate or switch to a virtual environment.

Options:
  -h, --help              Show help and exit.
  -v, --version           Show version and exit
```

If you want `genma` always available in your shell,
simply do `source ~/.genma/genma.sh` elsewhere (e.g. `~/.bashrc`).

### Creating Virtualenv

Assuming that you haven't create any virtualenv using Genma, let's do it now.

```sh
$ genma mkvirtualenv env
```

By default, your new virtualenv will be created under `~/.genma/virtualenv` directory.
This location is called `$GENMA_HOME` and it's defined as environment variable.

```sh
(g:env)$ tree ~/.genma/virtualenv
~/.genma/virtualenv
└── env
    ├── bin
    ├── pkg
    └── src
```

Notice that your shell prompt is prefixed with `(g:env)`.
That's how Genma tells you if you're in any active virtualenv.
The format itself is _(g:any_virtualenv_name)_.
The `g:` part distinguishes Go and Python virtualenv (in case you're a Pythonista too).

### Disabling Virtualenv

Once your virtualenv has been created, you can disable it with `genma
deactivate` command.
Behind the scene, Genma removes shell prompt prefix and
unsets some Go environment variables.

### Activating or Switching to Virtualenv

Assuming _env_ is in dormant state, how do you activate it? That's easy, just
do `genma workon env`. Ofcourse you can always change the virtualenv name.

### Deleting Virtualenv

So you want to remove unnecessary _env_? `genma rmvirtualenv env` will do the
dirty job for you. However you can't remove currently-active virtualenv though.

### Listing All Virtualenv

The `genma lsvirtualenv` likely useful if you have lots of virtualenv.

See illustration below:

```sh
(g:env)$ tree ~/.genma/virtualenv
~/.genma/virtualenv
└── env
    ├── bin
    ├── pkg
    └── src
└── env2
    ├── bin
    ├── pkg
    └── src
```

Given the hierarchy, the following command will return a list of virtualenv names:

```sh
$ genma lsvirtualenv
env
env2
```

That's it, you got the basic of Genma commands.

Genma and You
-------------

Genma might be overkill for your daily workflow.
But as the author of Genma, i find it useful especially when i have lots of
workspaces. I hope it helps you too.

[Go]: http://golang.org/
[virtualenv]: http://www.virtualenv.org/
[documentation]: http://golang.org/doc/code.html#Organization
[Genma]: https://github.com/iromli/genma
[virtualenvwrapper]: https://bitbucket.org/dhellmann/virtualenvwrapper
[v0.2.0]: https://github.com/iromli/genma/releases/tag/0.2.0
[goenv]: https://github.com/wfarr/goenv
