from foundry_client import get_client
from test_viisp_login_sdk.ontology.objects import TestViispLogin
from pydantic import BaseModel


class ViispLoginData(BaseModel):
    kodas: str
    miestas: str
    imone: str


def get_data(asm_kodas):
    client = get_client()
    TestViispLoginObject = client.ontology.objects.TestViispLogin.where(TestViispLogin.object_type.asmens_kodas == asm_kodas)
    items = []
    for item in list(TestViispLoginObject.iterate()):
        items.append(ViispLoginData(kodas=item.kodas, imone=item.imone, miestas=item.miestas))

    return items