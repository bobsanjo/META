---
permalink: /docs/cli/metabuild_http/
title: "metabuild http"
---

Upload or download an http file.

Usage:

Download a remote file
```
metabuild http download <remote link> [--dest <local path>]
```
If `--dest` is supplied, after downloading the file to the MetaBuild cache, it will also be copied to the destination.

Upload a file (to artifactory for example)
```
metabuild http upload <local path> <remote link>
```