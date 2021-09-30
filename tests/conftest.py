from app import app
import pytest
import json


@pytest.fixture
def client():
    return app.test_client()


@pytest.fixture
def eval_dict():
    submit_dict = {"manifest":
                   {"files": [
                    {"url": "http://synbiohub.org/expose/b41e63d6-10f4-4cac-b1c8-285f71156b56", "filename": "asdfasdf.xls", "type": "application/vnd.ms-excel"},
                    {"url": "http://synbiohub.org/expose/jkl9d8s7ufjqhoer8u709s", "filename": "file_name1.dna", "type": "application/xml"},
                    {"url": "http://synbiohub.org/expose/basdf-11230948f4-12344cac", "filename": "file_name2.xml", "type": "application/xml"},
                    {"url": "http://synbiohub.org/expose/09uj2k3j0", "filename": "file_name3.xml", "type": "application/xml"},
                    {"url": "http://synbiohub.org/expose/asdfasdf56", "filename": "file_name4.xml", "type": "application/xml"}
                    ]}
                   }
    submit_json = json.dumps(submit_dict)
    return submit_json


@pytest.fixture
def run_dict():
    run_dict = {"manifest": {"files": [
                            {
                                "filename": "0WaHXIKZD10gRGdC8U7weHWC.html",
                                "type": "text/html",
                                "url": "https://synbiohub.org/public/igem/BBa_E0040/1/sbol"
                            },
                            {
                                "filename": "Somethingelse.html",
                                "type": "text/html",
                                "url": "https://dev.synbiohub.org/expose/e9665a54-dbdd-485e-a20b-574e46412fc4"
                            }],
                            },
                "instanceUrl": "https://dev.synbiohub.org/"
                }
    run_json = json.dumps(run_dict)
    return run_json
