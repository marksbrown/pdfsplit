from pathlib import Path
import json
from typing import Iterable, TypeAlias
import json

dl: TypeAlias = dict[str, list[str]]


def fetch_metadata(fn="metadata.json"):
    with open(fn, "r") as f:
        metadata = json.load(f)

    return metadata


def reverse_dict(dict_: dl):
    reversed_ = {}
    for tag in dict_:
        for v in dict_[tag]:
            reversed_[v] = tag
    return reversed_


def merge_dicts(*dicts: list[dl]) -> dl:
    """
    >>> merge_dicts({"a" : 1},{"b" : 2}, {"c" : 3})
    {'a': 1, 'b': 2, 'c': 3}
    """
    # first : dl, second : dl
    if len(dicts) == 2:
        first, second = dicts
        r = first
        for k in second:
            if k not in r:
                r[k] = second[k]
            else:
                r[k] += second[k]
                r[k] = list(set(r[k]))
        return r
    elif len(dicts) > 2:
        first = dicts[0]
        second = dicts[1]
        return merge_dicts(merge_dicts(first, second), *dicts[2:])


def list_unparsed(dsl_loc):
    prev_path = None
    for p in Path(dsl_loc).glob("**/*.lark"):
        if prev_path is None or prev_path != p.parent:
            prev_path = p.parent
            print("==", prev_path)
        if p.stat().st_size == 1:
            yield p


def _listf(loc: Path, ext: str) -> Iterable[Path]:
    for fn in loc.glob(f"**/*.{ext}"):
        yield fn


def list_matched(pdf_loc, dsl_loc):
    for p in list_pdfs(pdf_loc):
        q = list(p.with_suffix(".lark").parts)
        q[0] = dsl_loc
        q = Path("/".join(q))
        yield p, q


def list_pdfs(pdf_loc, path=""):
    p = pdf_loc / Path(path)
    yield from _listf(p, "pdf")


def list_code(dsl_loc, path=""):
    p = dsl_loc / Path(path)
    yield from _listf(p, "lark")


def load_code(fn: Path) -> str:
    with open(fn) as f:
        r = f.readlines()
    return "".join(r)


def create_empty_code(dsl_loc, pdfs: list[Path], ext="lark") -> int:
    root = Path(dsl_loc)
    if not root.exists():
        root.mkdir(parents=True)
    count = 0
    for pdf in pdfs:
        loc = root.joinpath(*pdf.parent.parts[1:])
        p = loc / (pdf.stem + "." + ext)
        if not p.parent.exists():
            p.mkdir(parents=True)
        if not p.exists():
            count += 1
            with open(p, "w") as f:
                print("", file=f)

    return count
