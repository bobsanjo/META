---
permalink: /docs/api/load/
title: "load()"
---

```python
load(...)
```

`load()` allows you to bring python objects (variables or functions) from one `.meta.py` file to another. The use is `load(`[`module_ref`]({{ site.baseurl }}{% link _docs/guides/target_refs.md %}#module-reference)`, *args)`. The input to the function is a reference to a MetaBuild module


| Attribute | Type | Description |
|-----------|------|-------------|
| `module` | [`module_ref`]({{ site.baseurl }}{% link _docs/guides/target_refs.md %}#module-reference) | The file needed for upload. |
| `*args` | `string` | Name of object(s) to be loaded. |


## Examples

- [pybind11](https://git.corp.adobe.com/meta-specs/pybind11/blob/main/test.meta.py#L1) provides its users with `pybind11_module`.
- [pitchfork](https://git.corp.adobe.com/meta-specs/pitchfork/blob/main/sample/META.py#L4) provides its users with the object `pitchfork`.
- Here is an [internal usage of load](https://git.corp.adobe.com/meta-specs/boost/blob/main/deps.meta.py#L1) within a project, to bring in a variable, `boost_sha1`, from one file in the project to another.
