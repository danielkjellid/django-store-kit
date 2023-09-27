import rich_click as click

from .commands import translations

click.rich_click.USE_RICH_MARKUP = True


@click.group()
def cli() -> None:
    ...


cli.add_command(translations.translations)
