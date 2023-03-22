import boto3
import sys
import datetime
import pytz
# Set up the EC2 client
ec2 = boto3.client('ec2')

utc=pytz.UTC
#delete_inst = sys.argv[1] #delete time

# Define the tag key and value to search for
tag_key = 'Retention Period'
#tag_value = '5'

# Get a list of all snapshots with the specified tag
owner_id = sys.argv[1]
# Get a list of all snapshots with the specified tag

response = ec2.describe_snapshots(OwnerIds=[owner_id])
#print(response)

# Extract the snapshot IDs from the response
#snapshot_ids = [snapshot['SnapshotId'] for snapshot in response['Snapshots']]

for snapshot in response['Snapshots']:
    retention = ''
    if snapshot.get('Tags', False):
        for tag in snapshot['Tags']:
            if tag['Key'] == 'Retention Period':
                retention = int(tag['Value'])
                break
    else:
        continue
    if retention:
        start_time = snapshot['StartTime'] + datetime.timedelta(retention)
        delete_time = datetime.datetime.now()

        if utc.localize(delete_time) > start_time:
            print('SnapShot {0} will be deleted as start time : {1}, delete time: {2} and Rentention Period is : {3}'.format(snapshot['SnapshotId'], start_time, delete_time, retention))
            delete_response = ec2.delete_snapshot(SnapshotId=snapshot['SnapshotId'])
            #print(delete_response)
