# Docker CA Companion

Automatically injects custom CA certificates into Docker containers when they start.

## Installation

The container image is automatically built and published to GitHub Container Registry. You can pull it using:

```bash
docker pull ghcr.io/buethsam/docker-ca-companion:latest
```

## Usage

Set the `WATCH_CONTAINERS` environment variable to a comma-separated list of container names to monitor.

### Docker Compose

```yaml
version: '3.8'
services:
  ca-companion:
    image: ghcr.io/buethsam/docker-ca-companion:latest
    environment:
      - WATCH_CONTAINERS=web-app,api-server
    volumes:
      - /var/run/docker.sock:/var/run/docker.sock:ro
      - ./certificates:/config:ro
    restart: unless-stopped
```

### Docker Run

```bash
docker run -d \
  --name ca-companion \
  -e WATCH_CONTAINERS=container1,container2 \
  -v /var/run/docker.sock:/var/run/docker.sock:ro \
  -v /path/to/certificates:/config:ro \
  ghcr.io/buethsam/docker-ca-companion:latest
```

### Building from Source

If you prefer to build the image yourself:

```bash
docker build -t docker-ca-companion .
```

## How It Works

1. Monitors Docker events for container starts
2. Copies `.crt` files from `/config` to `/usr/local/share/ca-certificates/` in watched containers
3. Runs `update-ca-certificates` to update the CA store

## Requirements

- Target containers must be Debian/Ubuntu-based
- Target containers need root access for certificate installation
- Certificate files must have `.crt` extension

## License

This project is licensed under the GNU General Public License v3.0. See the [LICENSE](LICENSE) file for details.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## Changelog

### Current Version
- Initial release with basic certificate injection functionality
- Support for monitoring multiple containers
- Automatic restart on failure
- Debian/Ubuntu container support

## Support

For issues, questions, or contributions, please use the GitHub issue tracker.
