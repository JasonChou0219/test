"""
__________________________________________________________________________________________________

:project: SiLA2_python

:details: Basic data type for all standard SiLA data types.

:file:    type_basic.py
:authors: Timm Severin
          mark doerr

:date: (creation)          20190820
:date: (last modification) 20190820

__________________________________________________________________________________________________

**Copyright**:
  This file is provided "AS IS" with NO WARRANTY OF ANY KIND,
  INCLUDING THE WARRANTIES OF DESIGN, MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE.

  For further Information see LICENSE file that comes with this distribution.
__________________________________________________________________________________________________
"""

# import general packages
import logging
import datetime

# import meta packages
from typing import Any

# import package related packages
from .type_base import DataType


class BasicType(DataType):
    """
    Class for the basic data type as defined in the SiLA standards.
    """

    #: Default value, only available for BasicTypes
    default_value: Any
    default_response_values: str

    basic_data_types = {'Boolean': {'description': 'Basic logic/boolean type',
                                    'default_value': False,
                                    'default_response_values': "value=False",
                                    'python_type': 'bool'},
                        'Integer': {'description': 'Basic integer type',
                                    'default_value': 1,
                                    'default_response_values': "value=1",
                                    'python_type': 'int'},
                        'Real': {'description': 'Basic float/double type',
                                 'default_value': 1.0,
                                 'default_response_values': "value=1.0",
                                 'python_type': 'float'},
                        'String': {'description': 'Basic string type',
                                   'default_value': "'default string'",
                                   'default_response_values': "value='default string'",
                                   'python_type': 'str'},
                        'Binary': {'description': 'Basic byte type',
                                   'default_value': b"1",
                                   'default_response_values': "value=b'1'",
                                   'python_type': 'bytes'},
                        'Void': {'description': 'Void/empty type',
                                 'default_value': b"",
                                 'default_response_values': "value=b''",
                                 'python_type': 'bytes'},
                        'Date': {'description': 'Basic date type',
                                 'default_value': datetime.datetime.utcnow().strftime("%Y-%m-%d+0000"),
                                 'default_response_values': "day=1,month=2,year=3,timezone=silaFW_pb2.Timezone(hours=0, minutes=0)",
                                 'python_type': 'datetime.datetime'},
                        'Time': {'description': 'Basic time type',
                                 'default_value': datetime.datetime.utcnow().strftime("%H:%M:%S+0000"),
                                 'default_response_values': "second=1, minute=2, hour=3,timezone=silaFW_pb2.Timezone(hours=0, minutes=0)",
                                 'python_type': 'datetime.datetime'},
                        'Timestamp': {'description': 'Basic timestamp type',
                                      'default_value': datetime.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S+0000"),
                                      'default_response_values': "second=1, minute=2,hour=3, day=4, month=5, year=6, timezone=silaFW_pb2.Timezone(hours=0, minutes=0)",
                                      'python_type': 'datetime.datetime'},
                        }

    def __init__(self, xml_tree_element):
        """
        Class initialiser.: param xml_tree_element: The content of this < Basic > -xml element that contains this basic type.

        .. note: : For remaining parameters see : meth: `~.DataType.__init__`.

        .. note: : Date, Time and Timestamp follow the
                  `W3C format for .xsd < https: // www.w3.org/TR/xmlschema11-2 /  # dateTime>`_
                  files which in turn relies on `ISO 8601 < https: // en.wikipedia.org/wiki/ISO_8601 >`_
        """
        super().__init__(xml_tree_element=xml_tree_element)

        # Set specific data
        self.is_basic = True
        self.sub_type = xml_tree_element.text

        # The name is simply equal to the underlying data type
        self.name = self.sub_type
        if self.name in ('Date', 'Time', 'Timestamp'):
            self.is_datetime = True

        # and now distinguish between the named types
        try:
            basic_dt_dict = self.basic_data_types[self.sub_type]
        except KeyError as err:
            logging.error(f"ERROR ({err})")

        self.description = basic_dt_dict['description']
        self.default_value = basic_dt_dict['default_value']
        self.default_response_values = basic_dt_dict['default_response_values']
        self.python_type = basic_dt_dict['python_type']
