#!/usr/bin/env pypy3
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

from typing import Any, LiteralString


import sys
import json
import socket
import detection

__version__ = "0.0.1-1-xgui4fork"

argv: list[str] = sys.argv
argv.pop(0) 

NOTES_ENABLED = False
ALT_ENABLED = False
VERBOSE = False

for argument in argv:
    if argument in ('--notes', '-n'):
        NOTES_ENABLED = True # is that supposed to be a constant or a variable ?   # pyright: ignore[reportConstantRedefinition]
    elif argument in ('--alternatives', '-a'):
        ALT_ENABLED = True # is that supposed to be a constant or a variable ?  # pyright: ignore[reportConstantRedefinition]
    elif argument in ('--list-apps', '-l'):
        print("Supported apps:")
        with open("data/apps.json", encoding="ascii", errors="ignore") as tempdata:
            print("\n".join(json.loads(tempdata.read())))
        sys.exit(0)
    elif argument in ('-v', '--verbose'):
        VERBOSE = True # is that supposed to be a constant or a variable ?   # pyright: ignore[reportConstantRedefinition]
    elif argument in ('-h', '-?', '--help'):
        print(f"Virtual Lunduke {__version__}")
        print("Detects programs on your system that Lunduke wouldn't approve of.")
        print("Arguments:")
        print("\t --notes, -n: Enable notes on apps")
        print("\t --alternatives, -a: Enables alternatives for 'woke' apps")
        print("\t --list-apps, -l: Show all apps that can be detected")
        print("\t --verbose, -v: Debug info")
        print("\t -h, -?, --help: Show this help message")
        sys.exit(0)
    else:
        print("Unknown argument.")
        print("Run `./virtual-lunduke.py --help` for arguments")
        sys.exit(1)

def addition(lst: list, arg: str) -> list[Any]:
    if not lst:
        if not lst:
            lst.append(
                f"\t\tWoke applications installed on {socket.gethostname()}"
            )
        lst.append("")
    lst.append(arg)
    if VERBOSE:
        print(f"VERBOSE: Current output: {lst}")
    return lst

def get_alt(app : str, packages: str, altssys) -> str:
    if not ALT_ENABLED:
        return ""
    alts: list = altssys[app]
    packages_len: int = len(packages)
    spaces_len: int = 20 - packages_len
    spaces: str = " " * spaces_len

    formatted_alt_str = ""
    for alt in alts:
        if alt not in ('[',  ']',  '\''):
            formatted_alt_str += alt
    
    return f"{spaces}Alternatives : {formatted_alt_str}"

def get_notes(app: str, packages: str, notessys) -> str:
    if not NOTES_ENABLED:
        return ""
    note = notessys[app]
    packages_len = len(packages)
    spaces_len = 20 - packages_len
    spaces = " " * spaces_len
    return f"{spaces}{note}"

def check_all(data: list, detectsys, notessys, altsdata) -> list[Any]:
    total_results = []
    for program in data:
        if VERBOSE:
            print(f"VERBOSE: Checking for {program}")
        results = detectsys.check(program)
        if results:
            if VERBOSE:
                print(f"VERBOSE: Detected {program}")
            results_str: str = ", ".join(results)
            programlen: int = len(program)
            spaceslen: int = 20 - programlen
            spaces: str = " " * spaceslen
            note: str = get_notes(app=program, packages=results_str, notessys=notessys)
            alt: str = get_alt(app=program, packages=results_str,altssys=altsdata)
            total_results = addition(lst=total_results, arg=f"{program}{spaces}{results_str}{note}{alt}")
    if sys.implementation.name == "cpython":
        if NOTES_ENABLED or ALT_ENABLED:
            total_results = addition(lst=total_results, arg="CPython             python3             Use PyPy")
        else:
            total_results = addition(lst=total_results, arg="CPython             python3")
    if not total_results:
        total_results.append(f"No woke applications installed on {socket.gethostname()}! I'm sure Lunduke would be happy.")
    return total_results


if __name__ == "__main__":
    with open("data/apps.json", encoding="ascii", errors="ignore") as filedata:
        appdata = json.loads(filedata.read())
    with open("data/notes.json", encoding="ascii", errors="ignore") as filedata2:
        notesdata = json.loads(filedata2.read())
    with open("data/alternatives.json", encoding="ascii", errors="ignore") as filedata3:
        altsdata = json.loads(filedata3.read())
    detection_systems = detection.get_detection_system()
    if VERBOSE:
        print(f"VERBOSE: {detection_systems[1]} selected as detection system")
    DETECT_DATA = f"data/{detection_systems[1]}.json"
    detection_system = detection_systems[0](DETECT_DATA)
    if VERBOSE:
        print(f"VERBOSE: Created {detection_systems[0]} object")
    result = check_all(appdata, detection_system, notesdata, altsdata)
    print("\n".join(result))
