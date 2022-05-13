"""Websit management tasks."""

import shutil
import sys
from typing import List, Final
from pathlib import Path

import invoke

JEKYLL_VERSION = "3.8"

EXTRA_ARGS : List[str] = []
if sys.platform.startswith("win"):
    # https://github.com/microsoft/WSL/issues/216
    # this is not efficient at all, but seems to be only way to
    # get things working on windows.
    EXTRA_ARGS.append('--force_polling')

ROOT : Final = Path(__file__).absolute().parent

def get_base_docker_command() -> List[str]:
    return [
        "docker",
        "run",
        "--rm",
        f"--volume={ROOT}:/srv/jekyll",
        f"--volume={ROOT}/vendor/bundle:/usr/local/bundle",
        "--publish",
        "4000:4000",
        f"jekyll/jekyll:{JEKYLL_VERSION}",
    ]


@invoke.task
def serve(ctx):
    """Serves auto-reloading blog via Docker."""
    docker_command = get_base_docker_command()
    docker_command.extend(["jekyll", "serve", *EXTRA_ARGS])
    ctx.run(" ".join(docker_command))



@invoke.task
def clean(ctx):
    """Cleans build and vendor directories."""
    shutil.rmtree(ROOT / "_site", ignore_errors=True)
    shutil.rmtree(ROOT / "vendor", ignore_errors=True)


@invoke.task
def update_dependencies(ctx):
    """Updates blog's Ruby Gems."""
    docker_command = get_base_docker_command()
    docker_command.extend(["/bin/bash", "-ctx", "'bundle update'"])
    ctx.run(" ".join(docker_command))