
class Data:
    def __init__(self, current_value, value_replace):
        self.current_value = current_value
        self.value_replace = value_replace


class Replace:
    def __init__(self, column_name, data_replace: []):
        self.column_name = column_name
        self.data_replace = data_replace

    def get_data_replace(self):
            return {self.column_name: {data.current_value: data.value_replace for data in self.data_replace}}
