---
permalink: /docs/api/out_meta_node/
title: "OutMetaNode"
---

*Abstract class*

This is the base node type used by targets that generate or download files on disk. By default these targets automatically allocate a folder in the build directory. However, the `out` attribute can be used to customize the output folder.

Direct subclasses:

- [project_link()]({{ site.baseurl }}{% link _docs/api/project_link.md %})
- [git_checkout()]({{ site.baseurl }}{% link _docs/api/git_checkout.md %})
- [http_archive()]({{ site.baseurl }}{% link _docs/api/http_archive.md %})
- [http_file()]({{ site.baseurl }}{% link _docs/api/http_file.md %})
- [cxx_header_map()]({{ site.baseurl }}{% link _docs/api/cxx_header_map.md %})
- [ActionNode]({{ site.baseurl }}{% link _docs/api/action_node.md %})
- [CxxNode]({{ site.baseurl }}{% link _docs/api/cxx_node.md %})

**Note:** By default the `out` attribute should only be used for extraordinary cases where no other solution is available. Otherwise, let MetaBuild automatically allocate a folder for the target.
{: .notice--warn}

Inherits all attributes from [SharedNode]({{ site.baseurl }}{% link _docs/api/shared_node.md %}).

| Attribute | Type | Description |
|-----------|------|-------------|
| `out` | [`file_ref`]({{ site.baseurl }}{% link _docs/guides/file_refs.md %}) | Defaults to an automatically generated path. Use this to customize the location where the content is generated / downloaded. |
