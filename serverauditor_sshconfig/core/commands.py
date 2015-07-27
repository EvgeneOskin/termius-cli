# coding: utf-8
import logging
import getpass

from cliff.command import Command
from cliff.lister import Lister
from .settings import Config
from .storage import ApplicationStorage
from .storage.strategies import (
    SaveStrategy,
    RelatedSaveStrategy,
    GetStrategy,
    RelatedGetStrategy,
)


class PasswordPromptMixin(object):
    def prompt_password(self):
        return getpass.getpass("Serverauditor's password:")


class AbstractCommand(PasswordPromptMixin, Command):

    "Abstract Command with log."

    log = logging.getLogger(__name__)

    save_strategy = SaveStrategy
    get_strategy = GetStrategy

    def __init__(self, app, app_args, cmd_name=None):
        super(AbstractCommand, self).__init__(app, app_args, cmd_name)
        self.config = Config(self.app.NAME)
        self.storage = ApplicationStorage(
            self.app.NAME,
            save_strategy=self.save_strategy,
            get_strategy=self.get_strategy
        )

    def get_parser(self, prog_name):
        parser = super(AbstractCommand, self).get_parser(prog_name)
        parser.add_argument('--log-file', help="Path to log file.")
        return parser


class DetailCommand(AbstractCommand):

    save_strategy = RelatedSaveStrategy
    get_strategy = RelatedGetStrategy

    def get_parser(self, prog_name):
        parser = super(DetailCommand, self).get_parser(prog_name)
        parser.add_argument(
            '-d', '--delete',
            action='store_true', help='Delete hosts.'
        )
        parser.add_argument(
            '-I', '--interactive', action='store_true',
            help='Enter to interactive mode.'
        )
        parser.add_argument(
            '-L', '--label', metavar='NAME',
            help="Alias and Host's label in Serverauditor"
        )
        return parser


class ListCommand(Lister):

    log = logging.getLogger(__name__)

    def __init__(self, app, app_args, cmd_name=None):
        super(ListCommand, self).__init__(app, app_args, cmd_name)
        self.config = Config(self.app.NAME)
        self.storage = ApplicationStorage(self.app.NAME)

    def get_parser(self, prog_name):
        parser = super(ListCommand, self).get_parser(prog_name)
        parser.add_argument(
            '-l', '--list', action='store_true',
            help=('List hosts in current group with id, name, group in path '
                  'format, tags, username, address and port.')
        )
        parser.add_argument('--log-file', help="Path to log file.")
        return parser