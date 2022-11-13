def get_index(app, client):
    res = client.get('/')
    assert res.status_code == 200

def post_index(app, client):
    res = client.post('/', max_datetime="2020-12-23 01:10",min_datetime="2019-12-23 01:10")
    assert res.status_code == 200

