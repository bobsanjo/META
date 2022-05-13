---
permalink: /docs/guides/target_refs/
title: "Target References"
toc: true
---

All meta nodes can be referenced uniquely using a string composed of 3 parts. All The canonical reference follows a simple pattern adopted from other open source projects.

## Canonical form

```escape
[project_name]//[module_path]:[node_name]
```

- The first two parts are a reference to the module that the node resides in and the last part is the node name.
- The root module of a project - `META.py` - is considered to have no path, so we skip the `module_path` above.
- The recommended pattern for extra module file names is to use `[module_name].meta.py`. When referring to a node inside a module we don't have to include the `.meta.py` extension as MetaBuild will automatically find the correct module as needed.

### Examples:

In the examples below `LibraryAFolder` is the folder that contains the `META.py` file for the `LibraryA` library. 

1. `LibraryA//:root_node_a`: Refers to the `root_node_a` node inside `LibraryAFolder/META.py`
2. `LibraryA//extra_module:custom_node_in_extra_module` - Refers to the `custom_node_in_extra_module` node inside the `LibraryAFolder/extra_module.meta.py` module.
3. `LibraryA//my_folder/extra_module:custom_node_in_extra_module` - Refers to the `custom_node_in_extra_module` node inside the `LibraryAFolder/my_folder/extra_module.meta.py` module.

We can skip some of these components when referring to nodes in the same project or module.

## Referring to a node in the same project

1. If the other node is inside the same project as the caller, then we can skip the name of the project entirely. In this scenario, MetaBuild will look for `[node_name]` inside a module with path `[module_path] + .meta.py` relative to the "folder that contains the META.py for your project".
    ```escape
    //[module_path]:[node_name]
    ```
2. If you also omit the `//`,
    ```escape
    [module_path]:[node_name]
    ```
    MetaBuild will look for `[module_path]` in the same project, where `[module_path]` is relative to the folder that contains the current module.

> The rule `(2)` here is kept for backward compatibility. However, for the sake of consistency and keeping the rules as simple as possible try to not use rule `(2)` as much as possible and stick with `(1)`.


### Examples:

- `//extra_module:custom_node_in_extra_module`: refers to the `custom_node_in_extra_module` node inside the `extra_module.meta.py` module from the current project.
- `//:custom_node_in_extra_module` refers to `custom_node_in_extra_module` inside current project's `META.py`.

## Referring to a node in the same module

If the target is in the same module, we can skip the the module_path entirely. In this case we also need to skip the "//" prefix to make sure the parse understands we are referring to the current module and not the root `META.py`.

```escape
:[node_name]
```

### Examples:

- `:root_node_a` - Refers to the `root_node_a` from inside the same Meta Module as the one that is making this current request.

## Builtin project names

There are two project names that are prebuilt in MetaBuild.

### `root`

The `root` is just a symlink to the root project. For example, `root//:node_1` refers to the `node_1` node inside the toplevel root project. The `root` target can be used from any sub-project and always points back to the root project.

### `meta`

This is a builtin meta project that is provided out of box by MetaBuild.

> __NOT IMPLEMENTED YET__ The `meta` project can be forked and customized by the root projects. [Tracking bug for the `meta` forking support](https://git.corp.adobe.com/meta-build/meta-build/issues/56).

## Module Reference

Some functions such as [`load()`]({{ site.baseurl }}{% link _docs/api/load.md %}) and [`import_rules()`]({{ site.baseurl }}{% link _docs/api/import_rules.md %}) take references to modules as inputs (as opposed to node references). If you omit the `:` and anything after it in a target reference you arrive at a module reference, e.g. `project//module`, `//module`, `project//` (referring to META.py in project).

> You might see some code around that uses improper module references, such as `import_rules('//:deps')` (instead of correct form `//deps`). Due to backward compatibility we support such forms (the `:` is ignored), but use of them is deprecated and could be removed in future.
