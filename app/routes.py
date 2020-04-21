from datetime import datetime

from flask import request, jsonify

from app import app, db
from app.models import Resource
from app.utils import is_int


@app.route("/")
@app.route("/about")
def about():
    return "Данный сайт создан для конкурса 'Лучшее цифровое решение' Сергеем Наталенко"


@app.route("/resources", methods=['GET','POST', 'UPDATE', 'DELETE'])
def resource():
    if request.method == 'GET':
        """Метод возвращает перечень всех ресурсов в виде JSON объекта"""
        return get_all()

    elif request.method == 'POST':
        """Метод добавляет в базу данных новую запись о сырье. На вход принимает JSON объект"""
        return insert_resource(request.args)

    elif request.method == 'UPDATE':
        """Метод обновляет запись о материале в базе данных """
        return update_resource(request.args)

    elif request.method == 'DELETE':
        """Метод удаляет из базы запись о сырье по id"""
        id = request.args.get('id', None)
        return delete_resource(id)


@app.route("/total_cost", methods=['GET'])
def total_cost():
    """Метод возвращает общую стоимость запасов на складе"""
    return get_total_cost()


"""
РЕАЛИЗАЦИЯ МЕТОДОВ РАБОТЫ С БАЗОЙ ДАННЫХ
"""


def get_all():
    resources = Resource.query.all()
    return jsonify({"resources":[res.to_dict() for res in resources], "total_count":len(resources)})


def insert_resource(params):
    if len(params) == 0:
        return jsonify({"result": "error_id"})
    title = params.get('title', "")
    amount = params.get('amount', 0)
    price = params.get('price', 0)
    date = params.get('date', '00-00-0000').split("-")
    date = datetime(day=int(date[0]), month=int(date[1]), year=int(date[2]))
    unit = params.get('','')
    r = Resource(title=title, amount=amount,price=price,datetime=date, unit=unit)
    db.session.add(r)
    db.session.commit()
    return jsonify(r.to_dict())


def update_resource(params):
    if len(params) == 0:
        return jsonify({"result": "error_id"})
    if not is_int(params.get('id')):
        return jsonify({"result": "error_id"})
    r = Resource.query.get(params.get('id'))
    title = params.get('title')
    amount = params.get('amount')
    price = params.get('price')
    date = params.get('date').split("-")
    date = datetime(day=int(date[0]), month=int(date[1]), year=int(date[2]))
    unit = params.get('', '')
    r.title = title
    r.amount = amount
    r.price = price
    r.datetime = date
    r.unit = unit
    db.session.add(r)
    db.session.commit()
    return jsonify({"result": "success"})


def delete_resource(id):
    if not is_int(id):
        return jsonify({"result": "error_id"})
    r = Resource.query.get(int(id))
    if r is None:
        return jsonify({"result": "error_no_resource"})
    db.session.delete(r)
    db.session.commit()
    return jsonify({"result": "success"})


def get_total_cost():
    total_cost = 0
    resources = Resource.query.all()
    for res in resources:
        total_cost += res.price * res.amount
    return jsonify({"total_cost": total_cost})

