

DBPath = "/mnt/NAS_QData/Stas/omnik.sqlite"

import model
model.make_db(DBPath)
import sys
from OmnikDataLogger import OmnikExport
omnik_exporter = OmnikExport.OmnikExport('config.cfg')
omnik_exporter.run()


