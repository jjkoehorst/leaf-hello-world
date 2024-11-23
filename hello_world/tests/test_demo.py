import logging
import os
import unittest
import yaml
from leaf.adapters.functional_adapters.maq_observations import interpreter
from leaf.modules.logger_modules.logger_utils import get_logger
from leaf.modules.output_modules.mqtt import MQTT
from adapter import HelloWorldAdapter

logger = get_logger(__name__, log_file="app.log", log_level=logging.DEBUG)

class HelloWorldCase(unittest.TestCase):
    def setUp(self) -> None:
        logger.info("Clearing log file")
        if os.path.exists("app.log"):
            os.remove("app.log")

        # Load example.yaml
        curr_dir: str = os.path.dirname(os.path.realpath(__file__))
        example_path = os.path.join(curr_dir, "../../example.yaml")

        try:
            with open(example_path, "r") as file:
                self._config = yaml.safe_load(file)
                logger.info(f"Config: {self._config}")
        except FileNotFoundError:
            self.fail(f"Configuration file {example_path} not found.")

    def tearDown(self) -> None:
        logger.info("Test completed. Cleaning up resources.")

    def test_demo_adapter(self) -> None:
        self.output = MQTT("test.mosquitto.org", 1883)
        # self.output.transmit("test", """'{"test": "test"}""")
        self.instance_data: dict[str, str] = {
            "instance_id": "test_maq",
            "institute": "test_ins",
            "experiment_id": "test_exp",
        }

        adap = HelloWorldAdapter(instance_data=self.instance_data, output=self.output)
        adap.start()

        # Add assertions
        self.assertIsNotNone(adap)
        logger.info("HelloWorldAdapter started successfully.")

    def test_demo_interpreter_id(self) -> None:
        inter = interpreter.MAQInterpreter(token="_RANDOM_TOKEN_")
        logger.debug(f"ID of interpreter: {inter.id}")
        # Add assertions
        self.assertIsNotNone(inter.id)
        self.assertIsInstance(inter.id, str)

    def test_load_adapters(self) -> None:
        """Dynamically load adapters registered via entry points."""
        from importlib.metadata import entry_points
        adapters = {}
        for entry_point in entry_points(group="leaf.adapters"):
            adapters[entry_point.name] = entry_point.load()
        logging.warning(f"Adapters loaded: {adapters}")

        # Add assertions
        self.assertIn("hello_world", adapters)
        self.assertIsNotNone(adapters["hello_world"])

if __name__ == "__main__":
    unittest.main()
