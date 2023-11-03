"""Tests the input controller's functions except warning
"""
import json

import pytest
from pytest import MonkeyPatch

from controller.output_controller import OutputController
from controller.helpers import api_file_processor
from controller.widgets import file_tile_widget
import controller.constants as constants
from PyQt6.QtWidgets import QGraphicsView, QGraphicsScene, QSpinBox, QWidget, QProgressDialog 
from PyQt6.QtCore import QRunnable, QThreadPool
from PyQt6.QtGui import QPixmap 
from controller.helpers import api_file_processor

from  models.user_model import UserInfo
from controller.widgets.file_tile_widget import FileTile, WorkerSignals, FileTileCreatorWorker
@pytest.mark.order(1)
@pytest.fixture(scope="module")
def output_controller():
    
    parent = QWidget()
    file_grid_scene_in = QGraphicsScene()
    file_grid_view = QGraphicsView()
    quality_input_spinbox = QSpinBox()
    
    output_controller = OutputController(
        parent, file_grid_scene_in, file_grid_view, quality_input_spinbox
    )
    output_controller.size_type = "MB"
    
    yield output_controller


@pytest.mark.order(2)
def test_build_file_table(qtbot, mocker, output_controller:OutputController):
    """Testing the build file function. Testing the ability of the function to assign positions to
    the tiles and tell the tiles it's neighbors

    Args:
        qtbot (_type_): qt fixture from pyqt
        mocker (_type_): mock fixture from pyqt mock
        output_controller (OutputController): output_controller fixture
    """

    SAMPLE_METADATA_FILE = ".\\tests\\fake_user_data_files\\sample_file_metadata.json"
    file_metadata = []
    with open(SAMPLE_METADATA_FILE, "r") as json_file:
        file_metadata = json.load(json_file)
        
    def get_file_thumbnail(id):
        return QPixmap(50,50)
    mocker.patch('controller.helpers.api_file_processor.get_file_thumbnail', get_file_thumbnail)
    tiles = []
    for id in file_metadata:
        tiles.append(FileTile(file_metadata[id], 300, 300, "mb"))
    output_controller.file_tile_list = tiles
    output_controller.build_file_table()
    for file_tile in output_controller.file_tile_list:
        assert file_tile.x() == 10.0 or 220.0
        assert file_tile.y() == 10.0 or 220.0 or 430.0 or 640.0 or 850.0
        assert file_tile.ordered_sibling_tiles is not None
    
@pytest.mark.order(3)
def test_process_api_files_table(qtbot, monkeypatch, mocker, output_controller:OutputController):
    # output_controller.build_file_table()
    SAMPLE_METADATA_FILE = ".\\tests\\fake_user_data_files\\sample_file_metadata.json"
    file_metadata = []
    with open(SAMPLE_METADATA_FILE, "r") as json_file:
        file_metadata = json.load(json_file)


    class fake_pool():
        def __init__(self,r) -> None:
            pass
        def start(a):
            pass
    mocker.patch('PyQt6.QtCore.QThreadPool.start', fake_pool)
    
    class fake_thread():
        def init():
            pass
        def exec():
            pass
        
    mocker.patch('PyQt6.QtWidgets.QProgressDialog.exec', fake_thread)
    
    def get_file_thumbnail(self):
        return QPixmap(50,50)
    mocker.patch('controller.helpers.api_file_processor.get_file_thumbnail', get_file_thumbnail)
    
    tiles = []
    for id in file_metadata:
        tiles.append(FileTile(file_metadata[id], 300, 300, "mb"))
    mocker.patch('controller.widgets.file_display_scene_widget.FileDisplayScene', [])
    
    mocker.patch("controller.output_controller.OutputController")
    
    output_controller.process_api_files_metadata(file_metadata)
    