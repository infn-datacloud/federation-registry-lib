from glanceclient.client import Client as create_glance_client
from glanceclient.v2.client import Client as GlanceClient
from keystoneauth1.identity.v3 import OidcAccessToken
from keystoneauth1.session import Session
from keystoneclient.v3.client import Client as KeystoneClient
from novaclient.client import Client as create_nova_client
from novaclient.v2.client import Client as NovaClient

# subprocess.Popen(["oidc-token", "infncloud"],
# stdout=subprocess.PIPE, stderr=subprocess.PIPE)
# if subprocess.


auth = OidcAccessToken(
    auth_url="https://keystone.recas.ba.infn.it:443",
    identity_provider="infn-cloud",
    protocol="openid",
    access_token="",
    project_domain_name="default",
    project_name="infn-cloud",
)
sess = Session(auth=auth)
keystone = KeystoneClient(session=sess)

nova: NovaClient = create_nova_client(version="2", session=sess)
flavors = nova.flavors.list()
for flavor in flavors:
    print(flavor.to_dict())

glance: GlanceClient = create_glance_client(version="2", session=sess)
images = glance.images.list()
for image in images:
    print(image)
