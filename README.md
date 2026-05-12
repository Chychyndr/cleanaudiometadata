# Audio Metadata Cleaner

A simple Python script for removing extra metadata from audio files.

The script removes embedded tags such as title, artist, album, contributing artists, cover image and other hidden metadata.

The file name and audio quality stay unchanged.

## Supported formats

```text
.mp3, .flac, .m4a, .mp4, .aac, .ogg, .opus, .wav, .aiff, .aif, .wma
```

## Requirements

- Python 3.10+
- uv

## Install uv

On Windows, open PowerShell and run:

```powershell
irm https://astral.sh/uv/install.ps1 | iex
```

Check that uv is installed:

```powershell
uv --version
```

## How to run

Clone the repository:

```powershell
git clone https://github.com/Chychyndr/cleanaudiometadata.git
cd audio-metadata-cleaner
```

Run a safe check first:

```powershell
uv run --with mutagen python clean_audio_metadata.py "D:\Music" --recursive --dry-run
```

This command only shows which files will be processed. It does not change anything.

Remove metadata and create backup copies:

```powershell
uv run --with mutagen python clean_audio_metadata.py "D:\Music" --recursive --backup
```

Clean one audio file:

```powershell
uv run --with mutagen python clean_audio_metadata.py "D:\Music\song.mp3" --backup
```

## Options

```text
--recursive   Process files inside subfolders
--backup      Create backup copies before cleaning
--dry-run     Show files without changing them
```

## Examples

Clean all audio files in a folder:

```powershell
uv run --with mutagen python clean_audio_metadata.py "D:\Audio" --recursive --backup
```

Check one folder without changing files:

```powershell
uv run --with mutagen python clean_audio_metadata.py "D:\Audio" --recursive --dry-run
```

Clean a single file:

```powershell
uv run --with mutagen python clean_audio_metadata.py "D:\Audio\track.mp3" --backup
```

## Notes

After cleaning metadata, refresh the folder in Windows Explorer with `F5`.

Windows may still show old metadata for a short time because of cache.
