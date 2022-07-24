from os import listdir, mkdir
from shutil import move

formats = {
    'exe_msi':  ['exe', 'msi'],
    'media':    ['mp4', 'mp3', 'sfk', 'wav', 'avc', 'ogg', 'webm', 'mov', 'avi'],
    'image':    ['apng', 'png', 'gif', 'jpeg', 'svg', 'webp', 'ico', 'bmp', 'jpg'],
    'document': ['doc', 'docx', 'ppt', 'pptx', 'xlsx', 'pdf', 'txt', 'xml', 'PDF'],
    'achive':   ['7z', 's7z', 'rar', 'zip'],
    'torrent':  ['torrent']
}
created = []

def sorting_files(path):
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

if __name__ == '__main__':
    sorting_files(
        input('Введите путь до директории: ')
    )