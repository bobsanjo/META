---
permalink: /docs/api/cxx_binary/
title: "cxx_binary()"
---

```python
cxx_binary(...)
```

Inherits all attributes from [CxxNode]({{ site.baseurl }}{% link _docs/api/cxx_node.md %}).

| Attribute | Type | Description |
|-----------|------|-------------|
| `cli` | `bool` | *deprecated* Default is `false`. When `true` the generated Xcode target builds a command line executable target instead of an `.app` bundle. This property is deprecated, use `xcode_product_type = "tool"` instead. |

