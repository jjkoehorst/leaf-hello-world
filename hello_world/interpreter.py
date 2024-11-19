import logging
import os
from datetime import datetime, timezone
from typing import Any

from influxobject import InfluxPoint
from leaf.adapters.equipment_adapter import AbstractInterpreter
from leaf.modules.logger_modules.logger_utils import get_logger

logger = get_logger(__name__, log_file="app.log", log_level=logging.DEBUG)

# Note the biolector json file is an example, not a concrete decision on terms...
current_dir = os.path.dirname(os.path.abspath(__file__))
metadata_fn = os.path.join(current_dir, "device.json")


class HelloWorldInterpreter(AbstractInterpreter):
    # '<institute>/<equipment_id>/<instance_id>/details'
    def __init__(self) -> None:
        super().__init__()
        logger.info("Initializing DEMO Interpreter")

    def retrieval(self) -> dict[str, Any]:
        logger.debug(f"Retrieval...")
        return {"measurement": "some data?", "start": None, "stop": None}

    def measurement(self, ignore) -> InfluxPoint:
        # Prepare the data
        influx_object = InfluxPoint()
        influx_object.measurement = "demo"
        influx_object.tags = {"tag": "tag"}
        influx_object.fields = {"field": 1}
        influx_object.time = datetime.now(timezone.utc)
        logger.debug(f"Measurement {influx_object}")

        return influx_object

    def simulate(self) -> None:
        pass

    def metadata(self, data: str) -> dict[str, str]:
        logger.debug(f"Metadata {str(data)[:50]}")
        return {"metadata": "Some content"}