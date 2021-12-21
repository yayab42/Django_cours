# -*- coding: utf-8 -*-
"""
Created on Thu Oct 15 14:37:08 2020

@author: julien
"""
from django.urls import resolve
from project_0.connection import WebSocket
import logging


def mywebsockets(app):
    async def asgi(scope, receive, send):
        if scope["type"] == "websocket":
            try:
                match = resolve(scope["raw_path"].decode())
            except AttributeError:
                match = resolve(scope["raw_path"])
            await match.func(WebSocket(scope, receive, send), *match.args, **match.kwargs)
            return
        match = resolve(scope["raw_path"].decode())
        await app(scope, receive, send)
    return asgi