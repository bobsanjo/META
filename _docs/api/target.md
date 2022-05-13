---
permalink: /docs/api/target/
title: "target"
toc: true
---

The `target` global object can be used to create MetaBuild `Filter` objects. Any property in the MetaBuild specification can be targeted for a very specific configuration by replacing the value with a Python `tuple` with two values: `(<Filter>, filtered_value)`.

The following example uses `Filters` to add different files on Windows and MacOS.

```python
cxx_binary(
    name = "my_exe",
    srcs = [
        # This file is only included on Windows.
        (target.windows, "main_win.cpp"),

        # This file is only included on MacOS.
        (target.macos, "main_mac.cpp")
    ]
)
```

Python lists can be used to filter multiple files at once:

```python
srcs = [
    (target.windows, [
        "file1_win.cpp",
        "file2_win.cpp",
        "file3_win.cpp"
    ]),
    (target.macos, [
        "file1_mac.cpp",
        "file2_mac.cpp",

        # Use nesting to merge the filters.
        (target.debug, "debug_stuff_mac.cpp")
    ]),
]
```

## Merging filters

All of the primitive filters defined below can be merged via `|` or `&` Python operators.

Examples:

- adding a file for both iOS and Android:
`target.ios | target.android`

- add file only in debug configuration on Android:
`target.android & target.debug`

- add file only in debug configuration on Android and all configurations on iOS:
`(target.android & target.debug) | target.ios`

## Generic Filters

| Filter | Description |
|--------|-------------|
| `target.none` | Filter that doesn't match anything. Very useful when trying to exclude files out of the project. |

## Platform Filters

| Filter | Description |
|--------|-------------|
| `target.linux` | Matches only Linux projects. |
| `target.windows` | Matches only Windows projects. |
| `target.win32` | Matches only Win32 projects on Windows. |
| `target.uwp` | Matches only UWP projects on Windows. |
| `target.win10` | *Deprecated* alias for `target.uwp`. |
| `target.ios` | Matches only iOS projects. |
| `target.macos` | Matches only MacOS projects. |
| `target.apple` | Matches both iOS and MacOS projects. |
| `target.android` | Matches only Android projects. |
| `target.wasm` | Matches all WASM projects. |
| `target.posix` | Matches all projects, except Windows. |
| `target.native_posix` | Matches all projects, except Windows and WASM. |

## Configuration Filters

| Filter | Description |
|--------|-------------|
| `target.debug` | Matches `debug` configurations. |
| `target.coverage` | Matches `coverage` configurations. |
| `target.release` | Matches `release` configurations. |

## Compiler Flags Filters

| Filter | Description |
|--------|-------------|
| `target.lang_c` | Only adds the filtered compiler flag when compiling "C" files. |
| `target.lang_cpp` | Only adds the filtered compiler flag when compiling "C++" files. |

## ObjC helpers

| Filter | Description |
|--------|-------------|
| `target.enable_objc_xplat` | Makes the file use the "ObjC" compiler. |
| `target.no_objc_arc_xplat` | By default MetaBuild enables `ObjC Automatic Ref Counting` on all files. Wrap a source file using this filter to make the compiler disable the `ObjC Automatic Ref Counting` feature. |
| `target.enable_objc` | Same as `target.enable_objc_xplat`, but also removes the file from non-Apple platforms. |
| `target.no_objc_arc` | Same as `target.no_objc_arc_xplat`, but also removes the file from non-Apple platforms. |

## Bytecode Format Filters

| Filter | Description |
|--------|-------------|
| `target.arch_x86` | Matches only the `x86` architecture. |
| `target.arch_x86_64` | Matches only the `x86_64` architecture. |
| `target.arch_x64` | Same as `target.arch_x86_64`. |
| `target.arch_intel` | Matches any `intel` architecture. |
| `target.arch_arm` | Matches any `arm` architecture. |
| `target.arch_arm32` | Matches only the `arm32` architecture. |
| `target.arch_arm64` | Matches only the `arm64` architecture. |
| `target.arch_wasm32` | Matches only the `wasm32` architecture. Only valid with WASM builds. |
| `target.arch_wasm64` | **WASM64 is not yet supported by Emscripten SDK.** Matches only the `wasm64` architecture. Only valid with WASM builds. |

## iOS filters

| Filter | Description |
|--------|-------------|
| `target.ios_simulator` | Matches only the iOS simulator builds. |
| `target.ios_device` | Matches only the iOS device builds. |
| `target.iphone` | Matches only the iPhone/iPad builds. |
| `target.appletv` | Matches only the Apple TV builds. |
| `target.applewatch` | Matches only the Apple Watch builds. |

## Xcode Header Filters

Use these filters to change the visibility of the Xcode Framework header files when adding the files to the `xcode_headers` property.

| Filter | Description |
|--------|-------------|
| `target.xcode_private` | Makes the file a private Xcode header. |
| `target.xcode_public` | Makes the file a public Xcode header. |

### Example

```python
cxx_library(
    name = "MyFramework",
    xcode_product_type = "framework",
    xcode_flags = {
        'PRODUCT_BUNDLE_IDENTIFIER': "com.adobe.my-framework"
    },
    xcode_headers = [
        # Add the header to the Public section.
        (target.xcode_public, "MyFramework.h"),

        # Add the header to the Private section.
        (target.xcode_private, "MyFramework_Private.h"),

        # Add the header to the Project section.
        "MyFramework_Project.h",
    ]
)
```

## Custom flags added to source files

`Filters` can also be used to inject custom properties that only apply to a specific set of files.

| Filter | Description |
|--------|-------------|
| `target.flags(<string>)` | Adds custom compiler flags. Only used by Clang or GCC compilers. |
| `target.xcode_type(<string>)` | Changes the file type used when adding the file to the Xcode project. |
| `target.msvs_flags(<`[`msvs_flags`]({{ site.baseurl }}{% link _docs/guides/msvs_flags.md %})`>)` | Injects custom `Microsoft Visual Studio` flags only on a specific set of files. |
| `target.msvs_type(<string>)` | Changes the file type used when adding the file to the `Microsoft Visual Studio` project. |
| `target.msvs_condition(<string>)` | Changes the `condition` used when adding the file to the `Microsoft Visual Studio` project. |

## Custom flavors

MetaBuild can automatically generate different flavors for a target. Use this filter to only add files when a specific flavor is requested.

For example, when compiling UXP for `JavaScriptCore`, we use `(target.flavor("js", "jsc"), "jsc_file.cpp")` to only include that file when targeting `JavaScriptCore`.

| Filter |
|--------|
| `target.flavor(type : <string>, value : <string>)` |

## Custom options

MetaBuild can filter based on options injected by parent projects.

| Filter |
|--------|
| `target.option(option_node_reference : <target_ref>, expected_value : <string>)` | Checks if the value of the option node is equal to the `expected_value`. |
| `target.option(option_node_reference : <target_ref>)` | Checks if the value of the boolean option is True. |

#### Semver constraints

Options with type versions accept `semver` constraints for the expected value:

|--------|--------|
| Value | Effect |
|--------|--------|
| `@1.0.0`, `~=1.0.0` | Checks only the minor and major to match. |
| `>1.0.0` | Strictly higher than 1.0.0. |
| `<1.0.0` | Strictly smaller than 1.0.0. |
| `>=1.0.0` | Higher or equal to 1.0.0. |
| `<=1.0.0` | Smaller or equal to 1.0.0. |
| `==1.0.0` | Equal to 1.0.0. |
| `!=1.0.0` | Not equal to 1.0.0. |

Multiple constraints can be separated by spaces: `"~=1.0.0 !=1.0.2"`.

## MetaBuild Version


MetaBuild can filter based on its own version.

| Filter |
|--------|
| `target.metabuild(<version_constraints>)` | Checks if version of MetaBuild satisfies the constraints. Will respect any [override via configurations]({{ site.baseurl }}{% link _docs/guides/checking_metabuild_version.md %}). |
