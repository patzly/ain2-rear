#  This file is part of Cache Calculator.
#
#  Cache Calculator is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  Cache Calculator is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with Cache Calculator. If not, see <http://www.gnu.org/licenses/>.
#
#  Copyright (c) 2022 by Patrick Zedler

from utils import print_util as cprint


def invalid():
    print(cprint.red("Ungültige Eingabe. Erneut versuchen:"))


def string():
    # Prevent KeyboardInterrupt from being thrown when program is stopped
    try:
        return input().strip()
    except (KeyboardInterrupt, EOFError):
        raise SystemExit(0)


def integer(mini=None, maxi=None):
    # Prevent ValueError from being thrown when input is not a number or not in min max bounds
    try:
        user = int(string())
    except ValueError:
        invalid()
        return integer(mini, maxi)

    if mini is not None and maxi is not None:
        if mini <= user <= maxi:
            return user
        else:
            invalid()
            return integer(mini, maxi)
    elif mini is not None and maxi is None:
        if user >= mini:
            return user
        else:
            invalid()
            return integer(mini, maxi)
    elif mini is None and maxi is not None:
        if user <= maxi:
            return user
        else:
            invalid()
            return integer(mini, maxi)
    else:
        return user
