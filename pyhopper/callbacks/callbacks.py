import pickle
import os

import pyhopper
from pyhopper.utils import ParamInfo
import time


class Callback:
    def on_search_start(self, search: "pyhopper.Search"):
        """Called at the beginning of the search

        :param search: `pyhopper.Search` object handling the search
        """
        pass

    def on_evaluate_start(self, candidate: dict, info: ParamInfo):
        """Called after `candidate` was sampled and scheduled for evaluation

        :param candidate: Parameter value of the candidate to be evaluated
        """
        pass

    def on_evaluate_end(self, candidate: dict, f: float, info: ParamInfo):
        """Called after `candidate` was successfully evaluated

        :param candidate: Parameter value of the evaluated candidate
        :param f: Value of the objective function corresponding to the candidate
        """
        pass

    def on_evaluate_cancelled(self, candidate: dict, info: ParamInfo):
        """Called if `candidate` was cancelled (by an :meth:`pyhopper.cancellers.EarlyCanceller`)

        :param candidate: Parameter value of the cancelled candidate
        """
        pass

    def on_new_best(self, new_best: dict, f: float, info: ParamInfo):
        """Called when a new best parameter is found

        :param new_best: Value of the new best parameter
        :param f: Value of the objective function corresponding to the new best parameter
        """
        pass

    def on_search_end(self):
        """Called at the end of the search process"""
        pass


class History:
    """
    Public API for the history of the search. Can be used by the user for plotting and analyzing the search space.
    Persistent over several consecutive calls of ```run```
    """

    def __init__(self, keep_full_record=False):
        self._keep_full_record = keep_full_record
        self._log_candidate = []
        self._log_types = []
        self._log_f = []
        self._log_arrive_time = []
        self._log_best_f = []
        self._log_runtime = []

        self._cancelled_types = []
        self._cancelled_candidates = []
        self._cancelled_arrive_time = []
        self._cancelled_runtime = []
        self._start_time = time.time()

    def append_cancelled(self, candidate, candidate_type, runtime):
        self._cancelled_runtime.append(runtime)
        self._cancelled_types.append(candidate_type)
        self._cancelled_arrive_time.append(time.time() - self._start_time)
        if self._keep_full_record:
            self._cancelled_candidates.append(candidate)

    @property
    def keep_full_record(self):
        return self._keep_full_record

    def append(self, candidate, candidate_type, runtime, f, best_f):
        if self._keep_full_record:
            self._log_candidate.append(candidate)
        self._log_types.append(candidate_type)
        self._log_f.append(f)
        self._log_arrive_time.append(time.time() - self._start_time)
        self._log_best_f.append(best_f)
        self._log_runtime.append(runtime)

    def __getitem__(self, item):
        if not self._keep_full_record:
            raise ValueError(
                f"Error: Candidates were not recorded because ```keep_parameter_history``` argument passed to "
                f"```pyhopper.Search``` was set to False. "
            )
        return self._log_candidate[item]

    def get_marginal(self, item):
        if not self._keep_full_record:
            raise ValueError(
                f"Error: Candidates were not recorded because ```keep_parameter_history``` argument passed to "
                f"```pyhopper.Search``` was set to False. "
            )
        if len(self._log_candidate) > 0:
            if item not in self._log_candidate[0].keys():
                raise ValueError(
                    f"Error: Could not find key '{item}' in logged parameters"
                )
        return [self._log_candidate[i][item] for i in range(len(self._log_candidate))]

    def get_cancelled_marginal(self, item):
        if not self._keep_full_record:
            raise ValueError(
                f"Error: Candidates were not recorded because ```keep_parameter_history``` argument passed to "
                f"```pyhopper.Search``` was set to False. "
            )
        if len(self._cancelled_candidates) > 0:
            if item not in self._cancelled_candidates[0].keys():
                raise ValueError(
                    f"Error: Could not find key '{item}' in logged parameters"
                )
        return [
            self._cancelled_candidates[i][item]
            for i in range(len(self._cancelled_candidates))
        ]

    def __len__(self):
        return len(self._log_f)

    @property
    def fs(self):
        return self._log_f

    @property
    def best_f(self):
        return self._log_best_f[-1]

    @property
    def best_fs(self):
        return self._log_best_f

    @property
    def steps(self):
        return list(range(len(self._log_f)))

    @property
    def seconds(self):
        return self._log_arrive_time

    @property
    def minutes(self):
        return [t / 60 for t in self._log_arrive_time]

    @property
    def hours(self):
        return [t / 60 / 60 for t in self._log_arrive_time]

    def __repr__(self):
        repr_str = f"pyhopper.History(len={len(self)}"
        if len(self) > 0:
            repr_str += f", best={self.best_f:0.3g}"
        repr_str += ")"
        return repr_str

    def clear(self):
        self._log_candidate = []
        self._log_types = []
        self._log_f = []
        self._log_arrive_time = []
        self._log_best_f = []
        self._log_runtime = []

        self._cancelled_types = []
        self._cancelled_candidates = []
        self._cancelled_arrive_time = []
        self._cancelled_runtime = []
        self._start_time = time.time()


class SaveBestOnDisk(Callback):
    def __init__(self, filename=None, dir=None):
        if dir is not None and filename is not None:
            raise ValueError("Cannot specify filename and dir at the same time.")
        if dir is not None:
            os.makedirs(dir, exist_ok=True)
            for i in range(10000):
                filename = os.path.join(dir, f"run_{i:05d}.pkl")
                if not os.path.isfile(filename):
                    break

        self._filename = filename

    @property
    def filename(self):
        return self._filename

    def on_new_best(self, new_best, f):
        with open(self._filename, "wb") as f:
            pickle.dump(new_best, f)