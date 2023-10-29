"""
This file defines actions, i.e. functions the URLs are mapped into
The @action(path) decorator exposed the function at URL:

    http://127.0.0.1:8000/{app_name}/{path}

If app_name == '_default' then simply

    http://127.0.0.1:8000/{path}

If path == 'index' it can be omitted:

    http://127.0.0.1:8000/

The path follows the bottlepy syntax.

@action.uses('generic.html')  indicates that the action uses the generic.html template
@action.uses(session)         indicates that the action uses the session
@action.uses(db)              indicates that the action uses the db
@action.uses(T)               indicates that the action uses the i18n & pluralization
@action.uses(auth.user)       indicates that the action requires a logged in user
@action.uses(auth)            indicates that the action requires the auth object

session, db, T, auth, and tempates are examples of Fixtures.
Warning: Fixtures MUST be declared with @action.uses({fixtures}) else your app will result in undefined behavior
"""

from py4web import action, request, abort, redirect, URL, Flash
from yatl.helpers import A
from pydal.validators import *
from .common import (
    db,
    session,
    T,
    cache,
    auth,
    logger,
    authenticated,
    unauthenticated,
    flash,
)
from py4web.utils.grid import Grid, GridClassStyleBulma, GridClassStyleBootstrap5
from py4web.utils.form import FormStyleDefault, FormStyleBulma

flash = Flash()

class GridActionButton:
    def __init__(
        self,
        url,
        text=None,
        icon=None,
        additional_classes="",
        additional_styles="",
        override_classes="",
        override_styles="",
        message="",
        append_id=False,
        name=None,
        ignore_attribute_plugin=False,
        **attrs
    ):
        self.url = url
        self.text = text
        self.icon = icon
        self.additional_classes = additional_classes
        self.additional_styles = additional_styles
        self.override_classes = override_classes
        self.override_styles = override_styles
        self.message = message
        self.append_id = append_id
        self.name = name
        self.ignore_attribute_plugin = ignore_attribute_plugin
        self.attrs = attrs


@action("index")
@action.uses("index.html", auth, T)
def index():
    user = auth.get_user()
    message = T("Hello {first_name}".format(**user) if user else "Hello")
    return dict(message=message)


@action("drivers")
@action("drivers/<path:path>", method=["GET", "POST"])
@action.uses("drivers.html", session, db)
def drivers(path=None):
    grid = Grid(path,
                query=(db.sys_db_drivers.id > 0), 
                search_queries=None,
                search_form=None,
                #grid_class_style=GridClassStyleBootstrap5,
                formstyle=FormStyleBulma)
    return dict(locals())


@action.uses(db, flash, session)
def test_connect():
    import psycopg2 as driver
    print('ok')
    flash.set('ok', 'green')


test_connection_button = [
    lambda row: GridActionButton(
        lambda row: test_connect(),
        text=f'Test Connection'
    )
]

@action("connections")
@action("connections/<path:path>", method=["GET", "POST"])
@action.uses("connections.html", session, db, flash)
def connections(path=None):
    grid = Grid(path,
                query=(db.sys_connections.id > 0), 
                search_queries=None,
                search_form=None,
                grid_class_style=GridClassStyleBulma,
                formstyle=FormStyleBulma,
                #pre_action_buttons=test_connection_button
                )
    return dict(locals())


@action("library")
@action("library/<path:path>", method=["GET", "POST"])
@action.uses("library.html", session, db, flash)
def library(path=None):
    grid = Grid(path,
                query=(db.sys_library.id > 0), 
                search_queries=None,
                search_form=None,
                grid_class_style=GridClassStyleBulma,
                formstyle=FormStyleBulma,
                #pre_action_buttons=test_connection_button
                )
    return dict(locals())
