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

## Add ACL to application user to have READ access to topic: <topic_name>

```
bin/kafka-acls.sh --authorizer-properties zookeeper.connect=$ZookeeperConnectString --add --allow-principal "User:app_user" --operation Read --group=\* --topic <topic_name>
```

## Add ACL to application user to have WRITE access to topic: <topic_name>

```
bin/kafka-acls.sh --authorizer-properties zookeeper.connect=$ZookeeperConnectString --add --allow-principal "User:app_user" --operation Write --topic <topic_name>
```

## Add ACL to superuser to have read/write/delete access to all topics

```
bin/kafka-acls.sh --authorizer-properties zookeeper.connect=$ZookeeperConnectString --add --allow-principal "User:super_user" --operation All --topic=*
```

## Remove ACL for a topic

The best practice is to deny the use followed by removing the ACL. We do this because users who are already connected to cluster will continue to have access until a connection is reestablished. To
prevent this it is in best interest to deny permission followed by removing user.

### Deny ACL

```
bin/kafka-acls.sh --authorizer-properties zookeeper.connect=$ZookeeperConnectString  --deny-principal "User:app_user" --operation Write --topic <topic_name>
```

### Remove User

```
bin/kafka-acls.sh --authorizer-properties zookeeper.connect=$ZookeeperConnectString --remove --allow-principal "User:app_user" --operation Write --topic <topic_name>
```
