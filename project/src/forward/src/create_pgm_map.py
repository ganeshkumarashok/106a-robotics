import sys
import array
from PIL import Image, ImageDraw

def write_pgm_map(file_name, obstacles_lst):
    # obstacle_lst: a list of obstacle
    # each object has a center and a type ((x, y), type)
    # e.g. [((3, 5), 'human'), ((5, 8), 'block')]

    # define the width (columns) and
    # height (rows) of your image
    width = 100
    height = 100

    # use PIL.Image to draw circle and rectangle
    image = Image.new('1', (width, height), color=255)
    draw = ImageDraw.Draw(image)
    circle_size = 10
    block_size = 10

    for obstacle in obstacles_lst:
        # we will represent human as moving circle
        # other objects as rectangle

        # print(obstacle)
        x, y = obstacle[0]
        if obstacle[1] == 'human':
            # grey is 128
            draw.ellipse([(x - circle_size, y - circle_size), (x + circle_size, y + circle_size)], fill=128)
        elif obstacle[1] == 'block':
            draw.rectangle([(x - block_size, y - block_size), (x + block_size, y + block_size)], fill=0)

    # draw.ellipse((2, 2, 8, 8), outline ='white')
    # draw.rectangle([(2, 9), (8, 15)], fill=0)

    data = list(image.getdata())
    # image.save("kkk.pgm")

    # declare 1-d array of white (255 pixel)
    buff = array.array('B')
    for b in data:
        buff.append(b)

    # open file for writing
    try:
      fout = open(file_name, 'wb')
    except:
      print("Cannot open file, Exiting … \n")
      sys.exit()


    # define PGM Header
    pgmHeader = 'P5' + '\n' + str(width) + ' ' + str(height)+ ' ' + '\n' + str(255) + '\n'
    pgmHeader = str.encode(pgmHeader)

    # write the header to the file
    fout.write(pgmHeader)

    # write the data to the file
    buff.tofile(fout)

    # close the file
    fout.close()
write_pgm_map('x.pgm', [((4, 20), "human"), ((18, 8), "block")])
