---
permalink: /docs/api/glob/
title: "glob()"
---

```python
group(...)
```

| Attribute | Type | Description |
|-----------|------|-------------|
| `include` | `list<glob_pattern>` or `glob_pattern` | Include glob patterns. If a file matches any of the `glob_patterns`, then the file is included in the resulting list. If no pattern is specified, then all files are considered recursively. |
| `exclude` | `list<glob_pattern>` or `glob_pattern` | Exclude glob patterns. If a file matches any of the `glob_patterns`, then the file is excluded from the resulting list. |
| `exclude_directories` | `bool` | Defaults to `True`. When set to `True`, the method removes the matching directory entries from the resulting list. |
| `exclude_files` | `bool` | Defaults to `False`. When set to `True`, the method removes the matching file entries from the resulting list. |
| `exts` | `list<string>` | Defaults to `None`. List of extensions to look for. |
| `filters` | `list<filter_tuples>` | Defaults to `None`. List of filter tuples to apply on the resulting list. |
| `root_dir` | [`file_ref`]({{ site.baseurl }}{% link _docs/guides/file_refs.md %}) | Defaults to the root directory of the current module. Use this attribute to change the start point of the glob search. |

**Note on exclude**: The exclude patterns should either start with a `*` or have an absolute form. E.g., `/src/rendering/draco.h` or `*src/rendering/draco.h`. They will be appended to the current root directory (this is slightly different from normal behaviour of file references, see [`file_ref`]({{ site.baseurl }}{% link _docs/guides/file_refs.md %})). This is a measurement needed so that the patterns match the path inside the repo and it will not matter where the file is actually checked out. This is needed because of patterns like `*/test/*`. In this case the test folder could match anything in the path, so the builds were breaking when somebody used a folder like `/Users/test/code/...` to checkout MB projects.


## Glob Patterns

MetaBuild uses the [glob2](https://github.com/miracle2k/python-glob2) package to implement glob operations. Check the [documentation of glob2](https://github.com/miracle2k/python-glob2#python-glob2) for more details on supported glob operations.

## Filtering results

Most projects define a convention on how files used on a specific platform are separated via either a custom path or the file name format. For example, in UXP all files targeting "ios" are separated under "ios" subfolders.

In order to avoid writing multiple glob operations for the same folder, we can do a single glob pass and then identify subsets of files that match specific platform criteria.

The following example is adding platform files based on their containing directory.

Note that we are using the [cpp_glob]({{ site.baseurl }}{% link _docs/api/cpp_glob.md %}), which is an alias for glob that defines `ext` to a set of well known `C++` extensions.
{: .notice--info}

```python
cxx_binary(
    name = "my_exe",
    srcs = [
        # Note that by default if `include`
        # is omitted, all the files under
        # the root folder are considered
        # for the glob search.
        cpp_glob(filters = [
            # All folders under "win" subfolders will only
            # be compiled on Windows.
            (target.windows, "*/win/*"),

            # All folders under "ios" subfolders will only
            # be compiled on iOS.
            (target.ios, "*/ios/*")

            # All folders under "macos" subfolders will only
            # be compiled on MacOS.
            (target.macos, "*/macos/*")

            # All folders under "android" subfolders will only
            # be compiled on Android.
            (target.android, "*/android/*")
        ])
    ]
)
```

## Debugging Trick

If you want to debug your glob pattern, you can use this pattern to print what it resolves to.

```py
async def _debug_helper(ctx):
    # Don't use this in final code, it will reduce MetaBuild performance
    import json
    glob_object = glob(<my_pattern>)
    resolved_values = await ctx.eval_list_async(glob_object)
    log.info("Globbed values are: ", json.dumps(resolved_values, indent = 4))

cxx_library(
    srcs = _debug_helper, # instead of glob(<my_pattern>)
)
```

You can even add extra protective measures to your glob
```python

# Define a wrapper function (e.g. in common.meta.py)
async def aero_glob(*args, **kwargs):
   async def aero_glob_impl(ctx):
      result = glob(*args, **kwargs)
      # Debug code
      resolved_result = await ctx.eval_list_async(result)
      if not resolved_result:
         raise_meta_exception("Empty glob....")
      # just return the smart glob object again
      return result
   return aero_glob_impl


# Usage
load("//common", "aero_glob")

cxx_library(
    ...
    srcs = [
       aero_glob(...),
    ],   
    ...
)
```
