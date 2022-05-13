---
permalink: /docs/guides/xcode_plist/
title: "Xcode Plist Files"
---

An [information property list file (plist)](https://developer.apple.com/library/archive/documentation/General/Reference/InfoPlistKeyReference/Articles/AboutInformationPropertyListFiles.html) is a structured text file that contains essential configuration information for a bundled executable. By default the name of an information property list file is `Info.plist` and they are used by Apple, primarily on macOS and iOS.

MetaBuild generates a plist file with the default values stored in [PlistDefaults.py](https://git.corp.adobe.com/meta-build/meta-build/blob/main/metabuild/generator/xcode/PlistDefaults.py), and it further you to customize the content of this file via the `xcode_plist =` property to `cxx_binary()`.
```py
cxx_binary(
    ...
    xcode_plist = {
        "NSAppTransportSecurity": {
            "NSAllowsArbitraryLoads": True,
        },
        "NSMainStoryboardFile": "Main",
        "NSRequiresAquaSystemAppearance": True,
        "NSPrincipalClass": [
            (target.ios, "UIApplication"),
            (target.macos, "NSApplication"),
        ],
        "CFBundleName": "Torq Native",
        "CFBundleShortVersionString": "$(option //artifactory:build_version)",
        "CFBundleVersion": "$(option //artifactory:build_version)",
    },
)
```

If you are working on a project that is transitioning to MB and already has a plist file, you can ask MB to use that file instead of generating one. However, it is recommended that you eventually use `xcode_plist =` and stop using the generated file. This will allow you to keep all the information in the same place, and leverage MetaBuild's filters (e.g., target.ios, target.macos) to reduce duplicate information.

```py
cxx_binary(
    xcode_flags = {
        "INFOPLIST_FILE" : "path/to/generated.plist",
    }
)
```

This is how a generated plist file can look like.

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
    <dict>
        <key>BuildMachineOSBuild</key>
        <string>19E287</string>
        <key>CFBundleDevelopmentRegion</key>
        <string>en</string>
        <key>CFBundleExecutable</key>
        <string>copy_artifacts_app</string>
        <key>CFBundleIdentifier</key>
        <string>com.adobe.meta_build.copy_artifacts_app</string>
        <key>CFBundleInfoDictionaryVersion</key>
        <string>6.0</string>
        <key>CFBundleName</key>
        <string>copy_artifacts_app</string>
        <key>CFBundlePackageType</key>
        <string>APPL</string>
        <key>CFBundleShortVersionString</key>
        <string>1.0</string>
        <key>CFBundleSupportedPlatforms</key>
        <array>
            <string>MacOSX</string>
        </array>
        <key>CFBundleVersion</key>
        <string>1</string>
        <key>DTCompiler</key>
        <string>com.apple.compilers.llvm.clang.1_0</string>
        <key>DTPlatformBuild</key>
        <string>12C33</string>
        <key>DTPlatformName</key>
        <string>macosx</string>
        <key>DTPlatformVersion</key>
        <string>11.1</string>
        <key>DTSDKBuild</key>
        <string>20C63</string>
        <key>DTSDKName</key>
        <string>macosx11.1</string>
        <key>DTXcode</key>
        <string>1230</string>
        <key>DTXcodeBuild</key>
        <string>12C33</string>
        <key>LSMinimumSystemVersion</key>
        <string>10.12</string>
        <key>NSHumanReadableCopyright</key>
        <string>Copyright © 2020 Adobe Inc. All rights reserved.</string>
        <key>NSPrincipalClass</key>
        <string>NSApplication</string>
    </dict>
</plist>
```
