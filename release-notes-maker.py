#!/usr/bin/python3

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import sys
import re


def main():
    if len(sys.argv) != 2:
        print("Invalid arguments")

    issues = {}
    with open(sys.argv[1]) as f:
        data = f.read()

        commits = re.split('commit [a-f0-9]{40}\nAuthor:.*\nDate:.*\n', data)
        for c in commits:
            commit = c.strip()
            if len(commit) == 0:
                continue
            s = re.search('(ACCUMULO-\d+)[\]\- ]*(.*)', commit)
            i = 'UNKNOWN' if not s else s.group(1)
            subject = None if not s else s.group(2)
            commit_list = issues.get(i, [])
            commit_list.insert(0, (commit, subject))
            issues[i] = commit_list

    for (issue, commit_list) in sorted(issues.items()):
        print("* [", issue, "] - ", sep="", end="")
        if len(commit_list) == 1:
            commit, subject = commit_list[0]
            print(subject)
            if len(commit.split('\n')) > 1:
                print("```")
                print(commit)
                print("```")
        else:
            print()
            print("```")
            for idx, (commit, subject) in enumerate(commit_list):
                print("commit #", idx+1, ": ", commit, sep="")
            print("```")

    print()
    for issue in sorted(issues.keys()):
        if issue.startswith("ACCUMULO-"):
            print("[", issue, "]: https://issues.apache.org/jira/browse/", issue, sep="")


if __name__ == "__main__":
    main()
