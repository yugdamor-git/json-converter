
import streamlit as st
import time
import json

from streamlit.commands.page_config import valid_menu_item_key

# class JsonConverter:
#     def __init__(self):
#         print("json converter init")

#     def load_json(self,byte_data):
#         json_temp = None
#         json_temp = json.load(byte_data)
#         return json_temp

#     def json_to_json_converter(self,byte_data):
#         temp = {}

#         project = {
#             "name":"Part_342_(3a)"
#         }

#         core = {
#             "buffer_size":18,
#             "filepath":{},
#             "default_filepath":""
#         }

#         image_grid = {
#             "img_height":80,
#             "rshape_fill":"none",
#             "rshape_fill_opacity":0.3,
#             "rshape_stroke":"yellow",
#             "rshape_stroke_width":2,
#             "show_region_shape":True,
#             "show_image_policy":"all"
#         }

#         image = {
#             "region_label":"__via_region_id__",
#             "region_color":"__via_default_region_color__",
#             "region_label_font":"10px Sans",
#             "on_image_annotation_editor_placement":"NEAR_REGION"
#         }

#         ui = {
#             "annotation_editor_height":20,
#             "annotation_editor_fontsize":0.8,
#             "leftsidebar_width":18,
#             "image_grid":image_grid,
#             "image":image
#         }
#         via_settings = {
#             "ui":ui,
#             "core":core,
#             "project":project
#         }

#         src_json = self.load_json(byte_data)
#         st.write(src_json)
#         image =  src_json["image"]
#         root_key = image["filename"]
#         filename = root_key
#         size = 0
#         annotations = src_json["annotations"]
#         regions = []
#         unique_class = {}
#         unique_class["500"] = "Out_Of_Roi"
#         for annotation in annotations:
#             shape_attributes = {}
#             shape_attributes["name"] = "polyline"
#             polygon = annotation["polygon"]["path"]
#             name = annotation["name"]
#             temp_class = None
#             if not name in unique_class:
#                 temp_class = str(len(unique_class.keys()) + 1)
#                 unique_class[name] = temp_class
#             else:
#                 temp_class = unique_class[name]
#             Class = temp_class
#             all_points_x = []
#             all_points_y = []
#             for point in polygon:
#                 all_points_x.append(point["x"])
#                 all_points_y.append(point["y"])
#             shape_attributes["all_points_x"] = all_points_x
#             shape_attributes["all_points_y"] = all_points_y
#             region_attributes = {'Class':Class}
#             regions.append({"shape_attributes":shape_attributes,"region_attributes":region_attributes})
        
#         via_img_metadata = {
#             filename:{
#                 "filename":filename,
#                 "size":size,
#                 "regions":regions,
#                 "file_attributes":{}
#             }
#         }

#         dropdown_options = {}
#         for cls in unique_class:
#             dropdown_options[unique_class[cls]] = cls
#         region = {
#             "Class":{
#                 "type":"dropdown",
#                 "description":"",
#                 "options":dropdown_options,
#                 "default_options":{
#                     "500":True
#                 }
#             }
#         }
#         via_attributes = {
#             "region":region,
#             "file":{}
#         }
#         via_data_format_version = st.session_state["via_data_format_version"]
#         via_image_id_list = [
#             "_via_settings",
#             "_via_img_metadata",
#             "_via_attributes",
#             "_via_data_format_version",
#             "_via_image_id_list",
#             filename
#         ]


#         temp =  {
#             "_via_settings":via_settings,
#             "_via_img_metadata":via_img_metadata,
#             "_via_attributes":via_attributes,
#             "_via_data_format_version":via_data_format_version,
#             "_via_image_id_list":via_image_id_list
#         }

#         return temp,via_img_metadata

welcome_text = """
                                                                                                           
       _|    _|_|_|    _|_|    _|      _|      _|_|_|      _|_|    _|_|_|      _|_|_|  _|_|_|_|  _|_|_|    
       _|  _|        _|    _|  _|_|    _|      _|    _|  _|    _|  _|    _|  _|        _|        _|    _|  
       _|    _|_|    _|    _|  _|  _|  _|      _|_|_|    _|_|_|_|  _|_|_|      _|_|    _|_|_|    _|_|_|    
 _|    _|        _|  _|    _|  _|    _|_|      _|        _|    _|  _|    _|        _|  _|        _|    _|  
   _|_|    _|_|_|      _|_|    _|      _|      _|        _|    _|  _|    _|  _|_|_|    _|_|_|_|  _|    _|  
                                                                                                           
                                                                                                           
"""

import pandas as pd
PROJECT_NAME = ""
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
            value = op_val["class_name"].title().strip().replace(" ","_")
            all_ops[key] = value
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

        return temp,filename
    
    def load_json(self,f):
        # temp = None
        # with open(file_path,"r") as f:
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
        # self.load_labels_file()
        self.all_processed_files = []
    
    def parse_input_file(self,file_data):
        # all_input_files = os.listdir(self.input_dir)
        # if len(all_input_files) >  0:
        #     print(f'total input file : {len(all_input_files)}')
        #     for file in all_input_files:
        #         print(f'processing -> {file}')
        #         filepath = os.path.join(self.input_dir,file)
        # st.write(self.all_class)
        json_data = self.load_json(file_data)
        output_data,filename = self.parse_json_data(json_data)
        self.all_data.update(output_data)
        return self.all_data,True,filename

    def export_json_file(self,json_data,filename_postfix,file_prefix):
        filename = f'{file_prefix}_{filename_postfix}.json'
        file_path = os.path.join(self.output_dir,filename)
        print(f'Exporting {filename_postfix} file, path -> {file_path}'.upper())
        self.all_processed_files.append((filename,json_data))
        # with open(file_path, 'w') as outfile:
        #     json.dump(json_data, outfile)

    def load_text_file(self,path):
        data = None
        final_data = []
        with open(path,"r") as f:
            data = f.read()
        for line in data.split("\n"):
            if len(line.strip()) > 0:
                class_id_temp = line.split("-Class")
                class_name = class_id_temp[0].replace("_"," ").lower().strip()
                class_id = class_id_temp[1].replace("#","").strip()
                final_data.append({"index":class_id,"class_name":class_name})
        return final_data

    def load_labels_file(self,df):
        try:
            # label_file_name = "annotation.txt"
            # label_file_path = os.path.join(self.cur_dir,label_file_name)
            # loaded_data = self.load_text_file(label_file_path)
            # for row in loaded_data:
            #     self.all_class[row['class_name']] = row
            for index,row in df.iterrows():
                temp_dict = row.to_dict()
                id = str(temp_dict["id"]).lower()
                label = str(temp_dict["label"]).lower()
                if len(id) > 0 and len(label) > 0:
                    print(f'loading label : {id} {label}'.upper())
                    if not label in self.all_class.keys():
                        self.all_class[label] = {"class_name":label,"index":id}
        except Exception as e:
            print(str(e))
            print("No annotation.txt file found/format is different.".upper())
            exit(0)

def process_multiple_files(project_name,input_csv,input_files):
    all_out = []
    project = {}
    PROJECT_NAME = project_name
    project["name"] = PROJECT_NAME
    via_settings = {
        "ui":ui,
        "core":core,
        "project":project
    }
    project_file = {}
    annotation_file = {}
    jp = JsonParser()
    jp.load_labels_file(input_csv)
    all_input_files = input_files

    if len(all_input_files) >  0:
        st.info(f'You uploaded total {len(all_input_files)} files.')
        print(f'Total input file : {len(all_input_files)}'.upper())
        for file in all_input_files:
            # try:
            jp = JsonParser()
            jp.load_labels_file(input_csv)
            project_file = {}
            annotation_file = {}
            print(f'processing -> {file[0]}'.upper())
            # filepath = os.path.join(jp.input_dir,file)
            via_img_metadata,status,filename = jp.parse_input_file(file[1])
            if status == True:
                via_attributes = {
                    "region":{
                        "Class":{
                            "type":"dropdown",
                            "options":jp.get_options(),
                            "default_options":{
                                jp.all_class["out_of_roi"]["index"]:True
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
                file_prefix = filename.split(".")[0]
                print("export")
                jp.export_json_file(annotation_file,"mask",file_prefix)
                jp.export_json_file(project_file,"project",file_prefix)
                for f in jp.all_processed_files:
                    all_out.append(f)
            # except Exception as e:
            #     print(str(e))
            #     print("Please check this file , did not able to process it.".upper(),file)
    else:
        print("Please put some input files in input folder".upper())
    return all_out


def create_zip(files):
    import io
    import zipfile
    
    zip_buffer = io.BytesIO()
    
    with zipfile.ZipFile(zip_buffer, "a", zipfile.ZIP_DEFLATED, False) as zip_file:
        for file_name, data in files:
            j_str = json.dumps(data)
            j_obj = j_str.encode('utf-8')
            zip_file.writestr(file_name,j_obj)
    st.success(f'zip created : there are total {len(files)} files in zip.')
    return zip_buffer





def get_value(key):
    if key in st.session_state:
        return st.session_state[key]
    else:
        return None
def save_value(key,value):
    st.session_state[key] = value

def save_value_config(key,value):
    if not key in st.session_state:
        st.session_state[key] = value

def handle_config(config):
    for item in config:
        save_value_config(item,config[item])
        btn_value = sidebar.text_input(item,get_value(item))
        print(btn_value)
        print(get_value(item))
        if btn_value != get_value(item):
            save_value(item,btn_value)


# json_converter = JsonConverter()

# st.write(welcome_text)
sidebar = st.sidebar

sidebar.title("JSON CONVERTER - VGG")
sidebar.header("first upload labels.csv and then upload all input files. this app will create one combined zip file as output.")
input_csv = None
labels_csv = sidebar.file_uploader("Labels",type=["csv"])
if labels_csv == None:
    sidebar.warning("Please select labels.csv file first.")
else:
    try:
        input_csv = pd.read_csv(labels_csv)
        sidebar.write(input_csv)
    except:
        st.error("invalid file")
# config = {
#     "via_data_format_version":"2.0.10"
# }

# handle_config(config)

# input_format = st.selectbox("Please Select Input File Format",["json"],index=0,key="input_format")
# if not input_format is None:
#     output_format = st.selectbox("Please Select Output File Format",["json"],index=0,key="output_format")
#     if not output_format is None:
input_file  = st.file_uploader("please select input files.",type=['json'],accept_multiple_files=True)
# if not input_file.empty:
all_input_files = []
for file in input_file:
    all_input_files.append((file.name,file))

if len(all_input_files) > 0:
    all_output_files = process_multiple_files("yug damor",input_csv,all_input_files)

    if len(all_output_files) > 0:
        st.download_button("Download Zip",data=create_zip(all_output_files),mime="application/zip")
# else:
#     st.error("please upload labels.csv too...")
# st.write(input_file)
    # input_filename = input_file.name

    # output_filename = f'output_{input_filename}'

    # output_file_data,output_file_data_2 = json_converter.json_to_json_converter(input_file)
    # st.download_button("Download Output 1",data=json.dumps(output_file_data_2),mime="application/json")
    # st.download_button("Download Output 2",data=json.dumps(output_file_data),mime="application/json")

    # st.header("output preview")    
    # st.write(output_file_data)

    # st.header("target preview")    
    # tr = None
    # with open("files/output2.json","r") as f:
    #     tr = json.load(f)
    # st.write(tr)


