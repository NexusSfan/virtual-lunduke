"""Pacman Support for Python (by Xgui4)"""

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

import subprocess
from dataclasses import dataclass

@dataclass
class Package:
    installed: bool

class Query: 
    def get(self, key):
        if not self._package_exists(key):
            return None
        installed = self._package_installed(key)
        pkg = Package(installed=installed)
        return pkg
    
    def _package_exists(self, package_name):
        result = subprocess.run(
            ["pacman", "-Ss", package_name],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=True,
        )
        if package_name in result.stdout:
            return True
        return False

    
    def _package_installed(self, package_name):
        try:
            # Run pacman -Q and capture output
            result = subprocess.run(
                ['pacman', '-Q', package_name],
                capture_output=True,
                text=True,
                check=True  # Raise CalledProcessError if pacman returns non-zero exit code
            )
            # If no error, the package is installed
            return True
        except subprocess.CalledProcessError:
            # If pacman returns an error (package not found), it's not installed
            return False

