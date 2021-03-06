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
data['rama'] = []
data['omega'] = [('A', ' 153 ', 'HIS', None, (30.371000000000002, 9.347999999999999, 43.946999999999996)), ('A', ' 163 ', 'PRO', None, (41.602, 18.457, 47.09299999999999)), ('A', ' 438 ', 'GLY', None, (66.405, 30.119999999999997, 24.112999999999992))]
data['rota'] = [('A', '  86 ', 'MET', 0.0006421240627430862, (28.109999999999992, 40.909, 68.256)), ('A', ' 112 ', 'ILE', 0.11419374007049016, (41.358, 62.84599999999998, 59.902999999999984)), ('A', ' 117 ', 'LYS', 0.021859430668900597, (34.112999999999985, 59.437999999999995, 56.725999999999985)), ('A', ' 155 ', 'GLN', 0.008645213658939912, (28.470000000000002, 3.111999999999999, 46.722999999999985)), ('A', ' 240 ', 'LEU', 0.032146885637742276, (41.232, 43.202000000000005, 25.634)), ('A', ' 243 ', 'LEU', 0.17921734115801846, (43.233, 39.258, 22.303)), ('A', ' 303 ', 'GLU', 0.049807454370203105, (56.89999999999999, 16.369, 38.447999999999986)), ('A', ' 308 ', 'GLN', 0.21589790950579776, (63.084, 17.711999999999996, 43.853)), ('A', ' 363 ', 'LYS', 0.12234928108603361, (53.03699999999999, 41.636999999999986, 64.355)), ('A', ' 375 ', 'LEU', 0.0034760494848433726, (53.193, 25.712, 39.649)), ('A', ' 390 ', 'TYR', 0.29804282696648093, (50.92399999999998, 44.93999999999998, 52.027)), ('A', ' 394 ', 'TYR', 0.16012736777399103, (51.054999999999986, 49.76999999999999, 56.12399999999999)), ('A', ' 463 ', 'LEU', 0.06259529891546538, (31.498000000000008, 38.95, 34.597)), ('A', ' 537 ', 'LEU', 0.031053430640500153, (59.05899999999998, 47.98899999999998, 37.613)), ('A', ' 613 ', 'LYS', 0.04474929546321287, (35.194, 33.103, 12.798))]
data['cbeta'] = [('A', ' 486 ', 'TRP', ' ', 0.2647136753962532, (23.814999999999998, 30.645999999999994, 31.564999999999994))]
data['probe'] = [(' A 304  ALA  O  ', ' A 308  GLN  HG3', -0.891, (61.619, 19.768, 41.391)), (' A 463  LEU  C  ', ' A 463  LEU HD23', -0.817, (30.104, 37.985, 35.376)), (' A 104  VAL HG11', ' A 117  LYS  HG3', -0.743, (33.911, 62.358, 55.027)), (' A 304  ALA  O  ', ' A 308  GLN  CG ', -0.711, (62.208, 18.951, 40.842)), (' A 584  GLN  HB2', ' A 585  PRO  HD2', -0.658, (49.378, 58.725, 33.804)), (' A 463  LEU  O  ', ' A 463  LEU HD23', -0.63, (29.841, 38.104, 35.864)), (' A 462  TYR  O  ', ' A 466  GLN  HG2', -0.599, (31.138, 42.234, 34.519)), (' A 104  VAL  CG1', ' A 113  LYS  HG3', -0.589, (35.793, 64.785, 55.693)), (' A 348  ARG  HD3', ' A1624  NAG  H82', -0.574, (42.885, 21.53, 64.794)), (' A 584  GLN  HB2', ' A 585  PRO  CD ', -0.559, (49.384, 59.18, 34.625)), (' A  96  GLY  HA3', ' A 122  LEU  CD2', -0.548, (29.178, 53.269, 62.742)), (' A  98  GLN  HA ', ' A 101  LYS  HE2', -0.54, (29.241, 60.468, 67.405)), (' A 104  VAL HG13', ' A 113  LYS  HG3', -0.533, (36.074, 64.556, 56.296)), (' A 511  LYS  O  ', ' A 515  PRO  HD2', -0.53, (30.542, 31.2, 45.416)), (' A 578  MET  HG3', ' A 584  GLN  O  ', -0.527, (49.325, 55.309, 37.56)), (' A  52  ASP  O  ', ' A  56  GLN  HG3', -0.513, (43.358, 50.755, 66.897)), (' A  82  LEU  HA ', ' A  85  ASN HD22', -0.501, (28.703, 35.695, 64.243)), (' A 299  MET  HB2', ' A 433  LEU HD23', -0.485, (60.042, 22.73, 32.371)), (' A 463  LEU  C  ', ' A 463  LEU  CD2', -0.485, (30.749, 37.169, 35.623)), (' A 457  PHE  CE2', ' A 461  SER  HB3', -0.463, (39.264, 37.746, 36.994)), (' A  69 BTYR  CE1', ' A  78  SER  OG ', -0.462, (30.978, 26.943, 62.661)), (' A  96  GLY  HA3', ' A 122  LEU HD21', -0.454, (28.576, 53.687, 62.967)), (' A 116  ILE  O  ', ' A 120  GLN  HG3', -0.452, (32.382, 58.815, 59.542)), (' A 488  LEU HD22', ' A 492  TYR  HE1', -0.443, (27.525, 40.5, 31.478)), (' A 223  MET  HE1', ' A 519  PRO  HG2', -0.438, (34.193, 44.225, 47.844)), (' A 189  ALA  O  ', ' A 193  ILE HG12', -0.432, (26.113, 25.773, 47.169)), (' A 118  LYS  NZ ', ' A 403  GLU  OE2', -0.431, (38.763, 50.788, 55.582)), (' A 243  LEU HD13', ' A 600  LEU  HB2', -0.426, (46.974, 39.481, 21.395)), (' A 353  HIS  HD2', ' A2180  HOH  O  ', -0.422, (39.732, 32.442, 49.828)), (' A 476  ILE HG12', ' A 484  GLU  HG3', -0.422, (19.404, 38.898, 35.594)), (' A 455  ILE HD13', ' A 592  MET  HE2', -0.418, (45.456, 39.228, 29.191)), (' A 539  GLN  HB3', ' A 539  GLN HE21', -0.417, (60.056, 51.809, 34.257)), (' A 562  LEU  HB3', ' A 566  MET  HE2', -0.415, (55.606, 46.938, 46.718)), (' A  82  LEU  O  ', ' A  85  ASN  HB2', -0.415, (28.523, 37.077, 66.415)), (' A 507  ASP  N  ', ' A 508  PRO  CD ', -0.409, (24.54, 29.583, 39.761)), (' A 437  GLY  HA2', ' A 438  GLY  HA2', -0.401, (64.193, 31.189, 24.812))]
handle_read_draw_probe_dots_unformatted("molprobity_probe.txt", 0, 0)
show_probe_dots(True, True)
gui = coot_molprobity_todo_list_gui(data=data)
