from siteCardio_zt.Core.FileToProcess import FileToProcess
from siteCardio_zt.Core.ClearData import ClearData, ClearColumns
from siteCardio_zt.Core.Encoding import Replace, Data
from siteCardio_zt.Utils.UtilsFile import convert_obj_to_dict
from siteCardio_zt.models import FileToProcess as FTP
from django.conf import settings


class Automatic:
    #basic_columns = ["FECHA_ATENCION", "IDENTIFICACION", "NOMBRE_PACIENTE", "EDAD", "SEXO", "RAZA", "PAS",
    #                 "PAD", "IMC", "COL-T", "TRIGLICERIDOS", "HDL-C", "LDL-C", "FUMADOR", "ALCOHOL", "TTO_ESTATINAS",
    #                 "TTO_ANTI-HTA", "TTO_ASPIRINA"]
    null_to_boolean = ["MUERTE_CV", "HOSPITALIZACION", "IC"]
    #basic_columns = ["EDAD", "SEXO", "PAS", "PAD", "COL-T", "HDL-C", "LDL-C", "FUMADOR", "ALCOHOL", "DIAG_PRESUNTIVO"]
    basic_columns = ["EDAD", "SEXO", "PAS", "PAD", "COL-T", "HDL-C", "LDL-C", "FUMADOR", "ALCOHOL", "HTA"]
    answers_double = ["SEXO", "FUMADOR", "ALCOHOL", "TTO_ESTATINAS", "TTO_ANTI-HTA", "TTO_ASPIRINA"]
    #answers_double = ["SEXO", "HTA", "FUMADOR", "ALCOHOL", "TTO_ESTATINAS", "TTO_ANTI-HTA", "TTO_ASPIRINA"]

    def __init__(self, file_process: FileToProcess):
        self.file_process = file_process
        self.clear_data = ClearData(self.file_process, save_path=settings.BASE_DIR_DATASET)

    def _detect_columns(self):
        pass

    def get_replace_list(self) -> list:
        si_data = Data("SI", 1)
        si_data1 = Data("SI ", 1)
        si_data2 = Data(" SI", 1)
        no_data = Data("NO", 0)
        no_data1 = Data("NO ", 0)
        no_data2 = Data(" NO", 0)
        sexo_m = Data("M", 1)
        sexo_m1 = Data("M ", 1)
        sexo_m2 = Data(" M", 1)
        sexo_f = Data("F", 0)
        sexo_f1 = Data("F ", 0)
        sexo_f2 = Data(" F", 0)

        return [Replace(column, [si_data, si_data1, si_data2, no_data, no_data1, no_data2, sexo_m, sexo_m1, sexo_m2,
                                 sexo_f, sexo_f1, sexo_f2]) for column in self.answers_double]

    def get_clear_columns(self):
        return [ClearColumns(n) for n in self.basic_columns] + [ClearColumns(n, "replace", "0") for n in self.null_to_boolean]

    def get_info(self):
        return convert_obj_to_dict(self.file_process)

    def clear_file(self):
        self.clear_data.clear_headers()
        self.clear_data.set_index_to_clear(self.get_clear_columns())
        self.clear_data.clear_columns()
        self.clear_data.encoding_data(self.get_replace_list())

    def calc_risk(self):
        self.clear_data.calc_cardio_risk()

    def calc_perfil_limpidico(self):
        self.clear_data.calc_cardio_risk()
        print("saved")

    def write_changes(self):
        self.clear_data.write_changes()

    def save_file(self, description):
        ftp = FTP()
        ftp.file_name = self.file_process.file_name
        ftp.file_path = self.file_process.path_file
        ftp.description = description
        ftp.columns = list(self.clear_data.df_file_process.columns)
        ftp.save()
