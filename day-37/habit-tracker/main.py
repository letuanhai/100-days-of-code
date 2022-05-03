import os
from datetime import datetime as dt, timedelta
import requests

USERNAME = "letuanhai"
API_URL = "https://pixe.la"
user_endpoint = "/v1/users"
graph_endpoint = f"{user_endpoint}/{USERNAME}/graphs"

headers = {"X-USER-TOKEN": os.environ["PIXELA_TOKEN"]}

graph_config = {
    "id": "test-graph",
    "name": "Running graph",
    "unit": "km",
    "type": "float",
    "color": "shibafu",
}

# pixel_creation_config = {
#     "date": "20220503",
#     "quantity": "20",
# }


# pixel_creation_endpoint = f"{graph_endpoint}/{graph_config['id']}"

# r = requests.post(
#     url=API_URL + pixel_creation_endpoint, json=pixel_creation_config, headers=headers
# )
# print(r.text)

# update_date = dt.today() - timedelta(days=1)
# pixel_update_endpoint = (
#     f"{graph_endpoint}/{graph_config['id']}/{update_date.strftime(r'%Y%m%d')}"
# )
# pixel_update_config = {
#     "quantity": "25",
# }

# r = requests.put(
#     url=API_URL + pixel_update_endpoint, json=pixel_update_config, headers=headers
# )
# print(r.text)

delete_date = dt.today() - timedelta(days=1)
pixel_delete_endpoint = (
    f"{graph_endpoint}/{graph_config['id']}/{delete_date.strftime(r'%Y%m%d')}"
)

r = requests.delete(url=API_URL + pixel_delete_endpoint, headers=headers)
print(r.text)
