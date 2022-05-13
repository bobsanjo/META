---
permalink: /docs/guides/msvs_flags/
title: "Microsoft Visual Studio Flags"
---

The `msvs_flags` property is a dictionary of MSVS property names to values.

Find the required property names in the `properties` list inside the [MSVSProperties.py](https://git.corp.adobe.com/meta-build/meta-build/blob/main/metabuild/generator/msvs/MSVSProperties.py) file.

For example, in order to enable `WinRT` mode, use the following snippet of :

```python
cxx_binary(
    name = "my_exe",
    # The entire target gets the WinRT flag enabled.
    msvs_flags = {
        "ClCompile.CompileAsWinRT": True
    }
)
```

The compiler flags can also be applied only to a subset of files using the `target.msvs_flags()` method:

```python
cxx_binary(
    name = "my_exe",
    srcs = [
        (
            target.msvs_flags({
                "ClCompile.CompileAsWinRT": True
            }),
            [
                # Only the following files will get the WinRT flag enabled.
                "winrt_file1.cpp",
                "winrt_file2.cpp"
            ]
        ),

        "regular_file3.cpp"
    ]
)
```
