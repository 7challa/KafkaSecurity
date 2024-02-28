import subprocess
import yaml
import sys


def get_topics_from_cluster(bootstrap_servers):
    # Define the command to execute kafka-topics.sh with arguments
    command = ["/opt/app/kafka-2.8.1/bin/kafka-topics.sh", "--bootstrap-server", " ", "--list", "--command-config", "/opt/app/kafka-2.8.1/client.properties"]
    command[2] = bootstrap_servers
    xargs_command = ["xargs"]
    print("Connecting to MSK on: {}".format(command[2]))

    # Execute the command using subprocess
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    xargs_process = subprocess.Popen(xargs_command, stdin=process.stdout, stdout=subprocess.PIPE)
    output, error = xargs_process.communicate()

    if error:
        print("Unable to get existing topics on the cluster")
        print(error.decode())
    else:
        #print(output.decode())
        print()

    topics_list = output.decode().split()
    print("Current topics on the cluster are: {}".format(topics_list))
    return topics_list


def increase_partitions(topics, bootstrap_servers):
    existing_topics_list = get_topics_from_cluster(bootstrap_servers)

    for topic in topics:
        if topic['name'] not in existing_topics_list:
            print("Skipping alter topic: {} - Topic doesn't exist".format(topic['name']))
            continue

        # Creating topic if doesn't exist
        topic_name = topic['name']
        # print("Topic: {}, type: {}".format(topic_name, type(topic_name)))
        num_partitions = str(topic['partitions'])

        command = ["/opt/app/kafka-2.8.1/bin/kafka-topics.sh", "--bootstrap-server", " ", "--alter", "--topic", topic_name,
                   "--partitions", num_partitions, "--command-config", "/opt/app/kafka-2.8.1/client.properties"]
        command[2] = bootstrap_servers
        # print(command)

        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        output, error = process.communicate()

        if error:
            print("Unable to alter topic")
            print(error.decode())
        else:
            print(output.decode())
            print("Topic is altered!")

        command2 = ["/opt/app/kafka-2.8.1/bin/kafka-topics.sh", "--bootstrap-server", " ", "--describe", "--topic",
                   topic_name, "--command-config", "/opt/app/kafka-2.8.1/client.properties"]
        command2[2] = bootstrap_servers
        process = subprocess.Popen(command2, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        output2, error2 = process.communicate()

        if error:
            print("Unable to describe topic")
            print(error2.decode())
        else:
            print(output2.decode())



def load_topics_from_yaml(yaml_file):
    with open(yaml_file, 'r') as file:
        topics = yaml.safe_load(file)
    return topics['topics']

def check_arguments():
    arguments_length = len(sys.argv) - 1
    if arguments_length > 2 or arguments_length < 2 or arguments_length == 0:
        print("Incorrect arguments passed. Exiting...")
        print("Usage: increase_partitions.py <bootstrap-servers> <alter_topics.yaml>")
        print('Example: increase_partitions.py "localhost:9098" alter_topics.yaml')
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
       increase_partitions(topics, bootstrap_servers)
    except Exception as e:
       print("Error altering topic! {}".format(e))