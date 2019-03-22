from __future__ import print_function
from cloudmesh.shell.command import command
from cloudmesh.shell.command import PluginCommand
from cloudmesh.login.api.manager import Manager
from cloudmesh.common.console import Console
from cloudmesh.common.util import path_expand
from pprint import pprint


class LoginCommand(PluginCommand):

    # noinspection PyUnusedLocal
    @command
    def do_login(self, args, arguments):
        """
        ::

          Usage:
              login [KEY]

          This command does some useful things.

          Arguments:
              KEY   a file name

          Options:
              -f      specify the file

        """

        # m = Manager()

        if arguments.KEY is None:
            arguments.KEY = "~/.ssh/id_rsa.pub"

        pprint(arguments)

        key = path_expand(arguments.KEY)

        Console.msg("Login with", key)
        Console.error("not implemented")

        return ""