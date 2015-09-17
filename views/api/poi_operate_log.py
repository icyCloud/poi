# -*- coding: utf-8 -*-
__author__ = 'jiangfuqiang'

from views.base import BtwBaseHandler
from tools.log import Log, log_request
from models.poi_operate_log_mapping import PoiOperateLogModel as PoiOperateLogMapping
from config import showMotivations
from config import showModeuls
import traceback

class OperateLogAPIHandler(BtwBaseHandler):

    @log_request
    def get(self):
        otaId = self.get_query_argument('otaId',None)
        if otaId:
            otaId = int(otaId)
        name = self.get_query_argument('name',None)
        module = self.get_query_argument('module',None)
        if module:
            module = int(module)

        motivation = self.get_query_argument('motivation',None)
        if motivation:
            motivation = int(motivation)
        operator = self.get_query_argument('operator',None)
        startDate = self.get_query_argument('startDate',None)
        endDate = self.get_query_argument('endDate', None)
        start = int(self.get_query_argument('start',0))
        limit = int(self.get_query_argument('limit',10))
        operateLogs,total = PoiOperateLogMapping.get_poilog(self.db,otaId=otaId,hotelName=name,module=module,motivation=motivation,operator=operator,startDate=startDate,endDate=endDate,start=start,limit=limit)
        operateDatas = []
        for operateLog in operateLogs:
            olDict = operateLog
            olDict['motivationName'] = showMotivations[olDict['motivation']]
            olDict['moduleName']=showModeuls[olDict['module']]
            operateDatas.append(olDict)
        self.finish_json(result=dict(operateDatas=operateDatas,start=start,limit=limit,total=total))
