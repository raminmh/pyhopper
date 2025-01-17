# Copyright 2021 Mathias Lechner and the PyHopper team
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


from __future__ import absolute_import

import pyhopper.cancellers as cancellers
import pyhopper.callbacks as callbacks
from pyhopper.parameters import Parameter as Parameter
from pyhopper.parallel import CancelEvaluation as CancelEvaluation
from pyhopper.search import Search as Search
from pyhopper.search import register_float as float
from pyhopper.search import register_int as int
from pyhopper.search import register_custom as custom
from pyhopper.search import register_choice as choice
from pyhopper.utils import NTimesEvaluator as wrap_n_times
from pyhopper.utils import parse_timeout as parse_timeout
from pyhopper.utils import ParamInfo
from pyhopper.utils import CandidateType