# Copyright 2021 Google Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


# [START retail_create_product]
# Create product in a catalog using Retail API
#
import os
import random
import string

from google.api_core.client_options import ClientOptions
from google.cloud.retail import CreateProductRequest, Product, ProductServiceClient
from google.cloud.retail_v2 import PriceInfo
from google.cloud.retail_v2.types import product

from setup_product.setup_cleanup import delete_product

project_id = os.getenv("GOOGLE_CLOUD_PROJECT")
default_branch_name = (
    "projects/"
    + project_id
    + "/locations/global/catalogs/default_catalog/branches/default_branch"
)
endpoint = "retail.googleapis.com"
generated_product_id = "".join(random.sample(string.ascii_lowercase, 8))


# get product service client
def get_product_service_client():
    client_options = ClientOptions(endpoint)
    return ProductServiceClient(client_options=client_options)


# generate product to create
def generate_product() -> Product:
    price_info = PriceInfo()
    price_info.price = 30.0
    price_info.original_price = 35.5
    price_info.currency_code = "USD"
    return product.Product(
        title="Nest Mini",
        type_=product.Product.Type.PRIMARY,
        categories=["Speakers and displays"],
        brands=["Google"],
        price_info=price_info,
        availability="IN_STOCK",
    )


# get create product request
def get_create_product_request(product_to_create: Product, product_id: str) -> object:
    create_product_request = CreateProductRequest()
    create_product_request.product = product_to_create
    create_product_request.product_id = product_id
    create_product_request.parent = default_branch_name

    print("---create product request---")
    print(create_product_request)

    return create_product_request


# call the Retail API to create product
def create_product(product_id: str):
    create_product_request = get_create_product_request(generate_product(), product_id)
    product_created = get_product_service_client().create_product(
        create_product_request
    )

    print("---created product:---")
    print(product_created)
    return product_created


# create a product
created_product = create_product(generated_product_id)
# delete created product
delete_product(created_product.name)
# [END retail_create_product]
