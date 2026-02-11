#!/usr/bin/env python3
"""Download and prepare Kokoro German v1.1 model and voices."""

import json
import os
from pathlib import Path

from huggingface_hub import hf_hub_download
from loguru import logger

REPO_ID = "Tundragoon/Kokoro-German"

# Files to download: (repo filename, local relative path)
MODEL_FILES = [
    ("kokoro-german-v1_1-de.pth", "kokoro-german-v1_1-de.pth"),
    ("config.json", "config.json"),
]

VOICE_FILES = [
    ("voices/df_eva.pt", "df_eva.pt"),
    ("voices/dm_bernd.pt", "dm_bernd.pt"),
]


def verify_files(model_dir: str, voices_dir: str) -> bool:
    """Verify that model files exist and are valid."""
    try:
        model_path = os.path.join(model_dir, "kokoro-german-v1_1-de.pth")
        config_path = os.path.join(model_dir, "config.json")

        if not os.path.exists(model_path) or os.path.getsize(model_path) == 0:
            return False
        if not os.path.exists(config_path):
            return False

        with open(config_path) as f:
            json.load(f)

        for _, fname in VOICE_FILES:
            voice_path = os.path.join(voices_dir, fname)
            if not os.path.exists(voice_path) or os.path.getsize(voice_path) == 0:
                return False

        return True
    except Exception:
        return False


def download_model(output_dir: str) -> None:
    """Download German model and voice files from HuggingFace.

    Args:
        output_dir: Directory to save model files (e.g. api/src/models/v1_0)
    """
    try:
        voices_dir = os.path.join(os.path.dirname(output_dir), "..", "voices", "v1_0")
        voices_dir = os.path.normpath(voices_dir)

        os.makedirs(output_dir, exist_ok=True)
        os.makedirs(voices_dir, exist_ok=True)

        if verify_files(output_dir, voices_dir):
            logger.info("Model files already exist and are valid")
            return

        logger.info(f"Downloading Kokoro German v1.1 from {REPO_ID}")

        for repo_file, local_file in MODEL_FILES:
            local_path = os.path.join(output_dir, local_file)
            if os.path.exists(local_path) and os.path.getsize(local_path) > 0:
                logger.info(f"Skipping {local_file} (already exists)")
                continue
            logger.info(f"Downloading {repo_file}...")
            hf_hub_download(
                repo_id=REPO_ID,
                filename=repo_file,
                local_dir=output_dir,
            )
            # hf_hub_download preserves directory structure, move if needed
            downloaded = os.path.join(output_dir, repo_file)
            target = os.path.join(output_dir, local_file)
            if downloaded != target and os.path.exists(downloaded):
                os.replace(downloaded, target)

        for repo_file, local_file in VOICE_FILES:
            local_path = os.path.join(voices_dir, local_file)
            if os.path.exists(local_path) and os.path.getsize(local_path) > 0:
                logger.info(f"Skipping {local_file} (already exists)")
                continue
            logger.info(f"Downloading {repo_file}...")
            hf_hub_download(
                repo_id=REPO_ID,
                filename=repo_file,
                local_dir=voices_dir,
            )
            # Move from voices/ subdirectory to flat structure
            downloaded = os.path.join(voices_dir, repo_file)
            target = os.path.join(voices_dir, local_file)
            if downloaded != target and os.path.exists(downloaded):
                os.replace(downloaded, target)

        if not verify_files(output_dir, voices_dir):
            raise RuntimeError("Failed to verify downloaded files")

        logger.info(f"Model files prepared in {output_dir}")
        logger.info(f"Voice files prepared in {voices_dir}")

    except Exception as e:
        logger.error(f"Failed to download model: {e}")
        raise


def main():
    """Main entry point."""
    import argparse

    parser = argparse.ArgumentParser(description="Download Kokoro German v1.1 model")
    parser.add_argument(
        "--output", required=True, help="Output directory for model files"
    )

    args = parser.parse_args()
    download_model(args.output)


if __name__ == "__main__":
    main()
