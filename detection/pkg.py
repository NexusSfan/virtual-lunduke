"""Detection System for FreeBSD pkg"""

# This file is a part of Virtual Lunduke.
# Copyright (C) 2025 NexusSfan <nexussfan@duck.com>, [Xgui4](https://www.github.com/xgui4)

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

from . import base

try:
    import pkg
except ModuleNotFoundError:
    from . import py-freebsd as pkg


class AptDetectionSystem(base.DetectionSystem):
    def __init__(self, data: str):
        super().__init__(data)

    def check(self, app: str):
        self.exists_or_exception(app)
        packages = self.jsondata[app]
        packagesinstalled = []
        for package in packages:
            
        if packagesinstalled:
            return packagesinstalled
        return None