---
title: Welcoming Acrylamid
date: 23.01.2013, 22:36
author_image: iromli.jpeg
---

## A Short Story: An Introduction

Recently, i switched to [Acrylamid](http://posativ.org/acrylamid/) as my website generator.
So, what is Acrylamid anyway? Quoted from its GitHub project page:

> Acrylamid is a mixture of nanoc, Pyblosxom and Pelican licensed under BSD Style, 2 clauses.

Except [Pyblosxom](http://pyblosxom.bluesock.org/), i've tried [nanoc](http://nanoc.stoneship.org/) and [Pelican](http://getpelican.com/).
Both are cool projects, but in the end i chose nanoc over Pelican. Despite of being a Ruby-based, nanoc gave me all i want -- the flexibility.
Then the problem came up. Whenever i need to customize the library, i cringed for knowing that my Ruby knowledge is horrible.

During my journey to find a nanoc-like Python-based static website generator, i rant about it on Twitter.
Surprisingly, the core developer of nanoc gave his reaction.

![me and dennis having a talk](/img/2013/01/nanoc-convo.png){: class="thumbnail"}

As you could see, i was using [Mynth](https://github.com/Anomareh/mynt) before i found Acrylamid. Anyway, here's my reaction after reading Acrylamid's `README.rst`:

![first impression](/img/2013/01/i-found-acrylamid.png){: class="thumbnail"}

Well, that's true. Acrylamid is promising. Moreover, it's built on top of Python, i feel confident to use it whatever i want. I also made [my first contribution](https://github.com/posativ/acrylamid/pull/97) recently.

## Another Story: The Gotchas

> There is always first time for everything.

I use LESS alot, so i gave a try on how to integrate LESS and Acrylamid.
Fortunately, Acrylamid does have `LESS` static filter.
But the thing is, i have 2 LESS files, `a.less` and `b.less` under `theme/less` directory.

    #!css
    /* === a.less === */
    @size: 10px;
    .floatleft {
        float: left;
        margin: @size 0;
    }

    /* === b.less === */
    @size: 10px;
    .floatright {
        float: right;
        margin: @size 0;
    }

It was working fine when i invoked `acrylamid autocompile`, but things were going insane when i was trying to re-use variable.

    #!css
    /* === a.less === */
    @import "b";
    @size: 10px;
    .floatleft {
        float: left;
        margin: @size 0;
    }

    /* === b.less === */
    .floatright {
        float: right;
        margin: @size 0;
    }

Yeah, LESS was angry!
This happened because Acrylamid parses each file in separate process.
That's why when `b.less` is parsed, the `lessc` executable will complain about missing `@size` variable.

I was scratching my head then, until i found [an example](https://github.com/markvl/www.vlent.nl).
It uses SASS, but the concept of compiling the assets is similar to my case.
So i just moved all `.less` files out from `theme` to `less` directory.
Afterwards, since LESS doesn't have a watcher, i use [Watchdog](https://github.com/gorakhargosh/watchdog) to monitor the changes.

    #!sh
    watchmedo shell-command \
        --patterns="*.less" \
        --recursive \
        --command="lessc -x $PWD/less/a.less > $PWD/theme/css/b.css" \
        $PWD

Each time any `.less` is modified, `watchmedo` invokes `lessc` and compiles the file into CSS.
Acrylamid will recognize the changes there.
Voila, everything is worked as i expected.

## The Conclusion

Acrylamid is cool and flexible enough. I don't have more words to say, just Try It and See.
