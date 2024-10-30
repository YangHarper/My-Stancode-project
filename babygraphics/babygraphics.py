"""
File: babygraphics.py
Name: 
--------------------------------
SC101 Baby Names Project
Adapted from Nick Parlante's Baby Names assignment by
Jerry Liao.
"""

import tkinter
import babynames
import babygraphicsgui as gui

FILENAMES = [
    'data/full/baby-1900.txt', 'data/full/baby-1910.txt',
    'data/full/baby-1920.txt', 'data/full/baby-1930.txt',
    'data/full/baby-1940.txt', 'data/full/baby-1950.txt',
    'data/full/baby-1960.txt', 'data/full/baby-1970.txt',
    'data/full/baby-1980.txt', 'data/full/baby-1990.txt',
    'data/full/baby-2000.txt', 'data/full/baby-2010.txt',
    'data/full/baby-2020.txt'
]
CANVAS_WIDTH = 1080
CANVAS_HEIGHT = 600
YEARS = [1900, 1910, 1920, 1930, 1940, 1950,
         1960, 1970, 1980, 1990, 2000, 2010, 2020]
GRAPH_MARGIN_SIZE = 20
COLORS = ['red', 'purple', 'green', 'blue']
TEXT_DX = 2
LINE_WIDTH = 2
MAX_RANK = 1000


def get_x_coordinate(width, year_index):
    """
    Given the width of the canvas and the index of the current year
    in the YEARS list, returns the x coordinate of the vertical
    line associated with that year.

    Input:
        width (int): The width of the canvas
        year_index (int): The index where the current year is in the YEARS list
    Returns:
        x_coordinate (int): The x coordinate of the vertical line associated
                            with the current year.
    """
    # width = CANVAS_WIDTH
    x0 = GRAPH_MARGIN_SIZE
    # y0 = GRAPH_MARGIN_SIZE
    x_w = CANVAS_WIDTH - GRAPH_MARGIN_SIZE
    # y_w = CANVAS_HEIGHT - GRAPH_MARGIN_SIZE
    block_width = (x_w - x0) // len(YEARS)
    x = x0 + year_index * block_width
    return x


def draw_fixed_lines(canvas):
    """
    Draws the fixed background lines on the canvas.

    Input:
        canvas (Tkinter Canvas): The canvas on which we are drawing.
    """
    canvas.delete('all')            # delete all existing lines from the canvas

    # ----- Write your code below this line ----- #
    x0 = GRAPH_MARGIN_SIZE
    y0 = GRAPH_MARGIN_SIZE
    x_w = CANVAS_WIDTH-GRAPH_MARGIN_SIZE
    y_w = CANVAS_HEIGHT-GRAPH_MARGIN_SIZE
    # 加兩條橫線
    canvas.create_line(x0, y0, x_w, y0, width=LINE_WIDTH)
    canvas.create_line(x0, y_w, x_w, y_w, width=LINE_WIDTH)
    # 加中間直線

    for i in range(len(YEARS)):
        x = get_x_coordinate(CANVAS_WIDTH, i)
        # 畫直線
        canvas.create_line(x, 0, x, CANVAS_HEIGHT, width=LINE_WIDTH)
        # 標注年份
        canvas.create_text(x+TEXT_DX, y_w, text=YEARS[i],
                           anchor=tkinter.NW)


def draw_names(canvas, name_data, lookup_names):
    """
    Given a dict of baby name data and a list of name, plots
    the historical trend of those names onto the canvas.

    Input:
        canvas (Tkinter Canvas): The canvas on which we are drawing.
        name_data (dict): Dictionary holding baby name data
        lookup_names (List[str]): A list of names whose data you want to plot

    Returns:
        This function does not return any value.
    """
    draw_fixed_lines(canvas)        # draw the fixed background grid

    # ----- Write your code below this line ----- #
    # 將使用者輸入的name，與name_data比對吻合的，將所有data放入match_name
    match_name = {}
    for name in lookup_names:
        if name in name_data:
            match_name[name] = name_data[name]
        # 計算該名字使用哪種顏色
        color = COLORS[len(match_name) % len(COLORS)-1]   # 'red','purple'...

        # 記錄原始點座標
        previous_point = [None, None]

        # 取得 match_name 年份的x座標（用get_x_coordinate)
        for i in range(len(YEARS)):  # i=0,1,2...
            name_x = get_x_coordinate(CANVAS_WIDTH, i)

            # 如果有年份，計算x,y座標，在canvas上面標記
            if str(YEARS[i]) in match_name[name]:
                # 取得該年份rank並換算成y座標
                rank = match_name[name][str(YEARS[i])]
                # y刻度
                name_y = GRAPH_MARGIN_SIZE + (int(rank) / 1000 * 560)

                # 添加標籤
                label = f"{name} {rank}"
                canvas.create_text(name_x + TEXT_DX, name_y, text=label, fill=color, anchor='sw')

            # 如果沒有年份，y座標為貼底，並在原本名字旁邊顯示排名的地方就會換成 '' * ''
            else:
                name_y = CANVAS_HEIGHT - GRAPH_MARGIN_SIZE
                label = f"{name} *"
                canvas.create_text(name_x + TEXT_DX, name_y, text=label, fill=color, anchor='sw')

            # 繪製線條
            if previous_point[0] and previous_point[1]:
                canvas.create_line(previous_point[0], previous_point[1], name_x, name_y, fill=color, width=LINE_WIDTH)
            previous_point[0], previous_point[1] = name_x, name_y


# main() code is provided, feel free to read through it but DO NOT MODIFY
def main():
    # Load data
    name_data = babynames.read_files(FILENAMES)
    # for name, year in name_data.items():
    #     print(name_data[name])
    # Create the window and the canvas
    top = tkinter.Tk()
    top.wm_title('Baby Names')
    canvas = gui.make_gui(top, CANVAS_WIDTH, CANVAS_HEIGHT, name_data, draw_names, babynames.search_names)

    # Call draw_fixed_lines() once at startup so we have the lines
    # even before the user types anything.
    draw_fixed_lines(canvas)

    # This line starts the graphical loop that is responsible for
    # processing user interactions and plotting data
    top.mainloop()


if __name__ == '__main__':
    main()
