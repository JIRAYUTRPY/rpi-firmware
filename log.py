class Log :

    def __init__(self , debug) :
        self.debug = debug
    
    def info(self, func ,message) :
        if self.debug :
            print('[INFO][' + func + ']' + ' : ' + message)
    
    def warning(self, func ,message) :
        if self.debug :
            print('[WARN][' + func + ']' + ' : ' + message)

    def error(self, func ,message) :
        if self.debug :
            print('[ERROR][' + func + ']' + ' : ' + message)