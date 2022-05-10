from ..Utils.UtilsFile import get_basename
import pandas as pd


class FileToProcess:
    """
    Clase que represeta un archivo CSV para ser procesado como un objeto
    """
    def __init__(self, path_file, delimiter=",", index_column=0):
        self.path_file = path_file
        self.delimiter = delimiter
        self.__pandas_file = pd.read_csv(self.path_file, delimiter=self.delimiter, index_col=index_column)
        self.file_name = get_basename(path_file)["file_name"]
        self.extension_name = get_basename(path_file)["file_extension"]
        self.headers = self.get_headers()
        self.columns_number = self.get_columns_number()
        self.row_number = self.get_row_numbers()

    def get_headers(self) -> list:
        """
        Obtener una lista de las cabeceras (la primera columna) del archivo.
        :return: (list) Retorna una lista de string
        """
        if self.extension_name == ".csv":
            return list(self.__pandas_file.columns)
        else:
            raise Exception("Not supported extension.")

    def get_columns_number(self) -> int:
        """
        Funcion para obtener el numero de columnas del archivo CSV
        :return: Retorna el numero de columnas del archivo
        """
        return self.__pandas_file.shape[1]

    def get_row_numbers(self) -> int:
        """
        Funcion para obtener el numero de filas del archivo CSV
        :return: Retorna el numero de filas del archivo
        :return:
        """
        return self.__pandas_file.shape[0]

    def get_pandas_file(self) -> pd:
        """
        Funcion para tener el archivo CSV como un objeto de tipo pandas
        :return: Objeto de tipo pandas
        """
        return self.__pandas_file

    def convert_to_numpy(self):
        """
        Funcion para convertir el csv en un objeto de tipo numpy
        :return: Objeto de tipo numpy
        """
        return self.__pandas_file.to_numpy(copy=True)

    def get_columns_numpy(self, columns):
        return self.__pandas_file[columns].to_numpy(copy=True)
