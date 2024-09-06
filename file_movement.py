import asyncio
import shutil
from argparse import ArgumentParser
from pathlib import Path
import logging

parser = ArgumentParser(description='Sorting files by extension')
parser.add_argument("--source",
                    help="Source folder path",
                    type=str,
                    required=True)
parser.add_argument("--destination",
                    help="Destination folder path",
                    type=str,
                    required=True)
parser.add_argument('--log-level',
                    choices=['INFO', 'ERROR', 'WARNING', 'DEBUG'],
                    help="Log level",
                    default='INFO')

source_folder = None
destination_folder = None


async def read_folder(ctx):
    tasks = []
    for item in ctx['source_folder'].iterdir():
        if item.is_dir():
            tasks.append(read_folder(item))
        else:
            tasks.append(copy_file(item, ctx))
    await asyncio.gather(*tasks)


async def copy_file(file, ctx):
    extension = file.suffix[1:]
    target_folder = Path("{}/{}".format(ctx['destination_folder'], extension))
    target_folder.mkdir(parents=True, exist_ok=True)
    shutil.copy(file, target_folder / file.name)


def loglevel(loglevel):
    if loglevel == 'Info':
        return logging.INFO
    elif loglevel == 'ERROR':
        return logging.ERROR
    elif loglevel == 'WARNING':
        return logging.WARNING
    elif loglevel == 'DEBUG':
        return logging.DEBUG
    else:
        return logging.INFO


if __name__ == "__main__":
    args = parser.parse_args()
    logger = logging.getLogger(__name__)
    logging.basicConfig(level=loglevel(args.log_level))

    context = {}
    context["source_folder"] = Path(args.source)
    context["destination_folder"] = Path(args.destination)

    try:
        asyncio.run(read_folder(context))
        logger.info("Files movement was sorted")
    except Exception as e:
        logger.error("Error was happen: ", e)
