from python_hosts import Hosts, HostsEntry


def add_hosts_entry(address: str, name: str) -> None:
    """
    Add the given IP address and hostname to the hosts file
    :param address: IP address to be added to the hosts file
    :param name: hostname to be added to the hosts file
    """
    hosts = Hosts()
    new_entry = HostsEntry(entry_type='ipv4', address=address, names=[name])
    hosts.add([new_entry])
    hosts.write()
