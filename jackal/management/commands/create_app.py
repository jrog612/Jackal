import os

from django.conf import settings
from django.core.management import CommandError
from django.core.management.templates import TemplateCommand

from jackal.settings import jackal_settings


class Command(TemplateCommand):
    """
    jackal settings 내에 지정한 APP_DIR 내로 앱을 생성합니다.
    """

    help = (
        "Create Launchpack app in app folder"
    )
    missing_args_message = "You must provide an application name."

    create_file = {
        'serializer.py': 'from rest_framework import serializers\n\n',
        'mixin/model_mixin.py': '',
        'mixin/view_mixin.py': '',
        'views.py': 'from jackal.views import generics'
    }

    def handle(self, **options):
        app_name = options.pop('name')

        app_root = jackal_settings.APP_DIR if jackal_settings.APP_DIR is not None else os.getcwd()
        app_path = os.path.join(app_root, app_name)

        try:
            os.mkdir(app_path)
        except FileExistsError:
            raise CommandError('폴더가 이미 존재합니다.')

        try:
            super().handle('app', app_name, app_path, **options)
        except CommandError as e:
            os.removedirs(app_path)
            raise e

        os.remove(app_path + '/tests.py')
        os.remove(app_path + '/admin.py')
        os.remove(app_path + '/views.py')
        os.mkdir(app_path + '/mixin')

        open(app_path + '/mixin/__init__.py', 'w').write('')

        for file_name, inner_data in self.create_file.items():
            with open(app_path + f'/{file_name}', 'w') as f:
                f.write(inner_data)

        return
