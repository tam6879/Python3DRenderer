# Moses, Tristan
# 1001_123_456
# 2024_10_14
# Assignment_02_01

import numpy as np
import tkinter as tk
import time
from tkinter import simpledialog, filedialog
# | I should have thought of this sooner, it makes the code so much more readable, lol
# V CONSTS#
X = U = 0
Y = V = 1
Z = N = 2

PARALLEL = 0
PERSPECTIVE = 1

FINE = 0
CLIPPED = 1
CULLED = 2

class cl_world:
    def __init__(self):
        
        ################## Main Window ########################
        # Initialize the main window
        self.root = tk.Tk()
        self.root.title("Resizable Window")
        # Set the window gemetry (Size) and Make it resizable
        self.root.geometry("650x750")
        self.root.resizable(True, True)
        ################### Top Pnael ##########################
        # Create a top frame for the button
        self.top_frame = tk.Frame(self.root)
        self.top_frame.pack(side=tk.TOP, fill=tk.X)
        self.rot_frame = tk.Frame(self.root)
        self.rot_frame.pack(side=tk.TOP, fill=tk.X)
        self.scale_frame = tk.Frame(self.root)
        self.scale_frame.pack(side=tk.TOP, fill=tk.X)
        self.trans_frame = tk.Frame(self.root)
        self.trans_frame.pack(side=tk.TOP, fill=tk.X)
        self.cam_frame = tk.Frame(self.root)
        self.cam_frame.pack(side=tk.TOP, fill=tk.X)
        # Create a button in the top panel
        self.brwose_button = tk.Button(self.top_frame, text="Select Model", fg="blue", command=self.browse_file_clicked)
        self.brwose_button.pack(side=tk.LEFT)
        self.brwose_button = tk.Button(self.top_frame, text="Select Camera Settings", fg="red", command=self.browse_cam_clicked)
        self.brwose_button.pack(side=tk.LEFT)
        self.draw_button = tk.Button(self.top_frame, text="Draw", command=self.draw_button_clicked)
        self.draw_button.pack(side=tk.LEFT, padx=1, pady=5)
        # Rotation layer
        self.rot_axis = tk.IntVar()
        self.rot_label = tk.Label(self.rot_frame, text="Rotation Axis: ")
        self.rot_label.pack(side=tk.LEFT)
        self.rot_x_axis_button = tk.Radiobutton(self.rot_frame, text="X", value=1, variable=self.rot_axis)
        self.rot_x_axis_button.pack(side=tk.LEFT)
        self.rot_y_axis_button = tk.Radiobutton(self.rot_frame, text="Y", value=2, variable=self.rot_axis)
        self.rot_y_axis_button.pack(side=tk.LEFT)
        self.rot_z_axis_button = tk.Radiobutton(self.rot_frame, text="Z", value=3, variable=self.rot_axis)
        self.rot_z_axis_button.pack(side=tk.LEFT)
        self.rot_ab_axis_button = tk.Radiobutton(self.rot_frame, text="Line AB", value=4, variable=self.rot_axis)
        self.rot_ab_axis_button.pack(side=tk.LEFT)
        self.rot_x_axis_button.select()
        self.rot_a_label = tk.Label(self.rot_frame, text="A:")
        self.rot_a_label.pack(side=tk.LEFT)
        self.rot_point_a_field = tk.Entry(self.rot_frame, width=10)
        self.rot_point_a_field.pack(side=tk.LEFT)
        self.rot_point_a_field.insert(tk.END, "[0.0,0.0,0.0]")
        self.rot_b_label = tk.Label(self.rot_frame, text="B:")
        self.rot_b_label.pack(side=tk.LEFT)
        self.rot_point_b_field = tk.Entry(self.rot_frame, width=10)
        self.rot_point_b_field.pack(side=tk.LEFT)
        self.rot_point_b_field.insert(tk.END, "[1.0,1.0,1.0]")
        self.rot_deg_label = tk.Label(self.rot_frame, text="Degree:")
        self.rot_deg_label.pack(side=tk.LEFT)
        self.rot_deg_field = tk.Entry(self.rot_frame, width=5)
        self.rot_deg_field.pack(side=tk.LEFT)
        self.rot_deg_field.insert(tk.END, "90")
        self.rot_steps_label = tk.Label(self.rot_frame, text="Steps:")
        self.rot_steps_label.pack(side=tk.LEFT)
        self.rot_steps_field = tk.Entry(self.rot_frame, width=5)
        self.rot_steps_field.pack(side=tk.LEFT)
        self.rot_steps_field.insert(tk.END, "5")
        self.rotate_button = tk.Button(self.rot_frame, text="Rotate", command=self.rotate, fg="blue")
        self.rotate_button.pack(side=tk.LEFT)
        # Scale layer
        varscale_type = tk.IntVar()
        self.scale_point_label = tk.Label(self.scale_frame, text="Scale about point:")
        self.scale_point_label.pack(side=tk.LEFT)
        self.scale_point_field = tk.Entry(self.scale_frame, width=10)
        self.scale_point_field.pack(side=tk.LEFT)
        self.scale_point_field.insert(tk.END, "[0.0,0.0,0.0]")
        self.scale_ratio_label = tk.Label(self.scale_frame, text="Scale ratio:")
        self.scale_ratio_label.pack(side=tk.LEFT)
        self.scale_ratio_all_button = tk.Label(self.scale_frame, text="All: ")
        self.scale_ratio_all_button.pack(side=tk.LEFT)
        self.scale_ratio_all_field = tk.Entry(self.scale_frame, width=5)
        self.scale_ratio_all_field.pack(side=tk.LEFT)
        self.scale_ratio_all_field.insert(tk.END, "1")
        self.scale_ratio_custom_button = tk.Label(self.scale_frame, text="[Sx,Sy,Sz]: ")
        self.scale_ratio_custom_button.pack(side=tk.LEFT)
        self.scale_ratio_custom_field = tk.Entry(self.scale_frame, width=5)
        self.scale_ratio_custom_field.pack(side=tk.LEFT)
        self.scale_ratio_custom_field.insert(tk.END, "[1,1,1]")
        self.scale_steps_label = tk.Label(self.scale_frame, text="Steps:")
        self.scale_steps_label.pack(side=tk.LEFT)
        self.scale_steps_field = tk.Entry(self.scale_frame, width=5)
        self.scale_steps_field.pack(side=tk.LEFT)
        self.scale_steps_field.insert(tk.END, "5")
        self.scale_button = tk.Button(self.scale_frame, text="Scale Uniform", command=self.scale_all, fg="blue")
        self.scale_button.pack(side=tk.LEFT)
        self.scale_button = tk.Button(self.scale_frame, text="Scale Custom", command=self.scale_custom, fg="blue")
        self.scale_button.pack(side=tk.LEFT)
        # Translate Layer
        self.trans_steps = tk.IntVar(self.trans_frame)
        self.trans_point_label = tk.Label(self.trans_frame, text="Translation [dx,dy,dz]: ")
        self.trans_point_label.pack(side=tk.LEFT)
        self.trans_point_field = tk.Entry(self.trans_frame, width=10)
        self.trans_point_field.pack(side=tk.LEFT)
        self.trans_point_field.insert(tk.END, "[-0.5,-0.6,0.5]")
        self.trans_steps_label = tk.Label(self.trans_frame, text="Steps:")
        self.trans_steps_label.pack(side=tk.LEFT)
        self.trans_steps_field = tk.Entry(self.trans_frame, width=5)
        self.trans_steps_field.pack(side=tk.LEFT)
        self.trans_steps_field.insert(tk.END, "5")
        self.trans_button = tk.Button(self.trans_frame, text="Translate", command=self.translation, fg="blue")
        self.trans_button.pack(side=tk.LEFT)
        # Cam Layer
        self.current_vrp_label = tk.Label(self.cam_frame, text="Current VRP([x,y,z]): ")
        self.current_vrp_label.pack(side=tk.LEFT)
        self.current_vrp_field = tk.Entry(self.cam_frame, width=10)
        self.current_vrp_field.pack(side=tk.LEFT)
        self.current_vrp_field.insert(tk.END, "[0.0,0.0,0.0]")
        self.target_vrp_label = tk.Label(self.cam_frame, text="Target VRP([x,y,z]): ")
        self.target_vrp_label.pack(side=tk.LEFT)
        self.target_vrp_field = tk.Entry(self.cam_frame, width=10)
        self.target_vrp_field.pack(side=tk.LEFT)
        self.target_vrp_field.insert(tk.END, "[1.0,1.0,1.0]")
        self.cam_steps_label = tk.Label(self.cam_frame, text="Steps:")
        self.cam_steps_label.pack(side=tk.LEFT)
        self.cam_steps_field = tk.Entry(self.cam_frame, width=5)
        self.cam_steps_field.pack(side=tk.LEFT)
        self.cam_steps_field.insert(tk.END, "10")
        self.cam_button = tk.Button(self.cam_frame, text="Fly Camera", command=self.translation, fg="blue")
        self.cam_button.pack(side=tk.LEFT)

        ################### Canvas #############################
        # Create a canvas to draw on
        self.canvas = tk.Canvas(self.root, bg="dim gray")
        self.canvas.pack(fill=tk.BOTH, expand=True)
        # Bind the resize event to redraw the canvas when window is resized
        self.canvas.bind("<Configure>", self.canvas_resized)
        #################### Bottom Panel #######################
        # Create a bottom frame for displaying messages
        self.bottom_frame = tk.Frame(self.root)
        self.bottom_frame.pack(side=tk.BOTTOM, fill=tk.X)
        # Create a lebel for showing messages
        self.message_label = tk.Label(self.bottom_frame, text="")
        self.message_label.pack(padx=10, pady=10)
        ##################### New Stuff ########################
        self.vertex_count = 0
        self.face_count = 0
        self.vertices = [None]
        self.faces = []
        self.lines = []
        self.vmin = [0,0]
        self.vmax = [0,0]
        self.wmin = [0,0]
        self.wmax = [0,0]
        self.objects = []
        self.file_loaded = False
        self.cam_loaded = False
        self.object_drawn = False
        self.width = 0.0
        self.height = 0.0     
        self.outline_color = 'black'
        self.fill_color = 'cyan'
        # view reference point
        self.vrp = [0.0, 0.0, 0.0]
        # view point normal
        self.vpn = [0.0, 0.0, 1.0]
        # view point up
        self.vup = [0.0, 1.0, 0.0]
        # Parallel Reference Point
        self.prp = [0.0, 0.0, 1.0]
        # Direction of Projection
        self.dop = [0.0, 0.0, 1.0]
        # [umin, vmin, nmin]
        self.min = [-1, -1, -1]
        # [umax, vmax, nmax]
        self.max = [1, 1, 1]
        # viewport size [xmin, xmax, ymin, ymax]
        self.viewport = [0.1, 0.4, 0.1, 0.4]
        # camera name
        self.cam_name = ""
        # render mode
        self.render_mode = PARALLEL
        # boundries stored by actual pixel values [xmin, ymin, zmin]
        self.min_view_bounds = [0, 0, 0]
        self.max_view_bounds = [1, 1, 1]

        
        
        

    def browse_file_clicked(self):
        self.file_path = tk.filedialog.askopenfilename(filetypes=[("allfiles", "*"), ("pythonfiles", "*.txt")])
        self.message_label.config(text=self.file_path)
        self.load_file(self.file_path)
    
    def browse_cam_clicked(self):
        self.file_path = tk.filedialog.askopenfilename(filetypes=[("allfiles", "*"), ("pythonfiles", "*.txt")])
        self.message_label.config(text=self.file_path)
        self.load_cam_file(self.file_path)
    
    def load_cam_file(self, filename):
        # open the file in readmode
        self.t_file = open(filename, 'r')
        # if the file is null, abort
        if not self.t_file:
            return
        # mark that the cam file has been loaded
        self.cam_loaded = True
        # get all the lines of the file
        Lines = self.t_file.readlines()
        # for each line in the file...
        for t_line in Lines:
            # split them up by the spaces
            t_split = t_line.split(' ')
            if t_split[0] == 'i': ### CAM NAME ###
                self.cam_name = t_split[1]
            elif t_split[0] == 't': ### RENDER MODE ###
                self.render_mode = PERSPECTIVE if t_split[1] == "Perspective" else PARALLEL
            elif t_split[0] == 'r': ### VRP ###
                self.vrp = np.array([float(t_split[X + 1]), float(t_split[Y + 1]), float(t_split[Z + 1])])
            elif t_split[0] == 'n': ### VPN ###
                self.vpn = np.array([float(t_split[X + 1]), float(t_split[Y + 1]), float(t_split[Z + 1])])
            elif t_split[0] == 'u': ### VUP ###
                self.vup = np.array([float(t_split[X + 1]), float(t_split[Y + 1]), float(t_split[Z + 1])])
            elif t_split[0] == 'p': ### PRP ###
                self.prp = np.array([float(t_split[X + 1]), float(t_split[Y + 1]), float(t_split[Z + 1])])
            elif t_split[0] == 'w': ### VIEW VOLUME ###
                self.min = np.array([float(t_split[1]), float(t_split[3]), float(t_split[5])])
                self.max = np.array([float(t_split[2]), float(t_split[4]), float(t_split[6])])
            elif t_split[0] == 's': ### VIEWPORT ###
                self.viewport = np.array([float(t_split[1]), float(t_split[3]), float(t_split[2]), float(t_split[4])])


    def load_file(self,filename):
        # clear all cached objects
        self.objects.clear()
        self.vertices = [None]
        self.faces.clear()
        self.vertex_count = 0
        self.face_count = 0
        # open the file in readmode
        self.t_file = open(filename, 'r')
        # if the file is null, abort
        if not self.t_file:
            return
        # mark that a file has been loaded
        self.file_loaded = True
        self.object_drawn = False
        # get all the lines of the file
        Lines = self.t_file.readlines()
        # for each line in the file...
        for t_line in Lines:
            # split them up by the spaces
            t_split = t_line.split(' ')
            # print("t_split: ", t_split)
            # read the first char to determine what's being read
            if t_split[0] == 'v': ### VERTICES ###
                # add to the vertex count (do this FIRST because the faces use 1s indexing)
                self.vertex_count += 1
                # add it to the list of vertices
                self.vertices.append(np.array([float(t_split[X + 1]), float(t_split[Y + 1]), float(t_split[Z + 1])]))
                #print("vert: ", self.vertices[self.vertex_count])
            elif t_split[0] == 'f': ### FACES ###
                # add the face to the faces list
                n = len(t_split)
                t_face = []
                for v in range(1, n):
                    if t_split[v] != '\n': t_face.append(int(t_split[v]))
                self.faces.append(t_face)
                # self.faces.append([int(t_split[1]), int(t_split[2]), int(t_split[3][:-1])])
                #print("face: ", self.faces[self.face_count])
                # increment the face count (do this SECOND because we don't need to use 1s indexing here)
                self.face_count += 1 
            elif t_split[0] == 'w': ### WINDOW ###
                # get window paramaters
                self.wmin = [float(t_split[1]), float(t_split[2])]
                self.wmax = [float(t_split[3]), float(t_split[4])]
            elif t_split[0] == 's': ### VIEWPORT ###
                # get viewport parameters
                self.vmin = [float(t_split[1]), float(t_split[2])]
                self.vmax = [float(t_split[3]), float(t_split[4])]
            else:
                return

    def re_draw_objects(self,event=None):
        # get window size if we somehow don't have it
        if self.width == 0: self.width = float(self.canvas.cget("width"))
        if self.height == 0: self.height = float(self.canvas.cget("height")) 
        # get bounds of the viewport
        self.left_bound = self.width * self.viewport[0]
        self.right_bound = self.width * self.viewport[1]
        self.lower_bound = self.height * self.viewport[2]
        self.upper_bound = self.height * self.viewport[3]
        # get the width of the box
        x_scale = (self.right_bound - self.left_bound)
        # get the number of increments of 1 that it takes to cross it (bounds -2 -> 2 would be 4)
        x_inc_len = (self.max[U] - self.min[U])
        # get the increment length in pixels
        x_increment = 0 if not x_inc_len else x_scale / x_inc_len
        # do all the same stuff but for the y axis
        y_scale = (self.upper_bound - self.lower_bound)
        y_inc_len = (self.max[V] - self.min[V])
        y_increment = 0 if not y_inc_len else y_scale / y_inc_len
        # get the point that should be the origin
        origin = [self.left_bound - self.min[X] * x_increment, self.upper_bound + self.min[Y] * y_increment]
        self.max_view_bounds = [self.right_bound, self.lower_bound, self.max[N] ]
        self.min_view_bounds = [self.left_bound, self.upper_bound, self.min[N] ]
        #print("origin: ", origin, "\nx_scale: ", x_scale, "\ny_scale: ", y_scale, "\nx_inc_leng: ", x_inc_leng, "\ny_inc_len: ", y_inc_len, "\nx_increment: ", x_increment, "\ny_increment: ", y_increment)
        # draw a rectangle to represent the viewport
        self.canvas.coords(self.objects[0], int(self.left_bound), int(self.upper_bound), int(self.right_bound), int(self.lower_bound))
        # draw each face
        n = len(self.objects)
        for i in range(1, n):
            # get points
            t_line = self.lines[(i - 1)]
            # get clip results
            clip_res = self.clip_line(t_line)
            # get the new clipped line (same line if culled or completely in bounds)
            clipped_line = clip_res[1]
            # clipped_line = [self.vertices[clip_res[0]], self.vertices[clip_res[1]]]
            # print("t_line: ", t_line)
            self.canvas.coords(self.objects[i], clipped_line[0][X] * x_increment + origin[X], clipped_line[0][Y] * y_increment + origin[Y], clipped_line[1][X] * x_increment + origin[X], clipped_line[1][Y] * y_increment + origin[Y])
            # print("redrawing line: A: ", self.vertices[t_line[0]][X] * x_increment + origin[X], " ", self.vertices[t_line[0]][Y] * y_increment + origin[Y], " -> B: ", self.vertices[t_line[1]][X] * x_increment + origin[X], " ", self.vertices[t_line[1]][Y] * y_increment + origin[Y])
            # if the item is culled set its mode to be hidden
            if clip_res[0]: self.canvas.itemconfigure(self.objects[i], state = "normal")
            else: self.canvas.itemconfigure(self.objects[i], state = "hidden")

            # if v_n == 3: self.canvas.coords(self.objects[i], t_verts[0][X], t_verts[0][Y], t_verts[1][X], t_verts[1][Y], t_verts[2][X], t_verts[2][Y])
            # this is for the teapot lid specifically, because it has 4 verts in each face
            # elif v_n == 4: self.canvas.coords(self.objects[i], t_verts[0][X], t_verts[0][Y], t_verts[1][X], t_verts[1][Y], t_verts[2][X], t_verts[2][Y], t_verts[3][X], t_verts[3][Y])
    
    def draw_objects(self,event=None):
        # if no object or camera has been loaded return
        if not (self.file_loaded and self.cam_loaded): 
            return
        # if we have already cached objects, call redraw instead
        if self.objects:
            self.re_draw_objects()
            return
        self.object_drawn = True
        # clear the canvas
        self.canvas.delete("all")
        # get window size if we somehow don't have it
        if self.width == 0: self.width = float(self.canvas.cget("width"))
        if self.height == 0: self.height = float(self.canvas.cget("height")) 
        # get bounds of the viewport
        self.left_bound = self.width * self.viewport[0]
        self.right_bound = self.width * self.viewport[1]
        self.lower_bound = self.height * self.viewport[2]
        self.upper_bound = self.height * self.viewport[3]
        
        # print("origin: ", origin, "\nx_scale: ", x_scale, "\ny_scale: ", y_scale, "\nx_inc_leng: ", x_inc_len, "\ny_inc_len: ", y_inc_len, "\nx_increment: ", x_increment, "\ny_increment: ", y_increment)
        # draw a rectangle to represent the viewport
        self.objects.append(self.canvas.create_rectangle(int(self.left_bound), int(self.upper_bound), int(self.right_bound), int(self.lower_bound)))
        # print("origin: ", origin, " x_increment: ", x_increment, " y_increment: ", y_increment)
        print("Before Parallel Projection: vrp: ", self.vrp, " vpn: ", self.vpn, " vup: ", self.vup, " prp: ", self.prp, " volume min: ", self.min, " volume max: ", self.max , " viewport: ", self.viewport)

        print("STEP 1: translate VRP to origin")
        print("vrp before trans: ", self.vrp)
        vrp_trans = self.vrp * -1
        self.vrp += vrp_trans
        print("vrp after trans: ", self.vrp)

        print("STEP 2: rotate vpn on the x axis to be 0 on y axis") 
        print("vpn before rx: ", self.vpn)
        print("vup before rx: ", self.vup)
        theta_x = np.arctan(self.vpn[Y] / self.vpn[Z])
        self.vpn = [self.vpn[X], np.cos(theta_x) * self.vpn[Y] - np.sin(theta_x) * self.vpn[Z], np.sin(theta_x) * self.vpn[Y] + np.cos(theta_x) * self.vpn[Z]]
        self.vup = [self.vup[X], np.cos(theta_x) * self.vup[Y] - np.sin(theta_x) * self.vup[Z], np.sin(theta_x) * self.vup[Y] + np.cos(theta_x) * self.vup[Z]]
        if self.vpn[Z] < 0.0:
            print("rotate another 180")
            rad180 = np.deg2rad(180.0)
            theta_x += rad180
            self.vpn = [self.vpn[X], np.cos(rad180) * self.vpn[Y] - np.sin(rad180) * self.vpn[Z], np.sin(rad180) * self.vpn[Y] + np.cos(rad180) * self.vpn[Z]]
            self.vup = [self.vup[X], np.cos(rad180) * self.vup[Y] - np.sin(rad180) * self.vup[Z], np.sin(rad180) * self.vup[Y] + np.cos(rad180) * self.vup[Z]]
        print("vpn after rx: ", self.vpn)
        print("vup after rx: ", self.vup)

        print("STEP 3: rotate vpn on the y axis to be 0 on x axis") 
        print("vpn before ry: ", self.vpn)
        print("vup before ry: ", self.vup)
        theta_y = np.arctan(self.vpn [X] / self.vpn [Z])
        self.vpn  = [np.cos(theta_y) * self.vpn [X] - np.sin(theta_y) * self.vpn [Z], self.vpn[Y], np.sin(theta_y) * self.vpn [X] + np.cos(theta_y) * self.vpn[Z]]
        self.vup  = [np.cos(theta_y) * self.vup [X] - np.sin(theta_y) * self.vup [Z], self.vup[Y], np.sin(theta_y) * self.vup [X] + np.cos(theta_y) * self.vup[Z]]
        # if vpn is negative, rotate it another 180 degrees
        if self.vpn[Z] < 0.0:
            rad180 = np.deg2rad(180.0)
            theta_y += rad180
            self.vpn  = [np.cos(rad180) * self.vpn [X] - np.sin(rad180) * self.vpn [Z], self.vpn[Y], np.sin(rad180) * self.vpn [X] + np.cos(rad180) * self.vpn[Z]]
            self.vup  = [np.cos(rad180) * self.vup [X] - np.sin(rad180) * self.vup [Z], self.vup[Y], np.sin(rad180) * self.vup [X] + np.cos(rad180) * self.vup[Z]]
        print("vpn after ry: ", self.vpn)
        print("vup after ry: ", self.vup)

        print("STEP 4: rotate vup on the z axis to be 0 on x axis") 
        print("vpn before rz: ", self.vpn)
        print("vup before rz: ", self.vup)
        theta_z = np.arctan(self.vup [X] / self.vup [Y])
        self.vpn  = [np.cos(theta_z) * self.vpn [X] - np.sin(theta_z) * self.vpn [Y], np.cos(theta_z) * self.vpn [Y] + np.sin(theta_z) * self.vpn [X], self.vpn[Z]]
        self.vup  = [np.cos(theta_z) * self.vup [X] - np.sin(theta_z) * self.vup [Y], np.cos(theta_z) * self.vup [Y] + np.sin(theta_z) * self.vup [X], self.vup[Z]]
        if self.vup[Y] < 0.0:
            print("rotate another 180")
            rad180 = np.deg2rad(180.0)
            theta_z += rad180
            self.vpn  = [np.cos(rad180) * self.vpn [X] - np.sin(rad180) * self.vpn [Y], np.cos(rad180) * self.vpn [Y] + np.sin(rad180) * self.vpn [X], self.vpn[Z]]
            self.vup  = [np.cos(rad180) * self.vup [X] - np.sin(rad180) * self.vup [Y], np.cos(rad180) * self.vup [Y] + np.sin(rad180) * self.vup [X], self.vup[Z]]
        print("vpn after rz: ", self.vpn)
        print("vup after rz: ", self.vup)
        
        print("STEP 5: Shear dop to be parallel to z axis ( x and y = 0 )")
        shx = -(self.prp[X] - (self.min[U] + self.max[U]) / 2.0) / self.prp[Z]
        print("PRP before Shx: ", self.prp)
        self.prp[X] = (self.prp[X] + shx * self.prp[Z])
        print("PRP after Shx: ", self.prp)
        shy = -(self.prp[Y] - (self.min[V] + self.max[V]) / 2.0) / self.prp[Z]
        print("PRP before Shy: ", self.prp)
        self.prp[Y] = (self.prp[Y] + shy * self.prp[Z])
        print("PRP after Shy: ", self.prp)
    
        print("STEP 6: Translate the lower left corner to origin")
        view_trans = np.array([-(self.min[U] + self.max[U]) / 2.0, -(self.min[V] + self.max[V]) / 2.0, -self.min[N]])
        print("Translation: ", view_trans)
        print("VRP before translate: ", self.vrp)
        print("PRP before translate: ", self.prp)
        self.min += view_trans
        self.max += view_trans
        self.vrp += view_trans 
        self.prp += view_trans
        print("VRP after translate: ", self.vrp)
        print("PRP after translate: ", self.prp)

        print("STEP 7: Scale the view to be tha canonical view")
        view_scale = np.array([2.0 / (self.max[U] - self.min[U]), 2.0 / (self.max[V] - self.min[V]), 1.0 / (self.max[N] - self.min[N])])
        print("view_scale = ", view_scale)
        print("VRP before scale: ", self.vrp)
        print("PRP before scale: ", self.prp)
        self.min *= view_scale
        self.max *= view_scale
        self.vrp *= view_scale
        self.prp *= view_scale
        print("VRP after scale: ", self.vrp)
        print("PRP after scale: ", self.prp)

        # get the width of the box
        x_scale = (self.right_bound - self.left_bound)
        # get the number of increments of 1 that it takes to cross it (bounds -2 -> 2 would be 4)
        x_inc_len = (self.max[U] - self.min[U])
        # get the increment length in pixels
        x_increment = 0 if not x_inc_len else x_scale / x_inc_len
        # do all the same stuff but for the y axis
        y_scale = (self.upper_bound - self.lower_bound)
        y_inc_len = (self.max[V] - self.min[V])
        y_increment = 0 if not y_inc_len else y_scale / y_inc_len
        # get the point that should be the origin
        origin = [self.left_bound - self.min[X] * x_increment, self.upper_bound + self.min[Y] * y_increment]

        print("After Parallel Projection: vrp: ", self.vrp, " vpn: ", self.vpn, " vup: ", self.vup, " prp: ", self.prp, " volume min: ", self.min, " volume max: ", self.max , " viewport: ", self.viewport)
        # origin = [self.vrp[X] * x_increment + left_bound, self.vrp[Y] * y_increment + upper_bound]
        # now do all that bullshit ^ to every vert
        for i in range(1, len(self.vertices)):
            t_vert = self.vertices[i]
            print("initial vert: ", i, " = ", t_vert)
            # step 1 translate
            t_vert += vrp_trans
            print("translate vert: ", i, " = ", t_vert)
            # step 2 rotate x
            t_vert = [t_vert[X], np.cos(theta_x) * t_vert[Y] - np.sin(theta_x) * t_vert[Z], np.sin(theta_x) * t_vert[Y] + np.cos(theta_x) * t_vert[Z]]
            print("rotate x vert: ", i, " = ", t_vert)
            # step 3 rotate y
            t_vert = [np.cos(theta_y) * t_vert [X] - np.sin(theta_y) * t_vert [Z], t_vert[Y], np.sin(theta_y) * t_vert [X] + np.cos(theta_y) * t_vert[Z]]
            print("rotate y vert: ", i, " = ", t_vert)
            # step 4 rotate z
            t_vert = [np.cos(theta_z) * t_vert [X] - np.sin(theta_z) * t_vert [Y], np.cos(theta_z) * t_vert [Y] + np.sin(theta_z) * t_vert [X], t_vert[Z]]
            print("rotate z vert: ", i, " = ", t_vert)
            # step 5 shear
            t_vert = [(t_vert[X] + shx * t_vert[Z]), (t_vert[Y] + shy * t_vert[Z]), t_vert[Z]]
            print("shear vert: ", i, " = ", t_vert)
            # step 6 translate
            t_vert += view_trans
            print("translate vert: ", i, " = ", t_vert)
            # step 7 scale
            t_vert *= view_scale
            print("(final) scale vert: ", i, " = ", t_vert)
            # apply the transformations
            self.vertices[i] = t_vert
        
        # draw each face
        for t_face in self.faces:
            # if the face is null somehow, continue
            if not t_face: continue
            # get the number of verts in the face
            v_n = len(t_face)
            # if there are less than 3 points, it's not a polygon
            if v_n < 3: continue
            # get all the verts
            verts = []
            for i in range(v_n):
                verts.append([origin[X] + self.vertices[t_face[i]][X] * x_increment , origin[Y] - self.vertices[t_face[i]][Y] * y_increment])
            # this is for triangles, most files use this

            for i in range(v_n):
                j = i + 1 if i + 1 < v_n else 0
                self.lines.append(np.array([t_face[i], t_face[j]]))
                self.objects.append(self.canvas.create_line(verts[i][X], verts[i][Y], verts[j][X], verts[j][Y], fill = "cyan"))
                print("creating line: A: ", verts[i], " -> B: ", verts[j])


            # if v_n == 3: self.objects.append(self.canvas.create_polygon(verts[0][X], verts[0][Y], verts[1][X], verts[1][Y], verts[2][X], verts[2][Y], fill = '', outline = self.outline_color))
            # this one is pretty much just for the teapot lid, because each face has 4 verts
            # if v_n == 4: self.objects.append(self.canvas.create_polygon(verts[0][X], verts[0][Y], verts[1][X], verts[1][Y], verts[2][X], verts[2][Y], verts[3][X], verts[3][Y], fill = '', outline=self.outline_color))
        self.re_draw_objects()
        self.message_label.config(text="Object is drawn :)")

        print("CLIPPING TEST 1")
        # print(self.get_intersect(np.array([-1.0,    -1.055]), np.array([-1.0,    -1.055]), np.array([-1.0, -1.0]), np.array([-1.0, 1.0])))
    
    left_bound = 0
    right_bound = 0
    upper_bound = 0
    lower_bound = 0
    front_bound = 0
    back_bound = 0

    def perp(self, a) :
        b = np.empty_like(a)
        b[0] = -a[1]
        b[1] = a[0]
        return b


    def get_intersect(self, a1,a2, b1,b2, a_outside) :
        print("A: ", a1, " B: ", a2, " C: ", b1, " D: ", b2)
        a1 = np.array(a1)
        a2 = np.array(a2)
        b1 = np.array(b1)
        b2 = np.array(b2)
        da = a2-a1
        db = b2-b1
        dp = a1-b1
        print("da: ", da, " db: ", db, " dp: ", dp)
        dap = self.perp(da)
        print("dap: ", dap)
        denom = np.dot( dap, db)
        if denom == 0: return a1 if a_outside else a2
        print("denom: ", denom)
        num = np.dot( dap, dp )
        print("num: ", num)
        print("intersection = ", (num / denom.astype(float))*db + b1)
        return (num / denom.astype(float))*db + b1
        



    def clip_line(self, t_line):
        # get both points A and B
        print("t_line: ", t_line)
        a = np.copy(self.vertices[t_line[0]])
        b = np.copy(self.vertices[t_line[1]])
        print("clipping line A: ", a, " to B: ", b)
        # get codes for a and B
        # -1 = below bound, 0 = within bounds, 1 = above bound
        # if abs(code_a[X] + code_b[X]) == 2 then it is not crossing the view
        code_a = [0, 0, 0]
        code_b = [0, 0, 0]
        
        # get on the x axis
        if a[X] < self.min[X]: code_a[X] = -1
        else: code_a[X] = 1 if a[X] > self.max[X] else 0
        if b[X] < self.min[X]: code_b[X] = -1
        else: code_b[X] = 1 if a[X] > self.max[X] else 0
        within_x = np.abs(code_a[X] + code_b[X]) != 2

        # now the y axis
        if a[Y] < self.min[Y]: code_a[Y] = -1
        else: code_a[Y] = 1 if a[Y] > self.max[Y] else 0
        if b[Y] < self.min[Y]: code_b[Y] = -1
        else: code_b[Y] = 1 if a[Y] > self.max[Y] else 0
        within_y = np.abs(code_a[Y] + code_b[Y]) != 2

        # now the z axis
        # if a[Z] < self.min[Z]: code_a[Z] = -1
        # else: code_a[Z] = 1 if a[Z] > self.max[Z] else 0
        # if b[Z] < self.min[Z]: code_b[Z] = -1
        # else: code_b[Z] = 1 if a[Z] > self.max[Z] else 0
        # within_z = np.abs(code_a[Z] + code_b[Z]) != 2
        within_z = True

        print("code a: ", code_a, " code b: ", code_b)
        print("within x: ", within_x, " within y: ", within_y, " within z: ", within_z)

        # if the line is totally out of bounds on one of the axis, return false to cull the line
        if (not within_x or not within_y or not within_z): return [False, [a, b]]
        return_value = [True, [a, b]]
        # if all the codes are 0 then it is totally in bounds and can be drawn normally
        if (code_a == [0, 0, 0] and code_b == [0, 0, 0]): return return_value
        # otherwise, we get to the hard part...
        # if A is off the left side and B is not
        if code_a[X] == -1 and code_b[X] != -1:
            # then replace a with the intersection point of ab and the left boundry
            t_point = self.get_intersect(a[:-1], b[:-1], np.array([self.min[X], self.max[Y]]), np.array([self.min[X], self.min[Y]]), True)
            a[X] = t_point[X]
            a[Y] = t_point[Y]
        # if B is off the left side and A is not
        elif code_b[X] == -1 and code_a[X] != -1:
            # then replace a with the intersection point of ab and the left boundry
            t_point = self.get_intersect(a[:-1], b[:-1], np.array([self.min[X], self.max[Y]]), np.array([self.min[X], self.min[Y]]), False)
            b[X] = t_point[X]
            b[Y] = t_point[Y]
        # if A is off the right side and B is not
        if code_a[X] == 1 and code_b[X] != 1:
            # then replace a with the intersection point of ab and the left boundry
            t_point = self.get_intersect(a[:-1], b[:-1], np.array([self.max[X], self.max[Y]]), np.array([self.max[X], self.min[Y]]), True)
            a[X] = t_point[X]
            a[Y] = t_point[Y]
        # if B is off the right side and A is not
        elif code_b[X] == 1 and code_a[X] != 1:
            # then replace a with the intersection point of ab and the left boundry
            t_point = self.get_intersect(a[:-1], b[:-1], np.array([self.max[X], self.max[Y]]), np.array([self.max[X], self.min[Y]]), False)
            b[X] = t_point[X]
            b[Y] = t_point[Y]
        
        # if A is off the top side and B is not
        if code_a[Y] == -1 and code_b[Y] != -1:
            # then replace a with the intersection point of ab and the left boundry
            t_point = self.get_intersect(a[:-1], b[:-1], np.array([self.min[Y], self.max[X]]), np.array([self.min[Y], self.min[X]]), True)
            a[X] = t_point[X]
            a[Y] = t_point[Y]
        # if B is off the top side and A is not
        elif code_b[Y] == -1 and code_a[Y] != -1:
            # then replace a with the intersection point of ab and the left boundry
            t_point = self.get_intersect(a[:-1], b[:-1], np.array([self.min[Y], self.max[X]]), np.array([self.min[Y], self.min[X]]), False)
            b[X] = t_point[X]
            b[Y] = t_point[Y]
        # if A is off the bottom side and B is not
        if code_a[Y] == 1 and code_b[Y] != 1:
            # then replace a with the intersection point of ab and the left boundry
            t_point = self.get_intersect(a[:-1], b[:-1], np.array([self.max[Y], self.max[X]]), np.array([self.max[Y], self.min[X]]), True)
            a[X] = t_point[X]
            a[Y] = t_point[Y]
        # if B is off the bottom side and A is not
        elif code_b[Y] == 1 and code_a[Y] != 1:
            # then replace a with the intersection point of ab and the left boundry
            t_point = self.get_intersect(a[:-1], b[:-1], np.array([self.max[Y], self.max[X]]), np.array([self.max[Y], self.min[X]]), False)
            b[X] = t_point[X]
            b[Y] = t_point[Y]
        print("clipped points: ", [a, b])
        return [True, [a, b]]

       



    

    def draw_button_clicked(self):
        self.draw_objects()
    
    def canvas_resized(self,event):
        self.width, self.height = event.width, event.height
        # if there is stuff on the canvas
        if self.canvas.find_all():
            # reconfigure canvas width and height
            self.canvas.config(width=event.width, height=event.height)
            self.canvas.pack()
            # draw objects (should go to redraw)
            self.draw_objects()
    
    def rotate(self):
        type = self.rot_axis.get()
        if type == 1: # X axis
            self.rotate_x()
        elif type == 2: # Y axis
            self.rotate_y()
        elif type == 3: # Z axis
            self.rotate_z()
        else: # Custom axis
            self.rotate_custom()

    def rotate_x(self):
        # if there is no object drawn, return
        if not self.object_drawn: return
        try:
            # try to get steps
            steps = int(self.rot_steps_field.get())
            # get degrees
            deg = np.deg2rad(float(self.rot_deg_field.get()))
            print("deg: ", float(self.rot_deg_field.get()), " rads: ", deg)
        except:
            print("INVALID PARAMETERS")
            return
        # get vertex count
        v_count = len(self.vertices)
        deg_step = deg / steps
        # I really didn't want to do this, but I could NOT get it to work without caching the original verts :(
        original_verts = self.vertices.copy()
        print("deg step: ", float(self.rot_deg_field.get()) / steps, " rad step: ", deg_step)
        print("cos(deg_step): ", np.cos(deg_step), " sin(deg_step): ", np.sin(deg_step))
        
        # for each step
        for i in range(1, steps + 1):
            theta = deg_step * i
            print("theta rads: ", theta, " theta degs: ", np.rad2deg(theta), " cos(theta): ", round(np.cos(theta), 8), " sin(theta): ", round(np.sin(theta), 8))
            # for each vertex (except the first one)
            for j in range(1, v_count):
                t_vert = original_verts[j].copy()
                # rx = [x, cosy - sinz, siny + cosz]
                t_vert = [t_vert[X], (round(np.cos(theta), 8) * t_vert[Y]) - round((np.sin(theta) * t_vert[Z]), 8), (round(np.sin(theta), 8) * t_vert[Y]) + round((np.cos(theta) * t_vert[Z]), 8)]
                self.vertices[j] = t_vert
            # redraw objects after updating all verts and force an update
            self.re_draw_objects()
            self.root.update()

    def rotate_y(self):
        # if there is no object drawn, return
        if not self.object_drawn: return
        try:
            # try to get steps
            steps = int(self.rot_steps_field.get())
            # get degrees
            deg = np.deg2rad(float(self.rot_deg_field.get()))
            print("deg: ", float(self.rot_deg_field.get()), " rads: ", deg)
        except:
            print("INVALID PARAMETERS")
            return
        # get vertex count
        v_count = len(self.vertices)
        deg_step = deg / steps
        # I really didn't want to do this, but I could NOT get it to work without caching the original verts :(
        original_verts = self.vertices.copy()
        print("deg step: ", float(self.rot_deg_field.get()) / steps, " rad step: ", deg_step)
        print("cos(deg_step): ", np.cos(deg_step), " sin(deg_step): ", np.sin(deg_step))
        
        # for each step
        for i in range(1, steps + 1):
            theta = deg_step * i
            print("theta rads: ", theta, " theta degs: ", np.rad2deg(theta), " cos(theta): ", round(np.cos(theta), 8), " sin(theta): ", round(np.sin(theta), 8))
            # for each vertex (except the first one)
            for j in range(1, v_count):
                t_vert = original_verts[j].copy()
                # ry = [cosx - sinz, y, sinx + cosz]
                t_vert = [(round(np.cos(theta), 8) * t_vert[X]) - round((np.sin(theta) * t_vert[Z]), 8), t_vert[Y], (round(np.sin(theta), 8) * t_vert[X]) + round((np.cos(theta) * t_vert[Z]), 8)]
                self.vertices[j] = t_vert
            # redraw objects after updating all verts and force an update
            self.re_draw_objects()
            self.root.update()

    def rotate_z(self):
        # if there is no object drawn, return
        if not self.object_drawn: return
        try:
            # try to get steps and the translation 
            steps = int(self.rot_steps_field.get())
            # get degrees
            deg = np.deg2rad(float(self.rot_deg_field.get()))
            print("deg: ", float(self.rot_deg_field.get()), " rads: ", deg)
        except:
            print("INVALID PARAMETERS")
            return
        # get vertex count
        v_count = len(self.vertices)
        deg_step = deg / steps
        # I really didn't want to do this, but I could NOT get it to work without caching the original verts :(
        original_verts = self.vertices.copy()
        print("deg step: ", float(self.rot_deg_field.get()) / steps, " rad step: ", deg_step)
        print("cos(deg_step): ", np.cos(deg_step), " sin(deg_step): ", np.sin(deg_step))
        
        # for each step
        for i in range(1, steps + 1):
            theta = deg_step * i
            print("theta rads: ", theta, " theta degs: ", np.rad2deg(theta), " cos(theta): ", round(np.cos(theta), 8), " sin(theta): ", round(np.sin(theta), 8))
            # for each vertex (except the first one)
            for j in range(1, v_count):
                t_vert = original_verts[j].copy()
                # rz = [cosx - siny, sinx + cosx, z]
                t_vert = [(round(np.cos(theta), 8) * t_vert[X]) - round((np.sin(theta) * t_vert[Y]), 8), (round(np.sin(theta), 8) * t_vert[X]) + round((np.cos(theta) * t_vert[Y]), 8), t_vert[Z]]
                # print("vert ", j, " after rotate: ", t_vert)
                self.vertices[j] = t_vert
            # redraw objects after updating all verts and force an update
            self.re_draw_objects()
            self.root.update()
        

    def rotate_custom(self):
        # if there is no object drawn, return
        if not self.object_drawn: return
        try:
            # try to get steps
            steps = int(self.rot_steps_field.get())
            # get points a and b
            point_a = np.asarray([float(str) for str in self.rot_point_a_field.get()[1:-1].split(',')])
            point_b = np.asarray([float(str) for str in self.rot_point_b_field.get()[1:-1].split(',')])
            # get degrees
            deg = np.deg2rad(float(self.rot_deg_field.get()))
        except:
            print("INVALID PARAMETERS")
            return
        # transform point a to the origin
        a_to_origin = point_a * -1
        point_a += a_to_origin
        # apply the same tramsformation to point b
        point_b += a_to_origin
        # rotate b to allign with z axis
        
        # rotate around x axis to make y = 0
        print("b before x rot: ", point_b)
        theta_x = np.arctan(point_b[Y] / point_b[Z])
        print("theta x = arctan(z / y): ", theta_x, " cos theta x: ", np.cos(theta_x), " sin theta x: ", np.sin(theta_x))
        point_b = [point_b[X], np.cos(theta_x) * point_b[Y] - np.sin(theta_x) * point_b[Z], np.sin(theta_x) * point_b[Y] + np.cos(theta_x) * point_b[Z],]
        print("b after x rot: ", point_b)

        # rotate around y axis to make x = 0
        print("b before y rot: ", point_b)
        theta_y = np.arctan(point_b[X] / point_b[Z])
        print("theta y = arctan(z / x): ", theta_y, " cos theta y: ", np.cos(theta_y), " sin theta y: ", np.sin(theta_y))
        point_b = [np.cos(theta_y) * point_b[X] - np.sin(theta_y) * point_b[Z], point_b[Y], np.sin(theta_y) * point_b[X] + np.cos(theta_y) * point_b[Z]]
        print("b after y rot: ", point_b)

        # get vertex count
        v_count = len(self.vertices)
        deg_step = deg / (steps)
        # I really didn't want to do this, but I could NOT get it to work without caching the original verts :(
        original_verts = self.vertices.copy()
        print("deg step: ", float(self.rot_deg_field.get()) / steps, " rad step: ", deg_step)
        print("cos(deg_step): ", np.cos(deg_step), " sin(deg_step): ", np.sin(deg_step))
        degrees_rotated = 0
        # for each step
        for i in range(1, steps + 1):
            # get the step theta
            theta = deg_step * i
            print("i = ", i, " theta = ", np.rad2deg(theta))
            # for each vertex (except the first one)
            for j in range(1, v_count):
                # get the vert
                t_vert = original_verts[j].copy()
                # apply a to origin translate
                t_vert += a_to_origin
                # apply the same rotations as point b
                t_vert = [t_vert[X], np.cos(theta_x) * t_vert[Y] - np.sin(theta_x) * t_vert[Z], np.sin(theta_x) * t_vert[Y] + np.cos(theta_x) * t_vert[Z]]
                t_vert = [np.cos(theta_y) * t_vert[X] - np.sin(theta_y) * t_vert[Z], t_vert[Y], np.sin(theta_y) * t_vert[X] + np.cos(theta_y) * t_vert[Z]]
                # rotate around Z = [xcos - ysin, xsin + ycos, z]
                t_vert = [(np.cos(theta)* t_vert[X]) - (np.sin(theta) * t_vert[Y]), (np.sin(theta) * t_vert[X]) + (np.cos(theta) * t_vert[Y]), t_vert[Z]]
                # undo the set up rotations
                t_vert = [np.cos(-theta_y) * t_vert[X] - np.sin(-theta_y) * t_vert[Z], t_vert[Y], np.sin(-theta_y) * t_vert[X] + np.cos(-theta_y) * t_vert[Z]]
                t_vert = [t_vert[X], np.cos(-theta_x) * t_vert[Y] - np.sin(-theta_x) * t_vert[Z], np.sin(-theta_x) * t_vert[Y] + np.cos(-theta_x) * t_vert[Z]]
                # unapply the a to origin translation
                t_vert -= a_to_origin
                self.vertices[j] = t_vert
            # redraw objects after updating all verts and force an update
            self.re_draw_objects()
            self.root.update()
    

    def scale_all(self): 
        try:
            # try to call the real scale function with an array of all the same number
            t_array = np.asarray([float(self.scale_ratio_all_field.get())] * 3)
        except:
            print("INVALID PARAMETERS ALL")
            return
        self.scale(t_array)
        
    def scale_custom(self): 
        try:
            # try to call the real scale function with the custom entered one
            t_array = np.asarray([float(str) for str in self.scale_ratio_custom_field.get()[1:-1].split(',')])
        except:
            print("INVALID PARAMETERS CUSTOM")
            return
        self.scale(t_array)
        
    def scale(self, scale_vec):
        # if there is no object drawn, return
        if not self.object_drawn: return
        try:
            # try to get steps and the translation 
            steps = int(self.scale_steps_field.get())
            scale_point = np.asarray([float(str) for str in self.scale_point_field.get()[1:-1].split(',')])
        except:
            print("INVALID PARAMETERS")
            return
        # set all the "previous step" variables to 1 by default
        x_prev_step = y_prev_step = z_prev_step = 1.0
        t_point = [0.0 - scale_point[X], 0.0 - scale_point[Y], 0.0 - scale_point[Z]]
        # get vertex count
        v_count = len(self.vertices)
        # for each step (starting at 1 and ending with i = steps on the last one)
        for i in range(1, steps + 1):
            # This gets the "scale it should be" at this step, ternary to avoid divide by 0
            t_x_scale = ((i * (scale_vec[X] - 1.0) / steps) + 1.0) if scale_vec[X] != 1.0 else 1.0
            t_y_scale = ((i * (scale_vec[Y] - 1.0) / steps) + 1.0) if scale_vec[Y] != 1.0 else 1.0
            t_z_scale = ((i * (scale_vec[Z] - 1.0) / steps) + 1.0) if scale_vec[Z] != 1.0 else 1.0
            # divide by the previous step to get the actual amount we multiply the vertex by
            x_step = t_x_scale/ x_prev_step 
            y_step = t_y_scale / y_prev_step
            z_step = t_z_scale / z_prev_step
            # for each vertex (except the first one, which is None)
            for j in range(1, v_count):
                t_vert = self.vertices[j]
                # apply point transformation to vertice
                t_vert[X] += t_point[X]
                t_vert[Y] += t_point[Y]
                t_vert[Z] += t_point[Z]
                # multiply each axis by scale ammount
                t_vert[X] *= x_step
                t_vert[Y] *= y_step
                t_vert[Z] *= z_step
                # unapply point transformation to vertice
                t_vert[X] -= t_point[X]
                t_vert[Y] -= t_point[Y]
                t_vert[Z] -= t_point[Z]
            # redraw objects after updating all verts and force an update
            self.re_draw_objects()
            self.root.update()
            # set the previous scale to be the current scale for next time
            x_prev_step = t_x_scale
            y_prev_step = t_y_scale
            z_prev_step = t_z_scale


    def translation(self):
        # if there is no object drawn, return
        if not self.object_drawn: return
        try:
            # try to get steps and the translation 
            steps = int(self.trans_steps_field.get())
            trans_array = np.asarray([float(str) for str in self.trans_point_field.get()[1:-1].split(',')])
        except:
            print("INVALID PARAMETERS")
            return
        # divide 1 by step count to get the amount it should translate each time 
        t_step = 1.0 / steps
        trans_array *= t_step
        # get the number of vertices
        v_count = len(self.vertices)
        # for each step
        for i in range(steps):
            # for each vertex (except the first one, which is None)
            for j in range(1, v_count):
                # increment each vertex by the step ammount
                t_vert = self.vertices[j]
                t_vert[X] += trans_array[X]
                t_vert[Y] += trans_array[Y]
                t_vert[Z] += trans_array[Z]
            # redraw objects after updating all verts and force an update
            self.re_draw_objects()
            self.root.update()
            
            
            
            


# Run the tkinter main loop
world=cl_world()
world.root.mainloop()
