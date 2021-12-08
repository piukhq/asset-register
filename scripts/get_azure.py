import os

from azure.common.credentials import ServicePrincipalCredentials
from azure.mgmt.compute import ComputeManagementClient
from azure.mgmt.frontdoor import FrontDoorManagementClient
from azure.mgmt.keyvault import KeyVaultManagementClient
from azure.mgmt.network import NetworkManagementClient
from azure.mgmt.rdbms.postgresql import PostgreSQLManagementClient
from azure.mgmt.redis import RedisManagementClient

creds = ServicePrincipalCredentials(
    client_id=os.environ["AZURE_CLIENT_ID"],
    secret=os.environ["AZURE_CLIENT_SECRET"],
    tenant=os.environ["AZURE_TENANT_ID"],
)

vm_client = ComputeManagementClient(creds, "0add5c8e-50a6-4821-be0f-7a47c879b009")
for vm in vm_client.virtual_machines.list_all():
    print(f"{vm.name} ({vm.hardware_profile.vm_size}) - {vm.location}")
print()

redis_client = RedisManagementClient(creds, "0add5c8e-50a6-4821-be0f-7a47c879b009")
for redis in redis_client.redis.list():
    print(f"{redis.name} ({redis.sku.name} {redis.sku.family}{redis.sku.capacity}) - {redis.location}")
print()

sql_client = PostgreSQLManagementClient(creds, "0add5c8e-50a6-4821-be0f-7a47c879b009")
for sql in sql_client.servers.list():
    print(f"{sql.name} ({sql.sku.name}) - {sql.location}")
print()

keyvault_client = KeyVaultManagementClient(creds, "0add5c8e-50a6-4821-be0f-7a47c879b009")
for kv in keyvault_client.vaults.list():
    print(f"{kv.name} - {kv.location}")
print()

fd_client = FrontDoorManagementClient(creds, "0add5c8e-50a6-4821-be0f-7a47c879b009")
for fd in fd_client.front_doors.list():
    print(f"{fd.name} - {fd.location}")
print()

net_client = NetworkManagementClient(creds, "0add5c8e-50a6-4821-be0f-7a47c879b009")
for fw in net_client.azure_firewalls.list_all():
    print(f"{fw.name} ({fw.sku.tier} {fw.sku.name}) - {fw.location}")
print()

print()
