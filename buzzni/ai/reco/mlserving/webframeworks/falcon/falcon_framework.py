import falcon
from falcon_elastic_apm import ElasticApmMiddleware

from .error_handler import error_handler
from .health_resource import HealthResource
from .inference_resource import InferenceResource
from .. import WebFramework


class FalconFramework(WebFramework):

    def __init__(self, service_name):
        self._app = falcon.API(middleware=[
            ElasticApmMiddleware(
                service_name=service_name,
                server_url='http://apm-server.hsmoaworks.com'
            )
        ])

    @property
    def app(self):
        return self._app

    def add_inference_handler(self, rule, predictor, **kwargs):
        self.app.add_route(uri_template=rule,
                           resource=InferenceResource(predictor))

    def add_health_handler(self, rule, health_handler, **kwargs):
        self.app.add_route(uri_template=rule,
                           resource=HealthResource(health_handler))

    def set_error_handler(self, handler):
        falcon_handler = error_handler(handler)
        self.app.add_error_handler(Exception, falcon_handler)
