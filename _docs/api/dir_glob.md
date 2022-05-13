---
permalink: /docs/api/dir_glob/
title: "dir_glob()"
---

```python
dir_glob(...)
```

Alias for [`glob()`]({{ site.baseurl }}{% link _docs/api/glob.md %}) that automatically sets `exclude_directories = False` and  `exclude_files = True`.

| Attribute | Type | Description |
|-----------|------|-------------|
| `include` | `list<glob_pattern>` or `glob_pattern` | Include glob patterns. If a file matches any of the `glob_patterns`, then the file is included in the resulting list. If no pattern is specified, then all files are considered recursively. |
| `exclude` | `list<glob_pattern>` or `glob_pattern` | Exclude glob patterns. If a file matches any of the `glob_patterns`, then the file is excluded from the resulting list. |
| `filters` | `list<filter_tuples>` | Defaults to `None`. List of filter tuples to apply on the resulting list. |
| `root_dir` | [`file_ref`]({{ site.baseurl }}{% link _docs/guides/file_refs.md %}) | Defaults to the root directory of the current module. Use this attribute to change the start point of the glob search. |
