from rest_framework import serializers


class BaseModelSerializer(serializers.ModelSerializer):
    def get_fields(self):
        fields = super().get_fields()

        for field_name in fields:
            if isinstance(fields[field_name], serializers.ListSerializer):
                if isinstance(fields[field_name].child, BaseModelSerializer):
                    fields[field_name].child._context = self._context

            elif isinstance(fields[field_name], BaseModelSerializer):
                fields[field_name]._context = self._context

        return fields

    def request(self):
        return self.context.get('request')

    def current_user(self):
        request = self.request()
        if request is None:
            return self.context.get('user') or self.context.get('current_user')
        return request.user
