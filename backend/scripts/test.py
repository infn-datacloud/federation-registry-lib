import openstack as opst

# import sys
#
# openstack.enable_logging(True, stream=sys.stdout)


conn = opst.connect(cloud="recas-ba")

flavors = []
flav_proj = {}
for flavor in conn.compute.flavors():
    if not flavor.is_public:
        projects = conn.compute.get_flavor_access(flavor)
        flav_proj[flavor.id] = projects
    data = flavor.to_dict()
    data["uuid"] = data.pop("id")
    flavors.append(data)

images = []
imag_proj = {}
for image in conn.image.images():
    is_public = True
    if image.visibility in ["private", "shared"]:
        imag_proj[image.id] = [image.owner_id]
        is_public = False
    if image.visibility == "shared":
        members = list(conn.image.members(image))
        for member in members:
            if member.status == "accepted":
                imag_proj[image.id].append(member.id)
    data = image.to_dict()
    data["uuid"] = data.pop("id")
    data["is_public"] = is_public
    data.pop("visibility")
    images.append(data)

provider = {}
provider["flavors"] = flavors
provider["images"] = images

# print(provider)
# cmdb_url = "http://localhost:8000"

# print(conn.identity.projects())
# for project in conn.identity.projects():
#   print(project)

# resp = requests.post(
#    url=os.path.join(cmdb_url, "api/v1/providers/"),
#    data=provider,
#    headers={
#        "Authorization": "Bearer"
#    },
# )
# if resp.status_code != 201:
#    raise  # TODO
# print(resp.json())
#
# for service in conn.service_catalog:
#   print(service)
# for service in conn.list_services():
#    print(service)

# for image in conn.image.images():
# print(image)
#    print(image.to_dict().keys())
#    for k,v in image.to_dict().items():
#        print(f"{k}: {v}")
# for project in conn.identity.projects():
#    print(project)
# for idp in conn.identity.identity_providers():
#    print(idp)
