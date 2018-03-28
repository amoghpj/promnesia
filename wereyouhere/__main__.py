# TODO move to kython?
def import_config():
    import os, sys
    sys.path.append(os.getcwd())
    import config
    sys.path.pop()
    return config

config = import_config()

import json
import os.path

import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("WereYouHere")


def main():
    chrome_dir = config.CHROME_HISTORY_DB_DIR
    output_dir = config.OUTPUT_DIR
    if output_dir is None or not os.path.lexists(output_dir):
        raise ValueError("Expecting OUTPUT_DIR to be set to a correct path!")

    all_histories = []


    if chrome_dir is not None:
        import wereyouhere.generator.chrome as chrome_gen
        chrome_histories = list(chrome_gen.iter_chrome_histories(chrome_dir))
        all_histories.extend(chrome_histories)
        logger.info(f"Got {len(chrome_histories)} History storages from Chrome")
    else:
        logger.warning("CHROME_HISTORY_DB_DIR is not set, not using chrome entries to populate extension DB!")

    from wereyouhere.common import merge_histories
    res = merge_histories(all_histories)
    # # TODO filter somehow; sort and remove google queries, etc
    # # TODO filter by length?? or by query length (after ?)

    entries = sorted(res.values())

    dct = {e.url: sorted(e.visits) for e in entries}
    urls_json = os.path.join(output_dir, 'urls.json')
    with open(urls_json, 'w') as fo:
        json.dump(dct, fo, indent=1)

main()
