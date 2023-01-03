import random,pygame

class position:
    def __init__(self,state,end_of_game,velocity,rows,columns,cell_width,cell_height,snake,food):
        self.state = state
        self.end_of_game = end_of_game
        self.velocity = velocity
        self.rows = rows
        self.columns = columns
        self.cell_width = cell_width
        self.cell_height = cell_height
        self.snake = snake
        self.food = food

def run_pygame():
    screen_dimensions = initialize_screen_size()
    screen = initialize_pygame(screen_dimensions)
    clock = initialize_clock()
    current_position = initialize_position(screen_dimensions) 
    
    text = initialize_end_screen()
    text_point = text_point_cal(text,screen_dimensions)
    try_again = initialize_try_again_text()
    try_again_point = try_again_point_cal(try_again,text,screen_dimensions)
    
    but_bound = create_button_bound(try_again,try_again_point)
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP or event.key == pygame.K_w:
                    current_position.velocity = 1
                elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                    current_position.velocity = 2
                elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                    current_position.velocity = 3
                elif event.key == pygame.K_LEFT or event.key == pygame.K_a:
                    current_position.velocity = 4
            if current_position.end_of_game and event.type == pygame.MOUSEBUTTONDOWN:
                mouse = pygame.mouse.get_pos()
                if but_bound[0] <= mouse[0] <= but_bound[1] and but_bound[2] <= mouse[1] <= but_bound[3]:
                    current_position = initialize_position(screen_dimensions) 
        if current_position.end_of_game:   
            screen.fill((255,170,80))
            screen.blit(text,text_point)
            screen.blit(try_again,try_again_point)
                        
        else:
            screen.fill((0,0,0))
            display_position(screen,current_position)
            snake_contact_CHECK = snake_contact(current_position)
            update_position(current_position,snake_contact_CHECK)
       
        clock.tick(25)
        pygame.display.flip()

def initialize_screen_size():
    WIDTH = 700
    HEIGHT = 700
    return [WIDTH,HEIGHT]

def initialize_pygame(screen_dimensions):
    pygame.init()
    screen = pygame.display.set_mode([screen_dimensions[0],screen_dimensions[1]])
    return screen

def initialize_clock():
    clock = pygame.time.Clock()
    return clock

def initialize_end_screen():
    font = pygame.font.Font(pygame.font.get_default_font(),36)
    text = font.render('GAME OVER', True, (255,255,255))
    return text

def text_point_cal(text,screen_dimensions):
    text_x = (screen_dimensions[0] / 2) - (text.get_rect().width / 2) 
    text_y = (screen_dimensions[1] / 2) - (text.get_rect().height / 2)
    
    return [text_x,text_y]
    
def initialize_try_again_text():
    font = pygame.font.Font(pygame.font.get_default_font(),25)
    text = font.render('Try again?', True, (255,255,255))
    return text

def try_again_point_cal(try_again,text,screen_dimensions):
    try_again_x = (screen_dimensions[0] / 2) - (try_again.get_rect().width / 2)
    try_again_y = (screen_dimensions[1] / 2) - (try_again.get_rect().height / 2) + text.get_rect().height 

    return [try_again_x,try_again_y] 

def create_button_bound(try_again,try_again_point):
    width_of_bound = try_again_point[0]+try_again.get_rect().width
    height_of_bound = try_again_point[1]+try_again.get_rect().height
    return [try_again_point[0],width_of_bound,try_again_point[1],height_of_bound]

def initialize_position(screen_dimensions):
    ROWS = 60
    COLUMNS = 60
    VELOCITY = 1
    end_of_game = 0
    
    cell_width = screen_dimensions[0]/COLUMNS
    cell_height = screen_dimensions[1]/ROWS

    snake = [[random.randint(0,ROWS-1),random.randint(0,COLUMNS-1)]]
    food = []

    initial_position = position([[0]*COLUMNS for i in range(ROWS)],end_of_game,VELOCITY,ROWS,COLUMNS,cell_width,cell_height,snake,food)
    initial_position.state[snake[0][0]][snake[0][1]] = 1
    
    update_food(initial_position) 

    return initial_position

def snake_contact(position):
    food = position.food
    if food in position.snake:
        update_food(position)
        return True
    return False

def update_food(position):
    ROWS = position.rows
    COLUMNS = position.columns
    food_spawn = [random.randint(0,ROWS-1),random.randint(0,COLUMNS-1)]
    while food_spawn in position.snake:
        food_spawn = [random.randint(0,ROWS-1),random.randint(0,COLUMNS-1)]
    
    position.food = food_spawn
    position.state[food_spawn[0]][food_spawn[1]] = 2
    
def display_position(screen,position):
    cell_width = position.cell_width
    cell_height = position.cell_height
    x = y = 0
    for row in range(position.rows):
        y = row*cell_height
        for col in range(position.columns):
            x = col*cell_width
            cell = position.state[row][col] 
            if cell:
                if cell == 2:
                    pygame.draw.rect(screen,(255,0,255),pygame.Rect(x,y,cell_width,cell_height))
                else:   
                    pygame.draw.rect(screen,(255,255,255),pygame.Rect(x,y,cell_width,cell_height))

def update_position(position,snake_contact_CHECK):
    snake = position.snake
    snake_head = snake[0]
    velocity = position.velocity
     
    if velocity == 1: # move up
        if snake_head[0] == 0:
            new_head = [position.rows-1,snake_head[1]]
        else:   
            new_head = [snake_head[0]-1,snake_head[1]]
    elif velocity == 2: # move right
        if snake_head[1] == position.columns-1:
            new_head = [snake_head[0],0]
        else:   
            new_head = [snake_head[0],snake_head[1]+1]
    elif velocity == 3: # move down
        if snake_head[0] == position.rows-1:
            new_head = [0,snake_head[1]]
        else:   
            new_head = [snake_head[0]+1,snake_head[1]]
    elif velocity == 4: # move left
        if snake_head[1] == 0:
            new_head = [snake_head[0],position.columns-1]
        else:   
            new_head = [snake_head[0],snake_head[1]-1]
        
    if new_head in snake:
        position.end_of_game = True
    else:
        if not snake_contact_CHECK: 
            position.state[snake[-1][0]][snake[-1][1]] = 0
            snake.pop()
        
        position.state[new_head[0]][new_head[1]] = 1
        position.snake = [new_head] + snake
        
run_pygame()
pygame.quit()
