from typing import Awaitable, Callable
import dc


class Handler:
    def __init__(self, func: Callable[[dc.Context], Awaitable[None]], require_admin: bool) -> None:
        self.func = func
        self.require_admin = require_admin

    def __call__(self, ctx: dc.Context) -> Awaitable[None]:
        return self.func(ctx)
