# Photovoltaik
Die Photovoltaik Technik bildet einen grundlegenden Bestandteil dieses Projektes und wird daher an dieser Stelle genauer beleuchtet.

## Technik
Die Technik sollte jedem bekannt sein, falls dies nicht der Fall ist sind hier nochmal verschiedene Beschreibungen in ~aufsteigender Komplexität:

- [Planet Wissen](https://www.planet-wissen.de/technik/energie/solarenergie/index.html)
- [Solaranlagen-abc](https://www.solaranlagen-abc.de/funktion-photovoltaik/)
- [Wikipedia](https://de.wikipedia.org/wiki/Photovoltaik)
- [Fraunhofer Institut](https://www.ise.fraunhofer.de/content/dam/ise/de/documents/publications/studies/Photovoltaics-Report.pdf)
- [IOP-Science](https://iopscience.iop.org/article/10.1088/1361-6463/ab9c6a/pdf)

## gemessene Daten
Zu den Messdaten gehören verschiedene Größen. Primär gemessen wird die Leistung, welche von der PV-Anlage erzeugt wird. Diese wird mit mehreren Parametern in Verbindung gebracht um verglichen zu werden. Dazu gehören ein Zeitstempel und der Ort. Dieser ist bedeutsam, da an verschiedenen Orten verschiedene klimatische Bedingungen zu erwarten sind. Außerdem wichtig sind Informationen über die PV-Anlage selbst. Dies beinhaltet Daten über den Wechselrichter, die Anzahl an Zellen pro String und die Anzahl an Strings pro Wechselrichter. Ebenfalls notwendig ist die Information, wo im System die Leistung abgegriffen wird. Zu diesem Zeitpunkt wird davon ausgegangen, dass die Leistung am Wechselrichter gemessen wird.

### Leistung
Jede einzelne Solarzelle erzeugt eine Leistung auf einer bestimmten Spannung (z.B. 0,5V). Einzelne Solarzellen werden in Reihe zu Strings zusammen geschaltet. So wird die Spannung angehoben. (z.B. 50 Solarzellen * 0,5V = 25V) Über den Leistungsverlauf können Aussagen über den Zustand der Anlage gemacht werden. Dies ist Ziel des Projektes. Leider ist die Leistung nicht nur von der Anlage selbst abhängig, sondern auch von anderen Parametern, welche ständig Einfluss auf den Leistungsverlauf haben. Die wichtigsten dieser Parameter werden im Folgenden aufgelistet.

### Parameter

#### Sonneneinstrahlung

![Wetter](./Images/P_T_Wetter.jpg "Auswirkung der Sonneneinstrahlung")

#### Temperatur
![Temperatur](./Images/Temp_Auswirkung.jpg "Auswirkung der Temperatur auf die Leistungserzeugung")

#### Jahres- und Tagesverlauf

![Jahreszeit](./Images/P_T_Jahreszeit.jpg "Verteilung der Leistung über einem Jahr")

![Tagesverteilung_Jahresabhängig](./Images/P_T_Jahresverteilung.jpg "Verteilung der Leistung über verschiedenen Tagen im Jahr")

#### Neigung

![Ausrichtung](ausrichtung_neigung.jpg "Auswirkung der Neigung auf den Leistungsertrag")

## Fehler

Von Fehlern betroffene Zelle produzieren zum einen proportional zur fehlenden Fläche weniger Strom, zum Anderen beeinflusst dies die Leistung des gesamten Strings. Je nach Größe des abgetrennten Bereichs kann dies zum Abschalten eines Modulteilstrings über die Bypass-Diode führen. [energynet](https://www.energynet.de/2013/01/14/liste-5-fehler-photovoltaikmodule/)

Konstante Fehler:
- Verschmutzung
- Verschattung
- Leistungsnachlass

Sporadische Fehler
- Stromausfall
- Glasbruch
- Bewölkung
- Schlag-Störung
- Schnee
- Verschmutzung

Folgefehler
- Hotspots (nach Verschmutzung oder Verschattung)

## Defekt-Erkennung
Defekte an Photovoltaik Anlagen haben verschiedene Auswirkungen und können daher auf mehrere Arten ausgewertet werden. In diesem Projekt wird die Leistungs-Zeit Kurve untersucht.

### Leistungs-Zeit Kurve
Diese Kurve trägt die Leistung über der Zeit auf. Bei der Leistung handelt es sich um die Endgröße, welche das System erzeugt. Daher wirken sich alle Parameter auf diese Größe aus. Dies ergibt den Vorteil, dass jede Störung potentiell aus der Kurve erkannt werden kann. Gleichzeitig ergibt sich die Herausvorderung, Fehler zu erkennen und voneinander zu unterscheiden. Der Datensatz stellt die Leistungsmessung über mehrere Wochen/Monate dar.
Aufgaben:
- Untersuchen der Datensätze
  - Was bedeuten die einzelnen Spalten
  - Welche sind überhaupt wichtig
- Definition der Fehler (ist Verschmutzung ein Fehler?)
- Abgrenzung zwischen Fehlern und natürlichen Ereignissen
- Abgrenzung der Fehler untereinander

### Thermografie
Dieses Verfahren kann in diesem Projekt vermutlich nicht angewandt werden, da die nötigen Daten nicht vorliegen. Es wird hier der Vollständigkeit halber dennoch aufgeführt.

*Das Verfahren beruht darauf, dass Defekte in Solarmodulen lokal den elektrischen Widerstand erhöhen und somit zu einer Wärmeentwicklung führen. Daher sind defekte Stellen auf Wärmebildern im Allgemeinen gut zu erkennen.
Die Thermografie kann sowohl Risse in den Zellen als auch Verunreinigungen oder Schäden der Glasabdeckung sichtbar machen. In beiden Fällen beruht der Effekt auf einer lokalen Erhöhung des elektrischen Widerstands. Im Fall einer Beschädigung oder eines Produktionsfehlers des Moduls ist der Zusammenhang relativ offensichtlich. Aber auch eine eng lokalisierte Verschattung hat diesen Effekt, weil der Widerstand in verdunkelten Bereichen der Zelle deutlich höher ist.* [photovoltaik.org](https://www.photovoltaik.org/photovoltaikanlagen)

## Quellen

https://www.photovoltaik.org/photovoltaikanlagen
https://www.photovoltaik4all.de/blog/welche-rolle-spielt-die-temperatur-einer-photovoltaikanlage
https://www.pv-ertrag.com/neigung-und-ausrichtung/
https://www.energynet.de/2013/01/14/liste-5-fehler-photovoltaikmodule/