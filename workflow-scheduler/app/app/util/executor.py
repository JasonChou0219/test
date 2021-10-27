import docker


if __name__ == '__main__':
    client = docker.from_env()
    image = client.images.build(path="../../../../workflow-executor", dockerfile="workflow-executor.dockerfile", buildargs={"tag":"test"})
    # client.containers.run(image, ports={1880:1880})
    client.containers.run(image[0], ports={1880:1880}, name="NR-executor")