from os import listdir, mkdir
from shutil import move
from re import search
from copy import deepcopy



def find_max(formats) -> int:
    max_len = 0
    for name in formats:
        if max_len < len(name):
            max_len = len(name)
    return max_len

class Sorting:
    def __init__(self):
        self.new_formats = {}
        self.created = []
        self.formats = {}
        file = open('settings.txt')
        for line in file:
            self.formats[line[:line.find(':')]] = eval(line[line.find('['):])
        file.close()
        #чек на пустой файл

    
    def sorting_files(self, path):
        if '"' == path[0]:
            path = path[1:-1]
        filesList = listdir(path)
        for item in filesList:
            if item != item.split('.'):
                #isFile
                format = item.split('.')[-1]
                for i in self.formats:
                    if format in self.formats[i]:
                        if i not in self.created and i not in filesList:
                            mkdir(path+f'\{i}')
                            self.created.append(i)
                        move(path+f'\{item}', path+f'\{i}')
    
    def print_formats(self):
        print('//////////////////////////////////////')
        if self.new_formats:
            dict_ = self.new_formats
        else:
            dict_ = self.formats
        msg = 'Доступные форматы для сортировки:\n\nНазвание папки - [Форматы]\n'
        max_len = find_max(dict_)
        for i in dict_:
            msg += f"{i}{' ' * (max_len-len(i))}  -  {dict_[i]}\n"
        print(msg)
        print('//////////////////////////////////////')

    def add_category(self, name):
        if not self.new_formats:
            self.new_formats = deepcopy(self.formats)
        if search('[a-zA-z0-9]', name) and name not in self.new_formats:
            self.new_formats[name] = []
            print('\nКатегория успешно добавлена\n')
            return 1
        else:
            print('\nНекорректное название категории\n')
            return 0

if __name__ == '__main__':
    obj = Sorting()
    main_input = '''Выберите действие:
    1 - Отсортировать файлы
    2 - Настройка сортировки
    '''
    settings_input = '''Выберите действие:
    1 - Добавить категорию
    2 - Добавить формат в категорию
    3 - Удалить категорию
    4 - Удалить формат из категории
    5 - Вернуться в главное меню
    '''
    back_input =  '''Вы хотите сохранить изменения?
    1 - Да
    2 - Сохранить только для этой сессии
    3 - Нет
    '''
    menu = True
    set = False
    exit = False
#сохранение настроек при выходе из меню
    main = input(main_input)
    while True:
        if menu:
            match main:
                case '1':
                    obj.sorting_files(
                        input('Введите путь до директории: ')
                    )
                case '2':
                    menu = False
                    set = True
                    obj.print_formats()
                    settings = input(settings_input)
                case _:
                    main = input('    ')
        elif set:
            match settings:
                case '1':
                    name = input('Введите название для новой категории\n*Название может быть только на английксом языке. Не поддерживаются символы: \/:*?"<>|\n')
                    if obj.add_category(name):
                        obj.print_formats()
                    settings = input(settings_input)
                case '2':
                    pass
                case '3':
                    pass
                case '4':
                    pass
                case '5':
                    set = False
                    if obj.new_formats == obj.formats or not obj.new_formats:
                        menu = True
                        main = input(main_input)
                    else:
                        exit = True
                        back = input(back_input)
                case _:
                    settings = input('    ')

        elif exit:
            exit = False
            menu = True
            match back:
                case '1':
                    obj.formats = deepcopy(obj.new_formats)
                    obj.new_formats = {}
                    max_len = find_max(obj.formats)
                    f = open('settings.txt', 'w')
                    for i in obj.formats:
                        f.write(f"{i}:{' ' * (max_len-len(i))} {obj.formats[i]}\n")
                    f.close()
                    main = input(main_input)
                case '2':
                    pass
                case '3':
                    pass
                case _:
                    back = input('    ')
