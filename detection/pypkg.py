"""FreeBSD pkg Support for Python"""

# This file is a part of Virtual Lunduke.
# Copyright (C) 2025 NexusSfan <nexussfan@duck.com>,  [Xgui4](https://www.github.com/xgui4)

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


class Cache:
    def get(self, key):
        if not self._package_exists(key):
            return None
        installed = self._package_installed(key)
        pkg = Package(installed=installed)
        return pkg

    def _package_exists(self, package_name):
        result = subprocess.run(
            ["apt-cache", "policy", package_name],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=True,
        )
        if "Installed:" in result.stdout or "Candidate:" in result.stdout:
            return True
        return False

    def _package_installed(self, package_name):
        try:
            output = subprocess.check_output(
                ["dpkg", "-s", package_name], stderr=subprocess.STDOUT
            )
        except subprocess.CalledProcessError:
            return False
        if "install ok installed" in output.decode():
            return True
        return False
