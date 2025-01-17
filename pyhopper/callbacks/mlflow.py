import mlflow
from datetime import datetime
import os
import pickle


class MLflowCallback:
    def __init__(self, experiment_name=None, run_name=None):
        if experiment_name is None:
            experiment_name = "Pyhopper"
        mlflow.set_experiment(experiment_name)
        mlflow.start_run(run_name=run_name)
        self._best_params = None

    def on_search_start(self, search):
        mlflow.log_params(search.current_run_config)

    def on_evaluate_start(self, candidate):
        pass

    def on_evaluate_end(self, candidate, f):

        mlflow.log_metric("sampled_f", f)

    def on_new_best(self, new_best, f):
        self._best_params = new_best

        mlflow.log_metric("best_f", f)

    def on_search_end(self, history):
        os.makedirs("pyhopper_runs", exist_ok=True)
        filename = os.path.join(
            "pyhopper_runs", datetime.now().strftime("best_params_%Y%m%d_%H%M%S.pkl")
        )
        with open(filename, "wb") as f:
            pickle.dump(self._best_params, f)
        mlflow.log_artifact(filename)
        mlflow.end_run()