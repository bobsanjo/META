---
permalink: /docs/guides/build_win32_on_uwp/
title: "Building as WIN32 on UWP"
---

Some UWP projects require using regular WIN32 targets instead of compiling as Universal Projects. Use the [`target_remap`]({{ site.baseurl }}{% link _docs/api/meta_node.md %}) property to force all dependents that request a regular `UWP` configuration to switch to using the `WIN32` version instead.

```python
cxx_library(
    name = "win32_lib",
    target_remap = {
        target.uwp: target.win32
    }
    ...
)
```
