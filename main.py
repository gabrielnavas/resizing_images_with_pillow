import os
from PIL import Image
from typing import Union
import time


def verify_path(main_images_folter: str):
    assert isinstance(main_images_folter,
                      str), 'main_images_folter is not str type'
    if not os.path.isdir(main_images_folter):
        raise NotADirectoryError(f'{main_images_folter} is not exists')


def verify_new_width(new_width: int):
    assert isinstance(new_width,
                      int), 'new_width is not int type'
    if not os.path.isdir(main_images_folter):
        raise NotADirectoryError(f'{main_images_folter} is not exists')


def make_paths(root: Union[bytes, str], file: Union[bytes, str]) -> (str, str):
    file_full_path = os.path.join(root, file)
    file_name, extension = os.path.splitext(file)
    converted_tag = '__CONVERTED'
    new_file = f'{file_name}{converted_tag}{extension}'
    new_file_full_path = os.path.join(root, new_file)
    return file_full_path, converted_tag, new_file_full_path


def verify_files_duplicated(converted_tag: str, file_full_path: str):
    return converted_tag in file_full_path


def make_new_height(new_width, height_old, width_old):
    return round((new_width * height_old) / width_old)


def make_new_picture(root: Union[bytes, str], file: Union[bytes, str], new_width: int, verbose: bool) -> None:

    file_full_path, converted_tag, new_file_full_path = make_paths(root, file)
    if verify_files_duplicated(converted_tag, file_full_path):
        return

    if verbose:
        msg = f'[ * ] MAKING: {new_file_full_path}'
        print(msg)

    img_pillow = Image.open(file_full_path)

    width, height = img_pillow.size
    new_height = make_new_height(new_width=new_width,
                                 height_old=height, width_old=width)

    new_image = img_pillow.resize(
        (new_width, new_height), Image.LANCZOS)
    new_image.save(new_file_full_path, optimize=True, quality=70)

    new_image.close()
    img_pillow.close()


def main(main_images_folter: str, new_width: int = 800, verbose: bool = False):
    verify_path(main_images_folter)
    verify_new_width(new_width)

    total_pictures = 0
    for root, dirs, files in os.walk(main_images_folter):
        total_pictures += len(files)
        for file in files:
            make_new_picture(root, file, new_width, verbose)

    print('[ * ] FINISHES WITH {total_pictures} PICTURES.')


if __name__ == '__main__':
    start_time = time.time()
    main_images_folter = f'{os.getcwd()}/pictures'
    main(main_images_folter, new_width=1000, verbose=True)
    print("\n\nTOTAL TIME WITH %s SECONDS ---" % (time.time() - start_time))
