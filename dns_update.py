import boto3
import json
import urllib.request, urllib.parse, urllib.error
import argparse


class AWSDynDns(object):
    def __init__(self, domain, record, hosted_zone_id, profile_name, ttl):
        self.ip_service = "https://api.ipify.org/"
        session = boto3.Session(profile_name=profile_name)
        self.client = session.client('route53')
        self.domain = domain
        self.record = record
        self.ttl = ttl
        self.hosted_zone_id = hosted_zone_id
        if self.record:
            self.fqdn = "{0}.{1}".format(self.record, self.domain)
        else:
            self.fqdn = self.domain

    def get_external_ip(self):
        try:
            self.external_ip = urllib.request.urlopen(self.ip_service).read().decode()
            print("Found external IP: {0}".format(self.external_ip))
        except Exception as e:
            raise Exception("error getting external IP")

    def check_existing_record(self):
        """ Get current external IP address """
        self.get_external_ip()

        """ Check for existing record and if it needs to be modified """
        response = self.client.list_resource_record_sets(
            HostedZoneId=self.hosted_zone_id,
            StartRecordName=self.fqdn,
            StartRecordType='A',
        )

        found_flag = False

        if len(response['ResourceRecordSets']) == 0:
            raise Exception("Could not find any records matching domain: {0}".format(self.fqdn))

        if self.fqdn in response['ResourceRecordSets'][0]['Name']:
            for ip in response['ResourceRecordSets'][0]['ResourceRecords']:
                if self.external_ip == ip['Value']:
                    found_flag = True
        else:
            raise Exception("Cannot find record set for domain: {0}".format(self.fqdn))

        return found_flag

    def update_record(self):
        if self.check_existing_record():
             print("IP is already up to date")
        else:
            response = self.client.change_resource_record_sets(
                HostedZoneId=self.hosted_zone_id,
                ChangeBatch={
                    'Comment': 'string',
                    'Changes': [
                        {
                            'Action': 'UPSERT',
                            'ResourceRecordSet': {
                                'Name': self.fqdn,
                                'Type': 'A',
                                'TTL': self.ttl,
                                'ResourceRecords': [
                                    {
                                        'Value': self.external_ip
                                    },
                                ],
                            }
                        },
                    ]
                }
            )
            print(response)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Manage a dynamic home IP address with an AWS hosted route53 domain")

    parser.add_argument(
        "--domain", "-d",
        help="Domain to modify",
        required=True
    )

    parser.add_argument(
        "--record", "-r",
        help="record to modify",
        required=False
    )

    parser.add_argument(
        "--zone", "-z",
        help="AWS hosted zone id",
        required=True
    )

    parser.add_argument(
        "--profile", "-p",
        help="AWS credential profile",
        required=True
    )

    parser.add_argument(
        "--ttl",
        help="Record TTL",
        required=False,
        default=300

    )

    args = parser.parse_args()

    run = AWSDynDns(args.domain, args.record, args.zone, args.profile, args.ttl)
    run.update_record()
