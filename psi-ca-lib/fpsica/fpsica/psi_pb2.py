# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: proto/psi.proto
"""Generated protocol buffer code."""
from google.protobuf.internal import builder as _builder
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x0fproto/psi.proto\x12\tpsi_proto\"\x07\n\x05Setup\"%\n\x07Request\x12\x1a\n\x08\x65lements\x18\x01 \x03(\x0cR\x08\x65lements\"\xbe\x01\n\x08Response\x12\x32\n\x06masked\x18\x01 \x01(\x0b\x32\x1a.psi_proto.Response.MaskedR\x06masked\x12\x32\n\x06hashed\x18\x02 \x01(\x0b\x32\x1a.psi_proto.Response.HashedR\x06hashed\x1a$\n\x06Masked\x12\x1a\n\x08\x65lements\x18\x01 \x03(\x0cR\x08\x65lements\x1a$\n\x06Hashed\x12\x1a\n\x08\x65lements\x18\x01 \x03(\x0cR\x08\x65lements\"5\n\x06Result\x12+\n\x11intersection_size\x18\x01 \x01(\x05R\x10intersectionSizeb\x06proto3')

_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'proto.psi_pb2', globals())
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  _SETUP._serialized_start=30
  _SETUP._serialized_end=37
  _REQUEST._serialized_start=39
  _REQUEST._serialized_end=76
  _RESPONSE._serialized_start=79
  _RESPONSE._serialized_end=269
  _RESPONSE_MASKED._serialized_start=195
  _RESPONSE_MASKED._serialized_end=231
  _RESPONSE_HASHED._serialized_start=233
  _RESPONSE_HASHED._serialized_end=269
  _RESULT._serialized_start=271
  _RESULT._serialized_end=324
# @@protoc_insertion_point(module_scope)
