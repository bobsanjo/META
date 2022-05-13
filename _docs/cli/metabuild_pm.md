---
permalink: /docs/cli/metabuild_pm/
title: "metabuild pm"
---

MB is also a package manager for C++ libraries. This command can be used to clone repositories using the internal package manager of MB.

  metabuild pm clone [package_name] [dest_path]

> [dest_path] is optional. MB creates a folder with the name of the package by default.

Example:

  metabuild pm clone "boringssl == 1.0.4"
