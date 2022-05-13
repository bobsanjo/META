---
permalink: /docs/cli/metabuild_build/
title: "metabuild build"
---

Invokes the build of a specific target. By default builds starting from the root node in the build graph.

Use the `--build-target` argument to change the required target.

Note that `metabuild prepare` must be invoked ahead of time. The prepare creates a JSON file on disk that is used during the `build`. Note that changing any defines during the `build` call might not impact the actual build. All the defines used with the `prepare` call are preserved and re-applied during the `build`, so you don't have to repeat them again when running build.

By default `metabuild build` builds `Debug`. You can use one or more `--config` arguments to compile different / multiple configurations at once.

```
  --build-target BUILD_TARGET
                        The target to build. Defaults to the root target.
  --max-cpus MAX_CPUS   The maximum number of concurrent processes to build with.
```

## Passing arguments to build

Sometimes you may need to add extra arguments for the `xcodebuild`, `msbuild` or `cmake build` commands that are used internally by the `metabuild build` command.

All the arguments after `--` are carried over to the underlying build command.

For example, this passes `-allowProvisioningUpdates` to xcodebuild:

```shell
> metabuild build -- -allowProvisioningUpdates
```

## Universal Builds

By default Xcode projects build only the current architecture of the system when building for Debug. This is an optimization to improve the time spent building in the build/run/repeat cycle.

However, this optimization is not useful when the actual Universal binaries are needed. You can workaround this issue by using the `xcode.only_active_arch_debug` option in your CI/CD builds.

```shell
> metabuild prepare -—define xcode.only_active_arch_debug=false
> metabuild build
```
