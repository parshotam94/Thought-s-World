
def test_login_page(client):

    response=client.get('/login')


    assert response.status_code==200



def test_register_page(client):

    response=client.get('/register')


    assert response.status_code==200


def test_home_redirect(client):


    response=client.get('/')


    assert response.status_code==302


def test_post_requires_login(client):


    response=client.post(

    '/post',

    data={

    "content":"Hello"

    }

    )


    assert response.status_code==302
