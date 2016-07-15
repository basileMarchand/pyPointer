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
# file       : pointer.py                                                                                                  
# content    : Object definition and constructor function for pointers
# author     : Basile Marchand (basile.marchand@gmail.com)                                                                     
# date       : 15-07-2016                                                                                         
#----------------------------------      

import os
import psutil

__MEMORY_POINT = {}
__TIME_POINT   = {}

def create_or_connect(kind, name, pid=None):
    """
    Function which create a new Pointer (time or memory) or connect to an 
    existing one. 
    
    Parameters
    ------------
    kind : string {'memory', 'time'}
       the kind of Pointer we want declare
    name : string
       the name of the pointer, used to check if is already defined and then
       we connect to it or if it is necessary to declare a new Point object
    pid : int, optional
       the PID of the process to monitor, if None the current PID process is used. 

    Returns 
    -----------
    out : Point
       Point object (MemoryPoint or TimePoint)

    """

    if kind == "time":
        if name in __TIME_POINT.keys():
            print('TimePoint object named %s already exists you can connect to it'%(name))
        else:
            print("TimePoint object named %s doesn't exists, we create it"%(name))
            __TIME_POINT[name] = TimePoint(pid)
        return __TIME_POINT[name] 
    elif kind == "memory":
        if name in __MEMORY_POINT.keys():
            print('MemoryPoint object named %s already exists you can connect to it'%(name))
        else:
            print("MemoryPoint object named %s doesn't exists, we create it"%(name))
            __MEMORY_POINT[name] = MemoryPoint(pid)
        return __MEMORY_POINT[name] 
    else:
        print("Object %s not avalaible"%(kind))


class Point(object):
    def __init__(self, pid=None):
        if pid is None:
            pid = os.getpid()
        self.__process = psutil.Process(pid)
        self._header = {0:'Before ', 1:'After '}
        self._data = {}
        self._order = []
        self._tasks = []
        self._name = None

    def get_process(self):
        return self.__process

    PROC = property(get_process)

    def _get_val(self):
        return NotImplementedError

    def _store(self,label, io, *val):
        return NotImplementedError

    def start(self, label):
        val1, val2 = self._measure()
        self._store(label, 0, val1, val2)

    def stop(self, label):
        val1, val2 = self._measure()
        self._store(label, 1, val1, val2)

    def reboot(self, label):
        return NotImplementedError

    def resume(self, full=False):
        print(''.join(['-']*30) + self._name.center(20) + ''.join(['-']*30) )
        if full is False:
            self._final_display_by_tasks()
        else:
            self._final_display_full()

        print(''.join(['-']*80))

    def _final_display_full(self):
        for label in self._order:
            val = self._get_measures(label)
            msg = self._format(label, *val)
            print( msg )

    def _final_display_by_tasks(self):
        for task in self._tasks:
            val = self._get_tasks_val(task)
            msg = self._format2(task, *val)
            print( msg )

class MemoryPoint(Point):
    def __init__(self, pid=None):
        Point.__init__(self, pid)
        self._data = {}
        self._data['RSS'] = {}
        self._data['VIRTUAL'] = {}
        self._name = "Memory"
        
    def _measure(self):
        mem = self.PROC.memory_info()
        return mem.rss/1.e6, mem.vms/1.e6

    def _store(self,label, io, *val):
        if io==0 : self._tasks.append(label)
        label = self._header[io] + label
        self._order.append(label)
        self._data['RSS'][label] = val[0]
        self._data['VIRTUAL'][label] = val[1]
        
    def _format(self,label, *val):
        text = ("Memory Point %s (MB)"%(label) ).ljust(35)
        text += (":   %.2f (RSS)"%(val[0]) ).ljust(20) 
        text += "  -  " 
        text += ("%.2f (Virtual)"%(val[1]) ).ljust(20)
        return text

    def _format2(self, label, *val):
        text = ("Memory allocation for %s (MB)"%(label) ).ljust(35)
        text += (":   %.2f (RSS)"%(val[0]) ).ljust(20) 
        text += "  -  " 
        text += ("%.2f (Virtual)"%(val[1]) ).ljust(20)
        return text

    def _get_measures(self, label):
        return self._data['RSS'][label], self._data['VIRTUAL'][label]

    def _get_tasks_val(self, task_label):
        a = self._header[0] + task_label
        b = self._header[1] + task_label
        rss_diff = self._data['RSS'][b] - self._data['RSS'][a]
        virtual_diff = self._data['VIRTUAL'][b] - self._data['VIRTUAL'][a]
        return rss_diff, virtual_diff

class TimePoint(Point):
    def __init__(self, pid=None):
        Point.__init__(self, pid)
        self._data = {}
        self._data['WALL'] = {}
        self._data['CPU'] = {}
        self._name = "Time"

    def _measure(self):
        time = self.PROC.cpu_times()
        return time.user, time.system

    def _store(self,label, io, *val):
        if io==0 : self._tasks.append(label)
        label = self._header[io] + label
        self._order.append(label)
        self._data['WALL'][label] = val[0]
        self._data['CPU'][label] = val[1]

    def _format2(self, label, *val):
        text = ("Time for %s (s)"%(label) ).ljust(35)
        text += (":   %.2f (WALL)"%(val[0]) ).ljust(20) 
        text += "  -  " 
        text += ("%.2f (CPU)"%(val[1]) ).ljust(20)
        return text

    def _get_tasks_val(self, task_label):
        a = self._header[0] + task_label
        b = self._header[1] + task_label
        rss_diff = self._data['WALL'][b] - self._data['WALL'][a]
        virtual_diff = self._data['CPU'][b] - self._data['CPU'][a]
        return rss_diff, virtual_diff

