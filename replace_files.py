import os
from shutil import copyfile

# Retrieve the path to the sila2lib module
try:
    import sila2lib
except ModuleNotFoundError as error:
    print("sila2lib does not appear to be installed or you are not in the correct virtual environment")
    raise

sila2lib_path = os.path.dirname(sila2lib.__file__)

hugo_repository_path= os.path.dirname(os.path.abspath(__file__))


# Copy the files
# sila_server.py
copyfile(hugo_repository_path + '/source/device_manager/sila_server.py', sila2lib_path + '/sila_server.py')
# sila_service_detection.py
copyfile(hugo_repository_path + '/source/device_manager/sila_service_detection.py', sila2lib_path + '/sila_service_detection.py')
# SiLAService_pb2_grpc.py
copyfile(hugo_repository_path + '/source/device_manager/SiLAService_pb2_grpc.py', sila2lib_path + '/framework/std_features/SiLAService_pb2_grpc.py')
# SiLAService_pb2.py
copyfile(hugo_repository_path + '/source/device_manager/SiLAService_pb2.py', sila2lib_path + '/framework/std_features/SiLAService_pb2.py')
# SiLAService.py
copyfile(hugo_repository_path + '/source/device_manager/SiLAService.py', sila2lib_path + '/framework/std_features/SiLAService.py')
# data_basic.py
copyfile(hugo_repository_path + '/source/device_manager/data_basic.py', sila2lib_path + '/proto_builder/data/data_basic.py')
# _dynamic_command.py
copyfile(hugo_repository_path + '/source/device_manager/_dynamic_command.py', sila2lib_path + '/proto_builder/_dynamic_command.py')
