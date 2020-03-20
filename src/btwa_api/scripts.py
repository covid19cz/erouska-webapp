import getpass

import bcrypt
import click
from btwa_api.app.db.sql.models.handler import Handler
from btwa_api.app.db.sql.session import Session


def add_user(username, password):
    session = Session()
    handler = Handler(username=username,
                      password=bcrypt.hashpw(password.encode(), bcrypt.gensalt()))
    session.add(handler)
    session.commit()
    session.close()


@click.command("add-user")
@click.argument("username")
def add_user_cmd(username):
    add_user(username, getpass.getpass())


@click.group()
def cli():
    pass


if __name__ == "__main__":
    cli.add_command(add_user_cmd)
    cli()
