import rich_click as click
import functools
from datetime import datetime
from typing import Any
from ..console import console


DEFAULT_COLOR = "magenta"


def highlight(value: Any):
    return f"[bold cyan]{value}[white]"


def _click_style(text: str, *, color: str):
    return click.style(text, fg=color)


red = functools.partial(_click_style, color="red")
white = functools.partial(_click_style, color="white")
green = functools.partial(_click_style, color="green")


def text_color(color_: str = DEFAULT_COLOR):
    return functools.partial(_click_style, color=color_)


def echo_with_time(value: str, color: str = DEFAULT_COLOR, **kwargs: Any) -> None:
    color = text_color(color)
    _time = f"[{datetime.now():%H:%M:%S}]"
    click.echo(color(f"{_time} {value}"), **kwargs)
