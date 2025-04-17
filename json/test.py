import json
import xml.etree.ElementTree as ET
from xml.dom import minidom

# 协议配置
def load_protocol_config(config_path='protocol_config.json'):
    """从JSON文件加载协议配置"""
    with open(config_path, 'r') as f:
        return json.load(f)

def process_nested_data(parent_block, current_layer, data):
    """支持不进行进制转换的递归处理"""
    for full_key, value in data.items():
        # 统一替换所有点号为下划线
        field_name = full_key.replace('.', '_')
        key_parts = full_key.split('.')
        
        # 删除原有点号替换逻辑，直接使用替换后的字段名
        # field_name = '.'.join(key_parts[1:]) if (len(key_parts) > 1 and key_parts[0] == current_layer) else full_key

        if isinstance(value, dict):
            sub_block = ET.SubElement(parent_block, 'Block', {'name': field_name})
            process_nested_data(sub_block, field_name, value)
        else:
            processed_value = str(value)
            ET.SubElement(
                parent_block, 'String',
                {'name': field_name, 'value': processed_value}
            )


def create_state_model(root, protocol, data_model_names, protocol_config):
    """创建状态模型模块"""
    config = protocol_config.get(protocol, {})
    state_model = ET.SubElement(root, 'StateModel', {
        'name': f'StateModel_{protocol.capitalize()}',
        'initialState': 'Initial'
    })

    state = ET.SubElement(state_model, 'State', {'name': 'Initial'})

    action = ET.SubElement(state, 'Action', {'type': 'output'})
    for data_model_name in data_model_names:
        action.append(
            ET.Element('DataModel', {'ref': data_model_name})
        )

    return state_model

def create_agent(root, protocol, protocol_config):
    """创建代理模块"""
    config = protocol_config.get(protocol, {})
    agent = ET.SubElement(root, 'Agent', {'name': f'Agent_{protocol.capitalize()}'})

    # 调试监控器
    monitor = ET.SubElement(agent, 'Monitor', {'class': 'Process'})
    # 网络配置
    ET.SubElement(monitor, 'Param', {'name': 'port', 'value': str(config['default_port'])})
    ET.SubElement(monitor, 'Param', {'name': 'Executable', 'value': ''})
    ET.SubElement(monitor, 'Param', {'name': 'Arguments', 'value': ''})
    ET.SubElement(monitor, 'Param', {'name': 'RestartOnEachTest', 'value': 'false'})
    ET.SubElement(monitor, 'Param', {'name': 'Faultonearlyexit', 'value': 'true'})

    return agent

def create_test(root, protocol, data_model_names, protocol_config):
    """创建测试模块"""
    config = protocol_config.get(protocol, {})
    test = ET.SubElement(root, 'Test', {'name': f'Default'})
    # 基础配置
    # ET.SubElement(test, 'Agent', {'ref': f'Agent_{protocol.capitalize()}'})
    ET.SubElement(test, 'StateModel', {'ref': f'StateModel_{protocol.capitalize()}'})

    # 发布器配置（大写）
    publisher = ET.SubElement(test, 'Publisher', {'class': config['agent_class'], 'name': 'client'})
    ET.SubElement(publisher, 'Param', {'name': 'Host', 'value': '127.0.0.1'})
    ET.SubElement(publisher, 'Param', {'name': 'Port', 'value': str(config['default_port'])})
    # 变异策略
    # ET.SubElement(test, 'Agent', {'class': 'RandomDeterministic'})
    # 日志配置
    Logger = ET.SubElement(test, 'Logger', {'class': 'File'})
    ET.SubElement(Logger, 'Param', {'name': 'Path', 'value': 'LogsWorker'})
    return test

def convert_json_to_pit(input_json, output_pit, protocol, config_path='protocol_config.json'):
    """带协议配置的增强转换函数"""
    protocol_config = load_protocol_config(config_path)

    root = ET.Element('Peach')
    data_models = []

    for idx, message in enumerate(input_json):
        dm_name = f'DataModel_{protocol}_{idx}'
        data_model = ET.SubElement(root, 'DataModel', {'name': dm_name})
        data_models.append(dm_name)

        for layer, content in message['_source']['layers'].items():
            if isinstance(content, dict):
                block = ET.SubElement(data_model, 'Block', {'name': layer})
                process_nested_data(block, layer, content)

    if data_models:
        create_state_model(root, protocol, data_models, protocol_config)
        create_agent(root, protocol, protocol_config)
        create_test(root, protocol, data_models, protocol_config)

    # 生成美化后的XML
    xml_str = minidom.parseString(ET.tostring(root)).toprettyxml(indent='  ')
    with open(output_pit, 'w', encoding='utf-8') as f:
        f.write(xml_str)
# #modbus
# if __name__ == "__main__":
#     # 加载配置并转换
#     with open('/root/shared/json/modbus_output.json', 'r') as f:
#         convert_json_to_pit(
#             json.load(f),
#             '/root/shared/pit_coding/modbus_pit1.xml',
#             'modbus',
#             config_path='/root/shared/json/config/pro_config.json'
#         )
    
# # mqtt
# if __name__ == "__main__":
#     # 加载配置并转换
#     with open('/root/shared/json/mqtt.json', 'r') as f:
#         convert_json_to_pit(
#             json.load(f),
#             '/root/shared/pit_coding/mqtt_pit1.xml',
#             'mqtt',
#             config_path='/root/shared/json/config/pro_config.json'
#         )

# #opcua
# if __name__ == "__main__":
#     # 加载配置并转换
#     with open('/root/shared/json/opcua.json', 'r') as f:
#         convert_json_to_pit(
#             json.load(f),
#             '/root/shared/pit_coding/opcua_pit1.xml',
#             'opcua',
#             config_path='/root/shared/json/config/pro_config.json'
#         )

#ethernet
# if __name__ == "__main__":
#     # 加载配置并转换
#     with open('/root/shared/json/EthernetIP-CIP.json', 'r') as f:
#         convert_json_to_pit(
#             json.load(f),
#             '/root/shared/pit_coding/ethernet.xml',
#             'ethernet',
#             config_path='/root/shared/json/config/pro_config.json'
#         )
#

#bacnet
if __name__ == "__main__":
    # 加载配置并转换
    with open('/root/shared/json/BACnet.json', 'r') as f:
        convert_json_to_pit(
            json.load(f),
            '/root/shared/pit_coding/bacnet.xml',
            'bacnet',
            config_path='/root/shared/json/config/pro_config.json'
        )        