from sqlalchemy.ext.declarative import declared_attr, as_declarative
class Base():
    __abstract__ = True

    @declared_attr
    def __tablename__(self):
        return self.__name__.lower() + 's'

    def __repr__(self):
        fmt = u'{}({})'
        class_ = self.__class__.__name__
        attrs = sorted((c.name, getattr(self, c.name)) for c in self.__table__.columns)
        sattrs = u', '.join('{}={!r}'.format(*x) for x in attrs)
        return fmt.format(class_, sattrs)

def insert_or_ignore(model, **kargs):
    return model.__table__.insert(
    prefixes=['OR IGNORE'],
    values=kargs)

def insert_or_replace(model, **kargs):
    return model.__table__.insert(
    prefixes=['OR REPLACE'],
    values=kargs)
