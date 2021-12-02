"""
ASGI config for project_0 project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application
from rdv.socket import websocket_application


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project_0.settings')

django_application = get_asgi_application()


async def application(scope, receive, send):
    if scope['type'] == 'http':
        # Let Django handle HTTP requests
        await django_application(scope, receive, send)
    elif scope['type'] == 'websocket':
        await websocket_application(scope, receive, send)
    else:
        raise NotImplementedError(f"Unknown scope type {scope['type']}")


async def websocket_applciation(scope, receive, send):
    pass