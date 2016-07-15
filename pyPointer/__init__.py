#==============================================================================
# Copyright (C) 2016 Marchand Basile                                  
#                                                                     
# This file is part of pyPointer  
#                                                                     
# pyPointer is free software: you can redistribute it and/or modify   
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or   
# any later version.                           
#                                                               
# pyPointer is distributed in the hope that it will be useful,   
# but WITHOUT ANY WARRANTY; without even the implied warranty of 
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the  
# GNU General Public License for more details.
#                                
# You should have received a copy of the GNU General Public License 
# along with pyPointer.  If not, see <http://www.gnu.org/licenses/>   
#==============================================================================          
#----------------------------------      
# package    : pyPointer     
# file       : __init__.py                                                                                                  
# content    :                                                                         
# author     : Basile Marchand (basile.marchand@gmail.com)                                                                     
# date       : 15-07-2016                                                                                         
#----------------------------------      

__all__ = ['create_or_connect']

from .pointer import create_or_connect, Point, MemoryPoint, TimePoint



