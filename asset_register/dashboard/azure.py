import os
from azure.mgmt.compute import ComputeManagementClient
from azure.mgmt.redis import RedisManagementClient
from azure.mgmt.rdbms.postgresql import PostgreSQLManagementClient
from azure.mgmt.keyvault import KeyVaultManagementClient
from azure.mgmt.frontdoor import FrontDoorManagementClient
from azure.mgmt.network import NetworkManagementClient
from azure.common.credentials import ServicePrincipalCredentials
from django.conf import settings

creds = ServicePrincipalCredentials(
    client_id=settings.OIDC_RP_CLIENT_ID,
    secret=settings.OIDC_RP_CLIENT_SECRET,
    tenant=settings.AZURE_TENANT
)


def get_inventory():
    vm_client = ComputeManagementClient(creds, '0add5c8e-50a6-4821-be0f-7a47c879b009')
    # for vm in vm_client.virtual_machines.list_all():
    #     print(f'{vm.name} ({vm.hardware_profile.vm_size}) - {vm.location}')

    redis_client = RedisManagementClient(creds, '0add5c8e-50a6-4821-be0f-7a47c879b009')
    # for redis in redis_client.redis.list():
    #     print(f'{redis.name} ({redis.sku.name} {redis.sku.family}{redis.sku.capacity}) - {redis.location}')

    sql_client = PostgreSQLManagementClient(creds, '0add5c8e-50a6-4821-be0f-7a47c879b009')
    # for sql in sql_client.servers.list():
    #     print(f'{sql.name} ({sql.sku.name}) - {sql.location}')

    keyvault_client = KeyVaultManagementClient(creds, '0add5c8e-50a6-4821-be0f-7a47c879b009')
    # for kv in keyvault_client.vaults.list():
    #     print(f'{kv.name} - {kv.location}')

    fd_client = FrontDoorManagementClient(creds, '0add5c8e-50a6-4821-be0f-7a47c879b009')
    # for fd in fd_client.front_doors.list():
    #     print(f'{fd.name} - {fd.location}')

    net_client = NetworkManagementClient(creds, '0add5c8e-50a6-4821-be0f-7a47c879b009')
    # for fw in net_client.azure_firewalls.list_all():
    #     print(f'{fw.name} ({fw.sku.tier} {fw.sku.name}) - {fw.location}')

    result = {
        'vms': list(vm_client.virtual_machines.list_all()),
        'redis': list(redis_client.redis.list()),
        'postgres': list(sql_client.servers.list()),
        'keyvault': list(keyvault_client.vaults.list()),
        'frontdoor': list(fd_client.front_doors.list()),
        'firewall': list(net_client.azure_firewalls.list_all()),
    }

    return result
