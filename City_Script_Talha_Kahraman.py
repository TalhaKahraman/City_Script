#Import "Buildings(Import_This)" file for code to work. This contains the building polygons

import random

import pymel.core as pm
import maya.OpenMaya as OpenMaya

cmds.setAttr("Do_Not_Touch.visibility", lock=True)
cmds.setAttr("intersection.visibility", lock=True)
cmds.setAttr("road.visibility", lock=True)
cmds.setAttr("city_building04.visibility", lock=True)
cmds.setAttr("city_building3.visibility", lock=True)
cmds.setAttr("City_building2.visibility", lock=True)
cmds.setAttr("modular.visibility", lock=True)
cmds.setAttr("bottom.visibility", lock=True)
cmds.setAttr("mid_stack.visibility", lock=True)
cmds.setAttr("not_important.visibility", lock=True)
cmds.setAttr("roof.visibility", lock=True)
    
class CityGenerator():
    def __init__(self):
        self.buildUI()
    
    def buildUI(self):
        self.window = cmds.window( title="City Generator", widthHeight=(200, 330) )
        cmds.columnLayout( adjustableColumn=True )
        
        cmds.rowLayout(numberOfColumns=2, columnWidth2=[80, 200])
        cmds.text(label='Width')
        self.width_floatfield = cmds.floatField(value=150, width=70)
        cmds.setParent('..')
        
        cmds.rowLayout(numberOfColumns=2, columnWidth2=[80, 200])
        cmds.text(label='Height')
        self.height_floatfield = cmds.floatField(value=150, width=70)
        cmds.setParent('..')
        
        cmds.rowLayout(numberOfColumns=2, columnWidth2=[80, 200])
        cmds.text(label='Width Divisions')
        self.widthDiv_intfield = cmds.intField(value=10, width=70)
        cmds.setParent('..')
        
        cmds.rowLayout(numberOfColumns=2, columnWidth2=[80, 200])
        cmds.text(label='Height Divisions')
        self.heightDiv_intfield = cmds.intField(value=10, width=70)
        cmds.setParent('..')
        
        cmds.button( label='Plane', command=self.createPlane)
        
        cmds.rowLayout(numberOfColumns=2, columnWidth2=[80, 200])
        cmds.text(label='Max Height')
        self.maxHeight_intfield = cmds.intField(value=20, width=70)
        cmds.setParent('..')
        
        cmds.rowLayout(numberOfColumns=2, columnWidth2=[80, 200])
        cmds.text(label='Min Height')
        self.minHeight_intfield = cmds.intField(value=16, width=70)
        cmds.setParent('..')
        
        self.check1 = cmds.checkBox(label='Building 1', value=True)
        self.check2 = cmds.checkBox(label='Building 2', value=True)
        self.check3 = cmds.checkBox(label='Building 3', value=True)
        self.check4 = cmds.checkBox(label='Building 4', value=True)
        
        cmds.button( label='Buildings', command=self.place_buildings)
        
        self.check5 = cmds.checkBox(label='X', value=True)
        self.check6 = cmds.checkBox(label='Z', value=False)
        
        cmds.button( label='Road', command=self.make_road)
        
        cmds.button( label='Intersection', command=self.make_intersection)
        
    def show(self):
        cmds.showWindow( self.window )
    
    def make_building(self):
        
        width_value = cmds.floatField(self.width_floatfield, query=True, value=True)
        height_value = cmds.floatField(self.height_floatfield, query=True, value=True)
        widthDiv_value = cmds.intField(self.widthDiv_intfield, query=True, value=True)
        heightDiv_value = cmds.intField(self.heightDiv_intfield, query=True, value=True)

        maxHeight_value = cmds.intField(self.maxHeight_intfield, query=True, value=True)
        minHeight_value = cmds.intField(self.minHeight_intfield, query=True, value=True)
        
        randStack = random.randint(minHeight_value, maxHeight_value)
        randStack_value = randStack
        
        """this first part stacks the middle modular pieces together. it moves
        the new object (with the pivot point being at the bottom) to the previous
        objects top vertex position(I chose vtx[76]).
        """
        mid1 = cmds.duplicate(u'mid_stack', returnRootsOnly=True)
        mod_list = [mid1[0]]
        #(change description)5 is the input given by the user but added by 1 so it would be range(1, input + 1)
        for index in range(1, randStack_value + 1):
            indexing = index - 1
            old_piece = mod_list[indexing]
            piece = cmds.duplicate(u'mid_stack1')
            new_piece = piece[0]
            mod_list.append(new_piece)
            position = cmds.xform(mod_list[indexing] + ".vtx[76]", query=True, translation=True, worldSpace=True)
            cmds.move(position[1], new_piece, moveY=True, scalePivotRelative=True, worldSpace=True)
        
        """Here I move the top piece (with the pivot point being at the bottom)
        to the top of the last middle_stack piece. 
        """
        last_position = cmds.xform(mod_list[-1] + ".vtx[76]", query=True, translation=True, worldSpace=True)
        new_top = cmds.duplicate(u'roof')
        top1 = new_top[0]
        cmds.move(last_position[1], top1, moveY=True, scalePivotRelative=True, worldSpace=True)
        
        """Here I move the bottom piece (with the pivot point being at the top)
        to the bottom of the first middle_stack piece. 
        """
        first_position = cmds.xform(mod_list[0] + ".vtx[81]", query=True, translation=True, worldSpace=True)
        new_bottom = cmds.duplicate(u'bottom')
        bottom1 = new_bottom[0]
        cmds.move(first_position[1], bottom1, moveY=True, scalePivotRelative=True, worldSpace=True)
        
        building_combined = cmds.polyUnite(mod_list, bottom1, top1, name="buildingA", constructionHistory=False)
        building_merged= building_combined
    
        cmds.polyMergeVertex(building_merged)
        
        cmds.xform(centerPivotsOnComponents=True)
        
        my_building = building_merged
        
        building = my_building[0]
   
        # finds out what the bottom vtx is so I can move pivot to that point
        # 125 is number of vertices for top + bottom piece, 80 is vertices for one middle piece,
        # my_building[1] is randStack_value. I add them all to get a bottom vertex
        # so that I can move it on top of the plane without the building clashing into the plane
        #top vertex is 1 so all of the vertices added should give me a vertex at the bottom
        botVtx_point = 125 + (80 * (randStack_value))
        #finds position of vtx
        pos = cmds.xform(building + ".vtx[" + str(botVtx_point) + "]", query=True, translation=True, worldSpace=True)
        #moves pivot to bottom vertex point
        cmds.move(pos[1], building + ".scalePivot", moveY=True, worldSpace=True)
        cmds.move(pos[1], building + ".rotatePivot", moveY=True, worldSpace=True)
        
        return building, building_merged, randStack_value
        
    
    def make_building_2(self):
        
        maxHeight_value = cmds.intField(self.maxHeight_intfield, query=True, value=True)
        minHeight_value = cmds.intField(self.minHeight_intfield, query=True, value=True)
        
        randStack = random.randint(minHeight_value, maxHeight_value)
        randStack_value = randStack
        
        #Here I duplicate the building so I don't end up using the original as I will need it again when this method gets rerun
        cmds.duplicate(u'City_building2')
        cmds.rename("City_building3", "city_building_2")
        cmds.parent('city_building_2', world=True)
        
        #Selects top half vertices of the building
        cmds.select(u'city_building_2.vtx[1]', u'city_building_2.vtx[3]', u'city_building_2.vtx[5]', 
        u'city_building_2.vtx[7]', u'city_building_2.vtx[9]', u'city_building_2.vtx[11]', 
        u'city_building_2.vtx[13]', u'city_building_2.vtx[15]', u'city_building_2.vtx[17]',
        u'city_building_2.vtx[19]', u'city_building_2.vtx[21]', u'city_building_2.vtx[23]',
        u'city_building_2.vtx[25]', u'city_building_2.vtx[27]', u'city_building_2.vtx[29]',
        u'city_building_2.vtx[31:40]', u'city_building_2.vtx[50:349]')
        
        #moves the selected vertices. The reason I have multiplied randStack_value by 85 is to get the height of
        #building 2 to be in a similar range to building 1. randStack_value alone isn't enough as the buildings end
        #up being too short
        cmds.move(randStack_value * 85, moveY=True, relative=True)
        cmds.select(clear=True)
        
        #gets translate values of vertex 0
        vtx_pos = cmds.xform(u"city_building_2.vtx[0]", query=True, translation=True, worldSpace=True) 
        
        #moves pivot to bottom vertex 0 point
        cmds.move(vtx_pos[1], u"city_building_2" + ".scalePivot", moveY=True, worldSpace=True) 
        cmds.move(vtx_pos[1], u"city_building_2" + ".rotatePivot", moveY=True, worldSpace=True)
        
        cmds.select(u'city_building_2')
        cmds.rename("city_building_2", "buildingB")
        building2 = cmds.ls(selection=True)
        
        return building2       
            
    def make_building_3(self):
        
        maxHeight_value = cmds.intField(self.maxHeight_intfield, query=True, value=True)
        minHeight_value = cmds.intField(self.minHeight_intfield, query=True, value=True)
        
        randStack = random.randint(minHeight_value, maxHeight_value)
        randStack_value = randStack
        
        #Here I duplicate the building so I don't end up using the original as I will need it again when this method gets rerun
        cmds.duplicate(u'city_building3')
        cmds.parent('city_building4', world=True)
        
        #Selects top half vertices of the building
        cmds.select(u'city_building4.vtx[1]', u'city_building4.vtx[3]', u'city_building4.vtx[5]', 
        u'city_building4.vtx[7]', u'city_building4.vtx[9]', u'city_building4.vtx[11]', u'city_building4.vtx[13]',
        u'city_building4.vtx[15]', u'city_building4.vtx[17]', u'city_building4.vtx[19]', u'city_building4.vtx[21]',
        u'city_building4.vtx[23]', u'city_building4.vtx[25]', u'city_building4.vtx[27]', u'city_building4.vtx[29]',
        u'city_building4.vtx[31:63]', u'city_building4.vtx[65]', u'city_building4.vtx[67]', u'city_building4.vtx[69]',
        u'city_building4.vtx[71]', u'city_building4.vtx[73]', u'city_building4.vtx[75]', u'city_building4.vtx[77]',
        u'city_building4.vtx[79]', u'city_building4.vtx[81]', u'city_building4.vtx[83]', u'city_building4.vtx[85]',
        u'city_building4.vtx[87]', u'city_building4.vtx[89]', u'city_building4.vtx[91]', u'city_building4.vtx[93]',
        u'city_building4.vtx[95]', u'city_building4.vtx[97]', u'city_building4.vtx[99]', u'city_building4.vtx[101]',
        u'city_building4.vtx[103]', u'city_building4.vtx[105]', u'city_building4.vtx[107]', u'city_building4.vtx[109]',
        u'city_building4.vtx[111]', u'city_building4.vtx[113]', u'city_building4.vtx[115]', u'city_building4.vtx[117]',
        u'city_building4.vtx[119]', u'city_building4.vtx[121]', u'city_building4.vtx[123]', u'city_building4.vtx[125]',
        u'city_building4.vtx[127]', u'city_building4.vtx[129]', u'city_building4.vtx[131]', u'city_building4.vtx[133]',
        u'city_building4.vtx[135]', u'city_building4.vtx[137]', u'city_building4.vtx[139]', u'city_building4.vtx[141]',
        u'city_building4.vtx[143]', u'city_building4.vtx[145]', u'city_building4.vtx[147]', u'city_building4.vtx[149]',
        u'city_building4.vtx[151]', u'city_building4.vtx[153]', u'city_building4.vtx[155]', u'city_building4.vtx[157]',
        u'city_building4.vtx[159]', u'city_building4.vtx[161]', u'city_building4.vtx[163]', u'city_building4.vtx[165]',
        u'city_building4.vtx[167]', u'city_building4.vtx[169]', u'city_building4.vtx[171]', u'city_building4.vtx[173]',
        u'city_building4.vtx[175]', u'city_building4.vtx[177]', u'city_building4.vtx[179]', u'city_building4.vtx[181]',
        u'city_building4.vtx[183:215]')
        
        #moves the selected vertices. The reason I have multiplied randStack_value by 85 is to get the height of
        #building 2 to be in a similar range to building 1. randStack_value alone isn't enough as the buildings end
        #up being too short
        cmds.move(randStack_value * 85, moveY=True, relative=True)
        cmds.select(clear=True)
        
        #gets translate values of vertex 0
        vtx_pos = cmds.xform(u"city_building4.vtx[0]", query=True, translation=True, worldSpace=True) 
        
        #moves pivot to bottom vertex 0 point
        cmds.move(vtx_pos[1], u"city_building4" + ".scalePivot", moveY=True, worldSpace=True)
        cmds.move(vtx_pos[1], u"city_building4" + ".rotatePivot", moveY=True, worldSpace=True)
        
        cmds.select(u'city_building4')
        cmds.rename("city_building4", "buildingC")
        building3 = cmds.ls(selection=True)
        
        return building3
    
    def make_building_4(self):
        
        maxHeight_value = cmds.intField(self.maxHeight_intfield, query=True, value=True)
        minHeight_value = cmds.intField(self.minHeight_intfield, query=True, value=True)
        
        randStack = random.randint(minHeight_value, maxHeight_value)
        randStack_value = randStack
        
        #Here I duplicate the building so I don't end up using the original as I will need it again when this method gets rerun
        cmds.duplicate(u'city_building04')
        cmds.parent('city_building05', world=True)
        
        #Selects top half vertices of the building
        cmds.select(u'city_building05.vtx[1]', u'city_building05.vtx[3]', u'city_building05.vtx[5]', u'city_building05.vtx[7]', 
        u'city_building05.vtx[9]', u'city_building05.vtx[11]', u'city_building05.vtx[13]', u'city_building05.vtx[15]', 
        u'city_building05.vtx[17]', u'city_building05.vtx[19]', u'city_building05.vtx[21]', u'city_building05.vtx[23]', 
        u'city_building05.vtx[25]', u'city_building05.vtx[27]', u'city_building05.vtx[29]', u'city_building05.vtx[31]', 
        u'city_building05.vtx[33]', u'city_building05.vtx[35]', u'city_building05.vtx[37]', u'city_building05.vtx[39:55]', 
        u'city_building05.vtx[72:195]', u'city_building05.vtx[197]', u'city_building05.vtx[199]', u'city_building05.vtx[201]', 
        u'city_building05.vtx[203]', u'city_building05.vtx[205]', u'city_building05.vtx[207]', u'city_building05.vtx[209]', 
        u'city_building05.vtx[211]', u'city_building05.vtx[213]', u'city_building05.vtx[215]', u'city_building05.vtx[217]',
        u'city_building05.vtx[219]', u'city_building05.vtx[221]', u'city_building05.vtx[223]', u'city_building05.vtx[225]', 
        u'city_building05.vtx[227]', u'city_building05.vtx[229]', u'city_building05.vtx[231]', u'city_building05.vtx[233]', 
        u'city_building05.vtx[235]', u'city_building05.vtx[237]', u'city_building05.vtx[239]', u'city_building05.vtx[241]', 
        u'city_building05.vtx[243]', u'city_building05.vtx[245]', u'city_building05.vtx[247]', u'city_building05.vtx[249]', 
        u'city_building05.vtx[251]', u'city_building05.vtx[253]', u'city_building05.vtx[255]', u'city_building05.vtx[257]', 
        u'city_building05.vtx[259]', u'city_building05.vtx[261]', u'city_building05.vtx[263]', u'city_building05.vtx[265]', 
        u'city_building05.vtx[267]', u'city_building05.vtx[269]', u'city_building05.vtx[271]', u'city_building05.vtx[273]', 
        u'city_building05.vtx[275]', u'city_building05.vtx[277]', u'city_building05.vtx[279]', u'city_building05.vtx[281]', 
        u'city_building05.vtx[283]', u'city_building05.vtx[285]', u'city_building05.vtx[287]', u'city_building05.vtx[289]', 
        u'city_building05.vtx[291]', u'city_building05.vtx[293]', u'city_building05.vtx[295]', u'city_building05.vtx[297]', 
        u'city_building05.vtx[299]', u'city_building05.vtx[301]', u'city_building05.vtx[303]', u'city_building05.vtx[305]', 
        u'city_building05.vtx[307]', u'city_building05.vtx[309]', u'city_building05.vtx[311]', u'city_building05.vtx[313]', 
        u'city_building05.vtx[315]', u'city_building05.vtx[317]', u'city_building05.vtx[319]', u'city_building05.vtx[321]', 
        u'city_building05.vtx[323]', u'city_building05.vtx[325]', u'city_building05.vtx[327]', u'city_building05.vtx[329]', 
        u'city_building05.vtx[331]', u'city_building05.vtx[333]', u'city_building05.vtx[335]', u'city_building05.vtx[337]', 
        u'city_building05.vtx[339]', u'city_building05.vtx[341]', u'city_building05.vtx[343]', u'city_building05.vtx[345]', 
        u'city_building05.vtx[347]', u'city_building05.vtx[349]', u'city_building05.vtx[351]', u'city_building05.vtx[353]', 
        u'city_building05.vtx[355]')
        
        #moves the selected vertices. The reason I have multiplied randStack_value by 85 is to get the height of
        #building 2 to be in a similar range to building 1. randStack_value alone isn't enough as the buildings end
        #up being too short
        cmds.move(randStack_value * 85, moveY=True, relative=True)
        cmds.select(clear=True)
        
        #gets translate values of vertex 0
        vtx_pos = cmds.xform(u"city_building05.vtx[0]", query=True, translation=True, worldSpace=True) 
        
        #moves pivot to bottom vertex 0 point
        cmds.move(vtx_pos[1], u"city_building05" + ".scalePivot", moveY=True, worldSpace=True)
        cmds.move(vtx_pos[1], u"city_building05" + ".rotatePivot", moveY=True, worldSpace=True)
        
        cmds.select(u'city_building05')
        cmds.rename("city_building05", "buildingD")
        building4 = cmds.ls(selection=True)
        
        return building4
        
    def place_buildings(self, *args):
        
        sel_faces = cmds.ls(selection=True, flatten=True)
        
        for items in sel_faces:
 
            #all make_building methods are places here without "()" so they don't all end up being called
            all_buildings = [self.make_building, self.make_building_2, self.make_building_3, self.make_building_4]
            
            #This gets/queries the value of the checkbox
            check1_value = cmds.checkBox(self.check1, query=True, value=True)
            #If check1 is checked off, it removes make_building from the list
            if check1_value == False:
               all_buildings.remove(self.make_building)
               
            check2_value = cmds.checkBox(self.check2, query=True, value=True)
            if check2_value == False:
               all_buildings.remove(self.make_building_2)
           
            check3_value = cmds.checkBox(self.check3, query=True, value=True)
            if check3_value == False:
               all_buildings.remove(self.make_building_3)
               
            check4_value = cmds.checkBox(self.check4, query=True, value=True)
            if check4_value == False:
               all_buildings.remove(self.make_building_4)
            
            #random.choice does not work unless there is 2 or more values to choose from.
            #the next couple of lines until after else works around this issue
            length = len(all_buildings)
            new_rand_bulding = 'nothing'
            if length == 1:
                new_rand_building = all_buildings[0]()
            
            elif length == 0:
                import sys
                sys.exit("Error! Can't have 0 buildings. Please check at least one.")
            
            else:
                #here it chooses a method and calls it, hence the "()" after "(all_buildings)"
                rand_building = random.choice(all_buildings)()
                new_rand_building = rand_building
                
           
                   
            #gets the centre point of a face
            face = pm.MeshFace(items)
            pt = face.__apimfn__().center(OpenMaya.MSpace.kWorld)
            centerPoint = pm.datatypes.Point(pt)
            
            #moves building to the centre of a face
            cmds.move(centerPoint[0], centerPoint[1], centerPoint[2], new_rand_building[0], scalePivotRelative=True, worldSpace=True)
            
            width_value = cmds.floatField(self.width_floatfield, query=True, value=True)
            height_value = cmds.floatField(self.height_floatfield, query=True, value=True)
            widthDiv_value = cmds.intField(self.widthDiv_intfield, query=True, value=True)
            heightDiv_value = cmds.intField(self.heightDiv_intfield, query=True, value=True)
    
            maxHeight_value = cmds.intField(self.maxHeight_intfield, query=True, value=True)
            minHeight_value = cmds.intField(self.minHeight_intfield, query=True, value=True)
            
            face_width = width_value / widthDiv_value  
            face_height = height_value / heightDiv_value
            
            max_width = face_width - (face_width * 0.10)
            # max_depth(cube) = max_height(building)
            max_depth = face_height - (face_height * 0.10)
            min_width = face_width * 0.6
            min_depth = face_height * 0.6
            
            max_size = (1.005 * max_width) - max_width
            min_size = max_size * 0.6
                
            rand_size = random.uniform(min_size, max_size)
            
            cmds.scale(rand_size, rand_size, rand_size, new_rand_building[0])
            cmds.move(0.828, new_rand_building[0], moveY=True, scalePivotRelative=True, relative=True)
            
            block = cmds.polyCube(name="building_block", width=face_width, depth=face_height, height=0.85)
            block_pos = cmds.xform(block[0] + ".vtx[0]", query=True, translation=True)
            cmds.move(block_pos[1], block[0] + ".scalePivot", moveY=True, worldSpace=True)
            cmds.move(block_pos[1], block[0] + ".rotatePivot", moveY=True, worldSpace=True)
            cmds.move(centerPoint[0], centerPoint[1], centerPoint[2], block[0], scalePivotRelative=True, worldSpace=True)
            #cmds.rename("building_block", "build_block")
            cmds.polyUnite(block[0], new_rand_building[0], name="building1", constructionHistory=False)
            
        cmds.hide("modular")
        #return new_rand_building
    
    def createPlane(self, *args):
        width_value = cmds.floatField(self.width_floatfield, query=True, value=True)
        height_value = cmds.floatField(self.height_floatfield, query=True, value=True)
        widthDiv_value = cmds.intField(self.widthDiv_intfield, query=True, value=True)
        heightDiv_value = cmds.intField(self.heightDiv_intfield, query=True, value=True)
        cmds.polyPlane(name="Ground", width=width_value, height=height_value, subdivisionsWidth=widthDiv_value, subdivisionsHeight=heightDiv_value, constructionHistory=False)
        maxHeight_value = cmds.intField(self.maxHeight_intfield, query=True, value=True)
        minHeight_value = cmds.intField(self.minHeight_intfield, query=True, value=True)
        
    def make_road(self, *args):
        #find out how to scale road to fit on face in case the size is changed
        #and this is optional. make it so that if two or more faces are selected in 1 direction, it automatically finds 
        #out which direction to build the roads to

        sel_faces = cmds.ls(selection=True, flatten=True)
        for items in sel_faces:
            
            check5_value = cmds.checkBox(self.check5, query=True, value=True)
            check6_value = cmds.checkBox(self.check6, query=True, value=True)
            
            if check5_value == True and check6_value == True or check5_value == False and check6_value == False:
                sys.exit("Error! Pick one.")
                
            road = cmds.duplicate(u'road')
            
            cmds.parent(road, world=True)
            
            face = pm.MeshFace(items)
            pt = face.__apimfn__().center(OpenMaya.MSpace.kWorld)
            centerPoint = pm.datatypes.Point(pt)
            
            #moves road to the centre of a face
            cmds.move(centerPoint[0], centerPoint[1], centerPoint[2], road[0], scalePivotRelative=True, worldSpace=True)
            
            
            if check5_value == True and check6_value == False:
                pass
                
            elif check5_value == False and check6_value == True:
                cmds.rotate(90, road[0], rotateY=True)
        
    def make_intersection(*args):
        
        sel_faces = cmds.ls(selection=True, flatten=True)
        
        for items in sel_faces:
            
            intersection = cmds.duplicate(u'intersection')
            
            face = pm.MeshFace(items)
            pt = face.__apimfn__().center(OpenMaya.MSpace.kWorld)
            centerPoint = pm.datatypes.Point(pt)
    
            #moves intersection to the centre of a face
            cmds.move(centerPoint[0], centerPoint[1], centerPoint[2], intersection[0], scalePivotRelative=True, worldSpace=True)
            cmds.parent(intersection, world=True)
            
                        
city = CityGenerator()
city.show()