#! /usr/bin/env python
# right now this script reports usage of an s3 bucket in gigs

# import some modules
import boto
import os
import argparse
from hurry.filesize import size

aws_access_key = os.environ["AWS_ACCESS_KEY"]
aws_secret_access_key = os.environ["AWS_SECRET_ACCESS_KEY"]
conn = boto.connect_s3(aws_access_key, aws_secret_access_key)
bucket = conn.lookup('akiaj5id5wjv45cdcy5acomhaystacksoftwarearq')

total_bytes = 0
for key in bucket:
    total_bytes += key.size
print size(total_bytes)
