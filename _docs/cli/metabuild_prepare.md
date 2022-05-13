---
permalink: /docs/cli/metabuild_prepare/
title: "metabuild prepare"
---

Prepare Xcode, MSVS or CMake projects.

Usage:

```terminal
metabuild prepare
    [--meta PROJECT]
    [--out-dir OUT_DIR]
    [--target TARGET_REF]
    [--flavor FLAVORS]
    [--define DEFINES]
    [--platform {win32,uwp,ios,macos,android,linux,wasm}]
    [--generator {xcode,msvs,cmake}]
    [--overwrite]
```

| Argument | Description |
|----------|-------------|
| `--meta <PROJECT>`, `-m` | Path to the root META.py file. |
| `--out-dir` | Directory used to output the generated projects. Default: `[root_project]/dist/` |
| `--target <`[`target_ref`]({{ site.baseurl }}{% link _docs/guides/target_refs.md %})`>`, `-t` | Specify the root target to build. |
| `--platform {win32,uwp,ios,macos,android,linux,wasm}`, `-p` | Specify the target platform. Defaults to ``win32`` on Windows, ``macos`` on MacOS and ``linux`` on Linux. |
| `--flavor FLAVORS`, `-f` | Specify the flavor of the builds. For example, for UXP ``--flavor V8`` will build the V8 version of the target. |
| `--define DEFINES`, `-d` | Defines a global variable used by the build. Use this to override any of the settings set via the [`metabuild config`]({{ site.baseurl }}{% link _docs/cli/metabuild_config.md %}) command. |
| `--generator {xcode,msvs,cmake}`, `-g` | The generator type to use for the build. |
| `--overwrite` | If you have made any changes to the repositories that MetaBuild checks out (e.g, via git), or changed their HEAD to a sha1 or branch other than what MB is tracking, MetaBuild by default will not overwrite your changes to track its reference commits. This is a security measure so that you don't lose any local changes. To force MetaBuild to ignore local changes and set checkouts to point to their reference commits, use this option. Same effect can be achieved by setting the config `cache.overwrite_local_changes=true`.|

## Generator types

| Type | Description |
|----------|-------------|
| `msvs` | Generates a Microsoft Visual Studio solution. |
| `xcode` | Generates a Xcode project. |
| `cmake` | Generates a cmake based project. |

The default generator depends on the target `platform`:

| Platform | Generator |
|----------|-----------|
| win32    |   msvs    |
| uwp      |   msvs    |
| ios      |   xcode   |
| macos    |   xcode   |
| android  |   cmake   |
| linux    |   cmake   |
| wasm     |   cmake   |
