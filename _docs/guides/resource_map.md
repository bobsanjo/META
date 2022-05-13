---
permalink: /docs/guides/resource_map/
title: "Resource Map"
---

`copy_artifacts` and `cxx_binary` and certain `cxx_library` embed their build dependencies and can further embed other files via the [`resources`]({{ site.baseurl }}{% link _docs/guides/resource_spec.md %}) property. MetaBuild allows the destination of these files to be fine tuned via the `resource_map` property.

The resource map is a list in the format of `(filter, destination_prefix)` or just `destination_prefix`. For every file to be copied, the  file is checked against all the filters (order is important) in the resource map. If a match is made, the destination of the file is modified to be `destination_prefix of matched filter` + `old destination`.

__Notes__
-  If an unfiltered value is supplied, it will be always matched.
- The `destination_prefix` (which supports the following [special variables](#special-variables)) can be either a string or a [`<py method>`]({{ site.baseurl }}{% link _docs/guides/py_method.md %}).
- Each file is assigned a [`file_type`](#file_type) which can be both used for filtering and as a template macro in destination.
- If `target.none` is used as the `destination_prefix`, any file matching it, will not be copied.
- `copy_artifacts` has a [default resource map](#copy_artifacts-default-resource-map) based of `file_type`.
- You can find examples in the [examples](#examples) section and in the [resource_map_example](https://git.corp.adobe.com/meta-samples/resource_map_example) repository.

## `file_type`

MetaBuild divides these copied files into the following groups

| Type      | Description | Example file extensions |
|-----------|-------------|-------------------------|
| `bin`     | The application files. | `.exe`, `.app` |
| `include` | The public include headers. The headers are copied based on the public include directories. If the file doesn't show up in here, make sure to include the files via the `src` property of the `cxx_library` command. The host applications will only have to add this folder in their include path and it will automatically include all the public | `.h`, `.hpp`, `.hxx` |
| `gen_include` | Generated include files (e.g., the export header for cxx libraries) | `.h`, `.hpp`, `.hxx` |
| `lib`     | Static library files. | `.a`, `.lib` |
| `dylib`   | Shared library files | `.dylib`, `.dll` |
| `symbols` | The symbols for all the generated binary objects. | `.pdb`, `.dSYM` |
| `data` or `resource`  | Files added via the [`resource_spec`]({{ site.baseurl }}{% link _docs/guides/resource_spec.md %})  | `.txt`, `.png`, `.gif` |

> Note: any file added via the [`resource_spec`]({{ site.baseurl }}{% link _docs/guides/resource_spec.md %}) goes under `data`. Even if it is a `dylib`.


## Filters

| Type      | Description | Slot |
|-----------|-------------|------|
| `target.none`     | It means don't copy this item. | destination |
| `target.default`     | It means use the default destination.| destination |
| `target.file_type(<file_type>)`     | It matches any file of type `<file_type>`. | predicate |
| `target.matches(<target_ref>)`     | It matches any file originating from the node that has `<target_ref>`. It is possible to use `*` in parts of the `<target_ref>`, e.g., `usd//imaging:*` will match any file coming from any node within the imaging module of project `usd`.  | predicate |
| `target.label(label_name)`     | It matches any file that has the label `label_name` | predicate |
| `target.match_destination(prefix)`     | It matches any file that wants to go to a destination that starts with `prefix`. This will also trim the `prefix` from the destination of the file | predicate |

## Special template variables

The following special variables are supported with the `destination_prefix`.


| Variable name | Description | Example value  |
|---------------|-------------|----------------|
| `$(project.name)` | The name of the project of the target being copied. | `my_project` |
| `$(module.name)` | The name of the module of the target being copied. | `my_module` |
| `$(target.name)` | The name of the target being copied. | `my_library` |
| `$(target.file)` | The full lookup name of the target separated by an underscore `_`. | `my_project_my_module_my_library` |
| `$(target.dir)` | The full lookup name of the target separated by a path separator `/`. | `my_project/my_module/my_library` |
| `$(config.platform)` | The target platform this file has been built for. | `macos`, `ios`, `win32`, `uwp`, `android`, `linux` |
| `$(config.flavors)` | The flavors of the target. | `v8`, `jsc` |
| `$(config.arch)` | The name of the CPU architecture. | `x86`, `x64`, `arm32`, `arm64` |
| `$(config.type)` | The type of the build. | `Debug`, `Release`, `Coverage` |
| `$(config.file)` | Flat subdirectory name that uniquely identifies the target. | `macos_Debug_x64` |
| `$(config.dir)` | Deep subdirectory structure that uniquely identifies the target. | `macos/Debug/x64` |
| `$(file.type)` | Type of the file being copied. | `bin` |

## `copy_artifacts` default resource map

By default the copy_artifacts command has a default resource map in the following form`[$(file.type)]`. I.e., the destination of every file is prefixed by its typename.

## Examples


### Example 1


```python
copy_artifacts(
    name = "shipping_package",
    resource_map = [
        # Any file of type `include` will have its destination prefixed with `my_custom_include_folder`
        (target.file_type("include"), "my_custom_include_folder"),

        # If we are on windows, any file of type `dylib` will have its destination prefixed with dll
        (target.windows & target.file_type("dylib"), "dlls")

        # Any data inherited from `my_library` will be prefixed with custom_folder_for_my_library/$(file.type)
        (target.matches(":my_library"), "custom_folder_for_my_library/$(file.type)")

        # Anything coming from  the module scary_module within bad_project will not be copied.
        (target.matches("bad_project//scary_module:*"), target.none),

        # Any file with label stary_gazer or coming from a node with label stary_gazer gets the prefix start gazers.
        (target.label('stager_gazer'), 'start_gazers'),

        # anything else gets prefixed with big_box. If this value is not supplied, anything else would have just not gotten any prefix.
        'big_box',
    ],
    deps = [
        ":my_library"
    ]
)
```

> The star (`*`) wildcard can be used to match any target inside a subproject. For example, `target.matches("other_project_name//*:*")` will match any targets in the `other_project_name` project.

> Note that you can use `&` and `|` between the filters for further customization.


### Example 2, using custom Python code to compute the output path

```python
set_project_name('axedom')

cxx_library(
    name = "axedom",
    srcs = "lib.cpp"
)

def get_lib_location(ctx):
    platform = ctx.eval("$(config.platform)")
    arch = ctx.eval("$(config.arch)")
    config = ctx.eval("$(config.type)")
    path = f"libraries/{platform}/{arch}/static/{config.lower()}/axedom"
    return path

copy_artifacts(
    name = "copy_axedom",
    deps = [
        ":axedom"
    ],
    out = "axe/public",
    resource_map = [ 
        (target.file_type("lib"), get_lib_location)
    ],
)

group(
    name = "main",
    deps = ":copy_axedom"
)
```
