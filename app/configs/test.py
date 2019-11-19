# -*- coding: utf-8 -*-

from datetime import timedelta
from .common import Common


class Config(Common):
    TESTING = True
    TRANS_COMMENT = "automation[test]"
    CELERYBEAT_SCHEDULE = {
        'get_masternodes_online_data': {
            'task': 'tasks.common.get_masternodes_online_data',
            'schedule': timedelta(minutes=5),
            'args': None,
            'options': {
                'queue': 'celery',
            },
        },
        'disk_monitor': {
            'task': 'tasks.common.disk_monitor',
            'schedule': timedelta(hours=1),
            'args': None,
            'options': {
                'queue': 'celery',
            },
        },
    }
