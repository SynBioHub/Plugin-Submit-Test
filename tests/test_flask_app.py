

def test_status(client):
    resp = client.get('/status')
    assert resp.status_code == 200


def test_get_eval(client):
    resp = client.get('/evaluate')
    assert resp.status_code == 405


def test_eval_post(client, eval_dict):
    resp = client.post('/evaluate', data=eval_dict)
    assert resp.status_code == 200


def test_post_eval_dict(client, eval_dict):
    """Tests that the response manifest is the expected length and all
    requirements are 0,1, or 2
    """
    resp = client.post('/evaluate', data=eval_dict)
    file_list = resp.json['manifest']
    assert len(file_list) == 5
    for file in file_list:
        assert file['requirement'] in range(3)


def test_run_get(client, run_dict):
    # can't test run endpoint further without knowing what
    # kinds of sbol files it can handle
    # so just test that the run endpoint exists
    resp = client.get('/run')
    assert resp.status_code == 405
