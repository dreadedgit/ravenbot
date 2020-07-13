import yaml


class Config(dict):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.config_file = None

    def load(self, config_file=None):
        self.config_file = self.config_file or config_file

        try:
            with open(self.config_file, 'r') as f:
                self.update(yaml.safe_load(f))
            f.close()
        except FileNotFoundError:
            with open(self.config_file, 'x') as f:
                print(f'{self.config_file} created')
            f.close()

    def write(self, config_file, data):
        self.config_file = self.config_file or config_file
        with open(self.config_file, 'w') as f:
            yaml.safe_dump(dict(data), f)
        f.close()
