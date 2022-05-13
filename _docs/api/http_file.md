---
permalink: /docs/api/http_file/
title: "http_file()"
---

```python
http_file(...)
```

Inherits all attributes from [OutMetaNode]({{ site.baseurl }}{% link _docs/api/out_meta_node.md %}).

Downloads a file from the web. MetaBuild automatically adds the required headers for files coming from Artifactory.

| Attribute | Type | Description |
|-----------|------|-------------|
| `urls` | `list<string>` | List of fallback urls to use for the download. |
| `url` | `list<string>` | Alias for `urls` |
| `link_from_cache` | `boolean` | Links the `$(location)` of the node directly from the cache. Defaults to `False`. |
| `sha256` | `string` | The expected `sha256` of the file. The hash can also be added the the `META.lock` file, so this attribute is optional. |
