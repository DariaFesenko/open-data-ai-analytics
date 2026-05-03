import json
import os
from pathlib import Path

from flask import Flask, render_template, send_from_directory

app = Flask(__name__)

REPORTS_DIR = Path(os.getenv("REPORTS_DIR", "/reports"))
PLOTS_DIR = Path(os.getenv("PLOTS_DIR", "/plots"))


def read_json(path):
    if path.exists():
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    return None


def read_text(path):
    if path.exists():
        return path.read_text(encoding="utf-8")
    return "No report found."


@app.route("/")
def index():
    plots = []
    for name in ["all_contract_price_distribution.png", "top_legal_entities.png"]:
        if (PLOTS_DIR / name).exists():
            plots.append(name)

    return render_template(
        "index.html",
        quality_report=read_json(REPORTS_DIR / "quality_report.json"),
        research_report=read_json(REPORTS_DIR / "research_report.json"),
        quality_text=read_text(REPORTS_DIR / "quality_report.txt"),
        research_text=read_text(REPORTS_DIR / "research_report.txt"),
        plots=plots,
    )


@app.route("/plots/<path:filename>")
def plots(filename):
    return send_from_directory(PLOTS_DIR, filename)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)