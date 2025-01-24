from pathlib import Path
from lark import Lark, Transformer
import os

import pdfsplit as psp


def list_unparsed(parser_root_dir: str):
    prev_path = None
    for p in Path(parser_root_dir).glob("**/*.lark"):
        if prev_path is None or prev_path != p.parent:
            prev_path = p.parent
        if p.stat().st_size == 1:  # non-empty files only
            yield p


def fetch_grammar():
    fn = Path(os.path.realpath(__file__)).parent / "grammar.lark"
    with open(fn) as f:
        d = f.readlines()
    if d:
        return Lark("".join(d))
    else:
        raise FileNotFoundError("This file is empty")


class SplitTransformer(Transformer):
    def range(self, v):
        low, high = v
        return [int(low), int(high)]

    def sequences(self, v):
        return [
            (
                j
                if isinstance(j, list)
                else [
                    j,
                ]
            )
            for j in v
        ]

    def cmd(self, v):
        sequences, tags = v
        r = []
        for tag in tags:
            r.append([sequences, tag])
        return r

    def ESCAPED_STRING(self, v):
        return v[1:-1].replace(" ", "_")

    def tags(self, v):
        return v

    def INT(self, v):
        return int(v)

    def start(self, v):
        return [x for xs in v for x in xs]


def group_by_page(data):
    by_page = {}
    for p, t in data:
        if isinstance(p, list):
            low, high = p

            for sp in range(low, high + 1):
                if sp not in by_page:
                    by_page[sp] = [
                        t,
                    ]
                else:
                    by_page[sp].append(t)
        else:
            if p not in by_page:
                by_page[p] = [
                    t,
                ]
            else:
                by_page[p].append(t)

    return by_page


def parse_code(fn) -> list:
    code = psp.load_code(fn)
    p = fetch_grammar()
    tree = p.parse(code)
    r = SplitTransformer().transform(tree)
    return group_by_page(r)
