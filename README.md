# ansible-role-telefonefix

Setup ansible role for [téléfonefix](https://wip.tf/posts/telefonefix/)

This Ansible role sets up a Raspberry Pi (or alike) as a DHCP server, deploys Asterisk with Twilio integration, and configures an HT801 analogue telephone adapter to connect to Asterisk. The role includes three main tasks described below.

## Tasks Overview

1. **DHCP Configuration** (`dhcp.yml`) - Configures Raspberry Pi as DHCP server for HT801
2. **Asterisk Setup** (`asterisk.yml`) - Installs Docker and deploys Asterisk container with Twilio
3. **HT801 Configuration** (`ht801.yml`) - Configures HT801 device via its API
4. **Asterisk Playbacks Generate** (`asterisk_playbacks_generate.yml`) - Generates custom audio playbacks for Asterisk using TTS

## Example

```yaml
---
- hosts: raspberry_pi
  become: yes
  vars:
    # Network configuration
    telefonefix_network_subnet: "192.168.100.0/24"
    telefonefix_gateway_ip: "192.168.100.1"
    telefonefix_ethernet_interface: "eth0"
    
    # HT801 device configuration
    ht801_mac: "00:11:22:33:44:55"
    ht801_static_ip: "192.168.100.50"
    ht801_password: "admin"
    
    # Asterisk configuration
    telefonefix_public_ip: ""  # Your public IP
    telefonefix_asterisk_phone_user: "6001"
    telefonefix_asterisk_phone_password: "secure_phone_password"
    
    # Twilio configuration
    telefonefix_twilio_domaine: "your-domain.pstn.twilio.com"
    telefonefix_twilio_phone_number: "+15555551234"
    telefonefix_twilio_user: "your_twilio_username"
    telefonefix_twilio_password: "your_twilio_password"
    
    # HT801 SIP configuration (optional overrides)
    ht801_primary_sip_server: "{{ telefonefix_gateway_ip }}"
    ht801_sip_user_id: "{{ telefonefix_asterisk_phone_user }}"
    ht801_sip_authenticate_id: "{{ telefonefix_asterisk_phone_user }}"
    ht801_sip_authentication_password: "{{ telefonefix_asterisk_phone_password }}"
    
    # TTS Playbacks configuration (optional)
    telefonefix_asterisk_playback_patterns:
      connecting:
        en: "Connecting you to ${contact_name}"
        fr: "Connexion vers ${contact_name}"
      not-allowed:
        en: "Calls to ${contact_name} are not allowed at this time"
        fr: "Les appels vers ${contact_name} ne sont pas autorisés en ce moment"
      currently-busy:
        en: "${contact_name} is currently busy"
        fr: "${contact_name} est occupé"
      unavailable:
        en: "${contact_name} is currently unavailable"
        fr: "${contact_name} n'est pas disponible"

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

    - name: Generate custom Asterisk playbacks
      include_role:
        name: ansible-role-telefonefix
        tasks_from: asterisk_playbacks_generate.yml
```

## Task Details

### DHCP Configuration Task (`dhcp.yml`)

Configures the target to act as a DHCP server for the HT801 device.

**Key Variables:**
- `telefonefix_network_subnet`: Network subnet (default: `192.168.100.0/24`)
- `telefonefix_gateway_ip`: Gateway IP address (default: `192.168.100.1`)
- `ht801_mac`: MAC address of HT801 device (**required**)
- `ht801_static_ip`: Static IP for HT801 (**required**)
- `telefonefix_ethernet_interface`: Interface to configure (default: `eth0`)

### Asterisk Configuration Task (`asterisk.yml`)

Installs Docker and deploys an Asterisk container (using the image from https://github.com/nbr23/docker-asterisk) with Twilio SIP trunking.

**Key Variables:**
- `telefonefix_public_ip`: Your server's public IP (**required**)
- `telefonefix_asterisk_phone_user`: SIP extension (default: `6001`)
- `telefonefix_asterisk_phone_password`: SIP password (**required**)
- `telefonefix_twilio_domaine`: Twilio SIP domain (**required**)
- `telefonefix_twilio_phone_number`: Your Twilio number (**required**)
- `telefonefix_twilio_user`: Twilio SIP username (**required**)
- `telefonefix_twilio_password`: Twilio SIP password (**required**)
- `telefonefix_asterisk_extra_sounds_folder`: Local path to additional sound files to copy into Asterisk container (optional)
- `telefonefix_call_duration_limit_minutes`: Maximum call duration in minutes (default: 60 minutes)
- `telefonefix_super_user_override_prefix`: Prefix for bypassing time restrictions (optional) - if set, allows calling extensions regardless of allowed hours by prefixing the extension with this value (e.g., if set to "23", dialing 23101 will call extension 101 bypassing time restrictions)

### HT801 Configuration Task (`ht801.yml`)

Configures the HT801's FTX port

**Key Variables:**
- `ht801_password`: Admin password for HT801 (**required**)
- `ht801_primary_sip_server`: Primary SIP server (default: `telefonefix_gateway_ip`)
- `ht801_sip_user_id`: SIP user ID (default: `telefonefix_asterisk_phone_user`)
- `ht801_sip_authenticate_id`: SIP auth ID (default: `telefonefix_asterisk_phone_user`)
- `ht801_sip_authentication_password`: SIP password (default: `telefonefix_asterisk_phone_password`)

### Asterisk Playbacks Generate Task (`asterisk_playbacks_generate.yml`)

Generates custom TTS audio playbacks for Asterisk based on extension configuration and text patterns. This task uses a local TTS API container to generate personalized audio messages for each extension.

**Key Variables:**

- `telefonefix_asterisk_playback_patterns`: Text patterns for different call scenarios (**required**)
- Extension configuration file (YAML format) containing contact names and languages (**required**)

**Example `telefonefix_asterisk_playback_patterns` configuration:**

```yaml
telefonefix_asterisk_playback_patterns:
  connecting:
    en: "Connecting you to ${contact_name}"
    fr: "Connexion vers ${contact_name}"
  not-allowed:
    en: "Calls to ${contact_name} are not allowed at this time"
    fr: "Les appels vers ${contact_name} ne sont pas autorisés en ce moment"
  currently-busy:
    en: "${contact_name} is currently busy"
    fr: "${contact_name} est occupé"
  unavailable:
    en: "${contact_name} is currently unavailable"
    fr: "${contact_name} n'est pas disponible"
```

**Extension configuration file format:**

The task reads an allo-wed configuration file containing extension details. For the complete configuration format and examples, see: https://github.com/nbr23/allo-wed/

**Variable substitution:**

The `${contact_name}` variable in the pattern text is automatically replaced with the `contact_name` field from each extension's configuration. If no `contact_name` is specified for an extension, the extension number itself is used as a fallback.

The task will:
1. Start a local TTS API container using gopipertts
2. Generate audio files for each pattern/extension/language combination
3. Convert audio to Asterisk-compatible GSM format
4. Place generated files in the appropriate Asterisk sounds directory

Generated files will be organized by extension directory with the pattern: `{extension}/{pattern}.gsm` (e.g., `101/connecting.gsm`, `102/currently-busy.gsm`)

```

## What This Role Does

1. **Network Setup**: Configures Raspberry Pi as DHCP server with static lease for HT801
2. **Telephony Backend**: Deploys Asterisk container with Twilio SIP trunk integration
3. **Device Configuration**: Automatically configures HT801 to connect to Asterisk
4. **Custom Audio Generation**: Creates personalized TTS audio messages for each extension
5. **Complete Integration**: Creates a working phone system connecting analog phones to Twilio
