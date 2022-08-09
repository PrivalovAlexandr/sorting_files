from os import listdir, mkdir
from shutil import move
from re import search



normal = {
    'exe_msi':  ['exe', 'msi'],
    'media':    ['mp4', 'mp3', 'sfk', 'wav', 'avc', 'ogg', 'webm', 'mov', 'avi'],
    'image':    ['apng', 'png', 'gif', 'jpeg', 'svg', 'webp', 'ico', 'bmp', 'jpg'],
    'document': ['doc', 'docx', 'ppt', 'pptx', 'xlsx', 'pdf', 'txt', 'xml', 'PDF'],
    'achive':   ['7z', 's7z', 'rar', 'zip'],
    'torrent':  ['torrent']
}

created = []



def create_formats() -> dict:
    file = open('settings.txt')
    formats = {}
    for line in file:
        formats[line[:line.find(':')]] = eval(line[line.find('['):])
    return formats

def sorting_files(path):
    formats = create_formats()
    if '"' == path[0]:
        path = path[1:-1]
    filesList = listdir(path)
    for item in filesList:
        if item != item.split('.'):
            #isFile
            format = item.split('.')[-1]
            for i in formats:
                if format in formats[i]:
                    if i not in created and i not in filesList:
                        mkdir(path+f'\{i}')
                        created.append(i)
                    move(path+f'\{item}', path+f'\{i}')

def print_formats():
    formats = create_formats()
    msg = 'Доступные форматы для сортировки:\n\nНазвание папки - [Форматы]\n'
    max_len = 0
    for name in formats:
        if max_len < len(name):
            max_len = len(name)
    for i in formats:
        msg += f"{i}{' ' * (max_len-len(i))}  -  {formats[i]}\n"
    print(msg)
    
def add_category():
    formats = create_formats()
    name = input('Введите название для новой категории\n*Название может быть на английксом или русском. Не поддерживаются символы: \/:*?"<>|\n')
    if search('[a-zA-zа-яА-Я0-9]', name) and name not in formats:
        print('yes')


if __name__ == '__main__':
    add_category()
    #choice = input(
    #    'Выберите действие:\n\n1 - Отсортировать файлы\n2 - Настройка сортировки')
    #match choice:
    #    case '1':
    #        sorting_files(
    #            input('Введите путь до директории: ')
    #        )
    #    case '2':
    #        print_formats()
    #        sec_choice = input(
    #            '''Выберите действие:
    #            1 - Добавить категорию
    #            2 - Добавить формат в категорию
    #            3 - Удалить категорию
    #            4 - Удалить формат из категории
    #            5 - Выйти
    #            ''')