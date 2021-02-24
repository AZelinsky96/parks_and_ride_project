import os
import sys
import pytest

sys.path.append(
    os.path.join(os.getcwd(), "parks_and_ride", "lambda_functions")
)

from parks_and_ride.lambda_functions.data_modelling.database_interaction import (
    DatabaseLoader
)