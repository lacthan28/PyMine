def isset(self, variable):
    return variable in locals() or variable in globals()