---
permalink: /docs/internals/vscode_tips/
title: "VSCode Tips"
toc: true
---

## Connecting to a running docker image

If you have a running docker container, you can use vscode to view and edit files within the container.

To do so install the [remote containers](https://code.visualstudio.com/docs/remote/containers) add-on to visual studio code. Then to the left panel, a new section will be added name "Remote Explorer". If you go into this section, you see all the current running docker containers on your machine. Similar to this.

![image](https://git.corp.adobe.com/storage/user/30871/files/e4add980-00fc-11ec-83e2-cae9349be139)


You can right click on one, and select "Attach to Container". A new vscode window opens, that has access to the filesystem of the container.

## Multi-folder workspace

You can use vscode workspaces to
1. Have multiple folders open in the same instance of vscode.
2. Have configs for vscode that you do not check in, in your repo.

You can find an example of [`metabuild.code-project.example`](https://git.corp.adobe.com/meta-build/meta-build/blob/main/metabuild.code-workspace.example) in the MetaBuild repo.. Make a copy of it and remove the `.example` extension. For example, `metabuild.code-project`. Then you can open it with vscode's `Files > Open Workspace` feature.

You can add custom `launch` commands under the `"launch"` key in this file. You can also add more folders to the workspace under the "folders" key. You can further customize things (font size, python path, etc.) by using the settings under `"settings"` key.

To open a workspace from command-line use
```terminal
code -n -g /path/to/workspace-file
```

## Other useful tips

See [lagrange/DevGuide/VSCode](https://git.corp.adobe.com/pages/lagrange/DevGuide/VSCode/) for other VSCode tips.
