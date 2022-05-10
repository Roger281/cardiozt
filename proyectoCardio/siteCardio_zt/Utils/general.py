from django.http.request import QueryDict
from siteCardio_zt.Core.MLR import MLR
from siteCardio_zt.Core.FileToProcess import FileToProcess
from siteCardio_zt.models import RegressionLinearModel
import pandas as pd
from proyectoCardio import settings
import math


def create_mlr(form: QueryDict, file: FileToProcess) -> MLR:
    train_value = form.get("porcentaje", 0.2)
    independiente = form.getlist("inputVarInde")
    dependiente = form.getlist("inputVarDep")
    print("inde: {}, dep: {}".format(independiente, dependiente))
    return MLR(file, dependiente, independiente, test_size=int(train_value)/100)


def create_array(form: QueryDict, model: RegressionLinearModel):
    data_prediction = {}
    columns_indepe = model.dependent_var
    for column in columns_indepe:
        if column in form:
            data_prediction[column] = list(map(int, form.getlist(column)))
        else:
            raise Exception("Value {} does not exist".format(column))
    pd_data = pd.DataFrame(data_prediction)

    array_data = pd_data[columns_indepe].to_numpy(copy=True)
    print("array1: {}".format(array_data))
    print("array: {}".format(pd.DataFrame(data_prediction).to_numpy(copy=True)*2))
    return pd.DataFrame(data_prediction).to_numpy()


def get_gender(gender):
    allow_values = {"H": True, "M": False, "h": True, "m": False, 1: True, 0: False, "1": True, "0": False}
    return allow_values.get(gender)


def get_binary(gender):
    gender = gender.replace(" ", "").upper() if isinstance(gender, str) else gender
    allow_values = {"SI": True, "NO": False, 1: True, 0: False, "1": True, "0": False, "TRUE": True, "FALSE": False}
    return allow_values.get(gender)


def calc_l(gender="H", **kwargs):
    if get_gender(gender):
        # For men
        edad = kwargs.get("edad")
        col = stratify_b_c(kwargs.get("colesterol"))
        hdl = stratify_b_h(kwargs.get("HDL_C"))
        pas_pad = stratify_b_t(kwargs.get("PAS"), kwargs.get("PAD"))
        dia = stratify_b_d(kwargs.get("diabetes"))
        fuma = stratify_b_f(kwargs.get("fumador"))
        l = get_b_e1() * \
            edad + \
            col + \
            hdl + \
            pas_pad + \
            dia + \
            fuma
        print(l)
    else:
        # For women
        l = get_b_e1() * \
            kwargs.get("edad") + \
            get_b_e2() * \
            math.pow(kwargs.get("edad"), 2) + \
            stratify_b_c(kwargs.get("colesterol")) + \
            stratify_b_h(kwargs.get("HDL_C")) + \
            stratify_b_t(kwargs.get("PAS"), kwargs.get("PAD")) + \
            stratify_b_d(kwargs.get("diabetes")) + \
            stratify_b_f(kwargs.get("fumador"))
    return l


def calc_b(l, g):
    return math.exp(l - g)


def calc_r(s, b):
    return 1 - math.pow(s, b)


def get_b_e1(gender="H"):
    return settings.H_b_E1 if gender == "H" else settings.M_b_E1


def get_b_e2(gender="H"):
    return settings.H_b_E2 if gender == "H" else settings.M_b_E2


def stratify_b_c(value, gender="H"):
    if value < 160:
        return settings.H_b_C_less_160 if gender == "H" else settings.M_b_C_less_160
    elif 160 <= value <= 199:
        return settings.H_b_C_between_160_199 if gender == "H" else settings.M_b_C_between_160_199
    elif 200 <= value <= 239:
        return settings.H_b_C_between_200_239 if gender == "H" else settings.M_b_C_between_200_239
    elif 240 <= value <= 279:
        return settings.H_b_C_between_240_279 if gender == "H" else settings.M_b_C_between_240_279
    elif value >= 280:
        return settings.H_b_C_greater_or_equal_280 if gender == "H" else settings.M_b_C_greater_or_equal_280
    else:
        print(value)
        print("stratify_b_c: algo puede salir mal")


def stratify_b_h(value, gender="H"):
    if value < 35:
        return settings.H_b_H_less_35 if gender == "H" else settings.M_b_H_less_35
    elif 35 <= value <= 44:
        return settings.H_b_H_between_35_44 if gender == "H" else settings.M_b_H_between_35_44
    elif 45 <= value <= 49:
        return settings.H_b_H_between_45_49 if gender == "H" else settings.M_b_H_between_45_49
    elif 50 <= value <= 59:
        return settings.H_b_H_between_50_59 if gender == "H" else settings.M_b_H_between_50_59
    elif value >= 60:
        return settings.H_b_H_greater_or_equal_60 if gender == "H" else settings.M_b_H_greater_or_equal_60
    else:
        print("stratify_b_h: algo puede salir mal")


def stratify_b_t(pas_value, pad_value, gender="H"):
    if pas_value < 120 and pad_value < 80:
        return settings.H_b_T_Pas_less_120_pas_less_80 if gender == "H" else settings.M_b_T_Pas_less_120_pas_less_80
    elif pas_value < 130 and pad_value < 85:
        return settings.H_b_T_Pas_less_130_pas_less_85 if gender == "H" else settings.M_b_T_Pas_less_130_pas_less_85
    elif pas_value < 140 and pad_value < 90:
        return settings.H_b_T_Pas_less_140_pas_less_90 if gender == "H" else settings.M_b_T_Pas_less_140_pas_less_90
    elif pas_value < 160 and pad_value < 100:
        return settings.H_b_T_Pas_less_160_pas_less_100 if gender == "H" else settings.M_b_T_Pas_less_160_pas_less_100
    elif pas_value >= 100 and pad_value >= 100:
        return settings.H_b_T_Pas_g_or_e_160_pas_g_or_e_100 if gender == "H" else settings.M_b_T_Pas_g_or_e_160_pas_g_or_e_100
    else:
        print("stratify_b_t: algo puede salir mal")
        return 0


def stratify_b_d(value, gender="H"):
    print("d: {}".format(value))
    if "1" in str(value):
        print("si: {}".format(settings.H_b_D_Si if gender == "H" else settings.M_b_D_Si))
        return settings.H_b_D_Si if gender == "H" else settings.M_b_D_Si
    else:
        print("no: {}".format(settings.H_b_D_No if gender == "H" else settings.M_b_D_No))
        return settings.H_b_D_No if gender == "H" else settings.M_b_D_No


def stratify_b_f(value, gender="H"):
    if value == 1 and str(value) == "1":
        return settings.H_b_F_Si if gender == "H" else settings.M_b_F_Si
    else:
        return settings.H_b_F_No if gender == "H" else settings.M_b_F_NO


def get_g(gender="H"):
    return settings.H_G if gender == "H" else settings.M_G


def get_s(gender="H"):
    return settings.H_S if gender == "H" else settings.M_S
