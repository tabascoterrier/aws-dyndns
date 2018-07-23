# aws-dyndns
Manage a dynamic home IP address with an AWS hosted route53 domain

```
usage: dns_update.py [-h] --domain DOMAIN --record
                     RECORD --zone ZONE --profile PROFILE

Update an AWS route53 DNS record with your external IP

optional arguments:
  -h, --help             Show this help message and exit
  --domain DOMAIN, -d    DOMAIN Domain to modify
  --record RECORD, -r    RECORD Record to modify
  --zone ZONE, -z ZONE   AWS hosted zone id
  --profile PROFILE, -p  PROFILE  AWS credential profile to use
```
