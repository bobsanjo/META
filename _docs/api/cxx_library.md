---
permalink: /docs/api/cxx_library/
title: "cxx_library()"
toc: true
---

```python
cxx_library(...)
```

Inherits all attributes from [CxxNode]({{ site.baseurl }}{% link _docs/api/cxx_node.md %}).

By default properties added through the [CxxNode](cxx_node.md) attributes are only applied to the current target.

The `cxx_library` can also export properties that are automatically injected into targets that depend on this node.

| Attribute | Type | Description |
|-----------|------|-------------|
| `exported_srcs` | `list<`[`file_ref`]({{ site.baseurl }}{% link _docs/guides/file_refs.md %})`>` | List of files to be added to all the direct dependents of this target. Both headers and sources can be added using property. Targets can have 0 or more exported source files. This property is useful when you need the dependent targets to compile a file inside their own project instead of compiling inside the library. For example, this useful to inject files to be compiled by the EXE project bundle, which means we can have a single shared "main" method across multiple projects without getting linker errors. |
| `exported_preprocessor_macros` | `list<string>` | List of preprocessor macros to be used when compiling the files of the current target and any of the direct dependent targets. |
| `exported_compiler_flags` | `list<string>` | List of compiler flags to be used when compiling the files of the current target and any of the direct dependent targets. |
| `exported_linker_flags` | `list<string>` | List of linker flags to be used when compiling/linking the target with the final binary. |
| `exported_linker_directories` | `list<`[`file_ref`]({{ site.baseurl }}{% link _docs/guides/file_refs.md %})`>` | List of linker directories used when compiling / linking the target to the final binary. |
| `exported_framework_directories` | `list<`[`file_ref`]({{ site.baseurl }}{% link _docs/guides/file_refs.md %})`>` | List of Xcode framework directories used when compiling / linking the target to the final binary. |
| `exported_linker_libraries` | `list<`[`file_ref`]({{ site.baseurl }}{% link _docs/guides/file_refs.md %})` or `[`system_lib`]({{ site.baseurl }}{% link _docs/api/system_lib.md %})` or `[`user_lib`]({{ site.baseurl }}{% link _docs/api/user_lib.md %})`>` | List of libraries to be linked to the final target. See the [Linking binaries]({{ site.baseurl }}{% link _docs/guides/linking_binaries.md %}) page for more details. |
| `exported_xcode_flags` | [`xcode_flags`]({{ site.baseurl }}{% link _docs/guides/xcode_flags.md %}) | Custom flags added to the current target and all the direct dependent targets in the generated Xcode project. |
| `exported_msvs_flags` | [`msvs_flags`]({{ site.baseurl }}{% link _docs/guides/msvs_flags.md %}) | Custom flags added to the current target and all the direct dependent targets in the generated Microsoft Visual Studio project. |
| `public_include_directories` | `list<`[`file_ref`]({{ site.baseurl }}{% link _docs/guides/file_refs.md %})`>` | List of include directories used when compiling the files of the current target and any of the direct dependent targets. |
| `public_system_include_directories` | `list<`[`file_ref`]({{ site.baseurl }}{% link _docs/guides/file_refs.md %})`>` | Same as `public_include_directories` above, but allows using the `#include <name_of_file>` syntax to include the files. This property is exactly the same as `public_include_directories` when using the Microsoft Visual Studio generator. |
| `link_whole` | `bool` | Reserved for future use. |
| `reexport_all_header_dependencies` | `bool` | Defaults to false. When set to `true`, all the nodes from the `deps` list of the current target are automatically added to the list of `exported_deps` defined below. |
| `exported_deps` | `list<`[`target_ref`]({{ site.baseurl }}{% link _docs/guides/target_refs.md %})`>` | See [`exported_deps`](#exported_deps) section below. |

## DLLs support

Read more about creating dynamic loaded libraries in the [DLLs on MetaBuild]({{ site.baseurl }}{% link _docs/guides/dlls.md %}) guide.

| Attribute | Type | Description |
|-----------|------|-------------|
| `preferred_linkage` | `string` | Changes the preferred linking type of the current target. Accepted values are `any`, `static` or `shared`. Default value is `any`. |
| `lib_macro` | `string` | Macro name to use when creating DLLs with MetaBuild. Default value is `uppercase({project_name}_{module_name}_{target_name})`. If the target is defined in the root module, then the default value becomes `uppercase({project_name}_{target_name})`.  |
| `inside_macro` | `string` | This macro is automatically defined and can be used to detect if the file is compiled as part of the library or as part of a public include of the library. The default macro name is `MB_INSIDE_{lib_macro}`. |
| `export_macro` | `string` | Export macro that can be used to export symbols when creating DLLs with MetaBuild. The default name is `MB_EXPORT_{lib_macro}`. <br/>**Note** that the macro is not added automatically and the `ExportMacro.h` header needs to be included. Read more in the [DLLs on MetaBuild]({{ site.baseurl }}{% link _docs/guides/dlls.md %}) guide linked above. |
| `msvs_generates_import_library` | `boolean` | Whether a dll generates an import library too (.lib file). Default value is true. Set this to false when you create a shared DLL that doesn't export any `__declspec(dllexport)` symbols. |
| `msvs_import_library_name` | `string` | For an msvs dll, this can be used to change the name of the import library (.lib file) corresponding to a dll. Note that this value is only relevant for DLLs. The name of a .lib file generated for a static library is controlled by product_name. |



## exported_deps

By default a target only inherits the properties exported from the immediate set of dependencies. This does not affect linking, a chain of dependencies are always linked to the final target whether they are added in `deps` or `exported_deps`.

If the public headers exposed by this target require headers from other targets, then it is convenient to let the dependents know that extra headers are needed.

For example, if you define `library_a` which uses `boost` in the public headers, then anyone using `library_a` would also need to manually add `boost` to their own set of `deps`.

Using `exported_deps` property a target can automatically inject exported properties (i.e. `exported_preprocessor_macros`, `exported_xcode_flags`, etc) from libraries like `boost` into the dependents without changing the users of `library_a`.

The propagation of properties from a library (`library_1`) in a chain of dependencies - `library_1` -> `library_2` -> ...-> `library_n` - stops when one of the dependencies in the chain `library_k` uses `deps` instead of `exported_deps` when adding `library_k-1`.

Dependencies added to the `exported_deps` list are automatically added to the end of the `deps` list.

If you need to re-order the include directories between dependencies, then add the exported dependency to both `deps` and `exported_deps` and sort the `deps` list as needed.
