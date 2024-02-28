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


def increase_partitions(bootstrap_servers, topic_name, num_partitions):
    existing_topics_list = get_topics_from_cluster(bootstrap_servers)
    # Update retention to 5 seconds
    config_value = "retention.ms=" + num_partitions

    if topic_name not in existing_topics_list:
        print("Topic: {} - doesn't exist".format(topic_name))
        sys.exit(1)
    else:
        desc_command = ["/opt/app/kafka-2.8.1/bin/kafka-topics.sh", "--bootstrap-server", " ", "--describe", "--topic", topic_name, "--command-config", "/opt/app/kafka-2.8.1/client.properties"]
        desc_command[2] = bootstrap_servers

        process = subprocess.Popen(desc_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        output, error = process.communicate()

        if error:
            print("Unable to describe topic on the cluster")
            print(error.decode())
        else:
            print(output.decode())
            print()

        alter_command = ["/opt/app/kafka-2.8.1/bin/kafka-topics.sh", "--bootstrap-server", " ", "--alter", "--topic", topic_name,
                   "--partitions", num_partitions, "--command-config", "/opt/app/kafka-2.8.1/client.properties"]
        alter_command[2] = bootstrap_servers

        alter_process = subprocess.Popen(alter_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        output, error = alter_process.communicate()

        if error:
            print("Unable to alter topic configuration on topic {}".format(topic_name))
            print(error.decode())
        else:
            print(output.decode())

def check_arguments():
    arguments_length = len(sys.argv) - 1
    if arguments_length != 3:
        print("Incorrect arguments passed. Exiting...")
        print("Usage: increase_partitions.py <bootstrap-servers> <topic_name>")
        print('Example: increase_partitions.py "localhost:9098" alter_snaplogic_feed 5')
        sys.exit(1)

if __name__ == "__main__":
    check_arguments()
    bootstrap_servers = sys.argv[1]
    topic_name = sys.argv[2]
    num_partitions = sys.argv[3]

    try:
        increase_partitions(bootstrap_servers,topic_name, num_partitions)
    except Exception as e:
        print("Error updating topic partitions. {}".format(e))