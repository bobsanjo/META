---
permalink: /docs/api/http_upload/
title: "http_upload()"
---

```python
http_upload(...)
```

Inherits all attributes from [ActionNode]({{ site.baseurl }}{% link _docs/api/action_node.md %}).

Uploads a file to a remote HTTP service that supports POST-ing files.

It will automatically inject the required Artifactory login headers.

| Attribute | Type | Description |
|-----------|------|-------------|
| `src` | `filename` | The file needed for upload. |
| `url` | `string` | The remote URL where the file is to be uploaded. |

```python

cxx_binary(
    name = "myapp"
)

archive_artifacts(
    name = "myapp_archive",
    deps = [
        # MB automatically creates a list of artifacts from the dependencies list.
        ":myapp"
    ]
)

def _read_version(ctx):
    version_file = ctx.eval_async("$(resolve ./VERSION)")
    with open(version_file, "r") as stream:
        return stream.read()

option(
    name = "build_version",

    # By default read the value from the VERSION file.
    # This is used when the `myapp.build_version` config value
    # is not available.
    py = _read_version,

    # Let the builder manually change the version number if needed.
    config = "myapp.build_version",
)

option(
    name = "enable_upload",
    config = "myapp.enable_upload",
    type = "bool",
    default_value = False
)

http_upload(
    name = "myapp_upload",
    filter = target.option(":enable_upload"),
    src = "$(location :myapp_archive)",
    url = "https://artifactory.corp.adobe.com/my_location/$(option :build_version)/$(config.platform)/" +
        "$(config.type)/$(config.arch)/myapp.zip",
    deps = [
        # Make sure to create the archive before uploading it.
        ":myapp_archive"
    ]
)

group(
    name = "main",
    deps = [
        ":myapp",
        ":myapp_upload",
    ]
)
```

You can invoke this with the following commands. Once the build is finished, MB automatically uploads the archives.

```shell
metabuild prepare --define myapp.enable_upload=true --define myapp.build_version=CustomBuild1.0.0
metabuild build
```
