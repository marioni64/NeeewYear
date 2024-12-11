import pandas as pd

file_path = 'FileNew.txt'
data = pd.read_csv(file_path, sep=';')

print(data)