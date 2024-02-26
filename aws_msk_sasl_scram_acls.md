# Setting up ACLs on MSK Cluster

## Add brokers to the ACL

Get the cluster ARN from AWS Console and get the ZookeeperConnectString for the cluster

```
aws kafka get-bootstrap-brokers --cluster-arn $ClusterArn
```

Look for ZookeeperConnectString in the response JSON.

```
bin/kafka-acls.sh --authorizer-properties zookeeper.connect=$ZookeeperConnectString --add --allow-principal "User:CN=${DN}" --operation Read --group=* --topic <topic_name>
```

## List ACLs

```
bin/kafka-acls.sh --authorizer-properties zookeeper.connect=$ZookeeperConnectString --list --topic "*"
```

## Add ACL to application user to have READ access to topic: <topic_name>

```
bin/kafka-acls.sh --authorizer-properties zookeeper.connect=$ZookeeperConnectString --add --allow-principal "User:app_user" --operation Read --operation Describe --group '*' --topic <topic_name>
```

## Add ACL to application user to have WRITE access to topic: <topic_name>

```
bin/kafka-acls.sh --authorizer-properties zookeeper.connect=$ZookeeperConnectString --add --allow-principal "User:app_user" --operation Write --topic <topic_name>
```

## Add ACL to super_user to have read/write/delete access to all topics

```
bin/kafka-acls.sh --authorizer-properties zookeeper.connect=$ZookeeperConnectString --add --allow-principal "User:super_user" --operation All --topic=*
```

## Remove ACL for a topic

The best practice is to deny the user followed by removing the ACL. We do this because users who are already connected to cluster will continue to have access until a connection is reestablished. To
prevent this, it is in the best interest to deny permission followed by removing user.

### Deny ACL

```
bin/kafka-acls.sh --authorizer-properties zookeeper.connect=$ZookeeperConnectString  --deny-principal "User:app_user" --operation Write --topic <topic_name>
```

### Remove User

```
bin/kafka-acls.sh --authorizer-properties zookeeper.connect=$ZookeeperConnectString --remove --allow-principal "User:app_user" --operation Write --topic <topic_name>
```

### Examples

How do you remove ACL's with groups? Lets say you have two users with ACls as found from "list" command

```
Current ACLs for resource `ResourcePattern(resourceType=GROUP, name=*, patternType=LITERAL)`:
(principal=User:AmazonMSK_adhacp_2J3RFSBJ, host=_, operation=READ, permissionType=ALLOW)
(principal=User:AmazonMSK_adhacp_2J3RFSBJ, host=_, operation=DESCRIBE, permissionType=ALLOW)
(principal=User:AmazonMSK_adhacp_2TKVBWFA, host=_, operation=READ, permissionType=ALLOW)
(principal=User:AmazonMSK_adhacp_2TKVBWFA, host=_, operation=DESCRIBE, permissionType=ALLOW)
```

```
 bin/kafka-acls.sh --authorizer-properties zookeeper.connect=$ZookeeperConnectString --remove --allow-principal "User:AmazonMSK_adhacp_2TKVBWFA" --operation Describe --operation Read --group '*'
```

```
 bin/kafka-acls.sh --authorizer-properties zookeeper.connect=$ZookeeperConnectString --remove --allow-principal "User:AmazonMSK_adhacp_2J3RFSBJ" --operation Describe --operation Read --group '*'
```
