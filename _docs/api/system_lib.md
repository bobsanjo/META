---
permalink: /docs/api/system_lib/
title: "system_lib()"
---

```python
system_lib(name : <string>)
system_lib.framework(name : <string>, delay_load : <bool> = False)
system_lib.sdk(name : <string>)
system_lib.nuget(name : <string>)
```

Use `system_lib()` to point to a system provided library.

For Xcode System frameworks you can use `system_lib.framework()` to differentiate from regular libraries. Xcode system frameworks support delay loading (weak linking).

Examples:

```python
cxx_binary(
    name = "my_exe",
    linker_libraries = [
        (target.apple, [
            # Linking with the CoreFoundation framework.
            system_lib.framework("CoreFoundation"),

            # Linking with the Cocoa framework as delay loaded (optional). If it is missing 
            # but not used, the app the app can still launch
            system_lib.framework("Cocoa", delay_load = True),

            # Linking with a system provided `.tbd` file.
            system_lib("libcompression.tbd"),
        ),
        (target.windows, [
            # Linking with Shell32 on Windows.
            system_lib("Shell32.lib"),
        ])
    ]
)
```

## Windows SDKs references

A project may need to link to system libraries from the Windows SDKs. In order to figure out the name of the reference, add it by hand in Visual Studio then open the project in a raw text editor and look it up in the XML file. Copy the name into the MB specification as a call to `system_lib.sdk()` method.  

Example:

```python
linker_libraries = [
    system_lib.sdk("CppUnitTestFramework.Universal, Version=$(UnitTestPlatformVersion)")
]
```

## Windows Nuget packages

Reference the nuget package by name from the Python spec then add the nuget link in the META.lock file:

The `nuget` and `sdk` methods don't support the `delay_load` parameter.

Example:

```python
linker_libraries = [
    system_lib.nuget("Microsoft.WinUI")
]
```

META.lock

```
[nuget Microsoft.WinUI]
version = 3.0.0-preview2.200713.0
url = https://www.nuget.org/api/v2/package/Microsoft.WinUI/3.0.0-preview2.200713.0
sha256 = 678ed6f3c862b81f2607bc1f239bec19f388b3100d97ea459641269511e46cfd
```
