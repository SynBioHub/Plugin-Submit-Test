from flask import Flask, request, abort, send_file, jsonify
import os
import shutil
import tempfile
import sys
import traceback
from werkzeug.utils import secure_filename

app = Flask(__name__)


@app.route("/status")
def status():
    return("The Submit Test Plugin Flask Server is up and running")


@app.route("/evaluate", methods=["POST"])
def evaluate():
    # uses MIME types
    # https://developer.mozilla.org/en-US/docs/Web/HTTP/Basics_of_HTTP/MIME_types/Common_types

    eval_manifest = request.get_json(force=True)
    files = eval_manifest['manifest']['files']

    eval_response_manifest = {"manifest": []}

    for file in files:
        file_name = file['filename']
        file_type = file['type']
        # file_url = file['url']

        # ~~~~~~~~~~~ REPLACE THIS SECTION WITH OWN RUN CODE ~~~~~~~~~~~~~~~~~~
        # IN THE SPECIAL CASE THAT THE EXTENSION HAS NO MIME TYPE
        # USE SOMETHING LIKE THIS (UNCOMMENT LINE 29)
        # NB: THIS WILL REQUIRE UPDATING THE TESTING
        # file_type = file_name.split('.')[-1]
        #
        # #types that can be converted to sbol by this plugin
        # acceptable_types = {'dna', 'docx', 'txt'}

        # types that can be converted to sbol by this plugin
        acceptable_types = {'application/vnd.ms-excel',
                            'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'}

        # types that are useful (will be served to the run endpoint too but
        # noted that they won't be converted)
        useful_types = {'application/xml'}

        file_type_acceptable = file_type in acceptable_types
        file_type_useable = file_type in useful_types

        # to ensure all file types are accepted
        file_type_acceptable = True
        # ~~~~~~~~~~~~~~~~~ END SECTION ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

        if file_type_acceptable:
            useableness = 2
        elif file_type_useable:
            useableness = 1
        else:
            useableness = 0

        eval_response_manifest["manifest"].append({
            "filename": file_name,
            "requirement": useableness})

    return jsonify(eval_response_manifest)


@app.route("/run", methods=["POST"])
def run():

    # create a temporary directory
    temp_dir = tempfile.TemporaryDirectory()
    zip_in_dir_name = temp_dir.name

    # take in run manifest
    run_manifest = request.get_json(force=True)
    files = run_manifest['manifest']['files']

    # initiate response manifest
    run_response_manifest = {"results": []}

    for a_file in files:
        try:
            file_name = a_file['filename']
            file_type = a_file['type']
            file_url = a_file['url']
            data = str(a_file)

            converted_file_name = secure_filename(f"{file_name}.converted")
            file_path_out = os.path.join(zip_in_dir_name, converted_file_name)

            # ~~~~~~~~~~~~~ REPLACE THIS SECTION WITH OWN RUN CODE ~~~~~~~~~~~~
            cwd = os.getcwd()
            file_path = os.path.join(cwd, "Test.xml")

            # read in Test.xml
            with open(file_path, 'r') as xmlfile:
                result = xmlfile.read()

            # put in the url, filename, and instance given by synbiohub
            result = result.replace("TEST_FILE", file_name)
            result = result.replace("REPLACE_FILENAME", file_name)
            result = result.replace("REPLACE_FILETYPE", file_type)
            result = result.replace("REPLACE_FILEURL", file_url)
            result = result.replace("FILE_DATA_REPLACE", data)
            sbolcontent = result.replace("DATA_REPLACE", str(run_manifest))
            # ~~~~~~~~~~~~~~~~~~~~ END SECTION ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

            # write out result to "To_zip" file
            with open(file_path_out, 'w') as xmlfile:
                xmlfile.write(sbolcontent)

            # add name of converted file to manifest
            run_response_manifest["results"].append({"filename": converted_file_name,
                                                     "sources": [file_name]})

        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            lnum = exc_tb.tb_lineno
            abort(415, f'Exception is: {e}, exc_type: {exc_type}, exc_obj: {exc_obj}, fname: {fname}, line_number: {lnum}, traceback: {traceback.format_exc()}')

    # create manifest file
    file_path_out = os.path.join(zip_in_dir_name, "manifest.json")
    with open(file_path_out, 'w') as manifest_file:
        manifest_file.write(str(run_response_manifest))

    with tempfile.NamedTemporaryFile() as temp_file:
        # create zip file of converted files and manifest
        shutil.make_archive(temp_file.name, 'zip', zip_in_dir_name)

        # delete zip in directory
        shutil.rmtree(zip_in_dir_name)

        # return zip file
        return send_file(f"{temp_file.name}.zip")
