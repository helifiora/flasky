from enum import Enum


class ConfigEnum(Enum):
    Teste = 'teste'
    Prod = 'producao'
    Dev = 'dev'

    @staticmethod
    def parse(value: str) -> 'ConfigEnum':
        has_value = value in [x.value for x in ConfigEnum.__members__.values()]
        if has_value:
            return ConfigEnum(value)
        else:
            return ConfigEnum.Dev


print(ConfigEnum.parse('qwe'))
