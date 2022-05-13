---
permalink: /docs/internals/default_pfx_key_for_uwp/
title: "Default PFX key for UWP"
---

MetaBuild ships a default [pfx key](https://git.corp.adobe.com/meta-build/meta-build/blob/0.1.501/metabuild/builtin/TemporaryKey.pfx) that is needed for MSVS UWP projects. Visual studio generates this as part of a uwp project template.

In case you need to generate a new file, [here](https://docs.microsoft.com/en-us/windows/win32/appxpkg/how-to-create-a-package-signing-certificate) is the process. We will give a summary below.

Note that the executables `pvk2pfx.exe` and `makecert.exe` might not be on your path. You can find them under `C:\Program Files (x86)\Windows Kits\10\bin\VERSION`. `VERSION` can be a windows sdk installed on your machine, e.g., `10.0.19041.0`.


- Create a CER file
    ```terminal 
    makecert.exe /e "12/31/2100"  MetaBuildDefaultCert.cer /n "CN=adobe"
    ```
- Create a PVK file from it. When prompted for password, leave it empty.
    ```
    makecert.exe /n "CN=adobe" /r /h 0 /eku "1.3.6.1.5.5.7.3.3,1.3.6.1.4.1.311.10.3.13" /e 12/30/2100 /sv MetaBuildDefaultCert.pvk MetaBuildDefaultCert.cer
    ```
- Finally, create the PFX file.
    ```terminal
    pvk2pfx.exe /pvk .\MetaBuildDefaultCert.pvk /spc .\MetaBuildDefaultCert.cer  /pfx .\MetaBuildDefaultCert.pfx
    ```

Note that this is only used as the default file. Apps are expected to provide their own.