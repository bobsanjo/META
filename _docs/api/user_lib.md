---
permalink: /docs/api/user_lib/
title: "user_lib()"
---

```python
user_lib(lib, dll = None, symbols = None, delay_load = False)
```

Use `user_lib()` to point to a prebuilt binary and its symbols.

| Attribute | Type | Description |
|-----------|------|-------------|
| `lib` | [`file_ref`]({{ site.baseurl }}{% link _docs/guides/file_refs.md %}) | Path to `.lib` file for windows. Linkable static library for unix. |
| `dll` | [`file_ref`]({{ site.baseurl }}{% link _docs/guides/file_refs.md %}) | Path to `.dll` file for windows. Linkable shared library for unix. |
| `symbols` | [`file_ref`]({{ site.baseurl }}{% link _docs/guides/file_refs.md %}) | Path to the `.pdb` file on Windows or symbols file on MacOS. |
| `delay_load` | [`bool`] | __Only for shared libraries__. Specifies whether the library should be linked with `delay_load` linkage(defaults to `False`). This functionality is not currently supported for the cmake generator or on the UWP platform. |

If you pass a shared library on unix to `lib =`, it will still be linked against. However, in this case `copy_artifacts()` will classify it has `lib` and it will not be copied to the final executable directory for `cxx_binary()` (for backward compatibility for xcode it is still copied, but we plan to remove this feature).

Examples:

```python
cxx_binary(
    name = "my_exe",
    linker_libraries = [
        (target.windows, [
            user_lib(
                lib = "Vulcan.lib",
                dll = "Vulcan.dll",
                symbols = "Vulcan.pdb",
                # Make it delay loaded.
                # delay_load = True,
            )
        ])
    ]
)
```
