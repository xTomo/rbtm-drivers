#!/usr/bin/env python
# -*- coding:utf-8 -*- 


##############################################################################
## license :
##============================================================================
##
## File :        AngleMotor.py
## 
## Project :     
##
## This file is part of Tango device class.
## 
## Tango is free software: you can redistribute it and/or modify
## it under the terms of the GNU General Public License as published by
## the Free Software Foundation, either version 3 of the License, or
## (at your option) any later version.
## 
## Tango is distributed in the hope that it will be useful,
## but WITHOUT ANY WARRANTY; without even the implied warranty of
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
## GNU General Public License for more details.
## 
## You should have received a copy of the GNU General Public License
## along with Tango.  If not, see <http://www.gnu.org/licenses/>.
## 
##
## $Author :      diana.ichalova$
##
## $Revision :    $
##
## $Date :        $
##
## $HeadUrl :     $
##============================================================================
##            This file is generated by POGO
##    (Program Obviously used to Generate tango Object)
##
##        (c) - Software Engineering Group - ESRF
##############################################################################

""""""

__all__ = ["AngleMotor", "AngleMotorClass", "main"]

__docformat__ = 'restructuredtext'

import PyTango
import sys
# Add additional import
#----- PROTECTED REGION ID(AngleMotor.additionnal_import) ENABLED START -----#
import sys
sys.path.insert(0, 'lib')
import ximc
import time
import ConfigParser
from contextlib import closing
#----- PROTECTED REGION END -----#	//	AngleMotor.additionnal_import

## Device States Description
## STANDBY : 
## MOVING : 

class AngleMotor (PyTango.Device_4Impl):

    #--------- Add you global variables here --------------------------
    #----- PROTECTED REGION ID(AngleMotor.global_variables) ENABLED START -----#

    CONFIG_PATH = 'tango_ds.cfg'
    STEPS_IN_360 = 32400 # steps in 360 degrees
    STEPS_IN_DEGREE = STEPS_IN_360 / 360.

    def get_port_from_config(self):
        config = ConfigParser.RawConfigParser()
        config.read(AngleMotor.CONFIG_PATH)
        motor_port = config.get("angle motor", "port")
        return motor_port

    def _read_position(self, motor):
        self.debug_stream("In _read_position()")

        self.debug_stream("Reading position...")
        try:
            steps = motor.get_position()
        except PyTango.DevFailed as df:
            self.error_stream(str(df))
            self.init_device()
            raise
        except Exception as e:
            self.error_stream(str(e))
            raise
        self.info_stream("Position = {}".format(steps))
        return steps

    def _write_position(self, motor, steps):
        self.debug_stream("In _write_position()")

        self.info_stream("Setting position = {}".format(steps))
        try:
            motor.move_to_position(steps)
            motor.wait_for_stop()
            self.debug_stream("Position has been set")
        except PyTango.DevFailed as df:
            self.error_stream(str(df))
            self.init_device()
            raise
        except Exception as e:
            self.error_stream(str(e))
            raise

    #----- PROTECTED REGION END -----#	//	AngleMotor.global_variables

    def __init__(self,cl, name):
        PyTango.Device_4Impl.__init__(self,cl,name)
        self.debug_stream("In __init__()")
        AngleMotor.init_device(self)
        #----- PROTECTED REGION ID(AngleMotor.__init__) ENABLED START -----#
        
        #----- PROTECTED REGION END -----#	//	AngleMotor.__init__
        
    def delete_device(self):
        self.debug_stream("In delete_device()")
        #----- PROTECTED REGION ID(AngleMotor.delete_device) ENABLED START -----#
        
        #----- PROTECTED REGION END -----#	//	AngleMotor.delete_device

    def init_device(self):
        self.debug_stream("In init_device()")
        self.get_device_properties(self.get_device_class())
        self.attr_position_read = 0.0
        self.attr_speed_read = 0.0
        self.attr_accel_read = 0.0
        #----- PROTECTED REGION ID(AngleMotor.init_device) ENABLED START -----#

        motor_port = self.get_port_from_config()

        try:
            self.debug_stream("Creating link to motor drivers...")
            self.angle_motor = ximc.Motor(motor_port, 0)
            self.debug_stream("Links were created")
        except PyTango.DevFailed as df:
            self.error_stream(str(df))
            raise
        except Exception as e:
            self.error_stream(str(e))
            raise

        with closing(self.angle_motor.open()):
            self.angle_motor.set_move_settings(500, 500)
            steps = self._read_position(self.angle_motor)
        self.attr_position_read = steps

        self.set_state(PyTango.DevState.STANDBY)

        #----- PROTECTED REGION END -----#	//	AngleMotor.init_device

    def always_executed_hook(self):
        self.debug_stream("In always_excuted_hook()")
        #----- PROTECTED REGION ID(AngleMotor.always_executed_hook) ENABLED START -----#
        
        #----- PROTECTED REGION END -----#	//	AngleMotor.always_executed_hook

    #-----------------------------------------------------------------------------
    #    AngleMotor read/write attribute methods
    #-----------------------------------------------------------------------------
    
    def read_position(self, attr):
        self.debug_stream("In read_position()")
        #----- PROTECTED REGION ID(AngleMotor.position_read) ENABLED START -----#
        with closing(self.angle_motor.open()):
            self.attr_position_read = self._read_position(self.angle_motor) / AngleMotor.STEPS_IN_DEGREE
        attr.set_value(self.attr_position_read)
        #----- PROTECTED REGION END -----#	//	AngleMotor.position_read
        
    def write_position(self, attr):
        self.debug_stream("In write_position()")
        data=attr.get_write_value()
        #----- PROTECTED REGION ID(AngleMotor.position_write) ENABLED START -----#
        prev_state = self.get_state()
        self.set_state(PyTango.DevState.MOVING)
        angle = data
        steps = int(round(angle * AngleMotor.STEPS_IN_DEGREE)) % AngleMotor.STEPS_IN_360
        with closing(self.angle_motor.open()):
            self._write_position(self.angle_motor, steps)
        #self.angle_motor.close()

        self.set_state(prev_state)
        #----- PROTECTED REGION END -----#	//	AngleMotor.position_write
        
    def read_speed(self, attr):
        self.debug_stream("In read_speed()")
        #----- PROTECTED REGION ID(AngleMotor.speed_read) ENABLED START -----#
        with closing(self.angle_motor.open()):
            speed_steps = self.angle_motor.get_move_settings()["Speed"]
        speed_degrees = speed_steps / AngleMotor.STEPS_IN_DEGREE
        self.attr_speed_read = speed_degrees
        attr.set_value(self.attr_speed_read)
        #----- PROTECTED REGION END -----#	//	AngleMotor.speed_read
        
    def write_speed(self, attr):
        self.debug_stream("In write_speed()")
        data=attr.get_write_value()
        #----- PROTECTED REGION ID(AngleMotor.speed_write) ENABLED START -----#
        speed = int(round(data * AngleMotor.STEPS_IN_DEGREE))
        with closing(self.angle_motor.open()):
            self.angle_motor.set_move_settings(speed=speed)
        #----- PROTECTED REGION END -----#	//	AngleMotor.speed_write
        
    def read_accel(self, attr):
        self.debug_stream("In read_accel()")
        #----- PROTECTED REGION ID(AngleMotor.accel_read) ENABLED START -----#
        with closing(self.angle_motor.open()):
            accel_steps = self.angle_motor.get_move_settings()["Accel"]
        accel_degrees = accel_steps / AngleMotor.STEPS_IN_DEGREE
        self.attr_accel_read = accel_degrees
        attr.set_value(self.attr_accel_read)
        #----- PROTECTED REGION END -----#	//	AngleMotor.accel_read
        
    def write_accel(self, attr):
        self.debug_stream("In write_accel()")
        data=attr.get_write_value()
        #----- PROTECTED REGION ID(AngleMotor.accel_write) ENABLED START -----#
        accel = int(round(data * AngleMotor.STEPS_IN_DEGREE))
        with closing(self.angle_motor.open()):
            self.angle_motor.set_move_settings(accel=accel)
        #----- PROTECTED REGION END -----#	//	AngleMotor.accel_write
        
    
    
        #----- PROTECTED REGION ID(AngleMotor.initialize_dynamic_attributes) ENABLED START -----#
        
        #----- PROTECTED REGION END -----#	//	AngleMotor.initialize_dynamic_attributes
            
    def read_attr_hardware(self, data):
        self.debug_stream("In read_attr_hardware()")
        #----- PROTECTED REGION ID(AngleMotor.read_attr_hardware) ENABLED START -----#
        
        #----- PROTECTED REGION END -----#	//	AngleMotor.read_attr_hardware


    #-----------------------------------------------------------------------------
    #    AngleMotor command methods
    #-----------------------------------------------------------------------------
    
    def SetZero(self):
        """ 
        
        :param : 
        :type: PyTango.DevVoid
        :return: 
        :rtype: PyTango.DevVoid """
        self.debug_stream("In SetZero()")
        #----- PROTECTED REGION ID(AngleMotor.SetZero) ENABLED START -----#
        self.info_stream("Setting current angle position as new zero")
        with closing(self.angle_motor.open()):
            try:
                self.angle_motor.set_zero()
            except PyTango.DevFailed as df:
                self.error_stream(str(df))
                self.init_device()
                raise
            except Exception as e:
                self.error_stream(str(e))
                raise
            
        self.debug_stream("New zero has been set")
        #----- PROTECTED REGION END -----#	//	AngleMotor.SetZero
        

class AngleMotorClass(PyTango.DeviceClass):
    #--------- Add you global class variables here --------------------------
    #----- PROTECTED REGION ID(AngleMotor.global_class_variables) ENABLED START -----#
    
    #----- PROTECTED REGION END -----#	//	AngleMotor.global_class_variables

    def dyn_attr(self, dev_list):
        """Invoked to create dynamic attributes for the given devices.
        Default implementation calls
        :meth:`AngleMotor.initialize_dynamic_attributes` for each device
    
        :param dev_list: list of devices
        :type dev_list: :class:`PyTango.DeviceImpl`"""
    
        for dev in dev_list:
            try:
                dev.initialize_dynamic_attributes()
            except:
                import traceback
                dev.warn_stream("Failed to initialize dynamic attributes")
                dev.debug_stream("Details: " + traceback.format_exc())
        #----- PROTECTED REGION ID(AngleMotor.dyn_attr) ENABLED START -----#
        
        #----- PROTECTED REGION END -----#	//	AngleMotor.dyn_attr

    #    Class Properties
    class_property_list = {
        }


    #    Device Properties
    device_property_list = {
        }


    #    Command definitions
    cmd_list = {
        'SetZero':
            [[PyTango.DevVoid, "none"],
            [PyTango.DevVoid, "none"]],
        }


    #    Attribute definitions
    attr_list = {
        'position':
            [[PyTango.DevDouble,
            PyTango.SCALAR,
            PyTango.READ_WRITE]],
        'speed':
            [[PyTango.DevDouble,
            PyTango.SCALAR,
            PyTango.READ_WRITE],
            {
                'label': "speed",
                'unit': "degrees/s",
                'max value': "1100",
                'min value': "0",
            } ],
        'accel':
            [[PyTango.DevDouble,
            PyTango.SCALAR,
            PyTango.READ_WRITE],
            {
                'label': "acceleration",
                'unit': "degrees/s^2",
                'max value': "730",
                'min value': "0.012",
            } ],
        }


def main():
    try:
        py = PyTango.Util(sys.argv)
        py.add_class(AngleMotorClass,AngleMotor,'AngleMotor')

        U = PyTango.Util.instance()
        U.server_init()
        U.server_run()

    except PyTango.DevFailed,e:
        print '-------> Received a DevFailed exception:',e
    except Exception,e:
        print '-------> An unforeseen exception occured....',e

if __name__ == '__main__':
    main()
