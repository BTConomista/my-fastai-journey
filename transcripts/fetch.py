#!/usr/bin/env python3
"""Scarica i sottotitoli ufficiali di una lezione di fast.ai e ne fa una trascrizione leggibile.

    pip install yt-dlp
    python3 transcripts/fetch.py 8SF_h3xF3cE transcripts/lesson-01.md

Il file prodotto non viene versionato (vedi .gitignore in questa cartella): e' il testo
integrale della lezione, che appartiene ai suoi autori. Vedi README.md.

Nota su YouTube: al momento quasi tutti i player client di yt-dlp vengono respinti con
"Sign in to confirm you're not a bot". Il client `web_embedded` passa, ed e' quello che
questo script forza. Se un domani smettesse di funzionare, la cosa da cambiare e' li'.
"""

import json
import re
import subprocess
import sys
import tempfile
from pathlib import Path

CLIENT = "web_embedded"
PARAGRAPH_SECONDS = 45


def download_subtitles(video_id, workdir):
    """Scarica i sottotitoli inglesi in formato json3 e ne restituisce il path."""
    subprocess.run(
        [
            sys.executable, "-m", "yt_dlp",
            "--skip-download",
            "--ignore-no-formats-error",
            "--write-sub", "--sub-lang", "en", "--sub-format", "json3",
            "--extractor-args", "youtube:player_client=" + CLIENT,
            "-o", str(workdir / "sub.%(ext)s"),
            "https://youtu.be/" + video_id,
        ],
        check=True,
    )
    path = workdir / "sub.en.json3"
    if not path.exists():
        raise SystemExit("sottotitoli non trovati: il video non ne ha, o YouTube ha respinto la richiesta")
    return path


def cues(path):
    """I blocchi di sottotitolo come coppie (secondo di inizio, testo)."""
    out = []
    for event in json.load(open(path))["events"]:
        if "segs" not in event:
            continue
        text = "".join(seg.get("utf8", "") for seg in event["segs"]).replace("\n", " ")
        text = re.sub(r"\s+", " ", text).strip()
        if text:
            out.append((event["tStartMs"] / 1000.0, text))
    return out


def paragraphs(items):
    """Raggruppa i blocchi in paragrafi da ~PARAGRAPH_SECONDS, chiudendo a fine frase."""
    out, buf, start = [], [], items[0][0]
    for ts, text in items:
        buf.append(text)
        if ts - start >= PARAGRAPH_SECONDS and re.search(r'[.!?]"?$', text):
            out.append((start, " ".join(buf)))
            buf, start = [], ts
    if buf:
        out.append((start, " ".join(buf)))
    return out


def hms(seconds):
    s = int(seconds)
    return "%02d:%02d:%02d" % (s // 3600, (s % 3600) // 60, s % 60)


def main():
    if len(sys.argv) != 3:
        raise SystemExit(__doc__)
    video_id, out_path = sys.argv[1], Path(sys.argv[2])

    with tempfile.TemporaryDirectory() as tmp:
        items = cues(download_subtitles(video_id, Path(tmp)))

    paras = paragraphs(items)
    header = (
        "# Trascrizione — https://youtu.be/%s\n\n"
        "%d blocchi di sottotitolo in %d paragrafi. Testo degli autori del video, "
        "non versionato: vedi transcripts/README.md.\n\n---\n\n" % (video_id, len(items), len(paras))
    )
    body = "\n\n".join("**[%s]** %s" % (hms(t), re.sub(r"  +", " ", p)) for t, p in paras)
    out_path.write_text(header + body + "\n")
    print("%s — %d paragrafi, %d parole" % (out_path, len(paras), len(body.split())))


if __name__ == "__main__":
    main()
