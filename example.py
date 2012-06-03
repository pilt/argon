import sys

import argon


def main():
    app = argon.App(description="Argon example.")

    # If given, the output is reversed.
    app.arg("-r", "--reverse", default=False, action="store_true",
            help="reverse output")

    # Add math sub-commands. "sum" computes the sum args and "hex" converts
    # an integer to hex.
    with app.sub("math") as math:
        with math.command("sum") as math_sum:
            math_sum.arg("numbers", help="numbers to compute sum of",
                         nargs="+", type=int)
            math_sum.handler(do_sum)
        with math.command("hex", help="convert number to hex") as math_hex:
            math_hex.arg("number", type=int).handler(do_hex)

    # Add an echo command. It accepts an argument to uppercase its input.
    with app.command("echo") as echo:
        echo.arg("-u", dest="uppercase", default=False, action="store_true",
                 help="convert to uppercase") \
            .arg("string") \
            .handler(do_echo)

    app.run(sys.argv[1:])


def show(func):
    """Decorator to print the return value of func, possibly reversed. """
    def wrapper(args):
        output = str(func(args))
        if args.reverse:
            print "".join(reversed(output))
        else:
            print output
    return wrapper


@show
def do_sum(args):
    return sum(args.numbers)


@show
def do_hex(args):
    return hex(args.number)


@show
def do_echo(args):
    if args.uppercase:
        return args.string.upper()
    return args.string


if __name__ == "__main__":
    main()
