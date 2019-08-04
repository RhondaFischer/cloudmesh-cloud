# -*- coding: utf-8 -*-
"""We use a uniform naming convention method. The name is defined by different kinds of objects. The name is a string
its syntax is defined in a yaml file located at ``~/.cloudmesh/name.yaml``

::

    order:
    - experiment
    - group
    - user
    - kind
    - counter
    schema: '{experiment}-{group}-{user}-{kind}-{counter}'
    experiment: exp
    group: grp
    user: gregor
    kind: container
    counter: 2

This file is automatically generated if it does not exists by a simple `Name` object that can include an ordered
number of dictionary keys such as

:Experiment: is an experiment that all cloud objects can be placed under.

:Group: A group formulates a number of objects that logically build an entity,
        such as a number of virtual machines building a cluster

:User: A user name that may control the group

:Kind: A kind that identifies which kind of resource this is

The last is a counter which is always increased and written into this file in order to assure that the latest
value is safely included in it.


A typical use is

::

    n = Name(experiment="exp",
             group="grp",
             user="gregor",
             kind="vm",
             counter=1)

    n.incr()
    counter = n.get()

Which will return

::

    exp-grp-gregor-vm-1

"""
import os
from pprint import pprint
from cloudmesh.common.debug import VERBOSE
import oyaml as yaml

from cloudmesh.common.dotdict import dotdict
from cloudmesh.common.util import path_expand


class Name(dotdict):

    def __init__(self, schema=None, **kwargs):
        """
        Defines a name tag that sets the format of the name to the specified schema
        :param schema:
        """

        #
        # init dict with schema, path, kwargs
        #


        if schema is None  and len(kwargs) == 0:
            path = path_expand("~/.cloudmesh/name.yaml")
            data = self.load(path)
            self.assign(data)

        else:


            self.assign(kwargs)
            if "path" not in kwargs:
                path= self.__dict__['path'] = path_expand("~/.cloudmesh/name.yaml")
                data = self.load(path)
                self.assign(data)

            if schema is not None:
                self.__dict__['schema'] = schema


        if "counter" not in self.__dict__:
            self.reset()
        else:
            self.__dict__["counter"] = int(self.__dict__["counter"])

        self.flush()

    @property
    def schema(self):
        return self.__dict__['schema']


    def set(self, schema):
        self.__dict__['schema'] = schema


    def assign(self, data):
        for entry in data:
            self.__dict__[entry] = data[entry]

    def load(self, path):

        data = {"wrong": "True"}
        if os.path.exists(path):
            with open(path, 'rb') as dbfile:
                data = yaml.safe_load(dbfile) or dict()
        else:
            prefix = os.path.dirname(path)
            if not os.path.exists(prefix):
                os.makedirs(prefix)

            data = {
                'counter': 1,
                'path': path,
                'kind': "vm",
                'schema': "{experiment}-{group}-{user}-{kind}-{counter}",
                'experiment': 'exp',
                'group': 'group',
                'user': 'user'
            }
            self.flush(data)
        return data

    def flush(self, data=None):

        if data is None:
            data = self.__dict__

        with open(data['path'], 'w') as yaml_file:
            yaml.dump(data, yaml_file, default_flow_style=False)


    def __str__(self):
        return str(self.__dict__["schema"].format(**self.__dict__))

    def dict(self):
        return self.__dict__


    def reset(self):
        self.__dict__["counter"] = 1
        self.flush()

    def incr(self):
        self.__dict__["counter"] += 1
        self.flush()



