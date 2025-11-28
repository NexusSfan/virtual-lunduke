"""Detection systems"""

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

import shutil
from . import binary, apt, pacman


def get_detection_system():
    apt_binary = shutil.which("apt")
    pacman_binary = shutil.which("pacman")
    dnf_binary = shutil.which("dnf")
    if apt_binary:
        return (apt.AptDetectionSystem, "apt")
    if pacman_binary:
        return(pacman.PacmanDetectionSystem, "pacman")
    # todo: implement dnf
    return (binary.BinDetectionSystem, "bin")
