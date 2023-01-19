#!/bin/bash

# Stop the Prodigy service
sudo systemctl stop prodigy_bdrc_crop_images.service

# Run the Python script
python3 -m update_s3_url.py /usr/local/prodigy/bdrc_crop_images.sqlite

# Start the Prodigy service again
sudo systemctl start prodigy_bdrc_crop_images.service
