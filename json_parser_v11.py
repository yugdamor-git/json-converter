project = {
        "name":"project-xyz"
    }

core = {
    "buffer_size":18,
    "filepath":{},
    "default_filepath":""
}

image_grid = {
    "img_height":80,
    "rshape_fill":"none",
    "rshape_fill_opacity":0.3,
    "rshape_stroke":"yellow",
    "rshape_stroke_width":2,
    "show_region_shape":True,
    "show_image_policy":"all"
}

image = {
    "region_label":"__via_region_id__",
    "region_color":"__via_default_region_color__",
    "region_label_font":"10px Sans",
    "on_image_annotation_editor_placement":"NEAR_REGION"
}

ui = {
    "annotation_editor_height":20,
    "annotation_editor_fontsize":0.8,
    "leftsidebar_width":18,
    "image_grid":image_grid,
    "image":image
}
via_settings = {
    "ui":ui,
    "core":core,
    "project":project
}


import os
import uuid
import json

class JsonParser:
    def create_folder(self,path):
        try:
            os.mkdir(path)
            
        except:
            pass
        
    def get_class_index(self,Class):
        temp_class = Class.lower()
        if not temp_class in self.all_class:
            new_index = len(self.all_class.keys()) + 1
            self.all_class[temp_class] = {"class_name":temp_class,"index":str(new_index)}
        return self.all_class[temp_class]["index"]
    
    def get_options(self):
        all_ops = {}
        for op in self.all_class:
            op_val = self.all_class[op]
            key = op_val["index"]
            value = op_val["class_name"]
            all_ops[key] = value
        all_ops["10000"] = "Out_Of_Roi"
        return all_ops
    
    def parse_json_data(self,json_data):
        temp = {}
        image = json_data["image"]
        filename = image["filename"]
        if not filename in self.all_filenames:
            self.all_filenames.append(filename)
        size = 0
        regions = []
        file_attributes = {}

        annotations = json_data["annotations"]

        for annotation in annotations:
            Class = annotation["name"]
            index = self.get_class_index(Class)
            region_attributes = {"Class":index}
            for region_item in annotation.items():
                if region_item[0] == "polygon":
                    shape_attributes = {}
                    shape_attributes["all_points_x"] = []
                    shape_attributes["all_points_y"] = []
                    shape_attributes["name"] = "polyline"

                    for p in region_item[1]["path"]:
                        shape_attributes["all_points_x"].append(p["x"])
                        shape_attributes["all_points_y"].append(p["y"])

                    regions.append({"shape_attributes":shape_attributes,"region_attributes":region_attributes})
        temp[filename] = {
            "filename":filename,
            "size":size,
            "regions":regions,
            "file_attributes":{}
        }

        return temp
    
    def load_json(self,file_path):
        temp = None
        with open(file_path,"r") as f:
            temp = json.load(f)
        return temp
        
    def __init__(self):
        print("json parser")
        self.cur_dir = os.getcwd()
        self.input_dir = os.path.join(self.cur_dir,"input")
        self.create_folder(self.input_dir)
        self.output_dir = os.path.join(self.cur_dir,"output")
        self.create_folder(self.output_dir)
        self.all_data = {}
        self.all_class = {}
        self.all_filenames = []
    
    def parse_input_files(self):
        all_input_files = os.listdir(self.input_dir)
        if len(all_input_files) >  0:
            print(f'total input file : {len(all_input_files)}')
            for file in all_input_files:
                print(f'processing -> {file}')
                filepath = os.path.join(self.input_dir,file)
                json_data = self.load_json(filepath)
                output_data = self.parse_json_data(json_data)
                self.all_data.update(output_data)
            
            return self.all_data,True
        else:
            return {},False
    
    def export_json_file(self,json_data,filename_postfix,file_prefix):
        filename = f'{file_prefix}_{filename_postfix}.json'
        file_path = os.path.join(self.output_dir,filename)
        print(f'Exporting {filename_postfix} file, path -> {file_path}')
        with open(file_path, 'w') as outfile:
            json.dump(json_data, outfile)


if __name__ == "__main__":
    project_file = {}
    annotation_file = {}
    jp = JsonParser()
    via_img_metadata,status = jp.parse_input_files()
    if status == True:
        via_attributes = {
            "region":{
                "Class":{
                    "type":"dropdown",
                    "options":jp.get_options(),
                    "default_options":{
                        "10000":True
                    }
                }
            },
            "file":{}
        }

        via_data_format_version = "2.0.10"

        via_image_id_list = jp.all_filenames

        annotation_file = via_img_metadata

        project_file = {
            "_via_settings":via_settings,
            "_via_img_metadata":via_img_metadata,
            "_via_attributes":via_attributes,
            "_via_data_format_version":via_data_format_version,
            "_via_image_id_list":via_image_id_list
        }
        file_prefix = uuid.uuid4()
        jp.export_json_file(annotation_file,"mask",file_prefix)
        jp.export_json_file(project_file,"project",file_prefix)
    else:
        print("Please put some input files in input folder")
    
    print("")
    xxx = input("press any key to close this window")
