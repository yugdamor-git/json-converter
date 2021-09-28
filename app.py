
import streamlit as st
import time
import json

class JsonConverter:
    def __init__(self):
        print("json converter init")
    
    def load_json(self,byte_data):
        json_temp = None
        # with open(file_path) as f:
        json_temp = json.load(byte_data)
        return json_temp

    def json_to_json_converter(self,byte_data):
        temp = {}

        project = {
            "name":"Part_342_(3a)"
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

        src_json = self.load_json(byte_data)
        st.write(src_json)
        image =  src_json["image"]
        root_key = image["filename"]
        filename = root_key
        size = 0
        annotations = src_json["annotations"]
        regions = []
        unique_class = {}
        unique_class["500"] = "Out_Of_Roi"
        for annotation in annotations:
            shape_attributes = {}
            shape_attributes["name"] = "polyline"
            polygon = annotation["polygon"]["path"]
            name = annotation["name"]
            temp_class = None
            if not name in unique_class:
                temp_class = str(len(unique_class.keys()) + 1)
                unique_class[name] = temp_class
            else:
                temp_class = unique_class[name]
            Class = temp_class
            all_points_x = []
            all_points_y = []
            for point in polygon:
                all_points_x.append(point["x"])
                all_points_y.append(point["y"])
            shape_attributes["all_points_x"] = all_points_x
            shape_attributes["all_points_y"] = all_points_y
            region_attributes = {'Class':Class}
            regions.append({"shape_attributes":shape_attributes,"region_attributes":region_attributes})
        
        via_img_metadata = {
            filename:{
                "filename":filename,
                "size":size,
                "regions":regions,
                "file_attributes":{}
            }
        }

        dropdown_options = {}
        for cls in unique_class:
            dropdown_options[unique_class[cls]] = cls
        region = {
            "Class":{
                "type":"dropdown",
                "description":"",
                "options":dropdown_options,
                "default_options":{
                    "500":True
                }
            }
        }
        via_attributes = {
            "region":region,
            "file":{}
        }
        via_data_format_version = "2.0.10"
        via_image_id_list = [
            "_via_settings",
            "_via_img_metadata",
            "_via_attributes",
            "_via_data_format_version",
            "_via_image_id_list",
            filename
        ]


        temp =  {
            "_via_settings":via_settings,
            "_via_img_metadata":via_img_metadata,
            "_via_attributes":via_attributes,
            "_via_data_format_version":via_data_format_version,
            "_via_image_id_list":via_image_id_list
        }

        return temp


json_converter = JsonConverter()

sidebar = st.sidebar

sidebar.title("JSON CONVERTER")
sidebar.header("This web app allows you to convert json file to any other format.")

input_format = st.selectbox("Please Select Input File Format",["json"],index=0,key="input_format")
if not input_format is None:
    output_format = st.selectbox("Please Select Output File Format",["json"],index=0,key="output_format")
    if not output_format is None:
        input_file  = st.file_uploader("upload file",type=['json'])
        if input_file != None:
            input_filename = input_file.name
        
            output_filename = f'output_{input_filename}'
            output_file_data = json_converter.json_to_json_converter(input_file)

            st.download_button("Download",data=json.dumps(output_file_data),mime="application/json")

            st.header("output preview")    
            st.write(output_file_data)


