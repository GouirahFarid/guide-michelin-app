"""
GLM-4 LLM wrapper for LangChain integration.

Uses Zhipu AI's API to access GLM-4 models for response generation.
"""
import logging
from typing import Optional, List, Dict, Any
from dataclasses import dataclass

from langchain_core.language_models.llms import BaseLLM
from langchain_core.outputs import LLMResult, Generation
from langchain_core.callbacks.manager import CallbackManagerForLLMRun
from zhipuai import ZhipuAI

from config import get_settings

logger = logging.getLogger(__name__)
settings = get_settings()

# Default timeout for API calls (seconds)
DEFAULT_API_TIMEOUT = 30.0


# ============================================================================
# GLM-4 MODEL CONFIGURATION
# ============================================================================

@dataclass
class GLMModelConfig:
    """Configuration for GLM models."""
    model: str = "glm-4"  # Options: glm-4, glm-4-plus, glm-4-air, glm-4-flash
    temperature: float = 0.7
    top_p: float = 0.9
    max_tokens: int = 2048
    api_key: Optional[str] = None


# ============================================================================
# CUSTOM GLM-4 LLM CLASS
# ============================================================================

class GLM4LLM(BaseLLM):
    """Custom GLM-4 LLM implementation for LangChain.

    This class wraps Zhipu AI's GLM-4 API for use with LangChain.
    """

    model: str = "glm-4"
    temperature: float = 0.7
    top_p: float = 0.9
    max_tokens: int = 2048
    zhipuai_client: Optional[ZhipuAI] = None

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        api_key = kwargs.get('api_key', settings.zhipuai_api_key)
        if not api_key:
            raise ValueError("ZHIPUAI_API_KEY must be set in environment or config")
        self.zhipuai_client = ZhipuAI(api_key=api_key)
        self.model = kwargs.get('model', self.model)
        self.temperature = kwargs.get('temperature', self.temperature)
        self.top_p = kwargs.get('top_p', self.top_p)
        self.max_tokens = kwargs.get('max_tokens', self.max_tokens)

    @property
    def _llm_type(self) -> str:
        """Return the type of LLM."""
        return "glm-4"

    @property
    def _identifying_params(self) -> Dict[str, Any]:
        """Get identifying parameters."""
        return {
            "model": self.model,
            "temperature": self.temperature,
            "top_p": self.top_p,
            "max_tokens": self.max_tokens,
        }

    def _call(
        self,
        prompt: str,
        stop: Optional[List[str]] = None,
        run_manager: Optional[CallbackManagerForLLMRun] = None,
        **kwargs: Any,
    ) -> str:
        """Call the GLM-4 API with the prompt.

        Args:
            prompt: The prompt to send to the model
            stop: Optional stop sequences
            run_manager: Optional callback manager
            **kwargs: Additional arguments

        Returns:
            The generated text response
        """
        timeout = kwargs.get('timeout', DEFAULT_API_TIMEOUT)
        try:
            response = self.zhipuai_client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a helpful assistant specializing in Michelin restaurant recommendations."},
                    {"role": "user", "content": prompt}
                ],
                temperature=self.temperature,
                top_p=self.top_p,
                max_tokens=self.max_tokens,
                timeout=timeout,
            )
            return response.choices[0].message.content

        except Exception as e:
            logger.error(f"GLM-4 API call failed: {type(e).__name__}: {e}")
            raise RuntimeError(f"GLM-4 API call failed: {str(e)}")


# ============================================================================
# LANGCHAIN COMPATIBLE FACTORY FUNCTIONS
# ============================================================================

def create_glm4_llm(
    model: str = "glm-4",
    temperature: float = 0.7,
    max_tokens: int = 2048,
    api_key: Optional[str] = None
) -> GLM4LLM:
    """Create a GLM-4 LLM instance.

    Args:
        model: Model name (glm-4, glm-4-plus, glm-4-air, glm-4-flash)
        temperature: Sampling temperature (0-1)
        max_tokens: Maximum tokens to generate
        api_key: Zhipu AI API key (uses env var if not provided)

    Returns:
        Configured GLM4LLM instance

    Example:
        >>> llm = create_glm4_llm(temperature=0.3)
        >>> response = llm.invoke("Tell me about 3-star restaurants in Munich")
    """
    return GLM4LLM(
        model=model,
        temperature=temperature,
        max_tokens=max_tokens,
        api_key=api_key or settings.zhipuai_api_key
    )


def create_glm4_for_rag(
    temperature: float = 0.3,  # Lower temperature for more factual responses
    max_tokens: int = 1500
) -> GLM4LLM:
    """Create GLM-4 LLM optimized for RAG applications.

    Uses lower temperature for more focused, factual responses.
    """
    return create_glm4_llm(
        model="glm-4",
        temperature=temperature,
        max_tokens=max_tokens
    )


def create_glm4_for_chat(
    temperature: float = 0.8,  # Higher temperature for more conversational
    max_tokens: int = 2048
) -> GLM4LLM:
    """Create GLM-4 LLM optimized for conversational chat.

    Uses higher temperature for more natural, varied responses.
    """
    return create_glm4_llm(
        model="glm-4",
        temperature=temperature,
        max_tokens=max_tokens
    )


# ============================================================================
# DIRECT API FUNCTIONS (without LangChain)
# ============================================================================

async def chat_completion(
    messages: List[Dict[str, str]],
    model: str = "glm-4",
    temperature: float = 0.7,
    max_tokens: int = 2048,
    stream: bool = False,
    timeout: float = DEFAULT_API_TIMEOUT
) -> Dict[str, Any]:
    """Make a direct chat completion API call.

    Args:
        messages: List of message dicts with 'role' and 'content'
        model: Model name
        temperature: Sampling temperature
        max_tokens: Maximum tokens to generate
        stream: Whether to stream responses
        timeout: Request timeout in seconds

    Returns:
        API response as dictionary

    Example:
        >>> response = await chat_completion([
        ...     {"role": "user", "content": "What are the best 3-star restaurants?"}
        ... ])
    """
    client = ZhipuAI(api_key=settings.zhipuai_api_key)

    try:
        response = client.chat.completions.create(
            model=model,
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens,
            stream=stream,
            timeout=timeout,
        )
        return {
            "content": response.choices[0].message.content,
            "model": response.model,
            "usage": {
                "prompt_tokens": response.usage.prompt_tokens,
                "completion_tokens": response.usage.completion_tokens,
                "total_tokens": response.usage.total_tokens,
            }
        }
    except Exception as e:
        logger.error(f"Chat completion failed: {type(e).__name__}: {e}")
        raise RuntimeError(f"GLM-4 API call failed: {str(e)}")


def simple_chat(
    user_message: str,
    system_message: str = "You are a helpful assistant.",
    model: str = "glm-4",
    timeout: float = DEFAULT_API_TIMEOUT
) -> str:
    """Simple synchronous chat function.

    Args:
        user_message: User's message
        system_message: Optional system prompt
        model: Model to use
        timeout: Request timeout in seconds

    Returns:
        Model's response text
    """
    client = ZhipuAI(api_key=settings.zhipuai_api_key)

    messages = [
        {"role": "system", "content": system_message},
        {"role": "user", "content": user_message}
    ]

    try:
        response = client.chat.completions.create(
            model=model,
            messages=messages,
            timeout=timeout,
        )
        return response.choices[0].message.content
    except Exception as e:
        logger.error(f"Simple chat failed: {type(e).__name__}: {e}")
        raise


# ============================================================================
# STREAMING SUPPORT
# ============================================================================

async def stream_chat_completion(
    messages: List[Dict[str, str]],
    model: str = "glm-4",
    temperature: float = 0.7,
):
    """Stream chat completion responses.

    Yields chunks of the response as they arrive.
    """
    client = ZhipuAI(api_key=settings.zhipuai_api_key)

    try:
        stream = client.chat.completions.create(
            model=model,
            messages=messages,
            temperature=temperature,
            stream=True
        )

        for chunk in stream:
            if chunk.choices[0].delta.content:
                yield chunk.choices[0].delta.content

    except Exception as e:
        raise RuntimeError(f"GLM-4 streaming failed: {str(e)}")


# ============================================================================
# ERROR HANDLING & RETRY
# ============================================================================

from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type


class GLMAPIError(Exception):
    """Base exception for GLM API errors."""
    pass


class GLMRateLimitError(GLMAPIError):
    """Raised when rate limit is exceeded."""
    pass


class GLMAuthenticationError(GLMAPIError):
    """Raised when authentication fails."""
    pass


@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=2, max=10),
    retry=retry_if_exception_type(GLMRateLimitError)
)
async def chat_with_retry(
    messages: List[Dict[str, str]],
    model: str = "glm-4",
    temperature: float = 0.7
) -> str:
    """Chat completion with automatic retry on rate limit errors."""
    try:
        result = await chat_completion(messages, model, temperature)
        return result["content"]
    except Exception as e:
        error_msg = str(e).lower()
        if "rate limit" in error_msg or "429" in error_msg:
            raise GLMRateLimitError(f"Rate limit exceeded: {e}")
        elif "auth" in error_msg or "401" in error_msg:
            raise GLMAuthenticationError(f"Authentication failed: {e}")
        raise


# ============================================================================
# MODEL INFO
# ============================================================================

GLM_MODELS = {
    "glm-4": {
        "name": "GLM-4",
        "description": "Flagship model with best performance",
        "context_length": 128000,
        "input_price": 0.1,  # per 1K tokens
        "output_price": 0.1,
    },
    "glm-4-plus": {
        "name": "GLM-4 Plus",
        "description": "Enhanced version with better reasoning",
        "context_length": 128000,
        "input_price": 0.15,
        "output_price": 0.15,
    },
    "glm-4-air": {
        "name": "GLM-4 Air",
        "description": "Lightweight model for faster responses",
        "context_length": 128000,
        "input_price": 0.01,
        "output_price": 0.01,
    },
    "glm-4-flash": {
        "name": "GLM-4 Flash",
        "description": "Ultra-fast model for simple tasks",
        "context_length": 128000,
        "input_price": 0.001,
        "output_price": 0.001,
    },
}


def get_model_info(model_name: str = "glm-4") -> Dict[str, Any]:
    """Get information about a GLM model."""
    return GLM_MODELS.get(model_name, GLM_MODELS["glm-4"])


def list_available_models() -> List[str]:
    """List available GLM models."""
    return list(GLM_MODELS.keys())
