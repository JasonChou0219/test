from source.device_manager.device_layer.dynamic_client import DynamicSiLA2Client
from source.device_manager.sila_auto_discovery import sila_auto_discovery

if __name__ == "__main__":
    servers = sila_auto_discovery.find()

    for server in servers:
        print('Server: {server_uuid};{server_name};{server_ip}:{server_port}'.
              format(server_uuid=server.uuid,
                     server_name=server.name,
                     server_ip=server.ip,
                     server_port=server.port))
        client = DynamicSiLA2Client(name="DynamicClient",
                                    server_ip=server.ip,
                                    server_port=server.port)
        client.run()

        print('Available commands and properties for this server:')
        for feature in client.list_features():
            print('Feature: {feature_id}'.format(feature_id=feature))
            print('  Commands:'.format(feature_id=feature))
            commands = client.list_commands(feature_id=feature)
            for command in commands:
                print('    {command_id}: ({types_in}) -> ({types_out})'.format(
                    command_id=command.identifier,
                    # types_in=", ".join(command.input_data_path),
                    types_in=", ".join(command.input_data_type),
                    # types_out=", ".join(command.output_data_path)
                    types_out=", ".join(command.output_data_type)))
            print('  Properties:'.format(feature_id=feature))
            properties = client.list_properties(feature_id=feature)
            for property_element in properties:
                print('    {command_id}: () -> ({types_out})'.format(
                    command_id=property_element.identifier,
                    # types_out=", ".join(property_element.output_data_path)
                    types_out=", ".join(property_element.output_data_type)))
