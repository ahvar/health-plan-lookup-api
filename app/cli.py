import click
from flask import Blueprint

bp = Blueprint("cli", __name__, cli_group=None)

@bp.cli.command("load-data")
def load_data():
    """load test data"""
    