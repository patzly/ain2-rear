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

import math
from utils import input_util as cinput
from utils import print_util as cprint

cache_size_storage = []
block_size_storage = []
way_count_storage = []


def required_bits(x):
    return int(math.log10(x) / math.log10(2))


def level_name(level):
    match level:
        case 1:
            return "Second"
        case 2:
            return "Third"
        case 3:
            return "Forth"
        case _:
            return "First"


def address_calculation():
    global cache_size_storage
    global block_size_storage
    global way_count_storage

    if not cache_size_storage or not block_size_storage or not way_count_storage:
        print("Anzahl Cache-Levels eingeben:")
        level_count = cinput.integer(1, 4)

        cache_size_storage = [0] * level_count
        block_size_storage = [0] * level_count
        way_count_storage = [0] * level_count

        for level in range(level_count):
            match level:
                case 1:
                    level_string = "Second"
                case 2:
                    level_string = "Third"
                case 3:
                    level_string = "Forth"
                case _:
                    level_string = "First"

            print("Cache-Größe des " + cprint.magenta("{}-Level-Cache".format(level_name(level)))
                  + " in Bytes (z.B. " + cprint.green("512") + ", " + cprint.green("64*16") + ") oder Blöcken (z.B. "
                  + cprint.green("#64") + ") eingeben:")
            cache_size = cinput.string()
            cache_size_blocks = None
            if "#" in cache_size:
                cache_size_blocks = int(cache_size.replace("#", "").strip())
            elif "*" in cache_size:
                operators = cache_size.split("*")
                cache_size = int(math.prod(int(x) for x in operators))
                cache_size_storage[level] = cache_size
                print("Berechnete Cache-Größe:", cache_size, "Bytes")
            else:
                cache_size = int(cache_size)
                cache_size_storage[level] = cache_size

            print("Block-Größe des " + cprint.magenta("{}-Level-Cache".format(level_string))
                  + " in Bytes eingeben:".format(level_string))
            block_size = cinput.integer(0, None)
            block_size_storage[level] = block_size

            if cache_size_blocks is not None:
                # Calculate cache size if it was given in blocks
                cache_size = cache_size_blocks * block_size
                cache_size_storage[level] = cache_size
                print("Berechnete Cache-Größe:", cache_size, "Bytes")

            print("Anzahl Ways des " + cprint.magenta("{}-Level-Cache".format(level_string))
                  + " in Bytes eingeben (direct-mapped = 1):".format(level_string))
            way_count = cinput.integer(1, None)
            way_count_storage[level] = way_count

    print("Speicheradresse eingeben:")
    address = cinput.integer(0, None)

    for level in range(len(cache_size_storage)):
        cache_size = cache_size_storage[level]
        block_size = block_size_storage[level]
        way_count = way_count_storage[level]

        print(cprint.magenta_bold("{}-Level-Cache (".format(level_name(level)) + str(way_count) + "-Way, "
                                  + str(cache_size) + " Bytes, " + str(block_size) + "-Byte-Blöcke)"))

        block_count = int(cache_size / block_size)
        print(cprint.bold("Anzahl Blöcke: ")
              + "(Cache-Größe / Block-Größe) = (" + str(cache_size) + " / " + str(block_size) + ") = "
              + cprint.yellow_bold(block_count))

        set_count = int(block_count / way_count)
        if way_count != 1:
            print(cprint.bold("Anzahl Sets: ")
                  + "(Anzahl Blöcke / Anzahl Ways) = (" + str(block_count) + " / " + str(way_count) + ") = "
                  + cprint.yellow_bold(set_count))

        block_number = int(math.floor(address / block_size))
        print(cprint.bold("Blocknummer: ")
              + "(floor(Adresse / Block-Größe)) = (floor(" + str(address) + " / " + str(block_size) + ")) = "
              + cprint.yellow_bold(block_number))

        block_index = int(block_number % block_count)
        block_index_bits = required_bits(block_count)
        print(cprint.bold("Block-Index: ")
              + "(Blocknummer % Anzahl Blöcke) = (" + str(block_number) + " % " + str(block_count) + ") = "
              + cprint.yellow_bold(block_index)
              + " (2^{} = {} ⇒ max. {} Bits)".format(block_index_bits, block_count, block_index_bits))

        if way_count != 1:
            set_index = int(block_number % set_count)
            set_index_bits = required_bits(set_count)
            print(cprint.bold("Set-Index: ")
                  + "(Blocknummer % Anzahl Sets) = (" + str(block_number) + " % " + str(set_count) + ") = "
                  + cprint.yellow_bold(set_index)
                  + " (2^{} = {} ⇒ max. {} Bits)".format(set_index_bits, set_count, set_index_bits))

        tag = int(math.floor(block_number / set_count))
        print(cprint.bold("Tag: ")
              + "(floor(Blocknummer / Anzahl Sets)) = (floor(" + str(block_number) + " / " + str(set_count) + ")) = "
              + cprint.yellow_bold(tag))

        byte_offset = int(address % block_size)
        byte_offset_bits = required_bits(block_size)
        print(cprint.bold("Byte-Offset: ")
              + "(Adresse % Block-Größe) = (" + str(address) + " % " + str(block_size) + ") = "
              + cprint.yellow_bold(byte_offset)
              + " (2^{} = {} ⇒ max. {} Bits)\n".format(byte_offset_bits, block_size, byte_offset_bits))

    print(cprint.blue_bold("Optionen:\n") +
          cprint.bold(1) + " Neue Adresse, gleiche Caches\n" +
          cprint.bold(2) + " Neue Adresse, neue Caches\n" +
          cprint.bold(3) + " Menü")

    match cinput.integer(1, 3):
        case 1:
            address_calculation()
        case 2:
            cache_size_storage = []
            block_size_storage = []
            way_count_storage = []
            address_calculation()
        case 3:
            menu()


def dirty_calculation():
    print("Anzahl Sets des Cache-Levels, in welchem der Block sich befindet, eingeben:")
    set_count = cinput.integer(1, None)
    print("Set-Index des Blocks eingeben:")
    set_index = cinput.integer(0, None)
    print("Tag des Blocks eingeben:")
    tag = cinput.integer(0, None)
    print("Anzahl Sets des neuen Cache-Levels eingeben:")
    set_count_up = cinput.integer(0, None)

    print(cprint.magenta_bold("Angaben für neues Cache-Level:"))

    block_number_up = int(set_index + tag * set_count)
    print(cprint.bold("Blocknummer: ")
          + "(Set-Index + Tag * Anzahl Sets) = (" + str(set_index) + " + " + str(tag) + " * " + str(set_count) + ") = "
          + cprint.yellow_bold(block_number_up))

    set_index_up = int(block_number_up % set_count_up)
    print(cprint.bold("Set-Index: ")
          + "(Blocknummer % Anzahl Sets) = (" + str(block_number_up) + " % " + str(set_count_up) + ") = "
          + cprint.yellow_bold(set_index_up))

    tag_up = int(math.floor(block_number_up / set_count_up))
    print(cprint.bold("Tag: ")
          + "(floor(Blocknummer / Anzahl Sets)) = (floor(" + str(block_number_up) + " / " + str(set_count_up) + ")) = "
          + cprint.yellow_bold(tag_up))

    print(cprint.blue_bold("\nOptionen:\n") +
          cprint.bold(1) + " Funktion wiederholen\n" +
          cprint.bold(2) + " Menü")

    match cinput.integer(1, 2):
        case 1:
            dirty_calculation()
        case 2:
            menu()


def menu():
    global cache_size_storage
    cache_size_storage = []
    global block_size_storage
    block_size_storage = []
    global way_count_storage
    way_count_storage = []

    print(cprint.blue_bold("Menü:\n") +
          cprint.bold(1) + " Adressrechnung\n" +
          cprint.bold(2) + " Set-Index & Tag für anderes Cache-Level berechnen")

    match cinput.integer(1, 2):
        case 1:
            address_calculation()
        case 2:
            dirty_calculation()


print("Cache Calculator v1.0.2")
print(cprint.yellow("Viel Erfolg!\n"))
menu()

"""
Nicht im Programm enthaltene Formeln bezüglich Caching

# Hit-Ratio = Hits / Zugriffe
# Miss-Ratio = Misses / Zugriffe = 1 - Hit-Ratio
# Effektiver CPI = CPI + (Anteil Store-Instruktionen) * (Dauer des Speicherns eines Wortes in Takten)
# Memory Stall Cycles = (Memory accesses / Program) * Miss-Rate * Miss-Penalty
# Memory Stall Cycles = (Instructions / Program) * (Misses / Instruction) * Miss-Penalty
# Effektiver CPI: CPI + (Durchschnitt Memory-Miss-Cycles pro Instruktion, je nach Aufbau Addition mehrerer Caches)
# AMAT (Average Memory Access Time) = Hit-Time + Miss-Rate * Miss-Penalty

Allgemeine Begriffe

# Block: kleinste Speichereinheit, die zwischen Hierarchie-Ebenen kopiert wird
# Hit: von oberer Ebene angefragter Speicherinhalt ist vorhanden
# Hit-Ratio: Anteil erfolgreicher Speicherzugriffe
  Hit-Ratio = Hits / Zugriffe
# Miss: Block ist nicht vorhanden und muss von nächster Ebene nachgeladen werden
# Miss-Penalty: Dauer, um Block "nachzuladen"
# Miss-Ratio: Anteil nachzuladender Blöcke
  Miss-Ratio = Misses / Zugriffe = 1 - Hit-Ratio
  
1. Direct Mapped Cache

# Byte-Offset: Adressierung innerhalb eines Blocks
  Anzahl benötigter Bits: 2^x = Block-Größe in Bytes, z.B. 2^4 = 16, da 4 Bits benötigt, um binär bis 16 zu zählen
# Block-Index: Adressierung innerhalb des Caches
  Anzahl benötigter Bits: 2^x = Cache-Größe in Bytes, z.B. 2^6 = 64, da 6 Bits benötigt, um binär bis 64 zu zählen
# Tag: höherwertige Bits der Daten-Adresse, um Blöcke im Cache zuordnen zu können
# Cache-Hit: wenn V(Index) = Y und Tag(Index) = Tag, benötigte Daten sind vorhanden
  Data-Write-Hit: Wort wird in Speicherblock geschrieben, der im Cache vorhanden und valid ist
    Write-Through: Wort wird im Cache und direkt auch im Hauptspeicher geändert
      Nachteil: Schreiben dauert länger
      Effektiver CPI = CPI + (Anteil Store-Instruktionen) * (Dauer des Speicherns eines Wortes in Takten)
      Effektiver CPI = 1 + 0.1*100 = 11
    Write-Back: Wort wird nur im Cache geändert und Block als dirty markiert
      Beim Ersetzen des Blocks werden die Daten zurückgeschrieben
      Nachteil: inkonsistente Daten in Cache und Hauptspeicher, Ersetzen dauert länger
      Vorteil: weniger Schreib-Operationen
    Write-Buffer: speichert Daten zwischen, die in den Hauptspeicher geschrieben werden müssen
      CPU kann direkt weiterarbeiten, muss nur stoppen, falls der Buffer voll ist
      Einsatz bei Write-Through und Write-Back
# Dirty: Wort zunächst nur im Cache geändert und Block als geändert (dirty) markiert
  Erst beim Ersetzen des Blocks werden die Daten zurückgeschrieben
# Cache-Miss: Pipeline wird gestoppt (Stall), Block wird von der nächsten Ebene der Speicherhierarchie geladen
    Write-Through:
      Allocate on miss: Daten in Hauptspeicher schreiben und Block in Cache laden
      Write around: Daten nur in Hauptspeicher und Block nicht in Cache laden
    Write-Back: Daten in Hauptspeicher schreiben und Block in Cache laden
# Memory Stall Cycles (Speicher-Stalls): Pipeline muss wegen Speicherzugriffen (verursacht durch Cache-Misses) warten
  Memory Stall Cycles = (Memory accesses / Program) * Miss-Rate * Miss-Penalty
  Memory Stall Cycles = (Instructions / Program) * (Misses / Instruction) * Miss-Penalty
# Effektiver CPI: CPI + (Durchschnitt Memory-Miss-Cycles pro Instruktion, je nach Aufbau Addition mehrerer Caches)
  Durchschnitt Memory-Miss-Cycles pro Instruktion = Miss-Rate * Miss-Penalty
    Wenn Daten-Cache: Miss-Rate * Miss-Penalty * Anteil Lade- und Speicherbefehle
  Beispiel (System mit getrennten Instruktion- und Daten-Cache):
    Miss-Penalty = 100 Takte, CPI (bei 100% Hit-Rate) = 2, Anteil Lade- und Speicherbefehle = 36%
    Miss-Rate = 2% (Instruktion-Cache), 4% (Daten-Cache)
    Durchschnitt Memory-Miss-Cycles pro Instruktion (Instruktion-Cache) = 0.02 * 100 = 2
    Durchschnitt Memory-Miss-Cycles pro Instruktion (Daten-Cache) = 0.36 * 0.04 * 100 = 1.44
    Effektiver CPI = 2 + 2 + 1.44 = 5.44 -> Ideale CPU (100% Hit-Rate) ist über zweieinhalb-mal schneller
# Hit-Time: Speicherzugriffsdauer im Falle eines Hits
# AMAT (Average Memory Access Time): mittlere Speicherzugriffszeit
  AMAT = Hit-Time + Miss-Rate * Miss-Penalty
  Beispiel: CPU mit 1ns Taktung, Hit-Time = 1 Takt, Miss-Rate = 5%, Miss-Penalty = 20 Takte
    AMAT = 1 + 0.05 * 20 = 2ns -> im Mittel 2 Zyklen pro Load-/Store-Instruktion  
    
2. Assoziative Caches

# Assoziatives Feld: Zugriff auf Feld über Key und nicht über Index, Abbildung Key auf Index wird separat gespeichert
# Assoziativer Cache:
  Fully-Associative Cache: beliebige Zuordnung von Speicherblock auf Cache-Block
    Vorteil: wichtige Blöcke können im Cache gehalten werden
    Nachteil: aufwändiges Überprüfen von allen Cache-Blöcken auf Treffer
  N-Way-Set-Associative Cache: Kompromiss zwischen Direct-Mapped und Fully-Associative Cache
    Einteilung des Caches in Speicherbereiche (Sets) mit jeweils N Blöcken
    Direct-Mapped-Zugriff auf Sets
    Associative-Zugriff innerhalb der Sets
# Cache-Größe = Anzahl Sets * Blöcke pro Set * Bytes pro Block
# Ersetzen von Cache-Blöcken: bei einem Miss wird der benötigte Block in den Cache geladen und ersetzt existierenden
  Direct-Mapped -> keine Auswahl, Associative-Cache -> es kann entschieden werden, welcher Block im Set ersetzt wird
  Zuerst invalid Blocks ersetzen, falls keine invalid sind, entweder
    Least-Recently-Used (LRU): Ersetzen des Blocks, für den der letzte Zugriff am längsten zurückliegt
    Random: zufällige Wahl des zu ersetzenden Blocks, bei hoher Assoziativität (große Sets) ähnlich performant wie LRU
# Cache-Hierarchie: mehrere Caches (Level 1-n) mit verschiedenen Geschwindigkeiten hintereinander geschaltet
  L1-Cache: bei Miss in L2 nachschauen, ob Daten dort vorhanden, wenn ja, Daten aus L2 in CPU laden und in L1 speichern
  L2-Cache: bei Miss in L3 nachschauen, ob Daten dort vorhanden, wenn ja, Daten aus L3 laden und in L2 & L1 speichern
  L3-Cache: bei Miss Daten aus Hauptspeicher laden und in L3 & L2 & L1 speichern
"""
