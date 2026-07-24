```
1. Create a secret in AWS Secrets Manager
Go to AWS Console → Secrets Manager → Store a new secret.
```

```
2. Choose Other type of secret.
Select Plaintext and paste:
{
"username": "<user>",
"password": "<password>"
}
```

3. Select your encryption key (KMS key).

4. Choose Next and name the secret with the prefix AmazonMSK_ (e.g., AmazonMSK_tutorials/MyFirstSecret).

5. Disable automatic rotation and store the secret.

6. Associate the secret with your MSK Cluster
  • Go to your MSK cluster in the console → Associate secrets → select your secret → Associate secrets.

7. Create a client.properties file

Go to the kafka_2.13-{YOUR MSK VERSION}/bin directory. Copy the following property settings and paste them into a new file. Name the file client.properties and save it. Use your username and password.

```
security.protocol=SASL_SSL
sasl.mechanism=SCRAM-SHA-512
sasl.jaas.config=org.apache.kafka.common.security.scram.ScramLoginModule required username="<user>" password="<password>";
```
Note: Here you should create a separate file for each user. For Example: clientadmin.properties, client reader.properties, clients.properties.

### Add ACLs for kafka_admin:

Run the following command from the Kafka bin directory:
```
<path-to-your-kafka-installation>/bin/kafka-acls.sh
            --bootstrap-server <BootstrapServerString> \
            --command-config <client.properties> \
            --add \
            --allow-principal User:kafka_admin \
            --operation All \
            --group="*" \
            --topic="*" \
            --transactional-id "*"
```

This ACL command essentially grants the user 'kafka_admin' superuser or admin-level privileges for managing topics and consumer groups within the Kafka cluster.

```
expected output
--->Adding ACLs for resource `ResourcePattern(resourceType=TOPIC, name=*, patternType=LITERAL)`:
(principal=User:kafka_admin, host=*, operation=ALL, permissionType=ALLOW)
--->Adding ACLs for resource `ResourcePattern(resourceType=GROUP, name=*, patternType=LITERAL)`:
(principal=User:kafka_admin, host=*, operation=ALL, permissionType=ALLOW)
--->Current ACLs for resource `ResourcePattern(resourceType=TOPIC, name=*, patternType=LITERAL)`:
(principal=User:kafka_admin, host=*, operation=ALL, permissionType=ALLOW)
--->Current ACLs for resource `ResourcePattern(resourceType=GROUP, name=*, patternType=LITERAL)`:
(principal=User:kafka_admin, host=*, operation=ALL, permissionType=ALLOW)
```
Note: BootstrapServerString = the scram auth enabled URL (eg: broker_host:9096)

- To view ACLs assigned for user kafka_admin
```
<path-to-your-kafka-installation>/bin/kafka-acls.sh \
            --bootstrap-server <BootstrapServerString> \
            --command-config <client.properties> \
            --list
```

```
expected output
--->Current ACLs for resource `ResourcePattern(resourceType=TOPIC, name=*, patternType=LITERAL)`:
(principal=User:kafka_admin, host=*, operation=ALL, permissionType=ALLOW)
--->Current ACLs for resource `ResourcePattern(resourceType=GROUP, name=*, patternType=LITERAL)`:
(principal=User:kafka_admin, host=*, operation=ALL, permissionType=ALLOW)
```

8. Now, create kafka_cicd and associate with MSK cluster same as how you did it for kafka_admin. Add ACL's as below to give kafka_cicd user
   permission to create/describe/delete topics. Some extra permissions are needed for terraform to work (eg: describe)

BOOTSTRAP_SERVERS="b-1.demo2.orange.c23.kafka.us-east-1.amazonaws.com:9096,b-2.demo2.orange.c23.kafka.us-east-1.amazonaws.com:9096"

### Example: Give user kafka_cicd to create/describe/delete topic permission 
Additional permissions are needed for terraform 

```
./kafka-acls.sh --bootstrap-server $BOOTSTRAP_SERVERS \
            --command-config ./client_sasl.properties \
            --add \
            --allow-principal User:kafka_cicd \
            --operation Create \
            --topic "*"

./kafka-acls.sh --bootstrap-server $BOOTSTRAP_SERVERS \
            --command-config ./client_sasl.properties \
            --add \
            --allow-principal User:kafka_cicd \
            --operation Describe \
            --topic "*"

# Add Write permission (required for topic creation verification)
./kafka-acls.sh --bootstrap-server $BOOTSTRAP_SERVERS \
            --command-config ./client_sasl.properties \
            --add \
            --allow-principal User:kafka_cicd \
            --operation Write \
            --topic "*"

# Add Read permission (may be required for verification)
./kafka-acls.sh --bootstrap-server $BOOTSTRAP_SERVERS \
            --command-config ./client_sasl.properties \
            --add \
            --allow-principal User:kafka_cicd \
            --operation Read \
            --topic "*"

# Add Alter permission (required for topic configuration)
./kafka-acls.sh --bootstrap-server $BOOTSTRAP_SERVERS \
            --command-config ./client_sasl.properties \
            --add \
            --allow-principal User:kafka_cicd \
            --operation Alter \
            --topic "*"

# Add DescribeConfigs permission (required to read topic configs)
./kafka-acls.sh --bootstrap-server $BOOTSTRAP_SERVERS \
            --command-config ./client_sasl.properties \
            --add \
            --allow-principal User:kafka_cicd \
            --operation DescribeConfigs \
            --topic "*"

# Add AlterConfigs permission (required to set retention.ms and other configs)
./kafka-acls.sh --bootstrap-server $BOOTSTRAP_SERVERS \
            --command-config ./client_sasl.properties \
            --add \
            --allow-principal User:kafka_cicd \
            --operation AlterConfigs \
            --topic "*"

# Delete permission 
./kafka-acls.sh --bootstrap-server $BOOTSTRAP_SERVERS \
            --command-config ./client_sasl.properties \
            --add \
            --allow-principal User:kafka_cicd \
            --operation Delete \
            --topic "*"

# Grant principal access to any consumer group
./kafka-acls.sh \
            --bootstrap-server "$BOOTSTRAP_SERVERS" \
            --command-config ./client_sasl.properties \
            --add \
            --allow-principal User:kafka_cicd \
            --operation Read \
            --group '*'
```
