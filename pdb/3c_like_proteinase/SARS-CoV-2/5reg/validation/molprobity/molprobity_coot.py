# script auto-generated by phenix.molprobity


from __future__ import absolute_import, division, print_function
from six.moves import cPickle as pickle
from six.moves import range
try :
  import gobject
except ImportError :
  gobject = None
import sys

class coot_extension_gui(object):
  def __init__(self, title):
    import gtk
    self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
    scrolled_win = gtk.ScrolledWindow()
    self.outside_vbox = gtk.VBox(False, 2)
    self.inside_vbox = gtk.VBox(False, 0)
    self.window.set_title(title)
    self.inside_vbox.set_border_width(0)
    self.window.add(self.outside_vbox)
    self.outside_vbox.pack_start(scrolled_win, True, True, 0)
    scrolled_win.add_with_viewport(self.inside_vbox)
    scrolled_win.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)

  def finish_window(self):
    import gtk
    self.outside_vbox.set_border_width(2)
    ok_button = gtk.Button("  Close  ")
    self.outside_vbox.pack_end(ok_button, False, False, 0)
    ok_button.connect("clicked", lambda b: self.destroy_window())
    self.window.connect("delete_event", lambda a, b: self.destroy_window())
    self.window.show_all()

  def destroy_window(self, *args):
    self.window.destroy()
    self.window = None

  def confirm_data(self, data):
    for data_key in self.data_keys :
      outlier_list = data.get(data_key)
      if outlier_list is not None and len(outlier_list) > 0 :
        return True
    return False

  def create_property_lists(self, data):
    import gtk
    for data_key in self.data_keys :
      outlier_list = data[data_key]
      if outlier_list is None or len(outlier_list) == 0 :
        continue
      else :
        frame = gtk.Frame(self.data_titles[data_key])
        vbox = gtk.VBox(False, 2)
        frame.set_border_width(6)
        frame.add(vbox)
        self.add_top_widgets(data_key, vbox)
        self.inside_vbox.pack_start(frame, False, False, 5)
        list_obj = residue_properties_list(
          columns=self.data_names[data_key],
          column_types=self.data_types[data_key],
          rows=outlier_list,
          box=vbox)

# Molprobity result viewer
class coot_molprobity_todo_list_gui(coot_extension_gui):
  data_keys = [ "rama", "rota", "cbeta", "probe" ]
  data_titles = { "rama"  : "Ramachandran outliers",
                  "rota"  : "Rotamer outliers",
                  "cbeta" : "C-beta outliers",
                  "probe" : "Severe clashes" }
  data_names = { "rama"  : ["Chain", "Residue", "Name", "Score"],
                 "rota"  : ["Chain", "Residue", "Name", "Score"],
                 "cbeta" : ["Chain", "Residue", "Name", "Conf.", "Deviation"],
                 "probe" : ["Atom 1", "Atom 2", "Overlap"] }
  if (gobject is not None):
    data_types = { "rama" : [gobject.TYPE_STRING, gobject.TYPE_STRING,
                             gobject.TYPE_STRING, gobject.TYPE_FLOAT,
                             gobject.TYPE_PYOBJECT],
                   "rota" : [gobject.TYPE_STRING, gobject.TYPE_STRING,
                             gobject.TYPE_STRING, gobject.TYPE_FLOAT,
                             gobject.TYPE_PYOBJECT],
                   "cbeta" : [gobject.TYPE_STRING, gobject.TYPE_STRING,
                              gobject.TYPE_STRING, gobject.TYPE_STRING,
                              gobject.TYPE_FLOAT, gobject.TYPE_PYOBJECT],
                   "probe" : [gobject.TYPE_STRING, gobject.TYPE_STRING,
                              gobject.TYPE_FLOAT, gobject.TYPE_PYOBJECT] }
  else :
    data_types = dict([ (s, []) for s in ["rama","rota","cbeta","probe"] ])

  def __init__(self, data_file=None, data=None):
    assert ([data, data_file].count(None) == 1)
    if (data is None):
      data = load_pkl(data_file)
    if not self.confirm_data(data):
      return
    coot_extension_gui.__init__(self, "MolProbity to-do list")
    self.dots_btn = None
    self.dots2_btn = None
    self._overlaps_only = True
    self.window.set_default_size(420, 600)
    self.create_property_lists(data)
    self.finish_window()

  def add_top_widgets(self, data_key, box):
    import gtk
    if data_key == "probe" :
      hbox = gtk.HBox(False, 2)
      self.dots_btn = gtk.CheckButton("Show Probe dots")
      hbox.pack_start(self.dots_btn, False, False, 5)
      self.dots_btn.connect("toggled", self.toggle_probe_dots)
      self.dots2_btn = gtk.CheckButton("Overlaps only")
      hbox.pack_start(self.dots2_btn, False, False, 5)
      self.dots2_btn.connect("toggled", self.toggle_all_probe_dots)
      self.dots2_btn.set_active(True)
      self.toggle_probe_dots()
      box.pack_start(hbox, False, False, 0)

  def toggle_probe_dots(self, *args):
    if self.dots_btn is not None :
      show_dots = self.dots_btn.get_active()
      overlaps_only = self.dots2_btn.get_active()
      if show_dots :
        self.dots2_btn.set_sensitive(True)
      else :
        self.dots2_btn.set_sensitive(False)
      show_probe_dots(show_dots, overlaps_only)

  def toggle_all_probe_dots(self, *args):
    if self.dots2_btn is not None :
      self._overlaps_only = self.dots2_btn.get_active()
      self.toggle_probe_dots()

class rsc_todo_list_gui(coot_extension_gui):
  data_keys = ["by_res", "by_atom"]
  data_titles = ["Real-space correlation by residue",
                 "Real-space correlation by atom"]
  data_names = {}
  data_types = {}

class residue_properties_list(object):
  def __init__(self, columns, column_types, rows, box,
      default_size=(380,200)):
    assert len(columns) == (len(column_types) - 1)
    if (len(rows) > 0) and (len(rows[0]) != len(column_types)):
      raise RuntimeError("Wrong number of rows:\n%s" % str(rows[0]))
    import gtk
    self.liststore = gtk.ListStore(*column_types)
    self.listmodel = gtk.TreeModelSort(self.liststore)
    self.listctrl = gtk.TreeView(self.listmodel)
    self.listctrl.column = [None]*len(columns)
    self.listctrl.cell = [None]*len(columns)
    for i, column_label in enumerate(columns):
      cell = gtk.CellRendererText()
      column = gtk.TreeViewColumn(column_label)
      self.listctrl.append_column(column)
      column.set_sort_column_id(i)
      column.pack_start(cell, True)
      column.set_attributes(cell, text=i)
    self.listctrl.get_selection().set_mode(gtk.SELECTION_SINGLE)
    for row in rows :
      self.listmodel.get_model().append(row)
    self.listctrl.connect("cursor-changed", self.OnChange)
    sw = gtk.ScrolledWindow()
    w, h = default_size
    if len(rows) > 10 :
      sw.set_size_request(w, h)
    else :
      sw.set_size_request(w, 30 + (20 * len(rows)))
    sw.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
    box.pack_start(sw, False, False, 5)
    inside_vbox = gtk.VBox(False, 0)
    sw.add(self.listctrl)

  def OnChange(self, treeview):
    import coot # import dependency
    selection = self.listctrl.get_selection()
    (model, tree_iter) = selection.get_selected()
    if tree_iter is not None :
      row = model[tree_iter]
      xyz = row[-1]
      if isinstance(xyz, tuple) and len(xyz) == 3 :
        set_rotation_centre(*xyz)
        set_zoom(30)
        graphics_draw()

def show_probe_dots(show_dots, overlaps_only):
  import coot # import dependency
  n_objects = number_of_generic_objects()
  sys.stdout.flush()
  if show_dots :
    for object_number in range(n_objects):
      obj_name = generic_object_name(object_number)
      if overlaps_only and not obj_name in ["small overlap", "bad overlap"] :
        sys.stdout.flush()
        set_display_generic_object(object_number, 0)
      else :
        set_display_generic_object(object_number, 1)
  else :
    sys.stdout.flush()
    for object_number in range(n_objects):
      set_display_generic_object(object_number, 0)

def load_pkl(file_name):
  pkl = open(file_name, "rb")
  data = pickle.load(pkl)
  pkl.close()
  return data

data = {}
data['rama'] = [('A', ' 154 ', 'TYR', 0.019254372911985933, (10.289000000000001, -11.546, -9.318))]
data['omega'] = []
data['rota'] = [('A', '  22 ', 'CYS', 0.19551822033880914, (8.825, -14.677, 25.795)), ('A', '  72 ', 'ASN', 0.019328883808229, (-2.600999999999999, -22.14999999999999, 15.387)), ('A', ' 137 ', 'LYS', 0.2744049127390801, (7.795, 6.843, 9.035)), ('A', ' 279 ', 'ARG', 0.0, (-1.8109999999999993, 22.945999999999998, -7.267))]
data['cbeta'] = []
data['probe'] = [(' A 279 AARG  HG2', ' A 279 AARG HH11', -1.064, (-3.092, 24.89, -9.748)), (' A 279 AARG  CG ', ' A 279 AARG HH11', -0.984, (-2.194, 24.551, -9.517)), (' A 279 AARG  HG2', ' A 279 AARG  NH1', -0.908, (-3.105, 24.209, -10.375)), (' A 110  GLN  HG3', ' A 702  HOH  O  ', -0.868, (19.405, 0.871, -1.671)), (' A 401  DMS  H13', ' A 688  HOH  O  ', -0.84, (9.257, -25.66, 21.354)), (' A 240 BGLU  OE1', ' A 501  HOH  O  ', -0.817, (19.872, 10.95, -1.766)), (' A  58  LEU HD22', ' A  82 AMET  HE3', -0.777, (20.469, -13.03, 23.248)), (' A 279 AARG  CG ', ' A 279 AARG  NH1', -0.659, (-1.814, 23.871, -9.75)), (' A 221  ASN HD21', ' A 267  SER  HA ', -0.638, (11.672, 23.852, -13.097)), (' A 298  ARG  HG3', ' A 303  VAL  HB ', -0.614, (8.137, -3.357, -11.842)), (' A 221  ASN  ND2', ' A 267  SER  HA ', -0.611, (10.867, 24.253, -13.434)), (' A  41  HIS  HE1', ' A 164  HIS  O  ', -0.594, (10.932, -2.901, 18.96)), (' A 404  LWA  O  ', ' A 502  HOH  O  ', -0.592, (25.627, 4.689, 15.176)), (' A  70  ALA  O  ', ' A  73 AVAL HG12', -0.589, (1.011, -22.647, 12.648)), (' A 188  ARG  HG2', ' A 190  THR HG23', -0.567, (17.624, 3.498, 26.482)), (' A  54  TYR  HB3', ' A  82 AMET  HE1', -0.564, (20.321, -9.835, 24.012)), (' A 236  LYS  HD3', ' A 859  HOH  O  ', -0.564, (17.726, 28.916, -1.805)), (' A 217  ARG  NH2', ' A 503  HOH  O  ', -0.554, (2.784, 14.176, -21.316)), (' A 118  TYR  CE1', ' A 144  SER  HB3', -0.552, (1.612, -3.633, 15.293)), (' A  19  GLN HE21', ' A 119  ASN  HB3', -0.552, (-0.28, -13.065, 18.172)), (' A  67  LEU HD11', ' A 402  DMS  H12', -0.547, (5.241, -20.408, 27.327)), (' A  40  ARG  HA ', ' A  87  LEU  HG ', -0.541, (16.508, -11.352, 20.524)), (' A 197  ASP  HA ', ' A 578  HOH  O  ', -0.526, (15.49, 12.734, 7.016)), (' A  19  GLN  NE2', ' A 119  ASN  HB3', -0.521, (-0.197, -13.587, 18.561)), (' A 115  LEU HD11', ' A 122  PRO  HB3', -0.497, (0.296, -8.777, 6.119)), (' A  40  ARG  HB2', ' A  82 AMET  HE2', -0.487, (18.931, -10.105, 22.076)), (' A  41  HIS  CE1', ' A 164  HIS  O  ', -0.485, (11.635, -3.028, 19.652)), (' A  95  ASN  HB3', ' A  98  THR  OG1', -0.476, (10.243, -21.281, 5.264)), (' A 101  TYR  HA ', ' A 157  VAL  O  ', -0.453, (14.637, -13.235, -0.452)), (' A 165 AMET  SD ', ' A 186  VAL  O  ', -0.451, (16.186, 1.761, 19.734)), (' A 109  GLY  HA2', ' A 200  ILE HD13', -0.449, (14.731, 8.116, 0.376)), (' A 286  LEU  C  ', ' A 286  LEU HD12', -0.441, (4.516, 16.425, -1.57)), (' A 249  ILE HG22', ' A 293  PRO  HG2', -0.438, (17.146, 6.917, -9.602)), (' A 132  PRO  HD2', ' A 578  HOH  O  ', -0.438, (15.849, 11.631, 5.999)), (' A  72  ASN  H  ', ' A  72  ASN HD22', -0.432, (-2.553, -22.598, 13.218)), (' A  60 BARG  HA ', ' A  60 BARG  HD3', -0.429, (18.651, -16.925, 33.782)), (' A 279 AARG  NH1', ' A 532  HOH  O  ', -0.428, (-2.872, 21.95, -10.06)), (' A 404  LWA  C6 ', ' A 502  HOH  O  ', -0.426, (26.082, 5.192, 14.997)), (' A 288 BGLU  HG2', ' A 291  PHE  CE2', -0.423, (5.163, 9.077, -4.37)), (' A  65  ASN  HA ', ' A 402  DMS  O  ', -0.422, (8.903, -20.177, 28.034)), (' A 137 ALYS  NZ ', ' A 537  HOH  O  ', -0.42, (6.39, 10.632, 10.846)), (' A 127  GLN  NE2', ' A 535  HOH  O  ', -0.417, (9.352, 0.045, -2.81)), (' A 134  PHE  CE1', ' A 404  LWA  C7 ', -0.413, (22.441, 3.707, 7.288)), (' A  19  GLN HE21', ' A 119  ASN  CB ', -0.411, (-0.116, -12.684, 18.379)), (' A  52  PRO  HD2', ' A 188  ARG  HG3', -0.41, (18.172, 0.121, 27.46)), (' A 137 BLYS  NZ ', ' A 197  ASP  OD2', -0.41, (10.269, 12.283, 7.601)), (' A 117 BCYS  SG ', ' A 120  GLY  C  ', -0.409, (1.434, -11.951, 12.421)), (' A  67  LEU HD21', ' A 402  DMS  H23', -0.407, (6.299, -21.992, 26.45)), (' A 113  SER  O  ', ' A 149  GLY  HA2', -0.404, (8.705, -4.173, 4.137)), (' A  21  THR  HB ', ' A  67  LEU  HB2', -0.4, (4.832, -17.451, 22.967))]
handle_read_draw_probe_dots_unformatted("molprobity_probe.txt", 0, 0)
show_probe_dots(True, True)
gui = coot_molprobity_todo_list_gui(data=data)
