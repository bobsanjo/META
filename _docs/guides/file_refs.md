---
permalink: /docs/guides/file_refs/
title: "File References"
---

All file references are relative to the "root directory" of the current Meta module, with the exception of [escaped paths](#escaped-paths).

By default, the "root directory" is set to the parent directory of the current Meta module file.

In order to change the location of the current directory, the `set_root_directory(new_dir : <file_ref>)` can be used to change the root directory for all file references following after this method call.

Note that `set_root_directory` can be used multiple times in the same module.

## Escaped paths

There are certain corner cases where you would want MetaBuild to keep a path relative and not prepend the root directory before using the path. Or conversely, you might want MetaBuild to to prepend the root directory to a string and treat it as a path. In such scenarios, the following functions can be used:

- `absolute_path(value : <file_ref>)`: this tells MetaBuild to leave the path alone (treat it as if it was absolute already) and not prepend the root directory to it. 
- `relative_path(value : <file_ref>)`: this tells MetaBuild to prepend the root directory to a string and treat it as a relative path.

Also, any `$` within the `file_ref` passed to these functions will be left alone and [`value templates`]({{ site.baseurl }}{% link _docs/guides/value_templates.md %}) will not be expanded. In other words, these functions are special cases of [`escaped_value(...)`]({{ site.baseurl }}{% link _docs/guides/value_templates.md %}).

You can see examples of using such escape mechanisms [here](https://git.corp.adobe.com/meta-samples/escaped_values).
