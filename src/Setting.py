import configparser
import os.path


class Setting:
    def __init__(self, section, file_name='setting.ini'):
        self._section = section
        self.file_name = file_name
        self.conf = configparser.RawConfigParser()
        # 讀取INI
        current_path = os.path.dirname(__file__)
        file_path = current_path + '/' + self.file_name
        self.conf.read(file_path, encoding='utf-8')
        if not os.path.isfile(file_path):
            raise Exception(f'{file_path} 檔案不存在')
        if not self.conf.sections():
            raise Exception(f'{file_path} 配置為空，請配置section')

    def __getattr__(self, attr):
        """
        任意函式化
        :param attr:
        :return:
        """
        return self.value(attr)

    def value(self, key):
        return self.conf.get(self._section, key)

    def get_values(self):
        return self.conf.items()

    def get_keys(self):
        return self.conf.options(self._section)


LANGUAGE = Setting('LANGUAGE').language
