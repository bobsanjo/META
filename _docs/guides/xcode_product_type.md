---
permalink: /docs/guides/xcode_product_type/
title: "Xcode Product Type"
---

The `xcode_product_type` property can be used to change the type of Xcode target.

## Product Types for `cxx_library`

| Product Type | Xcode Product Type | Extension |
|--------------|--------------------|-----------|
| `"library"` (*Default*) | `com.apple.product-type.library.static` or `dynamic` | `.a` or `.dylib` |
| `"framework"` | `com.apple.product-type.framework` | `.framework` |
| `"bundle"` | `com.apple.product-type.bundle` | `.bundle` |
| `"unit_test"` | `com.apple.product-type.bundle.unit-test` | `.xctest` |
| `"ui_test"` | `com.apple.product-type.bundle.ui-testing` | `.xctest` |
| `"metal"` | `com.apple.product-type.metal-library` | `.metallib` |
| `"xpc_service"` | `com.apple.product-type.xpc-service` | `.xpc` |

## Product Types for `cxx_binary`

| Product Type | Xcode Product Type | Extension |
|--------------|--------------------|-----------|
| `"application"` (*Default*) | `com.apple.product-type.application` | `.app` |
| `"tool"` | `com.apple.product-type.tool` | |

When the *deprecated* `cli` property is set to `True`, the `xcode_product_type` is automatically changed to `"tool"`.

## Creating an Xcode Framework

```python
cxx_library(
    name = "MyFramework",

    # Change the product type to framework.
    xcode_product_type = "framework",

    xcode_flags = {
        # Add a bundle id.
        'PRODUCT_BUNDLE_IDENTIFIER': "com.adobe.my-framework"
    },

    xcode_headers = [
        # Add the header to the Public section.
        (target.xcode_public, "MyFramework.h"),

        # Add the header to the Private section.
        (target.xcode_private, "MyFramework_Private.h"),

        # Add the header to the Project section.
        (target.xcode_private, "MyFramework_Project.h"),
    ],

    data = [
        # Copy an asset into the framework resources.
        "FrameworkAssets.txt"
    ],
)

cxx_binary(
    name = "my_app",

    srcs = [
        "my_app.mm"
    ],

    deps = [
        ":MyFramework"
    ],

    xcode_resources = [
        # Add the Xcode Storyboard.
        "Main.storyboard"
    ]
)
```
