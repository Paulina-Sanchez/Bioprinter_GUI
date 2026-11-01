# BioPrinter Studio

Desktop control interface for a bioprinter running Marlin firmware. Built with Python and CustomTkinter.

## Download

- **Mac (Apple Silicon M1, M2, M3 or later):** [BioPrinterStudio-Mac.dmg](https://github.com/Paulina-Sanchez/Bioprinter_GUI/releases/latest/download/BioPrinterStudio-Mac.dmg)
- **Windows:** [BioPrinterStudio-Windows.exe](https://github.com/Paulina-Sanchez/Bioprinter_GUI/releases/latest/download/BioPrinterStudio-Windows.exe)

All versions are available in [Releases](https://github.com/Paulina-Sanchez/Bioprinter_GUI/releases).

## Installation on Mac

1. Open `BioPrinterStudio-Mac.dmg`.
2. Drag **BioPrinter Studio** into the **Applications** folder.
3. The first time, right-click the app and select **Open**.
4. If macOS blocks it, go to **System Settings → Privacy & Security** and click **Open Anyway**.

## Installation on Windows

1. Download `BioPrinterStudio-Windows.exe`.
2. Double-click to run it. No installation required.
3. If *Windows protected your PC* appears, click **More info**, then **Run anyway**.
4. If your antivirus blocks it, add it as an exception. This is a common false positive for Python-based apps.

## Getting Started

1. Connect the bioprinter via USB.
2. Open **BioPrinter Studio** and log in.
3. Select the serial port (`/dev/cu.usbmodem...` on Mac, `COM3`, `COM4`, etc. on Windows).
4. Set the baud rate to **115200** and click **Connect**.

## Run from source

    pip install -r requirements.txt
    python bioprinter_app.py

## License

MIT
