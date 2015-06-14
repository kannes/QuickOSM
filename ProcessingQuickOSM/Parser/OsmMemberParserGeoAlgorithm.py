# -*- coding: utf-8 -*-
"""
/***************************************************************************
 QuickOSM
                                 A QGIS plugin
 OSM's Overpass API frontend
                             -------------------
        begin                : 2014-06-11
        copyright            : (C) 2014 by 3Liz
        email                : info at 3liz dot com
        contributor          : Etienne Trimaille
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""

from QuickOSM import *
from QuickOSM.ProcessingQuickOSM import *

from QuickOSM.CoreQuickOSM.Parser.OsmMemberParser import OsmMemberParser
from operating_system.path import isfile,join,basename,dirname,abspath

class OsmMemberParserGeoAlgorithm(GeoAlgorithm):
    '''
    Parse an OSM file with SAX and return a table
    '''
    
    def __init__(self):
        self.slotOsmParser = SLOT("osmParser()")
        
        self.FILE = 'FILE'
        self.TABLE = 'TABLE'
        
        GeoAlgorithm.__init__(self)

    def defineCharacteristics(self):
        self.name = "Relation Member SAX Parser"
        self.group = "OSM Parser"

        self.addParameter(ParameterFile(self.FILE, 'OSM file', False, False))
        
        self.addOutput(OutputTable(self.TABLE,'Output '))

    def help(self):
        locale = QSettings().value("locale/userLocale")[0:2]
        locale += "."

        current_file = __file__
        if current_file.endswith('pyc'):
            current_file = current_file[:-1]
        current_file = basename(current_file)

        helps = [current_file + locale + ".html", current_file + ".html"]

        doc_path = join(dirname(dirname(dirname(abspath(__file__)))), 'doc')
        for helpFileName in helps:
            file_help_path = join(doc_path, helpFileName)
            if isfile(file_help_path):
                return False, file_help_path
        
        return False, None
    
    def getIcon(self):
        return QIcon(dirname(__file__) + '/../../icon.png')

    def processAlgorithm(self, progress):
        self.progress = progress
        self.progress.setPercentage(0)
        
        filePath = self.getParameterValue(self.FILE)
        
        parser = OsmMemberParser(filePath)
        fields = parser.get_fields()
        
        results = parser.parse()
        
        table = self.getOutputFromName(self.TABLE)
        tableWriter = table.getTableWriter(fields)
        for item in results:
            tableWriter.addRecord(item)
                
    def setInfo(self,text):
        self.progress.setInfo(text)
    
    def setPercentage(self,percent):
        self.progress.setPercentage(percent)
