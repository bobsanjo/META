---
permalink: /docs/api/build_spec/
title: "build_spec()"
---

```python
build_spec(...)
```

| Attribute | Type | Description |
|-----------|------|-------------|
| `output_name`| `string` | You can use this value to customize the output location of the build spec. |
| `config` | `dict` | A dictionary of preset values of MetaBuild [MetaBuild configs]({{ site.baseurl }}{% link _docs/cli/metabuild_config.md %}). |
| `lock_file` | `filename` | An additional lock file to be used for the build spec. |

A build_spec is a preset for MetaBuild config values with its dedicated output directory. This will allow accessing the projects generated for each preset simultaneously without needing to regenerate a project everytime you switch between them.

Note that build specs are only relevant for the [root project]({{ site.baseurl }}{% link _docs/guides/target_refs.md %}#root).

The workflow is that
1. Define the presets via calls to `build_specs()`
2. Create a group() with name `specs` in the root project's `META.py`. You can also use a different name. In that case set the `mb.specs_group` config to point to your group.
3. When running metabuild prepare, pass the name of the spec for which you like to generate the project with `--spec spec_name`.

## Example 1

[TechLibB/META.py](https://git.corp.adobe.com/meta-samples/flavor_and_option/blob/main/TechLibB/META.py): Generate different projects for different values of an option (or options). So that developers can work on the library without needing to generate a new project for each option value.

## Example 2

[MetaBuild unit test for build specs](https://git.corp.adobe.com/meta-build/meta-build/blob/0.1.510/tests/generator/__fixtures__/build_specs/META.py).