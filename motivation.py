import sys
import argparse

import argon

def using_argparse(args):
    # create the top-level parser
    parser = argparse.ArgumentParser(prog="PROG")
    parser.add_argument("--foo", action="store_true", help="foo help")
    subparsers = parser.add_subparsers()

    # create the parser for the "a" command
    parser_a = subparsers.add_parser("a", help="a help")
    parser_a.add_argument("bar", type=int, help="bar help")
    parser_a.set_defaults(func=handle_a)

    # create the parser for the "b" command
    parser_b = subparsers.add_parser("b", help="b help")
    parser_b.add_argument("--baz", choices="XYZ", help="baz help")
    parser_b.set_defaults(func=handle_b)

    # parse arguments and run handler
    parsed = parser.parse_args(args)
    parsed.func(parsed)


def using_argon_with_validation(args):
    # create the top-level parser
    app = argon.App(prog="PROG")
    app.arg("--foo", action="store_true", help="foo help")

    # create the parser for the "a" command
    with app.command("a", help="a help") as a:
        a.arg("bar", type=int, help="bar help").handler(handle_a)

    # create the parser for the "b" command
    with app.command("b", help="b help") as b:
        b.arg("--baz", choices="XYZ", help="baz_help").handler(handle_b)

    # parse arguments and run handler
    app.run(args)


def using_argon_without_validation(args):
    # create the top-level parser
    app = argon.App(prog="PROG")
    app.arg("--foo", action="store_true", help="foo help")

    # create the parser for the "a" command
    app.command("a", help="a help") \
       .arg("bar", type=int, help="bar help") \
       .handler(handle_a)

    # create the parser for the "b" command
    app.command("b", help="b help") \
       .arg("--baz", choices="XYZ", help="baz_help") \
       .handler(handle_b)

    # parse arguments and run handler
    app.run(args)


def handle_a(args):
    print "handling a", args.foo, args.bar


def handle_b(args):
    print "handling b", args.foo, args.baz


if __name__ == "__main__":
    for using in [using_argparse, using_argon_with_validation, 
                  using_argon_without_validation]:
        print "using", using
        for args in [["a", "12"], ["--foo", "b", "--baz", "Z"]]:
            using(args)
        print
