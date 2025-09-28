# tests/test_url_parser_comprehensive.py
"""
Comprehensive tests for URL parser to improve coverage
"""

import pytest
from unittest.mock import Mock, patch
from src.url_parser import URLParser


class TestURLParserComprehensive:
    """Comprehensive tests for URL parser"""
    
    def test_url_parser_initialization(self):
        """Test URL parser initialization"""
        parser = URLParser()
        assert parser is not None
        assert hasattr(parser, 'identify_url_type')
        assert hasattr(parser, 'parse_model_url')
    
    def test_identify_model_url_variations(self):
        """Test identifying various model URL formats"""
        parser = URLParser()
        
        # Test different model URL formats
        model_urls = [
            "https://huggingface.co/google/gemma-3-270m",
            "https://huggingface.co/google/gemma-3-270m/tree/main",
            "https://huggingface.co/microsoft/DialoGPT-medium",
            "https://huggingface.co/facebook/opt-125m",
            "https://huggingface.co/runwayml/stable-diffusion-v1-5"
        ]
        
        for url in model_urls:
            url_type = parser.identify_url_type(url)
            assert url_type == "MODEL"
    
    def test_identify_dataset_url_variations(self):
        """Test identifying various dataset URL formats"""
        parser = URLParser()
        
        # Test different dataset URL formats
        dataset_urls = [
            "https://huggingface.co/datasets/xlangai/AgentNet",
            "https://huggingface.co/datasets/squad",
            "https://huggingface.co/datasets/glue",
            "https://huggingface.co/datasets/wikipedia"
        ]
        
        for url in dataset_urls:
            url_type = parser.identify_url_type(url)
            assert url_type == "DATASET"
    
    def test_identify_code_url_variations(self):
        """Test identifying various code URL formats"""
        parser = URLParser()
        
        # Test different code URL formats
        code_urls = [
            "https://github.com/SkyworkAI/Matrix-Game",
            "https://github.com/huggingface/transformers",
            "https://github.com/microsoft/DialoGPT",
            "https://gitlab.com/example/repo"
        ]
        
        for url in code_urls:
            url_type = parser.identify_url_type(url)
            assert url_type == "CODE"
    
    def test_identify_invalid_urls(self):
        """Test identifying invalid URLs"""
        parser = URLParser()
        
        invalid_urls = [
            "not-a-url",
            "ftp://example.com",
            "http://example.com",
            "https://example.com/not-huggingface",
            "",
            None
        ]
        
        for url in invalid_urls:
            url_type = parser.identify_url_type(url)
            assert url_type == "UNKNOWN"
    
    def test_parse_model_url_basic(self):
        """Test parsing basic model URL"""
        parser = URLParser()
        
        url = "https://huggingface.co/google/gemma-3-270m"
        model_info = parser.parse_model_url(url)
        
        assert model_info is not None
        assert model_info.name == "google/gemma-3-270m"
        assert model_info.api_data is not None
    
    def test_parse_model_url_with_tree(self):
        """Test parsing model URL with tree path"""
        parser = URLParser()
        
        url = "https://huggingface.co/microsoft/DialoGPT-medium/tree/main"
        model_info = parser.parse_model_url(url)
        
        assert model_info is not None
        assert model_info.name == "microsoft/DialoGPT-medium"
    
    def test_parse_model_url_with_api_data(self):
        """Test parsing model URL with API data"""
        parser = URLParser()
        
        with patch('src.url_parser.requests.get') as mock_get:
            # Mock API response
            mock_response = Mock()
            mock_response.status_code = 200
            mock_response.json.return_value = {
                'id': 'google/gemma-3-270m',
                'downloads': 1000,
                'likes': 100,
                'tags': ['text-generation'],
                'license': 'apache-2.0',
                'lastModified': '2024-01-01T00:00:00Z'
            }
            mock_get.return_value = mock_response
            
            url = "https://huggingface.co/google/gemma-3-270m"
            model_info = parser.parse_model_url(url)
            
            assert model_info is not None
            assert model_info.name == "google/gemma-3-270m"
            assert model_info.downloads == 1000
            assert model_info.likes == 100
            assert model_info.tags == ['text-generation']
    
    def test_parse_model_url_api_failure(self):
        """Test parsing model URL when API fails"""
        parser = URLParser()
        
        with patch('src.url_parser.requests.get') as mock_get:
            # Mock API failure
            mock_response = Mock()
            mock_response.status_code = 404
            mock_get.return_value = mock_response
            
            url = "https://huggingface.co/nonexistent/model"
            model_info = parser.parse_model_url(url)
            
            # Should still return a model info with basic data
            assert model_info is not None
            assert model_info.name == "nonexistent/model"
    
    def test_parse_model_url_network_error(self):
        """Test parsing model URL with network error"""
        parser = URLParser()
        
        with patch('src.url_parser.requests.get') as mock_get:
            mock_get.side_effect = Exception("Network error")
            
            url = "https://huggingface.co/test/model"
            model_info = parser.parse_model_url(url)
            
            # Should handle error gracefully
            assert model_info is not None
            assert model_info.name == "test/model"
    
    def test_parse_model_url_invalid_url(self):
        """Test parsing invalid model URL"""
        parser = URLParser()
        
        invalid_urls = [
            "not-a-url",
            "https://example.com/not-huggingface",
            "",
            None
        ]
        
        for url in invalid_urls:
            model_info = parser.parse_model_url(url)
            assert model_info is None
    
    def test_extract_model_name_from_url(self):
        """Test extracting model name from URL"""
        parser = URLParser()
        
        test_cases = [
            ("https://huggingface.co/google/gemma-3-270m", "google/gemma-3-270m"),
            ("https://huggingface.co/microsoft/DialoGPT-medium/tree/main", "microsoft/DialoGPT-medium"),
            ("https://huggingface.co/facebook/opt-125m", "facebook/opt-125m"),
            ("https://huggingface.co/runwayml/stable-diffusion-v1-5", "runwayml/stable-diffusion-v1-5")
        ]
        
        for url, expected_name in test_cases:
            name = parser._extract_model_name_from_url(url)
            assert name == expected_name
    
    def test_extract_model_name_invalid_url(self):
        """Test extracting model name from invalid URL"""
        parser = URLParser()
        
        invalid_urls = [
            "not-a-url",
            "https://example.com/not-huggingface",
            "",
            None
        ]
        
        for url in invalid_urls:
            name = parser._extract_model_name_from_url(url)
            assert name is None
    
    def test_fetch_model_api_data_success(self):
        """Test successful API data fetching"""
        parser = URLParser()
        
        with patch('src.url_parser.requests.get') as mock_get:
            mock_response = Mock()
            mock_response.status_code = 200
            mock_response.json.return_value = {
                'id': 'test/model',
                'downloads': 500,
                'likes': 50,
                'tags': ['test'],
                'license': 'mit'
            }
            mock_get.return_value = mock_response
            
            api_data = parser._fetch_model_api_data("test/model")
            assert api_data is not None
            assert api_data['id'] == 'test/model'
            assert api_data['downloads'] == 500
    
    def test_fetch_model_api_data_failure(self):
        """Test API data fetching failure"""
        parser = URLParser()
        
        with patch('src.url_parser.requests.get') as mock_get:
            mock_response = Mock()
            mock_response.status_code = 404
            mock_get.return_value = mock_response
            
            api_data = parser._fetch_model_api_data("nonexistent/model")
            assert api_data is None
    
    def test_fetch_model_api_data_network_error(self):
        """Test API data fetching with network error"""
        parser = URLParser()
        
        with patch('src.url_parser.requests.get') as mock_get:
            mock_get.side_effect = Exception("Network error")
            
            api_data = parser._fetch_model_api_data("test/model")
            assert api_data is None
    
    def test_fetch_model_index_success(self):
        """Test successful model index fetching"""
        parser = URLParser()
        
        with patch('src.url_parser.requests.get') as mock_get:
            mock_response = Mock()
            mock_response.status_code = 200
            mock_response.json.return_value = [
                {
                    'results': [
                        {
                            'metrics': ['accuracy', 'bleu']
                        }
                    ]
                }
            ]
            mock_get.return_value = mock_response
            
            model_index = parser._fetch_model_index("test/model")
            assert model_index is not None
            assert isinstance(model_index, list)
            assert len(model_index) > 0
    
    def test_fetch_model_index_failure(self):
        """Test model index fetching failure"""
        parser = URLParser()
        
        with patch('src.url_parser.requests.get') as mock_get:
            mock_response = Mock()
            mock_response.status_code = 404
            mock_get.return_value = mock_response
            
            model_index = parser._fetch_model_index("nonexistent/model")
            assert model_index is None
    
    def test_fetch_model_index_network_error(self):
        """Test model index fetching with network error"""
        parser = URLParser()
        
        with patch('src.url_parser.requests.get') as mock_get:
            mock_get.side_effect = Exception("Network error")
            
            model_index = parser._fetch_model_index("test/model")
            assert model_index is None
    
    def test_parse_model_url_with_model_index(self):
        """Test parsing model URL with model index"""
        parser = URLParser()
        
        with patch('src.url_parser.requests.get') as mock_get:
            # Mock API response
            api_response = Mock()
            api_response.status_code = 200
            api_response.json.return_value = {
                'id': 'test/model',
                'downloads': 1000,
                'likes': 100,
                'tags': ['text-generation'],
                'license': 'apache-2.0'
            }
            
            # Mock model index response
            index_response = Mock()
            index_response.status_code = 200
            index_response.json.return_value = [
                {
                    'results': [
                        {
                            'metrics': ['accuracy', 'bleu']
                        }
                    ]
                }
            ]
            
            mock_get.side_effect = [api_response, index_response]
            
            url = "https://huggingface.co/test/model"
            model_info = parser.parse_model_url(url)
            
            assert model_info is not None
            assert model_info.name == "test/model"
            assert model_info.model_index is not None
            assert len(model_info.model_index) > 0
    
    def test_parse_model_url_timeout(self):
        """Test parsing model URL with timeout"""
        parser = URLParser()
        
        with patch('src.url_parser.requests.get') as mock_get:
            mock_get.side_effect = Exception("Timeout")
            
            url = "https://huggingface.co/test/model"
            model_info = parser.parse_model_url(url)
            
            # Should handle timeout gracefully
            assert model_info is not None
            assert model_info.name == "test/model"
    
    def test_parse_model_url_json_error(self):
        """Test parsing model URL with JSON error"""
        parser = URLParser()
        
        with patch('src.url_parser.requests.get') as mock_get:
            mock_response = Mock()
            mock_response.status_code = 200
            mock_response.json.side_effect = ValueError("Invalid JSON")
            mock_get.return_value = mock_response
            
            url = "https://huggingface.co/test/model"
            model_info = parser.parse_model_url(url)
            
            # Should handle JSON error gracefully
            assert model_info is not None
            assert model_info.name == "test/model"
    
    def test_parse_model_url_partial_data(self):
        """Test parsing model URL with partial data"""
        parser = URLParser()
        
        with patch('src.url_parser.requests.get') as mock_get:
            # Mock partial API response
            mock_response = Mock()
            mock_response.status_code = 200
            mock_response.json.return_value = {
                'id': 'test/model'
                # Missing other fields
            }
            mock_get.return_value = mock_response
            
            url = "https://huggingface.co/test/model"
            model_info = parser.parse_model_url(url)
            
            assert model_info is not None
            assert model_info.name == "test/model"
            assert model_info.downloads is None
            assert model_info.likes is None
