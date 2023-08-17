from typing import Dict

from fraud_detection.common import Workload
from fraud_detection.model_inference import ModelInference
from fraud_detection.utils.logger_utils import get_logger

_logger = get_logger()


class ModelInferenceJob(Workload):

    def _get_model_uri(self) -> str:
        model_name = self.env_vars['model_name']
        model_registry_stage = self.conf['mlflow_params']['model_registry_stage']
        model_uri = f'models:/{model_name}@{model_registry_stage}'

        return model_uri

    def _get_input_table_name(self) -> str:
        """
        Get the name of the input table to perform inference on
        """
        return f"{self.env_vars['feature_store_catalog_name']}.{self.env_vars['labels_table_database_name']}.{self.env_vars['labels_table_name']}"

    def _get_predictions_output_params(self) -> Dict:
        """
        Get a dictionary of delta_path, table_name, mode key-values to pass to run_and_write_batch of ModelInference
        """
        predictions_table_catalog_name = self.env_vars['predictions_table_catalog_name']
        predictions_table_database_name = self.env_vars['predictions_table_database_name']
        predictions_table_name = f'{predictions_table_catalog_name}.{predictions_table_database_name}.{self.env_vars["predictions_table_name"]}'

        return predictions_table_name

    def launch(self):
        _logger.info('Launching Batch ModelInferenceJob job')
        _logger.info(f'Running model-inference-batch in {self.env_vars["env"]} environment')
        ModelInference(model_uri=self._get_model_uri(),
                       input_table_name=self._get_input_table_name(),
                       output_table_name=self._get_predictions_output_params())\
            .run_and_write_batch(mode=self.conf['data_output']['mode'])
        _logger.info('Batch ModelInferenceJob job finished')


if __name__ == '__main__':
    job = ModelInferenceJob()
    job.launch()
