#! /usr/bin/env python
# right now this script reports usage of an s3 bucket in gigs

# import some modules
import boto
import os
import argparse
import sys
from hurry.filesize import size
from hurry.filesize import verbose

parser = argparse.ArgumentParser(description='Mrbucket is a script to determine S3 usage. It\'s buckets of fun!')

parser.add_argument('-b', action='store', dest='bucket_name',
                    required=True, help='name of bucket to get size of')

results = parser.parse_args()

try:
    aws_access_key = os.environ["AWS_ACCESS_KEY"]
    aws_secret_access_key = os.environ["AWS_SECRET_ACCESS_KEY"]
except KeyError:
    print "you need to have the aws access key secret access key in you environnment variable"
    sys.exit(1)

conn = boto.connect_s3(aws_access_key, aws_secret_access_key)
bucket = conn.lookup(results.bucket_name)

total_bytes = 0
for key in bucket:
    total_bytes += key.size
print(total_bytes)
print size(total_bytes, system=verbose)
