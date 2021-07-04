import cv2
import os
import numpy as np
import sys

def GetDesiredWidthAndHeight(spritesCnt):
    bits = spritesCnt.bit_length()
    width = 1
    height = 1
    if spritesCnt != (1 << (bits - 1)):
        bits += 1
    if bits & 1:
        width = (1 << (bits >> 1))
        height = width
    else:
        width = (1 << (bits >> 1))
        height = width >> 1
    return (width, height)

def GetIndexByCoords(width, height, imgWidth):
    return height * imgWidth + width

def GenerateSpriteSheet(inputPath, outputPath):
    spritesFilePaths = []
    # Read all files path from input path
    for root, dirs, files, in os.walk(inputPath):
        for file in files:
            if file.endswith('.png'):
                spritesFilePaths.append(os.path.join(root, file))

    # Empty list
    spritesList = []
    spritesCnt = len(spritesFilePaths)

    if spritesCnt == 0:
        return

    for i in range(0, spritesCnt):
        sprite = cv2.imread(spritesFilePaths[i], cv2.IMREAD_UNCHANGED)
        spritesList.append(sprite)

    (imgWidth, imgHeight, imgCol) = spritesList[0].shape
    (spriteSheetWidthCnt, spriteSheetHeightCnt) = GetDesiredWidthAndHeight(spritesCnt)

    spriteSheetResult = np.zeros
    spriteEmptyPlaceholder = np.full((imgWidth, imgHeight, 4), (255, 255, 255, 0), np.uint8)

    for h in range(0, spriteSheetHeightCnt):
        spriteSheetHorizontalResult = spriteEmptyPlaceholder
        for w in range(0, spriteSheetWidthCnt):
            indx = GetIndexByCoords(w, h, spriteSheetWidthCnt)
            spriteSheetCurrent = spriteEmptyPlaceholder
            if indx < spritesCnt:
                spriteSheetCurrent = spritesList[indx]
            if w == 0:
                spriteSheetHorizontalResult = spriteSheetCurrent
            else:
                spriteSheetHorizontalResult = cv2.hconcat([spriteSheetHorizontalResult, spriteSheetCurrent])
        if h == 0:
            spriteSheetResult = spriteSheetHorizontalResult
        else:
            spriteSheetResult = cv2.vconcat([spriteSheetResult, spriteSheetHorizontalResult])

    filePrefix = inputPath.split('\\')[-1]
    cv2.imwrite(os.path.join(outputPath, filePrefix + '_Output.png'), spriteSheetResult)

if __name__ == "__main__":
    GenerateSpriteSheet(sys.argv[1], sys.argv[2])
