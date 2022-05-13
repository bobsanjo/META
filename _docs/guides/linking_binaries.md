---
permalink: /docs/guides/linking_binaries/
title: "Linking Binaries"
---

The `linker_libraries` and `exported_linker_libraries` properties can be used to inject prebuilt binaries into the build.

> If you wish to only copy a shared library but not explicitly link against it (e.g., it is opened with `dlopen()`), use [resources]({{ site.baseurl }}{% link _docs/guides/resource_spec.md %}).

## Linking with system libraries

Use the [`system_lib`]({{ site.baseurl }}{% link _docs/api/system_lib.md %}) method in order to make `MetaBuild` understand that the library is provided by the operating system SDK.

```python
cxx_library(
    name = "my_lib",
    linker_libraries = [
        (target.apple, [
            system_lib("libiconv.tbd"),
            system_lib("CoreFoundation.framework")
        ]),
        (target.win32, [
            system_lib("Shell32.lib"),
        ]),
    ]
)
```

## Linking with prebuilt libraries

Wrap the library using the [`user_lib`]({{ site.baseurl }}{% link _docs/api/user_lib.md %}) method when symbols or extra DLL file need to be added to the build.

When a shared library is referenced via `linker_libraries`, the prebuilt binary is automatically added to the application bundle. On Windows, make sure to use the `dll` attribute of the `user_lib()` method in order to make MetaBuild automatically copy the DLL to the output folder of the application.

```python
cxx_library(
    name = "my_lib",
    linker_libraries = [
        # MetaBuild will automatically link and embed the binaries.
        (target.apple, [
            "MyFramework.framework",

            # Add a library that uses internal symbols or has no symbols at all.
            "my_lib_with_internal_symbols.dylib",

            # Add a library that uses dwarf symbols.
            user_lib("lib_with_external_symbols.dylib", symbols = "lib_with_external_symbols.dSYM"),
        ]),
        (target.win32, [
            # Add a static lib and its PDB file.
            user_lib("static.lib", symbols = "static.pdb"),

            # Add a shared lib with the DLL and the PDB.
            user_lib("dynamic.lib", dll = "dynamic.dll", symbols = "static.pdb" ),
        ]),
    ]
)
```

## Exporting vs not exporting

The difference between using `linker_libraries` and `exported_linker_libraries` is that

- `exported_linker_libraries`: The prebuilt binaries will not be copied into the current `cxx_library`. They will be copied into the executables that use this `cxx_library`.
- `linker_libraries`: For a `cxx_binary` and a `cxx_library` that can embed the prebuilt binaries (e.g., xcode framework), it will copy these prebuilt binaries into the target. Note that copying prebuilt binaries into xcode frameworks is not recommended, as it will create [Umbrella Frameworks](https://developer.apple.com/library/mac/documentation/MacOSX/Conceptual/BPFrameworks/Concepts/FrameworkAnatomy.html#//apple_ref/doc/uid/20002253-97623-BAJJHAJC) which are not recommended by apple and will complicate the runtime dependency structure. For a `cxx_library` that cannot embed these binaries, this has the same effect as `exported_linker_libraries`.
