# -*- coding: utf-8 -*-

from tornado.escape import json_encode, json_decode
from tornado.util import ObjectDict

from views.base import BtwBaseHandler
from models.provider import ProviderModel

from tools.auth import auth_login, auth_permission
from constants import PERMISSIONS


class ProviderAPIHandler(BtwBaseHandler):

    @auth_login(json=True)
    def get(self):
        start = self.get_query_argument('start', None)
        limit = self.get_query_argument('limit', None)

        providers = ProviderModel.get_all(self.db, start, limit)
        total = ProviderModel.get_count(self.db)

        providers = [provider.tojson() for provider in providers]


        self.finish_json(result=dict(
            providers=providers,
            start=start,
            limit=limit,
            total=total))

    @auth_login(json=True)
    @auth_permission(PERMISSIONS.admin | PERMISSIONS.provider_list, json=True)
    def post(self):
        provider = ObjectDict(json_decode(self.request.body))

        _provider = ProviderModel.add(self.db, provider.chain_id, provider.name, provider.contact,
                provider.phone, provider.email)
        self.finish_json(result=_provider.tojson())


    @auth_login(json=True)
    @auth_permission(PERMISSIONS.admin | PERMISSIONS.provider_list, json=True)
    def put(self):
        provider = ObjectDict(json_decode(self.request.body))

        _provider = ProviderModel.get_by_id(self.db, provider.id)
        if _provider:
            try:
                _provider = ProviderModel.update(self.db, provider.id, provider.chain_id, provider.name,
                        provider.contact, provider.phone, provider.email)
                self.finish_json(result=_provider.tojson())
            except Exception, e:
                print e
                self.finish_json(errcode=507, errmsg=str(e))
        else:
            self.finish_json(errcode=404, errmsg="no user")

class ProviderQueryAPIHandler(BtwBaseHandler):

    @auth_login(json=True)
    @auth_permission(PERMISSIONS.admin | PERMISSIONS.provider_list, json=True)
    def get(self):
        provider = self.get_query_argument('provider', None)
        contact = self.get_query_argument('contact', None)

        providers = ProviderModel.query_by_provider_and_contact(self.db, provider, contact)
        providers = [dict(
            id=provider.id,
            name=provider.name,
            contact=provider.contact,
            phone=provider.phone,
            email=provider.email)
            for provider in providers]


        self.finish_json(result=dict(
            providers=providers))
