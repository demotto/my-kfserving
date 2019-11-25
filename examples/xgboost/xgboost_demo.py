from kubernetes import client
from kfserving import KFServingClient
from kfserving import utils
from kfserving import constants

namespace = utils.get_default_target_namespace()

print(namespace)