import json
from tencentcloud.common import credential
from tencentcloud.common.profile.client_profile import ClientProfile
from tencentcloud.common.profile.http_profile import HttpProfile
from tencentcloud.common.exception.tencent_cloud_sdk_exception import TencentCloudSDKException
from tencentcloud.nlp.v20190408 import nlp_client, models

class NlpChat:
    def __init__(self):
        # 实例化一个认证对象，入参需要传入腾讯云账户secretId，secretKey,此处还需注意密钥对的保密
        # 密钥可前往https://console.cloud.tencent.com/cam/capi网站进行获取
        with open("nlp_account.txt","r",encoding="utf8") as f:
            account = f.readline().strip("\n")
            password = f.readline().strip("\n")
        self.cred = credential.Credential(account, password)
        # 实例化一个http选项，可选的，没有特殊需求可以跳过
        self.httpProfile = HttpProfile()
        self.httpProfile.endpoint = "nlp.tencentcloudapi.com"

        # 实例化一个client选项，可选的，没有特殊需求可以跳过
        self.clientProfile = ClientProfile()
        self.clientProfile.httpProfile = self.httpProfile
        # 实例化要请求产品的client对象,clientProfile是可选的
        self.client = nlp_client.NlpClient(self.cred, "ap-guangzhou", self.clientProfile)

    def get_response(self, msg) -> str:
        # 实例化一个请求对象,每个接口都会对应一个request对象
        req = models.ChatBotRequest()
        params = {
            "Flag": 0,
            "Query": str(msg)
        }
        req.from_json_string(json.dumps(params))

        # 返回的resp是一个ChatBotResponse的实例，与请求对象对应
        resp = self.client.ChatBot(req)

        # if resp.Confidence < 0.55:
            # response_str = "生成回复的置信度过低，牛牛不知道该说什么捏~"
        # else:
        response_str = resp.Reply
        return response_str
