import unittest

import argon


def returns(return_value):
    return lambda args: return_value


class TestArgon(unittest.TestCase):

    def test_command_ok(self):
        app = argon.App()
        with app.command("a") as a:
            a.handler(returns("a"))
        self.assertEqual(app.run(["a"]), "a")

    def test_command_no_handler(self):
        def no_handler():
            app = argon.App()
            with app.command("a") as a:
                pass  # no handler
        self.assertRaises(argon.CommandError, no_handler)

    def test_command_two_handlers(self):
        def two_handlers():
            app = argon.App()
            with app.command("a") as a:
                a.handler(returns("a"))
                a.handler(returns("a"))
        self.assertRaises(argon.CommandError, two_handlers)

    def test_sub_simple_ok(self):
        app = argon.App()
        with app.sub("a") as a:
            with a.command("a") as aa:
                aa.handler(returns("aa"))
            with a.command("b") as ab:
                ab.handler(returns("ab"))
        with app.command("c") as a:
            a.handler(returns("c"))
        self.assertEqual(app.run(["a", "a"]), "aa")
        self.assertEqual(app.run(["a", "b"]), "ab")
        self.assertEqual(app.run(["c"]), "c")

    def test_nesting(self):
        app = argon.App()
        with app.sub("a") as a:
            with a.sub("a") as aa:
                with aa.command("a") as aaa:
                    aaa.handler(returns("aaa"))
                with aa.command("b") as aab:
                    aab.handler(returns("aab"))
                with aa.sub("c") as aac:
                    with aac.command("a") as aaca:
                        aaca.handler(returns("aaca"))
                    with aac.command("b") as aacb:
                        aacb.handler(returns("aacb"))
            with a.sub("b") as ab:
                with ab.command("a") as aba:
                    aba.handler(returns("aba"))
                with ab.command("b") as abb:
                    abb.handler(returns("abb"))
                with ab.sub("c") as abc:
                    with abc.command("a") as abca:
                        abca.handler(returns("abca"))
                    with abc.command("b") as abcb:
                        abcb.handler(returns("abcb"))

        for comb in ["aaa", "aab", "aaca", "aacb",
                     "aba", "abb", "abca", "abcb"]:
            self.assertEqual(app.run(list(comb)), comb)

    def test_name_collisions(self):
        def same_sub_sub_name():
            app = argon.App()
            with app.sub("a") as a:
                with a.command("aa") as aa:
                    aa.handler(returns("aa"))
            with app.sub("a") as a:
                with a.command("aa") as aa:
                    aa.handler(returns("aa"))
        self.assertRaises(argon.SubError, same_sub_sub_name)

        def same_sub_command_name():
            app = argon.App()
            with app.sub("a") as a:
                with a.command("aa") as aa:
                    aa.handler(returns("aa"))
            with app.command("a") as a:
                a.handler(returns("a"))
        self.assertRaises(argon.SubError, same_sub_command_name)

        def same_command_command_name():
            app = argon.App()
            with app.command("a") as a:
                a.handler(returns("a"))
            with app.command("a") as a:
                a.handler(returns("a"))
        self.assertRaises(argon.SubError, same_command_command_name)

    def test_args(self):
        def xy(args):
            return (args.x, args.y)

        app = argon.App()
        with app.sub("a") as a:
            a.arg("-x", dest="x", nargs="?", default=False)
            with a.command("a") as aa:
                aa.arg("-y", dest="y", default=False, action="store_true")
                aa.handler(xy)

        self.assertEqual(app.run("a a".split()), (False, False))
        self.assertEqual(app.run("a -x a a".split()), ("a", False))
        self.assertEqual(app.run("a a -y".split()), (False, True))
        self.assertEqual(app.run("a -x foo a -y".split()), ("foo", True))

    def test_parse(self):
        handler = lambda args: args
        app = argon.App()
        with app.command("a") as a:
            a.handler(handler)
        func, args = app.parse(["a"])
        self.assertIs(func, handler)

    def test_parse_known(self):
        handler = lambda args: args
        app = argon.App()
        with app.command("a") as a:
            a.handler(handler)
        func, args, unknowns = app.parse_known(["a", "b"])
        self.assertIs(func, handler)
        self.assertEqual(unknowns, ["b"])

    def test_run_known(self):
        return_unknowns = lambda args, unknowns: unknowns
        app = argon.App()
        with app.command("a") as a:
            a.handler(return_unknowns)
        self.assertEqual(app.run_known(["a", "b"]), ["b"])

if __name__ == "__main__":
    unittest.main()
