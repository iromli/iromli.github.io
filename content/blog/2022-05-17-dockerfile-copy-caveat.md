+++
title = "Dockerfile COPY Caveat"
template = "post.html"

[taxonomies]
tags = ["docker"]
+++

Recently I worked on a project where I need to enhance an Docker image for the app.
The scope of the enhancements are:

1. Generate static files from app manifests using `npm`.
1. Copy static files (and exclude everything else) from previous step
1. Use [multi-stage builds](https://docs.docker.com/develop/develop-images/multistage-build/) to reduce unwanted layers.

The enhancements are pretty much simple to implement. But in the end, I encountered issue with the end-result image,
which I will explain in the next sections.

## Stage 1: Build static files

First things first, the image needs to build static files by running an `npm` command.

```dockerfile
FROM node:14.19.1-alpine3.15 AS builder
WORKDIR /app
# build static files
RUN npm run build
```

The command produces static files under `/app/dist` directory as seen below.

```plaintext
/app/dist/
├── app.bundle.js
├── fonts
│   └── nerd.ttf
├── index.html
└── static
    └── main.css
```

## Stage 2: Copy static files

Given the required static files are available in `builder` stage, the `runner` stage only need to copy from it.

```dockerfile
FROM alpine:3.15.4 AS runner
# copy static files
COPY --from=builder /app/dist/* /var/lib/nginx/html/
```

In this case, I thought that the `COPY` instruction will copy the contents of `/app/dist` directory recursively as-is.

This is the expected paths after `COPY` instruction.

```plaintext
/var/lib/nginx/html/
├── app.bundle.js
├── fonts
│   └── nerd.ttf
├── index.html
└── static
    └── main.css
```

Unfortunately, there is weird behavior where sub-directories contents are extracted out.

```plaintext
/var/lib/nginx/html/
├── app.bundle.js
├── index.html
├── main.css
└── nerd.ttf
```

As you can see, files structures aren't copied as-is. The `COPY` instruction doesn't work like `cp -R /src/* /dest/` command in unix shell.

## Re-thinking the instruction

Luckily, a simple modification on the `COPY` instruction solved the issue.

So, instead of

```dockerfile
COPY --from=builder /app/dist/* /var/lib/nginx/html/
```

do

```dockerfile
COPY --from=builder /app/dist/ /var/lib/nginx/html/
```

The structures are preserved correctly.

```plaintext
/var/lib/nginx/html/
├── app.bundle.js
├── fonts
│   └── nerd.ttf
├── index.html
└── static
    └── main.css
```

## Moral of the story

* Don't expect the `COPY` instruction always do the same thing as `cp` command.
* Double-check the end-result.

**NOTE:** Perhaps this is the Docker build design or perhaps I misunderstood how to use `COPY` correctly.
