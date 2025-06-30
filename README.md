# VICOMTECH PARSECGRAPH

This repository contains the needed modules to generate and deploy parsecgraph docker images, an opensource visualization tool for ANN model explainability <sup>[1](#1)</sup>.

## Overview

The aim of this tool is to provide a visual representation of the interpretability and explainability of an Artificial Neural Network model for image classification. The example provided in this repository is deep fake image classification, for which an example image and deepfake detection model are included.

The visualization divides the target artificial neural network (ANN) into blocks, which are groups of layers that are typically similar in function or structure. Each block can be selected for detailed inspection. Upon selecting a block, its internal layers are displayed in a graph format, where nodes represent the kernels in different layers. Each node is associated with two attributes—Impact and Influence—which are determined based on the input sample processed by the model.

The Impact attribute is represented by color, with a numerical value ranging from -1 to 1. In this example, the class is deep_fake, where values closer to -1 (strongly negative) indicate that the kernel tends to reduce considerably the internal value of the model, while values closer to 1 (strongly positive) indicate that the kernel increases considerably the internal value.

The Influence attribute is represented by the size of the node, with a value of either 0 or 1. A large node corresponds to a value of 1, indicating that the filter had an influence on the model's decision, while a small node (value 0) indicates no influence.

The image below displays the 15th block (highlighted in blue) of a model composed of 32 blocks. Each layer within the block is shown as a rectangular group of filters associated with the selected block.

![model by block](modelview-tagged.png?raw=true "model by block")

Besides the model interpretability feature, this visualization provides an explainability by filter feature with its own section, as shown below. A critical filter (the bigger circles) can be selected by clicking on it and the tool shows a heatmap of the pixels in the image where selected filter has focused to push final classification to one class or the other. In this example the pixels on the face image are marked if the selected filter has focused on them to weight the image towards legit or fake.

![explainability](explainability.png?raw=true "explainability")

## Basic use

This tool can be used in two modes that can be chosen by the user modifying the configuration file (see [bellow](#configuration)):
  1. Remote mode: The tool requests the model structure, the interpretability and explainability result to an external API.
  2. Local mode: The visualization is baked in the tool. The requests fetch the files included on the data folder (see structure [below](#folder-structure)).

When a user accesses the app they are shown one of the following screen, depending on the chosen mode

![Home Page Remote](homepage_remote.PNG?raw=true "Home Page Remote")

![Home Page Local](homepage_local.PNG?raw=true "Home Page Local")

The first image shows a remote set up, while the second is an example of a deployment with local data. As shown in the image, the main difference is the ability of the user to upload an image or pick one of the preloads. In both cases the selection of an image is made by clicking on it in found faces section, and once highlighted the user can acces the next step by clicking on "send to model" button.

From both access methods the model page is allways the following:

![Model exploration page](modelview-tagged.png?raw=true "Model exploration page")

The interaction with the page is by mouse, and different sections allow for different actions:

- The representation of the model is shown at the "Interpretability main section", and it allows for simple navigation such as panning with right mouse click and drag, zooming by mouse wheel scroll and selection of a critical filter by click.
- The block selection buttons allow to change the shown model block by clicking on one of the 'B*'.
- The layer activation and deactivation section allows bringing a layer to foreground or backgroun by clicking at any point in the layer area.
- The background display radio buttons allow the user to show or hide background by clicking on the non-higlighted one. The selection is shown by highlighting the chosen option.

## Tool Structure

This tool is comprised of three modules on the same network:

1) A postgresql database with the tables shown on the image bellow. This db provides a storage for the positions of the graph generated to visualize the model, and the structure of the model for navigation purposes.

![postgresql_tables](postgresql_tables.PNG?raw=true "postgresql_tables")

2) A python flask API communicating the visualization and the database, found in the folder parsecgraph-back-atlantis. In this documentation and for configuration purposes it's referenced as viz_api.
3) The visualization itself served through a nginx server and created from Vue framework found in the folder parsecgraph-front-atlantis.

## Folder Structure

```bash
vicomtech-evaxplainify # files to build module 2
├── README.md
├── docker-compose.yml
├── parsegraph-back-atlantis
│   ├── Dockerfile
│   ├── .env # environment variables for the flask API
│   ├── blueprints # api endpoints sorted by namespace
│   │   ├── __init__.py
│   │   └── endpoints
│   │       ├── __init__.py
│   │       ├── block_endpoints
│   │       │   └── __init__.py
│   │       ├── filter_endpoints
│   │       │   └── __init__.py
│   │       ├── image_endpoints
│   │       │   └── __init__.py
│   │       └── layer_endpoints
│   │           └── __init__.py
│   ├── db #sqlalchemy table models and database connection
│   │   ├── __init__.py
│   │   └── models
│   │       └── __init__.py
│   ├── entrypoint.py
│   └── requirements.txt
└── parsegraph-front-atlantis #  files to build module 3
    ├── Dockerfile
    ├── index.html
    ├── jsconfig.json
    ├── nginx
    │   └── nginx.conf # specific configuration for the visualization app server
    ├── package-lock.json
    ├── package.json
    ├── public
    │   ├── data # This directory holds the files to search when the app is set to local mode, and does not rely on external API
    │   │   ├── deepfakeModel.json # model structure file
    │   │   ├── images
    │   │   │   ├── explainability # directory of the explainability image results the name of each image correspond to the original image, the layer and the filter inside to which the image belongs to
    │   │   │   │   ├── face0_1_30.jpg
    │   │   │   │   ├── face0_36_11.jpg
    │   │   │   │   ├── face0_51_14.jpg
    │   │   │   │   └── face0_8_2.jpg
    │   │   │   └── original # directory of original images
    │   │   │       ├── face0.png
    │   │   │       ├── face1.png
    │   │   │       └── face2.png
    │   │   └── interpretability # interpretability results corresponding to the model output by block and image
    │   │       └── face0
    │   │           ├── block1.json
    │   │           ├── block10.json
    │   │           ├── block11.json
    │   │           ├── block12.json
    │   │           ├── block13.json
    │   │           ├── block14.json
    │   │           ├── block15.json
    │   │           ├── block16.json
    │   │           ├── block17.json
    │   │           ├── block18.json
    │   │           ├── block19.json
    │   │           ├── block2.json
    │   │           ├── block20.json
    │   │           ├── block21.json
    │   │           ├── block22.json
    │   │           ├── block23.json
    │   │           ├── block24.json
    │   │           ├── block25.json
    │   │           ├── block26.json
    │   │           ├── block27.json
    │   │           ├── block28.json
    │   │           ├── block29.json
    │   │           ├── block3.json
    │   │           ├── block30.json
    │   │           ├── block31.json
    │   │           ├── block32.json
    │   │           ├── block4.json
    │   │           ├── block5.json
    │   │           ├── block6.json
    │   │           ├── block7.json
    │   │           ├── block8.json
    │   │           └── block9.json
    │   ├── envconfig.json
    │   ├── favicon.ico
    │   └── placeholder
    │       └── placeholder-image.webp
    ├── resources # directory for the ssl certificates
    ├── src
    │   ├── App.vue
    │   ├── assets
    │   │   ├── base.css
    │   │   ├── icon-image-not-found-free-vector.jpg
    │   │   └── main.css
    │   ├── components
    │   │   ├── BlockSelectorComponent.vue
    │   │   ├── GraphComponent.vue
    │   │   ├── LegendComponent.vue
    │   │   ├── LoaderComponent.vue
    │   │   ├── MinimapComponent.vue
    │   │   └── OverlayComponent.vue
    │   ├── main.js
    │   ├── modules
    │   │   ├── APIservice.js
    │   │   ├── apimodule.js
    │   │   └── utils.js
    │   ├── router
    │   │   └── index.js
    │   ├── stores
    │   │   ├── manager.js
    │   │   └── networkStructure.js
    │   └── views
    │       ├── ImageSelectionView.vue
    │       └── ModelView.vue
    └── vite.config.js
```

## Configuration 

This app can run with locally stored data or Remote API (refered in this document as explainify API and in configuration as evapi). This API must provide the same template for model structure request as deepfakeModel.json, and as any of the blockN.json for the inblock request. For get faces and explainability request it must return  jpg images.

### Remote

In ./parsegraph-back-atlantis/.env change the variables accordingly to your host config
- DB_USER: the user of your database
- DB_PASSWORD: the password of your database
- DB_NAME: The name of your database
- DB_PORT: The port for your database where your host is listening
- DB_RESET: Wether the database should be rebuilt when initiating the API, posible values are True or False, default False
- DB_HOST: the url of the host of your database
- EVAPI_HOST: the url of the host of your explainify API 
- EVAPI_PORT: the port for your evaxplainify API where your host is listening 
- PGAPI_PORT: the url of the host of your Pgraph API

Make sure to add your certificates in ./parsegraph-front-atlantis/resources folder and modify the file ./parsegraph-front-atlantis/nginx/nginx.conf
lines 28 and 29 with the correct route to them in your container. Default /etc/ssl

In ./parsegraph-front-atlantis/nginx/nginx.conf locations for end point to APIs are tied to the name of the container on the same network, if containers change name or listening port adjust line 38 and 42 accordingly

In order to do so, the envconfig.json file located at ./parsegraph-front-atlantis/public must be adjusted. This file conforms to the following structure

```json
{
  "Envname": "<your_env>",
  "Mode": {
    "oneOf": [
      {
        "enum": [
          "LOCAL",
          "REMOTE"
        ],
        "type": "string"
      }
    ],
    "value": "REMOTE"
  },
  "endpoints": {
    "getBlockLayers": {
      "url": "viz_api/Layers/inblock",
      "method": "GET"
    },
    "getBlocknodes": {
      "url": "viz_api/Nodes",
      "method": "GET"
    },
    "getcrops": {
      "url": "evapi/get_faces/",
      "method": "POST"
    },
    "getInterpretabilitybyBlock": {
      "url": "evapi/interpretability_by_block/",
      "method": "GET"
    },
    "getExplainability": {
      "url": "evapi/explainability/",
      "method": "GET"
    },
    "getModel": {
      "url": "evapi/model_structure/",
      "method": "GET"
    }
  }
}
```
Make sure to change the field that contain '<' '>' with the appropriatte name for your environment and data. The endpoints of each available route are pointing to the endpoints stablished on the nginx.conf file and can be adjusted accordingly.

Finally in the docker compose file make sure the external ports match your needs for the host

The Explainability API must have these enpoints
  1) POST /get_faces/: enpoint to get the crops of faces in an image. The input body must follow this json:
      ```json
        {
          "file": "('image.jpg', io.BytesIO(byte_im), 'image/jpeg')"
        }
      ```
      And the output must follow the structure found in the file ./parsegraph-front-atlantis/public/data/deepfakeModel.json.

  2) GET /model_structure/: returns the model structure as JSON. Needed to load it to the database if the model is not already present.
  3) GET /interpretability_by_block/: Generates the result of impact and influence of the model by block. This call __requires__ 2 parameters: n_block indicating the block requested and face indicating the the number of the selected face. the output must follow the structure found in any of the files ./parsegraph-front-atlantis/public/data/interpretability/*face_image_name*/block\*.json.
  4) GET /explainability/: returns the image containing the heatmap of the pixels where the filter has focused on. This call __requires__ 3 parameters: layer indicating the layer of the node to be analyzed,  channel indicating the filter to be analyzed, and face indicating the the number of the selected face.

### Local

In ./parsegraph-back-atlantis/.env change the variables accordingly to your host config:
- DB_USER: the user of your database.
- DB_PASSWORD: the password of your database.
- DB_NAME: The name of your database.
- DB_PORT: The port for your database where your host is listening.
- DB_RESET: Wether the database should be rebuilt when initiating the API, posible values are True or False, default False.
- DB_HOST: the url of the host of your database.
- PGAPI_PORT: the url of the host of your Pgraph API.

Make shure to add your certificates in ./parsegraph-front-atlantis/resources folder and modify the file ./parsegraph-front-atlantis/nginx/nginx.conf
lines 28 and 29 with the correct route to them in your container. Default /etc/ssl.

In ./parsegraph-front-atlantis/nginx/nginx.conf locations for end points to the APIs are tied to the name of the container on the same network; if containers change name or listening port adjust line 38 and 42 accordingly.

In order to do so, the envconfig.json file located at ./parsegraph-front-atlantis/public must be adjusted. This file conforms to the following structure:

```json
{
  "Envname": "<your_env>",
  "Mode": {
    "oneOf": [
      {
        "enum": [
          "LOCAL",
          "REMOTE"
        ],
        "type": "string"
      }
    ],
    "value": "LOCAL"
  },
  "endpoints": {
    "getBlockLayers": {
      "url": "viz_api/Layers/inblock",
      "method": "GET"
    },
    "getBlocknodes": {
      "url": "viz_api/Nodes",
      "method": "GET"
    }
  },
  "localconf": {
    "modelfile": "<your_model_file>.json",
    "original": ["<your_image>.jpg", "<your_image>.jpg"]
  }
}
```
Make sure to change the field that contain '<' '>' with the appropriatte name for your environment and data. The endpoints of each available route are pointing to the endpoints stablished on the nginx.conf file and can be adjusted accordingly.

Finally in the docker compose file make sure the external ports match your needs for the host.


## docker deployment

After configuring your environment, position yourself on the top directory and run the following command:

```bash
docker-compose up --build -d
```
this will generate the following containers:
 1. parsegraph_os_database_container: the postgress db
 2. parsegraph-api_os: the API connecting the db with the front visualization
 3. evaxplainify_viz_os: the visualization front.

To check it you may run:

```bash
docker ps
```
And the containers should be listed with a running status.

NOTES: 
 - The model to be used is loaded to the db at the start of the back container. The analysis can be done with all models that exist already on the database, but loading a new one requires to restart the API with the appropriate configuration.
 - The env option reset db in true will drop the existing tables and rebuild them at the start of the back API.

## Adding local data

Users may increase the local visualization options by adding the required data to the following folders.

- parsegraph-front-atlantis/public/data/images/original: add all the images available for selection in the homepage view.

- parsegraph-front-atlantis/public/data/images/evaxplainify: Under a folder with the original image name add all explainability images. The name of each image must follow the structure <original_image_name>\_<number_layer>\_<number_filter>.jpg ex: face0_1_30.jpg.

- parsegraph-front-atlantis/public/data/interpretability: Under a folder with the original image name, add the interpretability info by block. The name of each file must follow the structure <block*blocknumber*>.json ex: block1.json.

Additionaly, the original image names must be added to the envconfig.json, in the localconf/original section.

The referenced model can be also stablished by adding its structure in a json file under parsegraph-front-atlantis/public and changing the envconfig.json in section localconf/modelfile accordingly.

## References

[1] <a name="1"></a>[EvaXplainability - Enhancing ANN Explainability for Improved Security and Transparency](https://www.atlantis-horizon.eu/whitepapers/).