import argparse


class Error(Exception):
    pass


class CommandError(Error):
    pass


class SubError(Error):
    pass


class Part(object):

    #: Overriden in subclass.
    parser = None

    def arg(self, *args, **kwds):
        """Add an argument.

        Arguments are passed to :meth:`argparse.ArgumentParser.add_argument`.
        """
        self.parser.add_argument(*args, **kwds)
        return self

    def validate(self):
        pass

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        if exc_type is None and exc_value is None and traceback is None:
            self.validate()


class Command(Part):
    """Used to create commands.
    """

    def __init__(self, parser):
        self.parser = parser
        self.func = None

    def handler(self, func):
        """Set handler function for command.

        The function must accept a single argument *args* (output from
        :meth:`argparse.ArgumentParser.parse_args`).
        """
        if self.func is not None:
            raise CommandError("handler already set")
        if not callable(func):
            raise CommandError("handler not callable")
        self.func = func
        self.parser.set_defaults(_argon_func=func)
        return self

    def validate(self):
        if not self.func:
            raise CommandError("no handler set")


class Sub(Part):
    """Used for sub-command groups.
    """

    def __init__(self, parser):
        self.parser = parser
        self.subs = set()
        self.commands = set()

    @property
    def subparsers(self):
        if not hasattr(self, "_subparsers"):
            self._subparsers = self.parser.add_subparsers()
        return self._subparsers

    def _check_not_exists(self, name):
        if name in self.subs:
            raise SubError("sub already exists: {}".format(name))
        if name in self.commands:
            raise SubError("command already exists: {}".format(name))

    def sub(self, name, *args, **kwds):
        """Add a sub-command group.

        This method adds a new parser to its subparsers. Arguments are passed to
        the :class:`argparse.ArgumentParser` constructor.
        """
        self._check_not_exists(name)
        self.subs.add(name)
        parser = self.subparsers.add_parser(name, *args, **kwds)
        return Sub(parser)

    def command(self, name, *args, **kwds):
        """Add a command.

        This method adds a new parser to its subparsers. Arguments are passed to
        the :class:`argparse.ArgumentParser` constructor.
        """
        self._check_not_exists(name)
        self.commands.add(name)
        parser = self.subparsers.add_parser(name, *args, **kwds)
        return Command(parser)

    def validate(self):
        if self.subs:
            return
        if not self.commands:
            raise SubError("missing commands")


class App(Sub):
    """Represents command-line applications.

    Arguments are passed to :class:`argparse.ArgumentParser`.
    """

    def __init__(self, *args, **kwds):
        parser = argparse.ArgumentParser(*args, **kwds)
        self.parser = parser
        self.subs = set()
        self.commands = set()

    def run(self, args):
        """Run application. Typically ``app.run(sys.argv[1:])``.
        """
        parsed_args = self.parser.parse_args(args)
        return parsed_args._argon_func(parsed_args)
