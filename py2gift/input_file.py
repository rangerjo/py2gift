# AUTOGENERATED! DO NOT EDIT! File to edit: 40_input_file.ipynb (unless otherwise specified).

__all__ = ['extract_class_settings', 'initialize', 'set_class_preamble', 'set_class_closing', 'write_header',
           'write_class_preamble', 'write_class_closing', 'function_to_make_hierarchical_category_name']

# Cell

import pathlib
from typing import Union, Optional, Callable

import py2gift.util

import yaml

# Cell

def extract_class_settings(category_name: Union[str, list], class_name: str, settings: dict):

    category_found = False

    for cat in settings['categories']:

        if cat['name'] == category_name:

            category_found = True

            for cls in cat['classes']:

                if cls['name'] == class_name:

                    return cls

    else:

        if category_found:

            print(f'cannot find the requested class, {class_name}')
            sys.exit(1)

        else:

            print(f'cannot find the requested category, {category_name}')
            sys.exit(1)

# Cell

def initialize(output_file: str, pictures_directory: str, ) -> dict:

    settings = {}

    settings['output file'] = output_file
    settings['pictures base directory'] = pictures_directory
    settings['path to gift-wrapper'] = '~/gift-wrapper/wrap.py'
    settings['categories'] = None

    return settings

# Cell

def set_class_preamble(settings: dict, category_name: str, base_category: Optional[str] = None, test_mode: bool = False) -> Union[str, list]:

    if test_mode:

        category_name = 'test'

    else:

        if base_category:

            category_name = [base_category, f'{base_category}/{category_name}']


    if settings['categories'] is None:

        settings['categories'] = []

    settings['categories'].append({'name': category_name, 'classes': None})

    return category_name

# Cell

def set_class_closing(settings: dict, n_instances: int, time: Optional[int] = None) -> None:

    if settings['categories'][-1]['classes'] is None:

        settings['categories'][-1]['classes'] = [{}]

    settings['categories'][-1]['classes'][-1]['number of instances'] = n_instances
    settings['categories'][-1]['classes'][-1]['time'] = time

# Cell

def write_header(file: Union[str, pathlib.Path], output_file: str, pictures_directory: str, ) -> None:

    settings = initialize(output_file, pictures_directory)

    py2gift.util.dict_to_yaml(settings, file)

#     with open(file, 'w') as f:

#         f.write(f'output file: {output_file}\n')
#         f.write(f'pictures base directory: {pictures_directory}\n')
#         f.write("path to gift-wrapper: '~/gift-wrapper/wrap.py'\n")
#         f.write('\n')

#         f.write('categories:\n')

# Cell

def write_class_preamble(file: Union[str, pathlib.Path], category_name: str, base_category: Optional[str] = None, test_mode: bool = False) -> Union[str, list]:


    settings = py2gift.util.yaml_to_dict(file)
    category_name = set_class_preamble(settings, category_name, base_category, test_mode)
    py2gift.util.dict_to_yaml(settings, file)

#     # file is *appended* (not overwritten)
#     with open(file, 'a') as f:

#         f.write('\n')

#         if test_mode:

#             category_name = 'test'

#         else:

#             if base_category:

#                 category_name = [base_category, f'{base_category}/{category_name}']

#         f.write(f'  - name: {category_name}\n\n')
#         f.write('    classes:\n')

    return category_name

# Cell

def write_class_closing(file: Union[str, pathlib.Path], n_instances: int, time: Optional[int] = None) -> None:

    settings = py2gift.util.yaml_to_dict(file)
    category_name = set_class_closing(settings, n_instances, time)
    py2gift.util.dict_to_yaml(settings, file)

#     with open(file, 'a') as f:

#         f.write(f'\n        number of instances: {n_instances}')

#         if time:

#             f.write(f'\n        time: {time}')

# Cell

def function_to_make_hierarchical_category_name(base_category: str) -> Callable[[str], list]:

    def make_subcategory(category: str) -> list:

        return [base_category, f'{base_category}/{category}']

    return make_subcategory