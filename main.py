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

normal = {
    'exe_msi':  ['exe', 'msi'],
    'media':    ['mp4', 'mp3', 'sfk', 'wav', 'avc', 'ogg', 'webm', 'mov', 'avi'],
    'image':    ['apng', 'png', 'gif', 'jpeg', 'svg', 'webp', 'ico', 'bmp', 'jpg'],
    'document': ['doc', 'docx', 'ppt', 'pptx', 'xlsx', 'pdf', 'txt', 'xml', 'PDF'],
    'achive':   ['7z', 's7z', 'rar', 'zip'],
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
            for i in normal:
                file.write(f"{i}:{' ' * (max_len-len(i))} {normal[i]}\n")
            file.close()
            file = open('settings.txt', encoding='utf-8')
        if search('[a-zA-zа-яА-я0-9.]', file.read()):
            for line in file:
                if line != '\n':
                    self.formats[line[:line.find(':')]] = eval(line[line.find('['):])
        else:
            self.formats = deepcopy(normal)
        file.close()

    
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
        if self.for_session:
            dict_ = dict_ | self.for_session
        msg = 'Доступные форматы для сортировки:\n\nНазвание папки - [Форматы]\n'
        for i in dict_:
            msg += f"{i.ljust(find_max(dict_), ' ')}  -  {dict_[i]}\n"
        print(msg)
        print('//////////////////////////////////////')

    def check_valid(self, sub:str, type:str):
        if self.new_formats:
            somedict = deepcopy(self.new_formats)
        else:
            somedict = deepcopy(self.formats)
        if self.for_session:
            somedict = somedict | self.for_session
            
        if search('[a-zA-zа-яА-я0-9.]', sub):
            sym = ''
            for i in ('/', ':', '*', '?', '"', '<', '>', '|', '\ '.strip()):
                if sub.find(i) != -1:
                    sym += f'{i}, '
            if sym:
                print(f'\nНайдены неподдерживаемые символы: {sym[:-2]}\n')
                return 0
            
            if type == 'category':
                if sub not in somedict:
                    return 1
                else:
                    print('\nДанная категория уже существует\n')
                    return 0
            elif type == 'format':
                if sub[0] == '.':
                    sub = sub[1:]
                for i in list(somedict.items()):
                    if sub in i[1]:
                        print(f'\nДанный формат уже находится в категории {i[0]}\n')
                        return 0
                return 1
        else:
            print('\nНекорректное название\n')
            return 0

    def add_category(self, category):
        if self.check_valid(category, 'category'):
            if not self.new_formats:
                self.new_formats = deepcopy(self.formats)

            self.new_formats[category] = []
            print('\nКатегория успешно добавлена\n')
            return 1
    
    def add_format(self, format, category):
        if self.check_valid(format, 'format'):
            if format[0] == '.':
                format = format[1:]
            if not self.new_formats:
                self.new_formats = deepcopy(self.formats)

            if category in self.new_formats:
                self.new_formats[category].append(format)
                print('\nФормат успешно добавлен\n')
                return 1
            elif category in self.for_session:
                self.for_session[category].append(format)
                print('\nФормат успешно добавлен\n')
                return 1
            else:
                print('\nВведенной категории не существует\n')
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
                case '2':
                    menu = False
                    set_ = True
                    obj.print_formats()
                    settings = input(settings_input)
                case _:
                    main = input('    ')
        elif set_:
            match settings:
                case '1':
                    name = input(name_input)
                    if obj.add_category(name):
                        obj.print_formats()
                    settings = input(settings_input)
                case '2':
                    #добавление нескольких форматов в категорию
                    format = input('\nВведите формат: ')
                    cat = input('\nВведите название категории: ')
                    if obj.add_format(format, cat):
                        obj.print_formats()
                    settings = input(settings_input)
                case '3':
                    pass
                case '4':
                    pass
                case '5':
                    pass
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
        elif exit:
            exit = False
            menu = True
            if back in ('1', '2', '3'):
                if back == '1':
                    #save
                    obj.formats = deepcopy(obj.new_formats)
                    max_len = find_max(obj.formats)
                    f = open('settings.txt', 'w', encoding='utf-8')
                    for i in obj.formats:
                        f.write(f"{i}:{' ' * (max_len-len(i))} {obj.formats[i]}\n")
                    f.close()
                elif back == '2':
                    #save for this session
                    obj.for_session = deepcopy(obj.new_formats)
                obj.new_formats = {}
                main = input(main_input)
            else:
                back = input('    ')
