# This Python file uses the following encoding: utf-8
"""autogenerated by genpy from msg_types/PositionArray.msg. Do not edit."""
import codecs
import sys
python3 = True if sys.hexversion > 0x03000000 else False
import genpy
import struct

import genpy
import msg_types.msg

class PositionArray(genpy.Message):
  _md5sum = "55fbca85e311ffe813e31fb2e1229ad7"
  _type = "msg_types/PositionArray"
  _has_header = False  # flag to mark the presence of a Header object
  _full_text = """time stamp
msg_types/Position[] objects


================================================================================
MSG: msg_types/Position
time stamp
float32 x
float32 y
float32 t
uint32 id
bool actual
"""
  __slots__ = ['stamp','objects']
  _slot_types = ['time','msg_types/Position[]']

  def __init__(self, *args, **kwds):
    """
    Constructor. Any message fields that are implicitly/explicitly
    set to None will be assigned a default value. The recommend
    use is keyword arguments as this is more robust to future message
    changes.  You cannot mix in-order arguments and keyword arguments.

    The available fields are:
       stamp,objects

    :param args: complete set of field values, in .msg order
    :param kwds: use keyword arguments corresponding to message field names
    to set specific fields.
    """
    if args or kwds:
      super(PositionArray, self).__init__(*args, **kwds)
      # message fields cannot be None, assign default values for those that are
      if self.stamp is None:
        self.stamp = genpy.Time()
      if self.objects is None:
        self.objects = []
    else:
      self.stamp = genpy.Time()
      self.objects = []

  def _get_types(self):
    """
    internal API method
    """
    return self._slot_types

  def serialize(self, buff):
    """
    serialize message into buffer
    :param buff: buffer, ``StringIO``
    """
    try:
      _x = self
      buff.write(_get_struct_2I().pack(_x.stamp.secs, _x.stamp.nsecs))
      length = len(self.objects)
      buff.write(_struct_I.pack(length))
      for val1 in self.objects:
        _v1 = val1.stamp
        _x = _v1
        buff.write(_get_struct_2I().pack(_x.secs, _x.nsecs))
        _x = val1
        buff.write(_get_struct_3fIB().pack(_x.x, _x.y, _x.t, _x.id, _x.actual))
    except struct.error as se: self._check_types(struct.error("%s: '%s' when writing '%s'" % (type(se), str(se), str(locals().get('_x', self)))))
    except TypeError as te: self._check_types(ValueError("%s: '%s' when writing '%s'" % (type(te), str(te), str(locals().get('_x', self)))))

  def deserialize(self, str):
    """
    unpack serialized message in str into this message instance
    :param str: byte array of serialized message, ``str``
    """
    codecs.lookup_error("rosmsg").msg_type = self._type
    try:
      if self.stamp is None:
        self.stamp = genpy.Time()
      if self.objects is None:
        self.objects = None
      end = 0
      _x = self
      start = end
      end += 8
      (_x.stamp.secs, _x.stamp.nsecs,) = _get_struct_2I().unpack(str[start:end])
      start = end
      end += 4
      (length,) = _struct_I.unpack(str[start:end])
      self.objects = []
      for i in range(0, length):
        val1 = msg_types.msg.Position()
        _v2 = val1.stamp
        _x = _v2
        start = end
        end += 8
        (_x.secs, _x.nsecs,) = _get_struct_2I().unpack(str[start:end])
        _x = val1
        start = end
        end += 17
        (_x.x, _x.y, _x.t, _x.id, _x.actual,) = _get_struct_3fIB().unpack(str[start:end])
        val1.actual = bool(val1.actual)
        self.objects.append(val1)
      self.stamp.canon()
      return self
    except struct.error as e:
      raise genpy.DeserializationError(e)  # most likely buffer underfill


  def serialize_numpy(self, buff, numpy):
    """
    serialize message with numpy array types into buffer
    :param buff: buffer, ``StringIO``
    :param numpy: numpy python module
    """
    try:
      _x = self
      buff.write(_get_struct_2I().pack(_x.stamp.secs, _x.stamp.nsecs))
      length = len(self.objects)
      buff.write(_struct_I.pack(length))
      for val1 in self.objects:
        _v3 = val1.stamp
        _x = _v3
        buff.write(_get_struct_2I().pack(_x.secs, _x.nsecs))
        _x = val1
        buff.write(_get_struct_3fIB().pack(_x.x, _x.y, _x.t, _x.id, _x.actual))
    except struct.error as se: self._check_types(struct.error("%s: '%s' when writing '%s'" % (type(se), str(se), str(locals().get('_x', self)))))
    except TypeError as te: self._check_types(ValueError("%s: '%s' when writing '%s'" % (type(te), str(te), str(locals().get('_x', self)))))

  def deserialize_numpy(self, str, numpy):
    """
    unpack serialized message in str into this message instance using numpy for array types
    :param str: byte array of serialized message, ``str``
    :param numpy: numpy python module
    """
    codecs.lookup_error("rosmsg").msg_type = self._type
    try:
      if self.stamp is None:
        self.stamp = genpy.Time()
      if self.objects is None:
        self.objects = None
      end = 0
      _x = self
      start = end
      end += 8
      (_x.stamp.secs, _x.stamp.nsecs,) = _get_struct_2I().unpack(str[start:end])
      start = end
      end += 4
      (length,) = _struct_I.unpack(str[start:end])
      self.objects = []
      for i in range(0, length):
        val1 = msg_types.msg.Position()
        _v4 = val1.stamp
        _x = _v4
        start = end
        end += 8
        (_x.secs, _x.nsecs,) = _get_struct_2I().unpack(str[start:end])
        _x = val1
        start = end
        end += 17
        (_x.x, _x.y, _x.t, _x.id, _x.actual,) = _get_struct_3fIB().unpack(str[start:end])
        val1.actual = bool(val1.actual)
        self.objects.append(val1)
      self.stamp.canon()
      return self
    except struct.error as e:
      raise genpy.DeserializationError(e)  # most likely buffer underfill

_struct_I = genpy.struct_I
def _get_struct_I():
    global _struct_I
    return _struct_I
_struct_2I = None
def _get_struct_2I():
    global _struct_2I
    if _struct_2I is None:
        _struct_2I = struct.Struct("<2I")
    return _struct_2I
_struct_3fIB = None
def _get_struct_3fIB():
    global _struct_3fIB
    if _struct_3fIB is None:
        _struct_3fIB = struct.Struct("<3fIB")
    return _struct_3fIB
