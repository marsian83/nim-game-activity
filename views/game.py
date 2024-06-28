# Copyright (C) 2024 Spandan Barve
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import math

import utils
import config

from components.board import Board
from components.robot import Robot
from components.button import Button
from components.common import Drawable


def view(game):
    buttons = []
    vw = game.vw
    vh = game.vh

    label = Drawable()
    label.gameDisplay = game.gameDisplay
    label.y = vh(10)

    robot_size = vh(30)
    robot = Robot(vw(95) - robot_size, vh(100) - robot_size, robot_size)

    robot_dialogue = {"msg" : "", "timer" : 0}
    def set_robot_dialogue(msg):
        robot_dialogue["timer"] = 300
        robot_dialogue["msg"] = msg

    def end_game(condition):
        label_img = utils.scale_image_maintain_ratio(
            config.images["label"][condition],
            h=vh(50))
        label.set_image_rect(label_img)
        label.set_image_rect(label.image, x = vw(50) - label.rect.w // 2)

    board = Board(vw(5), vh(3), vw(90), vh(60), set_robot_dialogue, end_game)
    board.generate_board(3, 9)

    def reset():
        set_robot_dialogue("")
        label.image = None
        board.generate_board(3, 9)
        
    reset_btn = Button(vw(5), vh(100 - 15), "RESET", vw(20), vh(10), font=config.font.xl)
    reset_btn.on_click = reset
    buttons.append(reset_btn)

    def update():
        board.update()
        robot.update()

        dialogue = config.font.xl.render(robot_dialogue["msg"], True, config.front_color)

        if (robot_dialogue["timer"] > 0):
            robot_dialogue["timer"] -= 1
        if (robot_dialogue["timer"] == 0):
            robot_dialogue["msg"] = ""
            robot_dialogue["timer"] = -1

        d_rect = dialogue.get_rect()
        d_rect.x = vw(93) - robot_size - d_rect.width
        d_rect.y = vh(100) - robot_size // 3 - d_rect.height
        game.gameDisplay.blit(dialogue, d_rect)

        for btn in buttons:
            btn.update()

        if label.image is not None:
            label.update()

    game.update_function = update
