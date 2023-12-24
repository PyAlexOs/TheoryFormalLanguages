from course_work.tokenizer import get_tokens
from course_work.parser import Parser
from course_work.tools.exceptions import ModelLanguageError
import json
import os
import re


class UnitTest:
    def __init__(self, directory: str, answers_file: str, encoding: str = "utf-8"):
        self.directory = directory
        self.answers_file = answers_file
        self.encoding = encoding
        self.passed = 0
        self.count = 0

    def __call__(self):
        if os.path.exists(self.directory):
            if os.path.exists(self.answers_file):
                with open(self.answers_file, "r", encoding=self.encoding) as file:
                    answers = json.load(file)

                key = lambda string: [(int(s) if s.isdigit() else s) for s in re.split(r'(\d+)', string)]

                for (number, file) in enumerate(sorted(os.listdir(self.directory), key=key)):
                    self.count += 1

                    verdict = "okay"
                    parser = Parser(get_tokens(self.directory + "/" + file, encoding=self.encoding))

                    try:
                        parser.parse()
                    except ModelLanguageError as error:
                        verdict = error.__str__()

                    if answers[file]["expected_result"] != verdict:
                        print(f"{number + 1} TEST FAILED: {file}\n"
                              f"Expected: {answers[file]['expected_result']}\n"
                              f"Found: {verdict}\n"
                              f"Error in program: {answers[file]['error_raised']}\n"
                              f"Comment: {answers[file]['comment']}\n")

                    else:
                        self.passed += 1
                        print(f"{number + 1} TEST PASSED: {file}\n"
                              f"Error in program: {answers[file]['error_raised']}\n"
                              f"Comment: {answers[file]['comment']}\n")

                print(f"RESULT: {self.passed}/{self.count} TESTS PASSED")

            else:
                exit("Path to the file with the answers doesn't exist.")

        else:
            exit("Path to the directory with the tests doesn't exist.")


def main():
    test = UnitTest("tests",
                    "expected_verdicts.json")
    test()


if __name__ == "__main__":
    main()
