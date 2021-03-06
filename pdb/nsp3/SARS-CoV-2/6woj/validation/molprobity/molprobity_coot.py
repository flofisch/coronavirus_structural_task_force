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
data['rama'] = [('B', ' 170 ', 'GLU', 0.003254257312059141, (28.31, 20.691, 10.186)), ('B', ' 171 ', 'MET', 0.006365512089758621, (31.908, 21.022, 8.842)), ('C', ' 170 ', 'GLU', 0.01646116821474092, (57.740000000000016, -17.618, -10.094))]
data['omega'] = []
data['rota'] = [('A', '   5 ', 'SER', 0.005359990245779045, (22.62900000000001, 19.746999999999996, 55.139)), ('A', ' 122 ', 'LEU', 0.022186181369244044, (19.946, 16.773, 44.546)), ('B', '   7 ', 'SER', 0.10937827822687149, (29.771000000000008, 8.155, -11.497)), ('B', ' 122 ', 'LEU', 0.010742558212136237, (36.426, 0.707, -2.547)), ('C', '   5 ', 'SER', 0.043549730621867656, (63.665, -0.17299999999999993, 13.215)), ('C', ' 114 ', 'GLU', 0.09190884613321933, (70.95200000000003, 2.019, -9.053)), ('C', ' 122 ', 'LEU', 0.18340331642702667, (66.424, 2.594, 2.476)), ('D', '   5 ', 'SER', 0.22176155828781138, (52.505, 15.748000000000001, 28.745)), ('D', '  14 ', 'ASP', 0.11157548204520551, (46.92200000000001, 4.999, 40.804)), ('D', '  22 ', 'ASP', 0.013144479905782797, (64.47000000000003, 19.019, 38.303)), ('D', ' 122 ', 'LEU', 0.14185263240535, (49.919, 18.758, 39.38))]
data['cbeta'] = []
data['probe'] = [(' B 171  MET  HE1', ' B 312  HOH  O  ', -0.691, (35.127, 19.414, 2.883)), (' D 100  VAL HG22', ' D 132  PHE  O  ', -0.584, (61.122, 20.549, 58.186)), (' A  80  SER  HA ', ' A  94  HIS  O  ', -0.556, (19.652, 7.772, 34.596)), (' C 169  LEU  O  ', ' C 171  MET  N  ', -0.554, (59.184, -17.996, -8.931)), (' A 100  VAL HG22', ' A 132  PHE  O  ', -0.528, (31.894, 14.326, 25.121)), (' C 114  GLU  HG2', ' C 303  HOH  O  ', -0.524, (74.132, 0.49, -9.617)), (' D  43  LEU  HB3', ' D  65  SER  HB3', -0.524, (54.754, 35.069, 47.156)), (' D 169  LEU  C  ', ' D 171  MET  H  ', -0.512, (57.323, -1.574, 50.231)), (' D 106  ILE HG22', ' D 336  HOH  O  ', -0.497, (55.002, 17.372, 64.009)), (' B 122  LEU  N  ', ' B 122  LEU HD12', -0.472, (38.125, 1.886, -2.12)), (' D 159  ASN  ND2', ' D 306  HOH  O  ', -0.466, (73.406, 11.9, 45.137)), (' D  80  SER  HA ', ' D  94  HIS  O  ', -0.456, (49.158, 27.596, 49.103)), (' B 163  LYS  CG ', ' B 415  HOH  O  ', -0.451, (19.519, 11.573, 10.094)), (' C 166  SER  O  ', ' C 301  HOH  O  ', -0.447, (53.576, -16.639, -8.411)), (' D 121  VAL  HA ', ' D 150  ASN  O  ', -0.429, (47.44, 15.916, 38.891)), (' D  43  LEU  CB ', ' D  65  SER  HB3', -0.426, (54.451, 35.025, 47.961)), (' A  20  ASN  HA ', ' A 155  VAL  O  ', -0.423, (34.554, 22.378, 43.404)), (' C   9  TYR  CD1', ' C  19  LYS  HB2', -0.42, (58.163, -4.807, 5.025)), (' B  20  ASN  HA ', ' B 155  VAL  O  ', -0.416, (21.953, 6.691, -1.668)), (' C  80  SER  HA ', ' C  94  HIS  O  ', -0.414, (66.832, 11.385, -7.288)), (' D 119  HIS  O  ', ' D 149  THR HG21', -0.414, (43.409, 17.378, 41.785)), (' C 100  VAL HG22', ' C 132  PHE  O  ', -0.414, (54.806, 4.193, -16.819)), (' A  46  GLY  O  ', ' A  51  GLY  HA3', -0.413, (34.863, 5.373, 37.905)), (' D  11  LYS  CD ', ' D 367  HOH  O  ', -0.411, (48.882, 3.002, 38.438)), (' B 170  GLU  C  ', ' B 172  LYS  H  ', -0.409, (30.331, 22.124, 10.235)), (' B   9  TYR  CD1', ' B  19  LYS  HB2', -0.406, (27.949, 8.175, -5.063)), (' A 122  LEU  N  ', ' A 122  LEU HD12', -0.405, (18.416, 17.973, 43.968)), (' B 121  VAL  HA ', ' B 150  ASN  O  ', -0.4, (38.701, 3.918, -2.724))]
handle_read_draw_probe_dots_unformatted("molprobity_probe.txt", 0, 0)
show_probe_dots(True, True)
gui = coot_molprobity_todo_list_gui(data=data)
