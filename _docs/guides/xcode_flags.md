---
permalink: /docs/guides/xcode_flags/
title: "Xcode Flags"
---

The `xcode_flags` property is a dictionary of Xcode property names to values.

Find the required property names in the `XCODE_PROPERTIES` list inside the [XcodePropertiesGen.py](https://git.corp.adobe.com/meta-build/meta-build/blob/main/metabuild/generator/xcode/XcodePropertiesGen.py#L17) file.

The property name can also be extracted using `Cmd + C` when the option is highlighted in Xcode.

```python
cxx_binary(
    name = "my_exe",
    # The entire target gets the GCC_WARN_PEDANTIC flag disabled.
    xcode_flags = {
        "GCC_WARN_PEDANTIC": False
    }
)
```

Note that `xcode_flags` can only be changed on an entire target and individual files cannot apply different flags. However, the `target.flags()` method can be used to add specific Clang compiler flags for individual files.

```python
cxx_binary(
    name = "my_exe",
    srcs = [
        (
            target.flags("-mavx2"),
            [
                # Only the following files will get the "-mavx2" flag.
                "avx2_file1.cpp",
                "avx2_file2.cpp"
            ]
        ),

        "regular_file3.cpp"
    ]
)
```
