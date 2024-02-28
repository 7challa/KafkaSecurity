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


def describe_topic(bootstrap_servers, topic_name):
    existing_topics_list = get_topics_from_cluster(bootstrap_servers)

    if topic_name not in existing_topics_list:
        print("Topic: {} - doesn't exist".format(topic_name))
        sys.exit(1)
    else:
        command = ["/opt/app/kafka-2.8.1/bin/kafka-topics.sh", "--bootstrap-server", " ", "--describe", "--topic", topic_name,
               "--command-config", "/opt/app/kafka-2.8.1/client.properties"]
        command[2] = bootstrap_servers
        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        output, error = process.communicate()

        if error:
            print("Unable to describe topic")
            print(error.decode())
        else:
            print(output.decode())

def check_arguments():
    arguments_length = len(sys.argv) - 1
    if arguments_length > 2 or arguments_length < 2 or arguments_length == 0:
        print("Incorrect arguments passed. Exiting...")
        print("Usage: describe_topic.py <bootstrap-servers> <topic_name>")
        print('Example: describe_topic.py "localhost:9098" alter_snaplogic_feed')
        sys.exit(1)

if __name__ == "__main__":
    check_arguments()
    bootstrap_servers = sys.argv[1]
    topic_name = sys.argv[2]

    try:
        describe_topic(bootstrap_servers,topic_name)
    except Exception as e:
        print("Error describing topic. {}".format(e))