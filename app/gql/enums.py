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


class AccountRoleEnum(Enum):
    USER = "USER"
    SERVICE_PROVIDER = "SERVICE_PROVIDER"
    ADMIN = "ADMIN"
    EDITOR = "EDITOR"


class AccountRoleGQLEnum(graphene.Enum):
    class Meta:
        name = "AccountRoleEnum"

    USER = AccountRoleEnum.USER
    SERVICE_PROVIDER = AccountRoleEnum.SERVICE_PROVIDER
    ADMIN = AccountRoleEnum.ADMIN
    EDITOR = AccountRoleEnum.EDITOR
