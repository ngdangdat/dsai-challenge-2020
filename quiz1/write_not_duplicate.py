import sys
import os
import logging
from datetime import datetime
from collections import OrderedDict

FORMAT = '%(asctime)-15s [%(levelname)s] %(message)s'
stream_handler = logging.StreamHandler()
stream_handler.setLevel(logging.INFO)
stream_handler.setFormatter(logging.Formatter(FORMAT))

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
logger.addHandler(stream_handler)
logger.propagate = False


def read_file_to_lines(file_path):
    lines = []
    with open(file_path) as f:
        lines = [line.strip() for line in f.readlines()]
        f.close()
    return lines


if __name__ == '__main__':
    if len(sys.argv) != 3:
        logger.error("Invalid number of argument")
        sys.exit(1)

    file_a = sys.argv[1]
    file_b = sys.argv[2]

    if not os.path.isfile(file_a) or not os.path.isfile(file_b):
        logger.error(f"{file_a} or {file_b} (can be both) is not invalid")
        sys.exit(1)

    output = f"{file_a}_{file_b}_{int(datetime.now().timestamp())}.output.txt"

    file_a_lines = read_file_to_lines(file_a)
    file_b_lines = read_file_to_lines(file_b)

    cnt_dict = OrderedDict()
    for i in range(max([len(file_a_lines), len(file_b_lines)])):
        if i < len(file_a_lines):
            el_a = file_a_lines[i]
            if el_a:
                cnt_dict[el_a] = cnt_dict.setdefault(el_a, 0) + 1

        if i < len(file_b_lines):
            el_b = file_b_lines[i]
            if el_b:
                cnt_dict[el_b] = cnt_dict.setdefault(el_b, 0) + 1

    keys_length = len(cnt_dict.keys())
    with open(output, 'w') as f:
        for index, key in enumerate(cnt_dict.keys()):
            if cnt_dict[key] > 1:
                continue
            f.write(f"{key}")
            if index < keys_length - 1:
                f.write("\n")
        f.close()
    logger.info(f"Done! Output: {output}")
    sys.exit(0)
