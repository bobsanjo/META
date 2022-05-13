---
permalink: /docs/guides/build_result_caching/
title: "Using prebuilts to save time"
---

There are two methods that MetaBuild plans to help with build result caching.
1. ccache
2. automatic upload and download of prebuild components based on target hashes computed via build environment (compiler flags, compiler version, etc.)

## ccache

MetaBuild has ccache integration. To enable ccache, pass the `ccache.enabled = true` config to MetaBuild.
MetaBuild ccache integration has been tested for `linux` and `macos` hosts. Recently (early 2022) ccache 4.6.0 added support for msvs and we plan to add support for that to MetaBuild.

See [ccache.meta.py](https://git.corp.adobe.com/meta-specs/ccache/blob/main/ccache.meta.py) for the implementation.

There is a bug with the ccache integration that boolean flags of ccache cannot be set to false correctly ([METAB-730](https://jira.corp.adobe.com/browse/METAB-730)).

## Sharing prebuilt components

Automatic sharing of prebuilt components is in MetaBuild's backlog, though we do have a proof of concept [METAB-11](https://jira.corp.adobe.com/browse/METAB-11).

However, do not despair. It is still possible to build prebuilt binaries and share them with your teammates. The process is just a little less automatic.

Imagine that you are project `R`, and depend on `usd` which have MetaBuild specs. You wish to be able to optional use prebuilt binaries for `usd`.

### Using artifacts built in external env (e.g. CI of dependency itself)

If you wish to download something uploaded by `usd` and don't want to build them in your environment, then your initial work is less. But you risk not building in save env and are not able to regenerate artifacts whenever you want independent of external forces. See [sharing_built_dependencies/build_externally](https://git.corp.adobe.com/meta-samples/sharing_built_dependencies/tree/master/build_externally).

### Building and using artifacts in your own build env

It is strongly recommended not to directly download what `usd` build in their own build environments. Instead MetaBuild allows you to build them in your own build environments and upload them to artifactry. You can then switch between build from source and consuming artifacts via MetaBuild options. See how this can be done in in the [sharing_built_dependencies/build_in_my_env](https://git.corp.adobe.com/meta-samples/sharing_built_dependencies/tree/master/build_in_my_env) sample. This example allows the final app to build and upload deps. This is nice since you can upload artifacts on demand and build them exactly with your own env (c++ version, compiler flags, iterator_debug_level, etc).


