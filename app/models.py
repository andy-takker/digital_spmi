from app import db


class Resource(db.Model):
    __tablename__ = 'RESOURCES'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    amount = db.Column(db.REAL)
    unit = db.Column(db.String)
    price = db.Column(db.REAL)
    datetime = db.Column(db.DATE)

    def __repr__(self):
        return '<Resource {}>'.format(self.title)

    def to_dict(self):
        return {"title":self.title,
                "id": self.id,
                "amount": self.amount,
                "": self.unit,
                "price": self.price,
                "cost" : self.price*self.amount,
                "date": self.datetime.strftime("%d-%m-%Y")
                }
