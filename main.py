from os import listdir, mkdir, rename
from shutil import Error, move
from re import search
from copy import deepcopy


def find_max(formats) -> int:
    max_len = 0
    for name in formats:
        if max_len < len(name):
            max_len = len(name)
    return max_len

normal = {
    'exe_msi':  ['exe', 'msi'],
    'media':    ['mp4', 'mp3', 'sfk', 'wav', 'avc', 'ogg', 'webm', 'mov', 'avi'],
    'image':    ['apng', 'png', 'gif', 'jpeg', 'svg', 'webp', 'ico', 'bmp', 'jpg'],
    'document': ['doc', 'docx', 'ppt', 'pptx', 'xlsx', 'pdf', 'txt', 'xml', 'PDF'],
    'archive':   ['7z', 's7z', 'rar', 'zip'],
    'torrent':  ['torrent']
}

class Sorting:
    def __init__(self):
        self.new_formats = {}
        self.created = []
        self.formats = {}
        self.for_session = {}
        try:
            file = open('settings.txt', encoding='utf-8')
        except FileNotFoundError:
            file = open('settings.txt', 'w+', encoding='utf-8')
            max_len = find_max(normal)
            file.write('{\n')
            for i in normal:
                file.write(f"    '{i}':{' ' * (max_len-len(i))} {normal[i]},\n")
            file.write('}\n')
            file.close()
            file = open('settings.txt', encoding='utf-8')
        try:
            self.formats = eval(file.read())
        except:
            self.formats = deepcopy(normal)
        file.close()

    
    def sorting_files(self, path):
        dict_ = self.formats
        if self.for_session:
            dict_ = self.formats | self.for_session
        if '"' == path[0]:
            path = path[1:-1]
        filesList = listdir(path)
        for item in filesList:
            if item != item.split('.'):
                #isFile
                format = item.split('.')[-1]
                for i in dict_:
                    if format in dict_[i]:
                        if i not in self.created and i not in filesList:
                            mkdir(path+f'\{i}')
                            self.created.append(i)
                        try:
                            move(path+f'\{item}', path+f'\{i}')
                        except Error:
                            try:
                                dst = f"{item[:-(len(format)+1)]}(1).{format}"
                                rename(f"{path}\{item}", f"{path}\{dst}")
                            except OSError:
                                dst = f"{item[:-(len(format)+1)]}(2).{format}"
                                rename(f"{path}\{item}", f"{path}\{dst}")
                            move(path+f'\{dst}', path+f'\{i}')
    
    def print_formats(self):
        print('//////////////////////////////////////')
        dict_ = self.new_formats
        if self.for_session:
            dict_ = dict_ | self.for_session
        msg = 'Доступные расширения для сортировки:\n\nНазвание папки - [Расширения]\n'
        for i in dict_:
            msg += f"{i.ljust(find_max(dict_), ' ')}  -  {dict_[i]}\n"
        print(msg)

    def check_valid(self, sub:str, type:str):
        dict_ = deepcopy(self.new_formats)
        if self.for_session:
            dict_ = dict_ | self.for_session
            
        if search('[\w_]', sub):
            sym = ''
            for i in ('/', ':', '*', '?', '"', '<', '>', '|', '\ '.strip()):
                if sub.find(i) != -1:
                    sym += f'{i}, '
            if sym:
                print(f'\nНайдены неподдерживаемые символы: {sym[:-2]}\n')
                return 0
            
            if type == 'category':
                if sub not in dict_:
                    return 1
                else:
                    print('\nКатегория уже существует\n')
                    return 0
            elif type == 'format':
                if sub[0] == '.':
                    sub = sub[1:]
                for i in list(dict_.items()):
                    if sub in i[1]:
                        print(f'\nРасширение уже находится в категории {i[0]}\n')
                        return 0
                return 1
        else:
            print('\nНекорректное название\n')
            return 0


    def add_category(self, category):
        if self.check_valid(category, 'category'):
            self.new_formats[category] = []
            print('\nКатегория успешно добавлена\n')
            return 1
    
    def add_format(self, format, category):
        if self.check_valid(format, 'format'):
            if format[0] == '.':
                format = format[1:]
            
            if category in self.new_formats:
                self.new_formats[category].append(format)
                print(f'\nРасширение {format} успешно добавлено\n')
                return 1
            elif category in self.for_session:
                self.for_session[category].append(format)
                print(f'\nРасширение {format} успешно добавлено\n')
                return 1
            else:
                print('\nКатегории не существует\n')
                return 0
    
    def del_category(self, category):
        dict_ = deepcopy(self.new_formats)
        if self.for_session:
            dict_ = dict_ | self.for_session
        if category in dict_.keys():
            if category in self.new_formats.keys():
                del self.new_formats[category]
            elif category in self.for_session:
                del self.for_session[category]
            print('\nКатегория была успешно удалена\n')
            return 1
        else:
            print('\nКатегории не существует\n')
            return 0
    
    def del_format(self, format):
        dict_ = deepcopy(self.new_formats)
        if self.for_session:
            dict_ = dict_ | self.for_session
        if format[0] == '.':
            format = format[1:]
        for i in list(dict_.items()):
            if format in i[1]:
                try:
                    if format in self.for_session[i[0]]:
                        self.for_session[i[0]].remove(format)
                except KeyError:
                    pass
                if format in self.new_formats[i[0]]:
                    self.new_formats[i[0]].remove(format)
                print(f'\nРасширение {format} было успешно удалено из категории {i[0]}\n')
                return 1
        print(f'\nРасширение {format} не было найдено\n')
        return 0
    
    def reset(self):
        max_len = find_max(normal)
        f = open('settings.txt', 'w', encoding='utf-8')
        f.write('{\n')
        for i in normal:
            f.write(f"    '{i}':{' ' * (max_len-len(i))} {normal[i]}, \n")
        f.write('}\n')
        f.close()
        print('\nНастройки сортировки были сброшены к заводским\n')
        return 1


if __name__ == '__main__':
    obj = Sorting()
    main_input = '''Выберите действие:
    1 - Отсортировать файлы
    2 - Настройка сортировки
    '''
    settings_input = '''Выберите действие:
    1 - Добавить категорию
    2 - Добавить расширения в категорию
    3 - Удалить категорию
    4 - Удалить расширения
    5 - Сбросить к заводским настройкам
    6 - Вернуться в главное меню
    '''
    back_input =  '''Вы хотите сохранить изменения?
    1 - Да
    2 - Сохранить только для этой сессии
    3 - Нет
    '''
    name_input = '''Введите название для новой категории

    *Название может быть на английксом или русском языке. Не поддерживаются символы: \/:*?"<>|
    
    '''
    menu = True
    set_ = False
    exit = False
    main = input(main_input)
    
    while True:
        if menu:
            match main:
                case '1':
                    obj.sorting_files(
                        input('Введите путь до директории: ')
                    )
                    main = input(main_input)
                case '2':
                    menu = False
                    set_ = True
                    obj.new_formats = deepcopy(obj.formats)
                    obj.print_formats()
                    settings = input(settings_input)
                case _:
                    main = input('    ')
        elif set_:
            code = 0
            match settings:
                case '1':
                    name = input(name_input)
                    code = obj.add_category(name)
                case '2':
                    format = input('\nВведите расширения через запятую: ')
                    category = input('\nВведите название категории: ')
                    formats = format.split(',')
                    for i in formats:
                        format = i.strip()
                        code = obj.add_format(format, category)
                        if code == 0:
                            break
                case '3':
                    category = input('\nВведите название категории: ')
                    code = obj.del_category(category)
                case '4':
                    format = input('\nВведите расширения через запятую: ')
                    formats = format.split(',')
                    for i in formats:
                        format = i.strip()
                        code = obj.del_format(format)
                case '5':
                    code = obj.reset()
                    set_ = False
                    menu = True
                    main = input(main_input)
                case '6':
                    set_ = False
                    if obj.new_formats == obj.formats or not obj.new_formats:
                        menu = True
                        main = input(main_input)
                    else:
                        exit = True
                        back = input(back_input)
                case _:
                    settings = input('    ')
            if code:
                obj.print_formats()
            if settings != '5' and settings != '6':
                settings = input(settings_input)
        elif exit:
            exit = False
            menu = True
            if back in ('1', '2', '3'):
                if back == '1':
                    #save
                    obj.formats = deepcopy(obj.new_formats)
                    max_len = find_max(obj.formats)
                    f = open('settings.txt', 'w', encoding='utf-8')
                    f.write('{\n')
                    for i in obj.formats:
                        f.write(f"    '{i}':{' ' * (max_len-len(i))} {obj.formats[i]}, \n")
                    f.write('}\n')
                    f.close()
                elif back == '2':
                    #save for this session
                    obj.for_session = deepcopy(obj.new_formats)
                obj.new_formats = {}
                main = input(main_input)
            else:
                back = input('    ')
