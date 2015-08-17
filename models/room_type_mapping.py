# -*- coding: utf-8 -*-

from models import Base
from sqlalchemy import Column
from sqlalchemy.dialects.mysql import BIT, INTEGER, VARCHAR, DATETIME, TIMESTAMP, TINYINT
from sqlalchemy.sql import exists, text
from tornado.util import ObjectDict
from sqlalchemy import  or_, and_

class RoomTypeMappingModel(Base):

    __tablename__ = 'roomTypeMapping'
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
    provider_hotel_id = Column('chainHotelId', VARCHAR(50), nullable=False)
    provider_roomtype_id = Column('chainRoomTypeId', VARCHAR(50), nullable=False)
    provider_roomtype_name = Column('chainRoomTypeName', VARCHAR(50), nullable=False)
    main_hotel_id = Column('mainHotelId', INTEGER(unsigned=True), nullable=False)
    main_roomtype_id = Column('mainRoomTypeId', INTEGER(unsigned=True), nullable=False)
    status = Column(TINYINT(4, unsigned=True), nullable=False)
    is_online = Column('onlineStatus', INTEGER, nullable=False, default=0)
    is_delete = Column('isDelete', BIT, nullable=False, default=0)
    is_new =  Column('isNew', BIT, nullable=False, default=0)
    ts_update = Column('tsUpdate', TIMESTAMP, nullable=False, server_default=text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'))
    info = Column(VARCHAR(100))

    @classmethod
    def new_roomtype_mapping_from_ebooking(cls, session, provider_hotel_id, provider_roomtype_id, provider_roomtype_name, main_hotel_id, main_roomtype_id):
        mapping = RoomTypeMappingModel(provider_id=6, provider_hotel_id=str(provider_hotel_id), provider_roomtype_id=provider_roomtype_id, provider_roomtype_name=provider_roomtype_name, main_hotel_id=main_hotel_id, main_roomtype_id=main_roomtype_id, status=cls.STATUS.valid_complete, is_new=1)
        session.add(mapping)
        session.commit()
        return mapping

    @classmethod
    def get_by_provider_roomtype(cls, session, provider_id, provider_roomtype_id):
        return session.query(RoomTypeMappingModel)\
                .filter(RoomTypeMappingModel.provider_id == provider_id)\
                .filter(RoomTypeMappingModel.provider_roomtype_id == provider_roomtype_id)\
                .filter(RoomTypeMappingModel.is_delete == 0)\
                .first()

    @classmethod
    def get_by_provider_and_main_roomtype(cls, session, provider_id, provider_roomtype_id, main_roomtype_id):
        return session.query(RoomTypeMappingModel)\
                .filter(RoomTypeMappingModel.provider_id == provider_id)\
                .filter(RoomTypeMappingModel.provider_roomtype_id == provider_roomtype_id,
                        RoomTypeMappingModel.main_roomtype_id == main_roomtype_id)\
                .filter(RoomTypeMappingModel.is_delete == 0)\
                .first()


    @classmethod
    def get_by_id(cls, session, id):
        return session.query(RoomTypeMappingModel)\
                .filter(RoomTypeMappingModel.id == id, RoomTypeMappingModel.is_delete == 0)\
                .first()

    @classmethod
    def get_by_ids(cls, session, ids):
        return session.query(RoomTypeMappingModel)\
                .filter(RoomTypeMappingModel.id.in_(ids))\
                .filter(RoomTypeMappingModel.is_delete == 0)\
                .all()

    @classmethod
    def gets_by_provider_hotel_id(cls, session, id):
        return session.query(RoomTypeMappingModel)\
                .filter(RoomTypeMappingModel.provider_hotel_id == str(id))\
                .filter(RoomTypeMappingModel.is_delete == 0)\
                .all()

    @classmethod
    def get_by_provider_hotel_ids(cls, session, ids):
        return session.query(RoomTypeMappingModel)\
                .filter(RoomTypeMappingModel.provider_hotel_id.in_(ids))\
                .filter(RoomTypeMappingModel.is_delete == 0)\
                .all()

    @classmethod
    def get_firstvalid_by_provider_hotel_ids(cls, session, ids):
        return session.query(RoomTypeMappingModel)\
                .filter(RoomTypeMappingModel.provider_hotel_id.in_(ids))\
                .filter(RoomTypeMappingModel.is_delete == 0)\
                .filter(RoomTypeMappingModel.status != cls.STATUS.init)\
                .all()

    @classmethod
    def get_secondvalid_by_provider_hotel_ids(cls, session, ids):
        return session.query(RoomTypeMappingModel)\
                .filter(RoomTypeMappingModel.provider_hotel_id.in_(ids))\
                .filter(RoomTypeMappingModel.is_delete == 0)\
                .filter(or_(RoomTypeMappingModel.status == cls.STATUS.wait_second_valid,RoomTypeMappingModel.status == cls.STATUS.valid_complete))\
                .all()

    @classmethod
    def get_polymer_provider_hotel_ids(cls, session, ids):
        return session.query(RoomTypeMappingModel)\
                .filter(RoomTypeMappingModel.provider_hotel_id.in_(ids))\
                .filter(RoomTypeMappingModel.is_delete == 0)\
                .filter(RoomTypeMappingModel.status == cls.STATUS.valid_complete)\
                .all()

    @classmethod
    def get_polymer_by_provider_hotels(cls, session, provider_id, ids):
        return session.query(RoomTypeMappingModel)\
                .filter(RoomTypeMappingModel.provider_id == provider_id)\
                .filter(RoomTypeMappingModel.provider_hotel_id.in_(ids))\
                .filter(RoomTypeMappingModel.is_delete == 0)\
                .filter(RoomTypeMappingModel.status == cls.STATUS.valid_complete)\
                .all()

    @classmethod
    def gets_wait_firstvalid_by_provider(cls, session, provider_id):
        return session.query(RoomTypeMappingModel)\
                .filter(RoomTypeMappingModel.is_delete == 0)\
                .filter(RoomTypeMappingModel.status == cls.STATUS.wait_first_valid)\
                .filter(RoomTypeMappingModel.provider_id == provider_id)\
                .all()

    @classmethod
    def gets_wait_firstvalid_by_provider_and_hotel(cls, session, provider_id, hotel_id):
        return session.query(RoomTypeMappingModel)\
                .filter(RoomTypeMappingModel.is_delete == 0)\
                .filter(RoomTypeMappingModel.status == cls.STATUS.wait_first_valid)\
                .filter(RoomTypeMappingModel.provider_id == provider_id)\
                .filter(RoomTypeMappingModel.provider_hotel_id == hotel_id)\
                .all()

    @classmethod
    def gets_wait_secondvalid_by_provider(cls, session, provider_id):
        return session.query(RoomTypeMappingModel)\
                .filter(RoomTypeMappingModel.is_delete == 0)\
                .filter(RoomTypeMappingModel.status == cls.STATUS.wait_second_valid)\
                .filter(RoomTypeMappingModel.provider_id == provider_id)\
                .all()

    @classmethod
    def reset_mapping_by_provider_hotel_id(cls, session, provider_hotel_id, main_hotel_id):
        session.query(RoomTypeMappingModel)\
                .filter(RoomTypeMappingModel.provider_hotel_id == provider_hotel_id)\
                .filter(RoomTypeMappingModel.is_delete == 0)\
                .update({RoomTypeMappingModel.main_hotel_id: main_hotel_id,
                         RoomTypeMappingModel.main_roomtype_id: 0,
                         RoomTypeMappingModel.status: cls.STATUS.init})
        session.commit()

    @classmethod
    def reset_mapping_by_id(cls, session, id, main_hotel_id):
        session.query(RoomTypeMappingModel)\
                .filter(RoomTypeMappingModel.id == id)\
                .filter(RoomTypeMappingModel.is_delete == 0)\
                .update({RoomTypeMappingModel.main_hotel_id: main_hotel_id,
                         RoomTypeMappingModel.main_roomtype_id: 0,
                         RoomTypeMappingModel.status: cls.STATUS.wait_first_valid})
        session.commit()

    @classmethod
    def update_main_hotel_id(cls, session, id, main_roomtype_id):
        r = cls.get_by_id(session, id)
        if r:
            r.main_roomtype_id = main_roomtype_id
            r.status = cls.STATUS.wait_first_valid
            session.commit()
        return r

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
    def revert_to_firstvalid_by_provider_hotel_id(cls, session, provider_hotel_id):
        session.query(RoomTypeMappingModel)\
                .filter(RoomTypeMappingModel.provider_hotel_id == provider_hotel_id)\
                .filter(RoomTypeMappingModel.is_delete == 0)\
                .update({RoomTypeMappingModel.status: cls.STATUS.wait_first_valid,
                            RoomTypeMappingModel.is_online: 0})
        session.commit()

    @classmethod
    def disable_by_provider_hotel_id(cls, session, provider_hotel_id):
        session.query(RoomTypeMappingModel)\
                .filter(RoomTypeMappingModel.provider_hotel_id == provider_hotel_id)\
                .filter(RoomTypeMappingModel.is_delete == 0)\
                .update({RoomTypeMappingModel.is_online: 0})
        session.commit()

    @classmethod
    def set_online(cls, session, id, is_online):
        r = cls.get_by_id(session, id)
        if r:
            r.is_online =  is_online
            r.is_new = 0
            session.commit()

        return r

    def todict(self):
        return ObjectDict(
                id=self.id,
                provider_id=self.provider_id,
                provider_hotel_id=self.provider_hotel_id,
                provider_roomtype_id=self.provider_roomtype_id,
                provider_roomtype_name=self.provider_roomtype_name,
                main_hotel_id=self.main_hotel_id,
                main_roomtype_id=self.main_roomtype_id,
                status=self.status,
                is_online=self.is_online,
                is_delete=self.is_delete,
                info=self.info,
                is_new=self.is_new,
                )
