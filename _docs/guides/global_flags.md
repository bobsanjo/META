---
permalink: /docs/guides/global_flags/
title: "Global Flags"
---

In order to support defining global flags, all `cxx_library` and `cxx_binary` nodes automatically depend on multiple predefined targets.

- `meta//:default_flags`, `meta//:xcode_defaults` and `meta//:msvs_defaults`
    These are a internal targets defined inside the [builtin MetaBuild project](https://git.corp.adobe.com/meta-build/meta-build/blob/main/meta/builtin/).

    **Note:** The builtin module is currently part of MetaBuild repo, but [issue 56](https://git.corp.adobe.com/meta-build/meta-build/issues/56) has been added to extract it out of the repo in order to allow projects to fork and customize the default flags.
    {: .notice--info}

- `root//:universe_flags`

    Any project can customize this target by adding a `cxx_library(name = "universe_flags")` to the root `META.py` file of the project.

    Note that `root` is a pseudo project name that always refers to the root project that is currently being compiled.

    As a result, any of the "universe_flags" nodes defined by sub-targets are completely ignored.

- `//:project_flags`

    Any project can customize this target by adding a `cxx_library(name = "project_flags")` to the root `META.py` file of the project.

    All the Cxx targets of current project automatically inherit the flags injected by this node.

- `:module_flags`

    Any module can customize this target by adding a `cxx_library(name = "module_flags")` to either `META.py` or `.meta.py` files.

    All the Cxx targets of the same module automatically inherit the flags injected by this node.

For a simple example of how global flags work, check the [global flags test case](https://git.corp.adobe.com/meta-build/meta-build/tree/main/tests/generator/__fixtures__/global_flags) in MetaBuild.

**Note:** The predefined targets can have any type including even [`group()`](group.md), meaning more flags can be grouped under a single umbrella using the `deps` property of the predefined node.
{: .notice--info}

## Examples

### Adding flags directly into the project

```python
cxx_library(
    name = "universe_flags",

    # Using the "exported_xcode_flags" to inject the flags into every target.
    exported_xcode_flags = {
        "GCC_WARN_PEDANTIC": True
    }
)
```

### Adding flags via a separate configuration project

The actual flags do not have to be defined in the root project, but instead the dependency chain can be used to pull in a shared configuration project instead.

Let's assume that we have two projects:

- a shared configuration project called `my_shared_config`
- our product project called `my_project`

#### `my_project/META.py`

```python
# Add a link to the `my_shared_config` project.
project_link("my_shared_config")

group(
    name = "universe_flags",
    deps = [
        # Link to the the shared flags from the `my_shared_config` repository.
        "my_shared_config//:all_flags",
    ]
)

cxx_binary(
    name = "my_exe",
    srcs = [
        "main.cpp"
    ]
)

group(
    # By default MetaBuild looks for the "root//:main" target.
    name = "main",
    deps = [
        ":my_exe"
    ]
)
```

#### `my_shared_config/META.py`

```python
cxx_library(
    name = "warning_flags",
    exported_xcode_flags = {
        "GCC_WARN_PEDANTIC": True
    }
)

cxx_library(
    name = "preprocessor_flags",
    exported_preprocessor_macros = [
        "MY_CUSTOM_GLOBAL_DEFINE=1"
    ]
)

cxx_library(
    name = "ios_flags",
    filter = target.ios,
    exported_xcode_flags = [
        DEVELOPMENT_TEAM = "TLYL9F912X",
    ]
)

group(
    name = "all_flags",
    deps = [
        ":warning_flags",
        ":preprocessor_flags",
        ":ios_flags"
    ]
)
```
