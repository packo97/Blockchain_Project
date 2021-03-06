# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: Transaction.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor.FileDescriptor(
  name='Transaction.proto',
  package='',
  syntax='proto3',
  serialized_options=None,
  create_key=_descriptor._internal_create_key,
  serialized_pb=b'\n\x11Transaction.proto\"c\n\x12TransactionRequest\x12\x0c\n\x04time\x18\x01 \x01(\t\x12\x0f\n\x07\x61\x64\x64ress\x18\x02 \x01(\t\x12\r\n\x05\x65vent\x18\x03 \x01(\t\x12\x0c\n\x04vote\x18\x04 \x01(\t\x12\x11\n\tbroadcast\x18\x05 \x01(\x08\"$\n\x13TransactionResponse\x12\r\n\x05valid\x18\x01 \x01(\x08\x32K\n\x0bTransaction\x12<\n\x0fsendTransaction\x12\x13.TransactionRequest\x1a\x14.TransactionResponseb\x06proto3'
)




_TRANSACTIONREQUEST = _descriptor.Descriptor(
  name='TransactionRequest',
  full_name='TransactionRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='time', full_name='TransactionRequest.time', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='address', full_name='TransactionRequest.address', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='event', full_name='TransactionRequest.event', index=2,
      number=3, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='vote', full_name='TransactionRequest.vote', index=3,
      number=4, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='broadcast', full_name='TransactionRequest.broadcast', index=4,
      number=5, type=8, cpp_type=7, label=1,
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
  serialized_start=21,
  serialized_end=120,
)


_TRANSACTIONRESPONSE = _descriptor.Descriptor(
  name='TransactionResponse',
  full_name='TransactionResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='valid', full_name='TransactionResponse.valid', index=0,
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
  serialized_start=122,
  serialized_end=158,
)

DESCRIPTOR.message_types_by_name['TransactionRequest'] = _TRANSACTIONREQUEST
DESCRIPTOR.message_types_by_name['TransactionResponse'] = _TRANSACTIONRESPONSE
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

TransactionRequest = _reflection.GeneratedProtocolMessageType('TransactionRequest', (_message.Message,), {
  'DESCRIPTOR' : _TRANSACTIONREQUEST,
  '__module__' : 'Transaction_pb2'
  # @@protoc_insertion_point(class_scope:TransactionRequest)
  })
_sym_db.RegisterMessage(TransactionRequest)

TransactionResponse = _reflection.GeneratedProtocolMessageType('TransactionResponse', (_message.Message,), {
  'DESCRIPTOR' : _TRANSACTIONRESPONSE,
  '__module__' : 'Transaction_pb2'
  # @@protoc_insertion_point(class_scope:TransactionResponse)
  })
_sym_db.RegisterMessage(TransactionResponse)



_TRANSACTION = _descriptor.ServiceDescriptor(
  name='Transaction',
  full_name='Transaction',
  file=DESCRIPTOR,
  index=0,
  serialized_options=None,
  create_key=_descriptor._internal_create_key,
  serialized_start=160,
  serialized_end=235,
  methods=[
  _descriptor.MethodDescriptor(
    name='sendTransaction',
    full_name='Transaction.sendTransaction',
    index=0,
    containing_service=None,
    input_type=_TRANSACTIONREQUEST,
    output_type=_TRANSACTIONRESPONSE,
    serialized_options=None,
    create_key=_descriptor._internal_create_key,
  ),
])
_sym_db.RegisterServiceDescriptor(_TRANSACTION)

DESCRIPTOR.services_by_name['Transaction'] = _TRANSACTION

# @@protoc_insertion_point(module_scope)
