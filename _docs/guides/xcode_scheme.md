---
permalink: /docs/guides/xcode_scheme/
title: "Xcode Scheme"
---

  Certain xcode configuration are written to `*.xcscheme` files. For example, most of the configurations where you can access in xcode's `Edit Scheme` page.

![](https://git.corp.adobe.com/storage/user/30871/files/a573c900-577d-11ec-8b0d-11557cbcdb75)

MetaBuild allows you to configure these values via the `xcode_scheme =` field of a `cxx_binary`. We pass the values inside the `xcode_scheme` field almost directly to xcode, so to find the correct values to pass to xcode, you can make the edit on xcode GUI first, then see the effect it makes in the corresponding xcscheme file, and then finally replicate it in the `xcode_scheme` field.

For example, let's see how to enable the `Thread Sanitizer`. 
- First, select the scheme for the binary or group you want to edit and click on edit schemes    
  ![](https://git.corp.adobe.com/storage/user/30871/files/59755400-577e-11ec-9a2c-49c61ae085fb)
- Then check the `Thread Sanitizer` check box. Save the project in xcode.
- Then open the `xcscheme` corresponding to your binary. You can find it by running `find . -name '*.xcscheme` inside the repository for example. In my case, it is `./dist/xcode_macos/project/spdlog.xcodeproj/xcshareddata/xcschemes/spdlog_app_test.xcscheme`, and see what changed in the file, in this case 
  ```
  <LaunchAction
  ...
  enableThreadSanitizer = "YES"
  ```
- Go ahead and put `xcode_scheme = { "LaunchAction": { "enableThreadSanitizer": True } }` in the xcode_scheme. Next time you run `metabuild prepare` this value will be automatically checked.

Note that passing values for `xcode_scheme` only edits the scheme corresponding the calling `cxx_library()` or `cxx_binary()`, and not the other schemes.
