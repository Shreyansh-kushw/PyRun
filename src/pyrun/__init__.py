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
        
        
