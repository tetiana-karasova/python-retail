# Copyright 2022 Google Inc. All Rights Reserved.
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

import argparse
import os


def main(bucket_name):
    # [START retail_import_user_events_from_gcs]
    # Import user events into a catalog from GCS using Retail API

    import time

    from google.cloud.retail import (
        GcsSource,
        ImportErrorsConfig,
        ImportUserEventsRequest,
        UserEventInputConfig,
        UserEventServiceClient,
    )

    # Read the project number from the environment variable
    project_id = os.getenv("GOOGLE_CLOUD_PROJECT")

    # TODO: Developer set the bucket_name
    # bucket_name = os.environ["EVENTS_BUCKET_NAME"]

    default_catalog = "projects/{0}/locations/global/catalogs/default_catalog".format(
        project_id
    )

    # Read bucket name from the environment variable
    gcs_bucket = "gs://{}".format(os.getenv("EVENTS_BUCKET_NAME"))
    gcs_errors_bucket = "{}/error".format(gcs_bucket)
    gcs_events_object = "user_events.json"

    # TO CHECK ERROR HANDLING USE THE JSON WITH INVALID PRODUCT
    # gcs_events_object = "user_events_some_invalid.json"

    # get import user events from gcs request
    def get_import_events_gcs_request(gcs_object_name: str):
        # TO CHECK ERROR HANDLING PASTE THE INVALID CATALOG NAME HERE:
        # default_catalog = "invalid_catalog_name"
        gcs_source = GcsSource()
        gcs_source.input_uris = [f"{gcs_bucket}/{gcs_object_name}"]

        input_config = UserEventInputConfig()
        input_config.gcs_source = gcs_source

        errors_config = ImportErrorsConfig()
        errors_config.gcs_prefix = gcs_errors_bucket

        import_request = ImportUserEventsRequest()
        import_request.parent = default_catalog
        import_request.input_config = input_config
        import_request.errors_config = errors_config

        print("---import user events from google cloud source request---")
        print(import_request)

        return import_request

    # call the Retail API to import user events
    def import_user_events_from_gcs():
        import_gcs_request = get_import_events_gcs_request(gcs_events_object)
        gcs_operation = UserEventServiceClient().import_user_events(import_gcs_request)

        print("---the operation was started:----")
        print(gcs_operation.operation.name)

        while not gcs_operation.done():
            print("---please wait till operation is done---")
            time.sleep(30)

        print("---import user events operation is done---")

        if gcs_operation.metadata is not None:
            print("---number of successfully imported events---")
            print(gcs_operation.metadata.success_count)
            print("---number of failures during the importing---")
            print(gcs_operation.metadata.failure_count)
        else:
            print("---operation.metadata is empty---")

        if gcs_operation.result is not None:
            print("---operation result:---")
            print(gcs_operation.result())
        else:
            print("---operation.result is empty---")

    import_user_events_from_gcs()


# [END retail_import_user_events_from_gcs]

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "bucket_name", nargs="?", default=os.environ["EVENTS_BUCKET_NAME"]
    )
    args = parser.parse_args()
    main(args.bucket_name)
