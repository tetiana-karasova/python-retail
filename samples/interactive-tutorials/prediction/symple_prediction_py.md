<walkthrough-metadata>
  <meta name="title" content="Getting The Recommendations. Prediction Service" />
  <meta name="description" content="Prediction service features" />
  <meta name="component_id" content="593554" />
  <meta name="short_id" content="true" />
</walkthrough-metadata>

# Getting the recommendations. Prediction service features

## Introduction

This is the third part of the complex Getting the Recommendation tutorial.

To request predictions from Recommendations AI, you need a trained and tuned recommendation model and one or more active serving configurations.

//TODO - add the linc to the tutorial
To learn how to prepare the data in a Retail catalog and to ingest the historical user events, go through the tutorial <...>

To create and train a recommendation model, proceed with the video tutorial: <...>

The detailed information about the recommendation service could be found in the [Retail API documentation](https://cloud.google.com/retail/docs/predict#recommendations-predict-java).

<walkthrough-tutorial-duration duration="10"></walkthrough-tutorial-duration>

<<_shared/_set_up_env_python.md>>

## Prediction service. Simple request

1. The `PredictRequest` request has the following fields:
    - `placement`—the ID of the Recommendations AI placement. Before you can request predictions from your model, you must create at least one placement for it.
    - `user_event`-the context about the user like what they are looking at or what action they took to trigger the predict request.
    - `page_size`—a maximum number of results to return per page. If set to zero, the service will choose a reasonable default. The maximum allowed value is 100.
    - `page_token`—the previous `PredictResponse.next_page_token`.
    - `filter`—a filter that restricts prediction results to a length limit of 5,000 characters. The filter can be applied to the `tags` field, or the `filterOutOfStockItems` flag can be used.
    - `params`—additional domain-specific parameters for the predictions.
    - `labels`—the labels applied to a resource. You can find more information about the labels in the [documentation](https://cloud.google.com/resource-manager/docs/creating-managing-labels#requirements).
   
//TODO check the file path
1. Open the <walkthrough-editor-select-regex filePath="cloudshell_open/python-retail/samples/interactive-tutorials/prediction/get_prediction.py" regex="# get prodciction request">prediction/get_prediction.py</walkthrough-editor-select-regex> file and check the `PredictRequest` request.
Here is an example of a simple prediction request with only the required fields set.
   
To send this PredictRequest to the Retail API, run the following code sample:

    ```bash
    python predict/get_prediction.py
    ```

1. Check the response in the Terminal. The PredictionResult consists of the following fields:
   -`results[]`-list of recommended products ordered by relevance from the most to the least relevant product.
   -`attribution_token`-a unique attribution token that is used for tracking the recommendation model performance.
   -`missing_ids[]`-IDs of products in the request that are missing from the inventory.
   
## Return products or scores

You can control what the response contains: either product objects or the products scores only. There are two parameters in the `PredictionRequest` to define it:
    -`returnProduct`-If set to True, the associated product object will be returned in the `results.metadata` field in the prediction response.
    -`returnScore`-If set to True, the prediction 'score' corresponding to each returned product will be set in the `results.metadata` field in the prediction response. 
                    The score indicates the probability that a user will click on/purchase a product, given the user's context and history.

Set the `returnScore` parameter, run the same code sample again and check the response:
    ```python
    params.returnScore = True
    ```
Now, the response contains only the probability score:

//TODO add the example of a response

Next, add the `returnProduct` parameter to the `ProdictRequest`:
    ```python
    params.returnProduct = True
    ```
Run the same code sample and check the returned product objects.
    ```bash
    python predict/get_prediction.py
    ```
## Error handling

The following fields are required in a `PredictRequest`:
    -`placement`
    -`user_event`

If any of these fields is set with an invalid value, the error message is expected. 
To request the Prediction service with a non-existent serving config as a placement, change the following field in the request in the code sample:
    ```python
    placement=f"projects/{project_id}/locations/global/catalogs/default_catalog/placements/nonexistent"
    ```
Run the code sample and check the error message:

//TODO - add the error message

The service also returns an error when the user event in the request is invalid.
Revert the latest changes you have made and remove the `user_event.product_details.prodcut` field.

Run the code sample again and check the error message.

//TODO - add the error message

## Congratulations

<walkthrough-conclusion-trophy></walkthrough-conclusion-trophy>

You have completed the tutorial! We encourage you to experiment with getting predictions by yourself.

<walkthrough-inline-feedback></walkthrough-inline-feedback>

### Do more with the Retail Recommendations
//TODO add the tutorials
<walkthrough-tutorial-card tutorialid="retail__retail_api_v2_<...>" icon="LOGO_PYTHON" title="<...>" keepPrevious=true>
<...></walkthrough-tutorial-card>
