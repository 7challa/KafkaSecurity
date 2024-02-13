# Setting up ACLs on MSK Cluster

## Add brokers to the ACL

Get the cluster ARN from AWS Console and get the ZookeeperConnectString for the cluster

```
aws kafka get-bootstrap-brokers --cluster-arn $ClusterArn
```

Look for ZookeeperConnectString in the response JSON.

```
bin/kafka-acls.sh --authorizer-properties zookeeper.connect=$ZookeeperConnectString --add --allow-principal "User:CN=${DN}" --operation Read --group=\* --topic <topic_name>
```
