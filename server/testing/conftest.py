#!/usr/bin/env python3

import os

import pytest

from app import app
from models import db, Plant

def pytest_itemcollected(item):
    par = item.parent.obj
    node = item.obj
    pref = par.__doc__.strip() if par.__doc__ else par.__class__.__name__
    suf = node.__doc__.strip() if node.__doc__ else node.__name__
    if pref or suf:
        item._nodeid = ' '.join((pref, suf))


@pytest.fixture(autouse=True)
def _reset_db():
    test_db_path = os.path.join(os.path.dirname(__file__), "test.db")
    app.config["TESTING"] = True
    app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:////{test_db_path.lstrip('/')}"

    with app.app_context():
        db.drop_all()
        db.create_all()

        plant_1 = Plant(
            name="Aloe",
            image="https://example.com/aloe.png",
            price=11.5,
            is_in_stock=True,
        )
        db.session.add(plant_1)
        db.session.commit()

    yield
