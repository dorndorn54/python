"""
_this serves as the library for all instances of the different goods_
and the tray rack
"""


class Pat:
    # this is the class for pineapple tarts
    def __init__(self, output, preptime=2, cooktime=18, posttime=5, cooltime = 10, packtime=3, pertray=48, rackspace=2):
        self.output = output
        self.preptime = preptime
        self.cooktime = cooktime
        self.posttime = posttime
        self.cooltime = cooltime
        self.packtime = packtime
        self.pertry = pertray
        self.rackspace = rackspace

    def get_preptime(self):
        return self.preptime

    def get_cooktime(self):
        return self.cooktime

    def get_posttime(self):
        return self.packtime
    
    def get_cooltime(self):
        return self.cooltime

    def get_packtime(self):
        return self.packtime

    def get_pertray(self):
        return self.pertray

    def get_rackspace(self):
        return self.rackspace
    
    def get_tray_data(self):
        # pass key information about the tray of goods to the tray class
        # this is to help the racktime
        tray_data = list()
        
        tray_data.append(self.get_preptime)
        tray_data.append(self.get_cooktime)
        tray_data.append(self.get_posttime)
        tray_data.append(self.get_cooltime)
        tray_data.append(self.get_packtime)
        tray_data.append(self.get_rackspace)
        
        return tray_data
    

class Tray:
    # this is the class for the tray that is to be inserted into the rack
    def __init__(preptime, cooktime, posttime, cooltime, packtime, rackspace):
        


class Rack:
    # this is the class for the rack
