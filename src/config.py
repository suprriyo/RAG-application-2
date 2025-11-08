"""Configuration management for RAG QA System."""

import os
import yaml
from typing import Dict, Any, Optional
from dotenv import load_dotenv


class ConfigError(Exception):

    pass


class Config:
 
   
    DEFAULTS = {
        'embedding': {
            'provider': 'openai',
            'model': 'text-embedding-ada-002'
        },
        'llm': {
            'provider': 'openai',
            'model': 'gpt-3.5-turbo',
            'temperature': 0.7,
            'max_tokens': 500
        },
        'chunking': {
            'chunk_size': 1000,
            'chunk_overlap': 200
        },
        'retrieval': {
            'top_k': 4,
            'score_threshold': 0.7
        },
        'storage': {
            'persist_directory': './data/chroma_db',
            'collection_name': 'educational_docs'
        }
    }
    
    def __init__(self, config_path: str = 'config.yaml', load_env: bool = True):
      
        self.config_path = config_path
        self._config: Dict[str, Any] = {}
        
        
        if load_env:
            load_dotenv()
        
     
        self._load_config()
        self._validate_config()
    
    def _load_config(self) -> None:
       
        self._config = self._deep_copy_dict(self.DEFAULTS)
        
       
        if os.path.exists(self.config_path):
            try:
                with open(self.config_path, 'r') as f:
                    yaml_config = yaml.safe_load(f) or {}
                   
                    self._config = self._merge_dicts(self._config, yaml_config)
            except Exception as e:
                print(f"Warning: Failed to load config file '{self.config_path}': {e}")
                print("Using default configuration values.")
        else:
            print(f"Warning: Config file '{self.config_path}' not found. Using defaults.")
    
    def _validate_config(self) -> None:
      
        
        embedding_provider = self.get('embedding.provider', 'openai')
        llm_provider = self.get('llm.provider', 'openai')
        
      
        if embedding_provider == 'openai':
            if not os.getenv('OPENAI_API_KEY'):
                raise ConfigError(
                    "Missing required API key: OPENAI_API_KEY\n"
                    "Please set it in your .env file or environment variables."
                )
        elif embedding_provider == 'huggingface':
           
            pass
        else:
            print(f"Warning: Unknown embedding provider '{embedding_provider}'")
        
      
        if llm_provider == 'openai':
            if not os.getenv('OPENAI_API_KEY'):
                raise ConfigError(
                    "Missing required API key: OPENAI_API_KEY\n"
                    "Please set it in your .env file or environment variables."
                )
        elif llm_provider == 'anthropic':
            if not os.getenv('ANTHROPIC_API_KEY'):
                raise ConfigError(
                    "Missing required API key: ANTHROPIC_API_KEY\n"
                    "Please set it in your .env file or environment variables."
                )
        else:
            print(f"Warning: Unknown LLM provider '{llm_provider}'")
        
       
        chunk_size = self.get('chunking.chunk_size')
        if not isinstance(chunk_size, int) or chunk_size <= 0:
            raise ConfigError(f"Invalid chunk_size: {chunk_size}. Must be a positive integer.")
        
        chunk_overlap = self.get('chunking.chunk_overlap')
        if not isinstance(chunk_overlap, int) or chunk_overlap < 0:
            raise ConfigError(f"Invalid chunk_overlap: {chunk_overlap}. Must be a non-negative integer.")
        
        if chunk_overlap >= chunk_size:
            raise ConfigError(
                f"chunk_overlap ({chunk_overlap}) must be less than chunk_size ({chunk_size})"
            )
        
        top_k = self.get('retrieval.top_k')
        if not isinstance(top_k, int) or top_k <= 0:
            raise ConfigError(f"Invalid top_k: {top_k}. Must be a positive integer.")
    
    def get(self, key: str, default: Any = None) -> Any:
       
        keys = key.split('.')
        value = self._config
        
        for k in keys:
            if isinstance(value, dict) and k in value:
                value = value[k]
            else:
                return default
        
        return value
    
    def get_section(self, section: str) -> Dict[str, Any]:
   
        return self._config.get(section, {})
    
    def to_dict(self) -> Dict[str, Any]:
        
        return self._deep_copy_dict(self._config)
    
    @staticmethod
    def _deep_copy_dict(d: Dict[str, Any]) -> Dict[str, Any]:
        """Deep copy a dictionary."""
        import copy
        return copy.deepcopy(d)
    
    @staticmethod
    def _merge_dicts(base: Dict[str, Any], override: Dict[str, Any]) -> Dict[str, Any]:
        
        result = base.copy()
        
        for key, value in override.items():
            if key in result and isinstance(result[key], dict) and isinstance(value, dict):
                result[key] = Config._merge_dicts(result[key], value)
            else:
                result[key] = value
        
        return result
