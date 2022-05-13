---
permalink: /docs/api/build_group/
title: "build_group()"
---

```python
build_group(...)
```

Inherits all attributes from [group()]({{ site.baseurl }}{% link _docs/api/group.md %}).

Similar to the `group` node, the `build_group` can be used to group together multiple nodes.

However, the `build_group` also shows up in the actual generated project. It becomes an utility target that can be used to build multiple nodes at once.

```python
build_group(
    name = "build_tests",
    deps = [
        ":test1",
        ":test2"
    ]
)
```

You can compile a specific `build_group` using the `metabuild build` command by adding the `--build-target` argument:

```shell
> metabuild prepare
> metabuild build --build-target :build_tests
```

## MSVS static targets

Static `cxx_library` nodes do not reference their dependencies when using MSVS projects.

This is a build optimization that allows MSVS to compile as many projects in parallel as possible. Adding references between nodes makes MSVS build them in sequence, loosing a lot of CPU power when building smaller targets.

As a side effect though, when building a single static library MSVS doesn't build any of its dependencies.

In order to work around this limitation, the `build_group` can be used to automatically collect all its dependencies under a single project inside the MSVS solution.

MB will automatically add all the required sub-dependencies, so adding a single top dependency to the `build_group` node should be enough to compile all the libs in its dependency sub-tree.
