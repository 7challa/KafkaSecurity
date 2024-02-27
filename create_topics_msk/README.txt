Usage: create_topics.py <bootstrap-servers> <topics.yaml>
Example: create_topics.py "b-2.mskdhacpkafka17801670.rtwrz0.c21.kafka.us-east-1.amazonaws.com:9098,b-3.mskdhacpkafka17801670.rtwrz0.c21.kafka.us-east-1.amazonaws.com:9098,b-1.mskdhacpkafka17801670.rtwrz0.c21.kafka.us-east-1.amazonaws.com:9098" topics.yaml

1. Creates topics as defined in topics.yaml
2. Skips topics if the topic is already present on the cluster
3. Doesn't automatically update topic paramters is they are update in the second run

