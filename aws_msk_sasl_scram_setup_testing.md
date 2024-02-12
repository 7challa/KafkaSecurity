# Follow the below steps after post MSK setup.

1. Retrieve cluster details. Run the below command to get the Zookeeper Connection String

```
aws kafka describe-cluster --cluster-arn <cluster-arn>
```

Look for ZookeeperConnectString in the response JSON.

2. Create Example Topic

```
<path-to-your-kafka-installation>/bin/kafka-topics.sh --create --zookeeper $ZookeeperConnectString --replication-factor 3 --partitions 1 --topic ExampleTopicName
```

3. Create JAAS config file name it users_jaas.conf

```
KafkaClient {
   org.apache.kafka.common.security.scram.ScramLoginModule required
   username="username_in_the_secret"
   password="password_in_the_secret";
};
```

4. Export JAAS config

```
export KAFKA_OPTS=-Djava.security.auth.login.config=<path-to-jaas-file>/conf/users_jaas.conf
```

5. Copy jks file

```
Copy /usr/java/latest/lib/security/cacerts <path-to-your-kafka-installation>/conf/kafka.client.truststore.jks
```

6. Create client_sasl.properties file under <path-to-jaas-file>/conf/ with the following content.

```
security.protocol=SASL_SSL
sasl.mechanism=SCRAM-SHA-512
ssl.truststore.location=<path-to-keystore-file>/kafka.client.truststore.jks
```

7. Retrieve bootstrap-servers of the cluster

```
aws kafka get-bootstrap-brokers --cluster-arn <ClusterArn>
```

8. Produce to the topic

```
<path-to-your-kafka-installation>/bin/kafka-console-producer.sh --broker-list BootstrapBrokerStringSaslScram --topic
ExampleTopicName --producer.config client_sasl.properties
```

9. Consume from the topic

```
<path-to-your-kafka-installation>/bin/kafka-console-consumer.sh --bootstrap-server BootstrapBrokerStringSaslScram --topic ExampleTopicName --from-beginning --consumer.config client_sasl.properties
```
