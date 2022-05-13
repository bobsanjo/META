---
permalink: /docs/api/archive_artifacts/
title: "archive_artifacts()"
---

```python
archive_artifacts(...)
```

`archive_artifacts` has the same behavior as `copy_artifacts` except that it places all the artifacts into an archive file instead. The name of the generated archive is based on the name of the node.

Inherits all attributes from [copy_artifacts]({{ site.baseurl }}{% link _docs/api/copy_artifacts.md %}).

| Attribute | Type | Description |
|-----------|------|-------------|
| `type` | `"zip"` | The type of archive to generate. Only `"zip"` is supported at the moment. |

> The `extract_files()` from `copy_artifacts` is not currently supported with the `archive_artifacts` node type.
