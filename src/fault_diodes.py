"""
"  python script to analyse simulated data.
"  This script used the functionality defined in plot_simulation.
"  It plots the data generated to simulate faulty diodes.
"  Graphics will be stored in data/plots
"  Script: fault_diodes.py
"  Version: 1.1
"""

import plot_simulation

data_sets = [
    plot_simulation.DataFetcherSimulated(r'../Daten_Simuliert/daten_defekteDioden.xls', '1subs_1BD', ['Time', 'S', 'T', 'T1', 'P', 'V', 'I']),
    plot_simulation.DataFetcherSimulated(r'../Daten_Simuliert/daten_defekteDioden.xls', '1subs_2BD', ['Time', 'S', 'T', 'T1', 'P', 'V', 'I']),
    plot_simulation.DataFetcherSimulated(r'../Daten_Simuliert/daten_defekteDioden.xls', '1subs_3BD', ['Time', 'S', 'T', 'T1', 'P', 'V', 'I']),
    plot_simulation.DataFetcherSimulated(r'../Daten_Simuliert/daten_defekteDioden.xls', '2subs_1BD', ['Time', 'S', 'T', 'T1', 'P', 'V', 'I']),
    plot_simulation.DataFetcherSimulated(r'../Daten_Simuliert/daten_defekteDioden.xls', '2subs_2BD', ['Time', 'S', 'T', 'T1', 'P', 'V', 'I']),
    plot_simulation.DataFetcherSimulated(r'../Daten_Simuliert/daten_defekteDioden.xls', '2subs_3BD', ['Time', 'S', 'T', 'T1', 'P', 'V', 'I'])
]

plot_simulation.plot_mult(data_sets, 'V', 'I', 'Diodenkennlinie', 'Voltage', 'Current')


plot_simulation.plot_mult(data_sets, 'S', 'P', 'Verlauf der Leistung abhängig von der Einstrahlung', 'Irradiance', 'Power')
plot_simulation.plot_mult(data_sets, 'S', 'V', 'Verlauf der Spannung abhängig von der Einstrahlung', 'Irradiance', 'Voltage')
plot_simulation.plot_mult(data_sets, 'S', 'I', 'Verlauf des Stromes abhängig von der Einstrahlung', 'Irradiance', 'Current')
print(data_sets[0].info)

plot_simulation.plot_mult(data_sets, 'T1', 'P', 'Verlauf der Leistung abhängig von der Temperatur', 'Temperature', 'Power')
plot_simulation.plot_mult(data_sets, 'T1', 'V', 'Verlauf der Spannung abhängig von der Temperatur', 'Temperature', 'Voltage')
plot_simulation.plot_mult(data_sets, 'T1', 'I', 'Verlauf des Stromes abhängig von der Temperatur', 'Temperature', 'Current')