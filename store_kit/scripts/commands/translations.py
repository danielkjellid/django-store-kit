import pathlib

import rich_click as click
from rich_click.rich_click import Panel, _get_rich_console, Table

from .. import utils
from ..helpers.text import echo_with_time
from ..helpers.context_managers import action, BulletListIterator
from ..constants import SUPPORTED_LOCALS
from ..console import console
from ..helpers.text import highlight
import logging
from rich.text import Text
from rich.logging import RichHandler
from rich.progress import (
    Progress,
    TimeElapsedColumn,
    RenderableColumn,
    TextColumn,
    BarColumn,
    TaskProgressColumn,
    TimeRemainingColumn,
)
from collections import deque
from time import sleep
from rich.padding import Padding
from time import monotonic
from datetime import datetime


@click.group(help="Sub-commands related to translations.")
def translations():
    ...


@translations.command()
def test():
    console.log("Started making translations")

    with action("Discovering project apps with translations"):
        translated_apps, untranslated_apps = discover_apps_with_translations()
        (
            translated_apps_mapping,
            untranslated_apps_mapping,
        ) = get_apps_with_translations_mapping(translated_apps, untranslated_apps)

        console.log(f"Discovered {len(translated_apps)} translated apps.")

        if untranslated_apps:
            console.log_warning(
                f"Some apps is missing translations - these apps will be skipped: \n"
                f"{highlight(' '.join(untranslated_apps_mapping.keys()))}"
            )

    with action("Select apps to make translations for"):
        selected_apps = utils.fzf(
            choices=list(translated_apps_mapping.keys()), allow_multiple=True
        )

    with action(f"Selected apps."):
        console.log(f"Selected {len(selected_apps)} apps.")

    locale_args = []
    for locale in SUPPORTED_LOCALS:
        locale_args.append("-l")
        locale_args.append(locale)

    with action("Making translations for apps"):
        with Progress(
            RenderableColumn(Padding("", (0, 0, 0, 10))),
            BarColumn(),
            TaskProgressColumn(),
            TimeElapsedColumn(),
            expand=False,
        ) as progress:
            task = progress.add_task("", total=len(selected_apps))
            queue = deque(selected_apps)

            while len(queue):
                current_task = queue.popleft()
                progress.advance(task, advance=0.2)

                utils.run_in_dir(
                    "django-admin",
                    "makemessages",
                    *locale_args,
                    folder=translated_apps_mapping[current_task],
                )
                progress.advance(task, advance=0.7)
                progress.advance(task, advance=0.1)


@translations.command()
@click.option("--all-apps", required=False, default=False)
def make_translations(all_apps: bool):
    table = Table(highlight=True, show_header=True, expand=True)
    table.add_row("Test1")
    console.log("Starting")
    # console.print(Panel(table, title="Testing"))
    with action("Discovering project apps with translations..."):
        (
            apps_with_locale_folder,
            apps_without_locale_folder,
        ) = discover_apps_with_translations()
        apps_mapping = {
            str(path).rsplit("/", 1)[-1]: path for path in apps_with_locale_folder
        }

    if apps_without_locale_folder:
        with action(
            "Found following apps without locale folder, will skip these",
            add_icon=False,
            color="yellow",
        ):
            with BulletListIterator(apps_without_locale_folder, color="yellow") as it:
                for app in it:
                    click.echo(app)

    if not all_apps:
        with action("Select app(s) to make translations for", add_icon=False):
            selected_apps = utils.fzf(
                choices=list(apps_mapping.keys()), allow_multiple=True
            )
            with BulletListIterator(selected_apps) as it:
                for app in it:
                    click.echo(app)
    else:
        selected_apps = list(apps_mapping.keys())

    locale_args = []
    for locale in SUPPORTED_LOCALS:
        locale_args.append("-l")
        locale_args.append(locale)

    for app in selected_apps:
        with action(f"Making translation in app {app}..."):
            utils.run_in_dir(
                "django-admin",
                "makemessages",
                *locale_args,
                folder=apps_mapping[app],
            )


@translations.command()
def compile_translations():
    with action("Discovering project apps with translations..."):
        apps_with_locale_folder, _ = discover_apps_with_translations()

    with action("Select app(s) to compile translations for."):
        ...


def discover_apps_with_translations():
    apps = utils.discover_project_apps()
    translated_apps = [
        path
        for path in apps
        if (path / "locale").exists() and (path / "locale").is_dir()
    ]
    untranslated_apps = set(apps) - set(translated_apps)

    return translated_apps, untranslated_apps


def get_apps_with_translations_mapping(
    translated_apps: list[pathlib.Path], untranslated_apps: list[pathlib.Path]
):
    translated_apps_mapping = {
        get_app_name_from_path(path): path for path in translated_apps
    }
    untranslated_apps_mapping = {
        get_app_name_from_path(path): path for path in untranslated_apps
    }

    return translated_apps_mapping, untranslated_apps_mapping


def get_app_name_from_path(path: pathlib.Path):
    return str(path).rsplit("/", 1)[-1]
