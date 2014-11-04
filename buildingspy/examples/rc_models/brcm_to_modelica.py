import os
from buildingspy.rc_models.rc_model import RcModel

def main():
    '''
    Main method that open the ``*.mat`` file containing the details of the
    BRCM model and creates a corresponding Modelica model.
    
    The models generated by this example are called
    
    * ``RcModelFiveZones.mo``
    * ``AvgModel.mo``
    
    and will be saved in the current directory where the module is executed
    '''
    
    # Path of the *.mat file that contains the details of the BRCM model
    dir_path = os.path.dirname(os.path.realpath(__file__))
    mat_file_path = os.path.abspath(os.path.join(dir_path, "mat_files", "model_summary.mat"))
    
    # Instantiate the RC model object
    m = RcModel()
    
    # Load the details of the BRCM model from the *.mat file
    m.load_from_brcm(mat_file_path)
    
    # Create the Modelica RC model named 'RcModelFiveZones.mo'
    m.generate_modelica_rc_model(dir_path = ".", model_name = "RcModelFiveZones", \
                                  description = "RC model of a five zones residential building")
    
    # Create the Modelica model that computes the average of the zone temperatures
    # named 'AvgModel.mo'   
    m.generate_modelica_avg_model(dir_path = ".", model_name = "AvgModel", \
                                   description = "Model that computes the average of the zones temperatures")

# Main function
if __name__ == '__main__':
    main()