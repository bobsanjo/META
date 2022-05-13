---
permalink: /docs/api/meta_policy/
title: "meta_policy()"
---

```python
meta_policy(...)
```

Inherits all attributes from [MetaNode]({{ site.baseurl }}{% link _docs/api/meta_node.md %}).

| Attribute | Type | Description |
|-----------|------|-------------|
| `on_http_request` | [`<py method>`]({{ site.baseurl }}{% link _docs/guides/py_method.md %}) | Callback invoked when MB needs to make an HTTP request (ie. HEAD, GET or PUT). |
| `on_git_request` | [`<py method>`]({{ site.baseurl }}{% link _docs/guides/py_method.md %}) | Callback invoked when MB needs to run `git fetch` or `git ls-remote` commands. |
| `on_git_resolved_commit` | [`<py method>`]({{ site.baseurl }}{% link _docs/guides/py_method.md %}) | Callback invoked when MB resolved the actual commit to be used for a repo. The repo is already downloaded at this time and the host can validate the downloaded repository and commit. |

This node can be used to install hooks when MetaBuild is executing various network requests. For example, a specification can inject a `meta_policy` that intercepts all the HTTP requests and validates if a request is allowed or not.

### Installing a meta policy

A `meta_policy` node must be linked using the `mb.policy` property in order to activate it. The CLI `--define mb.policy=:my_project_policy` or the `META.lock` file can be used for this purpose.

**Note:** Only the root project will run the policy hooks. Downstream projects do not run their own policies.

Note that the policy linked from the `mb.policy` can be a `group()` node, so that multiple policies can be installed at once.

All policies activate at once. That means no hooks are called while resolving the policy list. If a policy is loaded from a remote project, then no policy can catch that initial fetch.

### Example

#### META.lock
```ini
[mb]
policy = :my_project_policy
```

#### META.py

```python

def on_http_request_callback(ctx):
    if "artifactory.corp.adobe.com" not in ctx.request.url:
        raise Exception("Unexpected HTTP request URL: " + ctx.request.url)

meta_policy(
    name = "my_project_policy",
    on_http_request = on_http_request_callback
)
```

### Context Object

All the methods get a [`<Context Object>`]({{ site.baseurl }}{% link _docs/guides/py_method.md %}) object as their only argument. The context has a property `ctx.request` that can be used to identify the actual outgoing request. The callbacks can either change the `ctx.request` properties in case the URLs must be patched or fail the build by raising an exception.

| Attribute | Type | Description |
|-----------|------|-------------|
| `ctx.request` | `HttpRequest | GitRequest | GitResolvedRequest` | Each callback has a different request type |


#### HttpRequest

The `ctx.request` property is of type `HttpRequest` when the `on_http_request` callback is invoked.

| Attribute | Type | Description |
|-----------|------|-------------|
| `ctx.request.source` | `RequestSource` | Specification about the initiator of this request. Read only. |
| `ctx.request.method` | `string` | Possible values: `"HEAD"`, `"GET`" or `"PUT"`. Read only. |
| `ctx.request.url` | `string` | URL of the outgoing request. The policy callback can change this property. |
| `ctx.request.headers` | `Dict[string, string]` | Dictionary of headers. The policy callback can change this property. **NOTE:** MB automatically injects the required artifactory keys after the policy method is invoked depending the final URL of the request.  |
| `ctx.request.sha256` | `string` | The expected sha256 for the file. The policy callback can change this property. |
| `ctx.request.payload_file` | `string` | The file to be uploaded to the remote URL. Read only. |

#### GitRequest

The `ctx.request` property is of type `GitRequest` when the `on_git_request` callback is invoked.

| Attribute | Type | Description |
|-----------|------|-------------|
| `ctx.request.source` | `RequestSource` | Specification about the initiator of this request. Read only. |
| `ctx.request.type` | `GitRequestType` | Type of GIT request. Read only. |
| `ctx.request.repo` | `string` | GIT Repository URL. The policy callback can change this property. |
| `ctx.request.commit` | `string` | Commit or branch requested in the checkout. The policy callback can change this property. Can be null. |
| `ctx.request.commit_hash` | `string` | Actual commit hash hard coded in the META.lock. The policy callback can change this property. Can be null. |
| `ctx.request.set_refname(branch_name)` | `method` | Changes the ref name, MB will resolve this ref name to an actual commit hash using git commands. |
| `ctx.request.set_sha1(sha1)` | `method` | Changes the actual commit sha1. MB will use this sha1 without trying to resolve to an actual commit. |

##### GitRequestType enum

| Type      | Description |
|-----------|-------------|
| `git_request_type.FETCH` | GIT fetch request. |
| `git_request_type.LS_REMOTE` | GIT ls-remote request. |


#### GitResolvedRequest

The `ctx.request` property is of type `GitResolvedRequest` when the `on_git_resolved_commit` callback is invoked. In general this callback can only be used for logging and validation purposes.

| Attribute | Type | Description |
|-----------|------|-------------|
| `ctx.request.source` | `RequestSource` | Specification about the initiator of this request. Read only. |
| `ctx.request.path` | `string` | Path on disk where the GIT repo has been fetched. Read only. |
| `ctx.request.repo` | `string` | GIT Repository URL. Read only. |
| `ctx.request.commit` | `string` | Actual commit sha1 that has been fetched. Read only. |

#### RequestSource

| Attribute | Type | Description |
|-----------|------|-------------|
| `ctx.request.source.type` | `RequestType` | Type of request. Read only. |
| `ctx.request.source.node` | [`MetaNode`]({{ site.baseurl }}{% link _docs/api/meta_node.md %}) | Source node, can be null. Read only. |
| `ctx.request.source.module` | `MetaModule` | Source module, can be null. Read only. |
| `ctx.request.source.project` | `MetaProject` | Source project, can be null. Read only. |
| `ctx.request.source.target_config` | `TargetConfig` | The target configuration that initiated this request. Read only. |

##### RequestType enum

| Type      | Description |
|-----------|-------------|
| `request_type.HTTP_ARCHIVE` | Issued by an `http_archive()` node. |
| `request_type.HTTP_FILE` | Issued by an `http_file()` node. |
| `request_type.HTTP_UPLOAD` | Issued by an `http_upload()` node. |
| `request_type.CODEX_QUERY` | Issued by a `codex_query()` node. |
| `request_type.PROJECT_LINK` |  Issued by a `project_link()` node. |
| `request_type.GIT_CHECKOUT` |  Issued by a `git_checkout()` node. |
| `request_type.VALUE_EXPRESSION` | Issued by an HTTP expression (ie. `${http url}`). |
| `request_type.META_LIBS` | MB downloads the `meta-libs` GIT repository. |
| `request_type.BIN_CACHE_SOURCE` | Issued by the binary cache system (work in progress). |
| `request_type.CLI_SOURCE` | Issued by the a command line invocation. |
| `request_type.NUGET_PKG` | Issued by the a NuGet package. |
| `request_type.NUGET_BIN` | MB downloads the NuGet.exe. |
| `request_type.ANDROID_NDK` | MB downloads the Android NDK. |
| `request_type.CMAKE_BIN` | MB downloads the Cmake toolchain. |
| `request_type.CMAKE_VERSIONS` | MB downloads the list of Cmake versions. |
| `request_type.MSYS_BIN` | MB downloads the Msys installer. |
| `request_type.NINJA_BIN` | MB downloads the Ninja executable. |
| `request_type.NINJA_LATEST` | MB downloads the latest version of Ninja. |
| `request_type.NODEJS_BIN` | MB downloads the NodeJS installer. |
| `request_type.NODEJS_VERSIONS` | MB downloads the NodeJS versions. |
| `request_type.VSWHERE_BIN` | MB downloads the VSWhere.exe from Microsoft. |
| `request_type.EMSDK_GIT` | MB downloads the `meta-libs` GIT repository. |
| `request_type.BREW_GIT` | MB downloads the `Homebrew` GIT repo. |
| `request_type.INTERNAL_REQUEST` | Internal request type used only in MB unit tests. |
