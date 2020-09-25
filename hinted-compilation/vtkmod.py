#     Copyright 2019, Jorj McKie, mailto:<jorj.x.mckie@outlook.de>
#
#     Part of "Nuitka", an optimizing Python compiler that is compatible and
#     integrates with CPython, but also works on its own.
#
#     Licensed under the Apache License, Version 2.0 (the "License");
#     you may not use this file except in compliance with the License.
#     You may obtain a copy of the License at
#
#        http://www.apache.org/licenses/LICENSE-2.0
#
#     Unless required by applicable law or agreed to in writing, software
#     distributed under the License is distributed on an "AS IS" BASIS,
#     WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#     See the License for the specific language governing permissions and
#     limitations under the License.
#
""" Details see below in class definition.
"""
from logging import info
from nuitka.plugins.PluginBase import NuitkaPluginBase


class VTKPlugin(NuitkaPluginBase):

    plugin_name = __file__
    plugin_desc = "Required by the vtk package version 8.2.0+"

    def onModuleSourceCode(self, module_name, source_code):
        """ Insert an import statement to vtkmodules.__init__.py

        """
        lines = source_code.splitlines()
        if module_name == "vtkmodules":
            # appends a statement to vtkmodules.__init__.py
            text = "from vtkmodules.all import *"
            lines.append(text)
            info(self.plugin_name + " inserted '%s'" % text)
            return "\n".join(lines)

        new_source = (  # this replaces vtk.py completely
            "import sys",
            "import vtkmodules",
            "from vtkmodules import all as vtk",
            "vtk.__path__ = vtkmodules.__path__",
            "sys.modules[__name__] = vtk",
        )

        if module_name == "vtk":
            info(self.plugin_name + " replaced vtk.py")
            return "\n".join(new_source)

        if module_name.startswith("vtkmodules"):
            # we do not touch any of these files
            return source_code

        # now take care of any reference to subfolders of vtkmodules
        modified = False
        for i, line in enumerate(lines):
            if "vtk." in line:
                lines[i] = lines[i].replace("vtk.gtk", "vtkmodules.gtk")
                lines[i] = lines[i].replace(
                    "vtk.numpy_interface", "vtkmodules.numpy_interface"
                )
                lines[i] = lines[i].replace("vtk.qt", "vtkmodules.qt")
                lines[i] = lines[i].replace("vtk.qt4", "vtkmodules.qt4")
                lines[i] = lines[i].replace("vtk.tk", "vtkmodules.tk")
                lines[i] = lines[i].replace("vtk.util", "vtkmodules.util")
                lines[i] = lines[i].replace("vtk.wx", "vtkmodules.wx")
                modified = True

        if modified == True:
            info("Modified " + module_name)
            return "\n".join(lines)

        return source_code
