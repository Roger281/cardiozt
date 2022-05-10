from . import form as forms
from django.conf import settings
from django.core.mail import send_mail
from .Core.FileToProcess import FileToProcess
from .Core.MLR import MLR
from .Core.Processing import GeneralMetrics, PerfilLipidico
from siteCardio_zt.Core.ClearModel import Automatic
from .Utils.UtilsFile import get_files_directory
from .Utils.general import create_mlr, create_array, get_binary
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.http import HttpResponseNotFound
from django.contrib.auth import login as auth_login
from siteCardio_zt import models as mod
import json
import os
import ast


# Create your views here.
def index(request):
    return render(request, 'index.html', {})


def home(request):
    return render(request, 'home.html', {})


def hc(request):
    return render(request, 'historialClinico.html', {})


def validar_rcv_tag(value):
    value = value * 100
    print("RCV:", value)
    data = "Valor {}, se define como: {}"
    if value > 10:
        print("muy alto riesgo")
        data = data.format("{}%".format(value), "Muy Alto Riesgo")
    elif 5 <= value <= 10:
        print("alto riesgo")
        data = data.format("{}%".format(value), "Alto Riesgo")
    elif 1 <= value <= 5:
        print("moderado riesgo")
        data = data.format("{}%".format(value), "Moderado Riesgo")
    else:
        print("bajo")
        data = data.format("{}%".format(value), "Bajo Riesgo")
    return data


def resultados(request, pk):
    import ast
    pr = mod.PredictionsResult.objects.get(id=pk)
    print("file:")
    # print(pr.get_data())
    gm = GeneralMetrics(pr)
    table_metric, extra = gm.processing_data()

    general_metric = {}
    pre = pr.id_regresion_lm.accuracy
    result = pr.__dict__.copy()
    pre = float(ast.literal_eval(result["prediction"])[0][0])
    result["prediction"] = "{:.2%}".format(pre)
    result["details"] = validar_rcv_tag(pre)
    #result["precision"] = pre
    result.pop("_state", None)
    result.pop("id", None)
    print(f"EXTRA DATA: {extra}")
    return render(request, 'resultados.html', {"prediction_r": result, "general_R": general_metric,
                                               "metrics": table_metric, "extra_info": extra})


def login(request):
    if request.user.is_authenticated():  # Si el usuario ya esta logueado, no hay sentido mostrarle el logeo
        return redirect(home)
    else:
        if request.method == 'POST':
            form = forms.FormLogin(request.POST)
            if form.is_valid():
                username = form.cleaned_data["username"]
                password = form.cleaned_data["password"]
                user = authenticate(username=username, password=password)
                if user is None:
                    users = User.objects.filter(email=username)
                    if len(users) > 0:
                        user = authenticate(username=users[0].username, password=password)
                if user is not None:
                    if user.is_active:
                        auth_login(request, user)
                        if request.user.has_perm("spaapp.esAdmin"):
                            return redirect(list_models)
                        elif request.user.has_perm("spaapp.esTransportista"):
                            return redirect(index)
                        else:
                            # raise PermissionDenied("No tienes ningun rol!")
                            return redirect(home)
                    else:
                        # Return a 'disabled account' error message
                        print("User %s has valid credentials, but a disabled account." % username)
                else:
                    # Return an 'invalid login' error message.
                    print("Invalid Login for \"%s\"" % username)
            else:
                print("Invalid Form Data")
            return render(request, "login.html", {'form': form})
        else:
            form = forms.FormLogin()
    return render(request, "login.html", {'form': form})


def perfil_lipidico(request):
    result = None
    if request.method == "POST":
        form = request.POST
        print(form["col_t"])
        print(form["trigliceridos"])
        print(form["ldl_c"])
        print(form["hdl_c"])
        print(form["no_hdl_c"])
        print(form["sexo"])
        col_t = int(form["col_t"]) if form["col_t"] else 0
        tri = int(form["trigliceridos"]) if form["trigliceridos"] else 0
        ldl_c = int(form["ldl_c"]) if form["ldl_c"] else 0
        hdl_c = int(form["hdl_c"]) if form["hdl_c"] else 0
        no_hdl_c = int(form["no_hdl_c"]) if form["no_hdl_c"] else 0
        sexo = True if form["sexo"] == "1" else False
        pl = PerfilLipidico(sexo, col_t, hdl_c, no_hdl_c, tri, ldl_c)
        result = pl.results()
    return render(request, "perfil_lipidico.html", {"details": result})


def clear_data(request):
    list_file = get_files_directory(settings.BASE_DIR_DATASET_TO_CLEAR)
    json_pretty = {}
    if request.method == "POST":
        form = request.POST
        print("form: {}".format(form))
        file_path = os.path.join(settings.BASE_DIR_DATASET_TO_CLEAR, form.get("file"))
        print("data: {}".format(file_path))
        ftp = FileToProcess(file_path)
        if form.get("clear_option", "auto") == "auto":
            auto_clear = Automatic(ftp)
            auto_clear.clear_file()
            print("valor name: {}".format(form.get("new_name")))
            if get_binary(form.get("risk_option")):
                auto_clear.calc_risk()
            if get_binary(form.get("perfil_limpidico")):
                auto_clear.calc_perfil_limpidico()
            auto_clear.write_changes()
            auto_clear.save_file(form.get("descriptionModel"))
            json_pretty = json.dumps(auto_clear.get_info(), sort_keys=True, indent=4)
        else:
            print("data: {}".format(type(bool(form.get("risk_option")))))
            json_pretty = json.dumps({"result": "Option not supported!"}, sort_keys=True, indent=4)

    return render(request, "limpiar_datos.html", {"details": json_pretty, "files": list_file})


def train_model(request, id_model):
    try:
        my_model = mod.RegressionLinearModel.objects.get(id_model=id_model)
    except mod.RegressionLinearModel.DoesNotExist:
        return HttpResponseNotFound("Module not found!")
    print(id_model)
    if request.method == "POST":
        file_path = settings.BASE_DIR + settings.BASE_DIR_DATASET + "/" + "DataSet-EN-JUN-2018-LIPIDOS-20190922180553.csv"
        ftp = FileToProcess(file_path)

        mlr = MLR(ftp, ["PAS", "PAD"], ["IMC"])
        mlr.train_model(1)
        #mlr.start()
        #mlr.save_model()
    return render(request, "train_model.html", {"model": my_model})


def list_models(request):
    models_regression = mod.RegressionLinearModel.objects.all()
    return render(request, "list_models.html", {"models": models_regression})


def list_data(request):
    files = mod.FileToProcess.objects.all()
    return render(request, "list_data.html", {"data": settings.BASE_DIR_DATASET, "files": files})


def prediction(request, id_model):
    data = {}
    try:
        model_data = mod.RegressionLinearModel.objects.get(id_model=id_model)
        model_data.config_columns()
    except mod.RegressionLinearModel.DoesNotExist:
        return HttpResponseNotFound("Model not found!")

    if request.method == "POST":
        print(request.POST)
        x_data = create_array(request.POST, model_data)
        mlr = MLR()
        data = mlr.prediction(x_data, model_data)
        print("results: {}".format(data.pk))
        return redirect(resultados, data.pk)
    return render(request, "prediction.html", {"model": model_data, "var_binary": ["SEXO","DMT2","HTA","FUMADOR","ALCOHOL","TTO_ANTI-HTA","TTOASPIRINA","ENFERMEDAD_ADICIONAL","IC","IC_","HOSPITALIZACION","MUERTE_CV"]})


def update_file(request):
    # name = "EN-JUN-2018-LIPIDOS-20190915192214.csv"
    name = "BP_LIPIDOS_GENERAL_940ptes.csv"
    path = os.path.join(settings.BASE_DIR_DATASET, name)
    base = os.getcwd()
    print("base: {}".format(base))
    print("path: {}".format(path))

    absolute_path = os.path.join(base, path)
    print("absolute: {}".format(absolute_path))
    ftp = FileToProcess(absolute_path)
    mod.FileToProcess.objects.create(file_name=name, file_path=path, columns=ftp.get_headers())
    return render(request, "base.html", {})


def create_model(request, id_data):
    try:
        model_data = mod.FileToProcess.objects.get(id_file=id_data)
        model_data.columns = ast.literal_eval(model_data.columns)
    except mod.RegressionLinearModel.DoesNotExist:
        return HttpResponseNotFound("Module not found!")
    if request.method == "POST":
        form = request.POST
        ftp = FileToProcess(model_data.get_absolute_path())
        mlr = create_mlr(request.POST, ftp)
        mlr.create_model()
        mlr.save_model(model_data, form.get("nameModel"), form.get("descriptionModel"))
        print("data: {}".format(form))
    else:
        print(model_data.get_absolute_path())
    return render(request, "crete_model.html", {"data": model_data})


def send_email(request):
    from django.http import JsonResponse
    if request.method == "POST":
        print("send email to: {}".format(request.POST["email"]))

        subject = request.POST["name"]
        message = request.POST["message"]
        email_from = settings.EMAIL_HOST_USER
        recipient_list = [request.POST["email"]]
        print(subject)
        print(message)
        print(email_from)
        print(recipient_list)
        send_mail(subject, message, email_from, recipient_list)
    return JsonResponse({"result": "success"})
