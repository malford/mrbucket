#! /usr/bin/env python
# the idea of this script is to help delete archives from a glacier
# vault. I have set a static input file here that should change later.
# Once working to delete the archives in the list it will not register
# until next glacier inventory.


# import some modules
import boto, os, argparse, sys
from boto.glacier.layer1 import Layer1

# setup argparse
parser = argparse.ArgumentParser(description='Frozenbucket is a script to output S3 usage. It\'s buckets of fun!')
# add arguments and require a vault name
parser.add_argument('-v', action='store', dest='vault_name',
                    required=True, help='name of vault to remove archive from')

results = parser.parse_args()
#check for AWS access keys in the environment variables
try:
    aws_access_key = os.environ["AWS_ACCESS_KEY"]
    aws_secret_access_key = os.environ["AWS_SECRET_ACCESS_KEY"]
except KeyError:
    print "you need to have the aws access key and secret access key in you environnment variable"
    sys.exit(1)

glacier_layer1 = Layer1(aws_access_key_id=aws_access_key, aws_secret_access_key=aws_secret_access_key)

# from the stripped down json output file of the archive id's read the
# file and create a list as well as take off the new line charecter
f = map(lambda s: s.rstrip('\n'), [ i for i in open('archiveID.out.noquote', 'r').readlines()])

# for each item in the list delete it from the vault. 
for line in f:
    delete_output = glacier_layer1.delete_archive(results.vault_name, line)
    print delete_output

# connect to the glacier account and connect to the vault
#conn = boto.connect_s3(aws_access_key, aws_secret_access_key)
#vault = conn.lookup(results.vault_name)
