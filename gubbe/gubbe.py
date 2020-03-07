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

    Manage Minecraft Plugins with ease!

    Source code - https://github.com/VilhelmPrytz/gubbe
    """

    pass


if __name__ == "__main__":
    main()
