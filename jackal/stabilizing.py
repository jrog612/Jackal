from jackal.shortcuts import change_None, check_required, remove_None, remove_unexpected
from jackal.settings import jackal_settings


def data_stabilizing(data, key):
    param_structure = jackal_settings.structure()[key]

    filtered = data

    # 예상하지 못한 필드들은 제외
    expected = param_structure.get('expected', None)
    if expected is not None:
        filtered = remove_unexpected(data, expected)

    # 필수 값 체크
    required = param_structure.get('required', None)
    if required is not None:
        check_required(filtered, required=required)

    # 공백을 허용하지 않는 값 None 처리
    null_array = param_structure.get('null', None)
    if null_array is not None:
        filtered = change_None(filtered, param_structure['null'])

    # 디폴드 값이 있어서 빈 값이나 None 을 허용하지 않는 필드 제외
    default_array = param_structure.get('default', None)
    if default_array is not None:
        filtered = remove_None(filtered, param_structure['default'])

    return filtered
