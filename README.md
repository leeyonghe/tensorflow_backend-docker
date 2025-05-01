<!--
# Copyright 2020-2023, NVIDIA CORPORATION & AFFILIATES. All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
#  * Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
#  * Redistributions in binary form must reproduce the above copyright
#    notice, this list of conditions and the following disclaimer in the
#    documentation and/or other materials provided with the distribution.
#  * Neither the name of NVIDIA CORPORATION nor the names of its
#    contributors may be used to endorse or promote products derived
#    from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS ``AS IS'' AND ANY
# EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR
# PURPOSE ARE DISCLAIMED.  IN NO EVENT SHALL THE COPYRIGHT OWNER OR
# CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL,
# EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO,
# PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR
# PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY
# OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
-->

[![License](https://img.shields.io/badge/License-BSD3-lightgrey.svg)](https://opensource.org/licenses/BSD-3-Clause)

# TensorFlow Backend with Docker / TensorFlow 백엔드와 Docker

> 이 프로젝트는 NVIDIA의 [Triton Inference Server](https://github.com/triton-inference-server/server)를 기반으로 하며, TensorFlow 백엔드를 Docker 환경에서 실행할 수 있도록 구성한 것입니다.
> This project is based on NVIDIA's [Triton Inference Server](https://github.com/triton-inference-server/server) and is configured to run TensorFlow backend in a Docker environment.

이 프로젝트는 TensorFlow 모델을 Triton Inference Server를 통해 서빙하는 분산 시스템을 Docker 환경에서 구성한 것입니다.

## 시스템 구성 / System Architecture

시스템은 다음과 같은 주요 컴포넌트로 구성되어 있습니다:
The system consists of the following main components:

1. **Nginx (API Gateway)**
   - 포트: 80, 443 / Ports: 80, 443
   - SSL 지원 / SSL support
   - 로드 밸런싱 기능 / Load balancing functionality

2. **Triton Inference Server Cluster (3개 노드)**
   - 각 서버는 독립적인 GPU 리소스를 사용 / Each server uses independent GPU resources
   - HTTP, gRPC, Metrics 포트 제공 / Provides HTTP, gRPC, and Metrics ports
   - 모델 자동 로드 기능 (30초 간격) / Automatic model loading (30-second interval)

3. **Monitoring Stack**
   - Prometheus: 메트릭 수집 / Metric collection
   - Grafana: 대시보드 시각화 / Dashboard visualization

4. **Model Management Service**
   - 모델 다운로드 및 배포 관리 / Model download and deployment management
   - Triton 서버와 통신하여 모델 리로드 / Communicates with Triton server for model reloading

## 환경 요구사항 / Environment Requirements

- Docker
- NVIDIA GPU 드라이버 / NVIDIA GPU driver
- NVIDIA Container Toolkit (nvidia-docker2)
- 최소 3개의 GPU (Triton 서버당 1개) / Minimum 3 GPUs (1 per Triton server)

## 설치 및 실행 / Installation and Execution

1. **환경 변수 설정 / Set Environment Variables**
```bash
export MODEL_REPOSITORY=/models
export TRITON_SERVERS=triton:8000
```

2. **Docker Compose로 실행 / Run with Docker Compose**
```bash
docker-compose up -d
```

## 서비스 포트 / Service Ports

- Nginx: 80, 443
- Triton Server 1: 8000-8002
- Triton Server 2: 8003-8005
- Triton Server 3: 8006-8008
- Prometheus: 9090
- Grafana: 3000

## 모델 관리 / Model Management

### 모델 다운로드 및 배포 / Model Download and Deployment

Model Manager 서비스는 다음과 같은 기능을 제공합니다:
The Model Manager service provides the following features:

1. **모델 다운로드 / Model Download**
   - TensorFlow 모델을 자동으로 다운로드 / Automatically downloads TensorFlow models
   - SavedModel 형식으로 저장 / Stores in SavedModel format
   - config.pbtxt 파일 자동 생성 / Automatically generates config.pbtxt file

2. **모델 배포 / Model Deployment**
   - Triton 서버에 모델 자동 배포 / Automatically deploys models to Triton server
   - 모델 변경 시 자동 리로드 / Automatic reload on model changes

### 모델 구성 / Model Configuration

각 모델은 다음 구조로 저장됩니다:
Each model is stored in the following structure:
```
/models
  └── [model_name]
      ├── 1
      │   └── model.savedmodel
      └── config.pbtxt
```

## 모니터링 / Monitoring

1. **Prometheus**
   - 메트릭 수집 및 저장 / Metric collection and storage
   - 기본 포트: 9090 / Default port: 9090

2. **Grafana**
   - 대시보드 시각화 / Dashboard visualization
   - 기본 포트: 3000 / Default port: 3000
   - 기본 로그인: admin/admin / Default login: admin/admin

## 네트워크 구성 / Network Configuration

- 모든 서비스는 `inference_network` 브릿지 네트워크를 통해 통신
  All services communicate through the `inference_network` bridge network
- 내부 통신은 서비스 이름으로 접근 가능 (예: triton:8000)
  Internal communication is accessible via service names (e.g., triton:8000)

## GPU 설정 / GPU Configuration

각 Triton 서버는 독립적인 GPU를 사용하도록 구성되어 있습니다:
Each Triton server is configured to use an independent GPU:
```yaml
deploy:
  resources:
    reservations:
      devices:
        - driver: nvidia
          count: 1
          capabilities: [gpu]
```

## 문제 해결 / Troubleshooting

1. **모델 로드 실패 / Model Load Failure**
   - Model Manager 로그 확인 / Check Model Manager logs
   - Triton 서버 로그 확인 / Check Triton server logs
   - 모델 저장소 권한 확인 / Check model repository permissions

2. **GPU 관련 문제 / GPU-related Issues**
   - NVIDIA 드라이버 버전 확인 / Check NVIDIA driver version
   - nvidia-docker2 설치 확인 / Check nvidia-docker2 installation
   - GPU 할당 확인 / Check GPU allocation

## 보안 / Security

- SSL/TLS 지원 / SSL/TLS support
- Grafana 기본 비밀번호 변경 권장 / Recommended to change default Grafana password
- 내부 네트워크 격리 / Internal network isolation

## 라이센스 / License

이 프로젝트는 MIT 라이센스 하에 배포됩니다.
This project is distributed under the MIT License.

# TensorFlow 백엔드

TensorFlow를 위한 Triton 백엔드입니다. 백엔드에 대한 자세한 내용은 [백엔드 저장소](https://github.com/triton-inference-server/backend)에서 확인할 수 있습니다. 질문이나 문제는 메인 Triton [이슈 페이지](https://github.com/triton-inference-server/server/issues)에서 할 수 있습니다.

## 자주 묻는 질문

전체 문서는 아래에 포함되어 있지만, 이러한 단축키를 통해 올바른 방향으로 시작하는 데 도움이 될 수 있습니다.

### Triton과 Triton 백엔드에 대한 일반적인 질문은 어디서 할 수 있나요?

아래의 모든 정보와 메인 [서버](https://github.com/triton-inference-server/server) 저장소에서 제공하는 [일반 Triton 문서](https://github.com/triton-inference-server/server#triton-inference-server)를 반드시 읽어보세요. 거기에서 답을 찾지 못한 경우 메인 Triton [이슈 페이지](https://github.com/triton-inference-server/server/issues)에서 질문할 수 있습니다.

### 이 백엔드에서 지원하는 TensorFlow 버전은 무엇인가요?

23.04부터 TensorFlow 백엔드는 TensorFlow 2.x만 지원합니다. 특정 릴리스에서 지원하는 버전은 메인 [서버](https://github.com/triton-inference-server/server) 저장소에서 릴리스 노트를 확인할 수 있습니다.

### TensorFlow 백엔드는 구성 가능한가요?

각 모델의 구성은 [TensorFlow 특화 최적화](https://github.com/triton-inference-server/server/blob/main/docs/user_guide/optimization.md#framework-specific-optimization)를 활성화할 수 있습니다. 또한 Triton을 시작할 때 백엔드를 구성하는 데 사용할 수 있는 몇 가지 [명령줄 옵션](#command-line-options)도 있습니다.

### TensorFlow 백엔드를 어떻게 빌드하나요?

아래의 [빌드 지침](#build-the-tensorflow-backend)을 참조하세요.

### 백엔드를 빌드할 때 어떤 버전의 TensorFlow를 사용할 수 있나요?

현재 [NGC](https://ngc.nvidia.com)의 TensorFlow 버전을 사용해야 합니다. 아래의 [사용자 정의 TensorFlow 빌드 지침](#build-the-tensorflow-backend-with-custom-tensorflow)을 참조하세요.

### TensorFlow 백엔드는 GPU 메모리를 어떻게 관리하나요?

TensorFlow 백엔드는 Triton 프로세스가 종료될 때까지 GPU 메모리를 "해제"하지 않습니다. TensorFlow는 풀 할당자를 사용하므로 할당한 메모리를 자신의 프로세스가 종료될 때까지 유지합니다. 다른 TensorFlow 모델을 로드하면 해당 메모리를 재사용하지만, 더 이상 사용하지 않더라도 시스템에 반환하지 않습니다. 이러한 이유로, TensorFlow 모델을 반복적으로 로드/언로드할 경우 같은 Triton 프로세스에서 그룹화하는 것이 좋습니다.

TensorFlow GPU 문서에서: "[메모리 단편화를 유발할 수 있으므로 메모리가 해제되지 않습니다](https://www.tensorflow.org/guide/gpu#limiting_gpu_memory_growth)".

#### 해결 방법

TensorFlow가 할당할 수 있는 총 메모리 양을 제한하기 위한 몇 가지 옵션이 있습니다:

1. [여기](https://github.com/triton-inference-server/tensorflow_backend#--backend-configtensorflowgpu-memory-fractionfloat)에서 설명한 대로 `gpu-memory-fraction`을 사용할 수 있습니다. 이는 프로세스에 대해 TensorFlow가 할당할 수 있는 총 메모리의 상한을 제한합니다. 그러나 이 옵션을 사용할 때 allow-growth가 false로 설정되므로, TF가 실행에 필요한 메모리를 할당할 수 있는 것보다 더 많이 할당해야 하는 경우 TF 모델 실행이 여전히 실패할 수 있습니다.

2. 동시 TensorFlow 실행으로 인한 메모리 증가를 제한하기 위해 Triton의 [속도 제한기](https://github.com/triton-inference-server/server/blob/main/docs/user_guide/rate_limiter.md)를 사용하여 실행에 허용되는 요청 수를 제한할 수도 있습니다.

## 자동 완성 모델 구성

Triton이 `--disable-auto-complete-config` 명령줄 옵션으로 시작되지 않은 경우, TensorFlow 백엔드는 TensorFlow SavedModel에서 사용 가능한 메타데이터를 사용하여 모델의 config.pbtxt에서 필수 필드를 채웁니다. Triton의 자동 완성 모델 구성 지원에 대한 자세한 내용은 [여기](https://github.com/triton-inference-server/server/blob/main/docs/user_guide/model_configuration.md#auto-generated-model-configuration)에서 확인할 수 있습니다.

그러나 Graphdef 형식에서는 모델이 충분한 메타데이터를 포함하지 않으므로 Triton이 모델 구성을 생성할 수 없습니다. 결과적으로, 이러한 모델에 대해 config.pbtxt를 명시적으로 제공해야 합니다.

TensorFlow 백엔드는 모델 구성에서 다음 필드를 완성할 수 있습니다:

### max_batch_size

max_batch_size의 자동 완성은 다음 규칙을 따릅니다:

1. 자동 완성이 모델이 요청 배치를 처리할 수 있음을 확인했습니다.
2. 모델 구성에서 max_batch_size가 0이거나 max_batch_size가 모델 구성에서 누락되었습니다.

위의 두 규칙이 충족되면 max_batch_size는 [default-max-batch-size](#--backend-config=tensorflow,default-max-batch-size=\<int\>)로 설정됩니다. 그렇지 않으면 max_batch_size는 0으로 설정됩니다.

### 입력 및 출력

TensorFlow 백엔드는 모델에서 이 정보를 사용할 수 있는 경우 `name`, `data_type`, `dims`를 채울 수 있습니다. 알려진 제한 사항은 [`ragged_batching`](https://github.com/triton-inference-server/server/blob/main/docs/user_guide/ragged_batching.md#batch-input) 및 [`sequence_batching`](https://github.com/triton-inference-server/server/blob/main/docs/user_guide/model_configuration.md#sequence-batcher) 필드에 정의된 입력입니다. 모델에 백엔드가 이를 자동 완성할 수 있는 충분한 정보가 없습니다. 또한 백엔드는 스칼라 텐서에 대한 구성을 자동 완성할 수 없습니다.

출력 자동 완성은 다음 규칙을 따릅니다:
- 모델 구성에서 `outputs`가 비어 있거나 정의되지 않은 경우, savedmodel의 모든 출력이 자동 완성됩니다.
- 하나 이상의 출력이 `outputs`에 정의된 경우, 정의된 출력은 자동 완성되고 누락된 출력은 무시됩니다.

### 동적 배치

max_batch_size > 1이고 [스케줄러](https://github.com/triton-inference-server/server/blob/main/docs/user_guide/model_configuration.md#scheduling-and-batching)가 제공되지 않은 경우, 기본 설정으로 동적 배치 스케줄러가 활성화됩니다.

## 명령줄 옵션

명령줄 옵션은 백엔드를 사용하는 모든 모델에 적용되는 TensorFlow 백엔드의 속성을 구성합니다.

##### --backend-config=tensorflow,allow-soft-placement=\<boolean\>

GPU 구현을 사용할 수 없을 때 TensorFlow가 작업의 CPU 구현을 사용하도록 지시합니다.

##### --backend-config=tensorflow,gpu-memory-fraction=\<float\>

TensorFlow 모델을 위한 GPU 메모리의 일부를 예약합니다. 기본값 0.0은 TensorFlow가 필요에 따라 동적으로 메모리를 할당해야 함을 나타냅니다. 값 1.0은 TensorFlow가 GPU 메모리의 전부를 할당해야 함을 나타냅니다.

##### --backend-config=tensorflow,version=\<int\>

사용할 TensorFlow 라이브러리의 버전을 선택합니다. 기본 버전은 2입니다. 23.04 릴리스부터 TensorFlow 백엔드는 TensorFlow 2만 지원합니다. 23.04 이전의 Triton에서 TensorFlow 1을 사용하려면 이 명령줄 옵션을 사용하여 버전을 1로 지정할 수 있습니다.

##### --backend-config=tensorflow,default-max-batch-size=\<int\>

모델에서 배치 지원이 감지될 때 [자동 완성 모델 구성](https://github.com/triton-inference-server/server/blob/main/docs/user_guide/model_configuration.md#auto-generated-model-configuration) 중에 max_batch_size에 사용할 기본값입니다. 명시적으로 제공되지 않은 경우 이 옵션의 기본값은 4입니다.

## TensorFlow 백엔드 빌드

최신 cmake를 사용하여 빌드합니다. 먼저 필요한 종속성을 설치합니다.

```
$ apt-get install rapidjson-dev python3-pip
$ pip3 install patchelf==0.17.2
```

백엔드는 TensorFlow 2.x를 지원하도록 빌드할 수 있습니다. 23.04부터 Triton은 더 이상 TensorFlow 1.x를 지원하지 않으며 TensorFlow 2.x만 사용합니다. [NGC](https://ngc.nvidia.com)의 적절한 TensorFlow 컨테이너를 사용해야 합니다. 예를 들어, NGC의 23.04 버전의 TensorFlow 2.x 컨테이너를 사용하는 백엔드를 빌드하려면:

```
$ mkdir build
$ cd build
$ cmake -DCMAKE_INSTALL_PREFIX:PATH=`pwd`/install -DTRITON_TENSORFLOW_DOCKER_IMAGE="nvcr.io/nvidia/tensorflow:23.04-tf2-py3" ..
$ make install
```

다음 필수 Triton 저장소가 빌드에 사용됩니다. 기본적으로 각 저장소에 대해 "main" 브랜치/태그가 사용되지만 나열된 CMake 인수를 사용하여 재정의할 수 있습니다.

* triton-inference-server/backend: -DTRITON_BACKEND_REPO_TAG=[tag]
* triton-inference-server/core: -DTRITON_CORE_REPO_TAG=[tag]
* triton-inference-server/common: -DTRITON_COMMON_REPO_TAG=[tag]

## 사용자 정의 TensorFlow로 TensorFlow 백엔드 빌드

현재 Triton은 TensorFlow 백엔드와 함께 특별히 패치된 버전의 TensorFlow를 사용해야 합니다. 이러한 TensorFlow 버전의 전체 소스는 [NGC](https://ngc.nvidia.com)에서 Docker 이미지로 사용할 수 있습니다. 예를 들어, Triton의 23.04 릴리스와 호환되는 TensorFlow 2.x 버전은 nvcr.io/nvidia/tensorflow:23.04-tf2-py3로 사용할 수 있습니다.

이러한 이미지 내에서 TensorFlow를 수정하고 재빌드하여 Triton TensorFlow 백엔드에 필요한 공유 라이브러리를 생성할 수 있습니다. TensorFlow 2.x 컨테이너에서 다음을 사용하여 재빌드합니다:

```
$ /opt/tensorflow/nvbuild.sh
```

컨테이너 내에서 재빌드한 후 업데이트된 컨테이너를 새로운 Docker 이미지로 저장해야 합니다(예: *docker commit* 사용). 그런 다음 [위](#build-the-tensorflow-backend)에서 설명한 대로 TRITON_TENSORFLOW_DOCKER_IMAGE를 새 Docker 이미지를 참조하도록 설정하여 백엔드를 빌드합니다.

## TensorFlow 백엔드 사용
### 플랫폼

TensorFlow는 GraphDef와 SavedModel 두 가지 모델 형식을 인식합니다. 모델 형식을 구분하기 위해 모델의 `config.pbtxt` 파일에서 적절한 `platform`을 지정합니다:

```
# Graphdef 형식의 config.pbtxt
...
platform: "tensorflow_graphdef"
...
```
또는
```
# SavedModel 형식의 config.pbtxt
...
platform: "tensorflow_savedmodel"
...
```

### 매개변수

모델의 TensorFlow 구성은 모델의 `config.pbtxt` 파일의 Parameters 섹션을 통해 수행됩니다. 매개변수와 그 설명은 다음과 같습니다.

* `TF_NUM_INTRA_THREADS`: 개별 작업의 실행을 병렬화하는 데 사용할 스레드 수입니다. 기본적으로 자동 구성됩니다. [여기](https://github.com/tensorflow/tensorflow/blob/6f72753a66d6abab8b839cc263a9f1329861f6f9/tensorflow/core/protobuf/config.proto#L393)의 protobuf를 참조하세요. 음수가 아닌 숫자여야 합니다.
* `TF_NUM_INTER_THREADS`: 동시에 실행할 수 있는 연산자의 수를 제어합니다. 기본적으로 자동 구성됩니다. [여기](https://github.com/tensorflow/tensorflow/blob/6f72753a66d6abab8b839cc263a9f1329861f6f9/tensorflow/core/protobuf/config.proto#L404)의 protobuf를 참조하세요.
* `TF_USE_PER_SESSION_THREADS`: 세션별 스레드 사용 여부를 나타내는 부울 값입니다. "True", "On", "1"이 true로 인식됩니다.
* `TF_GRAPH_TAG`: 사용할 그래프의 태그입니다. [여기](https://github.com/tensorflow/tensorflow/blob/6f72753a66d6abab8b839cc263a9f1329861f6f9/tensorflow/core/protobuf/meta_graph.proto#L56)의 protobuf를 참조하세요.
* `TF_SIGNATURE_DEF`: 사용할 시그니처 정의입니다. [여기](https://github.com/tensorflow/tensorflow/blob/6f72753a66d6abab8b839cc263a9f1329861f6f9/tensorflow/core/protobuf/meta_graph.proto#L260-L331)의 protobuf를 참조하세요.
* `MAX_SESSION_SHARE_COUNT`: 이 매개변수는 [모델 인스턴스](https://github.com/triton-inference-server/server/blob/main/docs/user_guide/model_configuration.md#instance-groups)가 [TF 세션](https://github.com/tensorflow/tensorflow/blob/master/tensorflow/core/public/session.h)을 공유할 수 있는 최대 수를 지정합니다. 기본값은 1이며, 이는 Triton이 각 모델 인스턴스에 대해 별도의 TF 세션을 생성함을 의미합니다. 이 매개변수가 인스턴스의 총 수로 설정되면 Triton은 단일 TF 세션만 생성하며 이 세션은 모든 인스턴스에서 공유됩니다. 모델 인스턴스 간에 TF 세션을 공유하면 모델 로드 및 실행의 메모리 사용량을 줄일 수 있습니다.
* `TF_INIT_OPS_FILE`: 이 매개변수는 [초기화 작업](https://www.tensorflow.org/api_docs/python/tf/compat/v1/global_variables_initializer)을 포함하는 JSON 형식의 파일 이름을 지정합니다. JSON 파일은 초기화 작업 목록을 설명하는 'init_ops'라는 단일 요소를 가져야 합니다. 이 파일은 모델 버전 폴더나 모델 디렉토리에 저장할 수 있습니다. 두 위치 모두에 제공된 경우 모델 버전 폴더의 파일이 모델 폴더의 파일보다 우선합니다. 모델 버전 폴더에 제공된 경우 디렉토리 구조는 다음과 같아야 합니다:

```
|-- 1
|   |-- model.graphdef
|   `-- init_ops.json
`-- config.pbtxt
```

`init_ops.json` 파일의 내용 예시는 다음과 같습니다:

```json
{
    "init_ops": ["init"]
}
```

이러한 매개변수를 지정하는 모델 구성 파일의 섹션은 다음과 같습니다:

```
parameters: {
  key: "TF_NUM_INTRA_THREADS"
  value: {
    string_value:"2"
  }
}

parameters: {
  key: "TF_USE_PER_SESSION_THREADS"
  value: {
    string_value:"yes"
  }
}

parameters: {
  key: "TF_GRAPH_TAG"
  value: {
    string_value: "serve1"
  }
}

parameters: {
  key: "TF_INIT_OPS_FILE"
  value: {
    string_value: "init_ops.json"
  }
}

parameters: {
  key: "TF_SIGNATURE_DEF"
  value: {
    string_value: "serving2"
  }
}
```

## 중요 참고사항
* SavedModel 형식에서 모델 로드 및 언로드 중에 메모리 증가 문제를 관찰했습니다. 이는 실제 메모리 누수가 아닐 수 있으며, 시스템의 malloc 휴리스틱으로 인해 메모리가 운영 체제에 즉시 반환되지 않는 결과일 수 있습니다. 기본 malloc 라이브러리를 [tcmalloc](https://github.com/google/tcmalloc) 또는 [jemalloc](https://github.com/jemalloc/jemalloc)로 교체하면 메모리 사용량이 개선되는 것을 확인했습니다. tcmalloc 또는 jemalloc을 Triton과 함께 사용하는 방법에 대한 지침은 [문서](https://github.com/triton-inference-server/server/blob/main/docs/user_guide/model_management.md#model-control-mode-explicit)를 참조하세요.