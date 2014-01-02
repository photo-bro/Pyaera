#########################
# Shape.py
# 
# For shapes/pieces
#
# NOTE: The majority of the functions are not actually needed
#    because Python does not have public/private class data.
#    However, to maintain good programming etiquette we have
#    chosen to follow the traditional public/private class
#    implementation.
#
#    The use of self documenting identifiers has been used
#    in absence of full pre/post documentation
########################

class Shape(object):

    _Visible = False
    _Active = False
    _ShapeNum = None
    _x = _y = None
    _prev_pos_x = _prev_pos_y = None
    _image = None
    _player = None 
    _spot_x = _spot_y = None

    def __init__(self, num, player, sprite, visible, (x,y)):
        self._Active = False
        self._ShapeNum = num
        self._player = player
        self._image = sprite
        self._Visible = visible
        self._spot_x = '0'
        self._spot_y = '0'
        self._x = x
        self._y = y
        self._prev_pos_x, self._prev_pos_y = (0b0, 0b0)
    
    def isActive(self):
        return self._Active
    
    def setActive(self, active):
        self._Active = active
    
    def isVisible(self):
        return self._Visible
    
    def setVisible(self, visible):
        self._Visible = visible
    
    def getPosition(self):
        return (self._x, self._y)
    
    def setPosition(self, (x,y)):
        self._x = x
        self._y = y
        
    def changeSprite(self, sprite):
        self._image = sprite
        
    def getPlayer(self):
        return self._player
    
    def getNum(self):
        return self._ShapeNum
        
    def getSprite(self):
            return self._image
    
    def setSprite(self, sprite):
        self._image = sprite
        
    def getSpot(self):
        return (self._spot_x, self._spot_y)
    
    def setSpot(self, (x,y)):
        self.spot_x = x
        self.spot_y = y
        
    def setPrevPos(self, (pos_x, pos_y)):
        self._prev_pos_x = pos_x
        self._prev_pos_y = pos_y
        
    def getPrevPos(self):
        return (self._prev_pos_x, self._prev_pos_y) 