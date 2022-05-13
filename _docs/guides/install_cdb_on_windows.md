---
permalink: /docs/guides/install_cdb_on_windows/
title: "Installing CDB on Windows"
---

For projects that require debugging with CDB, MetaBuild assumes it is already installed on your machine.
CDB comes as part of Windows 10 SDK, but it needs a little extra work to install.

1. Install the Windows SDK version that you need from the Visual Studio Installer (e.g., Windows Software Development Kit XX.XX.XX.XX)
2. Then go into `Apps & Features` in the Windows Control Panel (you can also use the search feature in the windows panel to find `Add or Remove Programs`), then search for `Windows Software Development Kit` with the desired version. Then click `Modify`. 
3. Select Change, and make sure `Debugging Tools for Windows` is selected. Then click next, and it should install CDB for the selected version of the Windows SDK.

CDB usually goes into `C:\Program Files (x86)\Windows Kits\10\Debuggers\x64` after installation.

Make sure the version of CDB is at least `10.0.16299.15`.

![](https://git.corp.adobe.com/storage/user/30871/files/9e177d00-880b-11ec-82c8-41e6a9892f31)
