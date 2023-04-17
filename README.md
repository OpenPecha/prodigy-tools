<h1 align="center">
  <br>
  <a href="https://openpecha.org"><img src="https://avatars.githubusercontent.com/u/82142807?s=400&u=19e108a15566f3a1449bafb03b8dd706a72aebcd&v=4" alt="OpenPecha" width="150"></a>
  <br>
</h1>

<h3 align="center">Prodigy Tools</h3>

<!-- Replace the title of the repository -->

<p align="center">
  <a href="https://github.com/OpenPecha/Requests/issues/30">RFC</a> •
  <a href="#description">Description</a> •
  <a href="#owner">Owner</a> •
<!--   <a href="#floppy_disk-install">Install</a> • -->
  <a href="#docs">Docs</a>
</p>
<hr>

## Description

Tools for OpenPecha's use of Prodigy

<!-- This section provides a high-level overview for the repo -->

## Owner

- [Ta-Tsering](https://github.com/ta4tsering)

<!-- This section lists the owners of the repo -->


## Docs

## How to create new Instance

### Files Requirements

1. `Instance_Name.service` file (service unit file used by systemd)
2. `Instance_Name.json` file (Prodigy configuration file)
3. `Instance_Name.conf` file (Nginx web server configuration file)
4. `Instance_Name_recipe.py` (Instance's prodigy recipe file in .py)
5. Input data for recipe source file (can be .jsonl, .csv, etc.)

### Creating Required Files

1. Create Instance recipe to stream images to the Prodigy web application.
    - Location: `prodigy-tools/recipe/`
    - Example: [bdrc crop images recipe](https://github.com/OpenPecha/prodigy-tools/blob/main/recipes/bdrc_crop_images.py)
    ```
    return {
        "dataset": dataset,
        "stream": stream_from_s3(obj_keys),
        "view_id": "image_manual",
        "config": {
            "labels": ["PAGE"]
        }
    }
    ```
    - `dataset`: Name of the dataset (`bdrc-crop`)
    - `stream`: Yield image's s3 key or image URL
    - `view_id`: `image_manual` for annotating images
    - `labels`: List of labels to annotate on the image


2. Create Prodigy configuration JSON file.
    - Location: `prodigy-tools/configuration/`
    - Example: [bdrc_crop_images.json](https://github.com/OpenPecha/prodigy-tools/blob/main/configuration/bdrc_crop_images.json)
    ```
    "db_settings": {
        "sqlite": {
            "name": "bdrc_crop_images.sqlite",
            "path": "/usr/local/prodigy"
        }
    }
    ```
    - `name`: Name of the SQLite file where the annotations are saved
    - `path`: Path to where the SQLite file should be saved


3. Create `.service` file to be used by Systemd, a system and service manager for Linux OS.
    - Location: `/etc/systemd/system/`
    - Example: [bdrc_crop_images.service](https://github.com/OpenPecha/prodigy-tools/blob/main/install-scripts/prodigy_bdrc_crop_images.service)
    ```
    Environment=PRODIGY_CONFIG="/usr/local/prodigy/prodigy-tools/configuration/bdrc_crop_images.json"
    ```
    - `Environment=PRODIGY_CONFIG`: Path to the Prodigy configuration JSON file
    ```
    ExecStart=/usr/bin/python3.9 -m prodigy bdrc-crop-images-recipe bdrc_crop '/usr/local/prodigy/prodigy-tools/data/page_cropping.csv' -F /usr/local/prodigy/prodigy-tools/recipes/bdrc_crop_images.py
    ```
    - `bdrc-crop-images-recipe`: Name of the recipe from the recipe.py
    - `bdrc_crop`: Name of the dataset
    - `'/usr/local/prodigy/prodigy-tools/data/page_cropping.csv'`: Path to the data input source
    - `/usr/local/prodigy/prodigy-tools/recipes/bdrc_crop_images.py`: Path to instance recipe .py file


4. Create Nginx configuration `.conf`.
    - Location: `/etc/nginx/sites-enabled/`
    - Example: [prodigy.conf](https://github.com/OpenPecha/prodigy-tools/blob/main/install-scripts/prodigy.conf)
    ```
    upstream prodigyimages {
    server localhost:8090  fail_timeout=20s;
    keepalive 32;
    }
    ```
    - localhost: port number to listen to
        

## How to Load an instance
    
   - To test niginx configuration
        command : `sudo nginx -t`

   -  To restart the nginx (only needs to when .conf has been updated or changed)
        command : `sudo service nginx restart`

   -  To start the instance with service file
        command : 
            `sudo systemctl daemon-reload`
            `sudo systemctl restart name_of_service_file.service`

   -  To check the log of the instance
        command : `sudo journalctl -u name_of_service_file.service`
    
   -  To stop the instance from running
        command : `sudo systemctl stop name_of_service_file.service`
    
   -  To git pull the changes from the prodigy-tools to the server
        command : `sudo -u prodigy git pull` at `/usr/local/prodigy/prodigy-tools/`
