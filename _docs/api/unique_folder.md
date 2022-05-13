---
permalink: /docs/api/unique_folder/
title: "unique_folder"
---

```python
system_lib(...)
```

Inherits all attributes from [OutMetaNode]({{ site.baseurl }}{% link _docs/api/out_meta_node.md %}).

Creates a unique folder that can be shared across other nodes. The `branch` attribute changes the generated location inside the `dist` folder.

| Attribute | Type | Description |
|-----------|------|-------------|
| `branch` | `list<string>` | Defaults to `[ "common", "unique_folder" ]` |

In this example, we let MB create a unique folder and then we tell the C++ targets to generate their output as subfolders inside that unique folder. This is sometimes needed when the code requires a very specific structure on disk.

The main advantage is that the `unique_folder` is still owned by MB and it is not a hardcoded path inside the project.

```python
unique_folder(
    name = "builds_dir",
    branch = "my_build_dir",

    # We want a different folder for each build configuration & architecture.
    sharing = "build_arch"
)

cxx_binary(
    name = "target1",
    out = "$(location :builds_dir)/target1",
)

cxx_binary(
    name = "target2",
    out = "$(location :builds_dir)/target2",
)
```
