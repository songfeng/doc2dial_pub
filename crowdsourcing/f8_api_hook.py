import requests
import json
import os.path
from pathlib import Path
dir_path = os.path.dirname(os.path.realpath(__file__))
API_KEY = open(Path.home() / 'work' / 'data' / 'figure-eight' / 'api_key.txt').read()
API_URL = 'https://api.figure-eight.com/v1/'
job_id = "XXX"  # chat data agent
task = 'XXX'
FN_CML = os.path.join(dir_path, 'templates/f8_task.{}.cml'.format(task))
FN_INS = os.path.join(dir_path, 'templates/f8_instruction.{}.html'.format(task))
CML = open(FN_CML).read()
INS =open(FN_INS).read()
# data_json = os.path.join(APP_DATA, 'cf/data.json')
# conn = crowdflower.Connection(api_key=API_KEY, cache='filesystem')


class F8_API_Hook(object):

    def __init__(self, job_id=None, api_url=API_URL, api_key=API_KEY):
        self.api_key = api_key
        self.api_url = api_url
        self.job_id = job_id
        self.headers = {'content-type': 'application/json'}
        self.job_url = ""
        if self.job_id:
            self.job_url = self.api_url + "jobs/{}/".format(self.job_id)

    def create_blank_job(self): # create
        request_url = API_URL + 'jobs.json?key={}'.format(self.api_key)
        res = requests.post(request_url)
        self.job_id = res.json()['id']
        return res

    def create_job(self, title, instructions=None, cml=None):
        request_url = self.api_url + "jobs.json?"
        headers = {'content-type': 'application/json'}
        payload = {
            'key': self.api_key,
            'job': {
                'title': title,
                'instructions': instructions,
                'cml': cml
            }
        }
        res = requests.post(request_url, data=json.dumps(payload), headers=headers)
        self.job_id = res.json()['id']
        self.job_url = self.api_url + "jobs/{}/".format(self.job_id)
        return res

    def upload_data(self, csv_file):
        request_url = "https://api.figure-eight.com/v1/jobs/{}/upload".format(self.job_id)
        headers = {'content-type': 'text/csv'}
        payload = { 'key': self.api_key }
        res = requests.put(request_url, data=csv_file, params=payload, headers=headers)
        return res

    def set_row_data(self, data_json): # add data rows to a job
        # request_url = self.job_url + "/upload.json?key={api_key}&force=true".format(api_key=self.api_key)
        request_url = self.job_url + "/units.json"
        headers = {'content-type': 'application/json'}
        payload = {'key': self.api_key, 'unit': {'data': data_json}}
        res = requests.post(request_url, data=json.dumps(payload), headers=headers)
        return res

    def get_row_by_job(self):
        request_url = self.job_url + "/units.json?key={api_key}&page=1".format(api_key=self.api_key)
        res = requests.get(request_url)
        return res

    def launch(self, n=10, is_internal=True):
        if is_internal:
            channel_name = 'cf_internal'
        else:
            channel_name = 'on_demand'
        request_url = self.job_url + "/orders.json?key={api_key}".format(api_key=self.api_key)
        headers = {'content-type': 'application/json'}
        payload = {
            'channels': [channel_name],
            'debit': {
                'units_count': n
            }
        }
        res = requests.post(request_url, data=json.dumps(payload), headers=headers)
        return res

        # def cancel(self):
    #     self.conn.request('/jobs/%s/cancel' % self.job_id)

    def pause(self):
        request_url = self.job_url + "/pause.json?key={api_key}".format(api_key=self.api_key)
        res = requests.get(request_url)
        return res

    def resume(self):
        request_url = self.job_url + "/resume.json?key={api_key}".format(api_key=self.api_key)
        res = requests.get(request_url)
        return res

    def cancel(self):
        request_url = self.job_url + "/cancel.json?key={api_key}".format(api_key=self.api_key)
        res = requests.get(request_url)
        return res

    
    def ping(self):  # get the status
        request_url = self.job_url + "/ping.json?key={api_key}".format(api_key=self.api_key)
        res = requests.get(request_url)
        return res.json()

    def pay_bonus(self, job_id, worker_id, amount_in_cents):
        request_url = self.job_url + "/workers/{worker_id}/bonus.json?key={api_key}".format(worker_id=worker_id, api_key=self.api_key)
        headers = {'content-type': 'application/json'}
        payload = {
            'amount': amount_in_cents
        }
        res = requests.post(request_url, data=json.dumps(payload), headers=headers)
        return res

    def notify_worker(self, job_id, worker_id, message_to_worker):
        request_url = self.job_url + "/workers/{worker_id}/notify.json?key={api_key}".format(worker_id=worker_id, api_key=self.api_key)
        payload = {
            'message': message_to_worker
        }
        res = requests.post(request_url, data=json.dumps(payload))
        return res

    def flag_worker(self, job_id, worker_id, reason_for_flagging_contributor):
        request_url = self.job_url + "/workers/{worker_id}.json?key={api_key}".format(worker_id=worker_id, api_key=self.api_key)
        payload = {
            'flag': reason_for_flagging_contributor
        }
        res = requests.post(request_url, data=json.dumps(payload))
        return res

    def unflag_worker(self, job_id, worker_id, reason_for_flagging_contributor):
        request_url = self.job_url + "/workers/{worker_id}.json?key={api_key}".format(worker_id=worker_id, api_key=self.api_key)
        payload = {
            'unflag': reason_for_flagging_contributor
        }
        res = requests.post(request_url, data=json.dumps(payload))
        return res


    #     def get_job_by_id(self, job_id):
    #     for job in self.conn.jobs():
    #         if job_id == job.id:
    #             self.job = job
    #             return job

    # def find_job_tag(self, job_tag):
    #     for job in conn.jobs():
    #         if job_tag in job.tags:
    #             self.job = job
    #             return job

    
    # def add_data(self, data):
    #     self.job.upload(data)  # [{}, {}]



    # def results(self):
    #     job = _find_job()
    #     try:
    #         for judgment in job.judgments:
    #             print('\t'.join([judgment['label'], judgment['text']]))
    #     except(exc):
    #         # explain HTTP 202 Accepted response
    #         if exc.response.status_code == 202:
    #             print("Try again in a moment", file=sys.stderr)

    # def download(self):
    #     for judgment in job.judgments:
    #         print(json.dumps(judgment))


    # def request(self, path, method, params):
    #     res = self.conn.request('/jobs/%s/gold' % self.id, method='PUT', params=params)
    #     self.conn.request('/jobs/%s/units/%s' % (self.id, unit_id), method='DELETE')
    #     headers = {'Content-Type': 'application/json'}
    #     data = json.dumps({'unit': {'data': unit}})
    #     res = self.conn.request('/jobs/%s/units' % self.id, method='POST', headers=headers, data=data)

    # def set_bonus(self, amount_in_cents, job_id, worker_id):
    #     '''
    #     curl -X POST --data-urlencode "amount={amount_in_cents}" https://api.crowdflower.com/v1/jobs/{job_id}/workers/{worker_id}/bonus.json?key={api_key}
    #     '''
    #     # data = rails_params(dict(channels=channels, debit=dict(units_count=units_count)))
    #     data = rails_params(dict(amount=amount_in_cents))
    #     res = self.conn.request('/jobs/%s/orders/workers/%s/bonus' % (job_id, worker_id), method='POST', params=data)
    #     # self._cache_flush('properties')
    #     return res

    #     '''
    #     curl -X POST -d "channels[0]=on_demand&debit[units_count]={100}" https://api.crowdflower.com/v1/jobs/{job_id}/orders.json?key={api_key}

    #     channels = list(channels)
    #     data = rails_params(dict(channels=channels, debit=dict(units_count=units_count)))
    #     res = self._connection.request('/jobs/%s/orders' % self.id, method='POST', params=data)
    #     self._cache_flush('properties')
    #     '''


if __name__ == '__main__':
    csv_file = os.path.join(dir_path, 'data/f8_task_data.{}.csv'.format(task))
    csv_data = open(csv_file, 'rb')
    f = F8_API_Hook()
    res = f.create_job('api created job', INS, CML)
    print(res.json()['id'])
    # f = F8_API_Hook(job_id=1394425)
    # print(res.json())
    # task_url = "http://173.193.75.126:31880/login?task=label_sentence&task_ids=task1;;task2;;task3"
    # data_json = {"task_url": task_url, "total": 10, "task": "label_sentence", 'confirmation_code': 'test'}
    # res = f.cancel()
    # print(res)
    # print(res.json())
    # res = f.upload_data(csv_data)
    # res = f.create_job('test job 1 2 3', INS, CML)
    # print(res.json()['id'])
    # print(f.job_id)
    # res = f.set_row_data(data_json)
    # res = f.get_row_by_job()
    # print(res.json())
    # res = cf.launch_internal_channel()
    # print(res.json())
    # curl -X GET "https://api.crowdflower.com/v1/jobs/1187345/units.json?key=EryJhbCbXnzucFZGo4ih&page=1"
