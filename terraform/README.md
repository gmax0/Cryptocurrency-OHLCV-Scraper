Here you'll find basic Terraform resource declarations to provision an arbitrary number of AWS EC2 instances to scrape candlestick data with the scripts provided in this project. Scraped data will be saved to a provisioned S3 bucket.

I make no attempt to cosplay as a cLoUd gURu DEvOpS wizArD as this was hacked together in an evening.

### Usage

1. Setup a AWS Key Pair and make note of its name.
2. Download a local copy of the private key.
3. Execute the following command

```terraform apply -var ec2_count={N} -var key_name=MASTER_KEY -var key_location={path to private key} -var discord_webhook_url={webhook url}```

Variable | Description
--- | ---
ec2_count | number of EC2 instances
key_name | AWS Key Pair name 
key_location | AWS Key Pair private key path
discord_webhook_url | Webhook for notifying when jobs complete

Once EC2 instances become available, you can issue remote commands to each. This still needs to be fully automated.

For example:


```
ssh -i KEY.pem -o StrictHostKeyChecking=no ubuntu@XXX.XX.XXX.XXX "source /etc/profile; nohup python3 coinbasepro-scraper.py \
--startDate 1609459200000 \
--endDate 1612137600000 \
--resolution 1m \
--market ETH-USD > /dev/null 2>&1 &
```