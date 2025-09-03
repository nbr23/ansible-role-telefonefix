#!/usr/bin/env python3
# /// script
# dependencies = [
# ]
# ///

"""
TTS to Asterisk Audio Converter
Uses the gopipertts API to generate speech and convert to Asterisk-compatible format
"""

import argparse
import os
import sys
import subprocess
import urllib.parse
import urllib.request
import tempfile
import re
from pathlib import Path

# Default values
DEFAULT_VOICE = "en_US-amy-low"
DEFAULT_SPEED = "1.0"
TTS_SERVER = "http://localhost:8080"


def generate_filename_from_text(text):
    # Take first 30 characters, replace spaces with dashes, keep only alphanumeric and dashes
    filename = text[:30].replace(" ", "-")
    filename = re.sub(r"[^a-zA-Z0-9\-]", "", filename)
    return filename.lower()


def check_dependencies():
    try:
        subprocess.run(["sox", "--version"], capture_output=True, check=True)
    except (subprocess.CalledProcessError, FileNotFoundError):
        print(
            "Error: sox is required but not installed. Install with: apt-get install sox"
        )
        sys.exit(1)


def main():
    parser = argparse.ArgumentParser(
        description="TTS to Asterisk Audio Converter",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
EXAMPLES:
  %(prog)s "Hello world"
  %(prog)s -v en_US-ryan-high -s 1.2 -o /path/to/audio/greeting "Welcome to our system"
  %(prog)s fr_FR-gilles-low 1.0 "Un instant, je vous connecte."

The script will generate .gsm files for Asterisk compatibility
        """,
    )

    parser.add_argument("text", nargs="*", help="Text to convert to speech")
    parser.add_argument(
        "-v",
        "--voice",
        default=DEFAULT_VOICE,
        help=f"Voice model (default: {DEFAULT_VOICE})",
    )
    parser.add_argument(
        "-s",
        "--speed",
        default=DEFAULT_SPEED,
        help=f"Speech speed (default: {DEFAULT_SPEED})",
    )
    parser.add_argument(
        "-o", "--output", help="Output file or directory (creates dirs as needed)"
    )
    parser.add_argument(
        "-u",
        "--url",
        default=TTS_SERVER,
        help=f"TTS server URL (default: {TTS_SERVER})",
    )

    args = parser.parse_args()

    if len(args.text) == 3 and not any(
        [args.voice != DEFAULT_VOICE, args.speed != DEFAULT_SPEED]
    ):
        args.voice = args.text[0]
        args.speed = args.text[1]
        text = args.text[2]
    elif args.text:
        text = " ".join(args.text)
    else:
        print("Error: Text parameter is required")
        parser.print_help()
        sys.exit(1)

    if not args.output:
        output_path = generate_filename_from_text(text)
    else:
        output_arg = Path(args.output)

        if str(output_arg).endswith("/") or output_arg.is_dir():
            output_arg.mkdir(parents=True, exist_ok=True)
            filename = generate_filename_from_text(text)
            output_path = output_arg / filename
        else:
            output_arg.parent.mkdir(parents=True, exist_ok=True)
            output_path = output_arg.parent / output_arg.name.lower()

    output_path = Path(output_path)
    final_gsm = output_path.with_suffix(".gsm")

    print("Generating TTS audio...")
    print(f"Voice: {args.voice}")
    print(f"Speed: {args.speed}")
    print(f"Text: {text}")
    print(f"Output: {output_path}")

    check_dependencies()

    text_encoded = urllib.parse.quote(text)

    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as temp_wav:
        temp_wav_path = temp_wav.name

    try:
        print("Fetching audio from TTS API...")
        url = f"{args.url}/api/tts?voice={args.voice}&speed={args.speed}&text={text_encoded}"

        try:
            urllib.request.urlretrieve(url, temp_wav_path)
        except Exception as e:
            print(f"Error: Failed to fetch audio from TTS API at {args.url}")
            print("Make sure the gopipertts server is running and accessible")
            sys.exit(1)

        if not os.path.getsize(temp_wav_path):
            print("Error: Did not receive a valid WAV file from the API")
            print("Check if the TTS server is running and the parameters are correct")
            sys.exit(1)

        print("Converting to GSM format for Asterisk...")

        try:
            subprocess.run(
                ["sox", temp_wav_path, "-r", "8000", "-c", "1", str(final_gsm)],
                check=True,
                capture_output=True,
            )
        except subprocess.CalledProcessError as e:
            print("Error: Failed to convert to GSM format")
            print(f"Sox error: {e.stderr.decode() if e.stderr else 'Unknown error'}")
            sys.exit(1)

        print("Success! Generated file:")
        print(f"  GSM: {final_gsm}")
        print()
        print("To use in Asterisk dialplan:")
        print(f"  exten => s,1,Playback({output_path.stem})")

    finally:
        if os.path.exists(temp_wav_path):
            os.unlink(temp_wav_path)


if __name__ == "__main__":
    main()
