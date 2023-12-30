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


class ServiceTypeEnum(Enum):
    CAR_WASH = "Car wash"
    EXTERIOR_DETAILING = "Exterior detailing"
    GLASS_DETAILING = "Glass detailing"
    INTERIOR_DETAILING = "Interior detailing"
    COLOR_CORRECTION = "Color Correction"
    HEADLIGHT_RESTORATION = "Headlight Restoration"


class ServiceTypeGQLEnum(graphene.Enum):
    class Meta:
        name = "ServiceTypeEnum"

    CAR_WASH = ServiceTypeEnum.CAR_WASH
    EXTERIOR_DETAILING = ServiceTypeEnum.EXTERIOR_DETAILING
    GLASS_DETAILING = ServiceTypeEnum.GLASS_DETAILING
    INTERIOR_DETAILING = ServiceTypeEnum.INTERIOR_DETAILING
    COLOR_CORRECTION = ServiceTypeEnum.COLOR_CORRECTION
    HEADLIGHT_RESTORATION = ServiceTypeEnum.HEADLIGHT_RESTORATION


class VehicleTypeEnum(Enum):
    SEDAN = "Sedan"
    HATCHBACK = "Hatchback"
    PICKUP = "Pickup"
    SUV = "SUV"
    VAN = "Van"
    CLOSE_VAN = "Close Van"
    CARAVAN = "Caravan"
    MOTORCYCLE = "Motorcycle"


class VehicleTypeGQLEnum(graphene.Enum):
    class Meta:
        name = "VehicleTypeEnum"

    SEDAN = VehicleTypeEnum.SEDAN
    HATCHBACK = VehicleTypeEnum.HATCHBACK
    PICKUP = VehicleTypeEnum.PICKUP
    SUV = VehicleTypeEnum.SUV
    VAN = VehicleTypeEnum.VAN
    CLOSE_VAN = VehicleTypeEnum.CLOSE_VAN
    CARAVAN = VehicleTypeEnum.CARAVAN
    MOTORCYCLE = VehicleTypeEnum.MOTORCYCLE
