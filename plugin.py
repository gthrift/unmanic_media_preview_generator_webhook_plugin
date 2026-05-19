import logging

import requests

from unmanic.libs.unplugins.settings import PluginSettings

logger = logging.getLogger(__name__)


class Settings(PluginSettings):
    settings = {
        "webhook_url": "",
        "webhook_secret": "",
    }

    form_settings = {
        "webhook_url": {
            "label": "Webhook URL (e.g. http://host:8080/api/webhooks/custom)",
            "input_type": "text",
        },
        "webhook_secret": {
            "label": "Webhook Secret (sent as X-Auth-Token header; leave blank if not required)",
            "input_type": "text",
        },
    }


def on_postprocessor_task_results(data):
    """Notify Media Preview Generator after a successful task completes."""
    settings = Settings(library_id=data.get("library_id"))

    webhook_url = settings.get_setting("webhook_url").strip()
    if not webhook_url:
        return data

    if not data.get("task_processing_success", False):
        logger.debug("Task did not succeed; skipping Media Preview Generator webhook.")
        return data

    destination_files = data.get("destination_files", [])
    if not destination_files:
        fallback = data.get("source_data", {}).get("abspath")
        if fallback:
            destination_files = [fallback]

    if not destination_files:
        logger.warning("No output files found to send to Media Preview Generator.")
        return data

    webhook_secret = settings.get_setting("webhook_secret").strip()
    headers = {"Content-Type": "application/json"}
    if webhook_secret:
        headers["X-Auth-Token"] = webhook_secret

    for file_path in destination_files:
        try:
            response = requests.post(
                webhook_url,
                json={"file_path": file_path},
                headers=headers,
                timeout=10,
            )
            response.raise_for_status()
            logger.info(
                "Media Preview Generator webhook sent for '%s' — HTTP %s",
                file_path,
                response.status_code,
            )
        except requests.exceptions.RequestException as e:
            logger.error(
                "Failed to send Media Preview Generator webhook for '%s': %s",
                file_path,
                e,
            )

    return data
