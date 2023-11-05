import os
from pathlib import Path
import subprocess
from .constants import PROJECT_DIR
import rich_click as click
import tempfile
import pathlib
from typing import Any
import sys


def run_in_background(*args: str | pathlib.Path, **kwargs: Any):
    return subprocess.Popen(args, **kwargs)


def run_in_dir(*args: str | pathlib.Path, folder: str | pathlib.Path):
    return subprocess.Popen(args, cwd=folder, stdout=subprocess.DEVNULL)


def interact(command: str | pathlib.Path, *args: str, env=None) -> None:
    """
    Run a sub-command interactively.
    """

    env = os.environ | (env or {})
    process = subprocess.run([command, *args], check=False, shell=False, env=env)

    if process.returncode != 0:
        print(f"An error occurred while executing {[command, *args]}", file=sys.stderr)
        sys.exit(process.returncode)


def fzf(
    choices: list[str],
    fzf_options: str = "",
    allow_multiple: bool = False,
    allow_new_input: bool = False,
    allow_none: bool = False,
) -> str | None:
    """
    Spawn fzf select and select between 'choices'.
    """

    choices.sort(reverse=True)

    if allow_none:
        choices.append("None")
    if allow_new_input:
        choices.append("Give me a prompt instead")

    choices_str = "\n".join(map(str, choices))

    if not _fzf_available():
        click.echo(click.style("fzf is not installed", fg="red"))
        click.echo(choices_str)
        choice = click.prompt("Pick one")
        return choice

    with tempfile.NamedTemporaryFile() as input_file:
        with tempfile.NamedTemporaryFile() as output_file:
            input_file.write(choices_str.encode("utf-8"))
            input_file.flush()

            interact(
                "sh",
                "-c",
                f"cat {input_file.name} | fzf {'-m' if allow_multiple else ''} --height 1 {fzf_options} > {output_file.name}",
            )

            with open(output_file.name) as f:
                selection = f.read().strip("\n")

                if allow_multiple:
                    selection = selection.splitlines()

    if selection == "None":
        return None
    if selection == "Give me a prompt instead":
        return click.prompt("New value")

    return selection


def _fzf_available() -> bool:
    if check_exit_code("fzf", "--version"):
        return True
    return False


def check_exit_code(command: str, *args: str) -> bool:
    """
    Try to execute a command. Returns True if the command succeeds.
    """

    try:
        subprocess.run([command, *args], check=True, capture_output=True)
        return True
    except Exception:
        return False


def discover_project_apps() -> list[Path]:
    """
    Utility function to discover django apps inside project.
    """

    apps = []
    project_sub_folders = PROJECT_DIR.iterdir()

    for folder in filter(Path.is_dir, project_sub_folders):
        apps_path = folder / "apps.py"

        if apps_path.exists():
            apps.append(folder)

    return apps
