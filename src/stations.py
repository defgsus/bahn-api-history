from pathlib import Path
import hashlib
import os
import datetime

import dateutil.parser
import pandas as pd
import numpy as np
from tqdm import tqdm

from .changelog_reader import ChangelogReader
from .mapper import ObjectMapper
from .filter import *


class StationMapper(ObjectMapper):

    def __init__(self):
        super().__init__("stations")

