# antigravity_sync/schema.py
import copy
import time
import uuid

# This explicit typedef ensures blackboxprotobuf never accidentally decodes string fields as sub-messages.
TOP_TYPEDEF = {
    '1': {'message_typedef': {
            '1': {'name': 'cid', 'type': 'bytes'},
            '2': {'message_typedef': {
                    '1': {'name': 'inner_payload', 'type': 'bytes'}
                 },
                 'name': 'wrapper',
                 'type': 'message'}
         },
         'name': 'items',
         'type': 'message'}
}

INNER_TYPEDEF = {
    '1': {'name': 'title', 'type': 'bytes'},
    '2': {'name': 'step_count', 'type': 'int'},
    '3': {'message_typedef': {'1': {'name': 'seconds', 'type': 'int'}, '2': {'name': 'nanos', 'type': 'int'}}, 'name': 'updated_at', 'type': 'message'},
    '4': {'name': 'uuid', 'type': 'bytes'},
    '5': {'name': 'status', 'type': 'int'},
    '7': {'message_typedef': {'1': {'name': 'seconds', 'type': 'int'}, '2': {'name': 'nanos', 'type': 'int'}}, 'name': 'created_at', 'type': 'message'},
    '9': {'message_typedef': {'1': {'name': 'workspace_uri', 'type': 'bytes'}, '3': {'message_typedef': {}, 'name': 'flags', 'type': 'message'}}, 'name': 'workspace', 'type': 'message'},
    '10': {'message_typedef': {'1': {'name': 'seconds', 'type': 'int'}, '2': {'name': 'nanos', 'type': 'int'}}, 'name': 'last_accessed', 'type': 'message'},
    '15': {'message_typedef': {}, 'name': 'extra_flags', 'type': 'message'},
    '16': {'name': 'step_count_copy', 'type': 'int'},
    '17': {'message_typedef': {
            '1': {'message_typedef': {'1': {'name': 'workspace_uri', 'type': 'bytes'}, '3': {'message_typedef': {}, 'name': 'flags', 'type': 'message'}}, 'name': 'workspace_detail', 'type': 'message'},
            '2': {'message_typedef': {'1': {'name': 'seconds', 'type': 'int'}, '2': {'name': 'nanos', 'type': 'int'}}, 'name': 'created_at_copy', 'type': 'message'},
            '3': {'name': 'uuid1', 'type': 'bytes'},
            '6': {'name': 'uuid2', 'type': 'bytes'},
            '7': {'name': 'workspace_root', 'type': 'bytes'}
          }, 'name': 'details', 'type': 'message'},
    '22': {'name': 'extra_int', 'type': 'int'}
}

# A blank template to clone if the database is completely empty
BLANK_INNER_MSG = {
    '1': b'New Conversation',
    '2': 0,
    '3': {'1': 0, '2': 0},
    '4': b'',
    '5': 1,
    '7': {'1': 0, '2': 0},
    '9': {'1': b'file:///', '3': {}},
    '10': {'1': 0, '2': 0},
    '15': {},
    '16': 0,
    '17': {
        '1': {'1': b'file:///', '3': {}},
        '2': {'1': 0, '2': 0},
        '3': b'',
        '6': b'',
        '7': b'file:///'
    },
    '22': 4
}

def create_inner_msg(cid, title, created_ts, updated_ts, step_count=2, workspace_uri=b'file:///'):
    """Generates a fresh inner message dictionary for a given conversation."""
    msg = copy.deepcopy(BLANK_INNER_MSG)
    msg['1'] = title.encode('utf-8')[:100]
    msg['2'] = step_count
    msg['16'] = step_count
    msg['4'] = str(uuid.uuid4()).encode('utf-8')
    
    # Fill timestamps
    msg['3']['1'] = int(updated_ts)
    msg['7']['1'] = int(created_ts)
    msg['10']['1'] = int(updated_ts)
    msg['17']['2']['1'] = int(created_ts)
    
    msg['9']['1'] = workspace_uri
    msg['17']['1']['1'] = workspace_uri
    msg['17']['7'] = workspace_uri
    msg['17']['3'] = str(uuid.uuid4()).encode('utf-8')
    msg['17']['6'] = cid.encode('utf-8')
    return msg
