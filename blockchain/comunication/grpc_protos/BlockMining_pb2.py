# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: BlockMining.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor.FileDescriptor(
  name='BlockMining.proto',
  package='',
  syntax='proto3',
  serialized_options=None,
  create_key=_descriptor._internal_create_key,
  serialized_pb=b'\n\x11\x42lockMining.proto\"\xa9\x01\n\x12\x42lockMiningRequest\x12\x0c\n\x04time\x18\x01 \x01(\t\x12\x0c\n\x04seed\x18\x02 \x01(\x05\x12\x19\n\x11transactions_list\x18\x03 \x01(\t\x12\x19\n\x11transactions_hash\x18\x04 \x01(\t\x12\x12\n\nblock_hash\x18\x05 \x01(\t\x12\x16\n\x0elottery_number\x18\x06 \x01(\x05\x12\x15\n\rminer_address\x18\x07 \x01(\t\"$\n\x13\x42lockMiningResponse\x12\r\n\x05valid\x18\x01 \x01(\x08\x32S\n\x0b\x42lockMining\x12\x44\n\x17sendVictoryNotification\x12\x13.BlockMiningRequest\x1a\x14.BlockMiningResponseb\x06proto3'
)




_BLOCKMININGREQUEST = _descriptor.Descriptor(
  name='BlockMiningRequest',
  full_name='BlockMiningRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='time', full_name='BlockMiningRequest.time', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='seed', full_name='BlockMiningRequest.seed', index=1,
      number=2, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='transactions_list', full_name='BlockMiningRequest.transactions_list', index=2,
      number=3, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='transactions_hash', full_name='BlockMiningRequest.transactions_hash', index=3,
      number=4, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='block_hash', full_name='BlockMiningRequest.block_hash', index=4,
      number=5, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='lottery_number', full_name='BlockMiningRequest.lottery_number', index=5,
      number=6, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='miner_address', full_name='BlockMiningRequest.miner_address', index=6,
      number=7, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=22,
  serialized_end=191,
)


_BLOCKMININGRESPONSE = _descriptor.Descriptor(
  name='BlockMiningResponse',
  full_name='BlockMiningResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='valid', full_name='BlockMiningResponse.valid', index=0,
      number=1, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=193,
  serialized_end=229,
)

DESCRIPTOR.message_types_by_name['BlockMiningRequest'] = _BLOCKMININGREQUEST
DESCRIPTOR.message_types_by_name['BlockMiningResponse'] = _BLOCKMININGRESPONSE
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

BlockMiningRequest = _reflection.GeneratedProtocolMessageType('BlockMiningRequest', (_message.Message,), {
  'DESCRIPTOR' : _BLOCKMININGREQUEST,
  '__module__' : 'BlockMining_pb2'
  # @@protoc_insertion_point(class_scope:BlockMiningRequest)
  })
_sym_db.RegisterMessage(BlockMiningRequest)

BlockMiningResponse = _reflection.GeneratedProtocolMessageType('BlockMiningResponse', (_message.Message,), {
  'DESCRIPTOR' : _BLOCKMININGRESPONSE,
  '__module__' : 'BlockMining_pb2'
  # @@protoc_insertion_point(class_scope:BlockMiningResponse)
  })
_sym_db.RegisterMessage(BlockMiningResponse)



_BLOCKMINING = _descriptor.ServiceDescriptor(
  name='BlockMining',
  full_name='BlockMining',
  file=DESCRIPTOR,
  index=0,
  serialized_options=None,
  create_key=_descriptor._internal_create_key,
  serialized_start=231,
  serialized_end=314,
  methods=[
  _descriptor.MethodDescriptor(
    name='sendVictoryNotification',
    full_name='BlockMining.sendVictoryNotification',
    index=0,
    containing_service=None,
    input_type=_BLOCKMININGREQUEST,
    output_type=_BLOCKMININGRESPONSE,
    serialized_options=None,
    create_key=_descriptor._internal_create_key,
  ),
])
_sym_db.RegisterServiceDescriptor(_BLOCKMINING)

DESCRIPTOR.services_by_name['BlockMining'] = _BLOCKMINING

# @@protoc_insertion_point(module_scope)