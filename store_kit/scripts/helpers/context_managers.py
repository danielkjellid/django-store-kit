from contextlib import contextmanager

import rich_click as click
from .text import echo_with_time, text_color


@contextmanager
def action(text: str, *, add_icon: bool = True, color: str | None = None) -> None:
    echo_with_time(text, color=color, nl=not add_icon)
    try:
        yield
        if add_icon:
            click.echo(" ✅")
    except Exception as exc:
        if add_icon:
            click.echo(" ❌")
        raise exc


class BulletListIterator:
    def __init__(self, it, color: str = "", add_indent: bool = True):
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
