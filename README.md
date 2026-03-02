# music-tools

**Melodic Range Transposition Tool**

Use the web app: https://melodic-range-transposition.streamlit.app/

This small Python project provides a Streamlit‑based web application for
exploring simple key transpositions while keeping a melody within an
acceptable range. It is built with [music21](https://web.mit.edu/music21)
for music theory calculations and [Streamlit](https://streamlit.io) for
the user interface.

## Features

- Select a starting key (tonic and quality).
- Specify the lowest and highest notes of a melody.
- Use a slider to transpose up or down by a number of half‑steps.
- See the resulting key and adjusted melodic range.

The idea is to help performers or arrangers quickly test new keys whose
range matches the available vocal or instrumental range.

## Getting Started

### Requirements

- Python 3.13
- The dependencies listed in `pyproject.toml` (`music21`,
  `streamlit`)

### Installation

1. Clone the repository (or copy the files to your local machine).
2. Create and activate a virtual environment:

   ```sh
   python -m venv .venv
   source .venv/bin/activate      # on macOS/Linux
   # or .\.venv\Scripts\activate on Windows
   ```

3. Install the dependencies:

   ```sh
   pip install -e .
   # or pip install music21 streamlit
   ```

### Running the App

Start the Streamlit application from the project directory:

```sh
streamlit run sl_app.py
```

A browser window will open showing the interactive transposition tool.

## Project Structure

- `sl_app.py` – main Streamlit application.
- `pyproject.toml` – project metadata and dependencies.

## Contributing

Feel free to open issues or submit pull requests if you think of ways to
improve the tool (e.g. better interval handling, support for chords,
exporting results, etc.).

## License

This project is licensed under the terms of the [MIT License](LICENSE).
