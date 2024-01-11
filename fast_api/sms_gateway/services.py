import hashlib
import logging
import os
import requests

from fastapi.templating import Jinja2Templates

templates = Jinja2Templates(directory="templates")

logging.config.fileConfig('logging.conf', disable_existing_loggers=False)
logger = logging.getLogger(__name__)

MASK_START = 3
MASK_END = 4
YIROAMING_API_SEND_MESSAGE = 'http/submitSms'

class CoreService:
    def __init__(self, request):
        self.session = requests.Session()
        self.request = request

    def ___mask_number(self, phone_number) -> str:
        if len(phone_number) < (MASK_START + MASK_END):
            return phone_number
        return phone_number[:+MASK_START].ljust(len(phone_number) - MASK_END, '*') + phone_number[-MASK_END:]

    def log_info(self, class_name, request, response):
        if 'phone_number' in request:
            request.update({'phone_number': self.___mask_number(request['phone_number'])})
        if 'resDetail' in response and 'phoneNumber' in response['resDetail']:
            response['resDetail'].update({'phoneNumber': self.___mask_number(response['resDetail']['phoneNumber'])})
        logger.info((class_name, request, response))

class CyoloService(CoreService):
    def __request(self, method, path, kwargs):
        headers  = { 'Authorization': self.request.headers['Authorization'] }
        response = self.session.request(method, f"{os.environ['CYOLO_ENDPOINT']}/{path}", json=kwargs, headers=headers)
        self.log_info(self.__class__, kwargs, response)
        if 200 <= response.status_code < 300:
            return response

    def send(self, kwargs):
        return self.__request(self.request.method, self.request.path_params.get('path_name'), kwargs)

class YroamingService(CoreService):
    def __build_params(self, kwargs):
        kwargs.update({
            'account' : os.environ['YIROAMING_ACCOUNT'],
            'password': hashlib.md5(os.environ['YIROAMING_PASSWORD'])
        })
        return kwargs

    def __request(self, method, path, kwargs):
        response = self.session.request(method, f"{os.environ['YIROAMING_ENDPOINT']}/{path}", json=self.__build_params(kwargs))
        self.log_info(self.__class__, kwargs, response)
        if 200 <= response.status_code < 300:
            return response

    def __convert_message(self, kwargs):
        if not kwargs.get('user_name'):
            return templates.get_template('sms_yiroming_mfa.html').render(kwargs)
        else:
            return templates.get_template('sms_yiroming_supervisor.html').render(kwargs)

    def send(self, kwargs):
        return self.__request('POST', YIROAMING_API_SEND_MESSAGE, { 'message': self.__convert_message(kwargs) })