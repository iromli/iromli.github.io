+++
title = "Dockerfile COPY Caveat"
template = "post.html"

[taxonomies]
tags = ["docker"]
+++

Imagine when you have snippet like this:

```dockerfile
FROM node:14.19.1-alpine3.15 AS builder
WORKDIR /app
RUN npm run build
```

That produces static files as seen below:

```plaintext
/app/dist/
├── app.bundle.js
├── fonts
│   └── nerd.ttf
├── index.html
└── static
    └── main.css
```

And then you want to copy the files into new stage:

```dockerfile
FROM alpine:3.15.4 AS runner
COPY --from=builder /app/dist/* /var/lib/nginx/html/
```

But you get a different file structures:

```plaintext
/var/lib/nginx/html/
├── app.bundle.js
├── index.html
├── main.css
└── nerd.ttf
```

You may assume (at least I did) there's something wrong with the build command. The `COPY` instruction doesn't work like `cp -R /src/* /dest/` command does in unix shell.

**But why??**

## Workaround

Luckily, a simple modification on the `COPY` instruction solved the issue.

So, instead of

```dockerfile
COPY --from=builder /app/dist/* /var/lib/nginx/html/
```

do

```dockerfile
COPY --from=builder /app/dist/ /var/lib/nginx/html/
```

The structures are preserved correctly then.

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

* Don't expect the `COPY` instruction always do the same thing as `cp` command does.
