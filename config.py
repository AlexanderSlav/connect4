from enum import Enum
from pathlib import Path
from typing import Optional, Union

import yaml
from loguru import logger
from pydantic import BaseModel, Field, field_validator


class GameConfig(BaseModel):
    """Configuration for the game - easily adjustable"""

    rows: int = Field(
        default=6, ge=4, le=10, description="Number of rows in the game board"
    )
    cols: int = Field(
        default=7, ge=4, le=10, description="Number of columns in the game board"
    )
    win_length: int = Field(
        default=4, ge=3, le=8, description="Number of consecutive pieces needed to win"
    )

    @field_validator("win_length")
    @classmethod
    def validate_win_length(cls, v, info):
        """Ensure win_length is possible to achieve on the board"""
        if info.data:
            rows = info.data.get("rows", 6)
            cols = info.data.get("cols", 7)
            max_dimension = max(rows, cols)
            if v > max_dimension:
                raise ValueError(
                    f"win_length ({v}) cannot be greater than max board dimension ({max_dimension})"
                )
        return v


def load_config_from_yaml(config_path: Union[str, Path]) -> GameConfig:
    """
    Load configuration from a YAML file.

    Args:
        config_path: Path to the YAML configuration file

    Returns:
        GameConfig: Loaded and validated configuration

    Raises:
        FileNotFoundError: If the config file doesn't exist
        yaml.YAMLError: If the YAML file is invalid
        ValidationError: If the configuration is invalid
    """
    config_path = Path(config_path)

    if not config_path.exists():
        raise FileNotFoundError(f"Configuration file not found: {config_path}")

    try:
        with open(config_path, "r", encoding="utf-8") as file:
            config_data = yaml.safe_load(file)
    except yaml.YAMLError as e:
        raise yaml.YAMLError(f"Error parsing YAML file {config_path}: {e}")

    if config_data is None:
        config_data = {}

    return GameConfig(**config_data)


def get_config(config_path: Optional[Union[str, Path]] = None) -> GameConfig:
    """
    Get game configuration from file or defaults.

    Args:
        config_path: Optional path to configuration file

    Returns:
        GameConfig: Game configuration
    """
    if config_path:
        return load_config_from_yaml(config_path)

    logger.info("No configuration file found, using default configuration")
    return GameConfig()
