---
permalink: /docs/api/xcode_rule/
title: "xcode_rule()"
---

```python
xcode_rule(...)
```

Inherits all attributes from [MetaNode]({{ site.baseurl }}{% link _docs/api/meta_node.md %}).

An xcode_rule() is MetaBuild's API to create [xcode build rules](https://developers.google.com/j2objc/guides/xcode-build-rules). An xcode build rule tells xcode how to handle different file types within a target.


| Attribute | Type | Description |
|-----------|------|-------------|
| `compiler_spec` | `string` | Type of compiler or tool used to process the files|
| `file_type` | `string` | |
| `file_patterns` | `list<string>` | |
| `script` | `list<string>` | Bash script that can process the input file  |
| `input_files` | `list<`[`file_ref`]({{ site.baseurl }}{% link _docs/guides/file_refs.md %})`>` |  |
| `output_files` | `list<`[`file_ref`]({{ site.baseurl }}{% link _docs/guides/file_refs.md %})`>` |  |
| `is_editable` | `bool` |  |
| `needs_legacy_build_system` | `bool` | If true, any target inheritting from this rule will use the legacy build system. |

__Some notes__

- All the values `compiler_spec`, `file_type`, `file_patterns`, `script`, `input_files`, `output_files`, and `is_editable` are internal Xcode values and are directly passed to Xcode. To find the proper values for this inputs, you can create an Xcode project, and use Xcode UI to create custom rules within this project. Then open the file `[yourproject].xcodeproj/project.pbxproj` with a text editor and look for the text `PBXBuildRule`. You can then just use the exact same values when calling MetaBuild's `xcode_rule`. 
- The field `output_files` will make any relative path absolute before passing them to Xcode (relative to the to the output location folder that MetaBuild creates for the `xcode_rule` object). If you want to keep the value relative while passing it to Xcode, wrap the value within [`absolute_path()`]({{ site.baseurl }}{% link _docs/guides/file_refs.md %}#escaped-paths).
- If you want to use the legacy build system for all your project, and not just some targets, you can use the following xcode option `xcode.needs_legacy_build_system = true` (using the MetaBuild lock file).


## Example

- [Using the intel compiler](https://git.corp.adobe.com/meta-samples/mb_intel/blob/master/META.py)
- Using a custom compiler (nasm) for compiling `.asm` files.
    ```python
    http_file(
        name = 'nasm_binary',
        url = '/nasm/binary/url',
    )
    xcode_rule(
        name = "compile_asm_xcode",
        compiler_spec = 'com.apple.compilers.proxy.script',
        file_patterns = '*.asm',
        file_type = 'pattern.proxy',
        is_editable = '1',
        script = [
            # The rule can access xcode variables created by the target
            # this can be used to communicate information from the target to the rule
            'echo I can access CUSTOM_FLAG = ${CUSTOM_FLAG}\n',
            '$(location :nasm_binary) -Xgnu -f macho64 -F dwarf -o ${OBJECT_FILE_DIR}/${CURRENT_ARCH}/${INPUT_FILE_BASE}.o ${INPUT_FILE_PATH}',
        ],
        output_files = '${OBJECT_FILE_DIR}/${CURRENT_ARCH}/${INPUT_FILE_BASE}.o',
    )

    cxx_library(
        ...
        deps = [
            # add the rule as a dependency to have it applied to the library (or binary)
            ':compile_asm_xcode'
        ],
        xcode_flags = {
            # The rule can access xcode variables created by the target
            'CUSTOM_FLAG' : '12',
        }
    )
    ```

