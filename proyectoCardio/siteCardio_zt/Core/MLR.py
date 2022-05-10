from time import gmtime, strftime
from .FileToProcess import FileToProcess
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn import linear_model
from .ModelRL import ModelRL
from siteCardio_zt.models import  PredictionsResult
from siteCardio_zt.models import RegressionLinearModel
from django.conf import settings
from sklearn.externals import joblib
import os


class MLR:

    def __init__(self,
                 file_to_process: FileToProcess = None,
                 column_name_x: list = None,
                 column_name_y: list = None,
                 test_size: float = 0.2,
                 model_path: str = settings.BASE_DIR_MODEL,
                 file_name: str = None):

        self.file_to_process = file_to_process
        self.column_name_x = column_name_x
        self.column_name_y = column_name_y
        self.test_size = test_size
        self.model_rl = None
        self.model_path = model_path
        self.accuracy = None
        self.file_name = file_name

    @staticmethod
    def _get_model(model: RegressionLinearModel):
        file = os.path.join(model.model_path, model.file_name)
        print("get_file: {}".format(file))
        return joblib.load(file)

    def start(self):
        X_multiple = self.file_to_process.get_columns_numpy(self.column_name_x)
        print(X_multiple)
        print(type(X_multiple))
        # Defino los datos correspondientes a las etiquetas
        y_multiple = self.file_to_process.get_columns_numpy(self.column_name_y)

        # Separo los datos de "train" en entrenamiento y prueba para probar los algoritmos
        X_train, X_test, y_train, y_test = train_test_split(X_multiple, y_multiple, test_size=self.test_size)
        # Defino el algoritmo a utilizar
        self.model_rl = linear_model.LinearRegression()
        print("#########################::::::")
        print(type(self.model_rl))
        # Entreno el modelo
        self.model_rl.fit(X_train, y_train)
        # Realizo una predicción
        Y_pred_multiple = self.model_rl.predict(X_test)

        print('PREDICCION DEL MODELO DE REGRESIÓN LINEAL MULTIPLE')
        print(Y_pred_multiple)
        print('DATOS DEL MODELO REGRESIÓN LINEAL MULTIPLE')
        print()
        print('Valor de las pendientes o coeficientes "a":')
        print(self.model_rl.coef_)
        print('Valor de la intersección o coeficiente "b":')
        print(self.model_rl.intercept_)
        print('Precisión del modelo:')
        self.accuracy = self.model_rl.score(X_train, y_train)
        print(self.model_rl.score(X_train, y_train))

    def prediction(self, x_test, model: RegressionLinearModel):
        lr = self._get_model(model)
        p = lr.predict(x_test)
        pr = PredictionsResult(coef=lr.coef_, id_regresion_lm=model, intercept=lr.intercept_, prediction=p)
        pr.save()
        return pr

    def train_model(self, x_multiple, y_multiple, model=None):

        # Separo los datos de "train" en entrenamiento y prueba para probar los algoritmos
        X_train, X_test, y_train, y_test = train_test_split(x_multiple, y_multiple, test_size=self.test_size)
        if model:
            model.fit(X_train, y_train)
            self.model_rl = model
        else:
            self.model_rl.fit(X_train, y_train)

        print('Precisión del modelo:')
        self.accuracy = self.model_rl.score(X_train, y_train)
        print(self.model_rl.score(X_train, y_train))
        print("OK")

    def create_model(self):
        x_multiple = self.file_to_process.get_columns_numpy(self.column_name_x)
        y_multiple = self.file_to_process.get_columns_numpy(self.column_name_y)
        self.model_rl = linear_model.LinearRegression()
        self.train_model(x_multiple, y_multiple)

    def _write_model(self, extension=".sav"):
        self.file_name = "model" + "-" + strftime("%Y%m%d%H%M%S", gmtime()) + extension
        file = os.path.join(settings.BASE_DIR, self.model_path, self.file_name)
        joblib.dump(self.model_rl, file)

    def save_model(self, file, name, descrption):
        if self.model_rl:
            self._write_model()
            model_rl = RegressionLinearModel()
            model_rl.id_file = file
            model_rl.name = name
            model_rl.file_name = self.file_name
            model_rl.model_path = self.model_path
            model_rl.dependent_var = self.column_name_x
            model_rl.independent_var = self.column_name_y
            model_rl.description = descrption
            model_rl.coef = list(self.model_rl.coef_)
            model_rl.accuracy = self.accuracy
            model_rl.intercept = self.model_rl.intercept_.tolist()
            model_rl.save()
        else:
            raise Exception("The model does not exist (pls, train the model first)")
