import pandas as pd

file_path = 'FileNew.txt'

try:
    gift_data = pd.read_csv(file_path, delim_whitespace=True, encoding='utf-8')


    print("Столбцы в данных:", gift_data.columns)
    print("Первые строки данных:")
    print(gift_data.head())

    print("\nВсе GiftId:")
    print(gift_data['GiftId'])

except Exception as e:
    print(f"Ошибка при чтении файла: {e}")