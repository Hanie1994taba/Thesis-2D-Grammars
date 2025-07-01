# Thesis-2D-Grammars
# Subdivision2D: Parametric Subdivision Framework for Grasshopper

This repository contains a Python script for Grasshopper (via GhPython) that performs **recursive 2D subdivision** of closed curves. It uses multiple geometric transformation rules based on selected modes to produce generative and fabricatable patterns. The script is designed for integration with **interactive parametric design workflows** in Grasshopper.

## 🔧 Features

- Rule-based subdivision of 2D closed curves.
- Three levels of recursive subdivision (loop 1, 2, and 3).
- Five predefined subdivision modes per loop.
- Outputs generated as PolyLines suitable for fabrication or further transformation.
- Integration with Grasshopper-native components via `ghpythonlib`.

## 📥 Inputs

| Input     | Type    | Description                                                                 |
|-----------|---------|-----------------------------------------------------------------------------|
| `curve`   | Curve   | Closed planar curve (e.g. polygon or spline)                                |
| `loop`    | Integer | Recursion level: 0 (original), 1, 2, or 3                                    |
| `mode_1`  | Integer | Subdivision mode for loop 1 (options: 1–5)                                   |
| `mode_2`  | Integer | Subdivision mode for loop 2 (options: 1–4)                                   |
| `mode_3`  | Integer | Subdivision mode for loop 3 (options: 1–4)                                   |

> Example: Use `loop = 2`, `mode_1 = 1`, `mode_2 = 3` to apply two sequential rules.

## 📤 Output

- A list of subdivided PolyLines based on selected loop level and mode.
- Each loop builds recursively upon the previous one.

## 📦 Dependencies

This script is intended to run **inside Grasshopper** using the GhPython scripting component. It relies on:
- `ghpythonlib.components` – to access native Grasshopper functions like `Area`, `Explode`, `CurveMiddle`, `PolyLine`, etc.
- `rhinoscriptsyntax` (imported but not heavily used)

## 🧠 Subdivision Modes

Each mode applies a different geometric strategy:
- **Mode 1**: Triangulation using midpoints and centroid
- **Mode 2**: Diagonals from vertex pairs and centroid
- **Mode 3**: Scaled curve inset and quadrilateral generation
- **Mode 4**: Star-like centralization via midlines
- **Mode 5**: Radiating strips toward centroid (available in loop 1 only)

> Modes can be combined across recursive loops for richer patterns.

## 💡 Example Use Cases

- Design of **parametric tiles**, **structural subdivisions**, or **fabrication-friendly segments**
- **Interactive design tools** for architectural ideation
- Educational demonstrations of recursive logic in design

## 🖊 Author

Developed by **Hanie**  
Version: `2023.06.27`

## 📂 Repository Structure

