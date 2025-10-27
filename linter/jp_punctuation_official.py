import re

from model import Linter, LintResult

CommaPattern = re.compile(r"，")
PeriodPattern = re.compile(r"．")

class JpPunctuationOfficial(Linter):
    name = "公文書的な句読点"
    description = "いわゆる公文書な句読点，/．が使われていないかチェックします。"

    def run(self, body: str) -> list[LintResult]:
        results: list[LintResult] = []

        for i, line in enumerate(body.splitlines(), start=1):
            for m in CommaPattern.finditer(line):
                results.append(
                    LintResult(
                        line=i,
                        column=m.start() + 1,
                        message=line,
                        rule="句点に「，」が使われています。「、」を使うようにしてください。",
                    )
                )

            for m in PeriodPattern.finditer(line):
                results.append(
                    LintResult(
                        line=i,
                        column=m.start() + 1,
                        message=line,
                        rule="読点に「．」が使われています。「。」を使うようにしてください。",
                    )
                )

        return results


def run(body: str) -> list[LintResult]:
    linter = JpPunctuationOfficial()
    return linter.run(body)
