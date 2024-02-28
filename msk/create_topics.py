import subprocess
import yaml
import sys


def get_topics_from_cluster(bootstrap_servers):
    # Define the command to execute kafka-topics.sh with arguments
    command = ["/opt/app/kafka_2.13-2.8.1/bin/kafka-topics.sh", "--bootstrap-server", " ", "--list", "--command-config", "/opt/app/kafka_2.13-2.8.1/client.properties"]
    command[2] = bootstrap_servers
    xargs_command = ["xargs"]
    print("bootstrap_servers: {}".format(command[2]))

    # Execute the command using subprocess
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    xargs_process = subprocess.Popen(xargs_command, stdin=process.stdout, stdout=subprocess.PIPE)
    output, error = xargs_process.communicate()

    if error:
        print("Unable to get existing topics on the cluster")
        print(error.decode())
    else:
        print(output.decode())

    topics_list = output.decode().split()
    print("Current topics on the cluster are: {}".format(topics_list))
    return topics_list


def create_topics(topics, bootstrap_servers):
    existing_topics_list = get_topics_from_cluster(bootstrap_servers)

    for topic in topics:
        if topic['name'] in existing_topics_list:
            print("Skipping topic create {}".format(topic['name']))
            continue

        # Creating topic if doesn't exist
        topic_name = topic['name']
        print("Topic: {}, type: {}".format(topic_name,type(topic_name)))
        num_partitions = str(topic['partitions'])
        replication_factor = str(topic['replication_factor'])
        retention_time = str(topic['retention_time'])
        config_value = "retention.ms=" + retention_time

        command = ["/opt/app/kafka_2.13-2.8.1/bin/kafka-topics.sh", "--bootstrap-server", " ", "--create", "--topic", topic_name,
                   "--partitions", num_partitions, "--replication-factor", replication_factor, "--config", config_value,
                   "--command-config", "/opt/app/kafka_2.13-2.8.1/client.properties"]
        command[2] = bootstrap_servers
        print(command)

        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        output, error = process.communicate()

        if error:
            print("Unable to create topic")
            print(error.decode())
        else:
            print(output.decode())

def load_topics_from_yaml(yaml_file):
    with open(yaml_file, 'r') as file:
        topics = yaml.safe_load(file)
    return topics['topics']

def check_arguments():
    arguments_length = len(sys.argv) - 1
    if arguments_length > 2 or arguments_length < 2 or arguments_length == 0:
        print("Usage: create_topics.py <bootstrap-servers> <topics.yaml>")
        print('Example: create_topics.py "mskbrokerhost:9098" topics.yaml')
        sys.exit(1)

if __name__ == "__main__":
    check_arguments()
    bootstrap_servers = sys.argv[1]
    yaml_file = sys.argv[2]
    try:
        topics = load_topics_from_yaml(yaml_file)
    except Exception as e:
        print("Error loading yaml file. {}".format(e))

    try:
        create_topics(topics, bootstrap_servers)
    except Exception as e:
        print("Error creating topics")

