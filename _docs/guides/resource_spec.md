---
permalink: /docs/guides/resource_spec/
title: "(Exported) Resources"
---

Any [`cxx_library`]({{ site.baseurl }}{% link _docs/api/cxx_library.md %}) or [`cxx_binary`]({{ site.baseurl }}{% link _docs/api/cxx_binary.md %}) can inject resources into the final binary directory. Similarly, the [`copy_artifacts`]({{ site.baseurl }}{% link _docs/api/copy_artifacts.md %}) command can copy additional resources into the artifact directory that it creates.

The `resources` (or its alias `data`) and `exported_resources` properties are used to specify the files that are going to be copied over. They are a list of files or a dictionary with a format `destination : file`.

## `export`ing

The following example describes the difference between the behaviour of resources and exported_resources.

```py
cxx_library(
    # ...
    xcode_product_type = 'framework',

    # sometext is going to be embedded in this framework
    resources = ['sometext.txt'],

    # other.txt will be copied into any executable that uses this framework.
    exported_resources = ['other.txt'],
)

cxx_library(
    # ...

    # sometext.txt will be copied into any executable that uses this framework.
    # because this library will either be a dylib or a static lib and they don't
    # embed resources.
    resources = ['sometext.txt'],

    # other.txt will also be copied into any executable that uses this framework.
    exported_resources = ['other.txt'],
)

cxx_binary( # or copy_artifacts
    # ...

    # sometext.txt will be embedded in this binary (artifact folder)
    resources = ['sometext.txt'],

    # there is no exported_resources will cxx_binary or copy_artifacts
)

```

## Adding a file to the bundle

The following library will automatically add `my_file.txt` to the `Resources` folder of the application.

```python
cxx_library(
    name = "my_lib",
    data = [
        "assets/my_file.txt"
    ]
)
```

## Adding a file to the bundle only on a specific platform

The `target` tuple structure can be used to filter out the files for a specific platform.

```python
cxx_library(
    name = "my_lib",
    data = [
        (target.macos, "assets/my_file_macos.txt"),

        # Nested arrays are also supported.
        (target.ios, [
            "assets/my_file_ios_1.txt",
            "assets/my_file_ios_2.txt"
        ])
    ]
)
```

## Adding an entire folder

Note that `data` can also be used to copy the contents an entire folder. MetaBuild will retain the folder itself and its entire recursive structure.

To copy an entire folder just add the relative folder path to the `data` list. The result is that the bundle will now contain `Resources/assets_folder/...`.

- When using Xcode the folder will show up as a single reference. Adding new files into the folder **doesn't require** invoking `prepare` again.
- When using Visual Studio, the `prepare` command will actually inline all the files inside the folder. Adding new files into the folder **requires** invoking `prepare` again.

```python
cxx_library(
    name = "my_lib",
    data = [
        "assets_folder"
    ]
)
```

## Customize the output directory

A dictionary structure can be used to customize the destination folder. The key value of the dictionary is the destination path.

```python
cxx_library(
    name = "my_lib",
    data = {
        "sub_path_one": "file_to_copy.txt",

        # Not passing any special prefix is equivalent to using the `resources`
        # special destination. So this line will copy file_to_copy_2.txt to the same 
        # location as file_to_copy.txt.
        "resources/sub_path_one": "file_to_copy_2.txt",

        # You can still pass values that need to be filtered, or lists.
        "sub_path_two": [
            (target.windows, "/path/to/another_file_to_copy_for_win.txt"),
            (target.macos, [
                "/path/to/another_file_to_copy_for_win.txt"
            ]),
        ],
    },
)
```


### Well known destination folders

Xcode allows injecting files into a few places around the bundle. By default `metabuild` adds everything to the `Resources` folder. The first component of the destination folder can be used to customize the default destination.

```python
cxx_library(
    name = "my_lib",
    data = {
        "frameworks": [
            "file_to_copy.txt"
        ],
        "frameworks/USD": [
            "USD.dylib"
        ],
    }
)
```

### Mapping between Xcode locations and other platforms

| Destination (Xcode) |Visual Studio (refer to [MSDN](https://docs.microsoft.com/en-us/cpp/build/reference/common-macros-for-build-commands-and-properties?view=vs-2019) for details on the paths below). |
|---------------------|----------------|
| wrapper             | `$(TargetDir)` |
| executables         | `$(TargetDir)` |
| resources           | `$(TargetDir)` |
| frameworks          | `$(TargetDir)` |
| shared_frameworks   | `$(TargetDir)` |
| shared_support      | `$(TargetDir)` |
| plugins             | `$(TargetDir)/plugins/` |
| java_resources      | `$(TargetDir)/java_resources/` |
| products            | `$(TargetDir)` |
| xpc_services        | `$(TargetDir)` |
