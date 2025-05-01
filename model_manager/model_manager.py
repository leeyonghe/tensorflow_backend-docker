import os
import shutil
import requests
import tensorflow as tf
from pathlib import Path
import logging

# 로깅 설정 - Docker 환경에 맞게 수정
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class ModelManager:
    def __init__(self, model_repository, triton_servers):
        # Docker 환경에서 절대 경로 사용
        self.model_repository = Path(model_repository)
        self.triton_servers = triton_servers.split(',')
        logger.info(f"Model repository: {self.model_repository}")
        logger.info(f"Triton servers: {self.triton_servers}")
        
    def download_model(self, model_name, version="1"):
        """TensorFlow 모델 다운로드 및 설정"""
        try:
            model_path = self.model_repository / model_name / version
            model_path.mkdir(parents=True, exist_ok=True)
            
            logger.info(f"Downloading model {model_name} version {version}")
            
            # MobileNetV2 모델 다운로드 및 저장
            model = tf.keras.Sequential([
                tf.keras.layers.Input(shape=(224, 224, 3)),
                tf.keras.applications.MobileNetV2(weights='imagenet')
            ])
            
            # SavedModel 형식으로 저장
            tf.saved_model.save(model, str(model_path / "model.savedmodel"))
            logger.info(f"Model saved to {model_path}")
            
            # config.pbtxt 생성
            self._create_config(model_name)
            logger.info(f"Config file created for {model_name}")
            
            return True
        except Exception as e:
            logger.error(f"Error downloading model: {e}")
            return False
        
    def _create_config(self, model_name):
        """config.pbtxt 파일 생성"""
        config_path = self.model_repository / model_name / "config.pbtxt"
        config_content = f"""
name: "{model_name}"
platform: "tensorflow_savedmodel"
max_batch_size: 32
dynamic_batching {{
  preferred_batch_size: [8, 16, 32]
  max_queue_delay_microseconds: 1000
}}
input [
  {{
    name: "input_1"
    data_type: TYPE_FP32
    dims: [224, 224, 3]
  }}
]
output [
  {{
    name: "output_1"
    data_type: TYPE_FP32
    dims: [1000]
  }}
]
"""
        config_path.write_text(config_content)
        
    def reload_models(self):
        """모든 Triton 서버에 모델 리로드 요청"""
        for server in self.triton_servers:
            try:
                response = requests.post(f"http://{server}/v2/repository/index")
                logger.info(f"Model reload requested on {server}")
            except Exception as e:
                logger.error(f"Error reloading models on {server}: {e}")

def main():
    # Docker 환경 변수에서 설정 가져오기
    model_repository = os.getenv("MODEL_REPOSITORY", "/models")
    triton_servers = os.getenv("TRITON_SERVERS", "triton:8000")  # Docker 서비스 이름 사용
    
    # ModelManager 인스턴스 생성
    model_manager = ModelManager(model_repository, triton_servers)
    
    # MobileNetV2 모델 다운로드
    model_manager.download_model("mobilenet_v2")
    
    # 모델 리로드
    model_manager.reload_models()

if __name__ == "__main__":
    main() 