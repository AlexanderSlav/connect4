import sys
import argparse

from loguru import logger

from config import get_config, GameConfig
from src.engine import GameEngine


def parse_arguments() -> argparse.Namespace:
    """Parse command line arguments"""
    parser = argparse.ArgumentParser(
        description="Connect 4 Game - Two-player console version",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    parser.add_argument(
        '--config', '-c',
        type=str,
        default="config.yaml",
        help='Path to YAML configuration file'
    )
    
    return parser.parse_args()


def main():
    """Main entry point"""
    try:
        args = parse_arguments()
        
        try:
            config = get_config(args.config) if args.config else get_config()
        except Exception as e:
            logger.error(f"Error loading configuration: {e}")
            sys.exit(1)
        
        logger.info("Current configuration:")
        logger.info(config.model_dump_json(indent=4))
        
        logger.info("Starting Connect 4 Game...")
        logger.info(f"Board size: {config.rows}x{config.cols}")
        logger.info(f"Win length: {config.win_length}")
        
        game_engine = GameEngine(config)
        game_engine.play()
        
    except KeyboardInterrupt:
        logger.info("\n\nGame interrupted. Thanks for playing!")
        sys.exit(0)
    except Exception as e:
        logger.error(f"An error occurred: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()