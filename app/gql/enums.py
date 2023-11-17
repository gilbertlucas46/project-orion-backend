# enums.py
import graphene
from enum import Enum


class StatusEnum(Enum):
    PENDING = "PENDING"
    VERIFIED = "VERIFIED"
    DISABLED = "DISABLED"


class StatusGQLEnum(graphene.Enum):
    class Meta:
        name = "StatusEnum"

    PENDING = StatusEnum.PENDING
    VERIFIED = StatusEnum.VERIFIED
    DISABLED = StatusEnum.DISABLED
