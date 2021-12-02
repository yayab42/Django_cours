import asyncio
from asgiref.sync import sync_to_async
from django.core.exceptions import ObjectDoesNotExist

from rdv.models import Rdv


async def send_list(socket):
    """
    This socket send push redirect to the site in order to change the current page. This is used to navigate the site
    with Alexa
    :param socket:
    :return:
    """
    await socket.accept()

    get_number_rdv = sync_to_async(_get_number_rdv, thread_sensitive=True)
    number = await get_number_rdv()
    while True:
        try:
            get_number_rdv = sync_to_async(_get_number_rdv, thread_sensitive=True)
            new_number = await get_number_rdv()
            if number < new_number:
                get_last_rdv_start = sync_to_async(_get_last_rdv_start, thread_sensitive=True)
                last_rdv_start = await get_last_rdv_start()
                await socket.send_json({'last_start_booked': last_rdv_start})
                await socket.receive_json()
                print(f'La date à bien été envoyé au client')
                number += 1
            await asyncio.sleep(1)
        except Exception as ex:
            print(f'Exception with the socket : {ex} /  name-->{type(ex).__name__}')
            break
    await socket.close()


# |--------------------|
# |  sync sql request  |
# |--------------------|

def _get_number_rdv():
    try:
        number = Rdv.objects.all().count()
        return number
    except ObjectDoesNotExist:
        return False


def _get_last_rdv_start():
    try:
        last_start = Rdv.objects.last()
        return last_start.start
    except ObjectDoesNotExist:
        return False
