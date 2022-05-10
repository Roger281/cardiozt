from sklearn.linear_model import LinearRegression
from ..models import RegressionLinearModel as RLM


class ModelRL:
    def __init__(self, model: LinearRegression = None):
        self.model = model

    def save_model(self):
        if self.model:
            model_rl = RLM()
            model_rl.coef = list(self.model.coef_)
            model_rl.intercept = self.model.intercept_.tolist()
            model_rl.save()
        else:
            raise Exception("No hay modelo establecido")

    @staticmethod
    def get_model(id_model) -> LinearRegression:
        rml = RLM.objects.get(id_model=id_model)

        lr = LinearRegression()
        lr.coef_ = rml.coef
        lr.intercept_ = rml.intercept
        return lr

    def edit_model(self, id_model):
        pass

    def delete_model(self, id_model):
        pass
