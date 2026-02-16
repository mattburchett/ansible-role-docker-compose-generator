# ansible-role-docker-compose-generator

Pass this role a hash and it will generate a docker-compose.yml file. The following structure is supported and is designed to be passed to the role using `group_vars`.

Container definitions use **native docker-compose keys** directly. The only role-specific keys are:
- `service_name` (required) — becomes the service key in docker-compose
- `active` (required) — set to `true` to include the service, `false` to exclude it
- `include_global_env_vars` (optional) — set to `true` to prepend `global_env_vars` to this service's environment

Any valid docker-compose service key (ports, volumes, networks, deploy, healthcheck, etc.) can be added to a container definition and will be rendered automatically.

Rendered files are output to the `output` directory.

```
---

# global vars
global_env_vars:
  - "PUID=1313"
  - "PGID=1313"

# container definitions
containers:
  - service_name: letsencrypt
    active: true
    image: linuxserver/letsencrypt
    container_name: le
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - "{{ appdata_path }}/letsencrypt/config:/config"
    networks:
      - proxy
    restart: always
    depends_on:
      - unifi
      - nextcloud
      - quassel
    include_global_env_vars: true
    environment:
      - EMAIL=email@email.com
      - "URL=some.tld"
      - "SUBDOMAINS=nc, irc, unifi"
      - ONLY_SUBDOMAINS=true
      - DHLEVEL=4096
      - TZ=Europe/London
      - VALIDATION=http
    mem_limit: 256m
  - service_name: nextcloud
    active: true
    image: nextcloud
    container_name: nextcloud
    volumes:
      - "{{ appdata_path }}/nextcloud/html:/var/www/html"
      - "{{ appdata_path }}/nextcloud/apps:/var/www/html/custom_apps"
      - "{{ appdata_path }}/nextcloud/config:/var/www/html/config"
      - "{{ appdata_path }}/nextcloud/data:/var/www/html/data"
      - "{{ appdata_path }}/nextcloud/theme:/var/www/html/themes"
    mem_limit: 256m
    restart: unless-stopped
    ports:
      - "8081:80"
  - service_name: unifi
    active: true
    image: linuxserver/unifi
    container_name: unifi
    mem_limit: 512m
    volumes:
      - "{{ appdata_path }}/unifi:/config"
    depends_on:
      mongodb:
        condition: service_started
    include_global_env_vars: true
    restart: unless-stopped
  - service_name: quassel
    active: true
    image: linuxserver/quassel
    container_name: quassel
    include_global_env_vars: true
    volumes:
      - "{{ appdata_path }}/quassel:/config"
    mem_limit: 128m
    ports:
      - "4242:4242"
  - service_name: custom-app
    active: true
    build: ./app
    container_name: custom-app
    volumes:
      - "{{ appdata_path }}/custom-app:/data"
    restart: unless-stopped
  - service_name: advanced-app
    active: true
    build:
      context: ./src
      dockerfile: Dockerfile.prod
    container_name: advanced-app
    ports:
      - "8080:8080"

compose_networks:
  - name: proxy
    external: true
    network_name: proxy
```

## Migration from v1

If upgrading from the previous version, note these breaking changes:

| Old | New |
|-----|-----|
| `sysctl` | `sysctls` (native docker-compose key) |
| `single_command` | `command` |
| Omitting `container_name` (auto-defaulted to `service_name`) | Must specify `container_name` explicitly |
| `depends_on: [{service: mongodb, condition: service_started}]` | `depends_on: {mongodb: {condition: service_started}}` |
| GPU deploy with implicit driver/capabilities defaults | Specify the full `deploy` block |
