from ..Utils.UtilsFile import dirname
import os
from ..Utils.general import *
from .FileToProcess import FileToProcess
from time import gmtime, strftime
import logging
from .Encoding import Replace

logger = logging.getLogger(__name__)
level_log = 30
replace_values = {
    "afirmation": {
        "SI": 1,
        "NO": 0
    },
    "genero": {
        "M": 1,
        "F": 0
    }
}


class ClearColumns:
    """
    Clase para crear objetos de una columna de un csv para proceder a limpiar
    """
    clear_options = ["replace", "auto_complete", "delete"]

    def __init__(self, column_name, clear_type="delete", replace_with=None):
        self.column_name = column_name
        self.clear_type = self.option_to_clear(clear_type)
        self.replace_with = replace_with

    def option_to_clear(self, option_type) -> str:
        """
        Funcion para validar el tipo de opcion que se va aplicar para liminar la columna (por defecto es: delete)
        Los tipos oportados son:
        - replace: remplaza los valores vacios con otro valor (se tiene que especificar: replace_with)
        - auto_complete: auto completa los valores vacios tomando en cuenta los valores existentes
        - delete: elimina los valores vacios
        :param (str) option_type: Tipo de opcion para limpiar
        :return: opcion seleccionada
        """
        if option_type is None:
            return self.clear_options[2]
        elif option_type in self.clear_options:
            return option_type
        else:
            raise Exception("Option not support! Only support: {}".format(self.clear_options))


class ClearData:
    """
    Clase para limpiar los datos de un csv
    """
    actions_clear_headers = ["auto", "enumeration"]

    def __init__(self, file_process: FileToProcess, save_path: str = None, index_to_clear: list = None):
        self.file_process = file_process
        self.save_path = save_path
        self.index_to_clear = self.validate_list_index(index_to_clear) if index_to_clear else None
        self.df_file_process = file_process.get_pandas_file()

    @staticmethod
    def validate_list_index(list_clear_columns):
        """
        Funcion para validar que todos los objetos de la lista son de tipo: ClearColumns
        :param (list) list_clear_columns: Lista de objetos de tipo: ClearColumns
        :return: True o Exception
        """
        if all(isinstance(obj, ClearColumns) for obj in list_clear_columns):
            return list_clear_columns
        else:
            raise Exception("Type list not support!")

    def __replace(self, column: ClearColumns):
        """
        Funcion para remplazar los valores vaciones de una columna
        :param (ClearColumns) column: Objeto de tipo ClearColumns con el que se a trabajar
        :return:
        """
        self.df_file_process[column.column_name].fillna(column.replace_with, inplace=True)

    def __auto_complete(self, column: ClearColumns):
        """
        Funcion para auto completar los valores vacios de una columna
        :param ClearColumns) column: Objeto de tipo ClearColumns con el que se a trabajar
        :return:
        """
        pass

    def __delete(self, column: ClearColumns = None):
        """
        Funcion para eliminar los valores vacios de una columna
        :param ClearColumns) column: Objeto de tipo ClearColumns con el que se a trabajar
        :return:
        """
        if column:
            print("Delete: {}".format(column.column_name))
            self.df_file_process = self.df_file_process.dropna(subset=[column.column_name])
        else:
            print("Delete all")
            self.df_file_process = self.df_file_process.dropna()

    def __auto_clear_headers(self, current_headers):
        """
        Funcion para limpiar las cabeceras automaticamente
        :param (list) current_headers: las cabeceras actuales del archivo
        :return:
        """
        rename_headers = []
        for index, header in enumerate(current_headers):
            if "Unnamed:" in header:
                rename_headers.append("column_" + str(index))
            else:
                rename_headers.append(str(header).strip().replace(" ", "_"))
        columns_to_rename = dict(zip(current_headers, rename_headers))
        logger.info("Data:")
        logger.log(level_log, "data rename: {}".format(rename_headers))
        logger.log(level_log, "")
        logger.log(level_log, "data current: {}".format(current_headers))
        logger.log(level_log, "")
        logger.log(level_log, "data zip : {}".format(columns_to_rename))
        logger.info("Data:")
        self.df_file_process = self.df_file_process.rename(columns=columns_to_rename)

    def __enumeration_clear_headers(self, current_headers):
        """
        Funcion para enumerar las cabeceras automaticamente
        :param (list) current_headers: las cabeceras actuales del archivo
        :return:
        """
        for index, header in enumerate(current_headers):
            current_headers[index] = "column_" + str(index)
        self.df_file_process = self.df_file_process.rename(columns=current_headers)

    def set_index_to_clear(self, values: list):
        """
        Funcion para establecer el valor a la variable: index_to_clear
        :param (list) values: Lista de valores de tipo ClearColumns
        :return:
        """
        if values:
            self.index_to_clear = values
        else:
            raise Exception("Please, send values!")

    def clear_headers(self, custom_headers=None, action="auto"):
        """
        Funcion para limpiar las cabeceras del archivo csv
        :param custom_headers: Si desea renombrar las cabeceras con nombres personalizados
        :param action: Tipo de limpieza a ejecutar, disponible:
        - auto: limpia automaticamente el nombre de las cabeceras, borrando espacios y estableciendo nombres si no tienen
        - enumeration: enumera las cabeceras automaticamente
        :return:
        """
        current_headers = self.file_process.get_headers()
        if custom_headers is None:
            if action == "auto":
                self.__auto_clear_headers(current_headers)
            elif action == "enumeration":
                self.__enumeration_clear_headers(current_headers)
            else:
                raise Exception("Invalid action!")
        else:
            self.df_file_process.rename(columns=custom_headers)

    def clear_columns(self):
        """
        Funcion que se ejecuta para empezar con la limpieza del archivo
        :return:
        """
        if self.index_to_clear:
            for column in self.index_to_clear:
                if column.clear_type == "replace":
                    self.__replace(column)
                elif column.clear_type == "auto_complete":
                    self.__auto_complete(column)
                elif column.clear_type == "delete":
                    self.__delete(column)
        else:
            raise Exception("Error: index_to_clear is NONE.")

    def delete_nan(self):
        self.__delete()

    def write_changes(self):
        """
        Funcion para guardar los cambios realizado en el archivo
        :return:
        """
        if self.save_path:
            path_to_save = self.save_path
        else:
            print("NO PATH!!!")
            path_to_save = dirname(self.file_process.path_file)
        self.file_process.file_name = self.file_process.file_name + "-" + strftime("%Y%m%d%H%M%S", gmtime())
        self.file_process.path_file = os.path.join(path_to_save, self.file_process.file_name + self.file_process.extension_name)
        print("Path to save: {}".format(self.file_process.path_file))
        return self.file_process.path_file if self.df_file_process.to_csv(self.file_process.path_file) else None

    def encoding_data(self, data_to_clear: [Replace]):
        replace = dict()
        for data in data_to_clear:
            replace.update(data.get_data_replace())
        print("Replace data: {}".format(replace))
        self.df_file_process.replace(replace, inplace=True)

    def cardio_risk(self, **kwargs):
        l = calc_l(gender="H" if get_gender(kwargs.get("sexo")) else "M", edad=kwargs.get("edad"), colesterol=kwargs.get("colesterol"),
               HDL_C=kwargs.get("hdl_col"), PAS=kwargs.get("pas"), PAD=kwargs.get("pad"),
               diabetes=kwargs.get("diabetes"), fumador=kwargs.get("fumandor"))
        g = get_g(gender="H" if get_gender(kwargs.get("sexo")) else "M")
        b = calc_b(l, g)
        s = get_s(gender="H" if get_gender(kwargs.get("sexo")) else "M")
        return calc_r(s, b)

    def calc_cardio_risk(self):
        self.df_file_process["CARDIO_RISK"] = self.df_file_process.apply(lambda x: self.cardio_risk(
            sexo=x["SEXO"], edad=x["EDAD"], colesterol=x["COL-T"], hdl_col=x["HDL-C"], pas=x["PAS"], pad=x["PAD"],
            diabetes=x["DMT2"], fumandor=["FUMADOR"]), axis=1)
        print("Function apply")
        return True

    def calc_perfil(self):
        list_to_calc = ["COLUM-NAME", "COLUM-NAME"]
        for a in list_to_calc:
            print("Function apply")
        return True

    def overwrite(self):
        pass
