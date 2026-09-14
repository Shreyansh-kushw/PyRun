class VirtualMachineException(Exception):
    pass

class VirtualMachine:
    """The virtual machine class"""

    def __init__(self):
        self.frames = [] # call stack of rames
        self.frame = None # current frame
        self.return_value = None # return values
        self.last_exeption = None # exception states

    def run_code(self, code, global_names = None, local_names = None):
        """Entry point for the execution of the code"""

        frame = self.make_frame(code, global_names, local_names)
        self.run_frame(frame)
    
    # Frame manipulation
    def make_frame(self, code, callargs = {}, global_names = None, local_names = None):
        """Creates a new frame"""

        if global_names is not None and local_names is not None:
            local_names = global_names
        elif self.frames:
            global_names = self.frame.global_names
            local_names = {}
        else:
            global_names = local_names = {
                '__builtins__' : __builtins__,
                '__name__' : '__main__',
                '__docs__' : None,
                '__package__' : None,
            }
        local_names.update(callargs)
        frame = Frame(code, global_names, local_names, self.frame)
        return frame

    def push_frame(self, frame):
        """Pushes a frame into the call stack"""

        self.frames.append(frame)
        self.frame = frame
    
    def pop_frame(self):
        """Removes a frame from the call stack"""

        self.frame.pop()

        if self.frames:
            self.frame = self.frames[-1]
        
        else: 
            self.frame = None
    
    def run_frame(self):
        ...

class Frame:
    """The frame class containing the various attributes of the code object"""

    def __init__(
        self,
        code_obj,
        global_names,
        local_names,
        prev_frame,
    ):
        self.code_obj = code_obj
        self.global_names = global_names
        self.local_names = local_names
        self.prev_frame = prev_frame

        self.stack = [] # the data stack for this frame
        self.block_stack = [] # the block stack for this Frame

        # setting up the builtins
        if prev_frame:
            self.builtin_names = self.prev_frame.builtin_names
        else:
            self.builtin_names = local_names['__builtins__']
            if hasattr(self.builtin_names, '__dict__'):
                self.builtin_names = self.builtin_names.__dict__

        self.last_instruction = 0
        
        
