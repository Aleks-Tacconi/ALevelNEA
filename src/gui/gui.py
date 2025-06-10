# -*- coding: utf-8 -*-
"""
gui module

This module handles all the configuration for the GUI so that
the GUI is already configured upon instantiation

Classes:
- GUI
"""

import customtkinter as ctk


class GUI(ctk.CTk):
    """A preconfigured GUI class

    This is a GUI class which inherits from the CTK class from the
    customtkinter module and configures it
    """

    def __init__(self, *args, title: str = "CTKApplication", **kwargs) -> None:
        """Constructor for the GUI class

        Configures the GUI to look good and resizes the GUI
        from the default size

        Args:
            title (str): Tte title of the tkinter application
            *args: extra configuration for supported by CTK
            **kwargs: extra configuration supported by CTK

        Returns:
            None
        """

        super().__init__(*args, **kwargs)

        self.geometry("700x700")
        self.title(title)

        self.canvas = ctk.CTkCanvas(self, bg="#1E1E1E", highlightthickness=0)
        self.canvas.pack(fill=ctk.BOTH, expand=ctk.YES)
