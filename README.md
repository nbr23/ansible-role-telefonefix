# ansible-role-telefonefix

Setup ansible role for téléfonefix

## DHCP Configuration Task

The `dhcp` task configures a Raspberry Pi to act as a DHCP server for the HT801 device, providing network configuration and assigning a static IP address to the device based on its MAC address.

### Variables

The following variables can be configured in your playbook or inventory:

| Variable | Default | Description |
|----------|---------|-------------|
| `network_subnet` | `192.168.100.0/24` | Network subnet for the DHCP server |
| `gateway_ip` | `192.168.100.1` | Gateway IP address for the Raspberry Pi |
| `dhcp_pool_start_offset` | `10` | Starting offset for DHCP pool (e.g., 10 = .10) |
| `dhcp_pool_size` | `40` | Number of addresses in DHCP pool |
| `ht801_mac` | `""` | MAC address of the HT801 device |
| `ht801_static_ip` | `""` | Static IP to assign to the HT801 device |
| `dns_servers` | `["8.8.8.8", "8.8.4.4"]` | DNS servers for DHCP clients |
| `ethernet_interface` | `eth0` | Ethernet interface to configure |

### Example Usage

```yaml
- hosts: raspberry_pi
  become: yes
  vars:
    ht801_mac: "00:11:22:33:44:55"
    ht801_static_ip: "192.168.100.50"
  tasks:
    - include_tasks: tasks/dhcp.yml
```

### What it does

1. Installs and enables systemd-networkd
2. Configures the specified ethernet interface with a static IP
3. Sets up a DHCP server on that interface
4. Creates a static lease for the HT801 device
5. Restarts networking services and displays the interface configuration
