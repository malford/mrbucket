#! /usr/bin/env python
# right now this script reports usage of an s3 bucket in gigs

# import some modules
import boto, os, argparse, sys
from hurry.filesize import size, verbose
from datetime import datetime

# setup argparse
parser = argparse.ArgumentParser(description='Mrbucket is a script to output S3 usage. It\'s buckets of fun!')
# add arguments and require a bucket name
parser.add_argument('-b', action='store', dest='bucket_name',
                    required=True, help='name of bucket to get size of')
parser.add_argument('-d', dest='date', help='sort keys by date', action='store_true')
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
total_bytes = 0
try:
    keylist = []
    for key in bucket.list():
        total_bytes += key.size
        key_info = (key.name.encode('utf-8'), key.size, datetime.strptime(key.last_modified.encode('utf-8'), "%Y-%m-%dT%H:%M:%S.000Z"))
        keylist.append(key_info)
        # if the bucket name provided is in corect list out the buckets that we know
except (TypeError, AttributeError):
        print "Something is incorrect with the bucket name you provided. Here are the ones I know of:"
        print conn.get_all_buckets()
        sys.exit(1)

# if s option or d option were used sort the keys and print them out
if results.size:
    keylist.sort(key=lambda key_info: key_info[1])
    print '\n'.join(str(s3_key) for s3_key in keylist)
elif results.date:
    keylist.sort(key=lambda key_info: key_info[2])
    print '\n'.join(str(s3_key) for s3_key in keylist)

# print out the total bucket usage
print '------------------------------------' 
print "This bucket is using %s bytes." % total_bytes
print "Or approximately %s" % size(total_bytes, system=verbose)

sys.exit(0)
