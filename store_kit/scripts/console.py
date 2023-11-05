from rich_click.rich_click import _get_rich_console, ALIGN_ERRORS_PANEL

from rich.panel import Panel
from typing import Any


def format_warning(content: Any):
    console.print()
    console.log(
        Panel(
            content,
            border_style="yellow",
            title="[yellow] Warning",
            title_align=ALIGN_ERRORS_PANEL,
            expand=True,
            highlight=True,
        )
    )
    console.print()


console = _get_rich_console()
console.log_warning = format_warning
