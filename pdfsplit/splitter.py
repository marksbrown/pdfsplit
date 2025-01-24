import pdfsplit as psp
from subprocess import run
from pathlib import Path


def pdf_to_base64(fn: str, tmp_loc="/tmp") -> list[str]:
    """
    Each page of a PDF converted into a list of base64 images
    """
    cmd = "pdftoppm {} {}/pdfsplit -png".format(fn, tmp_loc)
    run(cmd, shell=True)
    for png in Path(tmp_loc).glob("pdfsplit*.png"):
        cmd = "base64 {}".format(png)
        r = run(cmd, shell=True, capture_output=True)
        yield png.stem.split("-")[-1], r.stdout
        png.unlink()
