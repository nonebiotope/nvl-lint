import json
import os
import subprocess
import sys

from model import LintResult

def lint(path: str, is_markdown: bool = False):
    if not os.path.exists(os.path.join(path, "nvllint.config.json")):
        print("nvllint.config.json not found.")
        return

    with open(os.path.join(path, "nvllint.config.json"), "r", encoding="utf-8") as f:
        pconfig = json.load(f)

    for linter_path in pconfig["linters"]:
        linter = __import__(f"linter.{linter_path.replace("/", ".")}", fromlist=["run"])
        for file in pconfig["files"]:
            with open(os.path.join(path, file), "r", encoding="utf-8") as f:
                body = f.read()
            lint_result: list[LintResult] = linter.run(body)
            for result in lint_result:
                if is_markdown:
                    print(
                        f"- <ins>{result.rule}</ins> {os.path.join(path, file)}:{result.line}:{result.column}\n`{result.message}`\n"
                    )
                else:
                    print(
                        f"{result.rule} {os.path.join(path, file)}:{result.line}:{result.column}\n{result.message}\n"
                    )


def add_linter(linter_name: str):
    if os.path.isfile(os.path.join("linter", linter_name)):
        print(f"Linter {linter_name} already exists.")
        return
    subprocess.run(
        [
            "git",
            "clone",
            f"https://github.com/{linter_name}.git",
            os.path.join("linter", linter_name.replace("/", "@")),
        ]
    )
    print(f"Linter {linter_name} has been added.")


def del_linter(linter_name: str):
    if not os.path.isdir(os.path.join("linter", linter_name.replace("/", "@"))):
        print(f"Linter {linter_name} does not exist.")
        return
    os.remove(os.path.join("linter", linter_name.replace("/", "@")))
    print(f"Linter {linter_name} has been removed.")


if __name__ == "__main__":
    if sys.argv[1] == "lint-cli" or sys.argv[1] == "lint":
        lint(sys.argv[2], is_markdown=False)
    elif sys.argv[1] == "lint-md":
        lint(sys.argv[2], is_markdown=True)
    elif sys.argv[1] == "add":
        add_linter(sys.argv[2])
    elif sys.argv[1] == "del":
        del_linter(sys.argv[2])
