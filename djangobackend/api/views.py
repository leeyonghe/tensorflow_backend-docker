from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.conf import settings
import weaviate
from typing import Optional, Dict, Any, List

class VectorDBView(APIView):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.client = settings.WEAVIATE_CLIENT
        
    def _create_schema_if_not_exists(self):
        """Weaviate 스키마가 없는 경우 생성"""
        try:
            class_obj = {
                "class": "Document",
                "vectorizer": "none",  # 벡터는 직접 제공
                "properties": [
                    {
                        "name": "content",
                        "dataType": ["text"],
                    },
                    {
                        "name": "metadata",
                        "dataType": ["object"],
                    }
                ]
            }
            
            if not self.client.schema.exists("Document"):
                self.client.schema.create_class(class_obj)
        except Exception as e:
            print(f"Schema creation error: {e}")

    def post(self, request) -> Response:
        """벡터 데이터 저장"""
        try:
            self._create_schema_if_not_exists()
            
            data = request.data
            content = data.get('content')
            vector = data.get('vector')
            metadata = data.get('metadata', {})
            
            if not content or not vector:
                return Response(
                    {"error": "content and vector are required"},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # Weaviate에 데이터 저장
            data_object = {
                "content": content,
                "metadata": metadata
            }
            
            self.client.data_object.create(
                data_object=data_object,
                class_name="Document",
                vector=vector
            )
            
            return Response({"message": "Data stored successfully"}, status=status.HTTP_201_CREATED)
            
        except Exception as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def get(self, request) -> Response:
        """벡터 유사도 검색"""
        try:
            vector = request.query_params.get('vector')
            limit = int(request.query_params.get('limit', 10))
            
            if not vector:
                return Response(
                    {"error": "vector parameter is required"},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # 벡터를 float 리스트로 변환
            vector = [float(x) for x in vector.split(',')]
            
            # 벡터 기반 유사도 검색
            result = (
                self.client.query
                .get("Document", ["content", "metadata"])
                .with_near_vector({
                    "vector": vector,
                    "certainty": 0.7
                })
                .with_limit(limit)
                .do()
            )
            
            return Response(result, status=status.HTTP_200_OK)
            
        except Exception as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class HealthCheckView(APIView):
    """서비스 상태 확인 API"""
    def get(self, request) -> Response:
        return Response({"status": "healthy"}, status=status.HTTP_200_OK) 