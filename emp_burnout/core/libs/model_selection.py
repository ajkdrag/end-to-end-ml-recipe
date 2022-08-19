import logging
from dataclasses import dataclass
from xgboost import XGBRegressor
from sklearn.model_selection import GridSearchCV
from sklearn.linear_model import LinearRegression, Ridge, Lasso
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.metrics import r2_score as r2, mean_squared_error as mse

LOG = logging.getLogger(__name__)

model_classes = {
    "linear_regression": LinearRegression,
    "ridge": Ridge,
    "lasso": Lasso,
    "xgboost": XGBRegressor,
    "random_forest": RandomForestRegressor,
    "gradient_boost": GradientBoostingRegressor
}


@dataclass
class ModelSelector:
    config: dict

    def get_best_model(self, train_x, train_y, test_x, test_y):
        hyps = self.config["hyps"]
        models = hyps["models"]

        # training
        model_scores = []
        for name, attrs in models.items():
            kwargs = {}
            if name == "xgboost":
                kwargs = {"verbosity": 0, "silent": True}

            model = model_classes[name]()
            param_grid = attrs
            grid = GridSearchCV(model, param_grid, cv=5)
            grid.fit(train_x, train_y)
            best_params = grid.best_params_
            LOG.info("%s tuned. Best params: %s", name, best_params)

            best_params.update(kwargs)
            tuned_model = model_classes[name](**best_params)
            tuned_model.fit(train_x, train_y)

            # score
            r2_val = r2(test_y, tuned_model.predict(test_x))
            mse_val = mse(test_y, tuned_model.predict(test_x))
            metrics = {"r2_score": r2_val, "mse": mse_val}
            LOG.info("%s metrics: %s", name, metrics)
            model_scores.append((name, tuned_model, grid.best_params_, metrics))

        criterion = hyps["sel_criterion"]
        return max(model_scores, key=lambda el: el[-1][criterion])
