import os

from django.conf import settings
from django.core.management import CommandError
from django.core.management.templates import TemplateCommand


class Command(TemplateCommand):
    """
    app 내에 지정한 폴더 명 대로 앱을 생성합니다.
    """

    help = (
        "Create Launchpack app in app folder"
    )
    missing_args_message = "You must provide an application name."

    create_file = {
        'serializer.py': 'from rest_framework import serializers\n\n',
        'mixin/model_mixin.py': '',
        'mixin/view_mixin.py': '',
    }

    def handle(self, **options):
        app_name = options.pop('name')
        app_dir = settings.APP_DIR + '/' + app_name
        try:
            os.mkdir(app_dir)
        except FileExistsError:
            raise CommandError('폴더가 이미 존재합니다.')

        try:
            super().handle('app', app_name, app_dir, **options)
        except CommandError as e:
            os.removedirs(app_dir)
            raise e

        os.remove(app_dir + '/tests.py')
        os.remove(app_dir + '/admin.py')
        os.mkdir(app_dir + '/mixin')

        open(app_dir + '/mixin/__init__.py', 'w').write('')

        for file_name, inner_data in self.create_file.items():
            with open(app_dir + f'/{file_name}', 'w') as f:
                f.write(inner_data)
