---
permalink: /docs/api/cxx_header_map/
title: "cxx_header_map()"
---

```python
cxx_header_map(...)
```

Inherits all attributes from [OutMetaNode]({{ site.baseurl }}{% link _docs/api/out_meta_node.md %}).

| Attribute | Type | Description |
|-----------|------|-------------|
| `headers` | `dict<string,`[`file_ref`]({{ site.baseurl }}{% link _docs/guides/file_refs.md %})`>` | List of headers to be added to the map. |
| `system_headers` | `dict<string,`[`file_ref`]({{ site.baseurl }}{% link _docs/guides/file_refs.md %})`>` | Same as `headers`, but allows using the `#include <name>` syntax to include the header. |

Use this target to remap include paths to specific files on disk.

For example, if the code includes a custom path like `document.h` and the actual include path should have been `jsoncpp/document.h` then you can use the following node to fix it:

```python
cxx_header_map(
    name = "rapidjson_fwd",
    system_headers = {
        "document.h": "$(location rapidjson//rapidjson:rapidjson_git)/include/rapidjson/document.h",
    },
    deps = [
        "rapidjson//rapidjson:rapidjson",
    ]
)

cxx_binary(
    name = "my_exe",
    srcs = [
        "file.cpp"
    ],
    deps = [
        ":rapidjson_fwd"
    ]
)
```

## Implementation details

This feature uses binary Clang header map files in Xcode.

On other platforms, MetaBuild generates a folder with header files that map to the actual files on disk via simple `#include "absolute_file_path.h"`. When this folder is included as an include directory, all the "keys" of the `headers` and `system_headers` map can be included via `#include`.

**Note:** The keys in the maps can even contain ".." folders in order to support code that used hacks like `#include "../projectname/config.h"`.
{: .notice--info}
