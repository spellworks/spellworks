from spellworks import db


class ModelMixin(object):
    def delete(self):
        if hasattr(self, 'deleted'):
            self.deleted = True
            db.session.add(self)
        else:
            db.session.delete(self)
        try:
            db.session.commit()
        except Exception, e:
            db.session.rollback()
            raise e

    def update(self):
        db.session.add(self)
        try:
            db.session.commit()
        except Exception, e:
            db.session.rollback()
            raise e

    def __repr__(self):
        return "<class: {0}, id: {1}>".format(self.__class__.__name__, self.id)
