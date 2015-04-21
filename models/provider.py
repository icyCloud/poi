# -*- coding: utf-8 -*-

from sqlalchemy import Column
from sqlalchemy.dialects.mysql import BIT, INTEGER, VARCHAR, DATETIME, TIMESTAMP

from models import Base
import cache


class ProviderModel(Base):

    __tablename__ = 'provider'
    __table_args__ = {
        'mysql_charset': 'utf8', 'mysql_engine': 'InnoDB'}

    id = Column(INTEGER(unsigned=True), primary_key=True, autoincrement=True)
    chain_id = Column("chainId", INTEGER, nullable=False)
    name = Column(VARCHAR(20), nullable=False)
    contact = Column(VARCHAR(20), nullable=False)
    phone = Column(VARCHAR(50), nullable=False)
    email = Column(VARCHAR(200))
    is_delete = Column('isDelete', BIT, nullable=False, default=0)
    ts_update = Column('tsUpdate', TIMESTAMP, nullable=False)
    type = Column(INTEGER, nullable=False, default=0)

    MC_ALL_PROVIDERS = __tablename__ + "mc_all_providers"
    MC_ALL_PROVIDERS_COUNT = __tablename__ + "mc_all_providers_count"

    @classmethod
    def get_by_id(cls, session, id):
        return session.query(ProviderModel)\
                .filter(ProviderModel.id == id, ProviderModel.is_delete == 0).first()

    @classmethod
    def get_by_ids(cls, session, ids):
        rs = [cls.get_by_id(session, id) for id in ids]
        return [r for r in rs if r]

    @classmethod
    def add(cls, session, name, contact, phone, email):
        provider = ProviderModel(
                name=name,
                contact=contact,
                phone=phone,
                email=email)


        session.add(provider)
        session.commit()
        #cache.delete(cls.MC_ALL_PROVIDERS_COUNT)
        #cache.delete(cls.MC_ALL_PROVIDERS)
        return provider

    @classmethod
    def delete(cls, session, id):
        provider = cls.get_by_id(session, id)
        if provider:
            provider.is_delete = 1
            session.commit()
            #cache.delete(cls.MC_ALL_PROVIDERS_COUNT)
            #cache.delete(cls.MC_ALL_PROVIDERS)

    @classmethod
    def update(cls, session, id, name, contact, phone, email):
        provider = cls.get_by_id(session, id)
        if provider:
            provider.name = name
            provider.contact = contact
            provider.phone = phone
            provider.email = email
            session.commit()
            #cache.delete(cls.MC_ALL_PROVIDERS)
            return provider


    @classmethod
    @cache.mc(MC_ALL_PROVIDERS)
    def get_all(cls, session, start=None, limit=None):
        #query = session.query(ProviderModel)\
                #.filter(ProviderModel.is_delete == 0)

        #if start is None and limit is None:
            #def creator():
                #return query.all()
            #return cache.get_or_create(cls.MC_ALL_PROVIDERS, creator)

        #else:
            #if start:
                #query = query.offset(start)
            #if limit:
                #query = query.limit(limit)

            #return query.all()

        query = session.query(ProviderModel)\
                .filter(ProviderModel.is_delete == 0)
        if start:
            query = query.offset(start)
        if limit:
            query = query.limit(limit)
        return query.all()

    def tojson(self):
        return dict(
                id=self.id,
                chain_id=self.chain_id,
                name=self.name,
                contact=self.contact,
                phone=self.phone,
                email=self.email)

    @classmethod
    #@cache.mc(MC_ALL_PROVIDERS_COUNT)
    def get_count(cls, session):
        return session.query(ProviderModel)\
                .filter(ProviderModel.is_delete == 0).count()

    @classmethod
    def query_by_provider_and_contact(cls, session, provider=None, contact=None):
        query = session.query(ProviderModel)
        if provider:
            query = query.filter(ProviderModel.name.like(u'%{}%'.format(provider)))
        if contact:
            query = query.filter(ProviderModel.contact.like(u'%{}%'.format(contact)))

        return query.all()



