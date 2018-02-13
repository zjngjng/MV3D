""" Tracklet XML file generation
"""
from config import cfg

def writeln(f, string, tab_count, tab_as_space=False):
    tab_spaces = 4
    indent_str = " " * tab_spaces * tab_count if tab_as_space else "\t" * tab_count
    f.write(indent_str + string + "\n")
    pass


class Tracklet(object):

    def __init__(self, object_type, l, w, h, first_frame=0):
        self.object_type = object_type
        self.h = h
        self.w = w
        self.l = l
        self.first_frame = first_frame
        self.poses = []

    def write_xml(self, f, class_id, tab_level=0):
        writeln(f, '<item class_id="{:d}" tracking_level="0" version="1">'.format(class_id), tab_level)
        tab_level += 1
        class_id += 1
        writeln(f, '<objectType>{:s}</objectType>'.format(self.object_type), tab_level)
        writeln(f, '<h>{:.16f}</h>'.format(self.h), tab_level)
        writeln(f, '<w>{:.16f}</w>'.format(self.w), tab_level)
        writeln(f, '<l>{:.16f}</l>'.format(self.l), tab_level)
        writeln(f, '<first_frame>{:d}</first_frame>'.format(self.first_frame), tab_level)
        writeln(f, '<poses class_id="{:d}" tracking_level="0" version="0">'.format(class_id), tab_level)
        class_id += 1
        tab_level += 1
        writeln(f, '<count>{:d}</count>'.format(len(self.poses)), tab_level)
        writeln(f, '<item_version>2</item_version>', tab_level)
        first_pose = True
        for p in self.poses:
            if first_pose:
                writeln(f, '<item class_id="%d" tracking_level="0" version="2">' % class_id, tab_level)
                first_pose = False
            else:
                writeln(f, '<item>', tab_level)
            tab_level += 1
            class_id += 1
            writeln(f, '<tx>{:.16f}</tx>'.format(p['tx']), tab_level)
            writeln(f, '<ty>{:.16f}</ty>'.format(p['ty']), tab_level)
            writeln(f, '<tz>{:.16f}</tz>'.format(p['tz']), tab_level)
            writeln(f, '<rx>{:.16f}</rx>'.format(p['rx']), tab_level)
            writeln(f, '<ry>{:.16f}</ry>'.format(p['ry']), tab_level)
            writeln(f, '<rz>{:.16f}</rz>'.format(p['rz']), tab_level)
            if cfg.TRACKLET_EXTRA_INFO:
                writeln(f, '<score>{:.16f}</score>'.format(p['score']), tab_level)
                writeln(f, '<bbox>{}</bbox>'.format(p['bbox']), tab_level)
            writeln(f, '<state>1</state>', tab_level)  # INTERP = 1
            writeln(f, '<occlusion>-1</occlusion>', tab_level) # UNSET = -1
            writeln(f, '<occlusion_kf>-1</occlusion_kf>', tab_level)
            writeln(f, '<truncation>-1</truncation>', tab_level) # UNSET = -1
            writeln(f, '<amt_occlusion>0.0</amt_occlusion>', tab_level)
            writeln(f, '<amt_occlusion_kf>-1</amt_occlusion_kf>', tab_level)
            writeln(f, '<amt_border_l>0.0</amt_border_l>', tab_level)
            writeln(f, '<amt_border_r>0.0</amt_border_r>', tab_level)
            writeln(f, '<amt_border_kf>-1</amt_border_kf>', tab_level)
            tab_level -= 1
            writeln(f, '</item>', tab_level)
        tab_level -= 1
        writeln(f, '</poses>', tab_level)
        writeln(f, '<finished>1</finished>', tab_level)
        tab_level -= 1
        writeln(f, '</item>', tab_level)


class TrackletCollection(object):

    def __init__(self):
        self.tracklets = []

    def write_xml(self, filename):
        tab_level = 0
        with open(filename, mode='w') as f:
            writeln(f, r'<?xml version="1.0" encoding="UTF-8" standalone="yes" ?>', tab_level)
            writeln(f, r'<!DOCTYPE boost_serialization>', tab_level)
            writeln(f, r'<boost_serialization signature="serialization::archive" version="9">', tab_level)
            writeln(f, r'<tracklets class_id="0" tracking_level="0" version="0">', tab_level)
            tab_level += 1
            writeln(f, '<count>%d</count>' % len(self.tracklets), tab_level)
            writeln(f, '<item_version>1</item_version> ', tab_level)
            class_id = 1
            for obj in self.tracklets:
                # Seems the class_id is only used in first item.
                # class_id = obj.write_xml(f, class_id, tab_level)
                obj.write_xml(f, class_id, tab_level)
            tab_level -= 1
            writeln(f, '</tracklets>', tab_level)
            writeln(f, '</boost_serialization> ', tab_level)
            f.close()
