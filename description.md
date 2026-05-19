After Unmanic successfully processes a media file, this plugin POSTs the output file path to a [Media Preview Generator](https://github.com/stevezau/media_preview_generator) webhook endpoint, triggering it to scan the file and generate preview images.

## Configuration

- **Webhook URL** — The full URL of your Media Preview Generator custom webhook endpoint (e.g. `http://192.168.1.100:8080/api/webhooks/custom`).
- **Webhook Secret** — The API token configured in Media Preview Generator, sent as the `X-Auth-Token` request header. Leave blank if authentication is not required.

The plugin only fires when a task completes **successfully** and is silently skipped if no webhook URL is configured.
