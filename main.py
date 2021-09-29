
#############################################################################
#                        정보-묶음 매듭-상자 셈-기계 V 0.1
#                                 by yor42
#                     ㅡ "우리는 작성한다 비단구렁이의 말을"
#############################################################################

import os, glob, logging
from pathlib import Path
import numpy as np

while True:
    pathtodataset = input("데이터셋 최상위 폴더를 입력해 주세요: ")
    if os.path.isdir(pathtodataset):
        break

while True:
    path2names = input("객체 이름 파일의 위치를 입력해 주세요: ")
    if os.path.isdir(pathtodataset):
        break

namefile = open(path2names, 'r')
names = namefile.readlines()
classcounts = np.zeros_like(names, dtype=np.int64)

filelist = glob.glob(pathtodataset+"/*.txt")

for file in filelist:
    filename_noextension = os.path.splitext(file)[0]
    if os.path.isfile(filename_noextension + ".jpg") or os.path.isfile(filename_noextension + ".png"):
        with open(file, 'r') as f:
            filename = Path(file).stem
            lines = f.readlines()
            lines2remove = []
            for i, line in enumerate(lines):
                parsed_class = line.split()[0]
                try:
                    parsed_class_int = int(parsed_class)
                    if parsed_class_int < len(names):
                        classcounts[parsed_class_int] += 1
                    else:
                        print(str(parsed_class_int)+" in "+file)
                        lines2remove.append(line)
                except:
                    logging.warning("경고: 라벨링 데이터 {}의 {}번째 줄 클래스 값 {}이 올바르지 않은 것 같습니다."
                                    .format(filename, i, parsed_class))
            f.close()
        if lines2remove:
            with open(file, 'w') as f:
                filename = Path(file).stem
                for line in lines:
                    parsed_class = line.split()[0]
                    if line in lines2remove:
                        print("{} 라벨링 파일의 비정상적인 클래스 {}를 가진 바운딩 박스를 제거합니다.".format(filename, parsed_class))
                        continue
                    else:
                        f.write(line)
                f.close()
    else:
        logging.warning("파일 {}는 올바른 라벨링 데이터가 아닌 것 같습니다: 동일한 이름의 이미지 데이터가 없습니다!".format(file))
for i,name in enumerate(names):
    print("클래스 {} {}개".format(name, classcounts[i]))
