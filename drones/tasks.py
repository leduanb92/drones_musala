import logging
from celery import shared_task
from .models import Drone

logger = logging.getLogger('battery-level-check-logger')


@shared_task
def log_drones_battery_levels():
    message = '\n--------------------START OF CHECK--------------------\n'
    drones = Drone.objects.all()
    message += f'Total Drones: {drones.count()}\n'
    message += f'Total Drones with low battery: {Drone.objects.filter(battery_capacity__lt=25).count()}\n'
    message += 'Battery level of each drone:'
    for drone in drones:
        message += f'  ({drone.serial_number} --> {drone.battery_capacity})'
    message += '\n---------------------END OF CHECK--------------------'

    logger.info(message)
