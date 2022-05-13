---
permalink: /docs/api/msvs_rule/
title: "msvs_rule()"
---

```python
msvs_rule(...)
```

You can customize how certain files are processed within a visual studio c++ target (library or executable) by adding a `msvs_rule()` to your project. For example you can compile assembly files (.ASM) using NASM or compile GPU kernels (OpenCL, DirectX) by registering a custom rule to process those file types.

Inherits all attributes from [MetaNode]({{ site.baseurl }}{% link _docs/api/meta_node.md %}).

| Attribute | Type | Description |
|-----------|------|-------------|
| `file_type` | `string` | file type that is matched against `msvs_type()` filter when adding sources to a [CxxNode]({{ site.baseurl }}{% link _docs/api/cxx_node.md %}). |
| `file_patterns` | `list<string>` | List of file patterns which this rule should be applied to (accepts wildcards). |
| `msvs_flags` | `dict<string, string>` | Dictionary of properties for the custom build rule. |

## Example 1

```python
msvs_rule(
    name = "compile_asm_with_custom_compiler",
    file_patterns = '*.asm',
    file_type = "asm_tag",
    msvs_flags = {
        "CustomBuild.Command": [
            # Notice how you can pass parameters from the library that uses the rule
            # to the rule itself, using Custom flags. Note the absence of prefix of `Custom.`
            # here.
            '"/path/to/CUSTOM_COMPILER" --tag $$(MyTag) -o "$$(IntDir)/%(Filename).obj" "%(FullPath)"'
        ],
        "CustomBuild.Outputs": "$$(IntDir)/%(Filename).obj",
        "CustomBuild.Message": "CUSTOM_COMPILER: %(Filename).asm",
        "CustomBuild.BuildInParallel": False,
    }
)

cxx_library(
    name = "my_lib",
    srcs = [
        # the rule will be applied to this file due to matching pattern
        "somefile.asm",

        # the rule will be applied to this file due to matching file type
        (target.msvs_type("asm_tag"), "somefile.asm"),

        # the rule will not be applied to this file.
        "foo.cpp",
    ]
    msvs_flags = {
        # If you want to communicate some information to the rule from the library, you can use
        # custom variables like below.  Note the use of the prefix of `Custom.`.
        'Custom.MyTag': 'something',
    }
    deps = [
        ":compile_asm_with_custom_compiler"
    ],
)

```


__Note__ Use `$$(var_name)` to reference msvs variables or wrap the string in `escaped_value()`. Metabuild parses `$()` as [`value templates`]({{ site.baseurl }}{% link _docs/guides/value_templates.md %}) by default.

__Note__ See [MsBuild well known metadata](https://docs.microsoft.com/en-us/visualstudio/msbuild/msbuild-well-known-item-metadata?view=vs-2019) regarding values wrapped in `%()`.
