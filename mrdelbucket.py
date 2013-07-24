#! /usr/bin/env python
# right now this script reports usage of an s3 bucket in gigs

# import some modules
import boto, os, argparse, sys

# setup argparse
parser = argparse.ArgumentParser(description='MrDelbucket is a script to recursivly delete objects in an S3 bucket. It\'s buckets of fun!')
# add arguments and require a bucket name
parser.add_argument('-b', action='store', dest='bucket_name',
                    required=True, help='name of bucket to get size of')
parser.add_argument('-s', dest='size', help='sort keys by size', action='store_true')

results = parser.parse_args()
#check for AWS access keys in the environment variables
try:
    aws_access_key = os.environ["AWS_ACCESS_KEY"]
    aws_secret_access_key = os.environ["AWS_SECRET_ACCESS_KEY"]
except KeyError:
    print "you need to have the aws access key secret access key in you environnment variable"
    sys.exit(1)

# connect to the s3 account and connect to the bucket
conn = boto.connect_s3(aws_access_key, aws_secret_access_key)
bucket = conn.lookup(results.bucket_name)

# make a list of tuples of the s3 key info
keylist = []
for key in bucket.list():
    bucket.delete_key(key.key)

sys.exit(0)
