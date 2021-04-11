from typing import Callable
import dc


class Handler:
    func: Callable
    require_admin: bool

    def __init__(self, func: Callable, require_admin: bool) -> None:
        self.func = func
        self.require_admin = require_admin

    def __call__(self, ctx: dc.Context) -> None:
        self.func(ctx)
