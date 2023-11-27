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


class RoleEnum(Enum):
    USER = "USER"
    SERVICE_PROVIDER = "SERVICE_PROVIDER"
    ADMIN = "ADMIN"
    EDITOR = "EDITOR"


class RoleGQLEnum(graphene.Enum):
    class Meta:
        name = "RoleEnum"

    USER = RoleEnum.USER
    SERVICE_PROVIDER = RoleEnum.SERVICE_PROVIDER
    ADMIN = RoleEnum.ADMIN
    EDITOR = RoleEnum.EDITOR
