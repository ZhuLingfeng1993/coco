import cv2 as cv
import os
import sys

image_dir = sys.argv[1]
src_format = '.bmp'
dst_format = '.png'
to_gray = True
delete_src = True


file_counter = 0

print('Starting...')
file_names = os.listdir(image_dir)
for file_id, file_name in enumerate(file_names):
    src_path = os.path.join(image_dir, file_name)
    if not os.path.isfile(src_path):
        continue
    [root_name, ext_name] = os.path.splitext(file_name)
    # Check file type.
    if ext_name != src_format:
        continue
    file_counter += 1

    img = cv.imread(src_path)
    if img is None:
        print('Can not open image: {}'.format(src_path))
        continue
    if to_gray:
        img = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    dst_path = os.path.join(image_dir, root_name + dst_format)
    cv.imwrite(dst_path, img)
    if delete_src:
        os.remove(src_path)

    # Show progress.
    if file_id % 100 == 0:
        print('{} files of {} processed.'.format(file_id, len(file_names)))

print('num_files:', len(file_names))
print('num_processed_files: {}'.format(file_counter))


