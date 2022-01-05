import pandas as pd
import numpy as np
from os import system
import time

from typing import Optional
from fastapi import FastAPI, Response, status, HTTPException
from fastapi.params import Body
from pydantic import BaseModel
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from starlette.status import HTTP_404_NOT_FOUND
import pickle
