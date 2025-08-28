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
    - name: DHCP config
      include_role:
        name: ansible-role-telefonefix
        tasks_from: dhcp.yml
```

### What it does

1. Installs and enables systemd-networkd
2. Configures the specified ethernet interface with a static IP
3. Sets up a DHCP server on that interface
4. Creates a static lease for the HT801 device
5. Restarts networking services and displays the interface configuration

## Asterisk Configuration Task

The `asterisk` task installs Docker and deploys an Asterisk container configured to work with Twilio SIP trunking for telephony services.

### Variables

The following variables can be configured in your playbook or inventory:

| Variable | Default | Description |
|----------|---------|-------------|
| `public_ip` | `""` | **Required:** Public IP address of your server |
| `asterisk_phone_user` | `"6001"` | SIP phone user/extension number |
| `asterisk_phone_password` | `""` | **Required:** Password for the SIP phone user |
| `twilio_domaine` | `""` | **Required:** Twilio SIP domain |
| `twilio_phone_number` | `""` | **Required:** Twilio phone number |
| `twilio_user` | `""` | **Required:** Twilio SIP username |
| `twilio_password` | `""` | **Required:** Twilio SIP password |
| `mounted_config_files` | `["pjsip.conf", "rtp.conf", "extensions.conf"]` | Configuration files to push and mount in container |

### Example Usage

```yaml
- hosts: asterisk_server
  become: yes
  vars:
    public_ip: "192.168.1.100"
    asterisk_phone_password: "secure_password"
    twilio_domaine: "your-twilio-domain.pstn.twilio.com"
    twilio_phone_number: "+15555555555"
    twilio_user: "your_twilio_username"
    twilio_password: "your_twilio_password"
  tasks:
    - name: Asterisk setup
      include_role:
        name: ansible-role-telefonefix
        tasks_from: asterisk.yml
```

### What it does

1. Uninstalls any existing Docker packages
2. Installs Docker CE from the official Docker repository
3. Starts and enables the Docker service
4. Adds the current user to the docker group
5. Creates the Asterisk configuration directory
6. Deploys templated configuration files (pjsip.conf, rtp.conf, extensions.conf)
7. Copies the [allo-wed](https://github.com/nbr23/allo-wed) configuration
8. Runs the Asterisk container with proper volume mounts and network configuration
