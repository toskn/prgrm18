

filename = input('Введите название файла с расширением: ')
with open(filename, encoding='utf-8') as file:
    file = file.read()
    file = file.replace('{', '')
    file = file.replace('}', ' ')
    file = file.replace('??', '')
    print(file)
