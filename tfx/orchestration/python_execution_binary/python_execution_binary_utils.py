# Copyright 2020 Google LLC. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
r"""Shared IR serialization logic used by TFleX python executor binary."""

import base64

from tfx.orchestration import metadata
from tfx.orchestration.portable import data_types
from tfx.proto.orchestration import executable_spec_pb2
from tfx.proto.orchestration import executor_invocation_pb2


def deserialize_execution_info(
    execution_info_b64: str) -> data_types.ExecutionInfo:
  """De-serializes the ExecutionInfo class from a binary string."""
  execution_info_proto = executor_invocation_pb2.ExecutorInvocation.FromString(
      base64.b64decode(execution_info_b64))
  return data_types.ExecutionInfo.from_proto(execution_info_proto)


def deserialize_mlmd_connection_config(
    mlmd_connection_config_b64: str) -> metadata.ConnectionConfigType:
  """De-serializes an MLMD connection config from base64 flag."""
  mlmd_connection_config = (
      executor_invocation_pb2.MLMDConnectionConfig.FromString(
          base64.b64decode(mlmd_connection_config_b64)))
  return getattr(mlmd_connection_config,
                 mlmd_connection_config.WhichOneof('connection_config'))


def deserialize_executable_spec(
    executable_spec_b64: str) -> executable_spec_pb2.PythonClassExecutableSpec:
  """De-serializes an executable spec from base64 flag."""
  return executable_spec_pb2.PythonClassExecutableSpec.FromString(
      base64.b64decode(executable_spec_b64))


def serialize_mlmd_connection_config(
    connection_config: metadata.ConnectionConfigType) -> str:
  """Serializes an MLMD connection config into a base64 flag of its wrapper."""
  mlmd_wrapper = executor_invocation_pb2.MLMDConnectionConfig()
  for name, descriptor in (executor_invocation_pb2.MLMDConnectionConfig
                           .DESCRIPTOR.fields_by_name.items()):
    if descriptor.message_type.full_name == connection_config.DESCRIPTOR.full_name:
      getattr(mlmd_wrapper, name).CopyFrom(connection_config)
      break
  return base64.b64encode(mlmd_wrapper.SerializeToString()).decode('ascii')


def serialize_executable_spec(
    executable_spec: executable_spec_pb2.PythonClassExecutableSpec) -> str:
  """Serializes an executable spec into a base64 flag."""
  return base64.b64encode(executable_spec.SerializeToString()).decode('ascii')


def serialize_execution_info(execution_info: data_types.ExecutionInfo) -> str:
  """Serializes the ExecutionInfo class from a base64 flag."""
  execution_info_proto = execution_info.to_proto()
  return base64.b64encode(
      execution_info_proto.SerializeToString()).decode('ascii')
