import typer
from pathlib import Path
import logging
from lark import UnexpectedEOF, UnexpectedCharacters

import pdfsplit as psp

logger = logging.getLogger("pdfsplit")
logging.basicConfig(filename="pdfsplit.log")
app = typer.Typer()


def _to_style(prompt: str, kind: str):
    k = kind[0].upper()
    msg_start = f"[{k}]"

    colors = {
        "success": {"fg": typer.colors.GREEN, "bold": True},
        "info": {"fg": typer.colors.BLUE},
        "warning": {"fg": typer.colors.YELLOW},
        "error": {"fg": typer.colors.RED},
    }
    assert kind in colors, f"Unknown kind {kind}"

    body = typer.style(prompt, **colors[kind])
    if kind not in ("error", "warning"):
        logging.info(prompt)
    else:
        logging.debug(prompt)

    return f"{msg_start} {body}"


def to_stdout(prompt: str, kind: str = "info"):
    lvl = {"success": 0, "info": 1, "warning": 2, "error": 3}
    logger.log(lvl[kind], prompt)
    typer.echo(_to_style(prompt, kind))


@app.command()
def list_unparsed(pdf_loc: str, dsl_loc: str) -> None:
    return psp.list_unparsed(dsl_loc)


@app.command()
def prepare_to(pdf_loc: str, dsl_loc: str, db_loc: str) -> None:
    psp.create_empty_code(dsl_loc, psp.list_pdfs(pdf_loc))
    psp.create_empty_db(db_loc)
    to_stdout("Successfully prepared!", "success")


@app.command()
def populate(
    pdf_loc: str, dsl_loc: str, db_loc: str, meta_loc: str, overwrite: bool = False
) -> None:
    """
    Populate sqlite3 database
    """
    db_loc = Path(db_loc)
    if overwrite and db_loc.exists():
        db_loc.unlink()
    else:
        if db_loc.exists():
            to_stdout(f"{db_path} already exists!", "error")
            raise typer.Exit(1)

    prepare_to(pdf_loc, dsl_loc, db_loc)

    if meta_loc is not None:
        metadata = psp.fetch_metadata(meta_loc)

    for ploc, dloc in psp.list_matched(pdf_loc, dsl_loc):
        try:
            tags = psp.parse_code(dloc)
        except UnexpectedEOF:
            print(f"\t! {c.name} is empty! Skipping ...")
            continue
        except UnexpectedCharacters as e:
            print(f"\t! Unable to parse {c.name} with Lark! Error given ::")
            print(e)
            continue

        data = psp.pdf_to_base64(ploc) or None
        if data is None:  # no data produced for this file
            to_stdout(f"No data produced from {fn}", kind="warning")
            continue
        if meta_loc is None:
            md = None
        else:
            md = metadata[Path(ploc).stem]

        psp.populate_db(db_loc, str(ploc), data, tags, md)
        to_stdout(f"{ploc.name} successfully loaded", "success")


if __name__ == "__main__":
    app()
