import logging
import os
from typing import Optional

from leaf.adapters.equipment_adapter import EquipmentAdapter
from leaf.error_handler.error_holder import ErrorHolder
from leaf.metadata_manager.metadata import MetadataManager
from leaf.modules.input_modules.polling_watcher import PollingWatcher
from leaf.modules.input_modules.simple_watcher import SimpleWatcher
from leaf.modules.logger_modules.logger_utils import get_logger
from leaf.modules.phase_modules.measure import MeasurePhase
from leaf.modules.phase_modules.start import StartPhase
from leaf.modules.phase_modules.stop import StopPhase
from leaf.modules.process_modules.discrete_module import DiscreteProcess

from hello_world.interpreter import HelloWorldInterpreter

logger = get_logger(__name__, log_file="app.log", log_level=logging.DEBUG)

class HelloWorldAdapter(EquipmentAdapter):
    def __init__(
        self,
        instance_data,
        output,
        error_holder: Optional[ErrorHolder] = None,
        interval: int = 10
    ) -> None:
        self.error_holder = error_holder
        logger.info(
            f"Initializing DEMO Adapter"
        )
        # Obtain device metadata
        current_dir = os.path.dirname(os.path.abspath(__file__))
        metadata_fn = os.path.join(current_dir, 'device.json') # Check what can be obtained through the API

        # Create a metadata manager
        metadata_manager: MetadataManager = MetadataManager()
        metadata_manager.load_from_file(metadata_fn)
        # Create a polling watcher
        watcher: PollingWatcher = SimpleWatcher(metadata_manager=metadata_manager, interval=interval, measurement_callbacks=[])
        # Create the phases?
        start_p: StartPhase = StartPhase(output, metadata_manager)
        stop_p: StopPhase = StopPhase(output, metadata_manager)
        measure_p: MeasurePhase = MeasurePhase(output_adapter=output, metadata_manager=metadata_manager)
        # details_p: InitialisationPhase = InitialisationPhase(output, metadata_manager)
        watcher.add_measurement_callback(measure_p.update)
        # watcher.add_stop_callback(stop_p.update)
        # watcher.add_initialise_callback(details_p.update)
        phase = [start_p, measure_p, stop_p]
        mock_process = [DiscreteProcess(phase)]

        instance_data: dict[str, str] = {
            "instance_id": "test_maq",
            "institute": "test_ins",
            "experiment_id": "test_exp",
        }

        super().__init__(instance_data=instance_data, watcher=watcher, process_adapters=mock_process, interpreter=HelloWorldInterpreter(), metadata_manager=metadata_manager)  # type: ignore
        self._metadata_manager.add_equipment_data(metadata_fn)

    def _fetch_data(self):
        logger.info("Fetching data????????????????????????????/")