from functools import wraps
from typing import Callable, TypeVar, cast

from flask import flash, redirect, session, url_for
from flask.typing import ResponseReturnValue

ViewFunc = TypeVar("ViewFunc", bound=Callable[..., ResponseReturnValue])


def login_required(view: ViewFunc) -> ViewFunc:
    @wraps(view)
    def wrapped(*args, **kwargs):
        if not session.get("user_id"):
            flash("Please log in to continue")
            return redirect(url_for("login"))
        return view(*args, **kwargs)

    return cast(ViewFunc, wrapped)


def anonymous_required(view: ViewFunc) -> ViewFunc:
    @wraps(view)
    def wrapped(*args, **kwargs):
        if session.get("user_id"):
            return redirect(url_for("home"))
        return view(*args, **kwargs)

    return cast(ViewFunc, wrapped)
