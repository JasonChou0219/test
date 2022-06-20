import sila_helper as sila


def run():
    sila.target_service_hostname = "http://10.152.248.14"
    blue_vary = sila.instantiate_sila_client(address="10.152.248.153", port=50103)
    print(blue_vary, flush=True)
