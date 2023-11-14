# enums.py
import graphene
from enum import Enum


class StatusEnum(Enum):
    PENDING = "PENDING"
    VERIFIED = "VERIFIED"
    DISABLED = "DISABLED"


class StatusGQLEnum(graphene.Enum):
    PENDING = StatusEnum.PENDING.value
    VERIFIED = StatusEnum.VERIFIED.value
    DISABLED = StatusEnum.DISABLED.value
