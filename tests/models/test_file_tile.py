"""Tests the settings model
"""
import json
import pytest 
from queue import Queue

from unittest.mock import MagicMock

from PyQt6.QtCore import QThreadPool, Qt
from PyQt6.QtWidgets import QGraphicsSceneMouseEvent

from models.file_tile import FileTile, FileTileCreatorWorker

FILESMETADATAEX = "FilesMetadataExample.json"

temp_path = f"tests\\models\\{FILESMETADATAEX}"

with open(temp_path, 'r') as file:
    files_metadata = json.load(file)

@pytest.fixture(autouse=True,scope="function")
def patch_thumbnail_mock(monkeypatch):
    """Patches thumbnail so it doesnt call api
    """
    
    thumbnail_mock = MagicMock()
    thumbnail_mock.return_value = MagicMock()
    monkeypatch.setattr("models.hydrus_api.get_file_thumbnail", thumbnail_mock)

def test_init_filetile_good_metadata():
    """Using good metadata, lets create a file
    """
    correct_metadata = files_metadata[0]
    
    file_tile_gb = FileTile(
        files_metadata[0],
        670,
        434,
        "GB"
    )
    assert file_tile_gb.calculated_size == round(correct_metadata["size"] / (1024**3), 2)

    tile_width = 200
    tile_height = 600
    file_tile = FileTile(
        files_metadata[0],
        tile_width,
        tile_height,
        "MB"
    )
    assert file_tile.calculated_size == round(correct_metadata["size"] / (1024**2), 2)
    
    assert file_tile.file_id == correct_metadata["file_id"]
    file_type, extension = correct_metadata["mime"].split("/")
    assert file_tile.file_type == file_type
    assert file_tile.extension == extension
    
    assert file_tile.size_bytes == correct_metadata["size"]
    assert file_tile.tags == correct_metadata["tags"]
    assert file_tile.ratings == correct_metadata["ratings"]
    assert file_tile.notes == correct_metadata["notes"]
    assert file_tile.unix_modified_time == correct_metadata["time_modified_details"]["local"]
    
    for service_id in file_tile.tags:
        assert file_tile.storage_tags[service_id] == file_tile.tags[service_id]["storage_tags"]
        

def test_filetile_update():
    """Test update event
    """
    correct_metadata = files_metadata[0]
    
    file_tile = FileTile(
        files_metadata[0],
        670,
        434,
        "GB"
    )
    file_tile.highlight_tile = True
    file_tile.update()
    

def test_filetile_paint():
    """ Test paint event just in case
    """
    mock_painter = MagicMock()
    
    file_tile = FileTile(
        files_metadata[0],
        670,
        434,
        "GB"
    )
    
    file_tile.scaled_pixmap = MagicMock()
    file_tile.highlight_tile = True
    file_tile.paint(mock_painter)
    
    file_tile.scaled_pixmap = MagicMock()
    file_tile.highlight_tile = False
    file_tile.paint(mock_painter)

def test_basic_click_event():
    """Test the basic click event
    """
    
    file_tile_list = []
    for i in range(0,5):
        file_tile_list.append(FileTile(
            files_metadata[0],
            i,
            434,
            "GB"
            ))
    
    for file in file_tile_list:
        file.set_ordered_tiles(file_tile_list)
        
    event = MagicMock(spec=QGraphicsSceneMouseEvent)
    
    file_tile = file_tile_list[0]
    file_tile.mousePressEvent(event)
    assert file_tile.highlight_tile == True
    

def make_file_tile_list(num_files:int, tile_width:int, tile_height:int)->[FileTile]:
    """Generates a file_tile list from a singular file_metadata

    Args:
        num_files (int): number of file_tiles
        tile_width (int): tile widht
        tile_height (int): tile height

    Returns:
        [fileTile]: resulting list
    """
    file_tile_list = []
    for i in range(0, num_files):
        file_tile_list.append(FileTile(
            files_metadata[0],
            tile_width,
            tile_height,
            "GB"))
        
    for file in file_tile_list:
        file.set_ordered_tiles(file_tile_list)
        
    return file_tile_list

def test_thread_make_file_tiles(qtbot):
    """This ability was implemented because I thought rendering might be better multi threaded
       Instead i was merely bad at coding
    """
    
    file_tile_list = make_file_tile_list(5, 10, 10)
    tiles = Queue()
    thread_pool = QThreadPool.globalInstance()
    assert tiles.qsize() == 0
    for file_metadata in files_metadata:
        worker = FileTileCreatorWorker(
            file_metadata,
            2,
            3,
            tiles,
            "MB"
        )
        thread_pool.tryStart(worker)
        
    thread_pool.waitForDone()
    assert tiles.qsize() == 2
    
    
def test_ctrl_click():
    """Multiple ctrl clicks on different tiles should highlight them all 
    """
    
    file_tile_list = make_file_tile_list(5, 10, 10)
    
    for file in file_tile_list:
        file.set_ordered_tiles(file_tile_list)
    
    file_tile_list[4].highlight_tile = True
    file_tile_list[3].highlight_tile = True
    
    event = MagicMock(spec=QGraphicsSceneMouseEvent)
    event.modifiers.return_value = Qt.KeyboardModifier.ControlModifier
    file_tile = file_tile_list[0]
    file_tile.mousePressEvent(event)
    assert file_tile_list[0].highlight_tile == True
    assert file_tile_list[1].highlight_tile == False
    assert file_tile_list[2].highlight_tile == False
    assert file_tile_list[3].highlight_tile == True
    assert file_tile_list[4].highlight_tile == True
    
    # test regular click should reset everything
    event.modifiers.return_value = Qt.KeyboardModifier.NoModifier
    file_tile_list[2].mousePressEvent(event)
    assert file_tile_list[0].highlight_tile == False
    assert file_tile_list[1].highlight_tile == False
    assert file_tile_list[2].highlight_tile == True
    assert file_tile_list[3].highlight_tile == False
    assert file_tile_list[4].highlight_tile == False
    
def test_shift_click_cases():
    """ After clicking somewhere, a shift click should highlight based off of that inital click
    """
    
    file_tile_list = make_file_tile_list(8, 100, 100)
    
    # pivot/first tile clicked
    click_event = MagicMock(spec=QGraphicsSceneMouseEvent)
    click_event.modifiers.return_value = Qt.KeyboardModifier.NoModifier
    file_tile_list[0].mousePressEvent(click_event)
    
    # click on second tile using shift, first on the 4th, then 7th, then back to 4th
    # expected to expand selection then expand again then shrink
    click_event.modifiers.return_value = Qt.KeyboardModifier.ShiftModifier
    file_tile_list[3].mousePressEvent(click_event)
    
    assert file_tile_list[0].highlight_tile == True
    assert file_tile_list[1].highlight_tile == True
    assert file_tile_list[2].highlight_tile == True
    assert file_tile_list[3].highlight_tile == True
    assert file_tile_list[4].highlight_tile == False
    assert file_tile_list[5].highlight_tile == False
    assert file_tile_list[6].highlight_tile == False
    assert file_tile_list[7].highlight_tile == False
    
    click_event.modifiers.return_value = Qt.KeyboardModifier.ShiftModifier
    file_tile_list[6].mousePressEvent(click_event)
    
    assert file_tile_list[0].highlight_tile == True
    assert file_tile_list[1].highlight_tile == True
    assert file_tile_list[2].highlight_tile == True
    assert file_tile_list[3].highlight_tile == True
    assert file_tile_list[4].highlight_tile == True
    assert file_tile_list[5].highlight_tile == True
    assert file_tile_list[6].highlight_tile == True
    assert file_tile_list[7].highlight_tile == False
    
    click_event.modifiers.return_value = Qt.KeyboardModifier.ShiftModifier
    file_tile_list[3].mousePressEvent(click_event)
    
    assert file_tile_list[0].highlight_tile == True
    assert file_tile_list[1].highlight_tile == True
    assert file_tile_list[2].highlight_tile == True
    assert file_tile_list[3].highlight_tile == True
    assert file_tile_list[4].highlight_tile == False
    assert file_tile_list[5].highlight_tile == False
    assert file_tile_list[6].highlight_tile == False
    assert file_tile_list[7].highlight_tile == False
    
    ######################
    # now testing expanding selection of either side of the pivot
    # also tests reset clicking
    
    click_event.modifiers.return_value = Qt.KeyboardModifier.NoModifier
    file_tile_list[4].mousePressEvent(click_event)
    
    click_event.modifiers.return_value = Qt.KeyboardModifier.ShiftModifier
    file_tile_list[0].mousePressEvent(click_event)
    
    assert file_tile_list[0].highlight_tile == True
    assert file_tile_list[1].highlight_tile == True
    assert file_tile_list[2].highlight_tile == True
    assert file_tile_list[3].highlight_tile == True
    assert file_tile_list[4].highlight_tile == True
    assert file_tile_list[5].highlight_tile == False
    assert file_tile_list[6].highlight_tile == False
    assert file_tile_list[7].highlight_tile == False
    
    click_event.modifiers.return_value = Qt.KeyboardModifier.ShiftModifier
    file_tile_list[7].mousePressEvent(click_event)
    
    assert file_tile_list[0].highlight_tile == False
    assert file_tile_list[1].highlight_tile == False
    assert file_tile_list[2].highlight_tile == False
    assert file_tile_list[3].highlight_tile == False
    assert file_tile_list[4].highlight_tile == True
    assert file_tile_list[5].highlight_tile == True
    assert file_tile_list[6].highlight_tile == True
    assert file_tile_list[7].highlight_tile == True
    
    #### finally we hit above with a ctrl click and then shift
    
    click_event.modifiers.return_value = Qt.KeyboardModifier.ControlModifier
    file_tile_list[2].mousePressEvent(click_event)
    assert file_tile_list[0].highlight_tile == False
    assert file_tile_list[1].highlight_tile == False
    assert file_tile_list[2].highlight_tile == True
    assert file_tile_list[3].highlight_tile == False
    assert file_tile_list[4].highlight_tile == True
    assert file_tile_list[5].highlight_tile == True
    assert file_tile_list[6].highlight_tile == True
    assert file_tile_list[7].highlight_tile == True
    
    
    click_event.modifiers.return_value = Qt.KeyboardModifier.ShiftModifier
    file_tile_list[0].mousePressEvent(click_event)
    assert file_tile_list[0].highlight_tile == True
    assert file_tile_list[1].highlight_tile == True
    assert file_tile_list[2].highlight_tile == True
    assert file_tile_list[3].highlight_tile == False
    assert file_tile_list[4].highlight_tile == True
    assert file_tile_list[5].highlight_tile == True
    assert file_tile_list[6].highlight_tile == True
    assert file_tile_list[7].highlight_tile == True
    
    ###
    # check to see if control click and dehighlight
    
    click_event.modifiers.return_value = Qt.KeyboardModifier.ControlModifier
    file_tile_list[1].mousePressEvent(click_event)
    assert file_tile_list[0].highlight_tile == True
    assert file_tile_list[1].highlight_tile == False
    assert file_tile_list[2].highlight_tile == True
    assert file_tile_list[3].highlight_tile == False
    assert file_tile_list[4].highlight_tile == True
    assert file_tile_list[5].highlight_tile == True
    assert file_tile_list[6].highlight_tile == True
    assert file_tile_list[7].highlight_tile == True