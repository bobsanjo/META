---
permalink: /docs/api/action_node/
title: "ActionNode"
---

*Abstract class*

Direct subclasses:

- [genrule]({{ site.baseurl }}{% link _docs/api/genrule.md %})
- [copy_artifacts]({{ site.baseurl }}{% link _docs/api/copy_artifacts.md %})
- [http_upload]({{ site.baseurl }}{% link _docs/api/http_upload.md %})

Inherits all attributes from [OutMetaNode]({{ site.baseurl }}{% link _docs/api/out_meta_node.md %}).

| Attribute | Type | Description |
|-----------|------|-------------|
| `phase` | `"prepare"` or `"build"` | The phase when the action node is going to be executed. If `prepare` is used, then MetaBuld runs the node during the prepare command. If `build` is used, then the node is executed during the build phase inside Xcode or Visual Studio.  Default value is `"build"`. |
| `version` | `string` or `int` | The version number of the action node. You can increment the version to force rebuild the node even when MetaBuild cannot detect any other changes. |
| `cache` | `bool` | MB caches the result of the action nodes and will not try to invoke the command again when no inputs have changed. If you turn it off, the command will always run again without checking for invalidated inputs. This is needed for cases where the command should always update a file based on values that are not easy to validate. Defaults to `true`. |
