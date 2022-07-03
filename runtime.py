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

"""
# CPU-Ausführungszeit (CPU-Zeit): Zeit, während der die CPU für die Bewältigung einer Aufgabe aktiv ist,
  wird bestimmt durch Taktgeschwindigkeit und Anzahl der Taktzyklen, besteht aus
  Benutzer-CPU-Zeit: Anteil der CPU-Zeit für die Abarbeitung innerhalb eines Programms
  System-CPU-Zeit: Anteil der CPU-Zeit für die Abarbeitung von Betriebssystemaufrufen für ein Programm
  CPU-Zeit eines Programms = (Anzahl CPU Taktzyklen für das Programm) / (Taktgeschwindigkeit der CPU)
# Prozessortakt: bestimmt, wann Ereignisse innerhalb der Hardware ausgeführt werden
# Taktzyklus: Zeit für ein Intervall (auch Tick, Taktintervall oder Takt)
  Taktzyklen = Ausführungszeit [s] * Taktgeschwindigkeit [GHz]
# Taktgeschwindigkeit: Anzahl Taktintervalle pro Zeiteinheit
  Taktgeschwindigkeit [GHz] = Taktzyklen / Ausführungszeit [s]
# Anzahl CPU Taktzyklen = (Anzahl Instruktionen) * CPI
"""
