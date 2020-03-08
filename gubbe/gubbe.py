# -*- coding: utf-8 -*-

#################################################################
#                                                               #
# Gubbe                                                         #
# Copyright (C) 2020, Vilhelm Prytz, <vilhelm@prytznet.se>      #
#                                                               #
# Licensed under the terms of the MIT license, see LICENSE.     #
# https://github.com/VilhelmPrytz/gubbe                         #
#                                                               #
#################################################################

import os
import click
import codecs
import locale

from gubbe.version import version, commit_date, commit_hash
from gubbe.config import Config
from gubbe.jar_detector import JARDetector

config = Config()
jar_detector = JARDetector()


def main():
    # snap packages raise some weird ASCII codec errors, so we just force C.UTF-8
    if (
        codecs.lookup(locale.getpreferredencoding()).name == "ascii"
        and os.name == "posix"
    ):
        os.environ["LC_ALL"] = "C.UTF-8"
        os.environ["LANG"] = "C.UTF-8"

    cli()


def print_version(ctx, param, value):
    """
    print version and exit
    """

    if not value or ctx.resilient_parsing:
        return

    _commit_hash = commit_hash[0:7]

    if str(version) == "0.0.0.dev0":
        click.echo(
            f"✨ gubbe version {_commit_hash}/edge (development build) built {commit_date}"
        )
    else:
        click.echo(
            f"✨ gubbe version v{version}/stable (commit {_commit_hash}) built {commit_date}"
        )

    ctx.exit()


@click.group()
@click.option(
    "--version", is_flag=True, callback=print_version, expose_value=False, is_eager=True
)
def cli():
    """
    Gubbe

    Manage Minecraft plugins with ease!

    Source code - https://github.com/VilhelmPrytz/gubbe
    """

    pass


@cli.command()
def init():
    """
    Initiate current directory with Gubbe
    """

    if len(jar_detector.files) > 1:
        selected = None
        while selected == None:
            click.echo(
                "Multiple JAR files detected. Select the JAR file you are using."
            )
            for i in range(len(jar_detector.files)):
                click.echo(
                    f"{i} - {jar_detector.files[i]['filename']} detected version {jar_detector.files[i]['version']}"
                )

            user_selection = click.prompt("Select JAR file", default=0)

            if 0 <= int(user_selection) <= len(jar_detector.files) - 1:
                selected = jar_detector.files[int(user_selection)]

    if len(jar_detector.files) == 1:
        selected = jar_detector.files[0]

    if len(jar_detector.files) == 0:
        click.echo("No JAR files detected.")
        exit(1)

    if selected["version"] == None:
        click.echo("Unable to automatically identify Minecraft version.")
        selected["version"] = click.prompt("Minecraft version", default="1.15.2")

    config.create(selected["filename"], selected["version"])

    pass


@cli.command()
def list():
    """
    List currently installed plugins.
    """

    pass


@cli.command()
def install():
    """
    Install a new plugin.
    """

    pass


@cli.command()
def update():
    """
    Update installed plugins.
    """

    pass


if __name__ == "__main__":
    main()
