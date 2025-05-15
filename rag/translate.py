import argparse
import logging
from enum import Enum
from pathlib import Path

import argostranslate.package
import argostranslate.translate

# Constants
PACKAGE_CACHE_DIR = Path.home() / ".argostranslate_packages"
VERBOSITY_LEVELS = {
    0: logging.WARNING,
    1: logging.INFO,
    2: logging.DEBUG,
    3: logging.NOTSET,
}


class Mode(Enum):
    ENG_TO_RUS = 'from_eng_to_rus'
    RUS_TO_ENG = 'from_rus_to_eng'


# Setup logging
logger = logging.getLogger(__name__)


def check_packages_installed(from_code: str, to_code: str) -> bool:
    """Check if language package is already installed."""
    installed_languages = argostranslate.translate.get_installed_languages()
    from_lang = next(
        (lang for lang in installed_languages if lang.code == from_code), None)
    to_lang = next(
        (lang for lang in installed_languages if lang.code == to_code), None)

    if not from_lang or not to_lang:
        return False

    # Check if translation between these languages is available
    try:
        return from_lang.get_translation(to_lang) is not None
    except Exception:
        return False


def download_package(from_code: str, to_code: str):
    """Download and install package if not already installed."""
    # First check if the translation is already available
    if check_packages_installed(from_code, to_code):
        logger.debug(
            f"Translation package {from_code}->{to_code} already installed")
        return

    logger.info(f"Installing translation package {from_code}->{to_code}...")
    argostranslate.package.update_package_index()

    available_packages = argostranslate.package.get_available_packages()
    package = next(
        (pkg for pkg in available_packages
         if pkg.from_code == from_code and pkg.to_code == to_code),
        None
    )

    if not package:
        raise ValueError(
            f"No package available for {from_code}->{to_code} translation")

    # Only proceed if the specific translation isn't available
    installed_languages = argostranslate.translate.get_installed_languages()
    from_lang = next(
        (lang for lang in installed_languages if lang.code == from_code), None)
    to_lang = next(
        (lang for lang in installed_languages if lang.code == to_code), None)

    if not from_lang or not to_lang or not from_lang.get_translation(to_lang):
        # Download and install only if needed
        package.download()
        package.install()
        logger.info(f"Successfully installed {from_code}->{to_code}")
    else:
        logger.debug(
            f"Translation capability {from_code}->{to_code} already exists")


def setup_logging(verbosity: int):
    level = VERBOSITY_LEVELS.get(min(verbosity, 3), logging.NOTSET)
    logging.basicConfig(
        level=level,
        format="%(asctime)s - %(levelname)s - %(message)s",
    )


def translate(mode: Mode, input_text: str) -> str:
    if mode == Mode.ENG_TO_RUS:
        download_package("en", "ru")
        return argostranslate.translate.translate(
            input_text, "en", "ru")
    elif mode == Mode.RUS_TO_ENG:
        download_package("ru", "en")
        return argostranslate.translate.translate(
            input_text, "ru", "en")


def main():
    parser = argparse.ArgumentParser(description="Offline translation tool")

    # Translation direction
    translation_group = parser.add_mutually_exclusive_group(required=True)
    translation_group.add_argument(
        "--en-ru",
        action="store_true",
        help="Translate from English to Russian"
    )
    translation_group.add_argument(
        "--ru-en",
        action="store_true",
        help="Translate from Russian to English"
    )

    parser.add_argument(
        "text",
        nargs="+",
        help="Text to translate (put in quotes if it contains spaces)"
    )
    parser.add_argument(
        "-v", "--verbose",
        action="count",
        default=0,
        help="Increase verbosity level (-v, -vv, -vvv)"
    )

    args = parser.parse_args()
    setup_logging(args.verbose)
    input_text = " ".join(args.text)

    try:
        if args.en_ru:
            download_package("en", "ru")
            translation = argostranslate.translate.translate(
                input_text, "en", "ru")
        else:
            download_package("ru", "en")
            translation = argostranslate.translate.translate(
                input_text, "ru", "en")

        print(translation)
    except Exception as e:
        logger.error(f"Translation failed: {str(e)}")
        exit(1)


if __name__ == "__main__":
    main()
