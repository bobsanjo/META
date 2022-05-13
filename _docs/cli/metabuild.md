---
permalink: /docs/cli/metabuild/
title: "metabuild"
---

```terminal
usage: metabuild [-h] command ...

Meta Builder command-line tool.

positional arguments:
  command
    config    Configure properties.
    prepare   Prepare projects.
    sync      Sync remote projects.
    build     Build projects.
    run       Run specific rule.
    tool      Run internal `tool` command line bash (based on homebrew or msys).
    nodejs    Run internal `nodejs` command line bash.
    cmake     Run internal `cmake` command line bash.
    nuget     Run internal `nuget` command line bash.
    android   Run internal `android` command line bash.
    ninja     Run internal `ninja` command line bash.
    pm        Run package manager commands.
    import    Automatically convert existing projects into MetaProjects.
    scm       Work with multiple SCM repos.
    graph     Generate the dependency graph.
    http      Http requests.
    codex     Codex requests.
    bin_cache
              Run internal cache commands.
    emsdk     Run internal `emsdk` command line bash.
    version   Prints the metabuild version.

optional arguments:
  -h, --help  show this help message and exit
```

## Generic arguments

```terminal
optional arguments:
  -h, --help            show this help message and exit
  -v, --verbose         Enable verbose logging.
  --no-live-status      Disable live status update.
  --profile PROFILE     Enable profiling.
  --raise               Avoids catching the errors for easier debugging.
  -d DEFINES, --define DEFINES
                        Adds a define used during the build.
  --defines DEFINES_FILES
                        Adds a JSON set of defines.
  --flag FLAGS          Adds a feature flag used during the build.
  --cached              The cache will automatically try to pull latest commits on generic branches for GIT repos. Use this to disable that behavior and always use the latest cached version instead.
  --pm-force-update     The Package Manager GIT repos is only updated when a version is not found. Use this property to force an update even if all versions are already present.
  --overwrite           Overwrite any local changes detected in the repositories checked out by MetaBuild.
  --trace TRACE_FILE    Dumps the tracing profile to this file.
  --log-file LOG_FILE   An optional log file for metabuild to write to.
  -m PROJECT, --meta PROJECT
                        The path to the root meta file.
  --out-dir OUT_DIR     The path to the dist folder.
  -t ROOT_TARGET, --target ROOT_TARGET
                        The main target to process (defaults to the 'mb.root_target' option or ':main').
  --specs-group SPECS_GROUP
                        The build specs group to process (defaults to the 'mb.specs_group' option or ':specs').
  -s BUILD_SPEC, --spec BUILD_SPEC
                        The build spec to process (defaults to the 'mb.build_spec' option).
  -p {win32,uwp,ios,macos,android,linux,wasm}, --platform {win32,uwp,ios,macos,android,linux,wasm}
                        The target platform used to generate the projects.
  -f FLAVORS, --flavor FLAVORS
                        The target flavors that should be enabled.
  -c {Debug,Release,Coverage}, --config {Debug,Release,Coverage}
                        The configuration used to run the target rule. Ignored by the generator rules that generate all configs.
  -a {x86,x64,arm32,arm64,wasm32}, --arch {x86,x64,arm32,arm64,wasm32}
                        The configuration used to run the target rule. Ignored by the generator rules that generate all configs.
  --ios-platform {iphoneos,iphonesimulator}
                        The configuration used to run the target rule. Ignored by the generator rules that generate all configs.
  --android-abi {x86,x86_64,armeabi-v7a,arm64-v8a}
                        The configuration used to run the target rule. Ignored by the generator rules that generate all configs.
  --xcode-archs XCODE_ARCHS
                        The configuration used to run the target rule. Ignored by the generator rules that generate all configs.
  --msvs-platform {Win32,x64,ARM,ARM64}
                        The configuration used to run the target rule. Ignored by the generator rules that generate all configs.
  -g {xcode,msvs,cmake}, --generator {xcode,msvs,cmake}
                        The generator used to generate the projects.
```

See [Command Line Args](metabuild_config.md#command-line-args) section for more info on `--define`. 

## Commands

- [`metabuild config`]({{ site.baseurl }}{% link _docs/cli/metabuild_config.md %})
- [`metabuild prepare`]({{ site.baseurl }}{% link _docs/cli/metabuild_prepare.md %})
- [`metabuild sync`]({{ site.baseurl }}{% link _docs/cli/metabuild_sync.md %})
- [`metabuild build`]({{ site.baseurl }}{% link _docs/cli/metabuild_build.md %})
- [`metabuild run`]({{ site.baseurl }}{% link _docs/cli/metabuild_run.md %})
- [`metabuild tool`]({{ site.baseurl }}{% link _docs/cli/metabuild_tool.md %})
- [`metabuild pm`]({{ site.baseurl }}{% link _docs/cli/metabuild_pm.md %})
- [`metabuild import`]({{ site.baseurl }}{% link _docs/cli/metabuild_import.md %})
- [`metabuild scm`]({{ site.baseurl }}{% link _docs/cli/metabuild_scm.md %})
- [`metabuild graph`]({{ site.baseurl }}{% link _docs/cli/metabuild_graph.md %})
