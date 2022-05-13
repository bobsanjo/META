---
permalink: /docs/api/option/
title: "Option"
---

Inherits all attributes from [SharedNode]({{ site.baseurl }}{% link _docs/api/shared_node.md %}).

| Attribute | Type | Description |
|-----------|------|-------------|
| `config` | `string` | The configuration name that can be used to change this value. |
| `type` | `string`, `bool`, `int`, `float`, `filename`, `file_list`, `version` | The type of the option value. Default is `string`. |
| `description` | `string` | User friendly description for this option. |
| `choices` | `string` | List of options available for this node. The type must be a `string`. |
| `default_value` | `<type>` | The default value of the option when there's no configuration from the user. |
| `py` | [`<py method>`]({{ site.baseurl }}{% link _docs/guides/py_method.md %}) | Method that will be invoked by MB when there's no configuration from the user to compute the default value dynamically. Useful when a value must be computed dynamically on demand. |

## `config`

The `config` indicates how the devs and the users of your project can set the value of this option via MetaBuild [config]({{ site.baseurl }}{% link _docs/cli/metabuild_config.md %}) workflow. For example, If the value of the config is `adobe_stager.licensing_backend`, then your project and your users can set the value of this option in the lock file with `[adobe_stager]licensing_backend=..`. 

> *It is highly recommended to use the name of your project for the config prefix (value before `.`) to prevent option name collision.*

## Filename type

Filenames are resolved relative to the configuration source. For example, if the option is set via a META.lock file, the file is resolved relative to the META.lock file. If the path is injected through CLI `--define` it is resolved relative to the root project. If the option is configured using global YAML configuration files, the paths are relative to those yaml files.

## Version type

Versions are using "semver" format. Internally MB uses https://pypi.org/project/semver/ to parse the versions.

The main advantage to using type version is the ability to compare values using semver semantics. This is very useful when building specifications for open-source libraries that can build more than one version.

```python
cxx_library(
    srcs = [
        (target.option(":mylib_version", ">= 1.0.5"), [
            "new_file_added_in_1_0_5.cpp"
        ]),

        (target.option(":mylib_version", ">= 1.0.0 < 1.0.5"), [
            "new_file_added_in_1_0_0_removed_in_1_0_5.cpp"
        ])
    ]
)

git_checkout(
    commit = [
        (target.option(":mylib_version", "== 1.0.0"), "sha1"),
        (target.option(":mylib_version", "== 1.0.2"), "sha2"),
        (target.option(":mylib_version", "== 1.0.3"), "sha3"),
    ]
)
```

## Using a Python method

If you need to compute a value and reuse it across different nodes, it is useful to wrap that up as an `option()` node.

The main advantages:

1. Can reuse the value across nodes / modules without recomputing it twice.
2. The model uses the target reference in MB, so it also works across different projects.

For more info on the `ctx` page check the [`<py method>`]({{ site.baseurl }}{% link _docs/guides/py_method.md %}) reference.

```python
async def _compute_value(ctx):
    # Can nest values using the context.eval_async method.
    file = await ctx.eval_async("$(resolve ./version.json)")
    with open(file) as stream:
        data = json.loads(stream.read())
        return data.get("version")

option(
    name = "computed_value",
    py = _compute_value
)

cxx_library(
    preprocessor_macro = [
        "VERSION=$(option :computed_value)"
    ]
)
```
