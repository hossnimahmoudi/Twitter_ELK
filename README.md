# Twitter_ELK
## Introduction
This repository aims to provide a fully working data pipeline for doing Machine learning on Twitter data using the ELK (Elasticsearch, Logstash, and Kibana) stack.
## Concerning the Elasticsearch part
## Concerning the Kibana part
On Kibana side the repository offer:

* A dashboard for general data visualization
* A dashboard for comparison between a positive and negative tweet
* Different kind of visualizations
## Requirements

For the pipeline to work, you need a Twitter developer account, which you can obtain here: https://dev.twitter.com/resources/signup

### Linux users

This guide assumes that you have already installed [Elasticsearch](https://www.elastic.co/guide/en/elasticsearch/reference/current/setup.html), [Logstash](https://www.elastic.co/guide/en/logstash/current/installing-logstash.html) and [Kibana](https://www.elastic.co/guide/en/kibana/current/install.html). All three need to be installed properly in order to use this pipeline.

Once having installed ELK, here are some instructions to configure Elasticsearch to start automatically when the system boots up.

      sudo /bin/systemctl daemon-reload
      sudo /bin/systemctl enable elasticsearch.service

Elasticsearch can be started and stopped as follows:

      sudo systemctl start elasticsearch.service
      sudo systemctl stop elasticsearch.service

(Note that the same steps can be used for Kibana and Logstash)
