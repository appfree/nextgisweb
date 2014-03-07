# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from sqlalchemy.orm.exc import NoResultFound

from ..component import Component, require
from ..auth import User

from .model import (
    Base,
    Resource,
    ResourceGroup,
    ResourceACLRule)
from .serialize import (
    Serializer,
    SerializedProperty,
    SerializedRelationship,
    SerializedResourceRelationship)

from .exception import *    # NOQA
from .interface import *    # NOQA
from .model import *        # NOQA
from .scope import *        # NOQA
from .permission import *   # NOQA
from .view import *         # NOQA
from .widget import *       # NOQA

__all__ = [
    'Resource',
    'IResourceBase',
    'Serializer',
    'SerializedProperty',
    'SerializedRelationship',
    'SerializedResourceRelationship',
    'Widget',
]


@Component.registry.register
class ResourceComponent(Component):
    identity = 'resource'
    metadata = Base.metadata

    @require('security')
    def initialize_db(self):
        administrator = User.filter_by(keyname='administrator').one()
        try:
            ResourceGroup.filter_by(id=0).one()
        except NoResultFound:
            obj = ResourceGroup(id=0, owner_user=administrator,
                                display_name="Основная группа ресурсов")
            obj.acl.append(ResourceACLRule(
                principal=administrator, action='allow'))
            obj.persist()

    @require('security')
    def setup_pyramid(self, config):
        from .view import setup_pyramid
        setup_pyramid(self, config)
