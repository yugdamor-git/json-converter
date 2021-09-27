
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
        src_json = self.load_json(byte_data)
        temp = {}
        image =  src_json["image"]
        root_key = image["filename"]
        filename = root_key
        size = 0
        annotations = src_json["annotations"]
        regions = []
        for annotation in annotations:
            shape_attributes = {}
            shape_attributes["name"] = "polyline"
            polygon = annotation["polygon"]["path"]
            Class = annotation["name"].split("#")[-1].strip()
            all_points_x = []
            all_points_y = []
            for point in polygon:
                all_points_x.append(point["x"])
                all_points_y.append(point["y"])
            shape_attributes["all_points_x"] = all_points_x
            shape_attributes["all_points_y"] = all_points_y
            region_attributes = {'Class':Class}
            shape_attributes["region_attributes"] = region_attributes
            regions.append({"shape_attributes":shape_attributes})
        temp[root_key] = {"filename":filename,"size":size,"regions":regions,"file_attributes":{}}
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


