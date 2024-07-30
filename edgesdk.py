import datetime
import time

# 導入 WISE-PaaS 相關庫
from wisepaasdatahubedgesdk.EdgeAgent import EdgeAgent
import wisepaasdatahubedgesdk.Common.Constants as constant
from wisepaasdatahubedgesdk.Model.Edge import EdgeAgentOptions, DCCSOptions, EdgeData, EdgeTag, EdgeStatus, \
    EdgeDeviceStatus, EdgeConfig, NodeConfig, DeviceConfig, AnalogTagConfig, DiscreteTagConfig, TextTagConfig


class EdgeDevice():
    def __init__(self):
        self._edgeAgent = None  # EdgeAgent 實例
        self.timer = None  # 定時器
        self.status = 'Disconnected'  # 連接狀態
        self.node_id = ''  # 節點 ID
        self.dccs_options = {}  # DCCS 選項
        # self.device_name = device_name

    def start(self):
        # 啟動應用程序
        id = "b304d384-7f02-4c65-bc25-0dd23243f31c"
        url = "https://api-dccs-ensaas.wise-paas.iotcenter.nycu.edu.tw/"
        key = "7179740cb057c11d5f0524679f9f59uw"
        self.connect(id, url, key)
        self.upload_config()


    def connect(self, id, url, key):
        try:
            self.node_id = id

            # 設置 EdgeAgent 選項
            edgeAgentOptions = EdgeAgentOptions(nodeId=self.node_id)
            edgeAgentOptions.connectType = constant.ConnectType['DCCS']
            self.dccs_options['apiUrl'] = url
            self.dccs_options['credentialKey'] = key
            dccsOptions = DCCSOptions(**self.dccs_options)
            edgeAgentOptions.DCCS = dccsOptions

            # 創建 EdgeAgent 實例
            if self._edgeAgent is None:
                self._edgeAgent = EdgeAgent(edgeAgentOptions)
                self._edgeAgent.on_connected = self.on_connected
                self._edgeAgent.on_disconnected = self.on_disconnected

            # 連接到 Edge Agent
            self._edgeAgent.connect()
        except ValueError as error:
            print(f"Warning: {str(error)}")

    def on_connected(self, edgeAgent, isConnected):
        # 連接成功回調
        if isConnected:
            self.status = 'Connected'
            print("Connected")

    def on_disconnected(self, edgeAgent, isDisconnected):
        # 斷開連接回調
        if isDisconnected:
            self.status = 'Disconnected'
            print("Disconnected")

    def on_message(self, edgeAgent, message):
        # 消息處理回調
        if message.type == constant.MessageType['ConfigAck']:
            response = f'Upload Config Result: {message.message.result}'
            print(response)
        elif message.type == constant.MessageType['WriteValue']:
            message = message.message

    def send_pos(self, pos):
        # 生成並發送數據
        data = EdgeData()
        x_tag = EdgeTag("Wi-Fi", "x", pos[0])
        y_tag = EdgeTag("Wi-Fi", "y", pos[1])
        data.tagList.append(x_tag)
        data.tagList.append(y_tag)
        data.timestamp = datetime.datetime.now()
        self._edgeAgent.sendData(data)

    def send_rssi(self, rssi):
        # 生成並發送數據
        data = EdgeData()
        for i, r in enumerate(rssi):
            tag = EdgeTag("Wi-Fi", "RSSI" + str(i), rssi[i])
            data.tagList.append(tag)
        data.timestamp = datetime.datetime.now()
        self._edgeAgent.sendData(data)

    def upload_config(self):
        # 上傳配置
        if self._edgeAgent is None or not self._edgeAgent.isConnected:
            print("Warning: edge not connected")
            return
        config = self.__generateConfig()
        self._edgeAgent.uploadConfig(action=constant.ActionType['Create'], edgeConfig=config)

    def __generateConfig(self):
        # 生成配置
        config = EdgeConfig()
        nodeConfig = NodeConfig(nodeType=constant.EdgeType['Gateway'])
        config.node = nodeConfig
        wifiDeviceConfig = DeviceConfig(
            id='Wi-Fi',
            name='Wi-Fi',
            description='smart cart Wi-Fi',
            deviceType='Wi-Fi Device',
            retentionPolicyName=''
        )
        # config x and y pos
        for n in ["x", "y"]:
            analog = AnalogTagConfig(
                name=n,
                description=n,
                readOnly=False,
                arraySize=0,
                spanHigh=1000,
                spanLow=0,
                engineerUnit='',
                integerDisplayFormat=4,
                fractionDisplayFormat=2
            )
            wifiDeviceConfig.analogTagList.append(analog)

        for j in range(4):
            analog = AnalogTagConfig(
                name='RSSI' + str(j),
                description='RSSI' + str(j),
                readOnly=False,
                arraySize=0,
                spanHigh=1000,
                spanLow=0,
                engineerUnit='',
                integerDisplayFormat=4,
                fractionDisplayFormat=2
            )
            wifiDeviceConfig.analogTagList.append(analog)
        config.node.deviceList.append(wifiDeviceConfig)
        return config
if __name__ == "__main__":
    app = EdgeDevice()
    app.start()
    while 1:
        app.send_pos((3,3))