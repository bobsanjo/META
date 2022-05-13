---
permalink: /docs/guides/dlls/
title: "Dynamic Loaded Libraries"
---

This section describes linking dependencies that are built with MetaBuild themselves (have MetaBuild specs) and are added as `deps` / `exported_deps` to the target. For linking libraries that are prebuilt outside of the MetaBuild environment see the section [Linking Binaries]({{ site.baseurl }}{% link _docs/guides/linking_binaries.md %}).

Any `cxx_library` target can be compiled as a DLL by changing the value of the `preferred_linkage` property. By default all targets are linked as `static`, unless the target requests using a shared library using `preferred_linkage = "shared"` or `preferred_linkage = "delay_load_shared"`.
The `delay_load_shared` linkage option (weak linking) is only supported for the `msvs` generator on `win32` platform, and the `xcode` generator for frameworks (when `xcode_product_type = framework`). When a binary is ran, it will not immediately look for shared libs linked in this manner. So if the dylib is missing, but not used in the executable, it will still work. Internally, delay loading is implemented by clang and msvs via [`dlopen()`](https://stackoverflow.com/a/23404579). Linux does not offer this high level delay loading technique.

When a target is linked with the `delay_load_shared` linkage it is added as `Link.DelayLoadDLLs` (`https://docs.microsoft.com/en-us/cpp/build/reference/delayload-delay-load-import?view=msvc-170`) of the final executable on windows. When used with xcode the framework is marked as optional (`https://developer.apple.com/library/archive/documentation/MacOSX/Conceptual/BPFrameworks/Concepts/WeakLinking.html`).

## Overriding the linkage using options

MetaBuild allows customization of the build targets via a number of mechanisms: META.lock, local configuration or CLI defines.

Any property in the specifications can be changed dynamically based on these options using the `option()` node type.

```python
option(
    name = "mylib_linkage",
    choices = [
        "static",
        "shared",
        "delay_load_shared",
    ],

    # This is the option that embedders can change to customize this library.
    config = "mylib.linkage",

    # A default value is needed for cases when the host doesn't want to change the type.
    default_value = [
        # Any value in MB can be customized per platform using `target` filters.
        (target.macos, "shared"),
        (target.wasm, "static"),
        (target.win32, "delay_load_shared"),
        (~(target.wasm | target.macos | target.win32), "static")
    ]
)

# Use a variable to not repeat ourselves.
is_shared = target.option(":mylib_linkage", "shared") | target.option(":mylib_linkage", "delay_load_shared")

cxx_library(
    name = "mylib",

    # Just use the option value directly.
    preferred_linkage = "$(option :mylib_linkage)",

    preprocessor_macro = [
        # Add a macro that can be used to distinguish in C++ between DLL or static.
        (is_shared, "MYLIB_DLL=1"),
    ],

    xcode_product_type = [
        # On ios we may want to make it a framework instead.
        (target.ios & is_shared, "framework")
    ],
)
```

The option can be changed in the `root` project using the META.lock or via the command line using the `--define` argument:

### META.lock

```
[mylib]
linkage = shared
```

### CLI defines:

```shell
> metabuild prepare --define mylib.linkage=shared
```

### Using static lib to build the shared lib

In some cases, you may want to actually use the static lib to build the shared lib to save build time. In this case you should still use the option method.
```python
cxx_library("acpl_static", preferred_linkage = "static")
cxx_library("acpl_shared", preferred_linkage = "shared", deps = [":acpl_static"])
group(name = "acpl", deps = [
    (target.option("//options:acpl_linkage", "shared"), ":acpl_shared"), 
    (target.option("//options:acpl_linkage", "static"), ":acpl_static"), 
]
```
Then mid level libs that depend on acpl, must use the `acpl//:acpl` target instead of `acpl//:acpl_shared` or `acpl//:acpl_static`.
This way the final app can set `[acpl]linkage=` in their lock file and that will enforce whether the static or shared variant is used uniformly through the build. However, if a mid level lib hardcodes whether to use `acpl//:acpl_shared` or `acpl//:acpl_static` then the final app cannot override that.

## Exporting APIs

The `target.option` can be used across different nodes. This is usually needed when multiple `static` libs are used to generate a single DLL.

For example, we may have a case where `mylib_module_a` and `mylib_module_b` export APIs that are bundled inside `mylib_dll`.

```python
# Save the target.option as a variable to make it easier to read below.
MYLIB_DLL = target.option(":mylib_linkage", "shared")

cxx_library(
    name = "mylib_export_headers",
    public_include_directories = [
        "./internal_headers"
    ],
    exported_preprocessor_macros = [
        (MYLIB_DLL, "INSIDE_MYLIB_DLL=1")
    ],
    srcs = [
        "./internal_headers/Mylib_Export.h"
    ]
)

cxx_library(
    name = "mylib_module_a",
    public_include_directories = [
        "./mylib__module_a/public",
    ],
    srcs = [
        "./mylib__module_a/public/MyLibModuleA.h",
        "./mylib__module_a/src/MyLibModuleA.cpp"
    ],
    deps = [
        ":mylib_export_headers"
    ]
)

cxx_library(
    name = "mylib_module_b",
    public_include_directories = [
        "./mylib_module_b/public",
    ],
    srcs = [
        "./mylib__module_b/public/MyLibModuleB.h",
        "./mylib__module_b/src/MyLibModuleB.cpp"
    ],
    deps = [
        ":mylib_export_headers"
    ]
)

cxx_library(
    name = "mylib",
    preferred_linkage = "$(option :mylib_linkage)",
    srcs = [
        (MYLIB_DLL, "mylib_dll_main.cpp"),
    ],
    deps = [
        # Note that `deps` are not re-exported to the dependents.

        # We have to add `:mylib_export_headers`
        # again even though A and B had them.

        ":mylib_export_headers",
    ],
    exported_deps = [
        # Using `exported_deps` to make users of `mylib`
        # inherit the public headers from A and B above.

        ":mylib_module_a",
        ":mylib_module_b"
    ]
)
```


## Library load paths

By default MetaBuild injects the following search paths that allow binaries and shared libs to find and load their dependency shared libraries:

- On macos, we set `@rpath` to `@executable_path`, `@loader_path`, `@executable_path/../Frameworks`, `@loader_path/../Frameworks`: First two are for cli apps or dlls. The last two for packaged apps and frameworks. executable_path is for executables (executable looking for executable dependency) and loader_path is for shared libraries (shared library looking for shared library dependency). Also, we set the id of each shared lib to `@rpath/...`.
- On ios, we set `@rpath` to `@executable_path`, `@loader_path`, `@executable_path/Frameworks`, `@loader_path/Frameworks`: Rational is same as macos. Just that packages on ios look differently. There is no Contents folder so no need for `..`. Same treatment is done for id of each shared lib.
- On linux we set `@rpath` to `$ORIGIN`.  Same treatment is done for id of each shared lib.
- We don't support shared libs on wasm.
- On android there is no dll loading relative to binary or rpath. Everything should be under LD_RUNTIME_PATH env var.
- On windows, there is no rpath. Everything should be next to executable (unless delay loading is used).

For more information regarding how they are used see:
https://gitlab.kitware.com/cmake/community/-/wikis/doc/cmake/RPATH-handling

To acheive the same behaviour between `cmake`, `msvs` and `xcode` on cmake we use `BUILD_WITH_INSTALL_PATH=true` with cmake (except wasm and android). However, you can disable it with
```
[cmake]
build_with_install_rpath = false # all platforms
build_with_install_rpath_linux = false # one platforms
```
