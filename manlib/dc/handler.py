from typing import Awaitable, Callable
from .context import Context


class Handler:
    def __init__(self, func: Callable[[Context], Awaitable[None]], require_admin: bool) -> None:
        self.func = func
        self.require_admin = require_admin

    def __call__(self, ctx: Context) -> Awaitable[None]:
        return self.func(ctx)
