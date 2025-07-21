import pytest
from rest_framework.test import APIClient
from model_bakery import baker
from students.models import Student, Course


@pytest.fixture
def base_url():
    base_url = "/api/v1/courses/"
    return base_url


@pytest.fixture
def client():
    return APIClient()


@pytest.fixture
def student_factory():
    def factory(*args, **kwargs):
        return baker.make(Student, *args, **kwargs)

    return factory

@pytest.fixture
def course_factory():
    def factory(*args, **kwargs):
        return baker.make(Course, *args, **kwargs)

    return factory


@pytest.mark.django_db
def test_list(client, course_factory, student_factory, base_url):

    #Arrange

    students = student_factory(_quantity=5)
    course = course_factory(_quantity=5, students=students)

    #Act

    response = client.get(base_url)

    #Assert

    # Список курсов успешно получен
    assert response.status_code == 200
    # Количество курсов в списке равно количеству созданных
    assert len(response.json()) == len(course)
    # Данные курсов в списке соответствуют созданным
    for i, c in enumerate(response.json()):
        assert c['name'] == course[i].name


@pytest.mark.django_db
def test_retrieve(client, course_factory, base_url):

    #Arrange

    course_factory(_quantity=1)

    #Act

    response_crt = client.get(base_url)
    url = base_url + str(response_crt.json()[0]["id"]) + "/"
    response_rtv = client.get(url)

    #Assert

    # Данные запрошенного курса успешно получены
    assert response_rtv.status_code == 200
    # Данные запрошенного курса совпадают с данными созданного курса
    assert response_rtv.json() == response_crt.json()[0]


@pytest.mark.django_db
def test_create(client, base_url):

    #Arrange

    data={'name':'Philosophy', 'students':[]}

    #Act

    response = client.post(base_url, data=data)

    #Assert

    # Курс создан успешно
    assert response.status_code == 201
    # Курс с заданными параметрами создан успешно
    response.json().pop('id')
    assert response.json() == data

@pytest.mark.django_db
def test_patch(course_factory, student_factory, client, base_url):

    #Arrange

    students = student_factory(_quantity=1)
    course = course_factory(_quantity=1, students=students)
    data={'name':'Philosophy', 'students':[students[0].id]}

    #Act

    response_crt = client.get(base_url)
    url = base_url + str(course[0].id) + "/"
    response_upd = client.patch(url, data=data)

    #Assert

    # Курс создан успешно
    assert response_crt.status_code == 200
    # Данные курса успешно обновлены
    assert response_upd.status_code == 200
    # id созданного курса совпадают с id обновлённого курса (обновлён правильный курс)
    assert response_upd.json()["id"] == response_crt.json()[0]["id"]
    # Данные созданного курса успешно обновлены на новые
    response_upd.json().pop('id')
    assert response_upd.json() == data


@pytest.mark.django_db
def test_destroy(course_factory, client, base_url):

    #Arrange

    course_factory(_quantity=1)

    #Act

    response_crt = client.get(base_url)
    url = base_url + str(response_crt.json()[0]["id"]) + "/"
    response_del = client.delete(url)
    response_chk = client.get(url)

    #Assert

    # Курс создан успешно
    assert response_crt.status_code == 200
    # Курс успешно удалён
    assert response_del.status_code == 204
    # Курс с id созданного курса более не доступен (удалён правильный курс)
    assert response_chk.status_code == 404


@pytest.mark.django_db
def test_filtering_by_id(client, course_factory, base_url):

    #Arrange

    course_factory(_quantity=5)
    test_query = client.get(base_url).json()[2]
    url = base_url + f'?id={test_query["id"]}'

    #Act

    response = client.get(url)

    #Assert

    # Список курсов c искомым id успешно получен
    assert response.status_code == 200
    # Результат фильтрации по id уникален
    assert len(response.json()) == 1
    # Данные курса c искомым id соответствуют созданному курсу c id
    assert response.json()[0] == test_query


@pytest.mark.django_db
def test_filtering_by_name(client, course_factory, base_url):

    #Arrange

    course_factory(_quantity=5)
    test_query = client.get(base_url).json()[2]
    url = base_url + f'?name={test_query["name"]}'

    #Act

    response = client.get(url)

    #Assert

    # Список курсов c искомым name успешно получен
    assert response.status_code == 200
    # Результат фильтрации по name уникален
    assert len(response.json()) == 1
    # Данные курса c искомым name соответствуют созданному курсу c name
    assert response.json()[0] == test_query


@pytest.mark.parametrize(
    'max_student_count, students_count, response_status',
    [(20, 10, 201), (20, 20, 201), (20, 30, 400)]
)
@pytest.mark.django_db
def test_max_students(client,
                      course_factory,
                      student_factory,
                      base_url,
                      settings,
                      max_student_count,
                      students_count,
                      response_status):
    settings.MAX_STUDENTS_PER_COURSE = max_student_count
    students = student_factory(_quantity=students_count)

    response = client.post(base_url, data={
        'name': 'Philosophy',
        'students': [item.id for item in students]
    })
    # Проверка заполнения курса данными студентов
    assert response.status_code == response_status