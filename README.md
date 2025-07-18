# Batch-Render-Tool-Script
A simple and efficient tool for batch rendering multiple Write nodes in Nuke with custom order and format control.

### Features

- Select and batch render multiple Write nodes  
- Set custom execution order for rendering  
- Choose output format (`png`, `exr`, `mov`) and frame padding  
- Specify root output directory and frame range  
- Automatically creates output folders as needed  
- Validates user inputs to avoid errors  
- Displays render times for each Write node  

### Usage

1. Run the script in Nuke's Script Editor  
2. Select which Write nodes to render and assign their order  
3. Set output directory, format, padding, and frame range  
4. Click **Validate**, then confirm to start rendering  
5. Review render time summary when finished  

### Installation

1. **Download** the script file from this repository  
2. **Rename** the script file to `batch_render_tool.py` (required for proper importing)  
3. Place it in your Nuke scripts folder (e.g., `~/.nuke/`)
   
#### Adding to Nuke Menu

1. Open or create `menu.py` in your `~/.nuke/` directory  
2. Add the following lines:
    ```python
    import nuke
    import batch_render_tool  # Make sure the filename is batch_render_tool.py

    nuke.menu("Nuke").addCommand("Custom Tools/Batch Render Tool", "batch_render_tool.batch_render_tool()", "Ctrl+Alt+B")
3. Restart Nuke  
4. Access the tool under `Custom Tools > Batch Render Tool`

## Prerequisites
- **Nuke** (tested on Nuke 12.0+)
- Python environment bundled with Nuke (no external installs needed)

## Contribution
Contributions are welcome! Feel free to submit pull requests or raise issues for any suggestions or bug reports.

## Acknowledgments
- **Foundry Nuke** for providing an industry-standard compositing platform.
- The Nuke community for continuous inspiration and support.


