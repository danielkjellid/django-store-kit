from contextlib import contextmanager

import rich_click as click
from .text import echo_with_time, text_color, DEFAULT_COLOR
from ..console import console
from typing import Sequence, Any
import rich_click as click
from rich.progress import Progress
from rich_click.rich_click import rich_format_error
from collections import deque


@contextmanager
def action(text: str, *, add_icon: bool = True, color: str = DEFAULT_COLOR) -> None:
    # Always print timestamp of action.
    console._log_render.omit_repeated_times = False
    console.log(text)
    # Reset so that following logs gets extended without timestamp.
    console._log_render.omit_repeated_times = True
    try:
        yield
    except Exception as exc:
        raise click.ClickException(str(exc)) from exc


@contextmanager
def progress(text: str, *, tasks: Sequence[Any]) -> None:
    with Progress(Progress.get_default_columns(), transient=True) as progress:
        task = progress.add_task(description=text, total=len(tasks))
        queue = deque(tasks)
        visited: set[str] = set()

        while queue:
            task_name = queue.popleft()
            visited.add(task_name)
            progress.advance(task)
            yield


class BulletListIterator:
    def __init__(self, it, color: str = DEFAULT_COLOR, add_indent: bool = True):
        self._it = iter(it)
        self._add_indent = add_indent
        self._color = text_color(color)
        self._last = None

    def __iter__(self):
        return self

    def __next__(self):
        self.__exit__(None, None, None)

        item = next(self._it)
        self._last = item

        if self._add_indent:
            click.echo(self._color("{:>13}".format("- ")), nl=False)
        else:
            click.echo(self._color("- "), nl=False)

        return self._color(item)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, exc_traceback):
        last = self._last
        if last is not None:
            self._last = None
