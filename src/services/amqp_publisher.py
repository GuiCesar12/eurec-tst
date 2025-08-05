import json
import uuid
import time
from typing import Dict, Any
from pika.exceptions import AMQPError
from utils.config import Config
import pika

class AmqpPublisher:
    def __init__(self):
        self.amqp_url = Config.get_amqp_url()
        self.exchange_name = Config.get_exchange_name()
        self.routing_key = Config.get_routing_key()
        self.connection = None
        self.channel = None

    def _ensure_connection(self):
        """Estabelece conexão com o servidor AMQP"""
        if not self.connection or self.connection.is_closed:
            self.connection = pika.BlockingConnection(
                pika.URLParameters(self.amqp_url)
            )
            self.channel = self.connection.channel()
            self.channel.exchange_declare(
                exchange=self.exchange_name,
                exchange_type='topic',
                durable=True
            )

    def _validate_message(self, message: Dict[str, Any]) -> Dict[str, Any]:
        """Valida e padroniza a estrutura da mensagem"""
        if not isinstance(message, dict):
            raise ValueError("Message must be a dictionary")
        
        # Garante que existe um ID na mensagem
        message['id'] = message.get('id') or str(uuid.uuid4())
        
        # Adiciona metadados padrão
        message.setdefault('metadata', {
            'version': '1.0',
            'source': 'diario-oficial-api'
        })
        
        return message

    def publish(self, message: Dict[str, Any]):
        """
        Publica uma mensagem no broker AMQP
        
        Args:
            message: Dicionário com os dados da publicação
                    Deve conter pelo menos um campo 'id'
        
        Raises:
            ValueError: Se a mensagem for inválida
            Exception: Se ocorrer erro na publicação
        """
        try:
            self._ensure_connection()
            validated_msg = self._validate_message(message)
            message_body = json.dumps(validated_msg)
            
            self.channel.basic_publish(
                exchange=self.exchange_name,
                routing_key=self.routing_key,
                body=message_body,
                properties=pika.BasicProperties(
                    delivery_mode=2,  # Persistente
                    content_type='application/json',
                    message_id=validated_msg['id'],
                    timestamp=int(time.time())
                )
            )
        except json.JSONEncodeError as e:
            raise ValueError(f"Invalid message format: {str(e)}")
        except AMQPError as e:
            raise Exception(f"AMQP publishing error: {str(e)}")
        except Exception as e:
            raise Exception(f"Unexpected error: {str(e)}")

    def close(self):
        """Fecha a conexão com o broker"""
        try:
            if self.connection and not self.connection.is_closed:
                self.connection.close()
        except Exception:
            pass

    def __enter__(self):
        self._ensure_connection()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()