from urllib.parse import urlencode
from urllib.request import urlopen

class DlgEvaluator:
    response = None
    params = {}
    req_str = None

#
    # dtiad08dma23p
    def __init__(self, endpoint='http://dtiad04dma07p.dc.dotomi.net:7070/dma_evaluatedlg.do'):
        self.endpoint = endpoint
        self.set_params(level=0,type='ULM_ecpm',submit='Test')

    def evaluate(self):
        body = ""
        for k, v in self.params.items():
            body += k + "=" + str(v) + "&"
        self.req_str = self.endpoint + '?' + body
        body = body.encode('ascii')
        response = urlopen(self.endpoint, body)
        self.response = response

    def get_code(self):
        return self.response.getcode()

    def get_data(self):
        return self.response.read()

    def get_req_str(self):
        return self.req_str

    def set_params(self, *initial_data, **kwargs):
        for dictionary in initial_data:
            for key in dictionary:
                self.params[key] = dictionary[key]
        for key in kwargs:
            self.params[key] = kwargs[key]

    """
        -- dtmid
        -- companyId
        -- msgCampaignId
        -- isTest
        -- bucketId
        -- base_ecpm
        -- cpm_decay
        -- non_cpm_decay
        -- model_score
        -- userAgent
        -- network_id
        -- seller_id
        -- site_id
        -- request_type_id
        -- supply_type_id
        -- ad_position
        -- media_size

        curl -X POST http://dtiad08dma23p.dc.dotomi.net:7070/dma_evaluatedlg.do
            -d type=ULM_ecpm
            -d submit=Test
            -d level=0
            -d dtmid=472303794465140040
            -d companyId=2997
            -d msgCampaignId=23254
            -d @formula_encoded.txt


    // API
    fun modelScore : Real ,
        viewability : {performance : Real} = viewability.performance

    """