import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    @staticmethod
    def get_amqp_url():
        # Prioriza variável do compose, depois .env, depois default
        return os.getenv("AMQP_URL", "amqp://guest:guest@localhost:5672/")
    
    @staticmethod
    def get_exchange_name():
        return os.getenv("AMQP_EXCHANGE_NAME", "diario_oficial")
    
    @staticmethod
    def get_routing_key():
        return os.getenv("AMQP_ROUTING_KEY", "publications.new")