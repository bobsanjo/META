---
permalink: /docs/api/import_rules/
title: "import_rules()"
---

```python
import_rules(...)
```

| Attribute | Type | Description |
|-----------|------|-------------|
| `module` | [`module_ref`]({{ site.baseurl }}{% link _docs/guides/target_refs.md %}#module-reference) | The module to import

`import_rules` achieves two tasks.

*(1)* Forces MetaBuild to read the contents of a module. This is often used to ask MetaBuild to read a `deps.meta.py` file where we place all the [`project_link()`]({{ site.baseurl }}{% link _docs/api/project_link.md %})s used by our project. See an example in the [glad](https://git.corp.adobe.com/meta-specs/glad/blob/v0.1.5/META.py#L3) repository. By placing the `import_rules()` call at the beginning of `META.py` we ensure that MetaBuild recognises all the `project_link()`s within `deps.meta.py` as soon as the `META.py` is read by MetaBuild. 

Note that the `project_link` calls don't actually download anything, they just let MetaBuild know that our project depends on another project([`glfw`](https://git.corp.adobe.com/meta-specs/glad/blob/v0.1.5/deps.meta.py#L2) in this example).


*(2)* Creates aliases for targets. Here is an example, you have project `MyProject` with two modules `MyProject//moduleA` and the main META.py module `MyProject//` with the following file structure
```
MyProject/META.py           # (MyProject//)
MyProject/moduleA.meta.py   # (MyProject//moduleA - contains a cxx_library(name = 'my_lib'))
```
And you have a `cxx_library(name = 'my_lib')` inside `moduleA`.
If you place `import_rules('MyProject//moduleA')` (or the equivalent `import_rules(//moduleA)` since they are both in the same project) inside `META.py`, an alias is created for any node in `moduleA` within `META.py`. In other words, you would be able to refer to `MyProject//moduleA:my_lib` as `MyProject//:my_lib`.

This is usually used to create aliases such as `icu//:icu` instead of `icu//icu:icu` [taken from here](https://git.corp.adobe.com/meta-specs/icu/blob/main/icu.meta.py#L90).

However, this is not the only way to create aliases, you can also use the `group()` node. For example, [here](https://git.corp.adobe.com/meta-specs/glad/blob/v0.1.5/META.py#L4) we create an alias `glad//:glad` for the node `glad//glad:glad`.

