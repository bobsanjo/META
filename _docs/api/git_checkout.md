---
permalink: /docs/api/git_checkout/
title: "git_checkout()"
---

```python
git_checkout(...)
```

Inherits all attributes from [OutMetaNode]({{ site.baseurl }}{% link _docs/api/out_meta_node.md %}).

Clones and checks out a GIT repository.

| Attribute | Type | Description |
|-----------|------|-------------|
| `repo` | `string` | The GIT remote URL - this string is passed directly to `git clone` without any processing. |
| `submodules` | `bool` | Defaults to `True`. Set this to `False` to avoid checking out the git submodules. |
| `commit` | `string` | The commit or branch to fetch. |

Note that all of these values are written to the `META.lock` file after the first `metabuild sync`. A developer can change the `META.lock` file of any of the projects in order to override the values in the specification.

The behaviour of `git_checkout()` can also be configured via the config files. The configs that affect the `git_checkout()` have the form `<target_ref of git_checkout>.property`, e.g., `zstd//deps:zstd_git.commit=...`. These are all the values that can be set via config files

| Attribute | Type | Description |
|-----------|------|-------------|
| `repo` | `string` | Same behaviour |
| `submodules` | `bool` | Same behaviour |
| `commit` | `string` | The commit to fetch. git tag also works, but not recommended (cannot be cached as good as sha and MetaBuild ends up doing more git calls). Instead add tag as a comment. |
| `auto_lock` | `bool` | see below |
| `dev_branch` | `string` | Name of a branch. This is only for prototyping and debugging and should not be used in production. |


Note that even if the `commit` property is set to a branch or a tag name, the commit value that is written to the lock file is the actual hash of the change. The lock file helps making the builds completely reproducible on different machines even if the branches added more commits.

However, if the option `auto_lock=false` is specified in the lock file, e.g.,
```
[curl//:curl_git]
auto_lock = false
```
MetaBuild will not write the git commit hash into the `META.lock` file anymore, and the `commit` value in the python file will be the reference value. This allows having the specifications for multiple versions of external libraries in a single `META.py` file.

### Conditions for commit

The commit you reference must be reachable from tagged commits, or head of branches. Otherwise, fetching will fail.

When the `commit` refers to a tagged commit or the head of a branch (not just being reachable), MetaBuild can perform faster fetches that only download data for that specific commit. Otherwise, MetaBuild has to fetch the entire repo which is slower.
