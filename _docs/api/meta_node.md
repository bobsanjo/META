---
permalink: /docs/api/meta_node/
title: "MetaNode"
---

*Abstract class*

Direct subclasses:

- [group()]({{ site.baseurl }}{% link _docs/api/group.md %})
- [meta_tool()]({{ site.baseurl }}{% link _docs/api/meta_tool.md %})
- [SharedNode]({{ site.baseurl }}{% link _docs/api/shared_node.md %})

Most APIs in MetaBuild are actually MetaNode constructors with different types.

All types of meta nodes inherit attributes from the base `MetaNode` class.

| Attribute | Type | Description |
|-----------|------|-------------|
| `name` | `string` | The name of the meta node. This is used to uniquely identify the node across the project. |
| `project_name` | `string` | The name used to create the Xcode/MSVS/Cmake targets. By default MB uses the `name` property. |
| `project_subpath` | `string` | The subfolder used for this project inside the MSVS solution explorer. Other project types like Xcode use this path to change the scheme naming to allow better grouping. |
| `deps` | `list<`[`target_ref`]({{ site.baseurl }}{% link _docs/guides/target_refs.md %})`>` | List of nodes that the node depends on. |
| `excluded_deps` | `list<`[`target_ref`]({{ site.baseurl }}{% link _docs/guides/target_refs.md %})`>` | CxxNode's can use this to excluded flavors getting propagated to them to not get flavored. Also you can use this to escape flags getting inheritted from other CxxNode's. Note thate the latter usage has performance costs (needs reocomputation of the dependency graph), so it should be used with caution and only for MetaBuild default flags stored in the [bultin](https://git.corp.adobe.com/meta-build/meta-build/blob/0.2.68/metabuild/builtin/META.py) project. |
| `licenses` | `list<string>` | Reserved for future use. |
| `labels` | `list<string>` | Each MetaBuild node can be assigned a label. This can be used in the `resource_map` of `copy_artifacts()` and `cxx_binary()`. |
| `filter` | [`filter`]({{ site.baseurl }}{% link _docs/api/target.md %}) | Use this property to remove the node from specific platforms or configurations. |
| `target_remap` | `dict<`[`src_platform_filter`]({{ site.baseurl }}{% link _docs/api/target.md %}#platform-filters)`, `[`dest_platform_filter`]({{ site.baseurl }}{% link _docs/api/target.md %}#platform-filters)`>` | Remaps from the `src_platform_filter` platform to the `dest_platform_filter` platform. When a project needs to use `src_platform_filter`, MetaBuild will automatically switch to using the `dest_platform_filter` version instead. <br /><br />For example, on UWP sometimes it is needed to build some of the targets as regular Win32 projects. For more info check the [Building Win32 projects on UWP guide]({{ site.baseurl }}{% link _docs/guides/build_win32_on_uwp.md %}). <br/><br/>**Note** that this remapping can only be used with platform `filters` like `target.uwp`, `target.win32`, etc. |
| `tests` | `list<`[`target_ref`]({{ site.baseurl }}{% link _docs/guides/target_refs.md %})`>` | List of tests for the node, see [`test()`]({{ site.baseurl }}{% link _docs/api/test.md %}). |
