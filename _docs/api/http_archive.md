---
permalink: /docs/api/http_archive/
title: "http_archive()"
---

```python
http_archive(...)
```

Inherits all attributes from [OutMetaNode]({{ site.baseurl }}{% link _docs/api/out_meta_node.md %}).

Downloads and extracts an archive from the web. MetaBuild automatically adds the required headers for archives coming from Artifactory.

| Attribute | Type | Description |
|-----------|------|-------------|
| `urls` | `list<string>` | List of fallback urls to use for the download. |
| `trim` | `int` | Number of folders to trim from the root of the archive. |
| `sha256` | `string` | The expected `sha256` of the file. The hash can also be added the the `META.lock` file, so this attribute is optional. |

Note: python must be compiled/installed with support for the specific archive types needed, for tar.xz support on MAC use
```brew install xz && pyenv install 3.x.x```
