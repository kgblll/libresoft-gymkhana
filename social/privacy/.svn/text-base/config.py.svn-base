#
#  Copyright (C) 2009 GSyC/LibreSoft
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
# 
#    Author : Jose Antonio Santos Cadenas <jcaden __at__ gsyc __dot__ es>
#


"""
This file defines how the privacy application works.
The main parameter is the variable privacy, it has this structure.

{"module.name":
    {"object":
        {"privacy_group": ["list", "of", "real", "fields" ], 
         # List is optional for privacy application but useful for upper layers
         # Only groups will be accepted as fields in field-level privacy
         # There must be a group called "basic" this will be the minimum fields
         #  present when the object is allowed, this field can not be allowed or
         #  restricted itself. This fields privacy will be always the same as the
         #  object privacy. 
        },
    }
}

The always public variable is used to open some groups of fields to every body.
If the object is in this structure, the basic group will be included by default
even if is not in the list or the list is open.

{"module.name":
    {"object": ["list", "of", "groups", "in", "privacy", "variable"],
    }
}

"""
 
privacy={"social.core.models":
             {"Person": {"basic": ["id",
                                   "name",
                                   "first_name",
                                   "last_name",
                                   "username",
                                   "status",
                                   "status_time",
                                   "tags",
                                   "type",
                                   "avatar"],
                         "position": ["position",
                                      "radius",
                                      "pos_time",
                                      "post_code",
                                      "country",
                                      ],
                         "birthday": ["birthday"],
                         "since": ["since"],
                         "email": ["email"],
                         "friends": [],
                         "photos" : [],
                         "notes" : [],
                         "groups" : [],
                        },
              "Photo" : {"basic"   : ["id",
                                      "name",
                                      "description",
                                      "photo",
                                      "tags",
                                      "type"],
                         "position": ["position",
                                      "radius",
                                      "pos_time",
                                      ],
                         "since"   : ["since"],
                         "uploader": ["uploader"],
                        },
              "Sound" : {"basic"   : ["id",
                                      "name",
                                      "description",
                                      "sound",
                                      "tags",
                                      "type"],
                         "position": ["position",
                                      "radius",
                                      "pos_time",
                                      ],
                         "since"   : ["since"],
                         "uploader": ["uploader"],
                        },
              "Note" : {"basic"    : ["id",
                                      "title",
                                      "text",
                                      "tags",
                                      "type",
                                     ],
                        "position": ["position",
                                     "radius",
                                     "pos_time",
                                     ],
                        "since"   : ["since"],
                        "uploader": ["uploader"],
                       },
              "Group" : {"basic"    : ["id",
                                       "groupname",
                                       "tags",
                                       "type",
                                      ],
                         "position": ["position",
                                      "radius",
                                      "pos_time",
                                      ],
                         "since"   : ["since"],
                         "members" : [],
                         },
              },
         "social.groupifier.models":
            {
             "DynGroup" : {"basic"    : ["id",
                                         "groupname",
                                         "tags",
                                         "type",
                                         "groupifier",
                                        ],
                           "position": ["position",
                                        "radius",
                                        "pos_time",
                                        ],
                           "since"   : ["since"],
                           "members" : [],
                           },
             },
        }

always_public={"social.core.models":
                  {"Group": ["basic", "position", "since", "members"],},
               "social.groupifier.models":
                  {"DynGroup": ["basic", "position", "since", "members"],}
              }


