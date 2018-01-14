from olx_discover import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

    def __repr__(self):
        return '<User %r>' % self.username


class AdsOrigin(db.Model):
    """ Ads Url Model """

    id = db.Column(db.Integer, primary_key=True, nullable=False)

    url = db.Column(db.String(256), unique=True, nullable=False)
    label = db.Column(db.String(256), nullable=False)

    ads = db.relationship('Ad', backref='ads_origin', lazy=True)


class Ad(db.Model):
    """ Advertisement Model """

    def __repr__(self):
        return '<Ad: {}>'.format(self.__str__())

    def __str__(self):
        return '{}'.format(self.label)

    ad_id = db.Column(db.Integer, primary_key=True, nullable=False)

    origin_id = db.Column(db.Integer, db.ForeignKey('ads_origin.id'))

    url = db.Column(db.String(256), unique=True, nullable=False)
    image = db.Column(db.String(256), unique=True)
    label = db.Column(db.String(256), nullable=False)
    price = db.Column(db.Float, nullable=False)
    details = db.Column(db.String(512), nullable=True)
    region = db.Column(db.String(256), nullable=True)
    inserted_in = db.Column(db.DateTime, nullable=True)
