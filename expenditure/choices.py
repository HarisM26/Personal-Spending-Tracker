from django.db import models


class LEAGUE(models.TextChoices):
    BRONZE = 'bronze', ('bronze')
    SILVER = 'silver', ('silver')
    GOLD = 'gold', ('gold')
    PLATINUM = 'platinum', ('platinum')
    DIAMOND = 'diamond', ('diamond')


LIMIT_STATUS = [
    ('reached', ('reached')),
    ('not reached', ('not reached')),
    ('approaching', ('approaching'))
]

TIME_LIMIT_TYPE = [
    ('daily', ('Daily')),
    ('weekly', ('Weekly')),
    ('monthly', ('Monthly')),
    ('yearly', ('Yearly'))
]

STATUS_CHOICE = [
    ('unread', ('unread')),
    ('read', ('read'))
]

TOGGLE_CHOICE = [
    ('ON', ('ON')),
    ('OFF', ('OFF'))
]
