---
permalink: /docs/api/flavor/
title: "flavor()"
---

| Attribute | Type | Description |
|-----------|------|-------------|
| `variants` | `string list` | The different variant values for the flavor. |
| `default_variant` | `string` | Optional, default value of the variant |

> If you somehow landed on this page, it is highly possible that you are looking for the [`option`]({ site.baseurl }}{% link _docs/api/option.md %}) node. Usages of the `flavor` node are much more rare compared to `option`.

A flavor node allows you to have multiple variants of the same target within the same project. For example, both the static and dynamic variants of a library.


## Example 1

Here is a toy example showing a very common use case: [meta-samples/flavor_and_option/TechLibA/META.py](https://git.corp.adobe.com/meta-samples/flavor_and_option/blob/0.1.0/TechLibA/META.py)

In this example, we have a target `TechLibA` which has two variants. Here it is simply the value of a macro, but in reality it can be different type of backend technologies (e.g., Javascript engine in [UXP](https://git.corp.adobe.com/torq/torq-native) or rendering technology in [RTE](https://git.corp.adobe.com/Aero/rte/)).
The developers of the library would like to have all the variants in the same project, so they can quickly test the effect of changing their code without needing to open a new project. In this case, a flavor node is used.

Even though the `TechLibA` is flavored, it is only used by the devs of this lib. For the users of `TechLibA` they only need a single backend in their project. An option node is used for users to select the backend type while the flavor is hidden from the users.

Here is a user of this library [Application/META.py](https://git.corp.adobe.com/meta-samples/flavor_and_option/blob/0.1.0/Application/META.py). They just deal with a single variant and set the backend_type in their [META.lock](https://git.corp.adobe.com/meta-samples/flavor_and_option/blob/0.1.0/Application/META.lock#L2).

# Example 2

[Static and shared variants of the same library](https://git.corp.adobe.com/meta-samples/dll_combo).

> Note that for many simple scenarios, you don't necessarily need flavors, and you can achieve a similar behavior by separate calls to `cxx_library`. For example, [here](https://git.corp.adobe.com/structure/structure/blob/1.1.0/META/sdk.meta.py#L80) we use a template function [structure_cxx_library()](https://git.corp.adobe.com/structure/structure/blob/1.1.0/META/utils.meta.py#L3-L16), to create two libraries, one static and one dynamic without the use of flavors.
