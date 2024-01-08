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
    CAR_WASH = "car_wash"
    EXTERIOR_DETAILING = "exterior_detailing"
    GLASS_DETAILING = "glass_detailing"
    INTERIOR_DETAILING = "interior_detailing"
    COLOR_CORRECTION = "color_correction"
    HEADLIGHT_RESTORATION = "headlight_restoration"


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
    SEDAN = "sedan"
    HATCHBACK = "hatchback"
    PICKUP = "pickup"
    SUV = "suv"
    VAN = "van"
    CLOSE_VAN = "close_van"
    CARAVAN = "caravan"
    MOTORCYCLE = "motorcycle"


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
