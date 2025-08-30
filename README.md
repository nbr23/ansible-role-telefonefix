# ansible-role-telefonefix

Setup ansible role for téléfonefix

This Ansible role sets up a Raspberry Pi (or alike) as a DHCP server, deploys Asterisk with Twilio integration, and configures an HT801 analogue telephone adapter to connect to Asterisk. The role includes three main tasks described below.

## Tasks Overview

1. **DHCP Configuration** (`dhcp.yml`) - Configures Raspberry Pi as DHCP server for HT801
2. **Asterisk Setup** (`asterisk.yml`) - Installs Docker and deploys Asterisk container with Twilio
3. **HT801 Configuration** (`ht801.yml`) - Configures HT801 device via its API

## Example

```yaml
---
- hosts: raspberry_pi
  become: yes
  vars:
    # Network configuration
    network_subnet: "192.168.100.0/24"
    gateway_ip: "192.168.100.1"
    ethernet_interface: "eth0"
    
    # HT801 device configuration
    ht801_mac: "00:11:22:33:44:55"
    ht801_static_ip: "192.168.100.50"
    ht801_password: "admin"
    
    # Asterisk configuration
    public_ip: ""  # Your public IP
    asterisk_phone_user: "6001"
    asterisk_phone_password: "secure_phone_password"
    
    # Twilio configuration
    twilio_domaine: "your-domain.pstn.twilio.com"
    twilio_phone_number: "+15555551234"
    twilio_user: "your_twilio_username"
    twilio_password: "your_twilio_password"
    
    # HT801 SIP configuration (optional overrides)
    ht801_primary_sip_server: "{{ gateway_ip }}"
    ht801_sip_user_id: "{{ asterisk_phone_user }}"
    ht801_sip_authenticate_id: "{{ asterisk_phone_user }}"
    ht801_sip_authentication_password: "{{ asterisk_phone_password }}"
    
  tasks:
    - name: Configure DHCP server
      include_role:
        name: ansible-role-telefonefix
        tasks_from: dhcp.yml
    
    - name: Setup Asterisk with Twilio
      include_role:
        name: ansible-role-telefonefix
        tasks_from: asterisk.yml
    
    - name: Configure HT801 device
      include_role:
        name: ansible-role-telefonefix
        tasks_from: ht801.yml
```

## Task Details

### DHCP Configuration Task (`dhcp.yml`)

Configures the target to act as a DHCP server for the HT801 device.

**Key Variables:**
- `network_subnet`: Network subnet (default: `192.168.100.0/24`)
- `gateway_ip`: Gateway IP address (default: `192.168.100.1`)
- `ht801_mac`: MAC address of HT801 device (**required**)
- `ht801_static_ip`: Static IP for HT801 (**required**)
- `ethernet_interface`: Interface to configure (default: `eth0`)

### Asterisk Configuration Task (`asterisk.yml`)

Installs Docker and deploys an Asterisk container (using the image from https://github.com/nbr23/docker-asterisk) with Twilio SIP trunking.

**Key Variables:**
- `public_ip`: Your server's public IP (**required**)
- `asterisk_phone_user`: SIP extension (default: `6001`)
- `asterisk_phone_password`: SIP password (**required**)
- `twilio_domaine`: Twilio SIP domain (**required**)
- `twilio_phone_number`: Your Twilio number (**required**)
- `twilio_user`: Twilio SIP username (**required**)
- `twilio_password`: Twilio SIP password (**required**)

### HT801 Configuration Task (`ht801.yml`)

Configures the HT801's FTX port

**Key Variables:**
- `ht801_password`: Admin password for HT801 (**required**)
- `ht801_primary_sip_server`: Primary SIP server (default: `gateway_ip`)
- `ht801_sip_user_id`: SIP user ID (default: `asterisk_phone_user`)
- `ht801_sip_authenticate_id`: SIP auth ID (default: `asterisk_phone_user`)
- `ht801_sip_authentication_password`: SIP password (default: `asterisk_phone_password`)

```

## What This Role Does

1. **Network Setup**: Configures Raspberry Pi as DHCP server with static lease for HT801
2. **Telephony Backend**: Deploys Asterisk container with Twilio SIP trunk integration
3. **Device Configuration**: Automatically configures HT801 to connect to Asterisk
4. **Complete Integration**: Creates a working phone system connecting analog phones to Twilio
