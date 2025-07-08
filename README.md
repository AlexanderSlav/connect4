# Connect 4 Game

A modern Python implementation of the classic Connect 4 game with configurable settings.


## Usage

### Basic Usage
```bash
python run.py
```


### Using a Custom Config File
```bash
python run.py --config path/to/your/config.yaml
```


```yaml
# Connect 4 Game Configuration
# This file controls the game settings

# Board dimensions
rows: 6          # Number of rows (4-10)
cols: 7          # Number of columns (4-10)

# Win condition
win_length: 4    # Number of consecutive pieces needed to win (3-8)

```
