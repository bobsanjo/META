---
permalink: /docs/guides/py_method/
title: "py method"
---

```python
async def my_method(ctx):
    location = await ctx.eval_async("$(location :other_node)")
    ...

genrule(
    ...
    py = my_method
    ...
)
```

## Context object

### `await ctx.eval_async(expr)`

Evaluates the expression using the MB value engine.

### `ctx.eval(expr)`

Same as `ctx.eval_async`, but returns the value without using `await`. Please use the `async` variant as much as possible to allow parallel loading of other projects.

### `await ctx.execute(cmd, ignore_error = False, return_error = False, env = None, cwd = None, show_progress = False, timeout = None)`

Executes the command using `subprocess.Popen`. Note that the command actually executes on a different thread, so it is not blocking the execution of the caller method. As a result, multiple commands can be invoked in parallel using different `ctx.execute` calls.

Using `ctx.execute` allows MB to handle errors and capture the commands in logs automatically.

| Attribute | Type | Description |
|-----------|------|-------------|
| `cmd` | `list<string>` | The command split up into arguments. These are passed directly to `subprocess.Popen` API in Python. |
| `ignore_error` | `bool` | By default MB will catch non zero return values and raise an exception. In some cases the errors are not supposed to break the build, so this parameter allows MB to ignore any errors coming out of executing this command. |
| `return_error` | `bool` | If the command fails, MB raise an exception back to the caller. Use this parameter to make MB return the error instead of raising it. |
| `env` | `dict<string, string>` or `EnvBuilder` | The environment flags to pass down to the command. |
| `cwd` | `string` | The current directory to use. |
| `show_progress` | `bool` | When enabled, MB will use the last line of the output of the command and show it as part of the live progress status table. Internally, MB uses this for most GIT commands that show progress. |
| `timeout` | `float` | Number of seconds the process is allowed to run. If the process does not terminate after timeout seconds a `MetaShellException` is raised. |

### `await ctx.shell(cmd, ignore_error = False, return_error = False, env = None, cwd = None, show_progress = False, timeout = None)`

Same as `ctx.execute` except that the `cmd` is a string and it is passed to a `bash` shell.

Note that on Windows, there's no `bash` shell out of box, so MB will automatically grab a copy of MSYS2 and install it inside the `.adobe_meta_cache` folder.

| Attribute | Type | Description |
|-----------|------|-------------|
| `cmd` | `string` | The command to pass to `bash`. |

### `await ctx.copy(src, dst)`

Copies the `src` file / directory to `dst`.

### `await ctx.move(src, dst)`

Moves the `src` file / directory to `dst`.

### `await ctx.rm(path)`

Removes the file / directory at `path`.

### `await ctx.extract(archive_path, local_path, trim = 0)`

Extracts the `archive_path` to `local_path`. Use `trim` to remove top level folders from the archive.

### `ctx.build_env()`

Creates an `EnvBuilder` object.

## EnvBuilder

Use this object to manipulate env properties before calling `ctx.execute` or `ctx.shell`.

### `env.copy()`

Return a copy of the `EnvBuilder` object.

### `env.get(prop)`

Reads the value from the environment.

### `env.set(prop, value)`

Sets the property in the environment.

### `env.set_props(props)`

Sets all properties inside the provided dictionary.

### `env.filter(check)`

```python
def check(key, value):
    return True
```

Runs the `check` method on all properties. If `check` returns `False` for a property, then that property is removed.

### `env.insert_path(key, path)`

Inserts a new value into the property preserving the platform format of path separation.

```python
env.insert_path("PATH", "/new/path")
```

### `env.filter_paths(key, check)`

```python
def check(path):
    return True
```

Runs the `check` method on all paths of a property. If `check` returns `False` for a path, then that path is removed.
