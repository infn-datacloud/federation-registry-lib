from fastapi import FastAPI, HTTPException
from fastapi.security import HTTPBearer
from flaat.fastapi import Flaat
import logging

logging.basicConfig(level="DEBUG")
logging.getLogger("flaat").setLevel("DEBUG")
logging.getLogger("urllib3").setLevel("DEBUG")


app = FastAPI()
security = HTTPBearer()

flaat = Flaat()

# todo: move the list of trusted idps to configuration file
flaat.set_trusted_OP_list(
    [
        "https://iam.cloud.infn.it/"
    ])
flaat.set_request_timeout(30)
flaat.set_verbosity(verbosity=3,set_global=True)
