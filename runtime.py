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
