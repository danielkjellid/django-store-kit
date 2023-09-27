import pathlib

import rich_click as click

from .. import utils
from ..helpers.text import echo_with_time
from ..helpers.context_managers import action, BulletListIterator
from ..constants import SUPPORTED_LOCALS


@click.group(help="Sub-commands related to translations.")
def translations():
    ...


@translations.command()
def make_translations():
    with action("Discovering project apps..."):
        apps = utils.discover_project_apps()
        apps_with_locale_folder = [
            path
            for path in apps
            if (path / "locale").exists() and (path / "locale").is_dir()
        ]
        apps_mapping = {
            str(path).rsplit("/", 1)[-1]: path for path in apps_with_locale_folder
        }

    apps_without_locale_folder = set(apps) - set(apps_with_locale_folder)
    if apps_without_locale_folder:
        with action(
            "Found following apps without locale folder, will skip these",
            add_icon=False,
            color="yellow",
        ):
            with BulletListIterator(apps_without_locale_folder, color="yellow") as it:
                for app in it:
                    click.echo(app)
    print(
        " -l ".join(SUPPORTED_LOCALS),
    )
    with action("Select app(s) to make translations for", add_icon=False):
        selected_apps = utils.fzf(
            choices=list(apps_mapping.keys()), allow_multiple=True
        )
        with BulletListIterator(selected_apps) as it:
            for app in it:
                click.echo(app)

    locale_args = []
    for locale in SUPPORTED_LOCALS:
        locale_args.append("-l")
        locale_args.append(locale)

    for app in selected_apps:
        with action(f"Making translation in app {app}"):
            utils.run_in_dir(
                "django-admin",
                "makemessages",
                *locale_args,
                folder=apps_mapping[app],
            )


@translations.command()
def compile_translations():
    ...
