# -*- coding: utf-8 -*-

from models import Base
from sqlalchemy import Column
from sqlalchemy.dialects.mysql import BIT, INTEGER, VARCHAR, DATETIME, TIMESTAMP, TINYINT, FLOAT
from tornado.util import ObjectDict

class RoomTypeModel(Base):

    __tablename__ = 'roomType'
    __table_args__ = {
        'mysql_charset': 'utf8', 'mysql_engine': 'InnoDB'}


    id = Column(INTEGER(unsigned=True), primary_key=True, autoincrement=True)
    elong_id = Column('elongId', VARCHAR(50), nullable=False)
    hotel_id = Column('hotelId', INTEGER(unsigned=True), nullable=False)
    name = Column(VARCHAR(50), nullable=False)
    floor = Column(VARCHAR(50), nullable=False)
    area = Column(FLOAT, nullable=False)
    broadnet_access = Column('broadnetAccess', BIT, default=0, nullable=False)
    broadnet_fee = Column('broadnetFee', BIT, default=0, nullable=False)
    comments = Column(VARCHAR(300))
    description = Column(VARCHAR(300))
    capacity = Column(TINYINT(4), nullable=False)
    bed_type = Column('bedType', INTEGER(unsigned=True), nullable=False)
    facility = Column(VARCHAR(300))
    is_valid = Column('isValid', BIT, default=0, nullable=False)
    is_online = Column('isOnline', BIT, default=0, nullable=False)


    @classmethod
    def get_by_id(cls, session, id, need_online=False, need_valid=False):
        q = session.query(RoomTypeModel)\
                .filter(RoomTypeModel.id == id)
        if need_online:
            q = q.filter(RoomTypeModel.is_online == 1)

        if need_valid:
            q = q.filter(RoomTypeModel.is_valid == 1)

        return q.first()

    @classmethod
    def get_by_ids(cls, session, ids, need_online=False, need_valid=False):
        q = session.query(RoomTypeModel)\
                .filter(RoomTypeModel.id.in_(ids))
        if need_online:
            q = q.filter(RoomTypeModel.is_online == 1)

        if need_valid:
            q = q.filter(RoomTypeModel.is_valid == 1)

        return q.all()

    @classmethod
    def gets_by_hotel_id(cls, session, hotel_id, need_online=False, need_valid=False):
        q = session.query(RoomTypeModel)\
                .filter(RoomTypeModel.hotel_id == hotel_id)

        if need_online:
            q = q.filter(RoomTypeModel.is_online == 1)

        if need_valid:
            q = q.filter(RoomTypeModel.is_valid == 1)

        return q.all()


    @classmethod
    def gets_by_hotel_ids(cls, session, hotel_ids, need_online=False, need_valid=False):
        q = session.query(RoomTypeModel)\
                .filter(RoomTypeModel.hotel_id.in_(hotel_ids))

        if need_online:
            q = q.filter(RoomTypeModel.is_online == 1)

        if need_valid:
            q = q.filter(RoomTypeModel.is_valid == 1)

        return q.all()

    @classmethod
    def new(cls, session, hotel_id, name, area="",
            floor="", comments="", description="",
            capacity=-1, facility="", bed_type=-1,
            broadnet_access=0, broadnet_fee=0, elong_id=0,
            is_online=1, is_valid=1):
        roomtype = RoomTypeModel(hotel_id=hotel_id, name=name, area=area,
                floor=floor, comments=comments, description=description,
                capacity=capacity, facility=facility, bed_type=bed_type,
                broadnet_fee=broadnet_fee, broadnet_access=broadnet_access,
                elong_id=elong_id, is_online=1, is_valid=1)
        session.add(roomtype)
        session.commit()
        return roomtype

    @classmethod
    def update(cls, session, id, name=None, area=None,
            floor=None, comments=None, description=None,
            capacity=None, facility=None, bed_type=None,
            broadnet_access=None, broadnet_fee=None, elong_id=None,
            is_online=None, is_valid=None, *argv, **kwargs):
        roomtype = cls.get_by_id(session, id)
        if roomtype:
            if name is not None:
                roomtype.name = name
            if area is not None:
                roomtype.area = area
            if floor is not None:
                roomtype.floor = floor 
            if comments is not None:
                roomtype.comments = comments
            if description is not None:
                roomtype.description = description
            if capacity is not None:
                roomtype.capacity = capacity 
            if facility is not None:
                roomtype.facility = facility
            if bed_type is not None:
                roomtype.bed_type = bed_type
            if broadnet_access is not None:
                roomtype.broadnet_access = broadnet_access
            if broadnet_fee is not None:
                roomtype.broadnet_fee = broadnet_fee
            if elong_id is not None:
                roomtype.elong_id = elong_id
            if is_online is not None:
                roomtype.is_online = is_online 
            if is_valid is not None:
                roomtype.is_valid = is_valid

            roomtype.is_valid = 1
            session.commit()
            return roomtype



    def todict(self):
        return ObjectDict(
                id=self.id,
                hotel_id=self.hotel_id,
                name=self.name,
                floor=self.floor,
                area=self.area,
                comments=self.comments,
                description=self.description,
                bed_type=self.bed_type,
                is_valid=self.is_valid,
                is_online=self.is_online,
                capacity=self.capacity,
                broadnet_access=self.broadnet_access,
                broadnet_fee=self.broadnet_fee,
                facility=self.facility,
                )
