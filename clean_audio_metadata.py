from __future__ import annotations

import argparse
import shutil
from pathlib import Path

from mutagen import File as MutagenFile


AUDIO_EXTENSIONS = {
    ".mp3", ".flac", ".m4a", ".mp4", ".aac",
    ".ogg", ".opus", ".wav", ".aiff", ".aif", ".wma",
}


def find_audio_files(target: Path, recursive: bool):
    if target.is_file():
        if target.suffix.lower() in AUDIO_EXTENSIONS:
            yield target
        return

    files = target.rglob("*") if recursive else target.iterdir()

    for file in files:
        if file.is_file() and file.suffix.lower() in AUDIO_EXTENSIONS:
            yield file


def get_tags_count(audio) -> int:
    tags = getattr(audio, "tags", None)

    if tags is None:
        return 0

    try:
        return len(tags)
    except TypeError:
        return 1


def backup_file(file: Path, root: Path, backup_dir: Path):
    relative_path = file.relative_to(root)
    backup_path = backup_dir / relative_path

    backup_path.parent.mkdir(parents=True, exist_ok=True)

    if not backup_path.exists():
        shutil.copy2(file, backup_path)


def clean_metadata(file: Path, root: Path, backup_dir: Path | None, dry_run: bool) -> tuple[str, str]:
    try:
        audio = MutagenFile(str(file))

        if audio is None:
            return "SKIP", "формат не распознан"

        tags_count = get_tags_count(audio)

        if tags_count == 0:
            return "SKIP", "метаданных нет"

        if dry_run:
            return "DRY", f"найдено тегов: {tags_count}"

        if backup_dir is not None:
            backup_file(file, root, backup_dir)

        audio.delete()

        return "OK", "метаданные удалены"

    except PermissionError:
        return "ERR", "файл занят другой программой"

    except Exception as error:
        return "ERR", str(error)


def main():
    parser = argparse.ArgumentParser(
        description="Удаляет метаданные из аудиофайлов: Title, Artist, Album, Cover и т.д."
    )

    parser.add_argument(
        "path",
        help="Путь к папке или аудиофайлу"
    )

    parser.add_argument(
        "-r", "--recursive",
        action="store_true",
        help="Обрабатывать вложенные папки"
    )

    parser.add_argument(
        "--backup",
        action="store_true",
        help="Сделать копию файлов перед очисткой"
    )

    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Только показать, какие файлы будут обработаны"
    )

    args = parser.parse_args()

    target = Path(args.path).expanduser().resolve()

    if not target.exists():
        print(f"[ERR] Путь не найден: {target}")
        return

    root = target if target.is_dir() else target.parent

    backup_dir = None
    if args.backup and not args.dry_run:
        backup_dir = root.parent / f"{root.name}_metadata_backup"
        backup_dir.mkdir(parents=True, exist_ok=True)
        print(f"[INFO] Копии будут сохранены в: {backup_dir}")

    files = list(find_audio_files(target, args.recursive))

    if not files:
        print("[INFO] Аудиофайлы не найдены.")
        return

    print(f"[INFO] Найдено аудиофайлов: {len(files)}")
    print()

    stats = {
        "OK": 0,
        "SKIP": 0,
        "DRY": 0,
        "ERR": 0,
    }

    for file in files:
        status, message = clean_metadata(file, root, backup_dir, args.dry_run)
        stats[status] += 1

        print(f"[{status}] {file.name} — {message}")

    print()
    print("Готово.")
    print(f"OK:   {stats['OK']}")
    print(f"SKIP: {stats['SKIP']}")
    print(f"DRY:  {stats['DRY']}")
    print(f"ERR:  {stats['ERR']}")


if __name__ == "__main__":
    main()