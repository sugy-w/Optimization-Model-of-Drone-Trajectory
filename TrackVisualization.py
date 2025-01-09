import tkinter

def visualize(matrix_of_positions, check_point_indices, x_max, mass, drag, theta_1, theta_2, time_step_of_simulation):
    '''
    Animation which visualizes optimal trajectory based on matrix of positions.

    matrix_of_positions = 2*T matrix of positions in R^2 plane
    check_point_indices = List of indices, where drone is supposed to be at certain index time
    x_max = Maximum +- coordinate, where dron is able to operate
    mass = Weight of the drone
    drag = Coefficient simulating drag of the environment
    theta_1, theta_2 = Orientation of engines 1,2 -> Initial angle of thrust force vector
    time_step_of_simulation = Time pauses between single point visualisation in milliseconds
    '''
    # Canvas and Window declaration
    root = tkinter.Tk()
    root.title("Animated trajectory visualisation")
    canvas = tkinter.Canvas(root, width=850, height=500)
    canvas.pack()
    
    # Visual template generating
    canvas.create_rectangle(20, 20, 480, 480, outline="", fill="white")
    canvas.create_text(675, 35, text="Optimal trajectory visualisation",
                       font="tahoma 18 bold")

    canvas.create_text(550, 85, text="MASS", font="tahoma 15 bold")
    canvas.create_text(620, 85, text=str(mass), font="tahoma 15")

    canvas.create_text(550, 115, text="DRAG", font="tahoma 15 bold")
    canvas.create_text(620, 115, text=str(drag), font="tahoma 15")

    canvas.create_text(560, 145, text="THETA 1", font="tahoma 15 bold")
    canvas.create_text(650, 145, text=str(theta_1), font="tahoma 15")

    canvas.create_text(560, 175, text="THETA 2", font="tahoma 15 bold")
    canvas.create_text(650, 175, text=str(theta_2), font="tahoma 15")

    canvas.create_text(575, 250, text="Current time", font="tahoma 15 bold")
    current_time_output = canvas.create_text(660, 250, text="0", font="tahoma 15")

    # Grid preparation
    canvas.create_line(250, 25, 250, 475, dash=(4, 1))
    canvas.create_line(25, 250, 475, 250, dash=(4, 1))

    # Animation control, mutable variables
    resume = [False]
    current_index = [0]

    # Animation control methods
    def play():
        # Initializes/Reinitializes Animation
        resume[0] = True
        draw_next(current_index[0])
    def pause():
        # Pauses animation
        resume[0] = False

    # Handling buttons with play() and pause() methods
    resume_button = tkinter.Button(root, text="Play", width=5, height=2, command=play)
    resume_button.place(x=600, y=400)

    stop_button = tkinter.Button(root, text="Stop", width=5, height=2, command=pause)
    stop_button.place(x=690, y=400)

    # Calculation of gap between coordinates
    one_step = 225 // x_max

    # Grid labels visualising
    for i in range(1, x_max + 1):
        canvas.create_text(250 + i * one_step, 260, text=str(i))
        canvas.create_text(250 - (i * one_step), 260, text=str(-i))
        canvas.create_text(240, 250 + i * one_step, text=str(-i))
        canvas.create_text(240, 250 - i * one_step, text=str(i))

    previous_coordinates = [0,0]

    def draw_next(i):
        '''
        Timed visualization of trajectory. Visualizes points and even connected trajectory.

        i = Current index of the certain point
        '''
        # Edge case to abort recursive function
        if not resume[0]:
            return
        # Edge case to abort recursive function
        if i >= len(matrix_of_positions[0]):
            return
        # Position fetch and conversion to px coordinates system
        x = matrix_of_positions[0][i] * one_step
        y = matrix_of_positions[1][i] * one_step

        # Visualization of point and connected line
        canvas.create_line(
            250 + previous_coordinates[0], 250 - previous_coordinates[1],
            250 + x, 250 - y
        )
        # Visalising points (checkpoint/not checkpoint)
        if i in check_point_indices:
            canvas.create_oval(
                250 + x - 4, 250 - y - 4,
                250 + x + 4, 250 - y + 4,
                fill = "green",
                outline = ""
            )
        else:
            canvas.create_oval(
                250 + x - 1, 250 - y - 1,
                250 + x + 1, 250 - y + 1,
                fill = "red"
            )
        
        # Update of control variables for next iteration of animation
        previous_coordinates[0] = x
        previous_coordinates[1] = y
        current_index[0] += 1

        # Animation Step
        canvas.after(time_step_of_simulation, draw_next, i + 1)
        canvas.itemconfig(current_time_output, text=str(i))
            
    draw_next(current_index[0])

    root.mainloop()

def visualize_from_data(data_source, time_step=200):
    '''
    Generalisation of method visualize() to read data from file

    data_source = Name of the file with inptu data
    time_step = Time gap between two point visualizations, equal to time_step_of_simulation in visualize() [Default = 200]
    '''
    try:
        # Data file opening and Data Fetch
        with open(data_source) as file:
            contains = file.readlines()
            position_matrix = [[],[]]
            buffer = int(contains[0])
            
            delta_t = contains[buffer + 1].strip()
            weight = contains[buffer + 2].strip()
            drag = contains[buffer + 3].strip()
            theta1 = contains[buffer + 4].split()[0]
            theta2 = contains[buffer + 4].split()[1]
            checkpoints = [int(x) for x in contains[buffer + 5].split()]
            x_max = int(contains[buffer + 6].strip())
            
            for i in range(1, buffer + 1):
                position_matrix[0].append(float(contains[i].split()[0]))
                position_matrix[1].append(float(contains[i].split()[1]))
        # Visualization, as previous method
        return visualize(position_matrix, checkpoints, x_max, weight, drag, theta1, theta2, time_step)    

    # Exception Handling
    except (FileNotFoundError, FileExistsError):
        raise Exception("Please enter existing file name")
    except IndexError:
        raise Exception("Please enter valid data file in desired template")

# Existing data source files, just uncomment certain line and Play as usual

#visualize_from_data("simulation1.txt") # (E-1)
#visualize_from_data("simulation6.txt") # (E-2)
#visualize_from_data("simulation2.txt") # (EE-1) □
#visualize_from_data("simulation3.txt") # (EE-2) <3
#visualize_from_data("simulation4.txt") # (EE-3)
#visualize_from_data("simulation5.txt") # (EE-4)