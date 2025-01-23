from testbench import data_treatement
import csv

# ouvle le csv de l'oscilloscope
with open("data/oscilloscope.csv", "r") as file:
    csv_reader = csv.reader(file)
    for row in csv_reader:
        print(row)
