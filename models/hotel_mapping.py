# -*- coding: utf-8 -*-

from models import Base
from sqlalchemy import Column, or_, and_
from sqlalchemy.dialects.mysql import BIT, INTEGER, VARCHAR, DATETIME, TIMESTAMP, TINYINT
from sqlalchemy.sql import exists, text
from tornado.util import ObjectDict


class HotelMappingModel(Base):

    __tablename__ = 'hotelMapping'
    __table_args__ = {
        'mysql_charset': 'utf8', 'mysql_engine': 'InnoDB'}

    STATUS = ObjectDict({
        'init': 0,
        'wait_first_valid': 1,
        'wait_second_valid': 2,
        'valid_complete': 3
    })

    id = Column(INTEGER(unsigned=True), primary_key=True, autoincrement=True)
    provider_id = Column('chainId', INTEGER(unsigned=True), nullable=False)
    provider_hotel_id = Column(
        'chainHotelId', VARCHAR(50), nullable=False)
    provider_hotel_name = Column(
        'chainHotelName', VARCHAR(50), nullable=False)
    provider_hotel_address = Column(
        'chainHotelAddress', VARCHAR(100), nullable=False)
    city_id = Column('cityId', INTEGER(unsigned=True), nullable=False)
    main_hotel_id = Column(
        'mainHotelId', INTEGER(unsigned=True), nullable=False)
    status = Column(TINYINT(4, unsigned=True), nullable=False)
    is_online = Column('onlineStatus', INTEGER, nullable=False, default=0)
    is_delete = Column('isDelete', BIT, nullable=False, default=0)
    is_new =  Column('isNew', BIT, nullable=False, default=0)
    info = Column(VARCHAR(100))
    merchant_id = Column("merchantId", INTEGER, nullable=False, default=0)
    merchant_name = Column("merchantName", VARCHAR(50), nullable=False, default='')
    ts_update = Column('tsUpdate', TIMESTAMP, nullable=False, server_default=text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'))


    @classmethod
    def get_by_id(cls, session, id):
        return session.query(HotelMappingModel)\
            .filter(HotelMappingModel.id == id, HotelMappingModel.is_delete == 0)\
            .first()

    @classmethod
    def get_by_provider_and_main_hotel(cls, session, provider_id, provider_hotel_id, main_hotel_id):
        return session.query(HotelMappingModel)\
                .filter(HotelMappingModel.provider_id==provider_id,
                        HotelMappingModel.provider_hotel_id==str(provider_hotel_id),
                        HotelMappingModel.main_hotel_id==main_hotel_id)\
                .filter(HotelMappingModel.is_delete == 0)\
                .first()

    @classmethod
    def get_by_chain_id_and_main_hotel_id(cls, session, provider_id, main_hotel_id):
        return session.query(HotelMappingModel)\
                .filter(HotelMappingModel.provider_id==provider_id,
                        HotelMappingModel.main_hotel_id==main_hotel_id)\
                .filter(HotelMappingModel.is_delete == 0)\
                .all()

    @classmethod
    def get_by_provider_hotel(cls, session, provider_id, provider_hotel_id):
        return session.query(HotelMappingModel)\
                .filter(HotelMappingModel.provider_id==provider_id,
                        HotelMappingModel.provider_hotel_id==str(provider_hotel_id))\
                .filter(HotelMappingModel.is_delete == 0)\
                .first()

    @classmethod
    def gets_wait_firstvalid(cls, session, start=0, limit=20):
        return session.query(HotelMappingModel)\
            .filter(HotelMappingModel.is_delete == 0)\
            .filter(HotelMappingModel.status == cls.STATUS.wait_first_valid)\
            .offset(start)\
            .limit(limit)\
            .all()

    @classmethod
    def new_hotel_mapping_from_ebooking(cls, session, provider_hotel_id, provider_hotel_name, provider_hotel_address, city_id, main_hotel_id, merchant_id, merchant_name):
        mapping = HotelMappingModel(provider_id=6, provider_hotel_id=str(provider_hotel_id), provider_hotel_name=provider_hotel_name,
                provider_hotel_address=provider_hotel_address, city_id=city_id, main_hotel_id=main_hotel_id,
                status=cls.STATUS.valid_complete, is_online=0, merchant_id=merchant_id, merchant_name=merchant_name, is_new=1)
        session.add(mapping)
        session.commit()
        return mapping



    @classmethod
    def gets_show_in_firstvalid(cls, session, provider_id=None, hotel_name=None, city_id=None, start=0, limit=20):
        from models.room_type_mapping import RoomTypeMappingModel
        stmt = exists().where(and_(HotelMappingModel.provider_id == RoomTypeMappingModel.provider_id,
                HotelMappingModel.provider_hotel_id == RoomTypeMappingModel.provider_hotel_id,
                RoomTypeMappingModel.status == RoomTypeMappingModel.STATUS.wait_first_valid,
                RoomTypeMappingModel.is_delete == 0))

        query = session.query(HotelMappingModel)
        if provider_id:
            query = query.filter(HotelMappingModel.provider_id == provider_id)
        if city_id:
            query = query.filter(HotelMappingModel.city_id == city_id)
        if hotel_name:
            query = query.filter(HotelMappingModel.provider_hotel_name.like(u'%{}%'.format(hotel_name)))

        query = query\
                .filter(HotelMappingModel.provider_id != 6)\
                .filter(HotelMappingModel.is_delete == 0)\
                .filter(HotelMappingModel.status != cls.STATUS.init)\
                .filter(or_(stmt, HotelMappingModel.status == cls.STATUS.wait_first_valid))


        r = query.offset(start).limit(limit).all()
        total = query.count()

        return r, total

    @classmethod
    def gets_show_in_secondvalid(cls, session, provider_id=None, hotel_name=None, city_id=None, start=0, limit=20):
        from models.room_type_mapping import RoomTypeMappingModel
        stmt = exists(
        ).where(and_(HotelMappingModel.provider_id == RoomTypeMappingModel.provider_id,
                HotelMappingModel.provider_hotel_id == RoomTypeMappingModel.provider_hotel_id,
                RoomTypeMappingModel.status == RoomTypeMappingModel.STATUS.wait_second_valid,
                RoomTypeMappingModel.is_delete == 0))

        query = session.query(HotelMappingModel)
        if provider_id:
            query = query.filter(HotelMappingModel.provider_id == provider_id)
        if city_id:
            query = query.filter(HotelMappingModel.city_id == city_id)
        if hotel_name:
            query = query.filter(HotelMappingModel.provider_hotel_name.like(u'%{}%'.format(hotel_name)))

        query = query\
                .filter(HotelMappingModel.provider_id != 6)\
                .filter(HotelMappingModel.is_delete == 0)\
                .filter(HotelMappingModel.status != cls.STATUS.init)\
                .filter(or_(stmt, HotelMappingModel.status == cls.STATUS.wait_second_valid))


        r = query.offset(start).limit(limit).all()
        total = query.count()

        return r, total

    @classmethod
    def gets_show_in_polymer(cls, session, provider_id=None, hotel_name=None, city_id=None, show_online_type=0, start=0, limit=20):
        query = session.query(HotelMappingModel)\
            .filter(HotelMappingModel.provider_id != 6)\
            .filter(HotelMappingModel.is_delete == 0)\
            .filter(HotelMappingModel.status == cls.STATUS.valid_complete)

        if provider_id:
            query = query.filter(HotelMappingModel.provider_id == provider_id)
        if city_id:
            query = query.filter(HotelMappingModel.city_id == city_id)

        if show_online_type == 1:
            query = query.filter(HotelMappingModel.is_online == 1)
        elif show_online_type == 2:
            query = query.filter(HotelMappingModel.is_online == 0)

        if hotel_name:
            query = query.filter(HotelMappingModel.provider_hotel_name.like(u'%{}%'.format(hotel_name)))
        
        r = query.offset(start).limit(limit).all()
        total = query.count()

        return r, total

    @classmethod
    def gets_show_in_ebooking(cls, session, hotel_name=None, city_id=None, merchant_ids=None, is_new=None, start=0, limit=20):
        query = session.query(HotelMappingModel)\
                .filter(HotelMappingModel.is_delete == 0)\
                .filter(HotelMappingModel.provider_id == 6,
                        HotelMappingModel.status == cls.STATUS.valid_complete)

        if is_new is not None:
            from models.room_type_mapping import RoomTypeMappingModel
            stmt = exists().where(and_(HotelMappingModel.provider_id == RoomTypeMappingModel.provider_id,
                        HotelMappingModel.provider_hotel_id == RoomTypeMappingModel.provider_hotel_id,
                        RoomTypeMappingModel.is_new == 1,
                        RoomTypeMappingModel.is_delete == 0))
            query = query.filter(or_(stmt, HotelMappingModel.is_new == is_new))

        if city_id:
            query = query.filter(HotelMappingModel.city_id == city_id)
        if merchant_ids is not None:
            query = query.filter(HotelMappingModel.merchant_id.in_(merchant_ids))
        if hotel_name:
            query = query.filter(HotelMappingModel.provider_hotel_name.like(u'%{}%'.format(hotel_name)))

        r = query.order_by(HotelMappingModel.id.desc()).offset(start).limit(limit).all()
        total = query.count()

        return r, total

    @classmethod
    def count_wait_firstvalid_count(cls, session):
        return session.query(HotelMappingModel)\
            .filter(HotelMappingModel.is_delete == 0)\
            .filter(HotelMappingModel.status == cls.STATUS.wait_first_valid)\
            .count()

    @classmethod
    def count_show_in_firstvalid(cls, session, start=0, limit=20):
        from models.room_type_mapping import RoomTypeMappingModel
        stmt = exists(
        ).where(and_(HotelMappingModel.provider_hotel_id == RoomTypeMappingModel.provider_hotel_id,
                RoomTypeMappingModel.status == RoomTypeMappingModel.STATUS.wait_first_valid,
                RoomTypeMappingModel.is_delete == 0))
        return session.query(HotelMappingModel)\
                .filter(HotelMappingModel.is_delete == 0)\
                .filter(HotelMappingModel.status != cls.STATUS.init)\
                .filter(or_(HotelMappingModel.status == cls.STATUS.wait_first_valid, stmt))\
                .count()

    @classmethod
    def gets_wait_second(cls, session):
        return session.query(HotelMappingModel)\
            .filter(HotelMappingModel.is_delete == 0)\
            .filter(HotelMappingModel.status == cls.STATUS.wait_second_valid)\
            .all()

    @classmethod
    def set_firstvalid_complete(cls, session, id):
        r = cls.get_by_id(session, id)
        if r:
            r.status = cls.STATUS.wait_second_valid
            session.commit()

        return r

    @classmethod
    def set_secondvalid_complete(cls, session, id):
        r = cls.get_by_id(session, id)
        if r:
            r.status = cls.STATUS.valid_complete
            session.commit()

        return r

    @classmethod
    def revert_to_firstvalid(cls, session, id):
        r = cls.get_by_id(session, id)
        if r:
            r.status = cls.STATUS.wait_first_valid
            r.is_online = 0
            session.commit()

        return r

    @classmethod
    def set_online(cls, session, id, is_online):
        r = cls.get_by_id(session, id)
        if r:
            r.is_online =  is_online
            r.is_new = 0
            session.commit()

        return r

    @classmethod
    def delete(cls, session, id):
        r = cls.get_by_id(session, id)
        if r:
            r.is_delete = 1
            session.commit()

        return r

    @classmethod
    def change_main_hotel_id(cls, session, id, hotel_id):
        r = cls.get_by_id(session, id)
        if r:
            r.main_hotel_id = hotel_id
            session.commit()

        return r



    def todict(self):
        return ObjectDict(
            id=self.id,
            provider_id=self.provider_id,
            provider_hotel_id=self.provider_hotel_id,
            provider_hotel_name=self.provider_hotel_name,
            provider_hotel_address=self.provider_hotel_address,
            city_id=self.city_id,
            main_hotel_id=self.main_hotel_id,
            status=self.status,
            is_online=self.is_online,
            is_delete=self.is_delete,
            info=self.info,
            merchant_id=self.merchant_id,
            merchant_name=self.merchant_name,
            is_new=self.is_new,
            )
