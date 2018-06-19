import os
import json
from pprint import pprint
from tkinter import *
from collections import defaultdict

# Plot settings
plot_scale = 10

# Grid for occupied areas in the map
grid_size = 40
grid = [[0 for x in range(grid_size)] for y in range(grid_size)]

# Tkinter canvas
master = Tk()
canvas = Canvas(master, width=plot_scale * grid_size, height=plot_scale * grid_size)

def get_rooms():
	rooms = defaultdict(list)
	for file in os.listdir("rooms"):
		with open("rooms/" + file, 'r') as f:
			j = json.load(f)
			rooms[j['name']] = j
	return rooms

available_rooms = get_rooms()

# rooms_in_map struct
# x, y, name, rotation (0, 90, 180, 270)
rooms_in_map = []

# unsatisfied exits contains x, y, direction
unsatisfied_exits = []


def add_room(name, x, y):
	if name in available_rooms.keys():
		rooms_in_map.append({"name" : name, "x": x, "y": y, "rotation": 0})
		for exit in available_rooms[name]['exits']:
			unsatisfied_exits.append({"x": x + exit['x'], "y": y + exit['y'], "direction": exit['direction']})


def plot_rooms(rooms_in_map, available_rooms, unsatisfied_exits):
	for room in rooms_in_map:
		print("plotting {} at {} {}:".format(room['name'], room['x'], room['y']))
		available_room = available_rooms[room['name']]
		x1 = room['x']
		y1 = room['y']
		x2 = x1 + available_room['width']
		y2 = y1 + available_room['height']
		canvas.create_rectangle(
			x1 * plot_scale,
			y1 * plot_scale,
			x2 * plot_scale, 
			y2 * plot_scale, 
			outline="blue", fill="lightgray")
		for exit in available_room['exits']:
			exit_x = x1 + exit['x']
			exit_y = y1 + exit['y']
			canvas.create_polygon(create_polygon_points(exit_x, exit_y, exit['direction']), fill="green")
	# Plot unsatisfied exits
	for exit in unsatisfied_exits:
		canvas.create_polygon(create_polygon_points(exit['x'], exit['y'], exit['direction']), fill="red")


def create_polygon_points(x, y, direction):
	points = []
	half_cell_height = 0.5
	cell_mid_x = x + half_cell_height
	cell_mid_y = y + half_cell_height
	points.append([(cell_mid_x) * plot_scale, (cell_mid_y) * plot_scale])
	if direction in ("up", "left"):
		points.append([x * plot_scale, y * plot_scale])
	if direction in ("down", "left"):
		points.append([x * plot_scale, (y + 1) * plot_scale])
	if direction in ("up", "right"):
		points.append([(x + 1) * plot_scale, y * plot_scale])
	if direction in ("down", "right"):
		points.append([(x + 1) * plot_scale, (y + 1) * plot_scale])
	
	print(points)
	return points


def draw_grid(grid_size, spacing):
	for x in range(0, grid_size, spacing):
		canvas.create_line(x * spacing, 0, x * spacing, grid_size * spacing, dash=(3,1))
		canvas.create_line(0, x * spacing, grid_size * spacing, (x * spacing), dash=(3,1))


add_room("mid1", 10, 10)
add_room("mid1", 20, 20)
plot_rooms(rooms_in_map, available_rooms, unsatisfied_exits)
draw_grid(grid_size, plot_scale)

canvas.pack()
mainloop()
