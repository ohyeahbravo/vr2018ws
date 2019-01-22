#!/usr/bin/python

### import guacamole libraries
import avango
import avango.gua
import avango.script
from avango.script import field_has_changed


### import python libraries
import time


class NavigationManager(avango.script.Script):

    ## input fields
    sf_technique_button0 = avango.SFBool()
    sf_technique_button1 = avango.SFBool()
    sf_technique_button2 = avango.SFBool()
    sf_toggle_technique_button = avango.SFBool()

    sf_reset_button = avango.SFBool()


    ## output fields
    sf_nav_mat = avango.gua.SFMatrix4()
    sf_nav_mat.value = avango.gua.make_identity_mat()


    ## constructor
    def __init__(self):
        self.super(NavigationManager).__init__()    
    
    
    def my_constructor(self,
        SCENEGRAPH = None,
        VIEWING_SETUP = None,
        INPUTS = None,
        ):


        ### external references ###
        self.SCENEGRAPH = SCENEGRAPH
        self.VIEWING_SETUP = VIEWING_SETUP
        self.INPUTS = INPUTS
        
        
        ### parameters ###
        self.ray_length = 25.0 # in meter
        self.ray_thickness = 0.015 # in meter
        self.intersection_point_size = 0.03 # in meter


        ### variables ###
        self.active_navigation_technique_index = 0
        self.active_navigation_technique = None

        ## picking stuff
        self.pick_result = None
        
        self.white_list = []   
        self.black_list = ["invisible"]

        self.pick_options = avango.gua.PickingOptions.PICK_ONLY_FIRST_OBJECT \
                            | avango.gua.PickingOptions.GET_POSITIONS \
                            | avango.gua.PickingOptions.GET_NORMALS \
                            | avango.gua.PickingOptions.GET_WORLD_POSITIONS \
                            | avango.gua.PickingOptions.GET_WORLD_NORMALS


        ### resources ###
           
        ## init nodes
        self.pointer_node = avango.gua.nodes.TransformNode(Name = "pointer_node")
        self.VIEWING_SETUP.navigation_node.Children.value.append(self.pointer_node)
        self.pointer_node.Transform.connect_from(self.INPUTS.sf_pointer_tracking_mat)

        _loader = avango.gua.nodes.TriMeshLoader()

        self.ray_geometry = _loader.create_geometry_from_file("ray_geometry", "data/objects/cylinder.obj", avango.gua.LoaderFlags.DEFAULTS)
        self.ray_geometry.Material.value.set_uniform("Color", avango.gua.Vec4(1.0,0.0,0.0,1.0))
        self.ray_geometry.Tags.value = ["invisible"]
        self.pointer_node.Children.value.append(self.ray_geometry)

        self.intersection_geometry = _loader.create_geometry_from_file("intersection_geometry", "data/objects/sphere.obj", avango.gua.LoaderFlags.DEFAULTS)
        self.intersection_geometry.Material.value.set_uniform("Color", avango.gua.Vec4(1.0,0.0,0.0,1.0))
        self.intersection_geometry.Tags.value = ["invisible"]
        self.SCENEGRAPH.Root.value.Children.value.append(self.intersection_geometry)


        self.ray = avango.gua.nodes.Ray() # required for trimesh intersection

        
        ## init manipulation techniques
        self.steeringNavigation = SteeringNavigation()
        self.steeringNavigation.my_constructor(self)
      
        self.teleportNavigation = TeleportNavigation()
        self.teleportNavigation.my_constructor(self, SCENEGRAPH)

        self.navidgetNavigation = NavidgetNavigation()
        self.navidgetNavigation.my_constructor(self, SCENEGRAPH)



        self.sf_technique_button0.connect_from(self.INPUTS.sf_technique_button0) # key 1
        self.sf_technique_button1.connect_from(self.INPUTS.sf_technique_button1) # key 2
        self.sf_technique_button2.connect_from(self.INPUTS.sf_technique_button2) # key 3
        self.sf_toggle_technique_button.connect_from(self.INPUTS.sf_toggle_technique_button)
        self.sf_reset_button.connect_from(self.INPUTS.sf_reset_button)

        self.VIEWING_SETUP.navigation_node.Transform.connect_from(self.sf_nav_mat)       
    
    
        ### set initial states ###
        self.set_navigation_technique(0)        


    ### functions ###
    def set_navigation_technique(self, INT):  
        # possibly disable prior technique
        if self.active_navigation_technique is not None:
            self.active_navigation_technique.enable(False)
    
        self.active_navigation_technique_index = INT
    
        # enable new technique
        if self.active_navigation_technique_index == 0: # Steering Navigation
            self.active_navigation_technique = self.steeringNavigation
            print("Switch to Steering Navigation")

        elif self.active_navigation_technique_index == 1: # Teleport Navigation
            self.active_navigation_technique = self.teleportNavigation
            print("Switch to Teleport Navigation")

        elif self.active_navigation_technique_index == 2: # Navidget Navigation
            self.active_navigation_technique = self.navidgetNavigation            
            print("Switch to Navidget Navigation")
                        
        self.active_navigation_technique.enable(True)


    def set_navigation_matrix(self, MAT4):
        self.sf_nav_mat.value = MAT4


    def get_navigation_matrix(self):
        return self.sf_nav_mat.value


    def get_head_matrix(self):
        return self.VIEWING_SETUP.head_node.Transform.value


    def calc_pick_result(self):
        # update ray parameters
        self.ray.Origin.value = self.pointer_node.WorldTransform.value.get_translate()

        _vec = avango.gua.make_rot_mat(self.pointer_node.WorldTransform.value.get_rotate()) * avango.gua.Vec3(0.0,0.0,-1.0)
        _vec = avango.gua.Vec3(_vec.x,_vec.y,_vec.z)

        self.ray.Direction.value = _vec * self.ray_length

        # intersect
        _mf_pick_result = self.SCENEGRAPH.ray_test(self.ray, self.pick_options, self.white_list, self.black_list)

        if len(_mf_pick_result.value) > 0: # intersection found
            self.pick_result = _mf_pick_result.value[0] # get first pick result
        else: # nothing hit
            self.pick_result = None


    def update_ray_visualization(self):
        if self.pick_result is not None: # something hit            
            _pick_world_pos = self.pick_result.WorldPosition.value # pick position in world coordinate system    
            _distance = self.pick_result.Distance.value * self.ray_length # pick distance in ray coordinate system        
        
            self.ray_geometry.Transform.value = \
                avango.gua.make_trans_mat(0.0,0.0,_distance * -0.5) * \
                avango.gua.make_rot_mat(-90.0,1,0,0) * \
                avango.gua.make_scale_mat(self.ray_thickness, _distance, self.ray_thickness)

            self.intersection_geometry.Tags.value = [] # set intersection point visible
            self.intersection_geometry.Transform.value = avango.gua.make_trans_mat(_pick_world_pos) * avango.gua.make_scale_mat(self.intersection_point_size)

        else:  # nothing hit --> apply default ray visualization
            self.ray_geometry.Transform.value = \
                avango.gua.make_trans_mat(0.0,0.0,self.ray_length * -0.5) * \
                avango.gua.make_rot_mat(-90.0,1,0,0) * \
                avango.gua.make_scale_mat(self.ray_thickness, self.ray_length, self.ray_thickness)
        
            self.intersection_geometry.Tags.value = ["invisible"] # set intersection point invisible


    def transform_mat_in_ref_mat(self, INPUT_MAT, REFERENCE_MAT):
        _mat = REFERENCE_MAT * \
            INPUT_MAT * \
            avango.gua.make_inverse_mat(REFERENCE_MAT)

        return _mat


    def reset_nav_matrix(self):
        print("reset navigation matrix")
        self.set_navigation_matrix(avango.gua.make_identity_mat())


    ### callback functions ###
    @field_has_changed(sf_technique_button0)
    def sf_technique_button0_changed(self):
        if self.sf_technique_button0.value == True: # button is pressed
            self.set_navigation_technique(0)
            

    @field_has_changed(sf_technique_button1)
    def sf_technique_button1_changed(self):
        if self.sf_technique_button1.value == True: # button is pressed
            self.set_navigation_technique(1)


    @field_has_changed(sf_technique_button2)
    def sf_technique_button2_changed(self):
        if self.sf_technique_button2.value == True: # button is pressed
            self.set_navigation_technique(2)


    @field_has_changed(sf_toggle_technique_button)
    def sf_toggle_technique_button_changed(self):
        if self.sf_toggle_technique_button.value == True: # button is pressed
            _index = (self.active_navigation_technique_index + 1) % 4
            self.set_navigation_technique(_index)


    @field_has_changed(sf_reset_button)
    def sf_reset_button_changed(self):
        if self.sf_reset_button.value == True: # button is pressed
            self.reset_nav_matrix()



class NavigationTechnique(avango.script.Script):


    ## constructor
    def __init__(self):
        self.super(NavigationTechnique).__init__()

        ### variables ###
        self.enable_flag = False
                          

    ### functions ###
    def enable(self, BOOL):
        self.enable_flag = BOOL


    ### calback functions ###
    def evaluate(self): # evaluated every frame
        raise NotImplementedError("To be implemented by a subclass.")


   
class SteeringNavigation(NavigationTechnique):

    ### fields ###

    ## input fields
    mf_dof = avango.MFFloat()
    mf_dof.value = [0.0,0.0,0.0,0.0,0.0,0.0] # init 6 channels

   
    ### constructor
    def __init__(self):
        NavigationTechnique.__init__(self) # call base class constructor


    def my_constructor(self, NAVIGATION_MANAGER):

        ### external references ###
        self.NAVIGATION_MANAGER = NAVIGATION_MANAGER

        ### parameters ###
        self.translation_factor = 0.2
        self.rotation_factor = 1.0

              
        ## init field connections
        self.mf_dof.connect_from(self.NAVIGATION_MANAGER.INPUTS.mf_dof_steering)
        

 
    ### callback functions ###
    def evaluate(self): # implement respective base-class function
        if self.enable_flag == False:
            return        


        ## handle translation input
        _x = self.mf_dof.value[0]
        _y = self.mf_dof.value[1]
        _z = self.mf_dof.value[2]
        
        _trans_vec = avango.gua.Vec3(_x, _y, _z)
        _trans_input = _trans_vec.length()
        #print(_trans_input)
        
        if _trans_input > 0.0: # guard
            # transfer function for translation
            _factor = pow(min(_trans_input,1.0), 2)

            _trans_vec.normalize()
            _trans_vec *= _factor * self.translation_factor


        ## handle rotation input
        _rx = self.mf_dof.value[3]
        _ry = self.mf_dof.value[4]
        _rz = self.mf_dof.value[5]

        _rot_vec = avango.gua.Vec3(_rx, _ry, _rz)
        _rot_input = _rot_vec.length()

        if _rot_input > 0.0: # guard
            # transfer function for rotation
            _factor = pow(_rot_input, 2) * self.rotation_factor

            _rot_vec.normalize()
            _rot_vec *= _factor


        _input_mat = avango.gua.make_trans_mat(_trans_vec) * \
            avango.gua.make_rot_mat(_rot_vec.y,0,1,0) * \
            avango.gua.make_rot_mat(_rot_vec.x,1,0,0) * \
            avango.gua.make_rot_mat(_rot_vec.z,0,0,1)


        ## transform input into head orientation (required for HMD setup)
        _head_rot_mat = avango.gua.make_rot_mat(self.NAVIGATION_MANAGER.get_head_matrix().get_rotate())
        _input_mat = self.NAVIGATION_MANAGER.transform_mat_in_ref_mat(_input_mat, _head_rot_mat)
        
        ## accumulate input to navigation coordinate system
        _new_mat = self.NAVIGATION_MANAGER.get_navigation_matrix() * \
            _input_mat

        self.NAVIGATION_MANAGER.set_navigation_matrix(_new_mat)
        



class TeleportNavigation(NavigationTechnique):

    ### fields ###

    ## input fields
    sf_pointer_button = avango.SFBool()
    
    ### constructor
    def __init__(self):
        NavigationTechnique.__init__(self) # call base class constructor


    def my_constructor(self, NAVIGATION_MANAGER, SCENEGRAPH):

        ### external references ###
        self.NAVIGATION_MANAGER = NAVIGATION_MANAGER

        # set the ray to visible
        self.NAVIGATION_MANAGER.ray_geometry.Tags.value = []

        self.sf_pointer_button.connect_from(self.NAVIGATION_MANAGER.INPUTS.sf_pointer_button)

        self.always_evaluate(True) # change global evaluation policy



    ### callback functions ###
    def evaluate(self): # implement respective base-class function
        if self.enable_flag == False:
            return

        ## To-Do: realize Teleport navigation here
        self.NAVIGATION_MANAGER.calc_pick_result()
        self.NAVIGATION_MANAGER.update_ray_visualization()



class NavidgetNavigation(NavigationTechnique):

    ### fields ###

    ## input fields
    sf_pointer_button = avango.SFBool()
    
    ### constructor
    def __init__(self):
        NavigationTechnique.__init__(self) # call base class constructor


    def my_constructor(self, NAVIGATION_MANAGER, SCENEGRAPH):

        ### external references ###
        self.NAVIGATION_MANAGER = NAVIGATION_MANAGER


        ### parameters ###
        self.navidget_duration = 3.0 # in seconds


        self.sf_pointer_button.connect_from(self.NAVIGATION_MANAGER.INPUTS.sf_pointer_button)

        self.always_evaluate(True) # change global evaluation policy

        

    ### functions ###
    def get_rotation_matrix_between_vectors(self, VEC1, VEC2): # helper function to calculate rotation matrix to rotate one vector (VEC3) on another one (VEC2)
        VEC1.normalize()
        VEC2.normalize()

        _z_axis = VEC2
        _y_axis = VEC1
        _x_axis = _y_axis.cross(_z_axis)
        _y_axis = _z_axis.cross(_x_axis)

        _x_axis.normalize()
        _y_axis.normalize()

        # create new rotation matrix
        _mat = avango.gua.make_identity_mat()
        
        _mat.set_element(0,0, _x_axis.x)
        _mat.set_element(1,0, _x_axis.y)
        _mat.set_element(2,0, _x_axis.z)

        _mat.set_element(0,1, _y_axis.x)
        _mat.set_element(1,1, _y_axis.y)
        _mat.set_element(2,1, _y_axis.z)
        
        _mat.set_element(0,2, _z_axis.x)
        _mat.set_element(1,2, _z_axis.y)
        _mat.set_element(2,2, _z_axis.z)
        
        _mat = _mat * avango.gua.make_rot_mat(180.0,0,1,0)
        
        return _mat

        

    ### callback functions ###
    def evaluate(self): # implement respective base-class function
        if self.enable_flag == False:
            return

        ## To-Do: realize Navidget navigation here

