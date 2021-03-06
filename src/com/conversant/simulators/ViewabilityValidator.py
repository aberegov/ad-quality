from com.conversant.simulators.AbstractViewabilitySimulator import AbstractViewabilitySimulator
from com.conversant.viewability.ViewabilityGldEvaluator import ViewabilityGldEvaluator
import time
from urllib.parse import quote_plus
import re

class ViewabilityValidator(AbstractViewabilitySimulator):
    def __init__(self, source='ad_quality.bids_view'):
        super().__init__(source)

    def extract_key(self, row):
        return row[0:-4]

    def process_row(self, row, view):
        eval = ViewabilityGldEvaluator()
        # ad_format_id,network_id,seller_id,site_id,media_size,ad_position,device,os,browser_name,browser_version
        eval.set_params({
            'companyId': int(row[-4]),
            'msgCampaignId': int(row[-3]),
            'userAgent': quote_plus(row[-2]),
            'dtmid': row[-1],
            'request_type_id': int(row[0]) >> 4,
            'supply_type_id': int(row[0]) & 0xf,
            'network_id': int(row[1]),
            'media_size': int(row[4]),
            'ad_position': int(row[5])
        })

        if row[2] != '(null)':
            eval.set_params(seller_id = quote_plus(row[2]))

        if row[3] != '(null)':
            eval.set_params(site_id = quote_plus(row[3]))

        eval.evaluate()
        dlg = eval.get_data().decode("utf-8")
        r = 0
        m = re.search('<result>\[(.+?)\]</result>', dlg)
        if m:
            dlg = m.group(1)
            r = 1 if int(float(dlg) * 1000) == int(view * 1000) else 0

        self.append(list(row[0:-4]) + [view, dlg, r, row[-2], eval.get_req_str()])
        time.sleep(0.1)


if __name__ == '__main__':
    validator = ViewabilityValidator()
    validator.execute("SELECT {0}, company_id, campaign_id, user_agent, dtm_id FROM {1} WHERE dtm_id is not NULL", 10000)
    validator.output(['predictor', 'from dlg', 'match', 'user agent', 'dlg call'])
