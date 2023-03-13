from PyQt6.QtWidgets import (QLabel, QLineEdit, QPushButton,
                             QDialog,
                             QHBoxLayout, QGridLayout)
from PyQt6.QtCore import Qt
import pretty_midi


class ParamDialog(QDialog):

    def __init__(self, parent):
        super().__init__()
        self.params = parent.params
        self.parent = parent
        layout = QGridLayout()
        layout.setSpacing(10)

        cancel_button = QPushButton(text="Cancel")
        cancel_button.setMaximumWidth(70)
        cancel_button.adjustSize()
        cancel_button.clicked.connect(self.reject)
        ok_button = QPushButton(text="Ok")
        ok_button.setMaximumWidth(70)
        ok_button.adjustSize()
        ok_button.clicked.connect(self.accept)
        footer_box = QHBoxLayout()
        footer_box.addSpacing(10)
        footer_box.addWidget(cancel_button)
        footer_box.addWidget(ok_button)
        footer_box.setAlignment(Qt.AlignmentFlag.AlignRight)

        self.note_name_input = QLineEdit(str(self.params["note_name"]))
        self.note_name_input.setMaximumWidth(60)
        # self.note_name_input.textChanged.connect(self.note_name_changed)
        self.note_name_input.setAlignment(Qt.AlignmentFlag.AlignRight)
        note_name_label = QLabel("Note name")
        self.duration_for_analysis_input = QLineEdit(str(self.params["duration_for_analysis"]))
        self.duration_for_analysis_input.setMaximumWidth(60)
        self.duration_for_analysis_input.setAlignment(Qt.AlignmentFlag.AlignRight)
        duration_for_analysis_label = QLabel("Duration of analysis")
        self.filter_timescale_input = QLineEdit(str(self.params["filter_timescale"])) # number input
        self.filter_timescale_input.setMaximumWidth(60)
        self.filter_timescale_input.setAlignment(Qt.AlignmentFlag.AlignRight)
        filter_timescale_label = QLabel("Filter timescale")
        self.threshold_input = QLineEdit(str(self.params["threshold"])) # number input
        self.threshold_input.setMaximumWidth(60)
        self.threshold_input.setAlignment(Qt.AlignmentFlag.AlignRight)
        threshold_label = QLabel("Threshold")
        self.min_note_duration_input = QLineEdit(str(self.params["min_note_duration"])) # number input
        self.min_note_duration_input.setMaximumWidth(60)
        self.min_note_duration_input.setAlignment(Qt.AlignmentFlag.AlignRight)
        min_note_duration_label = QLabel("Minimum note duration")
        
        # cols 0 & 1
        layout.addWidget(self.note_name_input, 0, 0)
        layout.addWidget(note_name_label, 0, 1)
        layout.addWidget(self.duration_for_analysis_input, 1, 0)
        layout.addWidget(duration_for_analysis_label, 1, 1)
        layout.addWidget(self.filter_timescale_input, 2, 0)
        layout.addWidget(filter_timescale_label, 2, 1)
        layout.setColumnMinimumWidth(2, 25)
        # cols 3 & 4
        layout.addWidget(self.threshold_input, 0, 3)
        layout.addWidget(threshold_label, 0, 4)
        layout.addWidget(self.min_note_duration_input, 1, 3)
        layout.addWidget(min_note_duration_label, 1, 4)
        layout.setRowMinimumHeight(3, 25)
        layout.addLayout(footer_box, 4, 0, 1, 5)
        
        self.accepted.connect(self.param_changed)
        self.setWindowTitle("Change params")
        self.setLayout(layout)
    

    def param_changed(self):
        # TODO : verify that new values are correct
        # TODO : add midi_note param from note_name
        print("params changed called")
        self.params["note_name"] = self.note_name_input.text()
        if self.params["note_name"] in self.params["note_list"]:
            self.params["midi_note"] = pretty_midi.note_name_to_number(self.params["note_name"])
        self.params["duration_for_analysis"] = int(self.duration_for_analysis_input.text())
        self.params["filter_timescale"] = int(self.filter_timescale_input.text())
        self.params["threshold"] = float(self.threshold_input.text())
        self.params["min_note_duration"] = float(self.min_note_duration_input.text())
        # call a parent method to change its params values
        self.parent.store_new_params(self.params)

    
    def verify_note_proposition(self, note_name: str):
        """Verify a note name proposal (by the user)

        Args:
            note_list (list[str]): List of possible notes as strings
            note_name (str): name of note

        Returns:
            A tuple containing :
                str : the note name
                int or None : the note number in pretty_midi format or None if note_name was not in note_list
        """
        midi_note = None
        if note_name in self.params["note_list"]:
            midi_note = pretty_midi.note_name_to_number(note_name)
        return note_name, midi_note
    
    # def note_name_changed(self):
    # verify values
    #     value = self.note_name_input.text()
    #     self.params["note_name"]
