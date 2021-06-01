import plot_simulation

data_sets = [
    plot_simulation.DataFetcherSimulated(r'../Daten_Simuliert/daten_schatten.xls', '1subs_moving shadow', ['Time', 'S', 'T', 'S1', 'P', 'V', 'I']),
    plot_simulation.DataFetcherSimulated(r'../Daten_Simuliert/daten_schatten.xls', '2subs_fixed shadow', ['Time', 'S', 'T', 'S1', 'P', 'V', 'I']),
    plot_simulation.DataFetcherSimulated(r'../Daten_Simuliert/daten_schatten.xls', '2subs_moving shadow', ['Time', 'S', 'T', 'S1', 'P', 'V', 'I'])
]

data_sets[1].plot_data()
data_sets[2].plot_data()

plot_simulation.plot_mult(data_sets, 'V', 'I', 'Diodenkennlinie', 'Voltage', 'Current')


plot_simulation.plot_mult(data_sets, 'S', 'P', 'Verlauf der Leistung abhängig von der Einstrahlung', 'Irradiance', 'Power')
plot_simulation.plot_mult(data_sets, 'S', 'V', 'Verlauf der Spannung abhängig von der Einstrahlung', 'Irradiance', 'Voltage')
plot_simulation.plot_mult(data_sets, 'S', 'I', 'Verlauf des Stromes abhängig von der Einstrahlung', 'Irradiance', 'Current')


plot_simulation.plot_mult(data_sets, 'T', 'P', 'Verlauf der Leistung abhängig von der Temperatur', 'Temperature', 'Power')
plot_simulation.plot_mult(data_sets, 'T', 'V', 'Verlauf der Spannung abhängig von der Temperatur', 'Temperature', 'Voltage')
plot_simulation.plot_mult(data_sets, 'T', 'I', 'Verlauf des Stromes abhängig von der Temperatur', 'Temperature', 'Current')