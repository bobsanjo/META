---
permalink: /docs/api/shared_node/
title: "SharedNode"
---

*Abstract class*

This is the base node type used by targets that can have different results across different platforms or CPU architectures. For example, a script may generate a different value when compiled for iOS than when compiled for MacOS. In other cases a script might generate a different value for X86 than the value for ARM64. The `sharing` property of these nodes can be used to customize the expectations of the node.

Direct subclasses:

- [option()]({{ site.baseurl }}{% link _docs/api/option.md %})
- [OutMetaNode()]({{ site.baseurl }}{% link _docs/api/out_meta_node.md %})

Inherits all attributes from [MetaNode]({{ site.baseurl }}{% link _docs/api/meta_node.md %}).

| Attribute | Type | Description |
|-----------|------|-------------|
| `sharing` | `<sharing type>` | The sharing model. The default value depends on the type of the node. |

## Sharing Types

| `"root"` | A single out folder is created. | `dist` |
| `"generic"` | A single out folder is created. | `dist/common` |
| `"platform"` | Created for each platform. | `dist/[platform_name]` |

The rest of the types below always create a subfolder inside the "generator". The generator folder is using the `[generator_type]_[platform_name]` format.

| `"generator"` | Each type of generator (cmake, xcode, msvs). | `./` |
| `"generator_platform"` | A a subfolder is used for cross-platform builds. | `./` or `./[cross_platform_name]` if cross-platform target. |
| `"build_config"` | Each configuration generates a separate item (debug, release etc.). | `./[config_type]` |
| `"build_arch"` | Each architecture generates a separate file (x86, arm64 etc.). Note that `universal` is used for universal builds on MacOS instead of actual arch. | `./[config_type]/[arch_type]` |
| `"only_build_arch"` | Same as `build_arch`, but the `[config_type]` is ignored. | `./[arch_type]` |
| `"cpu_arch"` | Each architecture generates a separate file (x86, arm64 etc.). Separate files are generated for each actual architecture of the `universal` builds. | `./[config_type]/[actual_arch_type]` |
| `"only_cpu_arch"` | Same as `cpu_arch`, but the `[config_type]` is ignored.  | `./[actual_arch_type]` |
