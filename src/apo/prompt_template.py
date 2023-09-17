import json
import string

from abc import ABC
from abc import abstractmethod
from dataclasses import asdict
from dataclasses import dataclass
from dataclasses import field
from typing import Dict
from typing import List
from typing import Optional
from typing import Union


@dataclass
class BasePromptTemplate(ABC):
    """Base template prompts flexibly."""

    initial_template: Dict[str, str] = field(default_factory=dict, init=False)

    def __post_init__(self) -> None:
        """Keep the initial template."""
        self.initial_template = self._initialize_template()

    @abstractmethod
    def _initialize_template(self) -> None:
        """To be implemented by child classes"""
        pass

    @staticmethod
    @abstractmethod
    def _from_dict(data: Dict) -> None:
        """Create a Template instance from a dictionary."""
        pass

    def format_message(self, **kwargs) -> None:
        """Process a message and fill in any placeholders."""

        def recursive_format(value: Union[str, dict]) -> Union[str, dict]:
            if isinstance(value, str):
                placeholders = self._extract_placeholders(value)
                if placeholders:
                    return value.format(**kwargs)
                return value
            elif isinstance(value, dict):
                return {k: recursive_format(v) for k, v in value.items()}
            else:
                return value

        for k in self.__dict__.keys():
            if k != "initial_template":
                self.__dict__[k] = recursive_format(self.initial_template[k])

    @classmethod
    def load(cls, obj: Union[Dict, str]) -> "BasePromptTemplate":
        """Load a Template instance from a JSON file or a dictionary."""
        if isinstance(obj, str):
            return cls._from_json(obj)
        elif isinstance(obj, Dict):
            return cls._from_dict(obj)
        else:
            raise TypeError(f"Expected a JSON file path or a dictionary, got {type(obj)}.")

    @staticmethod
    def _exclude_keys(
        d: dict,
        exclude: Optional[List[str]] = None,  # noqa: B006
    ) -> dict:
        """Exclude keys from a dictionary."""
        if not d["name"]:
            d.pop("name", None)

        if exclude:
            for item in exclude:
                d.pop(item, None)
            return d
        return d

    def to_prompt(
        self,
        exclude: Optional[List[str]] = ["initial_template"],  # noqa: B006
    ) -> Dict:
        """Convert a Template instance to a JSON string."""
        d = asdict(self)
        return self._exclude_keys(d, exclude=exclude)

    @staticmethod
    def _extract_placeholders(s: str) -> List[str]:
        """Extract placeholder variables that can be filled in an f-string."""
        formatter = string.Formatter()
        return [field_name for _, field_name, _, _ in formatter.parse(s) if field_name is not None]

    @classmethod
    def _from_json(cls, json_path: str) -> "BasePromptTemplate":
        """Create a Template instance by providing a JSON path."""
        return cls._from_dict(cls._read_json(json_path))

    @staticmethod
    def _read_json(json_path: str) -> Dict:
        """Read a JSON file."""
        with open(json_path, "r") as f:
            return json.load(f)

    def to_json(self, path: str) -> None:
        """Convert a Template instance to a JSON string."""
        self._write_json(self.initial_template, path)

    def _write_json(self, data: Dict, path: str) -> None:
        """Write a JSON file."""
        with open(path, "w") as f:
            json.dump(data, f)


@dataclass
class MessageTemplate(BasePromptTemplate):
    """Create a template for a message prompt."""

    role: str
    content: str
    name: Optional[str] = None

    def __post_init__(self) -> None:
        """Keep the initial template and error when the role is function but not name was given."""
        super().__post_init__()
        if self.role == "function" and not self.name:
            raise ValueError("The 'name' attribute is required when 'role' is 'function'.")

    def _initialize_template(self) -> Dict[str, str]:
        return {"role": self.role, "content": self.content, "name": self.name}

    @staticmethod
    def _from_dict(data: Dict) -> "MessageTemplate":
        instance = MessageTemplate(**data)
        # Step 2: Add a validation step after initialization
        if instance.role == "function" and not instance.name:
            raise ValueError("The 'name' attribute is required when 'role' is 'function'.")
        return instance


@dataclass
class FunctionTemplate(BasePromptTemplate):
    """Create a template for an OpenAI function."""

    name: str
    description: str
    parameters: Dict[str, Union[str, Dict[str, Dict[str, Union[str, List[str]]]], List[str]]]

    def _initialize_template(self) -> Dict[str, Union[str, Dict[str, Dict[str, Union[str, List[str]]]], List[str]]]:
        return {
            "name": self.name,
            "description": self.description,
            "parameters": self.parameters,
        }

    @staticmethod
    def _from_dict(data: Dict) -> "FunctionTemplate":
        """Create a Template instance from a dictionary."""
        return FunctionTemplate(**data)
