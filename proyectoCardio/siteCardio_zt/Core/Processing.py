from ..models import PredictionsResult

class Metrics:
    def __init__(self, edad=0, men=0, woman=0, imc=0, pas=0, pad=0, col_t=0, hdl_c=0, no_hdl_c=0,
                 trigliceridos=0, ldl_c=0, smoke=0):
        self.edad = edad
        self.men = men
        self.woman = woman
        self.imc = imc
        self.pas = pas
        self.pad = pad
        self.col_t = col_t
        self.hdl_c = hdl_c
        self.no_hdl_c = no_hdl_c
        self.trigliceridos = trigliceridos
        self.ldl_c = ldl_c
        self.smoke = smoke

    @staticmethod
    def round_f(num, r=2):
        return round(float(num), r)

    def round_and_per(self, num, r=2):
        return "{} %".format(self.round_f(num, r))

    def get_data(self):
        return {"Edad": self.round_f(self.edad),
                "Hombres": self.round_and_per(self.men),
                "Mujeres": self.round_and_per(self.woman),
                "Superficie Corporal (IMC)": self.round_f(self.imc),
                "Sistólica (PAS)": self.round_f(self.pas),
                "Diastólica (PAD)": self.round_f(self.pad),
                "Colesterol total": self.round_f(self.col_t),
                "HDL-C": self.round_f(self.hdl_c),
                "NO HDL-C": self.round_f(self.no_hdl_c),
                "Triglicéridos": self.round_f(self.trigliceridos),
                "LDL-C": self.round_f(self.ldl_c),
                "Tabaco - NO (%)": self.round_and_per(self.smoke)
                }


class GeneralMetrics:
    def __init__(self, predict_result: PredictionsResult):
        self.predict_result = predict_result

    def get_dataframe(self):
        file_to_process = self.predict_result.id_regresion_lm.id_file
        df = file_to_process.get_df()
        print("df: {}".format(df))
        return df

    def processing_data(self):
        import numpy as np
        extra_info = {}
        df = self.get_dataframe()
        genero = df["SEXO"].value_counts(normalize=True) * 100
        genero_muertos_f = df.loc[(df["MUERTE_CV"] == 1) & (df["SEXO"] == 0)]
        genero_muertos_m = df.loc[(df["MUERTE_CV"] == 1) & (df["SEXO"] == 1)]
        #hta_count = (df['HTA'].values == 1).sum()
        hta_count = df['HTA'].value_counts().to_dict()
        #dmt2_count = (df['DMT2'].values == 1).sum()
        dmt2_count = df['DMT2'].value_counts().to_dict()
        #anti_hta_count = (df['TTO_ANTI-HTA'].values == 1).sum()
        anti_hta_count = df['TTO_ANTI-HTA'].value_counts().to_dict()
        edad_mean = df["EDAD"].value_counts(bins=np.array([1, 17, 18, 64, 65, 110]), sort=False)

        count_f = genero_muertos_f["SEXO"].value_counts().values[0]
        count_m = genero_muertos_m["SEXO"].value_counts().values[0]
        extra_info["muertos"] = {"Hombre": count_m, "Mujeres": count_f}
        extra_info["edad"] = {"1-17": edad_mean.values[0], "18-64": edad_mean.values[2], "65-110": edad_mean.values[3]}
        extra_info["hta_dmt2_si"] = {"HTA": hta_count[1], "DMT2": dmt2_count[1], "TTO-ANTI-HTA": anti_hta_count[1]}
        extra_info["hta_dmt2_no"] = {"HTA": hta_count[0], "DMT2": dmt2_count[0], "TTO-ANTI-HTA": anti_hta_count[0]}

        fumador = df["FUMADOR"].value_counts(normalize=True) * 100
        metrics = Metrics()
        metrics.edad = df["EDAD"].mean()
        metrics.men = genero[1]
        metrics.woman = genero[0]
        metrics.imc = df["IMC"].mean()
        metrics.pas = df["PAS"].mean()
        metrics.pad = df["PAD"].mean()
        metrics.col_t = df["COL-T"].mean()
        metrics.hdl_c = df["HDL-C"].mean()
        metrics.no_hdl_c = df["COL_NO-HDL"].mean()
        metrics.trigliceridos = df["TRIGLICERIDOS"].mean()
        metrics.ldl_c = df["LDL-C"].mean()
        metrics.smoke = fumador[0]

        return metrics.get_data(), extra_info


class PerfilLipidico:
    def __init__(self, men=True, col_t=0, hdl_c=0, no_hdl_c=0, trigliceridos=0, ldl_c=0):
        self.men = men
        self.col_t = col_t
        self.hdl_c = hdl_c
        self.no_hdl_c = no_hdl_c
        self.ldl_c = ldl_c
        self.trigliceridos = trigliceridos
        self.ok = "success"
        self.warning = "warning"
        self.bad = "danger"
        self.not_found = "primary"
        self.msg_not_found = "Rango no encontrado"
        self.result = {
            "status": self.ok,
            "msg": "Nada"
        }

    def get_col_t(self):
        msg = "COL_T: En meta de control terapeutico"
        print(self.col_t)
        if self.col_t < 200:
            self.result["msg"] = msg
            self.result["status"] = self.ok
        else:
            self.result["status"] = self.bad
            self.result["msg"] = "COL_T: Fuera de meta de control terapeutico"
        return self.result.copy()

    def get_hdl_c(self):
        msg_ok = "HDL: En meta de control terapeutico."
        msg_bad = "HDL: Fuera de meta de control terapeutico."
        value_condition = 40 if self.men else 45
        if self.hdl_c > value_condition:
            self.result["status"] = self.ok
            self.result["msg"] = msg_ok
        else:
            self.result["status"] = self.bad
            self.result["msg"] = msg_bad
        return self.result.copy()

    def get_no_hdl_c(self):
        msg_ok = "NO_HDL: En meta secundaria de control terapeutico."
        msg_bad = "NO_HDL: Fuera de meta secundaria de control terapeutico."
        if self.no_hdl_c <= 85:
            self.result["status"] = self.ok
            self.result["msg"] = msg_ok
        elif 85 <= self.no_hdl_c <= 100:
            self.result["status"] = self.bad
            self.result["msg"] = msg_bad
        elif 100 <= self.no_hdl_c <= 130:
            self.result["status"] = self.bad
            self.result["msg"] = msg_bad
        else:
            self.result["status"] = self.ok
            self.result["msg"] = msg_ok
        return self.result.copy()

    def get_ldl_c(self):
        msg_ok = "LDL: En meta primaria de control terapeutico"
        msg_moderate = "LDL: En meta primaria de control terapeutico"
        msg_wn = "LDL:Fuera de meta primaria de control terapeutico"
        msg_bad = "LDL: En meta primaria de control terapeutico"
        msg_bad2 = "LDL: En meta primaria sugerida de control terapeutico"
        msg_default = "LDL: Fuera de meta primaria de control terapeutico"
        if 101 <= self.ldl_c <= 116:
            self.result["status"] = self.ok
            self.result["msg"] = msg_ok
        elif 71 <= self.ldl_c <= 100:
            self.result["status"] = self.warning
            self.result["msg"] = msg_moderate
        elif 56 <= self.ldl_c <= 70:
            self.result["status"] = self.warning
            self.result["msg"] = msg_wn
        elif 41 <= self.ldl_c <= 55:
            self.result["status"] = self.ok
            self.result["msg"] = msg_bad
        elif 0 <= self.ldl_c <= 40:
            self.result["status"] = self.ok
            self.result["msg"] = msg_bad2
        else:
            self.result["status"] = self.bad
            self.result["msg"] = msg_default
        return self.result.copy()

    def get_trigliceridos(self):
        msg_ok = "TRI: En meta de control terapeutico."
        msg_bad = "TRI: Fuera de meta de control terapeutico."
        if self.trigliceridos <= 150:
            self.result["status"] = self.ok
            self.result["msg"] = msg_ok
        else:
            self.result["status"] = self.bad
            self.result["msg"] = msg_bad
        return self.result.copy()

    def results(self):
        return [
            self.get_col_t(),
            self.get_hdl_c(),
            self.get_ldl_c(),
            self.get_trigliceridos(),
            self.get_no_hdl_c()
        ]


