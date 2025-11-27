"""Virtual Lunduke: Detects programs on your system that Lunduke wouldn't approve of."""

# This file is a part of Virtual Lunduke.
# Copyright (C) 2025 NexusSfan <nexussfan@duck.com>

# Virtual Lunduke is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# Virtual Lunduke is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with Virtual Lunduke. If not, see <https://www.gnu.org/licenses/>.

import sys
import json
import socket
import detection

__version__ = "0.0.0"

argv = sys.argv
argv.pop(0)

NOTES_ENABLED = False

for argument in argv:
    if argument in ('--notes', '-n'):
        NOTES_ENABLED = True
    elif argument in ('--list-apps', '-a'):
        print("Supported apps:")
        with open("data/apps.json", encoding="ascii", errors="ignore") as tempdata:
            print("\n".join(json.loads(tempdata.read())))
        sys.exit(0)
    elif argument in ('-h', '-?', '--help'):
        print(f"Virtual Lunduke {__version__}")
        print("Detects programs on your system that Lunduke wouldn't approve of.")
        print("Arguments:")
        print("\t --notes, -n: Enable notes on apps")
        print("\t --list-apps, -a: Show all apps that can be detected")
        print("\t -h, -?, --help: Show this help message")
        sys.exit(0)
    else:
        print("Unknown argument.")
        print("Run `./virtual-lunduke.py --help` for arguments")
        sys.exit(1)

def addition(lst: list, arg: str):
    if not lst:
        if not lst:
            lst.append(
                f"\t\tWoke applications installed on {socket.gethostname()}"
            )
        lst.append("")
    lst.append(arg)
    return lst

def get_notes(app: str, packages: str, notessys):
    if not NOTES_ENABLED:
        return ""
    note = notessys[app]
    packages_len = len(packages)
    spaces_len = 20 - packages_len
    spaces = " " * spaces_len
    return f"{spaces}{note}"

def check_all(data: list, detectsys, notessys):
    total_results = []
    for program in data:
        results = detectsys.check(program)
        if results:
            results_str = ", ".join(results)
            programlen = len(program)
            spaceslen = 20 - programlen
            spaces = " " * spaceslen
            note = get_notes(program, results_str, notessys)
            total_results = addition(total_results, f"{program}{spaces}{results_str}{note}")
    if sys.implementation.name == "cpython":
        total_results = addition(total_results, "CPython             python3             Use PyPy")
    if not total_results:
        total_results.append(f"No woke applications installed on {socket.gethostname()}! I'm sure Lunduke would be happy.")
    return total_results


if __name__ == "__main__":
    with open("data/apps.json", encoding="ascii", errors="ignore") as filedata:
        appdata = json.loads(filedata.read())
    with open("data/notes.json", encoding="ascii", errors="ignore") as filedata2:
        notesdata = json.loads(filedata2.read())
    detection_systems = detection.get_detection_system()
    DETECT_DATA = f"data/{detection_systems[1]}.json"
    detection_system = detection_systems[0](DETECT_DATA)
    result = check_all(appdata, detection_system, notesdata)
    print("\n".join(result))
